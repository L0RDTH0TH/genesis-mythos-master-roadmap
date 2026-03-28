---
title: Phase 4.2.3.1 — Interpolation Contract
roadmap-level: task
phase-number: 4
subphase-index: "4.2.3.1"
project-id: genesis-mythos-master
status: archived
progress: 0
created: 2026-03-10
tags: [roadmap, genesis-mythos-master, phase, task]
para-type: Archive
links:
  - "[[Phase-4-2-3-Mode-Interpolation]]"
---

## Phase 4.2.3.1 — Interpolation Contract

Given source and target camera state (position, rotation, projection type, FOV/ortho size), animate over a short duration with configurable easing. Depth-4: API and pseudo-code.

### API contract

```ts
interface CameraState {
  position: Vec3;
  rotation: Quat;
  projection: 'perspective' | 'orthographic';
  fov_or_ortho_size: number;  // FOV rad if perspective, half-extent if ortho
}

interface CameraInterpolator {
  interpolate(
    source: CameraState,
    target: CameraState,
    duration_sec: number,
    easing?: EasingFn
  ): void;
  update(dt: number): CameraState | null;  // null when complete
  readonly done: boolean;
}
```

- **Invariant:** While `!done`, caller uses returned `CameraState` for view matrix; when `done`, caller switches to target rig for subsequent frames.
- **Duration:** Default 0.2–0.5s; clamp to [0.05, 2.0] to avoid instant or overly slow transitions.

### Edge cases

- **Projection switch:** When source is perspective and target ortho (or vice versa), interpolate position and rotation; at mid-point or last 10% of duration, cross-fade or snap projection type to avoid invalid intermediate projection.
- **Zero duration:** If `duration_sec <= 0`, set `done = true` and return target state on first `update`.
