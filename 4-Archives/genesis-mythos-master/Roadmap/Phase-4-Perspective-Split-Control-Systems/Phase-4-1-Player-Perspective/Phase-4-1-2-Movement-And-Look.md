---
title: Phase 4.1.2 — Movement and Look
roadmap-level: tertiary
phase-number: 4
subphase-index: "4.1.2"
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

## Phase 4.1.2 — Movement and Look

WASD (or configurable) + look (mouse/gamepad); movement respects simulation (collision, terrain). Look drives camera orientation only; no decoupled free-cam. Mid-technical: interfaces and algorithm sketches.

### Tasks

- [ ] **Movement input** — Map WASD (or configurable bindings) to movement intent (forward/back, strafe) in player space. Optional: run modifier, crouch. Send to simulation so movement is authoritative (collision, slope, physics).
- [ ] **Look input** — Mouse delta or gamepad right stick → yaw/pitch (or quaternion). Clamp pitch to avoid flip. Look drives camera and player entity orientation together (first-person: same).
- [ ] **Simulation respect** — Movement resolved by simulation layer (collision, terrain height, triggers). No client-side prediction requirement for MVP; optional later. Contract: input → intent; simulation advances entity; camera follows.

### Interface sketch

- **PlayerInput** (raw): `move_delta: Vec2`, `look_delta: Vec2`, `run: bool`, `interact: bool`. Produced by input loop (Phase 4.1.5).
- **Movement resolution**: Simulation consumes move_delta + current position → new position (collision, terrain). Look_delta → new yaw/pitch on player entity. Camera rig reads entity transform.
