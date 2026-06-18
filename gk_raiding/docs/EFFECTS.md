# GK Raiding — Effects Reference

Quick reference for player-facing mechanics. Keep this file up to date when war goals, civics, policies, plundering, or pop-raiding behavior changes.

## Civics

The raiding civics form a matrix: every empire type has a **pop-raiding** lane (abduct populations) and a **resource-raiding** lane (plunder stockpiles via the Plundering stance). Some civics cover both.

| Empire | Pop-raid | Resource-raid |
|---|---|---|
| **Standard** | Barbaric Despoilers *(vanilla)* / Emancipators | **Reavers** |
| **Megacorp** | Harvest Incorporated / Liberation Enterprise | **Letters of Marque** *(vanilla)* |
| **Machine** | Harvesting Protocol *(does both)* | Harvesting Protocol / **Corsair Protocol** |
| **Hive** | **Ravager Swarm** *(does both)* | **Ravager Swarm** |
| **Nomad** | — | Void Reavers *(vanilla)* |

Resource-raid civics grant native plundering: the Plundering bombardment stance, the Plunder CB (`cb_pirate_raid`), and the `wg_plunder_raid` war goal — all routed through the single `gk_can_plunder` access trigger. They also grant a commander trait, per civic: **Reavers** → the **Plunderer** trait (eligible Commanders only — not Pacifist, not Xenophile); **Corsair Protocol** → the **Shipbreaker** trait (any Commander); **Ravager Swarm** → no commander trait. Letters of Marque and Void Reavers grant their own equivalent traits in vanilla, so the mod does not double-add to them.

### Emancipators / Liberation Enterprise

Available to: Standard and Megacorp

**Requirements:** Egalitarian + Militarist
**Modifiers:** Army Morale +50%
**Councilor:** Liberation Commander (Commander) — Ship Fire Rate +2%/level
**Effects:** Unlocks pop raiding access and the raiding bombardment stance. With Slavery banned, can select the Emancipation raiding focus.

### Harvest Incorporated

Available to: Megacorp only

**Requirements:** Militarist + (Authoritarian or Xenophobe), not Xenophile
**Modifiers:** Slave Bonus Workforce +10%, Purge Workforce +100%
**Councilor:** Renderings Director (Commander / Official) — Livestock Trade +0.25/level, Purge Trade +1.00/level
**Effects:** Grants Raiding and Plundering CBs. Unlocks Raiding, Reaping, and Plunder war goals. Can plunder resources.

### Harvesting Protocol

Available to: Machine Intelligence only

**Modifiers:** Organic Battery Energy +1, Organic Battery Unity +1, Legion Node XP +25%
**Effects:** Starts with Grid Amalgamated organic battery pops. Grants Raiding and Plundering CBs. Unlocks Raiding, Reaping, and Plunder war goals. Can plunder resources.

### Reavers

Available to: Standard (non-corporate, non-gestalt)

**Requirements:** (Militarist or Authoritarian), not Pacifist
**Modifiers:** Ship Upkeep −5% (with Overlord: also +1 Enclave Capacity)
**Effects:** Native resource plundering — Plundering stance, Plunder CB, and the `wg_plunder_raid` war goal. Eligible Commanders gain the Plunderer trait. Plunders resources only; cannot abduct pops. The non-corporate counterpart to vanilla Letters of Marque.

### Letters of Marque (vanilla civic)

Available to: Megacorp

Vanilla `civic_crusader_spirit_corporate`. Grants the Corsair ("Material Liberator") commander trait, native plundering, and +1 Enclave Capacity with Overlord. The mod routes it through the same `gk_can_plunder` access as the other resource-raiders. No mod changes to the civic itself (Corsair is its Plunderer-equivalent, so Plunderer is not added).

### Corsair Protocol

Available to: Machine Intelligence (not Servitor / Assimilator / Exterminator)

**Modifiers:** Ship Upkeep −5%, Ship Weapon Damage +5%, Ship Capture Chance +10%
**Effects:** Native resource plundering — Plundering stance, Plunder CB, and the `wg_plunder_raid` war goal. Commanders gain the **Shipbreaker** trait (alloys from destroyed ships — fitting its ship-breaking theme). The **+10% ship-capture chance** gives it a shot at stealing enemy ships it destroys in combat, via the base game's ship-capture mechanic (Privateer Enclave raid fleets get +30%).

### Ravager Swarm

Available to: Hive Mind (not Devouring Swarm)

**Modifiers:** Purge Workforce +100%, Food Jobs +10%
**Effects:** Combined raider — grants **both** pop-raiding (Raiding and Reaping CBs/war goals, raiding bombardment stance) **and** resource plundering (Plundering stance, Plunder CB). Raided populations are processed as biomass for workforce and food. Replaces the old Bodysnatcher hack — vanilla Hive Bodysnatcher no longer grants any raiding access.

## Nihilistic Acquisition

The ascension perk grants pop raiding access and the raiding bombardment stance, same as Barbaric Despoilers. Xenophobe empires with Nihilistic Acquisition can also select the Reaping focus.

Nihilistic Acquisition works with any raiding policy combination:

- **Driven Assimilator** with Raiding: raid any pops, assimilate them on arrival
- **Rogue Servitor** with Raiding + Organics Only: rescue organic pops for bio-trophies, leave robots behind
- **Rogue Servitor** with Emancipation + Organics Only: specifically target enslaved organics
- **Materialist** with Raiding + Robots Only: steal robots from other empires
- **Egalitarian** with Emancipation: liberate enslaved pops through force
- **Xenophobe** with Reaping: no limits, no surrender

Reaping is available to Xenophobe empires with Barbaric Despoiler civics or Nihilistic Acquisition, plus Harvesting Protocol and Ravager Swarm unconditionally. These empires don't need Influence to take everything, but the galaxy will hate them for it.

## Policies

### Raiding Focus

Cannot be changed while at war. Governs pop-raiding war goals only; does not disable plundering.

- **Raiding**: Standard pop-raiding. Bucket-based escalation with Influence costs.
- **Emancipation**: Targets enslaved pops only. Can demand abolition of slavery. Requires Slavery to be banned (or Rogue Servitor).
- **Reaping**: Removes all pop capture limits and prevents surrender. Available to Barbaric Despoiler civics and Ravager Swarm only.

### Robot Raiding

Cannot be changed while at war. Only available to empires with pop-raiding access.

- **Capture Robots**: Organics and robots
- **Organics Only**: Skip robotic pops
- **Robots Only**: Only robotic pops (requires Materialist, Synthetic empire, Cybernetic ascension, or Machine Intelligence). Incompatible with Emancipation focus.

## Pop Raiding Escalation

Pop raiding uses a tiered bucket system. Each tier is a cumulative cap on how much of the target population you can have captured so far:

| Tier | Cumulative Cap |
|------|----------------|
| 0 | 10% |
| 1 | 25% |
| 2 | 50% |
| 3 | 100% |

When a tier is filled, the war leader chooses:

- **Hold position** — Pause raiding, reassess in one year
- **Authorize deeper raids** — Spend Influence to unlock the next tier
- **Switch to plundering** (Raiding only) — Stop pop raids, switch war goal to Plunder. Plundering this target then steals +20% of output per tick instead of the +40% of a declared Plunder war.
- **Authorize total depopulation** (Raiding only, tier 5) — Switch war goal to Reaping. No surrender, no limits.
- **Demand tribute** (Raiding only) — Send a resource demand. If accepted, Influence refunded and war goal switches to Humiliation. If refused, raiding continues.
- **Demand abolition** (Emancipation) — Demand slavery be outlawed. If accepted, war goal switches to Humiliation.

Influence costs scale with how significant the raid is relative to the raider's empire size. Small raids against minor empires are cheap. Major raids against large empires cost substantially more.

With sufficient intel on the target, the escalation popup shows estimated eligible pops remaining.

**Reaping** bypasses all tiers. No limits, no surrender, significant galaxy-wide opinion penalty.

## Opportunistic Raiding

A raiding war goal auto-authorizes raiding only against the **enemy-side war leader** — the empire actually named by the casus belli. Every other target (co-belligerent defenders of a raiding war, or any enemy in a non-raiding war) requires opportunistic authorization.

The first time a raid vector fires against an unauthorized target (bombardment tick in raiding stance, ground-invasion win, or monthly auto-raid on an occupied planet), a prompt appears:

- **Authorize** — Spend 50 Influence. That target becomes raidable for the rest of the war. Escalation tier costs against this target are 2× normal.
- **Decline** — No raiding against this target for the next 5 years. The flag also clears when the war ends, so a future war prompts you again.

Invasion bursts against an unauthorized target do not capture pops on the winning tick; once authorized, the following monthly auto-raid picks up the occupied planet. Escalation popups for opportunistic targets omit Pivot to Plundering, Demand Tribute, and Demand Reforms — those options only apply to primary raiding-war targets.

## War Goals

| War Goal | CB | Pop Type | Cap | Surrender | Plunder |
|---|---|---|---|---|---|
| **Raiding** (vanilla OW) | Despoliation | All | Bucket escalation | Bucket remainder | Separate system |
| **Plunder** (vanilla OW) | Plundering | None | — | Surrender tribute | +2 loot-months |
| **Emancipation** | Emancipation | Enslaved | Bucket escalation | Bucket remainder | No |
| **Reaping** | Despoliation | All | Unlimited | All | No |

## Opinion

| Modifier | Base | Decay | Notes |
|----------|------|-------|-------|
| Declared Reaping War | -100 | 0.5/month | Galaxy-wide on declaration |
| Raided Pops | -0.025/pop | 1/month | Galaxy-wide, accumulative. Raiding/Reaping focus only — Emancipation raids generate no galaxy-wide opinion. |
| Escalated Raids | -12/press | 1/month | Galaxy-wide, raiding only |
| Raided Our Population | -25/application | 0.5/month | Target only, applies regardless of raid focus |

All modifiers exclude fallen empires and homicidal empires. Ethics bonuses (egalitarian, xenophile) add extra penalties.

## Plundering

Resource plundering is available to empires with **Barbaric Despoilers**, **Harvesting Protocol**, **Harvest Incorporated**, **Letters of Marque**, or the **Despoliation** tradition adoption. Plundering happens **through bombardment**: select the **Plundering** bombardment stance — vanilla's own stance, which the mod opens to any empire that can plunder (so there is one shared plunder stance, not a parallel mod one) — and you steal a slice of the planet's output each tick. The mod uses vanilla's `steal_planet_output` engine effect, so loot is the enemy's **actual resources**, scaled to the target's real economy.

Three loot vectors:

- **Bombardment (Plundering stance):** each tick (throttled to once per 30 days per bombarding fleet, and suppressed by planetary defenders) steals a percentage of the planet's **current** monthly output. The take naturally tapers as devastation suppresses the planet's production — no devastation gate, no hard cliff. Percentage (capped at 100%):

| Source | Steal % |
|--------|---------|
| Base | 40% |
| Plunder war goal (`wg_plunder_raid`) | +40% (or +20% if pivoted-to-plundering) |
| Native despoilator | +20% |

- **Invasion (conquest):** winning a ground invasion plunders **~a year's worth** of the planet's output in one shot (the same composition × 12 months, uncapped — drawn from the enemy's stockpile).
- **Surrender (Plunder war goal):** steals **50% of the loser's entire stockpile** (all stored resources).

There is no post-war "Ransacked" colony debuff or re-plunder lockout — plundering simply tapers as devastation suppresses output, and a planet can be plundered again whenever it is producing.

## Invasion and Occupation

Occupied enemy planets are automatically raided each month during war. Transfer rate: 50 base + 10 per offensive army on the planet.

Multi-raider invasions distribute captured pops proportionally among each army's owner. Allies without pop-raiding capability redirect their share to the war leader.

## Tradition Tree — Despoliation

Available to any default empire. Uses the Unyielding 3+2 layout.

**Adoption**

- Enables resource plundering, even without a native plunder civic
- Unlocks the **Plundering** casus belli and **Plunder** war goal
- Unlocks the **Recovery Fleets** council agenda (active: Salvage +10%, Ship Alloys Upkeep -5%; finish: Salvage +30%, Ship Alloys Upkeep -10%)
- If the empire already has native plundering, adoption instead adds +2 effective loot-months in all wars

**Traditions**

1. **Raider's Fervor** — Orbital Bombardment Army Damage +50%. Each destroyed enemy ship and army grants Unity, scaled by the size of what you killed. The Unity-per-kill is delivered by events on ship/army destruction, not by a static modifier.
2. **Forward Raiding Bases** — For **non-nomad** empires, unlocks the **Forward Raiding Base** starbase building (one per starbase): it raids **3%** of output from nearby **non-ally** colonies within 3 systems each tick (the skim quietly runs twice). For **nomad** empires it grants the three **pirate waystation modules** instead (Pirate Hideout / Concealment Field / Reaver Stronghold); **Void Reavers** instead get **+50% pirate-waystation collection** via their swap. Pirate-waystation access is also extended to the Letters of Marque (corporate) and the hive/machine resource-plunder civics when they're nomadic.
3. **Restless Raiders** — Stability from staying at war. Won a war in the last 10 years: +10 stability and -15% amenity usage. At war, or any war within the last 10 years: +5 stability. After 20 years of unbroken peace: -5 stability.
4. **Boarding Cables** — Salvage Chance +10%. Grants the **Boarding Cables** technology with Grand Archive DLC. With the technology, **nomad** empires can construct **Boarding Cables** on an arkship (one per arkship) from the arkship's Auxiliary build slots, equipping three boarding cables for a chance to steal defeated ships and capture enemy commanders.
5. **Acquisitive Officers** — A commander gains **one of** three traits: **Plunderer** (vanilla, trade — only for non-xenophile/non-pacifist commanders), **Corsair** ("Material Liberator", energy), or **Shipbreaker** (alloys); Plunderer is simply skipped in the draw when the commander is ineligible. Commanders who already hold Corsair/Shipbreaker are upgraded toward their tier-2 versions instead. Ship-kill resource rewards +50% (stacks to 2.25x with Hell's Heart) — Corsair (energy), Shipbreaker (alloys), and Plunderer (trade).

**Finish:** Ascension Perks +1. With **Overlord** DLC: +1 Enclave Capacity and unlocks **Privateer Enclaves**. Without Overlord: Ship Fire Rate +5%, Army Damage +10%. Mindwardens get +2 Enclave Capacity instead. Fanatic Purifiers always get the combat bonuses.

## Privateer Enclave

Requires **Overlord** DLC.

Founded by completing the **Despoliation** tradition finisher. Uses a mercenary enclave slot. Not available to Mindwardens or Fanatic Purifiers. The enclave inherits one ethic from its patron alongside Fanatic Militarist.

Six personality types assigned at founding (Automaton, Stoic, Screamer, Cultist, Calculating, Merchant), some gated by patron ethics.

- Raids autonomously each month (25% base chance, scaling with upgrades to 50%) and pays dividends on a recurring cycle
- Patron can fund raids against rivals and purchase services (intelligence, Smuggler's Port, mercenary armies) through the diplomacy menu
- Five upgrade tiers increase fleet size, raid frequency, and dividend payouts
- Enclave fleets: +15% speed, +10% weapon damage, +5%/day hull regen, +5%/day armor regen
- **Smuggler's Port**: Purchasable starbase building. +20% Trade from Jobs in-system, produces 4 Trade Value per Trade Hub on the starbase, +5 Crime empire-wide.
- **Ship Capture**: Privateer raiders have a 30% chance to capture enemy ships they destroy during raids, adding them to the raider fleet.
- **Conversion**: Patrons can convert between mercenary and privateer enclaves via the diplomacy menu for 100 Influence. Upgrade ranks are preserved.
- **Cancel Raid**: The raid initiator can recall an active raid at no cost through the diplomacy menu.
- **Raid Pricing**: Funded raids use fleet-value-based pricing, matching mercenary fleet hire costs.
- AI empires found privateer enclaves based on ethics (militarist and xenophobe weighted, never pacifist).
