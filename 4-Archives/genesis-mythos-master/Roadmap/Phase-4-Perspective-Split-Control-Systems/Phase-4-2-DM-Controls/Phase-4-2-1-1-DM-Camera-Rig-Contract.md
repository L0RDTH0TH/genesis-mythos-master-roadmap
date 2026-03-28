---
title: Phase 4.2.1.1 — DM Camera Rig Contract
roadmap-level: task
phase-number: 4
subphase-index: "4.2.1.1"
project-id: genesis-mythos-master
status: archived
progress: 0
created: 2026-03-09
tags: [roadmap, genesis-mythos-master, phase, task]
para-type: Archive
links:
  - "[[Phase-4-2-1-Free-Cam-God-View]]"
---

## Phase 4.2.1.1 — DM Camera Rig Contract

One free-flight rig for DM role only. Position and orientation fully controllable; not bound to any entity. Depth-4: pseudo-code and API contract.

### API contract

```ts
interface DMCameraRig {
  readonly position: Vec3;
  readonly orientation: Quat;  // or yaw, pitch, roll
  orbit(delta_theta: number, delta_phi?: number): void;
  pan(delta_x: number, delta_y: number): void;
  zoom(delta: number): void;
  tilt(angle_rad: number): void;
  soar(delta: number): void;   // forward in look direction
  dive(delta: number): void;   // backward in look direction
  get_view_matrix(): Mat4;
}
```

- **Invariant:** `position` and `orientation` are writable only via the six methods (no direct set from outside). Input layer calls these each frame from DM bindings.
- **Scene graph:** Rig is not a child of any entity node; it is a standalone camera controller. Renderer uses `get_view_matrix()` for the active DM view.

### Edge cases

- **Gimbal lock:** Use quaternion for orientation; avoid euler (yaw/pitch/roll) in storage to prevent gimbal lock at poles.
- **Zoom limits:** Clamp zoom (e.g. min 0.1, max 1000) to avoid near-plane clipping or numerical instability.
- **Role switch:** When switching from DM to player (if supported), freeze DM rig state; do not reset. Restore on switch back.
