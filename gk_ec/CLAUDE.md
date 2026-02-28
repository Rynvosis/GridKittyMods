# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**ryn_misc** is a kitchen-sink Stellaris overhaul mod targeting v4.3.0. It contains a variety of independent features — civics, origins, system initializers, gameplay tweaks, etc. Features are loosely related and do not necessarily depend on each other.

## Naming Conventions

- **`rec_`** prefix on nearly all entities (buildings, events, triggers, effects, modifiers, values, variables, initializers). Use this prefix for all new content.
- **`OW` suffix** on filenames that overwrite vanilla content. These should include a `# Version last updated:` comment header.
- Civic variants use suffixes: `_megacorp`, `_hive`, `_machine`. Building variants use `_gestalt`.
- Event namespaces: `rec_<feature>.<number>`. IDs are allocated in blocks of 100 per feature (0-99 = misc).

## Scripting Patterns

### Country Modifier Accumulator
Buildings can contribute values to a country-level scripted modifier, which capital buildings then read via script values to determine job counts. This decouples per-planet contributions from the formula that consumes them.

### Government-Type Variants
Civics have standard + megacorp variants (sometimes hive/machine too). Standard civics producing Unity swap to Trade Value for megacorp. Buildings use `convert_to` for capital/colony auto-transformation. Civics use `alternate_civic_version` for government type transitions.

### Coordinate Geometry Library
`rec_values.txt` and `rec_triggers.txt` implement 2D geometry using only distance measurements (law of cosines, cross products) since Stellaris doesn't expose coordinates or trig. Used for procedural hyperlane generation.

## Localisation

Only English. Files in `localisation/english/` must be UTF-8 with BOM and use the `l_english:` header.
