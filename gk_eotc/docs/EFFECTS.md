# GK End of the Cycle — Effects Reference

## Aura of the End — rival-side rework

### Rival fleets

Hull damage now applies **only to military ships**. Science ships, constructors, colonizers, and transports pass through unharmed. Damage values unchanged (5 / 10 / 15 hull/month at levels 1 / 2 / 3).

### Owner planets

Added `pop_bonus_workforce_mult` at the same scale as the existing produces modifiers — at level 3, the owner gets both **+100% production** and **+100% workforce** in every aura system.

| Level | Output (existing) | Workforce (new) |
|---|---|---|
| 1 | +33% station / planet job produces | +33% workforce |
| 2 | +66% station / planet job produces | +66% workforce |
| 3 | +100% station / planet job produces | +100% workforce |

The two stack multiplicatively in Stellaris's production pipeline, so a max-level aura system runs at roughly 4× effective output for the owner.

### Rival planets

| Level | Vanilla | Modded |
|---|---|---|
| 1 | `planet_stability_add = -6`, `planet_jobs_upkeep_mult = +0.12` | `planet_crime_mult = +0.10` |
| 2 | `planet_stability_add = -12`, `planet_jobs_upkeep_mult = +0.24` | `planet_crime_mult = +0.20` |
| 3 | `planet_stability_add = -18`, `planet_jobs_upkeep_mult = +0.36` | `planet_crime_mult = +0.30` |

Job upkeep penalty removed; stability hit replaced with proportional crime pressure.

## Covenant of the End of the Cycle — owner naval cap bonus

Adds a second `triggered_modifier` block to the EotC covenant:

- `country_naval_cap_add = 10` × number of systems currently carrying the owner's Aura of the End.

Uses `mult = value:gk_eotc_aura_systems_count` (wrapping `trigger:count_systems_with_aura`). Scales smoothly as the aura spreads and contracts. Stacks additively on top of the vanilla `country_naval_cap_mult = 1` covenant bonus.

Also added flat to the covenant:

- `shipclass_military_build_speed_mult = +1.0` (+100% military ship build speed)
- `ship_military_cost_mult = -0.5` (−50% military ship build cost)

### Untouched

- Owner-side fleet/planet bonuses on the aura itself, level thresholds, spread mechanics, encounter events, win condition, clashing, and accord interactions all preserved verbatim from vanilla.
- All other patrons' definitions remain untouched (override is keyed only to `end_of_the_cycle`).
