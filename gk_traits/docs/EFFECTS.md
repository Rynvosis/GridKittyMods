# GK Traits Mod Effects Reference

Quick reference for all gameplay effects in the GK Traits mod. Keep this up to date when traits change.

## Category Suite Scaffolds

Three files, one per new trait category. Each will eventually host that category's full positive/negative trait suite; for now each contains only an invisible placeholder marker trait so we can verify gates in-game before writing the suite.

| File | Marker | Category gate |
|---|---|---|
| `gk_traits_cyber_synth.txt` | `trait_gk_marker_cybsynth` | CYBER + SYNTH + MACHINE_ROBOT (55 portraits) |
| `gk_traits_biogenesis.txt`  | `trait_gk_marker_biogen`   | BIOGENESIS (13 portraits) |
| `gk_traits_common.txt`      | `trait_gk_marker_common`   | COMMON (167 portraits) |

Marker design: cost 0, no modifier block. Uses the vanilla psionic-trait gate pattern - `species_class = { <vanilla ship-set-only class> }` + `portrait_override = { <category portraits> }`. The ship-set-only classes (`CYBERNETIC`, `BIOGENESIS_02`, `WILDERNESS`) are vanilla species_classes that exist but are never assigned to any species, so the class check never matches; the `portrait_override` list is the actual gate.

Class anchors used:
| File | Anchor species_class | Why |
|---|---|---|
| `gk_traits_cyber_synth.txt` | `CYBERNETIC` | vanilla cybernetic ship-set class |
| `gk_traits_biogenesis.txt` | `BIOGENESIS_02` | vanilla biogenesis ship-set class |
| `gk_traits_common.txt`     | `WILDERNESS`  | vanilla biogenesis city-set class (used as a neutral never-match anchor) |

### Tinkerer (placeholder, in `gk_traits_cyber_synth.txt`)

Trait ID: `trait_gk_tinkerer`. Cost 2. Sits alongside the cybsynth marker as the first real content in the CYBER/SYNTH file - placeholder until the full suite is written.

| Modifier | Value |
|---|---|
| Engineer Jobs Bonus Workforce | +20% |
| Roboticist Jobs Bonus Workforce | +10% |
| Biologist Jobs Workforce | -10% |
| Physicist Jobs Workforce | -10% |

Gated by the same 55-portrait CYBER/SYNTH portrait_override as the marker. Slave cost 1000 energy.

DLC checks aren't needed on these traits - the portrait is the gate. If a DLC portrait is in the override list and the player lacks the DLC, the portrait is unavailable so the trait is unreachable through it.

When the sheet changes the per-category portrait list, regenerate the lists with `python3 tools/build_gate_lists.py` and paste the relevant block into the `portrait_override` of each trait in the matching file. (No auto-patcher: trait content is hand-maintained.)

## Vanilla Trait Widening

For each cross-classified portrait in the sheet, the mod widens vanilla phenotype-gated traits so the portrait can take them. Implemented via whole-file overwrites in `common/traits/`:

| File | Traits widened |
|---|---|
| `04_species_traits.txt` | 9 (LITHOID / PLANT / FUN base traits + cross-tagged additions) |
| `09_ascension_traits.txt` | 1 |
| `15_biogenesis_species_traits.txt` | 16 (biogenesis suite including `trait_shelled` etc.) |
| `16_infernals_traits.txt` | 4 (INF traits) |
| `17_shroud_species_traits.txt` | 4 (psionic traits; adds `nec5` to the psionic portrait pool) |

Each trait's `portrait_override` is the UNION of the vanilla list and the new sheet-derived additions. Vanilla single-portrait exceptions (e.g., `rep14` and `pro2` on `trait_shelled`) are preserved. All vanilla `host_has_dlc` / `has_X` triggers are preserved.

To regenerate after sheet edits:

```
# Re-copy the vanilla file, then patch:
cp ~/.local/share/Steam/steamapps/common/Stellaris/common/traits/<file>.txt common/traits/<file>.txt
python3 tools/build_gate_lists.py --patch-vanilla common/traits/<file>.txt
```

The script refuses to write if any DLC-trigger line would be removed.

## Portrait Cross-Listing

For every "Also moving into X" note in the sheet, the mod surfaces the portrait inside the target phenotype's empire-designer dropdown via new portrait_sets in `common/portrait_sets/01_gk_crosslist_sets.txt` and category extensions in `common/portrait_categories/zz_gk_categories.txt`.

| Set | Portraits | Target | DLC gate |
|---|---|---|---|
| `gk_inf_as_art` | inf1 | ART | has_infernals |
| `gk_fun_hum_rep_as_inf` | fun13, humanoid_hp_01, rep17 | INF | has_infernals |
| `gk_tox_as_inf` | tox9 | INF | has_toxoids + has_infernals |
| `gk_inf_as_lithoid` | inf6 | LITHOID | has_infernals + has_lithoids |
| `gk_lithoid_as_plant` | lith6, lith8 | PLANT | has_lithoids + Plantoids DLC |
| `gk_inf_as_rep` | inf2, inf3, inf7 | REP | has_infernals |
| `gk_inf_as_tox` | inf10 | TOX | has_infernals + has_toxoids |

Each set's `conditional_portraits` block gates `randomizable` and `playable` on the listed DLC triggers, so cross-listings stay invisible without the required DLC. Cross-listing an Infernal portrait into another phenotype never grants Infernal gameplay without the DLC.

The `zz_gk_categories.txt` file adds these sets to the existing `infernals`, `plantoids`, `reptilians`, `arthropoids`, `toxoids`, `lithoids` UI categories. The `zz_` prefix forces it to load after vanilla and any other mods. Each duplicate block lists ONLY the new gk sets - Stellaris merges the inner `sets` list across files, so vanilla entries are preserved automatically. Re-declaring them would cause duplicates in the empire designer dropdown.

To regenerate after sheet edits:

```
python3 tools/build_gate_lists.py --emit-crosslist-sets
```

This rewrites `01_gk_crosslist_sets.txt`. The category file is hand-maintained.
