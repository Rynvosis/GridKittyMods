#!/usr/bin/env python3
"""Copy source-mod trait icons into gk_traits, renamed to the gk trait id.

Reads the shipping CSV, resolves each row's original trait icon in its source
mod, and copies it to gfx/interface/icons/traits/<new_id>.dds so Stellaris picks
it up by the trait-id filename fallback (no `icon =` line needed).

Most source traits have no explicit `icon =` line and rely on that same fallback,
so we look for <original_id>.dds when no path is declared.

    python3 tools/steal_icons.py            # report only
    python3 tools/steal_icons.py --copy     # actually copy
"""

from __future__ import annotations

import argparse
import csv
import re
import shutil
from pathlib import Path

MOD_ROOT = Path(__file__).resolve().parent.parent
DEST = MOD_ROOT / "gfx" / "interface" / "icons" / "traits"
DEFAULT_CSV = Path.home() / "Downloads" / "shipping_traits_v3.csv"

# Source mods live in one of two places depending on whether they are still
# subscribed in Steam or were extracted by hand.
SEARCH_ROOTS = [
    Path.home() / ".local/share/Steam/steamapps/workshop/content/281990",
    Path.home() / "Downloads",
]

ICON_RE = re.compile(r'icon\s*=\s*"([^"]+)"')

# Known errors in the shipping CSV: new_id -> (original_id, mod_id).
# Remove an entry once the sheet is corrected.
OVERRIDES = {
    # sheet says trait_v_extremophiles; V_TRAITS defines it singular
    "trait_gk_extremophiles": ("trait_v_extremophile", "2872760980"),
    # sheet credits Additional Traits (681576508); the v_ prefix gives it away
    "trait_gk_gregarious": ("trait_v_pack_behaviour", "2872760980"),
}

# CSV new_id -> the id the trait actually shipped as (the icon filename must
# match the shipped id, not the sheet). Remove once the sheet is corrected.
DEST_RENAMES = {
    "trait_gk_ill-led": "trait_gk_arrested_learning",
}


def mod_root(mod_id: str) -> Path | None:
    for root in SEARCH_ROOTS:
        candidate = root / mod_id
        if (candidate / "common").is_dir():
            return candidate
    return None


def find_declared_icon(root: Path, trait_id: str) -> str | None:
    """Return the icon path declared on trait_id, if the trait declares one.

    Trait blocks are not always flush-left (Galactic Diversity indents them), so
    match the id anywhere on the line followed by `= {`.
    """
    start_re = re.compile(r"^\s*" + re.escape(trait_id) + r"\s*=\s*\{")
    for path in (root / "common" / "traits").glob("*.txt"):
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for i, line in enumerate(lines):
            if not start_re.match(line):
                continue
            # Scan the block until the next flush-ish top-level key.
            for follow in lines[i + 1 : i + 60]:
                if start_re.match(follow):
                    break
                m = ICON_RE.search(follow)
                if m:
                    return m.group(1)
            return None
    return None


def resolve(root: Path, trait_id: str) -> Path | None:
    declared = find_declared_icon(root, trait_id)
    if declared:
        p = root / declared
        if p.is_file():
            return p
    # Fallback: file named after the trait id.
    p = root / "gfx/interface/icons/traits" / f"{trait_id}.dds"
    return p if p.is_file() else None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    ap.add_argument("--copy", action="store_true", help="perform the copy")
    args = ap.parse_args()

    found, authored, missing = [], [], []

    with args.csv.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            new_id = (row.get("new_id") or "").strip()
            original = (row.get("original_id") or "").strip()
            source = (row.get("source_mod") or "").strip()
            if not new_id:
                continue

            if new_id in OVERRIDES:
                original, mod_id = OVERRIDES[new_id]
            else:
                mod_id_match = re.match(r"(\d+)", source)
                if not mod_id_match or original in ("", "-"):
                    authored.append(new_id)
                    continue
                mod_id = mod_id_match.group(1)

            root = mod_root(mod_id)
            if root is None:
                missing.append((new_id, f"source mod {mod_id} not installed"))
                continue

            src = resolve(root, original)
            if src is None:
                missing.append((new_id, f"no icon for {original} in {root.name}"))
                continue

            found.append((new_id, src))

    if args.copy:
        DEST.mkdir(parents=True, exist_ok=True)
        for new_id, src in found:
            dest_id = DEST_RENAMES.get(new_id, new_id)
            shutil.copy2(src, DEST / f"{dest_id}.dds")

    verb = "copied" if args.copy else "resolved"
    print(f"{len(found)} {verb}, {len(authored)} authored (no source), {len(missing)} missing")
    for new_id, why in missing:
        print(f"  MISSING  {new_id}: {why}")
    for new_id in authored:
        print(f"  AUTHORED {new_id}: needs hand-drawn art")


if __name__ == "__main__":
    main()
