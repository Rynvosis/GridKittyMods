# GK Raiding — Effects Reference

Quick reference for the current GK Raiding mechanics. Keep this file up to date when war goals, civics, policies, pillaging, or pop-raiding behavior changes.

## Overview

GK Raiding now runs as two separate systems:

- **Pillaging** is a resource-only system. Empires that pass `gk_can_pillage` can strip resources from hostile colonies in any war through devastation and invasion.
- **Pop Raiding** is a pop-only system. It is gated by explicit raiding war goals and personal pop-raiding capability.

The two systems now have separate event flows, separate notifications, and separate storage:

- **Pillaging** uses loot receipts.
- **Pop Raiding** uses dedicated pop trackers.

## Civics

### Emancipators / Liberation Enterprise

Available to: Standard (`civic_gk_emancipators`) and Megacorp (`civic_gk_emancipators_megacorp`)

**Requirements:** Egalitarian + Militarist

| Modifier | Value |
|---|---|
| Army Morale | +50% |
| Raiding Capacity | +50% |

**Councilor:** Liberation Commander (Commander)
- Ship Fire Rate: +2% per level

**Effects**
- Unlocks the Emancipation policy option
- Unlocks the Emancipation war goal

### Robo-Liberators / Synthetic Liberation Corp

Available to: Standard (`civic_gk_robo_liberators`) and Megacorp (`civic_gk_robo_liberators_megacorp`)

| Modifier | Value |
|---|---|
| Raiding Capacity | +50% |

**Councilor:** Synthetic Rights Advocate (Scientist / Commander)
- Robot Upkeep: -2% per level
- Robot Happiness: +1% per level

**Effects**
- Unlocks the Robo-Liberation policy option
- Unlocks the Robo-Liberation war goal

### Harvest Incorporated

Available to: Megacorp only (`civic_gk_barbaric_despoilers_megacorp`)

| Modifier | Value |
|---|---|
| Slave Market Cost | -20% |
| Slave Bonus Workforce | +10% |

**Councilor:** Acquisitions Director (Commander / Official)
- Slave Market Cost: -4% per level
- Slave Upkeep: -2% per level

**Effects**
- Grants the Raiding and Pillaging casus belli
- Unlocks Raiding, Reaping, and Pillage war goals
- Can pillage resources through `gk_can_pillage`

### Harvesting Protocol

Available to: Machine Intelligence only (`civic_gk_barbaric_despoilers_machine`)

| Modifier | Value |
|---|---|
| Organic Battery Energy | +1 |
| Organic Battery Unity | +1 |
| Legion Node XP | +25% |

**Effects**
- Starts with Grid Amalgamated organic battery pops
- Grants the Raiding and Pillaging casus belli
- Unlocks Raiding, Reaping, and Pillage war goals
- Can pillage resources through `gk_can_pillage`

### Freedom Directive

Available to: Machine Intelligence only (`civic_gk_robo_liberators_machine`)

| Modifier | Value |
|---|---|
| Robot Upkeep | -15% |
| Pop Assembly | +10% |
| Raiding Capacity | +50% |
| Legion Node XP | +25% |

**Effects**
- Unlocks the Robo-Liberation policy option
- Unlocks the Robo-Liberation war goal

## Policies

### Raiding Focus (`gk_raiding_focus`)

Cannot be changed while at war.

| Option | Policy Flag | Effect |
|---|---|---|
| Plunder | `gk_focus_plunder` | Standard pop-raiding setup |
| No Pop-Raiding | `gk_focus_no_pop_raiding` | Disables pop-raiding war goals |
| Emancipation | `gk_focus_emancipation` | Unlocks Emancipation war goal access |
| Robo-Liberation | `gk_focus_robo_liberation` | Unlocks Robo-Liberation war goal access |

This policy only governs the **pop-raiding** side of the mod. It does not disable pillaging for empires that can pillage.

### Robot Raiding (`gk_robot_raiding`)

Cannot be changed while at war.

| Option | Policy Flag | Effect |
|---|---|---|
| Capture Robots | `gk_allow_robot_raiding` | Organics and robots may be captured |
| Organics Only | `gk_forbid_robot_raiding` | Skip robotic pops |
| Robots Only | `gk_robots_only_raiding` | Only robotic pops may be captured |

## War Goals

### Raiding (`wg_plunder`)

Vanilla overwrite. CB: `cb_despoliation`

| Mechanic | Value |
|---|---|
| During-war pop cap | 20% of enemy population, scaled by Raiding Capacity |
| Surrender pop cap | 10% of enemy population, scaled by Raiding Capacity |
| Peace outcome | Pops only |
| Resource surrender tribute | None |

Notes:
- Pillage-capable empires may still pillage resources during the war through the separate pillaging system.
- The war goal itself no longer grants surrender tribute.

### Pillage (`wg_plunder_raid`)

Vanilla overwrite. CB: `cb_pirate_raid`

| Mechanic | Value |
|---|---|
| Pop capture | None |
| Pillage multiplier | 6x devastation-based resource yield for the war-goal side |
| Peace outcome | Guaranteed surrender tribute |

Notes:
- This war goal does not unlock pillaging by itself. It magnifies pillaging for empires that can already pillage.
- Surrender tribute is now exclusive to this war goal.

### Emancipation (`wg_gk_emancipation`)

CB: `cb_despoliation`

| Mechanic | Value |
|---|---|
| Pop type | Enslaved pops only |
| During-war pop cap | 20% of enemy population, scaled by Raiding Capacity |
| Surrender pop cap | 10% of enemy population, scaled by Raiding Capacity |
| Resource surrender tribute | None |

### Robo-Liberation (`wg_gk_robo_liberation`)

CB: `cb_despoliation`

| Mechanic | Value |
|---|---|
| Pop type | Robotic pops only |
| During-war pop cap | 20% of enemy population, scaled by Raiding Capacity |
| Surrender pop cap | 10% of enemy population, scaled by Raiding Capacity |
| Resource surrender tribute | None |

### Reaping (`wg_gk_reaping`)

CB: `cb_despoliation`

| Mechanic | Value |
|---|---|
| Pop type | All sapient pops |
| Pop cap | Unlimited |
| Resource surrender tribute | None |

## Pop Raiding

### Core Rules

- Pop raiding only happens in explicit pop-raiding contexts:
  - `wg_plunder`
  - `wg_gk_emancipation`
  - `wg_gk_robo_liberation`
  - `wg_gk_reaping`
- Pop raiding requires personal pop-raiding capability.
- Non-raiding wars do not grant pop capture, except primitive / total-war style exceptions already handled by the trigger layer.

### Side-Wide Quotas

- During-war pop quotas are tracked by **war-goal side leader vs defender**, not by each allied raider separately.
- Any eligible ally on that side may capture pops for itself.
- Those captures all spend the same shared quota against that defender.
- Final surrender pop payouts remain owned by the war-goal owner.

### Result Reporting

- Invasion and surrender pop outcomes are reported through notification messages.
- No visible invade/surrender popup windows remain in the pop system.

## Pillaging

### Capability

Resource pillaging is available to empires that pass `gk_can_pillage`:

- `civic_barbaric_despoilers`
- `civic_gk_barbaric_despoilers_machine`
- `civic_gk_barbaric_despoilers_megacorp`
- `civic_crusader_spirit_corporate`

If an empire can pillage, it can pillage in **any hostile war**.

### Devastation-Driven Extraction

1. `on_planet_bombarded` and `on_ground_combat_devastation` add `local_devastation` to a per `raider + planet` loot receipt
2. Every 10 stored devastation resolves 1 loot packet
3. Each packet pays out 1 month of the planet's current output immediately
4. In `wg_plunder_raid`, that packet is multiplied by 6 for pillage-capable empires on the war-goal side

### Loot Transformation

After base loot is calculated:

- Trade value is doubled
- Unity converts to Consumer Goods at 2:1
- Physics Research converts to Consumer Goods at 2:1
- Society Research converts to Consumer Goods at 2:1
- Engineering Research converts to Consumer Goods at 2:1

### Invasion Cashout

When a pillage-capable empire seizes a colony by ground victory or forced orbital surrender:

- It cashes out the planet's remaining `0-100` devastation headroom at the current rate
- It does **not** add extra devastation
- It applies a local tribute modifier tier based on half of that remaining headroom
- It marks the colony as already cashed out for the relevant Pillage-war surrender owner, preventing future Pillage-war surrender double dipping

### Surrender Tribute

Only `wg_plunder_raid` grants final surrender tribute.

On surrender:
- Each surviving colony pays from its remaining `0-50` devastation band
- Colonies already cashed out by invasion for that same surrender owner are skipped
- No extra devastation is applied
- A local tribute modifier is applied to colonies that still had tribute left to pay

### Planet Tribute Modifiers

Duration: 5 years

| Modifier | Workforce |
|---|---|
| `gk_planet_tribute_0` | -5% |
| `gk_planet_tribute_1` | -10% |
| `gk_planet_tribute_2` | -20% |
| `gk_planet_tribute_3` | -30% |
| `gk_planet_tribute_4` | -40% |
| `gk_planet_tribute_5` | -50% |

These are local planet aftermath modifiers, not country-wide tribute modifiers.

### Result Reporting

- Daily devastation packets create pillage notifications
- Invasion cashouts create pillage notifications
- Pillage-war surrender tribute creates pillage notifications
- No visible invade/surrender popup windows remain in the pillage system
