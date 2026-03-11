# GK Raiding — Effects Reference

Quick reference for all gameplay effects in the GK Raiding mod. Keep this up to date when modifiers change.

## Civics

### Emancipators / Liberation Enterprise

Available to: Standard (`civic_gk_emancipators`) and Megacorp (`civic_gk_emancipators_megacorp`).

**Requirements:** Egalitarian + Militarist

| Modifier | Value |
|---|---|
| Army Morale | +50% |
| Raiding Capacity | +50% |

**Councilor** (Liberation Commander — Commander):
- Ship Fire Rate: +2% per level

**Effects:**
- Unlocks Emancipation raiding policy
- Unlocks Emancipation war goal (enslaved pops only, no pillaging)

### Robo-Liberators / Synthetic Liberation Corp

Available to: Standard (`civic_gk_robo_liberators`) and Megacorp (`civic_gk_robo_liberators_megacorp`).

**Requirements:** Materialist (implicit via AI weight)

| Modifier | Value |
|---|---|
| Raiding Capacity | +50% |

**Councilor** (Synthetic Rights Advocate — Scientist/Commander):
- Robot Upkeep: -2% per level
- Robot Happiness: +1% per level

**Effects:**
- Unlocks Robo-Liberation raiding policy
- Unlocks Robo-Liberation war goal (robots only, no pillaging)

### Harvest Incorporated (Megacorp Despoilers)

Available to: Megacorp only (`civic_gk_barbaric_despoilers_megacorp`).

**Requirements:** Militarist

| Modifier | Value |
|---|---|
| Slave Market Cost | -20% |
| Slave Bonus Workforce | +10% |

**Councilor** (Acquisitions Director — Commander/Official):
- Slave Market Cost: -4% per level
- Slave Upkeep: -2% per level

**Effects:**
- Grants Raiding casus belli
- Unlocks Reaping war goal

### Harvesting Protocol (Machine Despoilers)

Available to: Machine Intelligence only (`civic_gk_barbaric_despoilers_machine`). Game-start only.

**Requirements:** Not Servitor, Assimilator, or Terminator

| Modifier | Value |
|---|---|
| Organic Battery Energy | +1 |
| Organic Battery Unity | +1 |
| Legion Node XP | +25% |

**Effects:**
- Starts with secondary species (Grid Amalgamated organic batteries)
- Grants Raiding casus belli

### Freedom Directive (Machine Robo-Liberators)

Available to: Machine Intelligence only (`civic_gk_robo_liberators_machine`).

| Modifier | Value |
|---|---|
| Robot Upkeep | -15% |
| Pop Assembly | +10% |
| Raiding Capacity | +50% |
| Legion Node XP | +25% |

**Effects:**
- Unlocks Robo-Liberation raiding policy and war goal

## Policies

### Raiding Focus (`gk_raiding_focus`)

Cannot change while at war.

| Option | Policy Flag | Availability |
|---|---|---|
| Plunder | `gk_focus_plunder` | All except Emancipators/Robo-Liberators |
| No Raiding (Despoliation) | `gk_focus_no_pop_raiding` | All except Emancipators/Robo-Liberators |
| Emancipation | `gk_focus_emancipation` | Emancipators civic, or any Egalitarian (not Robo-Liberators) |
| Robo-Liberation | `gk_focus_robo_liberation` | Robo-Liberators civic only |

### Robot Raiding (`gk_robot_raiding`)

Cannot change while at war.

| Option | Policy Flag | Availability |
|---|---|---|
| Capture Robots | `gk_allow_robot_raiding` | All except Robo-Liberators |
| Organics Only | `gk_forbid_robot_raiding` | All except Robo-Liberators |
| Robots Only | `gk_robots_only_raiding` | Robo-Liberators only |

## War Goals

### Raiding (`wg_plunder` — vanilla overwrite)

CB: `cb_despoliation`. Surrender acceptance: -75.

| Mechanic | Value |
|---|---|
| Surrender pop cap | 10% (scaled by Raiding Capacity) |
| Bombardment/invasion pop cap | 20% (scaled by Raiding Capacity) |
| Resource pillage | Pillage-capable empires on this side gain 1 month of current output per 10 devastation |
| Invasion bonus | Remaining 0-100 devastation headroom at current rate |
| Surrender tribute | Each surviving colony pays from its remaining 0-50 devastation band |
| Surrender aftermath | Local planet tribute modifier for 5 years |

### Pillage (`wg_plunder_raid` — vanilla overwrite)

CB: `cb_pirate_raid`. Surrender acceptance: -50.

| Mechanic | Value |
|---|---|
| Pop capture | None (resources only) |
| Resource pillage | Pillage-capable empires on this side gain 6 months of current output per 10 devastation |
| Invasion bonus | Remaining 0-100 devastation headroom at current rate |
| Surrender tribute | Each surviving colony pays from its remaining 0-50 devastation band |
| Surrender aftermath | Local planet tribute modifier for 5 years |

### Emancipation (`wg_gk_emancipation`)

CB: `cb_despoliation`. Surrender acceptance: -50.

| Mechanic | Value |
|---|---|
| Pop type | Enslaved pops only |
| Surrender pop cap | 10% (scaled by Raiding Capacity) |
| Bombardment/invasion pop cap | 30% (scaled by Raiding Capacity) |
| Pillaging | None |

Defender must have enslaved pops.

### Robo-Liberation (`wg_gk_robo_liberation`)

CB: `cb_despoliation`. Surrender acceptance: -50.

| Mechanic | Value |
|---|---|
| Pop type | Robots only |
| Surrender pop cap | 10% (scaled by Raiding Capacity) |
| Bombardment/invasion pop cap | 30% (scaled by Raiding Capacity) |
| Pillaging | None |

Defender must have robotic pops.

### Reaping (`wg_gk_reaping`)

CB: `cb_despoliation`. Surrender acceptance: -1000 (effectively forces war to exhaustion).

| Mechanic | Value |
|---|---|
| Pop type | All sapient pops |
| Pop cap | Unlimited |
| Pillaging | None |

## Pop Cap Rates — Summary

| War Goal | Context | Base Rate | With +50% Raiding Capacity |
|---|---|---|---|
| Raiding | Surrender | 10% | 15% |
| Raiding | Bombardment/Invasion | 20% | 30% |
| Emancipation | Surrender | 10% | 15% |
| Emancipation | Bombardment/Invasion | 30% | 45% |
| Robo-Liberation | Surrender | 10% | 15% |
| Robo-Liberation | Bombardment/Invasion | 30% | 45% |
| Reaping | All | Unlimited | Unlimited |
| Pillage | All | 0% | 0% (resources only) |

**Cap formula:** `(total_pops + already_taken) * rate - already_taken`, min 0.

## Pillaging System

Available to: `civic_barbaric_despoilers`, `civic_gk_barbaric_despoilers_machine`, `civic_gk_barbaric_despoilers_megacorp`, and `civic_crusader_spirit_corporate`.

### Devastation-Driven Process

1. **Damage Banking** — `on_planet_bombarded` and `on_ground_combat_devastation` add `local_devastation` to a per `raider + planet` receipt
2. **Threshold Resolution** — every 10 stored devastation pays out 1 month of the planet's current output immediately for pillage-capable empires (`wg_plunder_raid` multiplies this by 6x for the war-goal side)
3. **Loot Transformation** — Apply efficiency multiplier, then convert:
   - Trade value doubled
   - Unity, Physics, Society, Engineering research all convert to Consumer Goods at 2:1
4. **Remaining Headroom Cashout** — invasion converts the remaining 0-100 devastation headroom on a planet into loot at the planet's current rate, applies a local tribute modifier scaled from half that value, and marks the colony as already cashed out for the relevant surrender owner. Planets that are about to surrender directly to orbital bombardment are resolved from the main bombardment event before ownership flips, with the later conquer hook only clearing the temporary marker. Surrender converts only the remaining 0-50 band on uncashed colonies without applying extra devastation

### Pop-Raiding Side Rules

- Pop capture remains tied to raiding-style war goals (`wg_plunder`, `wg_gk_emancipation`, `wg_gk_robo_liberation`, `wg_gk_reaping`)
- Any empire on that war-goal side that can personally pop-raid may capture pops for itself
- The during-war pop quota is shared across that whole war-goal side, using the side leader's cap rate
- Final surrender pop payouts remain leader-owned

### Resources Pillaged (16 types)

Trade, Energy, Minerals, Food, Consumer Goods, Alloys, Unity, Physics/Society/Engineering Research, Volatile Motes, Exotic Gases, Rare Crystals, Living Metal, Zro, Dark Matter, Nanites.

### Surrender Aftermath: Planet Tribute Tiers

Applied to each surviving colony that still had tribute left to pay when the defender surrendered in `wg_plunder` or `wg_plunder_raid`.

Tier is determined by `effective_remaining = (100 - planet_devastation) / 2` (integer division, always rounds down):

| Modifier | Workforce | Threshold |
|---|---|---|
| `gk_planet_tribute_0` | -5% | effective_remaining 0–9 |
| `gk_planet_tribute_1` | -10% | effective_remaining 10–19 |
| `gk_planet_tribute_2` | -20% | effective_remaining 20–29 |
| `gk_planet_tribute_3` | -30% | effective_remaining 30–39 |
| `gk_planet_tribute_4` | -40% | effective_remaining 40–49 |
| `gk_planet_tribute_5` | -50% | effective_remaining 50 |

Tribute modifiers never downgrade — if a planet already has an equal or higher tier modifier, the new one is skipped.

Colonies already at 100 devastation (effective_remaining = 0) still receive the token tribute tier.
Colonies already fully cashed out by invasion for that same raider are skipped entirely during surrender to prevent double dipping.

Duration: 5 years.

### Loot Receipt Pattern

- `Raider + planet` receipts store the partial devastation bank during active warfare.
- `Raider + country` receipts store total surrender loot for event display and collection.
- Invasion reuses the planet receipt so unspent partial devastation is included before the receipt is destroyed on collection.

## Abduction System

### Pop Eligibility

Must pass all checks:
1. Planet owner is hostile to raider
2. Not virtual species or being purged
3. War goal check — raider must be in a raiding war with this specific defender (or target is primitive/total war). Non-raiding wars (conquest, subjugation, etc.) do NOT allow pop capture
4. Pop type filter: all pops (raiding/reaping), enslaved only (emancipation), robots only (robo-liberation)
5. Robot policy check (both/organics only/robots only)
6. `pop_group_size > 0`

### Per-Iteration Limit

Max 100 pops per abduction loop iteration.

### Destination Planet Weighting

Priority: free housing > free jobs > high habitability (>=70%: x2, >=50%: x1.5). Falls back to raider capital.

### Tracking & Recovery

**Raidee variables:**
- `gk_raidee_plundered` — pops taken in standard/pillage wars
- `gk_raidee_emancipated` — pops taken in emancipation wars

**Recovery modifier** (`gk_plunder_recovery`, scaled by % of pops lost):
- Workforce: up to +100%
- Founder Species Growth: up to +300%

**Decay:** Variables decay 10% yearly with threshold clearing.

## Bombardment Stance: Raiding (vanilla overwrite)

| Setting | Value |
|---|---|
| Planet Damage | 50% |
| Army Damage | 50% |
| Kill Pop Chance | 15% base |
| Min Pops to Kill | 100 |
| Abduct Pops | Yes |

Available to: Nihilistic Acquisition, Barbaric Despoilers, Slavers origin, Khan Successor, or any empire with `gk_can_use_raiding_bombardment`.

## Opinion Modifiers

### Declared Reaping (`opinion_gk_declared_reaping`)

Base: -50. Additional: up to -25/-50 for Egalitarian, -25 for altruist, -50 for Fanatic Xenophile. Max: -200. Decays 1/month.

### Reaped Pops (`opinion_gk_reaped_pops`)

Accumulative per pop. Base -0.05/pop for normal empires, additional penalties for Egalitarian/Xenophile. Max -0.35/pop. Decays 1/month. Floor: -1000.

## Custom Modifiers

| Modifier | Type | Effect |
|---|---|---|
| `gk_raiding_capacity` | Country % | Increases pop capture cap rates |
| `gk_pillage_efficiency` | Country % | Increases resource pillaging yields |
