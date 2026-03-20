# GK Raiding — Effects Reference

Quick reference for player-facing mechanics. Keep this file up to date when war goals, civics, policies, pillaging, or pop-raiding behavior changes.

## Civics

### Emancipators / Liberation Enterprise

Available to: Standard and Megacorp

**Requirements:** Egalitarian + Militarist
**Modifiers:** Army Morale +50%
**Councilor:** Liberation Commander (Commander) — Ship Fire Rate +2%/level
**Effects:** Unlocks the Emancipation policy option and war goal. With the Robots Only raiding policy, emancipation wars can target synthetic citizen rights instead.

### Harvest Incorporated

Available to: Megacorp only

**Requirements:** Militarist + (Authoritarian or Xenophobe), not Xenophile
**Modifiers:** Slave Bonus Workforce +10%, Purge Workforce +100%
**Councilor:** Renderings Director (Commander / Official) — Livestock Trade +0.25/level, Purge Trade +1.00/level
**Effects:** Grants Raiding and Pillaging CBs. Unlocks Raiding, Reaping, and Pillage war goals. Can pillage resources.

### Harvesting Protocol

Available to: Machine Intelligence only

**Modifiers:** Organic Battery Energy +1, Organic Battery Unity +1, Legion Node XP +25%
**Effects:** Starts with Grid Amalgamated organic battery pops. Grants Raiding and Pillaging CBs. Unlocks Raiding, Reaping, and Pillage war goals. Can pillage resources.

### Hive Bodysnatcher (vanilla civic, enhanced)

Available to: Hive Mind only

**Effects:** Vanilla effects plus: Grants pop raiding access, raiding bombardment stance, and reaping war goal.

## Nihilistic Acquisition

The ascension perk grants pop raiding access and the raiding bombardment stance, same as Barbaric Despoilers. However, Nihilistic Acquisition does **not** grant Reaping. To fully depopulate an empire, spend Influence to authorize deeper raids through the escalation system.

Nihilistic Acquisition works with any raiding policy combination:

- **Driven Assimilator** with Plunder: raid any pops, assimilate them on arrival
- **Rogue Servitor** with Plunder + Organics Only: rescue organic pops for bio-trophies, leave robots behind
- **Rogue Servitor** with Emancipation + Organics Only: specifically target enslaved organics
- **Materialist** with Plunder + Robots Only: steal robots from other empires
- **Egalitarian** with Emancipation: liberate enslaved pops through force
- **Egalitarian** with Emancipation + Robots Only: demand synthetic citizen rights from the target

Reaping is reserved for Barbaric Despoiler civics and Hive Bodysnatcher. These empires don't need Influence to take everything, but the galaxy will hate them for it.

## Policies

### Raiding Focus

Cannot be changed while at war. Governs pop-raiding war goals only; does not disable pillaging.

- **Plunder**: Standard pop-raiding. Bucket-based escalation with Influence costs.
- **No Pop-Raiding**: Disables pop-raiding war goals entirely.
- **Emancipation**: Targets enslaved pops only. Can demand abolition of slavery or synthetic rights (with Robots Only policy).
- **Reaping**: Removes all pop capture limits and prevents surrender. Available to Barbaric Despoiler civics and Hive Bodysnatcher only.

### Robot Raiding

Cannot be changed while at war. Only available to empires with pop-raiding access.

- **Capture Robots**: Organics and robots
- **Organics Only**: Skip robotic pops
- **Robots Only**: Only robotic pops (requires Materialist, Synthetic empire, Cybernetic ascension, or Machine Intelligence)

## Pop Raiding Escalation

Pop raiding uses a tiered bucket system. Each tier captures a portion of the target population:

| Tier | Capture Rate | Cumulative |
|------|-------------|-----------|
| 0 | 10% | 10% |
| 1 | 12.5% | 21% |
| 2 | 16.7% | 34% |
| 3 | 25% | 50% |
| 4 | 50% | 75% |
| 5 | 100% | 100% |

When a tier is filled, the war leader chooses:

- **Hold position** — Pause raiding, reassess in one year
- **Authorize deeper raids** — Spend Influence to unlock the next tier
- **Switch to pillaging** (Plunder only) — Stop pop raids, activate resource pillaging with +1 loot month bonus
- **Demand tribute** (Plunder only) — Send a resource demand. If accepted, Influence refunded. If refused, raiding continues.
- **Demand abolition** (Emancipation) — Demand slavery be outlawed
- **Demand synthetic rights** (Emancipation + Robots Only) — Demand full AI citizen rights

Influence costs scale with how significant the raid is relative to the raider's empire size. Small raids against minor empires are cheap. Major raids against large empires cost substantially more.

With sufficient intel on the target, the escalation popup shows estimated eligible pops remaining.

**Reaping** bypasses all tiers. No limits, no surrender, significant galaxy-wide opinion penalty.

## War Goals

| War Goal | CB | Pop Type | Cap | Surrender | Pillage |
|---|---|---|---|---|---|
| **Raiding** (vanilla OW) | Despoliation | All | Bucket escalation | Bucket remainder | Separate system |
| **Pillage** (vanilla OW) | Pillaging | None | — | Surrender tribute | +2 loot-months |
| **Emancipation** | Emancipation | Enslaved | Bucket escalation | Bucket remainder | No |
| **Reaping** | Despoliation | All | Unlimited | All | No |

## Opinion

| Modifier | Base | Decay | Notes |
|----------|------|-------|-------|
| Declared Reaping War | -100 | 0.5/month | Galaxy-wide on declaration |
| Raided Pops | -0.025/pop | 1/month | Galaxy-wide, accumulative |
| Escalated Raids | -12/press | 1/month | Galaxy-wide, plunder only |
| Raided Our Population | -25/application | 0.5/month | Target only |

All modifiers exclude fallen empires and homicidal empires. Ethics bonuses (egalitarian, xenophile) add extra penalties.

## Pillaging

Resource pillaging is available to empires with **Barbaric Despoilers**, **Harvesting Protocol**, **Harvest Incorporated**, **Letters of Marque**, or the **Despoliation** tradition adoption. Pillaging works in **any hostile war**.

- Loot scales with what the planet actually produces. Doubling trade and converting Research/Unity to CGs
- Bombardment and ground combat both generate loot, Invasions cash out whatever a planet had left to give
- The **Pillage** war goal doubles to triples resources from raiding and grants surrender tribute
- Invaded colonies receive a 5-year workforce penalty (-5% to -50%) based on how much was extracted

**Pillage Yield** stacks from multiple sources:

| Source | Yield |
|--------|-------|
| Base | 2 |
| Pillage war goal | +3 |
| Despoliation tradition | +1 |

Higher yield means more resources per devastation tick and harsher workforce penalties on invaded worlds.

## Invasion and Occupation

Occupied enemy planets are automatically raided each month during war. Transfer rate: 50 base + 10 per offensive army on the planet.

Multi-raider invasions distribute captured pops proportionally among each army's owner. Allies without pop-raiding capability redirect their share to the war leader.

## Tradition Tree — Despoliation

Available to any default empire. Uses the Unyielding 3+2 layout.

**Adoption**
- Enables resource pillaging, even without a native pillage civic
- Unlocks the **Pillaging** casus belli and **Pillage** war goal
- Unlocks the **Recovery Fleets** council agenda (active: Salvage +10%, Ship Alloys Upkeep -5%; finish: Salvage +30%, Ship Alloys Upkeep -10%)
- If the empire already has native pillaging, adoption instead adds +2 effective loot-months in all wars

**Traditions**
1. **Raider's Fervor** — While at war: Happiness +10%, Unity +25%
2. **Predatory Bombardment** — Orbital Bombardment Damage +20%, Army Collateral Damage +50%
3. **Triumph in Ruin** — Gain 1 month of unity output per 10 devastation inflicted, prorated
4. **Boarding Cables** — Unlocks Research & Scavenge Debris policy option. Ship Alloys Upkeep -5%, Building Refund +10%, Megastructure Dismantle Refund +10%. Salvage Chance +10% with Scavenger civics. Grants the **Boarding Cables** technology with Grand Archive DLC.
5. **Acquisitive Officers** — Grants or upgrades Corsair and Shipbreaker traits on admiral-commanders. Ship-kill resource rewards +50% (stacks to 2.25x with Hell's Heart).

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
- **Debris Scavenging**: Battles during raids generate debris. The enclave auto-salvages debris at raid end, with a 30% base chance to recover ships per debris field.
- **Conversion**: Patrons can convert between mercenary and privateer enclaves via the diplomacy menu for 100 Influence. Upgrade ranks are preserved.
- **Cancel Raid**: The raid initiator can recall an active raid at no cost through the diplomacy menu.
- **Raid Pricing**: Funded raids use fleet-value-based pricing, matching mercenary fleet hire costs.
- AI empires found privateer enclaves based on ethics (militarist and xenophobe weighted, never pacifist).
