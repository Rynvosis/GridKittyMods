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
| Pillage tiers on surrender | 2 |
| Pillage resource multiplier | 1x |

### Pillage (`wg_plunder_raid` — vanilla overwrite)

CB: `cb_pirate_raid`. Surrender acceptance: -50.

| Mechanic | Value |
|---|---|
| Pop capture | None (resources only) |
| Pillage tiers on surrender | 6 |
| Pillage resource multiplier | 2x |

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

### Three-Phase Process

1. **Tier Setup** — Set max tiers and resource multiplier based on war goal
2. **Base Loot Calculation** — `production * months_per_tier * tiers`
3. **Loot Transformation** — Apply efficiency multiplier, then convert:
   - Trade value doubled
   - Unity, Physics, Society, Engineering research all convert to Consumer Goods at 2:1

### Resources Pillaged (16 types)

Trade, Energy, Minerals, Food, Consumer Goods, Alloys, Unity, Physics/Society/Engineering Research, Volatile Motes, Exotic Gases, Rare Crystals, Living Metal, Zro, Dark Matter, Nanites.

### Planet Modifier: `gk_pillaged` (per tier, scales with tier count)

| Effect | Per Tier |
|---|---|
| Pop Happiness | -3% |
| Workforce | -6% |
| Stability | +3 |

Tiers decay by 1 per year (paused while planet is occupied by enemy).

### Loot Receipt Pattern

Surrender pillaging uses a hidden leader on `global_event_country` to safely accumulate loot across multiple planets before delivering to the raider in one batch.

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
