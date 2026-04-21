#!/usr/bin/env python3
"""Audit hand-written gk_lithogenesis OW files against generator output.

For each hand-written `000_flgsis_*.txt` in the mod's component_templates dir,
find the corresponding `zz_flgsis_*.txt` generator output (by matching keys),
and report:

- Keys only in hand-written — potential balance tweaks or content the generator
  missed (would need to either preserve or fix the generator).
- Keys only in generator — vanilla content the hand-written file didn't cover
  (the generator's value-add).
- Overlapping keys — where both define the same key. Hand-written is dead code
  here (generator's zz_ loads later and wins).

Use the output to decide per-file whether to delete the hand-written version
safely, or to preserve specific blocks.
"""

from __future__ import annotations

import glob
import sys
from pathlib import Path
from typing import Dict, Set

import pdxscript as p


DEFAULT_MOD = Path("/home/ryn/Projects/Stellaris/mod/gk_lithogenesis")


def keys_in(path: Path) -> Set[str]:
    """Return the set of component_template keys defined at the top level of a file."""
    try:
        ast = p.parse_file(str(path))
    except Exception as e:
        print(f"  [parse error] {path.name}: {e}", file=sys.stderr)
        return set()
    keys: Set[str] = set()
    for child in ast.children:
        if isinstance(child, p.Assign) and child.key in (
            "utility_component_template",
            "weapon_component_template",
            "strike_craft_component_template",
        ):
            if isinstance(child.value, p.Block):
                k = p.find_assign(child.value, "key")
                if k and isinstance(k.value, p.Scalar):
                    keys.add(k.value.raw.strip('"'))
    return keys


def main() -> int:
    mod = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_MOD
    ct_dir = mod / "common/component_templates"
    if not ct_dir.is_dir():
        print(f"error: {ct_dir} not found", file=sys.stderr)
        return 2

    hand_files = sorted(glob.glob(str(ct_dir / "000_flgsis_*.txt")))
    gen_files = sorted(glob.glob(str(ct_dir / "zz_flgsis_*.txt")))
    if not hand_files:
        print("no hand-written 000_flgsis_*.txt files found — nothing to audit")
        return 0

    # Collect all generator keys across all zz_flgsis_* files (any zz_ file may
    # cover any hand-written file's keys; the mapping isn't 1:1 by filename).
    gen_key_to_file: Dict[str, str] = {}
    for gf in gen_files:
        for k in keys_in(Path(gf)):
            gen_key_to_file[k] = Path(gf).name

    print(f"Generator coverage: {len(gen_key_to_file)} unique keys across {len(gen_files)} zz_flgsis_* files")
    print(f"Auditing {len(hand_files)} hand-written 000_flgsis_* file(s):\n")

    for hf in hand_files:
        hand_path = Path(hf)
        hand_keys = keys_in(hand_path)
        if not hand_keys:
            print(f"=== {hand_path.name}: no top-level component_template blocks")
            continue
        only_hand = sorted(hand_keys - gen_key_to_file.keys())
        overlap = sorted(hand_keys & gen_key_to_file.keys())
        print(f"=== {hand_path.name} ({len(hand_keys)} keys total)")
        print(f"    overlap with generator: {len(overlap)}")
        print(f"    only in hand-written:   {len(only_hand)}")
        if only_hand:
            # Show which keys — these are potentially unique content.
            for k in only_hand:
                print(f"       * {k}")
        print()

    # Generator-only coverage (keys the generator has that no hand-written file covers)
    all_hand_keys: Set[str] = set()
    for hf in hand_files:
        all_hand_keys.update(keys_in(Path(hf)))
    only_gen = sorted(gen_key_to_file.keys() - all_hand_keys)
    print(f"Keys in generator output but NOT in any hand-written file: {len(only_gen)}")
    if only_gen and len(only_gen) <= 50:
        for k in only_gen:
            print(f"    * {k}  (in {gen_key_to_file[k]})")
    elif only_gen:
        for k in only_gen[:20]:
            print(f"    * {k}  (in {gen_key_to_file[k]})")
        print(f"    ... and {len(only_gen) - 20} more")
    return 0


if __name__ == "__main__":
    sys.exit(main())
