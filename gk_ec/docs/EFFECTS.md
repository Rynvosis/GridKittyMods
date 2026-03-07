# GK_EC Mod Effects Reference

Quick reference for all gameplay effects in the ryn_misc / GK_EC mod. Keep this up to date when modifiers change.

## Ethics

Ethic categories: `col` (Authoritarian/Egalitarian), `ind` (Individualist/Collectivist), `str` (vanilla Militarist/Pacifist).

### Authoritarian (`00_ethics.txt` — vanilla overwrite)

Changed vs vanilla: removed Worker Bonus Workforce, added Slave Bonus Workforce, changed Leader Lifespan from flat to %.

| Ethic | Modifiers |
|---|---|
| **Fanatic Authoritarian** | Leader Lifespan +10%, Influence +1, Slave Bonus Workforce +10% |
| **Authoritarian** | Leader Lifespan +5%, Influence +0.5, Slave Bonus Workforce +5% |

### Egalitarian (`00_ethics.txt` — vanilla overwrite)

Unchanged from vanilla.

| Ethic | Modifiers |
|---|---|
| **Fanatic Egalitarian** | Faction Output +30%, Specialist Bonus Workforce +10% |
| **Egalitarian** | Faction Output +15%, Specialist Bonus Workforce +5% |

### Individualist (`gk_ec_ethics.txt` — new axis)

| Ethic | Modifiers |
|---|---|
| **Fanatic Individualist** | Ruler Bonus Workforce +20%, Trade Fee -10% |
| **Individualist** | Ruler Bonus Workforce +10%, Trade Fee -5% |

- Allows Stratified Economy (living standard override)
- **Faction** (`gk_ec_individualist`): Wants free trade, mercantile stance, commercial pacts, private enterprise, civilian economy. Opposes welfare, cooperativism, shared burden.
- Promoted/Suppressed: attraction +100% / -75%

### Collectivist (`gk_ec_ethics.txt` — new axis)

| Ethic | Modifiers |
|---|---|
| **Fanatic Collectivist** | Amenities Usage -20%, Housing Usage -20%, Worker Production +10% |
| **Collectivist** | Amenities Usage -10%, Housing Usage -10%, Worker Production +5% |

- Allows Utopian Abundance (living standard override)
- **Faction** (`gk_ec_collectivist`): Wants social welfare, worker ownership, cooperative stance, nutritional plenitude. Opposes stratification, private monopolies, mercantilism, trade leagues.
- Promoted/Suppressed: attraction +100% / -75%

## Civics

### Centralized State / Centralized Synapse / Core Processing Hub / Corporate Monolith

Available to: All authority types (separate variants).

**Capital planet** (via inline script on all capital buildings):
- +20 Stability, +100% Governing Ethics Attraction
- Ruler jobs scaling with capital tier: `floor(2^(tier-1)) × BASE` — 100/200/400 at tier 1/2/3 (BASE=100)
  - Standard: Politicians (BASE=100), Worker Coop: Bureaucrats (BASE=150), Gestalt: Coordinators (BASE=150)
  - Standard/Worker Coop also add councilor-scaled jobs (see below)

**Non-capital planets**:
- -5 Stability, -25% Governing Ethics Attraction

**Councilor** (Capital Prefect / Head of Headquarters):
- +25 ruler jobs per level on capital (doubled to +50/level if councilor governs capital)

### Penal Colonies / Correctional Profit Centers

Available to: Standard empires & Megacorps.

**Effects**:
- Start with Penal Colonies technology
- Standard: +1 Enforcer Unity output
- Megacorp: +1 Enforcer Trade Value output

**Councilor** (High Warden / Rehabilitation Director):
- -5% Crime

### Leisure Society / Hospitality Conglomerate

Available to: Standard empires & Megacorps.

**Effects**:
- Start with Resort Colonies technology
- Standard: +1 Entertainer Unity output
- Megacorp: +1 Entertainer Trade Value output

**Councilor** (Minister of Leisure / Chief Experience Officer):
- Standard: +10% Immigration Pull
- Megacorp: +5% Trade Value

### Raiding Civics (WIP)

Planned: Barbaric Overwrite, Emancipators, Roboliberators — not yet implemented.

## System Initializers

- `gk_ec_habitat_system_initializers.txt` — Custom habitat system starts
- `gk_ec_lunar_colony_initializers.txt` — Lunar colony origin systems
- `gk_ec_titanic_system_intializers.txt` — Titanic life system variants
