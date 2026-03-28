---
title: Phase 4.2.1.3 — No First-Person Lock (DM Boundary)
roadmap-level: task
phase-number: 4
subphase-index: "4.2.1.3"
project-id: genesis-mythos-master
status: archived
progress: 0
created: 2026-03-09
tags: [roadmap, genesis-mythos-master, phase, task]
para-type: Archive
links:
  - "[[Phase-4-2-1-Free-Cam-God-View]]"
---

## Phase 4.2.1.3 — No First-Person Lock (DM Boundary)

DM rig never switches to player first-person; keep clear boundary from Phase 4.1 player camera. Depth-4: invariants and implementation guard.

### Invariant

- **Active camera source:** At any time, exactly one of `PlayerCameraRig` (Phase 4.1) or `DMCameraRig` (this phase) drives the rendered view for the local client, depending on **role**.
- **No shared rig:** There is no "current camera" that can be toggled between player and DM; there are two separate rigs. Role selects which rig's `get_view_matrix()` is used.

### Implementation guard

```ts
function get_active_view_matrix(role: Role): Mat4 {
  if (role === 'player') return player_camera_rig.get_view_matrix();
  if (role === 'dm')     return dm_camera_rig.get_view_matrix();
  throw new Error('Unknown role');
}
```

- **UI/input:** No button or shortcut in the DM flow that "attaches" the DM camera to a player entity or switches to first-person. Any "spectate player" feature must be a separate optional rig (e.g. Phase 4.2.x optional), not the default DM free-cam.

### Edge cases

- **Role change mid-session:** On switch DM → player, ensure input is routed to player intent path (Phase 4.1.5) and view matrix from PlayerCameraRig; no residual DM input affecting player.
- **Replay / observer:** If a third role (e.g. observer) is added later, it must not reuse the player first-person rig without explicit design; keep DM/player boundary documented.
