# GK Civics Mod Effects Reference

Quick reference for all gameplay effects in the GK Civics mod. Keep this up to date when civics change.

## Vanilla Overrides

### Galvanic Symbiosis (`galvanic_symbiosis_OW.txt`)

Available to: any species (vanilla locks to Infernal species_class). Requires the Infernals Species Pack DLC.

**Changed vs vanilla**: removed `species_class = { value = INF }` from the `possible` block on the standard, hive, and corporate variants. All other gates (DLC, origin/civic exclusions, authority/ethic potential, random_weight) are preserved.

**Variants covered**:
- `civic_galvanic_symbiosis` (standard)
- `civic_hive_galvanic_symbiosis` (hive mind)
- `civic_corporate_galvanic_symbiosis` (corporate)

`civic_machine_galvanic_symbiosis` is unchanged because vanilla never gated it on species_class.

**Localisation** (`localisation/replace/`): `civic_galvanic_symbiosis_desc` is overridden to drop the "WARNING: Blocks access to Synthetic Ascension" line, since gk_ec removes `is_galvanic_empire = no` from `ap_synthetic_evolution`. The corporate and hive descriptions inherit the same key, so all three variants are covered.

### Scorched Earth (`scorched_earth_OW.txt`)

Available to: any empire whose homeworld is Volcanic, or any Infernal species. Requires the Infernals Species Pack DLC.

**Changed vs vanilla**: `species_class = { value = INF }` becomes an `OR` of that plus `preferred_planet_class = { value = pc_volcanic }`. The civic itself carries `added_planet_types = { pc_volcanic }`, so selecting it puts Volcanic in the homeworld picker and a non-Infernal empire can then satisfy the requirement.

`civic_hive_scorched_earth` also gains the four climate/planet-type lines the standard variant already had. Without them the hive variant could never offer a Volcanic homeworld, leaving the new requirement unsatisfiable.

**Variants covered**: `civic_scorched_earth`, `civic_hive_scorched_earth`. There is no corporate or machine variant in vanilla.

### Idyllic Bloom (`idyllic_bloom_OW.txt`)

Available to: any species (vanilla locks to Fungoid or Plantoid). Requires the Plantoids Species Pack DLC.

**Changed vs vanilla**: removed the `species_class` FUN/PLANT block from the `possible` block on both variants. Nothing downstream needed changing, because `is_idyllic_bloom_empire` already admits non-plantoids through `civic_life_seeded`, whose origin has no species-class gate. The Gaiaseeders buildings, the Composer of Strands attunement, the councilor, and the storm resolutions all key on that trigger.

**Variants covered**: `civic_idyllic_bloom`, `civic_hive_idyllic_bloom` (including its `civic_wilderness_idyllic_bloom` swap type).

## Maintenance

Each overwrite carries a `# Version last updated:` header. These are full copies of vanilla civic definitions, since `common/` merges per top-level key and a `possible` block cannot be patched in isolation. Re-diff them against `common/governments/civics/` after a Stellaris patch.
