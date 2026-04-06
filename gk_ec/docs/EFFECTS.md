# GK_EC Mod Effects Reference

Quick reference for all gameplay effects in the ryn_misc / GK_EC mod. Keep this up to date when modifiers change.

## Ethics

Ethic categories: `col` (Authoritarian/Egalitarian), `ind` (Individualist/Collectivist), `str` (vanilla Militarist/Pacifist).

### Authoritarian (`00_ethics.txt` — vanilla overwrite)

Changed vs vanilla: removed Worker Bonus Workforce and Leader Lifespan, added Enforcer Jobs Bonus Workforce.

| Ethic | Modifiers |
|---|---|
| **Fanatic Authoritarian** | Influence +1, Enforcer Jobs Bonus Workforce +20%, Slave Bonus Workforce +10% |
| **Authoritarian** | Influence +0.5, Enforcer Jobs Bonus Workforce +10%, Slave Bonus Workforce +5% |

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
| **Fanatic Collectivist** | Amenities Usage -10%, Housing Usage -10%, Worker Bonus Workforce +20% |
| **Collectivist** | Amenities Usage -5%, Housing Usage -5%, Worker Bonus Workforce +10% |

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
- Standard: +2.5% Amenities
- Megacorp: +2.5% Amenities

### Pathfinders / Prospecting Venture / Questing Tendrils / Exploration Matrix

Available to: All authority types.

**Effects**:
- +25% Survey Speed
- +20% Anomaly Chance
- +25% Anomaly Research Speed
- -15% Starbase Influence Cost

**Councilor** (Chief Surveyor / Prospecting Director):
- +2% Anomaly Chance per level

### Surveillance State / Data Brokerage / Omniscient Network

Available to: Standard empires, Megacorps & Hive Minds (no machine variant).

**Effects**:
- +1 Intel Decryption, +25% Spy Network Growth, -25 Trust Cap
- Standard/Hive: +5 Stability
- Megacorp: +1 Envoy

**Councilor** (Intelligence Director / Data Analytics Officer):
- +0.2 Ship Cloaking Strength per level

### Paternalism / Nurturing Overmind / Caretaker Protocol

Available to: Standard empires (Authoritarian required), Hive Minds, Machine Intelligences.

**Effects**:
- +10 Stability, -10% Leader XP Gain
- Standard: +5% Happiness, -25% Ethics Shift Speed. Forces Social Welfare living standard.
- Hive/Machine: -10% Deviancy

**Councilor** (Minister of Social Harmony):
- +2% Governing Ethics Attraction per level

### Industrial Democracy

Available to: Megacorps only.

**Effects**:
- +50% Worker Political Power, +5% Worker Happiness, +5 Stability, -15% Ethics Shift Speed
- Forces Social Welfare living standard

**Councilor** (Labor Relations Director):
- +0.10 Trade Value from Workers per level

### Social Democracy

Available to: Standard empires (Democratic authority required).

**Effects**:
- -10% Housing Usage, +5% Pop Growth, +5 Stability, -15% Ethics Shift Speed
- Forces Social Welfare living standard

**Councilor** (Minister of Public Welfare):
- -1% Housing Usage per level

### War Engineers / Arms Conglomerate / Evolved Armaments / Weapons Research Node

Available to: All authority types. Requires Militarist (standard/megacorp).

**Effects**:
- +10% Ship Hull, +5% Weapon Damage, +25% Military Theory Research, +10% Ship Upkeep

**Councilor** (Master Armorer / Arms Director):
- Soldiers produce +0.05 Physics, +0.05 Society, +0.05 Engineering per level
- Soldiers cost +0.075 Alloys upkeep per level

### Austere Society / Lean Enterprise / Hive Ascetic (OW) / Low-Power Mode

Available to: All authority types. Hive variant overwrites vanilla Hive Ascetic.

**Effects**:
- -15% Amenities Usage, -5% All Job Output
- Standard/Megacorp: -10% Consumer Goods Upkeep
- Hive: +5% Habitability (replaces vanilla Hive Ascetic)
- Machine: -10% Robotics Upkeep

**Councilor** (Minister of Austerity / Efficiency Auditor):
- -2% Building Upkeep per level

### Constitutional Monarchy

Available to: Standard empires (Democratic authority required). Cannot be removed.

**Effects**:
- +1 Official Cap, +1 Envoy
- Spawns a **Constitutional Monarch** leader (official, cannot sit on council) on game start
- Monarch trait (diplomatic figurehead):
  - Galactic Community: +25% Diplomatic Weight
  - Federation: +0.50 Federation XP, -10% Join Malus, -25% Cohesion Ethics Penalty
- On monarch death, a new monarch is crowned (coronation event)

**Councilor** (Royal Chancellor):
- +0.2 Influence per level

### Parliamentary Monarchy

Available to: Standard empires (Imperial or Dictatorial authority required).

**Effects**:
- +25% Faction Output, +50% Specialist Political Power, +5% Unity

**Councilor** (Speaker of Parliament):
- +2% Faction Output per level

### Algocracy

Available to: Standard empires (Dictatorial authority required). Cannot be removed. Non-machine species only.

**Effects**:
- Replaces ruler with an immortal AI leader with the **Central AI** destiny trait
- +5% Politician output per leader level (trait)
- +10 Energy upkeep per leader level (trait)
- +100% Politician Automated Workforce

**Councilor** (System Administrator):
- -1.5% Automated Jobs Upkeep per level

### Raiding Civics

See `gk_raiding/docs/EFFECTS.md` — implemented in the GK Raiding mod.

## System Initializers

- `gk_ec_habitat_system_initializers.txt` — Custom habitat system starts
- `gk_ec_lunar_colony_initializers.txt` — Lunar colony origin systems
- `gk_ec_titanic_system_intializers.txt` — Titanic life system variants
