---
title: Phase 4.2.1 — Free-Cam God-View
roadmap-level: tertiary
phase-number: 4
subphase-index: "4.2.1"
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

## Phase 4.2.1 — Free-Cam God-View

Single DM camera rig: free-flight (orbit, pan, zoom, tilt, soar, dive). Halo Forge–style or Sparky-inspired input mapping. No first-person lock; full 3D navigation for the DM. Mid-technical: interfaces and algorithm sketches.

### Tasks

- [ ] **DM camera rig contract** — One free-flight rig for DM role only. Position and orientation fully controllable; not bound to any entity. Inputs: orbit, pan, zoom, tilt, soar, dive (mapped to Halo Forge–style or Sparky-inspired bindings).
- [ ] **Input mapping** — Map keyboard/mouse/gamepad to flight axes and speeds. Document default bindings and allow remapping via config or UI.
- [ ] **No first-person lock** — DM rig never switches to player first-person; keep clear boundary from Phase 4.1 player camera.

### Interface sketch

- **DMCameraRig**: free-flight controller; position (Vec3), orientation (Quat or yaw/pitch/roll). Methods: `orbit(delta)`, `pan(delta)`, `zoom(delta)`, `tilt(angle)`, `soar(delta)`, `dive(delta)`. Updated each frame from input layer.
- **Scene graph**: DM camera as separate node; not a child of any entity. Switchable with orthographic rig (Phase 4.2.2) via interpolator (Phase 4.2.3).

## Depth-4 tasks

- [[Phase-4-2-1-1-DM-Camera-Rig-Contract]] — API contract, invariants, edge cases.
- [[Phase-4-2-1-2-Input-Mapping]] — Default bindings, remap, tick pseudo-code.
- [[Phase-4-2-1-3-No-First-Person-Lock]] — Role boundary, get_active_view_matrix guard.
