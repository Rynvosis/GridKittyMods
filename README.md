# GridKitty Mod Suite

A monorepo of mods for [Stellaris](https://www.paradoxinteractive.com/games/stellaris), Paradox's grand-strategy 4X. Each mod lives in its own directory and shares common tooling, documentation, and conventions.

## Published mods

| Mod | Description |
| --- | --- |
| **[GridKitty's Raiding Expanded](https://steamcommunity.com/sharedfiles/filedetails/?id=3686119381)** | A full overhaul of the raiding mechanic — abduct populations, strip planets, and fund a pirate enclave. The suite's flagship, with several thousand Steam Workshop subscribers. |
| **GK Ascension Pacing** | Rebalances the pace of ascension perks and megastructures. |
| **GK Ethics & Civics** | Adds new civics and ethics options for empire-building. |

Additional modules (`gk_lithogenesis`, `gk_rubberbanding`, `gk_primitive_start`, `gk_crisis_among_us`, and compatibility patches) are in development or maintained privately for an ongoing multiplayer roleplay group.

## Repository layout

```
gk_<mod>/
  common/        Stellaris script (civics, war goals, policies, scripted effects/triggers)
  localisation/  UTF-8 (BOM) loc files
  docs/          EFFECTS.md (player-facing mechanics) + Workshop description
  CHANGELOG.md
tools/           Python tooling — showcase image rendering, generators
assets/          Shared icons and source art
```

## Conventions

- `OW` filename suffix marks a partial or full overwrite of vanilla content.
- Localisation files are UTF-8 **with BOM**; concepts use `['concept_name']` syntax.
- Script values are preferred over temporary variables on persistent scopes.
- Conventional commits scoped per mod, e.g. `feat(gk_raiding):`, `fix(gk_ec):`.

## Tooling

`tools/` contains Python utilities for the suite, including a showcase-image renderer and content generators used to keep Workshop art and documentation in sync with the mod data.
