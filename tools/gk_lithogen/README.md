# gk_lithogen — zero-config bio-ship cost regenerator

Regenerates gk_lithogenesis's vanilla-derived overwrites from current vanilla
Stellaris source. Run it after a vanilla update to catch new bio-ship components
and structural changes (e.g. the 4.3 `injected_modifier` restructuring).

No manifest, no configuration. Bio-ship scope is detected by structural
heuristics in `transform.py`:

- **inline_scripts**: glob `common/inline_scripts/ship_components/bio_*.txt`.
  Catches all bio-ship cost dispatchers. Excludes `behemoth_*` (Distant Stars
  space fauna), `grand_archive/mutations/*` (Grand Archive space fauna), and
  every other food-using inline_script unrelated to bio ships.
- **component_templates**: glob `common/component_templates/*.txt`, per
  top-level block match on bio-ship signal triggers (`country_uses_bio_ships`,
  `is_galvanic_empire`, `ship_uses_weaver_components`) **AND** food in
  resources.

Only blocks that match both rules are rebased. Everything else is left alone.

## Run

```
python3 tools/gk_lithogen/generate.py --dry-run   # preview
python3 tools/gk_lithogen/generate.py             # write output
```

Defaults:
- vanilla: `~/.steam/steam/steamapps/common/Stellaris`
- mod:     `/home/ryn/Projects/Stellaris/mod/gk_lithogenesis`

## Output layout

- `gk_lithogenesis/common/inline_scripts/ship_components/bio_*.txt` — one
  file per vanilla source, same filename. Each begins with a `# GENERATED`
  header comment.
- `gk_lithogenesis/common/component_templates/zz_flgsis_generated_components.txt`
  — aggregate of all rebased component_template blocks, ordered by vanilla
  source file. `zz_` prefix ensures later load order than hand-authored files.

## What it never touches

Hand-authored files and binary assets:
- `common/component_templates/000_flgsis_special_utility_components.txt`
- `common/graphical_culture/`, `common/scripted_variables/`,
  `common/species_classes/`, `common/economic_plans/`
- `common/ship_sizes/`, `common/section_templates/`, `common/megastructures/`,
  `common/armies/`, `common/governments/` (not in MVP scope yet)
- `localisation/`, `gfx/`, `descriptor.mod`, `thumbnail.png`

Adding ship_sizes/section_templates to the generator is a future extension.

## Transform

The `rebase_food_to_minerals` transform finds `cost { food = X ... }` and
`upkeep { food = X ... }` clauses and rewrites them as a paired pair:

```
cost = {
    food = X
    ...original siblings...
    trigger = { from = { country_uses_bio_ships = yes NOT = { graphical_culture = lithogenesis_01 } } }
}
cost = {
    minerals = X
    ...original siblings...
    mult = 0.8
    trigger = { from = { country_uses_bio_ships = yes graphical_culture = lithogenesis_01 } }
}
```

Idempotent: if the clause already mentions `graphical_culture = lithogenesis_01`,
it's skipped.

## First-run validation

Compare generator output against the hand-written files it's replacing:
```
git diff gk_lithogenesis/
```
Expected: mostly stylistic differences (blank lines stripped, `NOT` expanded
to multi-line, alloys upkeep duplicated in both branches instead of extracted
to a standalone clause). Any material divergence is a real difference to
inspect before committing.

Once you trust the output, delete the superseded hand-written overwrites
(`000_flgsis_utility_component_overwrites.txt`, the weapon OW for
`LM_BIO_ACCELERATOR`, etc.) and regeneration becomes the source of truth.

## Files

- `pdxscript.py` — parser/writer for Paradox script (tokenizer + recursive-
  descent parser, preserves comments).
- `transform.py` — the `rebase_food_to_minerals` transform and bio-ship
  detection helpers.
- `generate.py` — CLI driver.
