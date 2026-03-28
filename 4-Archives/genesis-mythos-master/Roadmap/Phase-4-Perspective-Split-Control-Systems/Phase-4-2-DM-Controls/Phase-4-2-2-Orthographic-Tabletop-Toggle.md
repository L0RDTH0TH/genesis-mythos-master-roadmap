---
title: Phase 4.2.2 — Orthographic Tabletop Toggle
roadmap-level: tertiary
phase-number: 4
subphase-index: "4.2.2"
project-id: genesis-mythos-master
status: archived
priority: high
progress: 0
created: 2026-03-09
tags: [roadmap, genesis-mythos-master, phase, subphase]
para-type: Archive
links:
  - "[[Phase-4-2-DM-Controls-Roadmap-2026-03-09-1903]]"
---

## Phase 4.2.2 — Orthographic Tabletop Toggle

Instant seamless transition to orthographic / top-down view for tactical work: token placement, measurements, fog, line-of-sight. Clean, flat, ruler-precise. Mid-technical: interfaces and algorithm sketches.

### Tasks

- [ ] **Orthographic projection contract** — DM can switch to orthographic projection; camera looks straight down (or configurable angle) at the play surface. No perspective distortion; uniform scale for measurements.
- [ ] **Tactical use cases** — Support token placement, ruler/measurements, fog-of-war painting, line-of-sight checks. Document as primary use for this mode.
- [ ] **Toggle trigger** — Single input or UI action to switch between free-cam and orthographic; transition handled by interpolator (Phase 4.2.3).

### Interface sketch

- **DMOrthoRig**: orthographic projection; position (XZ or world plane), fixed rotation (top-down or configurable), ortho size/scale. Same world state as free-cam; only projection and lock differ.
- **Camera interpolator**: Receives source rig (free-cam or ortho) and target rig; interpolates position, rotation, FOV/projection over time (Phase 4.2.3).

## Depth-4 tasks

- [[Phase-4-2-2-1-Ortho-Projection-Contract]] — Ortho params and constraints.
- [[Phase-4-2-2-2-Tactical-Tools]] — Tokens, rulers, fog, LOS in ortho.
- [[Phase-4-2-2-3-Toggle-Wiring]] — Toggle state machine and interpolator wiring.
