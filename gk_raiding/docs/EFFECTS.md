# GK Raiding — Effects Reference

Quick reference for player-facing mechanics. Keep this file up to date when war goals, civics, policies, pillaging, or pop-raiding behavior changes.

## Civics

### Emancipators / Liberation Enterprise

Available to: Standard and Megacorp

**Requirements:** Egalitarian + Militarist
**Modifiers:** Army Morale +50%
**Councilor:** Liberation Commander (Commander) — Ship Fire Rate +2%/level
**Effects:** Unlocks the Emancipation policy option and war goal

### Robo-Liberators / Synthetic Liberation Corp

Available to: Standard and Megacorp

**Councilor:** Synthetic Rights Advocate (Scientist / Commander) — Robot Upkeep -2%/level, Robot Happiness +1%/level
**Effects:** Unlocks the Robo-Liberation policy option and war goal

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

### Freedom Directive

Available to: Machine Intelligence only

**Modifiers:** Robot Upkeep -15%, Pop Assembly +10%, Legion Node XP +25%
**Effects:** Unlocks the Robo-Liberation policy option and war goal

## Policies

### Raiding Focus

Cannot be changed while at war. Only governs pop-raiding; does not disable pillaging.

- **Plunder**: Standard pop-raiding setup
- **No Pop-Raiding**: Disables pop-raiding war goals
- **Emancipation**: Unlocks **Emancipation** war goal access
- **Robo-Liberation**: Unlocks **Robo-Liberation** war goal access

**Letters of Marque** does not use this policy (pillaging-only).

### Robot Raiding

Cannot be changed while at war. Only available to empires with pop-raiding access.

- **Capture Robots**: Organics and robots
- **Organics Only**: Skip robotic pops
- **Robots Only**: Only robotic pops

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

## War Goals

All pop-raiding war goals use the **Despoliation** casus belli.

| War Goal | Pop Type | During-War Cap | Surrender Cap | Pillage |
|---|---|---|---|---|
| **Raiding** (vanilla OW) | All | 20% | 10% | Separate system, no tribute |
| **Pillage** (vanilla OW) | None | — | — | +4 loot-months, surrender tribute |
| **Emancipation** | Enslaved | 30% | 15% | No |
| **Robo-Liberation** | Robotic | 30% | 15% | No |
| **Reaping** | All | Unlimited | Unlimited | No |

- Pillage-capable empires can still pillage resources during any war via the separate pillaging system.
- Surrender tribute is exclusive to the Pillage war goal.
- During-war pop quotas are shared across all allies on the same war-goal side.

## Pillaging

Resource pillaging is available to empires with **Barbaric Despoilers**, **Harvesting Protocol**, **Harvest Incorporated**, **Letters of Marque**, or the **Despoliation** tradition adoption. Pillaging works in **any hostile war**.

- Loot scales with what the planet actually produces. Doubling trade and converting Research/Unity to CGs
- Bombardment and ground combat both generate loot, Invasions cash out whatever a planet had left to give
- The **Pillage** war goal doubles to triples resources from raiding and grants surrender tribute
- Invaded colonies receive a 5-year workforce penalty (-5% to -50%) based on how much was extracted

## Privateer Enclave

Requires **Overlord** DLC.

Founded by completing the **Despoliation** tradition finisher. Uses a mercenary enclave slot. Not available to Mindwardens or Fanatic Purifiers. The enclave inherits one ethic from its patron alongside Fanatic Militarist.

Six personality types assigned at founding (Automaton, Stoic, Screamer, Cultist, Calculating, Merchant), some gated by patron ethics.

- Raids autonomously each month (25% base chance, scaling with upgrades to 50%) and pays dividends on a recurring cycle
- Patron can commission raids against rivals and purchase services (intelligence, Smuggler's Port, mercenary armies) through the diplomacy menu
- Five upgrade tiers increase fleet size, raid frequency, and dividend payouts
- Enclave fleets: +15% speed, +10% weapon damage, +5%/day hull regen, +5%/day armor regen
- **Smuggler's Port**: Purchasable starbase building. +20% Trade from Jobs in-system, produces 4 Trade Value per Trade Hub on the starbase, +5 Crime empire-wide.
- **Debris Scavenging**: Battles during raids generate debris. The enclave auto-salvages debris at raid end, with a 30% base chance to recover ships per debris field.
