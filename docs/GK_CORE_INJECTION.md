# GK Core Inline Injection Framework

Decentralized system for injecting content into shared vanilla overwrites across GK mods. Any subset of GK mods can be loaded together without conflicts, and adding a new mod requires zero changes to existing ones.

## Quick Start

### Using an existing injection point

Your mod wants to add something to the soldier job. GK mod ID 5.

1. Define your compat variable:
   ```
   # common/scripted_variables/mymod_compat.txt
   @gk_mod_5_active = 1
   ```

2. Create your adapter:
   ```
   # common/inline_scripts/gk_core/mod_5.txt
   inline_script = { script = $DIR$/mymod_$SUFFIX$ }
   ```

3. Ship your content:
   ```
   # common/inline_scripts/jobs/mymod_soldier.txt
   triggered_planet_modifier = {
       potential = { exists = owner owner = { has_valid_civic = civic_mymod_something } }
       trade_value_add = 1
   }
   ```

4. Copy the shared boilerplate from any existing GK mod:
   - `gk_core/mod_loop.txt`
   - `gk_core/if_active.txt`
   - `gk_core/if_active_0.txt`
   - `gk_core/if_active_1.txt`

5. Copy the shared soldier overwrite: `common/pop_jobs/gk_soldier_OW.txt`

That's it. No other mod needs updating.

### Creating a new injection point

Adding the loop to a new overwrite (e.g. enforcer job):

```
enforcer = {
    ...vanilla definition...
    inline_script = { script = gk_core/mod_loop N = 1 DIR = jobs SUFFIX = enforcer }
}
```

Copy the overwrite to all GK mods that might be loaded standalone. Each mod ships its content at `jobs/<modname>_enforcer.txt`.

## Mod ID Registry

| ID | Mod | Variable |
|----|-----|----------|
| 1  | GK Empires Expanded | `@gk_mod_1_active` |
| 2  | GK Raiding | `@gk_mod_2_active` |
| 3  | GK Rubberbanding | `@gk_mod_3_active` |
| 4-10 | Available | |

## How It Works

### The loop

`mod_loop.txt` recurses from N=1 to N=10. At each step it checks `@gk_mod_N_active`. If the variable is 1 (mod loaded), it includes that mod's adapter which routes to the content file. If 0 (mod not loaded or variable undefined), it hits the empty `if_active_0.txt` and the content path is never resolved.

```
mod_loop(N=1)
  → @gk_mod_1_active = 1? → mod_1.txt → jobs/gk_ec_soldier.txt
  → @gk_mod_1_active = 0? → (empty)
→ mod_loop(N=2)
  → @gk_mod_2_active = 1? → mod_2.txt → jobs/gk_raiding_soldier.txt
  → ...
→ mod_loop(N=10) → @[10-10]=0 → stop
```

### The conditional

Based on the community pattern from Gigastructural Engineering. Uses parameter substitution to select between two files:

```
# if_active.txt — routes to _0 or _1 based on toggle
inline_script = { script = gk_core/if_active_$toggle$ code = "$code$" }

# if_active_0.txt — empty (mod absent)
# if_active_1.txt — expands the code parameter
```

### The adapter

Maps numeric mod ID to pretty mod-namespaced paths:

```
# gk_core/mod_2.txt (shipped by gk_raiding)
inline_script = { script = $DIR$/gk_raiding_$SUFFIX$ }
```

DIR and SUFFIX are passed from the original `mod_loop` call, so the same adapter works for any injection point (soldier, enforcer, buildings, etc.).

## File Layout

```
<any_gk_mod>/common/
  inline_scripts/
    gk_core/
      mod_loop.txt        # Shared boilerplate (identical in all mods)
      if_active.txt       # Shared boilerplate
      if_active_0.txt     # Shared boilerplate
      if_active_1.txt     # Shared boilerplate
      mod_<ID>.txt        # Unique adapter per mod
    jobs/
      <modname>_soldier.txt   # Content injected into soldier job
      <modname>_enforcer.txt  # Content injected into enforcer job
  pop_jobs/
    gk_soldier_OW.txt    # Shared overwrite (identical in all mods)
  scripted_variables/
    <modname>_compat.txt  # @gk_mod_<ID>_active = 1
```

## Credits

Pattern based on TTFTCUTS' conditional inline_script invention and the Gigastructural Engineering loop design. Community mod compatibility conventions from the [Stellaris Mod Compatibility Spreadsheet](https://docs.google.com/spreadsheets/d/1wbKhAVczL0By2F2D9dDy5WC-do3XqguNuj-dms9vzIo/).
