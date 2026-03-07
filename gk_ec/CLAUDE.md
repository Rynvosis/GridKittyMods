# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Vanilla Stellaris Install Path

`/home/ryn/.local/share/Steam/steamapps/common/Stellaris/`

Use this as the source of truth for vanilla game files when comparing overrides.

## Project Overview

**ryn_misc** is a kitchen-sink Stellaris overhaul mod targeting v4.3.0. It contains a variety of independent features — civics, origins, system initializers, gameplay tweaks, etc. Features are loosely related and do not necessarily depend on each other.

## Naming Conventions

- **`gk_ec_`** prefix on all entities (buildings, events, triggers, effects, modifiers, values, variables, initializers). Use this prefix for all new content.
- **`GK_EC_`** prefix for localisation keys.
- **`OW` suffix** on filenames that partially overwrite vanilla content.
- Full/Partial file overwrites should include a `# Version last updated:` comment header and details of what was ovewritten
- Civic variants use suffixes: `_megacorp`, `_hive`, `_machine`. Building variants use `_gestalt`.
- Event namespaces: `gk_ec_<feature>.<number>`. IDs are allocated in blocks of 100 per feature (0-99 = misc).

## Ethics & Civics Suite (GK_EC)

This mod includes a bespoke ethics & civics suite branded **GK_EC** (GridKitty Ethics and Civics).

- **Hierarchy axis**: Authoritarian/Egalitarian remains the naming, but the design emphasis is **hierarchy vs liberties/anti-caste** rather than authority type.
- **Ownership axis**: Individualist vs Collectivist focuses on **private vs collective ownership of production**. Trade/diplomacy demands are secondary flavor, not the core identity.
- **Factions** are keyed with `gk_ec_` identifiers; demand localisation uses `GK_EC_` keys.

## Localisation

Only English. Files in `localisation/english/` must be UTF-8 with BOM and use the `l_english:` header.

## Maintenance

- **`docs/EFFECTS.md`**: Keep this file updated whenever ethic modifiers, civic effects, faction demands, councilor bonuses, living standard overrides, or other gameplay effects are added or changed. Update the relevant table/section after each modification.
