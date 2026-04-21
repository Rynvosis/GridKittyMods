# gk_utils — Effects & Console Commands

## Hyperlane graph

### `gk_utils_add_hyperlane_to_target`, `gk_utils_remove_hyperlane_to_target`
System scope. Adds/removes a hyperlane to `event_target:gk_target`. Guarded — idempotent if the hyperlane already exists / is already absent.

### `gk_utils_rewire_neighbors_to`
System scope. Reroutes all hyperlane neighbors of the current system to `event_target:gk_target` via flag-based batching.

### `gk_utils_add_hyperlanes_in_range`
System scope. Connects every system within a given Euclidean range.

### `gk_utils_add_every_non_intersecting_hyperlane`
System scope. Brute-force neighbor scan with intersection-check stub. Geometry helpers in `gk_utils_geometry_effects.txt` back this.

## BFS over hyperlanes

### `gk_utils_bfs_apply`
System scope. Floods a scripted_effect out from a seed system across hyperlane-connected neighbors.

Parse-time parameters:
- `FLAG` — star flag set on every visited system (persists after the call)
- `EFFECT` — scripted_effect name invoked on each visited system in its own scope
- `MAX_DEPTH` — integer hop budget (recommend 10 for most galaxy clusters)

Example — seal a cluster:
```
effect gk_utils_bfs_apply = {
    FLAG = gk_utils_sealed_cluster
    EFFECT = gk_utils_seal_system
    MAX_DEPTH = 10
}
```

Recursion note: the called `EFFECT` runs one scripted_effect level below `gk_utils_bfs_apply`. Stellaris caps the scripted_effect stack at 5, so the passed effect may nest ~3 more levels safely.

## Sealed systems

### `gk_utils_seal_system`
System scope. Marks the system with `gk_utils_sealed_system`, removes all in-system gateways (all states: `gateway_0`, `gateway_ruined`, `gateway_restored`) and L-gates (`lgate_base`).

Wormholes are not removed (no vanilla script primitive exists). Instead, the fleet-entry hook (`gk_utils_seal.1` on `on_entering_system_fleet`) MIAs any arriving fleet, neutralizing all travel vectors — hyperlane, jump drive, quantum catapult, wormhole, and surviving external gateway/L-gate links — uniformly.

Fleets exempt from MIA:
- Starbases and military stations (filtered by ship class — they don't move anyway)
- Non-default country types (crisis, guardians, enclaves, swarm, fallen empires are passed through)
- Fleets that can't go MIA (`can_go_mia = no`)

## Contact sharing

### Share Contact button
Button added to the diplomacy view via `interface/diplomacy_view.gui` (OW of vanilla). Fires button_effect `gk_utils_share_contact_button` which opens a paginated event picker (9 per page) → confirmation window showing the selected empire's portrait → grants `establish_communications` on confirm.

**Overwrites:** `interface/diplomacy_view.gui` — adds an `effectButtonType` below the diplomatic actions list. Must be kept in sync with vanilla updates.

### `gk_utils_contact_build_page`
Country scope. Populates `event_target:gk_contact_0` through `gk_contact_8` with empires the actor knows but `event_target:gk_contact_target` does not. Uses `gk_contact_page` variable for pagination offset. Sets `gk_contact_total`, `gk_contact_page_count`, and `gk_contact_next_start`.

### `gk_utils_contact_cleanup`
Country scope. Removes the `gk_sharing_contacts_with@` tracking flag.

## Role-play utilities

### `event gk_utils_rp.2`
Console command. Sets global flag `gk_utils_rp_galcom_allowed` and kicks off vanilla Galactic Community formation via `galcom.1`.

### Global flag `gk_utils_rp_mp_game`
Set automatically at game start if `is_multiplayer = yes`. Readable via `has_global_flag = gk_utils_rp_mp_game`.
