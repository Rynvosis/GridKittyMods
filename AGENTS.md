# GK Mod Suite — Monorepo

## Structure

Each mod lives in its own directory (`gk_raiding/`, `gk_ec/`, `gk_rubberbanding/`). Each mod has `docs/EFFECTS.md` and `docs/WORKSHOP_DESCRIPTION.bbcode`.

## Conventions

- OW suffix on filenames = partial/full overwrite of vanilla content
- Stellaris loc files must be UTF-8 with BOM
- Concepts in loc use `['concept_name']` syntax (square brackets), NOT `$concept_name$`
- Script values preferred over temp variables on persistent scopes
- `count_owned_pop_amount` requires `complex_trigger_modifier`, cannot use `trigger:` syntax
- Conventional commits: `feat(gk_raiding):`, `fix(gk_raiding):`, `refactor(gk_raiding):`, etc.

## Post-Task Checklist

After completing major tasks, update these files:

1. **`<mod>/CHANGELOG.md`** — Add entries for completed work. If reworking/removing an unpublished feature, reword or remove its existing changelog entry instead of adding "removed X" lines. Use the changelog itself as context for what's published vs unpublished.
2. **`<mod>/docs/EFFECTS.md`** — Update player-facing mechanics reference when civics, war goals, policies, or raiding behavior changes.
3. **`<mod>/docs/WORKSHOP_DESCRIPTION.bbcode`** — Update Steam Workshop description if the mod's feature set changed.
