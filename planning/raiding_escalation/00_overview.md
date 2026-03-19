# Raiding Escalation System — Overview

## Problem

The current percentage-based pop caps (10%/20%/30% by war type) feel arbitrary. The number is invisible to the defender, decided by the modder, and creates friction in multiplayer where limits need manual coordination. The system should feel like a natural part of the game where the *player* decides how far to push.

## Core Idea

- **Flat 10% base cap** for all non-reaping war types
- **When cap is reached**, event popup fires with escalation options
- **Repeatable** — each press costs more influence
- **Bucket is per-war, not per-raider** — all allies in the same war share the same bucket tracker against the defender. Robot-only raiders and take-all raiders both contribute equally since buckets are based on total pops.
- **Reaping stays unlimited + anti-surrender** — Barbaric Despoilers identity. With escalation, any raider can push to 100%, but only reapers prevent the defender from surrendering early (-1000 acceptance).

## Phasing

- [x] **Phase 1**: Bucket formula + escalation event (consolidate + press the raid only) + surrender updates. Core mechanic.
- [x] **Phase 2**: Pivot to Pillaging + Demand options (tribute, reforms, autonomy). Intel hook on escalation popup.
- [x] **Phase 3**: Civic/wargoal simplification, opinion overhaul, gestalt support, deprecation stubs.
- **Phase 4**: Update `EFFECTS.md`, `WORKSHOP_DESCRIPTION.bbcode`, and regenerate workshop showcase images (via `/mod-showcase` skill). See [Screenshot Changes](#screenshot-changes) below.

## Hard Rule

**gk_raiding must have zero knowledge of or dependency on gk_ec.** No references to gk_ec ethics, civics, mechanics, or files. All gk_raiding features must work with vanilla Stellaris alone.

## What Stays Unchanged

- Pillaging system (own devastation-tier mechanics)
- Reaping (unlimited, no escalation needed)
- Total war bypasses caps
- Primitives uncapped
- Loot receipts, decay
- `gk_raidee_plundered` / `gk_raidee_emancipated` tracking (future use for catch-up mechanic)

## Screenshot Changes

When regenerating showcase images (`/mod-showcase gk_raiding`), the following screenshots need to be retaken. Grouped by page.

### Page 1: Pop Raiding + Pillaging

| Screenshot | What changed | Notes |
|------------|-------------|-------|
| `surrender.png` | Old shows "770 pops, 10% cap". Now bucket-based with different cap display. Surrender acceptance changed from -50 to -75 for emancipation/robo-lib. | Retake with new surrender tooltip showing bucket-based numbers |
| `pop_raiding.png` | Pop Raiding game concept text likely updated to describe escalation/bucket system | Retake game concept tooltip |
| `wg_raiding.png` | War goal tooltip updated with new escalation estimates | Retake |
| `captives.png` | "Captives Taken" notification may show different numbers with proportional distribution | Retake |

### Page 2: Civics

| Screenshot | What changed | Notes |
|------------|-------------|-------|
| `civic_harvest_inc.png` | Harvest Incorporated reworked: new ethics requirements (Auth/Xenophobe), new modifiers (purge workforce +100%, livestock/purge trade value), renamed councilor | Retake civic tooltip |
| `iconbox_harvest_inc.png` | Icon may need refresh if civic icon changed | Check if DDS changed |
| `civic_robo.png` | **Phase 3 will delete this civic entirely.** Keep for now, replace when robo-lib is removed | No action yet |
| `wg_robo.png` | **Phase 3 will delete this war goal.** Keep for now | No action yet |
| `wg_reaping.png` | Reaping war goal tooltip may show updated text (bucket references, -1000 acceptance) | Retake |
| `wg_emanc.png` | Emancipation war goal tooltip, surrender acceptance changed to -75 | Retake |

### Page 3: Despoliation Tradition Tree

| Screenshot | What changed | Notes |
|------------|-------------|-------|
| `finisher.png` | Finisher reworked with DLC-aware swaps (Overlord gates enclave capacity, fallback to combat bonuses) | Retake finisher tooltip |
| `tree.png` | Tree overview may show updated finisher text | Retake |
| `adoption.png` | Check if adoption text changed | Verify, retake if needed |
| `perk_*.png` | Corsair trait rename (privateer -> corsair) may affect perk text | Check each perk for trait references |

### Page 4: Privateer Enclave

| Screenshot | What changed | Notes |
|------------|-------------|-------|
| `smuggler_name.png` | Starbase building reworked (removed trading hub requirement, changed modifier) | Retake building name/tooltip |
| `smuggler_tip.png` | Same | Retake |
| `comms.png` | Incoming Transmission may have updated text | Verify |
| `raid_complete.png` | Privateer raid events changed | Verify, retake if text differs |
| `plundered_cargo.png` | Plundered Cargo event may have changed | Verify |
| `tooltip.png` | Enclave tooltip description may reference new features (scavenging, corsair rename) | Retake |

### New screenshots needed

| Feature | Suggested screenshot | Page |
|---------|---------------------|------|
| Escalation event popup | `escalation.png` showing Consolidate vs Press the Raid options | Page 1 (new tile) |
| Bucket cap notification | Message showing bucket completion / cap reached | Page 1 (new tile) |
| Debris scavenging | Privateer scavenge event or notification | Page 4 (new tile) |
| Livestock/purge econ | Harvest Inc job output with new modifiers | Page 2 (optional) |
