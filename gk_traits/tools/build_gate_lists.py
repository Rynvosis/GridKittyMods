#!/usr/bin/env python3
"""Read PORTRAIT_MAPPING CSV and drive gk_traits gate widening / crosslisting.

Source of truth: the user's Google Sheet, exported as
~/Downloads/PORTRAIT_MAPPING - PORTRAIT_MAPPING.csv (configurable).

Modes:
    (default --print)   per-category portrait lists to stdout. Copy the
                        relevant block into the portrait_override of any
                        trait in gk_traits_cyber_synth.txt / gk_traits_biogenesis.txt
                        / gk_traits_common.txt when the sheet changes.
    --widen-vanilla F   read a vanilla trait file, print proposed widening
                        additions per trait (no edits)
    --patch-vanilla F   in-place patch a copy-of-vanilla trait file in our mod
                        adding sheet-derived portraits to each phenotype-gated
                        trait's portrait_override. Refuses to remove DLC lines.
    --list-crosslists   parse the sheet's Notes column for 'Also moving into X'
                        entries and emit a structured table to stdout
    --emit-crosslist-sets
                        regenerate the portrait_sets file
                        common/portrait_sets/01_gk_crosslist_sets.txt
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

MOD_ROOT = Path(__file__).resolve().parent.parent
# The mod's own committed snapshot is the source of truth (the Downloads exports
# drift). Re-export the sheet over this file to update the mapping.
DEFAULT_CSV = MOD_ROOT / "PORTRAIT_MAPPING.csv"
CROSSLIST_FILE = MOD_ROOT / "common" / "portrait_sets" / "01_gk_crosslist_sets.txt"
INLINE_DIR = MOD_ROOT / "common" / "inline_scripts" / "traits"

# Phenotype + overlay tags + COMMON.
ALL_TAGS = {
    "HUM", "MAM", "REP", "AVI", "ART", "MOL", "FUN", "PLANT", "LITHOID",
    "NECROID", "AQUATIC", "TOX", "INF", "MACHINE_ROBOT",
    "CYBER", "SYNTH", "CYBER_SYNTH", "BIOGENESIS", "PSIONIC", "COMMON",
}

# Groups for marker traits. The sheet writes CYBER+SYNTH as one combined
# CYBER_SYNTH tag; older exports split them, so accept both.
GROUP_CYBSYNTH = {"CYBER", "SYNTH", "CYBER_SYNTH", "MACHINE_ROBOT"}
GROUP_BIOGEN = {"BIOGENESIS"}
GROUP_COMMON = {"COMMON"}

# Map vanilla species_class names to our sheet tags. Vanilla uses MACHINE and
# ROBOT as two separate classes; we collapse both to MACHINE_ROBOT in the sheet.
VANILLA_CLASS_TO_TAG = {
    "HUM": "HUM",
    "MAM": "MAM",
    "REP": "REP",
    "AVI": "AVI",
    "ART": "ART",
    "MOL": "MOL",
    "FUN": "FUN",
    "PLANT": "PLANT",
    "LITHOID": "LITHOID",
    "NECROID": "NECROID",
    "AQUATIC": "AQUATIC",
    "TOX": "TOX",
    "INF": "INF",
    "PSIONIC": "PSIONIC",
    "MACHINE": "MACHINE_ROBOT",
    "ROBOT": "MACHINE_ROBOT",
}

# Vanilla DLC strings + has_X triggers we must never strip when patching.
DLC_GUARD_PATTERNS = [
    re.compile(r"host_has_dlc\s*=\s*\""),
    re.compile(r"\bhas_infernals\s*="),
    re.compile(r"\bhas_lithoids\s*="),
    re.compile(r"\bhas_aquatics\s*="),
    re.compile(r"\bhas_toxoids\s*="),
    re.compile(r"\bhas_necroids\s*="),
    re.compile(r"\bhas_machine_age_dlc\s*="),
    re.compile(r"\bhas_shroud_dlc\s*="),
    re.compile(r"\bhas_biogenesis_dlc\s*="),
    re.compile(r"\bhas_stargazer_dlc\s*="),
    re.compile(r"\bhas_vipra_the_vapor_dlc\s*="),
]

# Crosslist DLC gates per source phenotype tag. Each entry is the trigger
# block that must appear in conditional_portraits randomizable / playable.
CROSSLIST_DLC_GATES = {
    "INF": ["has_infernals = yes"],
    "LITHOID": ["has_lithoids = yes"],
    "AQUATIC": ["has_aquatics = yes"],
    "TOX": ["has_toxoids = yes"],
    "NECROID": ["has_necroids = yes"],
    "PLANT": ["host_has_dlc = \"Plantoids Species Pack\""],
}

# Target-side DLC gating layered on top of source gate. If the target
# phenotype's portraits require a DLC (e.g. PLANT requires Plantoids), the
# crosslist set must also gate on it so non-DLC players don't see the option.
TARGET_DLC_GATES = {
    "INF": ["has_infernals = yes"],
    "LITHOID": ["has_lithoids = yes"],
    "AQUATIC": ["has_aquatics = yes"],
    "TOX": ["has_toxoids = yes"],
    "PLANT": ["host_has_dlc = \"Plantoids Species Pack\""],
}


# ----------------------------------------------------------------------------
# CSV loading
# ----------------------------------------------------------------------------

def find_header_row(rows: list[list[str]]) -> int:
    for idx, row in enumerate(rows):
        if row and row[0].strip() == "Internal ID":
            return idx
    raise RuntimeError("Could not find header row (expected first cell 'Internal ID')")


def load_mapping(csv_path: Path) -> list[dict]:
    with csv_path.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))
    header_idx = find_header_row(rows)
    header = [c.strip() for c in rows[header_idx]]
    col = {name: i for i, name in enumerate(header)}
    id_i = col["Internal ID"]
    a_i = col["Category A"]
    b_i = col["Category B"]
    c_i = col.get("Category C (Optional)")
    status_i = col.get("Status")
    notes_i = col.get("Notes")

    out = []
    for row in rows[header_idx + 1:]:
        if not row or not row[id_i].strip():
            continue
        pid = row[id_i].strip()
        cats = set()
        for i in (a_i, b_i, c_i):
            if i is None or i >= len(row):
                continue
            tag = row[i].strip()
            if tag:
                cats.add(tag)
        unknown = cats - ALL_TAGS
        if unknown:
            print(f"warn: portrait {pid} has unknown tag(s): {sorted(unknown)}", file=sys.stderr)
        cat_a = row[a_i].strip() if a_i < len(row) else ""
        out.append({
            "id": pid,
            "cats": cats,
            "cat_a": cat_a,
            "status": row[status_i].strip() if status_i is not None and status_i < len(row) else "",
            "notes": row[notes_i].strip() if notes_i is not None and notes_i < len(row) else "",
        })
    return out


def portraits_with(mapping: list[dict], tags: set[str]) -> list[str]:
    matched = [m["id"] for m in mapping if m["cats"] & tags]
    return sorted(set(matched))


def format_list(ids: list[str], per_line: int = 8, indent: str = "\t\t") -> str:
    lines = []
    for i in range(0, len(ids), per_line):
        lines.append(indent + " ".join(ids[i:i + per_line]))
    return "\n".join(lines)


# ----------------------------------------------------------------------------
# Modes: --print, --patch-markers (existing)
# ----------------------------------------------------------------------------

def cmd_print(mapping: list[dict]) -> None:
    groups = [
        ("CYBSYNTH (CYBER + SYNTH + MACHINE_ROBOT)", GROUP_CYBSYNTH),
        ("BIOGEN (BIOGENESIS)", GROUP_BIOGEN),
        ("COMMON", GROUP_COMMON),
    ]
    for label, tags in groups:
        ids = portraits_with(mapping, tags)
        print(f"\n# {label} -- {len(ids)} portraits")
        print("portrait_override = {")
        print(format_list(ids))
        print("}")

    print("\n\n# === Per-tag portrait counts ===")
    for tag in sorted(ALL_TAGS):
        ids = portraits_with(mapping, {tag})
        print(f"{tag:>16}: {len(ids):3d} portraits")


# ----------------------------------------------------------------------------
# Gate inline files: the three portrait_override lists the trait suite inlines.
# ----------------------------------------------------------------------------

GATE_FILES = {
    "gk_portraits_cyber.txt": GROUP_CYBSYNTH,
    "gk_portraits_biogen.txt": GROUP_BIOGEN,
    "gk_portraits_common.txt": GROUP_COMMON,
}

TRAITS_DIR = MOD_ROOT / "common" / "traits"

# Traits that write a gate list longhand + trait-specific extras (a whole-statement
# inline can't be appended to). --check-gates verifies they equal group + extras.
GATE_EXTRAS = {
    "trait_gk_hosts": (GROUP_BIOGEN, ["mol2", "fun4", "fun16"], "gk_traits_cyberbio_positive.txt"),
    "trait_gk_polycephalous": (GROUP_BIOGEN, ["mol16", "lith6", "aqu7", "tox3"], "gk_traits_cyberbio_positive.txt"),
}


def trait_portrait_override(fname: str, tid: str) -> list[str]:
    text = (TRAITS_DIR / fname).read_text(encoding="utf-8")
    m = re.search(r"(?ms)^" + re.escape(tid) + r"\s*=\s*\{.*?portrait_override\s*=\s*\{([^}]*)\}", text)
    return sorted(m.group(1).split()) if m else []


def render_gate(ids: list[str]) -> str:
    return "portrait_override = {\n" + format_list(ids, per_line=8, indent="\t") + "\n}\n"


def write_trait_override(fname: str, tid: str, ids: list[str]) -> bool:
    """Rewrite one trait's longhand portrait_override in place."""
    path = TRAITS_DIR / fname
    text = path.read_text(encoding="utf-8")
    pat = re.compile(r"(?ms)(^" + re.escape(tid) + r"\s*=\s*\{.*?portrait_override\s*=\s*\{)([^}]*)(\})")
    m = pat.search(text)
    if not m:
        return False
    block = "\n" + format_list(ids, per_line=8, indent="\t\t") + "\n\t"
    path.write_text(text[:m.start(2)] + block + text[m.end(2):], encoding="utf-8")
    return True


def cmd_write_gates(mapping: list[dict]) -> None:
    for fn, tags in GATE_FILES.items():
        ids = portraits_with(mapping, tags)
        (INLINE_DIR / fn).write_text(render_gate(ids), encoding="utf-8")
        print(f"wrote {fn}: {len(ids)} portraits")
    for tid, (group, extras, fname) in GATE_EXTRAS.items():
        ids = sorted(set(portraits_with(mapping, group)) | set(extras))
        ok = write_trait_override(fname, tid, ids)
        print(f"wrote {tid}: {len(ids)} portraits" if ok else f"FAILED {tid}: block not found")


def cmd_check_gates(mapping: list[dict]) -> None:
    bad = 0
    for fn, tags in GATE_FILES.items():
        expected = portraits_with(mapping, tags)
        text = (INLINE_DIR / fn).read_text(encoding="utf-8")
        actual = sorted(text[text.index("{") + 1: text.rindex("}")].split())
        if actual == expected:
            print(f"OK    {fn}: {len(expected)} portraits")
            continue
        bad += 1
        exp, act = set(expected), set(actual)
        print(f"DRIFT {fn}: +{sorted(exp - act) or 'none'}  -{sorted(act - exp) or 'none'}")

    for tid, (group, extras, fname) in GATE_EXTRAS.items():
        expected = sorted(set(portraits_with(mapping, group)) | set(extras))
        actual = trait_portrait_override(fname, tid)
        if actual == expected:
            print(f"OK    {tid} (biogen + extras)")
            continue
        bad += 1
        exp, act = set(expected), set(actual)
        print(f"DRIFT {tid}: +{sorted(exp - act) or 'none'}  -{sorted(act - exp) or 'none'}")
    sys.exit(1 if bad else 0)


# ----------------------------------------------------------------------------
# Trait-file parsing (line-based; relies on vanilla single-line conventions)
# ----------------------------------------------------------------------------

GENERIC_BRACES_RE = re.compile(r"[{}]")
TRAIT_START_RE = re.compile(r"^(\s*)(trait_\w+)\s*=\s*\{")
SPECIES_CLASS_LINE_RE = re.compile(
    r"^(\s*)species_class\s*=\s*\{([^}]*)\}"
)
PORTRAIT_OVERRIDE_LINE_RE = re.compile(
    r"^(\s*)portrait_override\s*=\s*\{([^}]*)\}"
)


def strip_inline_comment(line: str) -> str:
    """Remove # comments from a line for brace-counting purposes."""
    # Naive: split on # not inside a string. Stellaris uses # for comments.
    idx = line.find("#")
    return line if idx < 0 else line[:idx]


def parse_trait_file(text: str) -> list[dict]:
    """Return list of trait dicts with metadata:
        name, header_line_idx, end_line_idx,
        species_class_line_idx, species_class_set,
        portrait_override_line_idx, portrait_override_set
    Line indices are 0-based.
    """
    lines = text.splitlines()
    traits = []
    current: dict | None = None
    depth = 0  # global brace depth

    for i, line in enumerate(lines):
        code = strip_inline_comment(line)

        # If at depth 0 and not in a trait, look for a trait start.
        if current is None and depth == 0:
            m = TRAIT_START_RE.match(code)
            if m:
                current = {
                    "name": m.group(2),
                    "indent": m.group(1),
                    "header_line_idx": i,
                    "end_line_idx": None,
                    "species_class_line_idx": None,
                    "species_class_set": None,
                    "portrait_override_line_idx": None,
                    "portrait_override_set": None,
                }
                # Count braces on this line
                depth += code.count("{") - code.count("}")
                continue

        if current is not None:
            # Detect species_class single-line
            m_sc = SPECIES_CLASS_LINE_RE.match(code)
            if m_sc and depth == 1 and current["species_class_line_idx"] is None:
                tokens = m_sc.group(2).split()
                current["species_class_line_idx"] = i
                current["species_class_set"] = tokens

            # Detect portrait_override single-line
            m_po = PORTRAIT_OVERRIDE_LINE_RE.match(code)
            if m_po and depth == 1 and current["portrait_override_line_idx"] is None:
                tokens = m_po.group(2).split()
                current["portrait_override_line_idx"] = i
                current["portrait_override_set"] = tokens

            # Update depth for this line
            depth += code.count("{") - code.count("}")

            if depth == 0:
                current["end_line_idx"] = i
                traits.append(current)
                current = None

    return traits


def compute_widening_additions(
    species_class_tokens: list[str],
    existing_override: list[str],
    mapping: list[dict],
) -> list[str]:
    """For a trait's species_class set, return portraits to ADD to its
    portrait_override (sorted, dedup, excluding those already present)."""
    tags = set()
    for token in species_class_tokens:
        mapped = VANILLA_CLASS_TO_TAG.get(token)
        if mapped:
            tags.add(mapped)
    if not tags:
        return []
    candidates = set(portraits_with(mapping, tags))
    return sorted(candidates - set(existing_override))


# ----------------------------------------------------------------------------
# Mode: --widen-vanilla (print only)
# ----------------------------------------------------------------------------

def cmd_widen_vanilla(mapping: list[dict], path: Path) -> None:
    if not path.exists():
        print(f"error: file not found: {path}", file=sys.stderr)
        sys.exit(1)
    text = path.read_text(encoding="utf-8-sig")
    traits = parse_trait_file(text)

    print(f"# Widening proposal for {path}")
    print(f"# {len(traits)} traits parsed; gates derived from sheet\n")
    total_widened = 0
    for t in traits:
        if not t["species_class_set"]:
            continue
        existing = t["portrait_override_set"] or []
        additions = compute_widening_additions(
            t["species_class_set"], existing, mapping
        )
        if not additions:
            continue
        total_widened += 1
        sc = " ".join(t["species_class_set"])
        ex = " ".join(existing) if existing else "(none)"
        ad = " ".join(additions)
        print(f"## {t['name']}")
        print(f"   species_class = {{ {sc} }}")
        print(f"   existing portrait_override = {{ {ex} }}")
        print(f"   additions = {{ {ad} }}")
        print()
    print(f"# {total_widened} traits would gain new portrait_override entries")


# ----------------------------------------------------------------------------
# Mode: --patch-vanilla (in-place edit)
# ----------------------------------------------------------------------------

def assert_dlc_lines_preserved(before: list[str], after: list[str], path: Path) -> None:
    """Refuse to write the patch if any DLC-gate line was removed."""
    def count_dlc(lines: list[str]) -> int:
        n = 0
        for line in lines:
            for pat in DLC_GUARD_PATTERNS:
                if pat.search(line):
                    n += 1
                    break
        return n
    if count_dlc(after) < count_dlc(before):
        print(
            f"error: patching {path} would remove DLC-gate line(s); aborting",
            file=sys.stderr,
        )
        sys.exit(1)


def cmd_patch_vanilla(mapping: list[dict], path: Path) -> None:
    if not path.exists():
        print(f"error: file not found: {path}", file=sys.stderr)
        sys.exit(1)
    original = path.read_text(encoding="utf-8-sig")
    lines = original.splitlines()
    traits = parse_trait_file(original)

    # Build a list of edits keyed by line index.
    # Each edit is either "replace_line" or "insert_after".
    replacements: dict[int, str] = {}  # line_idx -> new line
    insertions: dict[int, str] = {}    # line_idx -> line(s) to insert AFTER

    widened_count = 0
    for t in traits:
        if not t["species_class_set"]:
            continue
        existing = t["portrait_override_set"] or []
        additions = compute_widening_additions(
            t["species_class_set"], existing, mapping
        )
        if not additions:
            continue
        widened_count += 1

        full = sorted(set(existing) | set(additions))
        new_value = " ".join(full)

        if t["portrait_override_line_idx"] is not None:
            # Replace the existing line with extended content
            old_line = lines[t["portrait_override_line_idx"]]
            indent_match = PORTRAIT_OVERRIDE_LINE_RE.match(strip_inline_comment(old_line))
            indent = indent_match.group(1) if indent_match else "\t"
            replacements[t["portrait_override_line_idx"]] = (
                f"{indent}portrait_override = {{ {new_value} }}"
            )
        else:
            # Insert after the species_class line
            sc_idx = t["species_class_line_idx"]
            sc_line = lines[sc_idx]
            indent_match = SPECIES_CLASS_LINE_RE.match(strip_inline_comment(sc_line))
            indent = indent_match.group(1) if indent_match else "\t"
            insertions[sc_idx] = (
                f"{indent}portrait_override = {{ {new_value} }}"
            )

    # Emit the new file
    out_lines = []
    for i, line in enumerate(lines):
        if i in replacements:
            out_lines.append(replacements[i])
        else:
            out_lines.append(line)
        if i in insertions:
            out_lines.append(insertions[i])

    assert_dlc_lines_preserved(lines, out_lines, path)

    new_text = "\n".join(out_lines)
    if original.endswith("\n"):
        new_text += "\n"
    path.write_text(new_text, encoding="utf-8")
    print(f"patched {widened_count} trait(s) in {path}")


# ----------------------------------------------------------------------------
# Mode: --list-crosslists and --emit-crosslist-sets
# ----------------------------------------------------------------------------

CROSSLIST_NOTE_RE = re.compile(
    r"Also moving into\s+(\S+)\s+(?:Potrait|Portrait)\s+list",
    re.IGNORECASE,
)

# Map note-target name to canonical phenotype tag.
NOTE_TARGET_TO_TAG = {
    "thermophile": "INF",
    "infernal": "INF",
    "plant": "PLANT",
    "rep": "REP",
    "reptilian": "REP",
    "art": "ART",
    "arthropoid": "ART",
    "tox": "TOX",
    "toxoid": "TOX",
    "lithoid": "LITHOID",
    "mol": "MOL",
    "molluscoid": "MOL",
    "aqu": "AQUATIC",
    "aquatic": "AQUATIC",
    "mam": "MAM",
    "mammalian": "MAM",
    "avi": "AVI",
    "avian": "AVI",
    "fun": "FUN",
    "fungoid": "FUN",
    "hum": "HUM",
    "humanoid": "HUM",
    "necroid": "NECROID",
    "nec": "NECROID",
}


def extract_crosslists(mapping: list[dict]) -> list[dict]:
    """Return one entry per portrait that has 'Also moving into X' notes.

    Each entry: {portrait, source_phenotype, target_tags, source_dlc_gate}.
    A note can list multiple target words across multi-line strings - we scan
    every match in the notes cell.
    """
    out = []
    for row in mapping:
        note = row.get("notes", "")
        if not note:
            continue
        # The Notes column may contain "Also moving into X Potrait list" and
        # also "and Y Potrait list" - check both.
        targets = set()
        for m in CROSSLIST_NOTE_RE.finditer(note):
            word = m.group(1).strip().lower()
            mapped = NOTE_TARGET_TO_TAG.get(word)
            if mapped:
                targets.add(mapped)
        if not targets:
            continue
        # Source phenotype = Cat A (the row's original phenotype as recorded
        # in the sheet). Determines which DLC gate the source portrait needs.
        source = row.get("cat_a") or None
        out.append({
            "portrait": row["id"],
            "source_phenotype": source,
            "target_tags": sorted(targets),
            "notes": note,
        })
    return out


def cmd_list_crosslists(mapping: list[dict]) -> None:
    entries = extract_crosslists(mapping)
    print(f"# {len(entries)} portraits flagged for crosslisting")
    for e in entries:
        print(
            f"  {e['portrait']:30s} "
            f"source={e['source_phenotype'] or '?':10s} "
            f"-> targets={','.join(e['target_tags'])}"
        )


def cmd_emit_crosslist_sets(mapping: list[dict]) -> None:
    entries = extract_crosslists(mapping)

    # Group by target phenotype and combined-DLC-gate (so portraits with
    # identical gates land in one bundled set).
    # Key: (target_tag, frozenset(dlc_triggers))
    buckets: dict[tuple, list[str]] = {}
    bucket_meta: dict[tuple, dict] = {}

    for e in entries:
        source = e["source_phenotype"]
        for target in e["target_tags"]:
            # Combine source-DLC gate + target-DLC gate (deduped)
            gate_lines = list(CROSSLIST_DLC_GATES.get(source, []))
            for t_line in TARGET_DLC_GATES.get(target, []):
                if t_line not in gate_lines:
                    gate_lines.append(t_line)
            key = (target, tuple(gate_lines))
            buckets.setdefault(key, []).append(e["portrait"])
            bucket_meta.setdefault(key, {
                "target": target,
                "gate_lines": gate_lines,
                "sources": set(),
            })
            bucket_meta[key]["sources"].add(source)

    # Sort keys deterministically.
    out_lines = []
    out_lines.append(
        "# Cross-listing portrait_sets for gk_traits.\n"
        "# Auto-generated by tools/build_gate_lists.py --emit-crosslist-sets.\n"
        "# Each set surfaces a portrait inside a different phenotype's empire\n"
        "# designer dropdown, gated by the appropriate DLC triggers.\n"
    )

    for key in sorted(buckets.keys(), key=lambda k: (k[0], k[1])):
        target = bucket_meta[key]["target"]
        gate_lines = bucket_meta[key]["gate_lines"]
        sources = sorted(bucket_meta[key]["sources"])
        portraits = sorted(set(buckets[key]))
        # Set name: combine source(s) -> target
        src_part = "_".join(s.lower() for s in sources) if sources else "src"
        set_name = f"gk_{src_part}_as_{target.lower()}"

        gate_block = ""
        if gate_lines:
            gate_block = "\n".join(f"\t\t\t{line}" for line in gate_lines)
            gate_block_str = f"\n{gate_block}\n\t\t"
        else:
            gate_block_str = " always = yes "

        portrait_lines = "\n".join(f"\t\t\t\"{p}\"" for p in portraits)

        block = (
            f"{set_name} = {{\n"
            f"\tspecies_class = {target}\n"
            f"\tconditional_portraits = {{\n"
            f"\t\trandomizable = {{{gate_block_str}}}\n"
            f"\t\tplayable = {{{gate_block_str}}}\n"
            f"\t\tportraits = {{\n"
            f"{portrait_lines}\n"
            f"\t\t}}\n"
            f"\t}}\n"
            f"}}\n"
        )
        out_lines.append(block)

    text = "\n".join(out_lines)
    CROSSLIST_FILE.parent.mkdir(parents=True, exist_ok=True)
    CROSSLIST_FILE.write_text(text, encoding="utf-8")
    print(f"wrote {len(buckets)} portrait_set(s) to {CROSSLIST_FILE}")


# ----------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--widen-vanilla", type=Path, metavar="PATH")
    parser.add_argument("--patch-vanilla", type=Path, metavar="PATH")
    parser.add_argument("--list-crosslists", action="store_true")
    parser.add_argument("--emit-crosslist-sets", action="store_true")
    parser.add_argument("--write-gates", action="store_true",
                        help="write the three gk_portraits_* inline files from the CSV")
    parser.add_argument("--check-gates", action="store_true",
                        help="assert the inline files match the CSV; report drift")
    args = parser.parse_args()

    if not args.csv.exists():
        print(f"error: csv not found: {args.csv}", file=sys.stderr)
        sys.exit(1)

    mapping = load_mapping(args.csv)

    if args.widen_vanilla:
        cmd_widen_vanilla(mapping, args.widen_vanilla)
    elif args.patch_vanilla:
        cmd_patch_vanilla(mapping, args.patch_vanilla)
    elif args.list_crosslists:
        cmd_list_crosslists(mapping)
    elif args.emit_crosslist_sets:
        cmd_emit_crosslist_sets(mapping)
    elif args.write_gates:
        cmd_write_gates(mapping)
    elif args.check_gates:
        cmd_check_gates(mapping)
    else:
        cmd_print(mapping)


if __name__ == "__main__":
    main()
