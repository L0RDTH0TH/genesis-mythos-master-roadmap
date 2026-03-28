---
title: Phase 4.2.3.3 — Swappable Easing
roadmap-level: task
phase-number: 4
subphase-index: "4.2.3.3"
project-id: genesis-mythos-master
status: archived
progress: 0
created: 2026-03-10
tags: [roadmap, genesis-mythos-master, phase, task]
para-type: Archive
links:
  - "[[Phase-4-2-3-Mode-Interpolation]]"
---

## Phase 4.2.3.3 — Swappable Easing

Module or parameter for easing curve (linear, ease-in-out, custom) per Roadmap Structure; allow future VR/AR views to plug different behavior. Depth-4: API and edge cases.

### Easing API

```ts
type EasingFn = (t: number) => number;  // t in [0,1] -> eased t in [0,1]

const EASING = {
  linear: (t) => t,
  ease_in_out_quad: (t) => t < 0.5 ? 2*t*t : 1 - Math.pow(-2*t + 2, 2)/2,
  ease_in_out_cubic: (t) => t < 0.5 ? 4*t*t*t : 1 - Math.pow(-2*t + 2, 3)/2,
} as const;
```

- **Interpolator usage:** `lerp_position = lerp(src.pos, tgt.pos, EASING[easing](elapsed/duration))`; same for rotation (slerp), FOV/ortho size.
- **Config:** Expose `camera_interpolation_easing` in project or user config (default `ease_in_out_quad`). Optional UI dropdown for "Transition style".

### Extensibility

- **VR/AR:** A future module can register a custom `EasingFn` or replace the interpolator entirely (e.g. teleport-style or fade). Keep `CameraInterpolator` behind an interface so implementations are swappable.
- **No snap:** Easing must be monotonic in t so the camera never "backs up" during a single transition.

### Edge cases

- **Invalid easing key:** Fall back to `ease_in_out_quad` and log warning.
- **Custom easing that returns out-of-range:** Clamp eased t to [0, 1] before lerp to avoid invalid state.
