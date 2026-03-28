---
title: Phase 4.2.3 — Mode Interpolation
roadmap-level: tertiary
phase-number: 4
subphase-index: "4.2.3"
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

## Phase 4.2.3 — Mode Interpolation

Smooth transitions (position, rotation, FOV) with natural easing when switching between free-cam and orthographic. Keep flow unbroken. Mid-technical: interfaces and algorithm sketches.

### Tasks

- [ ] **Interpolation contract** — Given source and target camera state (position, rotation, projection type, FOV/ortho size), animate over a short duration (e.g. 0.2–0.5s) with configurable easing (ease-in-out or similar).
- [ ] **No snap** — Avoid instant cuts; always interpolate so the DM retains spatial awareness when toggling.
- [ ] **Swappable easing** — Module or parameter for easing curve (linear, ease-in-out, custom) per Roadmap Structure; allow future VR/AR views to plug different behavior.

### Interface sketch

- **CameraInterpolator**: `interpolate(source_rig, target_rig, duration_sec, easing?)`. Output: camera state per frame until complete. Caller (DM input loop) drives current camera from interpolator output during transition.
- **Easing**: Enum or function: linear, ease_in_out_quad, etc. Default: ease_in_out for natural feel.

## Depth-4 tasks

- [[Phase-4-2-3-1-Interpolation-Contract]] — CameraState API, duration, projection switch.
- [[Phase-4-2-3-2-No-Snap-Invariant]] — No direct rig switch; interpolator-driven view.
- [[Phase-4-2-3-3-Swappable-Easing]] — EasingFn, config, VR/AR pluggable.
