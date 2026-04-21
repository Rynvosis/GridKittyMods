"""Minimal Paradox-script parser/writer.

Parses .txt files (component_templates, inline_scripts) into an AST that
preserves comments and block structure. Serializes back with tab indentation.

AST node types:
    Comment(text)              # a "# ..." line
    Assign(key, value, inline) # key = value ; value is Scalar or Block
    Scalar(raw)                # anything to the right of an '=' that isn't a block
    Block(children)            # children is a list of nodes

The parser is tolerant: unknown syntax is captured as Scalar so we can round-trip
files we don't fully understand. Transforms operate on the AST without breaking
parts they don't recognize.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Union


@dataclass
class Comment:
    text: str  # includes leading '#', no trailing newline


@dataclass
class Scalar:
    raw: str  # verbatim text after '=', up to end-of-line or block boundary


@dataclass
class Block:
    children: List["Node"] = field(default_factory=list)


@dataclass
class Assign:
    key: str
    value: Union[Scalar, Block]
    op: str = "="  # '=', '>', '<', '>=', '<=' etc.


Node = Union[Comment, Assign, Block]


class ParseError(Exception):
    pass


class _Tokenizer:
    """Minimal tokenizer. Emits (kind, text) pairs.

    Kinds: 'word', 'string', 'lbrace', 'rbrace', 'op', 'comment', 'ws' (dropped).
    """

    def __init__(self, src: str) -> None:
        self.src = src
        self.i = 0

    def peek(self) -> str:
        return self.src[self.i] if self.i < len(self.src) else ""

    def eof(self) -> bool:
        return self.i >= len(self.src)

    def _skip_ws(self) -> None:
        while self.i < len(self.src) and self.src[self.i] in " \t\r\n":
            self.i += 1

    def next_token(self):
        """Return (kind, text) or (None, None) at EOF."""
        self._skip_ws()
        if self.eof():
            return None, None
        c = self.src[self.i]
        if c == "#":
            j = self.src.find("\n", self.i)
            if j == -1:
                j = len(self.src)
            tok = self.src[self.i:j]
            self.i = j
            return "comment", tok
        if c == "{":
            self.i += 1
            return "lbrace", "{"
        if c == "}":
            self.i += 1
            return "rbrace", "}"
        if c == "=":
            self.i += 1
            return "op", "="
        if c in "<>":
            # support '<', '>', '<=', '>='
            if self.i + 1 < len(self.src) and self.src[self.i + 1] == "=":
                self.i += 2
                return "op", c + "="
            self.i += 1
            return "op", c
        if c == '"':
            j = self.i + 1
            while j < len(self.src) and self.src[j] != '"':
                j += 1
            if j >= len(self.src):
                raise ParseError(f"unterminated string at offset {self.i}")
            tok = self.src[self.i:j + 1]
            self.i = j + 1
            return "string", tok
        # bare word: letters, digits, _, -, @, ., :, |, $, /, digits signs
        j = self.i
        while j < len(self.src) and self.src[j] not in " \t\r\n{}=#<>\"":
            j += 1
        tok = self.src[self.i:j]
        if not tok:
            raise ParseError(f"empty token at offset {self.i}: {self.src[self.i:self.i+20]!r}")
        self.i = j
        return "word", tok


class Parser:
    def __init__(self, src: str) -> None:
        self.tok = _Tokenizer(src)
        self._peeked = None

    def _peek(self):
        if self._peeked is None:
            self._peeked = self.tok.next_token()
        return self._peeked

    def _consume(self):
        t = self._peek()
        self._peeked = None
        return t

    def parse_top(self) -> Block:
        """Parse a whole file as a Block of children."""
        root = Block([])
        while True:
            kind, text = self._peek()
            if kind is None:
                return root
            if kind == "rbrace":
                raise ParseError(f"unexpected '}}' at top level")
            root.children.append(self._parse_node())

    def _parse_node(self) -> Node:
        kind, text = self._peek()
        if kind == "comment":
            self._consume()
            return Comment(text)
        if kind == "lbrace":
            # bare block at this level — treat as an unnamed block. rare.
            return self._parse_block()
        if kind in ("word", "string"):
            # look ahead for '=' or comparison op
            key_kind, key_text = self._consume()
            nxt_kind, nxt_text = self._peek()
            if nxt_kind == "op":
                self._consume()
                # value is either a block or a scalar (the next token)
                val_kind, val_text = self._peek()
                if val_kind == "lbrace":
                    block = self._parse_block()
                    return Assign(key_text, block, op=nxt_text)
                elif val_kind in ("word", "string"):
                    self._consume()
                    return Assign(key_text, Scalar(val_text), op=nxt_text)
                else:
                    raise ParseError(
                        f"expected value after '{key_text} {nxt_text}', got {val_kind!r}")
            # no '=' — this is a bareword list element. Treat as Assign with empty op? We
            # keep it as Scalar by promoting to key='' Assign so the writer can emit it.
            # In practice, bare word lists occur inside blocks (e.g. tags = { a b c }).
            return _BareWord(key_text)
        raise ParseError(f"unexpected token {kind!r}: {text!r}")

    def _parse_block(self) -> Block:
        kind, text = self._consume()
        assert kind == "lbrace", kind
        block = Block([])
        while True:
            nxt_kind, nxt_text = self._peek()
            if nxt_kind is None:
                raise ParseError("unexpected EOF inside block")
            if nxt_kind == "rbrace":
                self._consume()
                return block
            block.children.append(self._parse_node())


@dataclass
class _BareWord:
    """A bare token inside a block (e.g. 'weapon_type_kinetic' inside tags = {}).
    Not an Assign; we emit it as-is."""
    word: str


def parse(src: str) -> Block:
    return Parser(src).parse_top()


def parse_file(path: str) -> Block:
    with open(path, "r", encoding="utf-8-sig") as f:
        return parse(f.read())


# -----------------------------------------------------------------------------
# Writer
# -----------------------------------------------------------------------------


def write(node: Block) -> str:
    out: list[str] = []
    _write_block_children(node, out, indent=0)
    # ensure trailing newline, no leading newline
    text = "".join(out)
    if not text.endswith("\n"):
        text += "\n"
    return text


def _ind(n: int) -> str:
    return "\t" * n


def _write_block_children(block: Block, out: list, indent: int) -> None:
    for child in block.children:
        _write_node(child, out, indent)


def _write_node(node: Node, out: list, indent: int) -> None:
    if isinstance(node, Comment):
        out.append(_ind(indent) + node.text + "\n")
        return
    if isinstance(node, _BareWord):
        out.append(_ind(indent) + node.word + "\n")
        return
    if isinstance(node, Assign):
        if isinstance(node.value, Scalar):
            out.append(f"{_ind(indent)}{node.key} {node.op} {node.value.raw}\n")
        else:
            assert isinstance(node.value, Block), type(node.value)
            if not node.value.children:
                out.append(f"{_ind(indent)}{node.key} {node.op} {{}}\n")
            else:
                out.append(f"{_ind(indent)}{node.key} {node.op} {{\n")
                _write_block_children(node.value, out, indent + 1)
                out.append(f"{_ind(indent)}}}\n")
        return
    if isinstance(node, Block):
        # bare block — rare
        out.append(_ind(indent) + "{\n")
        _write_block_children(node, out, indent + 1)
        out.append(_ind(indent) + "}\n")
        return
    raise TypeError(f"unknown node type: {type(node).__name__}")


# -----------------------------------------------------------------------------
# Helpers used by transforms
# -----------------------------------------------------------------------------


def iter_assigns(block: Block):
    """Yield Assign children of a block (skipping comments, bare words)."""
    for child in block.children:
        if isinstance(child, Assign):
            yield child


def find_assign(block: Block, key: str):
    """Return the first Assign with the given key, or None."""
    for a in iter_assigns(block):
        if a.key == key:
            return a
    return None


def contains_text(node: Node, needle: str) -> bool:
    """Recursive substring scan over the serialized form of a node.

    Used for cheap heuristics like 'does this block mention country_uses_bio_ships?'.
    """
    if isinstance(node, Comment):
        return needle in node.text
    if isinstance(node, _BareWord):
        return needle in node.word
    if isinstance(node, Scalar):
        return needle in node.raw
    if isinstance(node, Assign):
        if needle in node.key:
            return True
        return contains_text(node.value, needle)
    if isinstance(node, Block):
        return any(contains_text(c, needle) for c in node.children)
    return False
