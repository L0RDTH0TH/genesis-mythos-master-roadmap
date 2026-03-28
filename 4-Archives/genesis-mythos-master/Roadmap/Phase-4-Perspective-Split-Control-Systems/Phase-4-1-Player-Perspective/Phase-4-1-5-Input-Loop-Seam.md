---
title: Phase 4.1.5 — Input Loop Seam
roadmap-level: tertiary
phase-number: 4
subphase-index: "4.1.5"
project-id: genesis-mythos-master
status: archived
priority: high
progress: 0
created: 2026-03-09
tags: [roadmap, genesis-mythos-master, phase, subphase]
para-type: Archive
links:
  - "[[Phase-4-1-Player-Perspective-Roadmap-2026-03-09-1854]]"
  - "[[Phase-4-Perspective-Split-Control-Systems-Roadmap-2026-03-08-2358]]"
---

## Phase 4.1.5 — Input Loop Seam

Player input flows into a single intent/command path consumed by simulation and rendering. Document the seam so DM and player inputs stay isolated; Phase 4.2 consumes DM-side. Mid-technical: interfaces and algorithm sketches.

### Tasks

- [ ] **Single intent path (player)** — All player input (movement, look, interact, hotkeys) is collected in one place and emitted as **PlayerIntent** (or command list) each frame. No direct coupling to simulation from raw input; simulation reads intent.
- [ ] **Role-based routing** — When active role = player, input goes to player intent path. When active role = DM, input goes to DM control path (Phase 4.2). Switch only on role change (session or debug); no mid-session mix.
- [ ] **Consumers** — Simulation consumes movement/look intent to advance player entity. Interaction system consumes interact intent + raycast result. Rendering consumes nothing directly; it reads entity/camera state.
- [ ] **Documentation** — Document the boundary: raw input → [role router] → player intent OR DM intent. No cross-leak; DM cannot inject into player intent and vice versa.

### Interface sketch

- **InputRouter**: `set_active_role(role: "player" | "dm")`, `poll() -> PlayerIntent | DMIntent`. Single source of truth for which path is active.
- **PlayerIntent**: `move_delta`, `look_delta`, `interact`, `hotkeys[]`. Filled each frame from raw input when role = player. Consumed by simulation and interaction.
