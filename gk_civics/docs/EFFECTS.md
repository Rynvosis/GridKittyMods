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
