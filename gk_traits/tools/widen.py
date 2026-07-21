#!/usr/bin/env python3
"""Regenerate / audit the vanilla trait-gate widening overwrites.

Five files in common/traits/ (04_, 09_, 15_, 16_, 17_) shadow their vanilla
namesakes. They must stay byte-identical to CURRENT vanilla EXCEPT for the
portrait-gate widening recorded in tools/widen_spec.json, and every widened
line carries a `# gk_widen:` marker.

    python3 tools/widen.py --regen   rewrite the overwrites from current vanilla + spec
    python3 tools/widen.py --check   assert each overwrite == current vanilla + spec

--check is the drift guard: if it reports DRIFT, vanilla changed something we are
silently shadowing. The printed diff IS the vanilla change to review; --regen ports
it (re-sync), then re-inspect the marked lines.
"""
from __future__ import annotations
import argparse, difflib, json, re, sys
from pathlib import Path

VANILLA = Path.home() / ".local/share/Steam/steamapps/common/Stellaris"
VTRAITS = VANILLA / "common/traits"
MOD = Path(__file__).resolve().parent.parent
MTRAITS = MOD / "common/traits"
SPEC = json.loads((MOD / "tools/widen_spec.json").read_text())
SENTINEL = "# === gk header ends; below is current vanilla + lines marked '# gk_widen:' ==="


def vanilla_version() -> str:
    try:
        return json.loads((VANILLA / "launcher-settings.json").read_text()).get("rawVersion", "?")
    except Exception:
        return "?"


def _match_braces(text: str, open_pos: int) -> int:
    """Return index just past the '}' that closes the '{' at open_pos."""
    depth, i = 0, open_pos
    while i < len(text):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return len(text)


def block_span(text: str, tid: str):
    m = re.search(r"(?m)^" + re.escape(tid) + r"\s*=\s*\{", text)
    if not m:
        return None
    return m.start(), _match_braces(text, m.end() - 1)


def field_span(block: str, field: str):
    m = re.search(field + r"\s*=\s*\{", block)
    if not m:
        return None
    return m.start(), _match_braces(block, m.end() - 1)


def field_tokens(block: str, field: str):
    fs = field_span(block, field)
    if not fs:
        return None
    inner = block[fs[0]:fs[1]]
    return inner[inner.index("{") + 1: inner.rindex("}")].split()


def widen_block(block: str, additions: list[str]) -> str:
    existing = field_tokens(block, "portrait_override") or []
    merged = sorted(set(existing) | set(additions))
    line = "\tportrait_override = { " + " ".join(merged) + " } # gk_widen: +" + " +".join(sorted(additions))
    fs = field_span(block, "portrait_override")
    if fs:  # replace the physical line(s) the vanilla portrait_override occupies
        lstart = block.rfind("\n", 0, fs[0]) + 1
        lend = block.find("\n", fs[1])
        lend = len(block) if lend < 0 else lend
        return block[:lstart] + line + block[lend:]
    # insert: after species_class, else after allowed_archetypes, else at block top
    anchor = field_span(block, "species_class") or field_span(block, "allowed_archetypes")
    pos = block.find("\n", anchor[1]) + 1 if anchor else block.find("{") + 1
    return block[:pos] + line + "\n" + block[pos:]


def generate_body(vtext: str, fspec: dict) -> str:
    edits = []
    for tid, e in fspec.items():
        if "portrait_override" not in e:
            continue
        span = block_span(vtext, tid)
        if span is None:
            print(f"  WARN: {tid} absent from vanilla — skipped", file=sys.stderr)
            continue
        edits.append((span[0], span[1], e["portrait_override"]))
    for start, end, adds in sorted(edits, reverse=True):  # end-to-start keeps spans valid
        vtext = vtext[:start] + widen_block(vtext[start:end], adds) + vtext[end:]
    return vtext


def header(fname: str, fspec: dict, version: str) -> str:
    return "\n".join([
        f"# OVERWRITE of vanilla common/traits/{fname}",
        "# Purpose: widen phenotype trait gates (portrait_override) so gk cross-classified",
        "# portraits can take these vanilla traits. The ONLY intended deviation from vanilla",
        "# is each line marked '# gk_widen:'. Grep that tag to see every change.",
        f"# Synced against vanilla {version}. Re-sync: python3 tools/widen.py --regen",
        f"# Widened: {' '.join(sorted(fspec))}",
        SENTINEL, "",
    ])


def body_after_sentinel(text: str) -> str:
    i = text.find(SENTINEL)
    return text[text.find("\n", i) + 1:] if i >= 0 else text


def cmd_regen() -> int:
    ver = vanilla_version()
    for f, fspec in SPEC.items():
        vtext = (VTRAITS / f).read_text(encoding="utf-8", errors="replace")
        (MTRAITS / f).write_text(header(f, fspec, ver) + generate_body(vtext, fspec), encoding="utf-8")
        print(f"regen {f}: {len(fspec)} traits widened")
    return 0


def cmd_check() -> int:
    drift = 0
    for f, fspec in SPEC.items():
        vtext = (VTRAITS / f).read_text(encoding="utf-8", errors="replace")
        expected = generate_body(vtext, fspec).strip()
        committed = body_after_sentinel((MTRAITS / f).read_text(encoding="utf-8", errors="replace")).strip()
        if committed == expected:
            print(f"OK    {f}")
            continue
        drift += 1
        print(f"DRIFT {f}: overwrite != current vanilla + spec (vanilla changed, or hand-edited)")
        for line in list(difflib.unified_diff(
                expected.splitlines(), committed.splitlines(),
                "vanilla+spec", "committed", lineterm=""))[:60]:
            print("   " + line)
    print(f"\nvanilla {vanilla_version()} — {'clean' if not drift else str(drift)+' file(s) drifted'}")
    return 1 if drift else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--regen", action="store_true")
    g.add_argument("--check", action="store_true")
    args = ap.parse_args()
    sys.exit(cmd_regen() if args.regen else cmd_check())
