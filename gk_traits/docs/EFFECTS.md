# GK Traits Mod Effects Reference

Quick reference for all gameplay effects in the GK Traits mod. Keep this up to date when traits change.

## Trait Access Gates

Every gk trait is gated two ways at once, and a species needs only one of them to pass.

The **portrait leg** is the primary gate: a `portrait_override` list pulled in by inline script, so the trait is offered to anything wearing one of those portraits. The **override leg** is `species_class_override`, a second route for species that qualify by what they have become rather than by what they look like.

| Suite | Portrait leg | Override leg | Override file |
|---|---|---|---|
| Mechanist (CYBER) | `gk_portraits_cyber` — cybernetic, synthetic and machine portraits | has `trait_cybernetic`, so ascended cyborgs qualify whatever their portrait | `gk_class_override_cyber` |
| Biogenesis | `gk_portraits_biogen` | empire has the Engineered Evolution ascension perk | `gk_class_override_biogen` |
| Phenotype | per-phenotype lists | empire has the Unnatural Selection tradition (vanilla `can_add_or_remove_phenotype_traits`) | `gk_class_override` |
| Common | `gk_portraits_common` | none | none |

A trait's `species_class` is a **direct grant**, not a restriction the other two legs widen (vanilla `common/traits/000_documentation_species_traits.txt:52-64`). A reptilian can take Dragon Scales on phenotype alone, without Engineered Evolution. The portrait and override legs extend reach beyond the phenotype; they never gate it.

Three further points, all easy to get wrong:

The Mechanist override reads on the **species** (`has_trait`), so only species you actually cyberised qualify. The Biogenesis and Phenotype overrides read on the **country** (through `from`), so once the empire qualifies, every species in it does. That asymmetry is deliberate, not an oversight.

Engineered Evolution is the single perk behind all four genetics trees (base without Biogenesis, then cloning, purity and mutation with it), so gating on the perk covers every genetic ascension path. Gating on a tradition would reach only one of them, which is why the Biogenesis leg does not share the phenotype override.

DLC checks are not needed on these traits, because the portrait is the gate. A DLC portrait in an override list is simply unavailable to a player without that DLC, so the trait is unreachable through it.

Vanilla's random-trait mechanics, Evolutionary Predators above all, select on a trait's `tags` rather than on any list of trait ids, so nothing can omit us by oversight. The consequence is that `tags` must name every phenotype the trait is available to, or that phenotype's DNA pool will skip it. The `cybernetic` and `drawbacks` tags are exclusions in those pools, which is why no Mechanist trait can be rolled by Evolutionary Predators.

Portrait cross-listing re-keys which DNA an empire banks: a species picked through our `inf1`-as-arthropoid set registers arthropoid DNA, not infernal, because vanilla keys that on `is_species_class` and never on portrait. Consistent, and not a bug.

When the sheet changes a per-category portrait list, regenerate with `python3 tools/build_gate_lists.py`.

## Trait Category Tooltips

The "belongs to the following categories" line on a trait comes from its `localized_tags`. The trait list *inside* each of those category popups is a separate hand-written enumeration in localisation, which the engine never derives from the tags. Both halves have to be maintained or a trait appears in one direction only.

Our half lives in `localisation/replace/english/gk_phenotype_concepts_l_english.yml`: the twelve vanilla phenotype lists rebuilt with gk traits appended, plus a psionic list, plus the two suite concepts `concept_gk_mechanist_traits` and `concept_gk_biogenesis_traits`. Each suite concept opens with its access rules and then lists its traits. The `replace` directory is used so the override wins regardless of load order.

Traits carrying a `portrait_override` also need a `<trait>_portrait_override_tt` key, or the game logs an error and drops the explanation line from the tooltip. This applies to the vanilla traits widened below, not just to gk traits.

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
