# GK End of the Cycle — Changelog

## 0.1.0 — initial

- Aura of the End: rival-fleet hull damage now restricted to military ships (science / construction / colony / transport ships pass through unharmed).
- Aura of the End: removed `planet_jobs_upkeep_mult` penalty from rival planets.
- Aura of the End: replaced `planet_stability_add` (−6 / −12 / −18) with `planet_crime_mult` (+10% / +20% / +30%) on rival planets.
- EotC covenant: added `country_naval_cap_add = +10` per system currently carrying the owner's Aura of the End (scales via `mult = value:gk_eotc_aura_systems_count`).
- Aura of the End: added `pop_bonus_workforce_mult` to `owner_planet_modifier` at 0.33 / 0.66 / 1.0 (matches existing produces tracks). Max-level aura now grants +100% output and +100% workforce on owner planets.
- EotC covenant: added `shipclass_military_build_speed_mult = +1.0` (+100% military ship build speed) and `ship_military_cost_mult = -0.5` (−50% military ship cost).
