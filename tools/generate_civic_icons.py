#!/home/ryn/pyflex/bin/python3
"""Civic & trait icon generator, driven entirely by assets/civic-icons/used_icons.csv.

The CSV is the single source of truth: each row is one icon to generate. Add, edit, or
remove rows by hand (or via the stellaris-civic-icon skill) and rerun this script to
regenerate everything — no other state is kept.

CSV columns: icon_name,id,mod,type,scheme_or_category,glyph_size,offset_x,offset_y,alpha_gamma,invert
- icon_name          basename (no .svg) to search for under assets/civic-icons/game-icons/
- id                 civic_* or trait_* identifier, also the output DDS filename
- mod                target mod directory (gk_ec, gk_raiding, ...)
- type               civic | trait — selects background set, canvas size, and output path
- scheme_or_category civic: positive/hive/machine/megacorp/negative/psi
                     trait: species_generic, leader_physics, climate_cold, ... (see TRAIT_BACKGROUNDS)
- glyph_size         glyph render size in px before centering on the canvas (default 40 civic / 21 trait)
- offset_x/offset_y  pixel offset from center (default 0,0)
- alpha_gamma        optional >1 gamma lift on the glyph's alpha to firm up detail-dense
                     icons (blank/1 = off). The glyph is always clipped to the background's
                     own alpha, so overflow past the frame is trimmed regardless.
- invert             optional 1/yes to negate the glyph alpha (figure/ground swap): the
                     glyph becomes negative space knocked out of a filled tinted disc.

Usage: tools/generate_civic_icons.py [--preview]
  --preview   write upscaled PNGs to /tmp/civic_icon_previews/ instead of real DDS files
  (no flag)   write the real DDS files into each mod's gfx/interface/icons/... tree
"""

import argparse
import csv
import os
import subprocess
import sys
import tempfile
from pathlib import Path

MOD_ROOT = Path(__file__).resolve().parent.parent
ASSETS = MOD_ROOT / "assets" / "civic-icons"
TRAIT_ASSETS = MOD_ROOT / "assets" / "trait-icons"
SVG_ROOT = ASSETS / "game-icons" / "icons" / "000000" / "transparent" / "1x1"
REGISTRY = ASSETS / "used_icons.csv"
PREVIEW_DIR = Path("/tmp/civic_icon_previews")

CIVIC_TINT_BY_SCHEME = {
    "positive": "#00211D",
    "negative": "#210300",
    "hive": "#EBDDBE",
    "machine": "#002728",
    "megacorp": "#0D0D05",
    "psi": "#0E0517",
}
CIVIC_CANVAS = 50
CIVIC_DEFAULT_GLYPH_SIZE = 40

TRAIT_BACKGROUNDS = {
    "species_generic": "species_generic_trait_template.png",
    "species_generic_negative": "species_generic_negative_trait_template.png",
    "species_energy": "species_energy_trait_template.png",
    "species_machine": "species_machine_trait_template.png",
    "species_overtuned": "species_overtuned_trait_template.png",
    "species_psionic": "species_psionic_trait_template.png",
    "leader_engineering": "leader_engineering_trait_template.png",
    "leader_physics": "leader_physics_trait_template.png",
    "leader_society": "leader_society_trait_template.png",
    "leader_subject": "leader_subject_trait_template.png",
    "climate_cold": "climate_cold_trait_template.png",
    "climate_dry": "climate_dry_trait_template.png",
    "climate_wet": "climate_wet_climate_trait_template.png",
    "climate_special": "climate_special_trait_template.png",
}
# Per-category glyph tint, recovered from each vanilla template's top-right marker pixel
# (Paradox convention: that pixel encodes the intended glyph colour for the category).
# The marker pixel has since been cleared from our template assets; these values preserve it.
TRAIT_TINT_BY_CATEGORY = {
    "species_generic":          "#002320",
    "species_generic_negative": "#210500",
    "species_energy":           "#071022",
    "species_machine":          "#001F21",
    "species_overtuned":        "#130E02",
    "species_psionic":          "#160825",
    "leader_engineering":       "#231B00",
    "leader_physics":           "#001523",
    "leader_society":           "#081B0D",
    "leader_subject":           "#1B1400",
    "climate_cold":             "#020303",
    "climate_dry":              "#24201B",
    "climate_wet":              "#171A14",
    "climate_special":          "#0F0D01",
}
TRAIT_CANVAS = 29
TRAIT_DEFAULT_GLYPH_SIZE = 21


def magick(*args):
    result = subprocess.run(["magick", *[str(a) for a in args]], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"magick error: {result.stderr}", file=sys.stderr)
        raise SystemExit(1)
    return result.stdout.strip()


def find_svg(icon_name):
    # icon_name may be "author/name" to disambiguate icons that share a filename
    # across multiple game-icons.net contributors (e.g. two different "revolt.svg")
    if "/" in icon_name:
        path = SVG_ROOT / f"{icon_name}.svg"
        if not path.exists():
            print(f"  ! no SVG at '{icon_name}.svg' — skipping", file=sys.stderr)
            return None
        return path

    matches = list(SVG_ROOT.rglob(f"{icon_name}.svg"))
    if not matches:
        print(f"  ! no SVG found for '{icon_name}' — skipping", file=sys.stderr)
        return None
    if len(matches) > 1:
        authors = ", ".join(sorted(m.parent.name for m in matches))
        print(f"  ! '{icon_name}' is ambiguous ({authors}) — use 'author/{icon_name}' in the "
              f"registry to disambiguate. Using {matches[0]} for now.", file=sys.stderr)
    return matches[0]


def resolve_background(row):
    if row["type"] == "civic":
        scheme = row["scheme_or_category"]
        bg = ASSETS / "backgrounds" / f"civic_bg_{scheme}.png"
        tint = CIVIC_TINT_BY_SCHEME.get(scheme)
        if tint is None:
            print(f"  ! unknown civic scheme '{scheme}' for {row['id']} — skipping", file=sys.stderr)
            return None
        return bg, tint, CIVIC_CANVAS, int(row["glyph_size"] or CIVIC_DEFAULT_GLYPH_SIZE)
    elif row["type"] == "trait":
        category = row["scheme_or_category"]
        filename = TRAIT_BACKGROUNDS.get(category)
        if filename is None:
            print(f"  ! unknown trait category '{category}' for {row['id']} — skipping", file=sys.stderr)
            return None
        tint = TRAIT_TINT_BY_CATEGORY.get(category)
        if tint is None:
            print(f"  ! no tint recorded for trait category '{category}' for {row['id']} — skipping", file=sys.stderr)
            return None
        bg = TRAIT_ASSETS / "backgrounds" / filename
        return bg, tint, TRAIT_CANVAS, int(row["glyph_size"] or TRAIT_DEFAULT_GLYPH_SIZE)
    else:
        print(f"  ! unknown type '{row['type']}' for {row['id']} — skipping", file=sys.stderr)
        return None


def output_path(row, preview):
    if preview:
        PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
        # icon_name may contain "author/name" (see find_svg) — flatten for a valid filename
        icon_label = row["icon_name"].replace("/", "_")
        return PREVIEW_DIR / f"{row['id']}__{row['scheme_or_category']}__{icon_label}.png"
    subdir = "governments/civics" if row["type"] == "civic" else "traits"
    out_dir = MOD_ROOT / row["mod"] / "gfx" / "interface" / "icons" / subdir
    out_dir.mkdir(parents=True, exist_ok=True)
    ext = ".png" if preview else ".dds"
    return out_dir / f"{row['id']}{ext}"


def generate_row(row, preview):
    svg = find_svg(row["icon_name"])
    if svg is None:
        return False
    resolved = resolve_background(row)
    if resolved is None:
        return False
    bg, tint, canvas, glyph_size = resolved
    off_x = int(row["offset_x"] or 0)
    off_y = int(row["offset_y"] or 0)
    alpha_gamma = (row.get("alpha_gamma") or "").strip()
    gamma_args = ["-gamma", alpha_gamma] if alpha_gamma and alpha_gamma not in ("1", "1.0") else []
    # invert: swap figure/ground by negating the glyph alpha, so the glyph reads as
    # negative space knocked out of a filled tinted disc (engraved/cameo look).
    invert = (row.get("invert") or "").strip().lower() in ("1", "yes", "true")
    invert_args = ["-negate"] if invert else []

    with tempfile.TemporaryDirectory() as work:
        work = Path(work)
        magick("-background", "none", svg, "-resize", f"{glyph_size}x{glyph_size}", work / "glyph_raw.png")
        magick("-size", f"{canvas}x{canvas}", "xc:none", work / "glyph_raw.png",
               "-gravity", "center", "-geometry", f"+{off_x}+{off_y}", "-composite", work / "rendered.png")
        magick(work / "rendered.png", "-channel", "A", "-separate", "+channel", *gamma_args, *invert_args,
               "-define", "png:color-type=6", work / "alpha.png")
        magick(work / "rendered.png", "-fill", tint, "-colorize", "100%",
               "-define", "png:color-type=6", work / "tinted.png")
        magick(work / "tinted.png", work / "alpha.png", "-alpha", "off",
               "-compose", "CopyOpacity", "-composite", "-define", "png:color-type=6", work / "tinted.png")
        # Clip the glyph to the background's own alpha (DstIn) so any overflow past the
        # circular frame is trimmed to the frame's exact edge, then composite normally so
        # the frame's own feathered rim is preserved untouched.
        magick(work / "tinted.png", bg, "-compose", "DstIn", "-composite",
               "-define", "png:color-type=6", work / "clipped.png")
        magick(bg, work / "clipped.png", "-compose", "Over", "-composite",
               "-define", "png:color-type=6", work / "final.png")

        out = output_path(row, preview)
        if preview:
            magick(work / "final.png", "-filter", "point", "-resize", f"{canvas * 4}x{canvas * 4}", out)
        else:
            magick(work / "final.png", "-define", "dds:compression=none", out)

    print(f"  OK  {row['id']} -> {out}")
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--preview", action="store_true", help="write PNGs to /tmp instead of real DDS files")
    args = parser.parse_args()

    if not REGISTRY.exists():
        print(f"No registry at {REGISTRY}", file=sys.stderr)
        raise SystemExit(1)

    with open(REGISTRY) as f:
        rows = list(csv.DictReader(f))

    print(f"{len(rows)} entries in {REGISTRY.relative_to(MOD_ROOT)}")
    print(f"{'PREVIEW MODE — writing to ' + str(PREVIEW_DIR) if args.preview else 'REAL MODE — writing DDS into mod trees'}\n")

    ok = sum(generate_row(row, args.preview) for row in rows)
    print(f"\n{ok}/{len(rows)} generated")


if __name__ == "__main__":
    main()
