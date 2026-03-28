---
title: Phase 4.1.1 — First-Person Camera Lock
roadmap-level: tertiary
phase-number: 4
subphase-index: "4.1.1"
project-id: genesis-mythos-master
status: archived
priority: high
progress: 0
created: 2026-03-09
tags: [roadmap, genesis-mythos-master, phase, subphase]
para-type: Archive
links:
  - "[[Phase-4-1-Player-Perspective-Roadmap-2026-03-09-1854]]"
---

## Phase 4.1.1 — First-Person Camera Lock

Single active camera rig: fixed first-person (no orbit, no god-view). Position and orientation bound to player entity; no toggle to other perspectives for players. Mid-technical: interfaces and algorithm sketches.

### Tasks

- [ ] **Camera rig contract** — One active camera per player; rig type = first-person only. No second camera, no perspective switch. Position = player entity position (with optional offset for eye height); orientation = player look direction.
- [ ] **Binding to player entity** — Camera transform updated every frame from player entity transform (or from a dedicated "head" node if entity has skeleton). No decoupling; player and camera move as one.
- [ ] **No escape** — Disable any UI or input that would switch to top-down, third-person, or free-cam for the player role. Document that DM role uses a different rig (Phase 4.2).

### Interface sketch

- **PlayerCameraRig**: position, rotation from **PlayerEntity**; read-only. `get_position(): Vec3`, `get_rotation(): Quat` (or yaw/pitch). Updated by simulation or input layer each tick.
- **Scene graph**: One camera node child of player entity (or driven by same transform). No alternate camera stack for player view.
