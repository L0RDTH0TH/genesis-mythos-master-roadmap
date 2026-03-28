---
title: Phase 4.2.3.2 — No-Snap Invariant
roadmap-level: task
phase-number: 4
subphase-index: "4.2.3.2"
project-id: genesis-mythos-master
status: archived
progress: 0
created: 2026-03-10
tags: [roadmap, genesis-mythos-master, phase, task]
para-type: Archive
links:
  - "[[Phase-4-2-3-Mode-Interpolation]]"
---

## Phase 4.2.3.2 — No-Snap Invariant

Avoid instant cuts; always interpolate so the DM retains spatial awareness when toggling. Depth-4: implementation guard and tests.

### Invariant

- **No direct rig switch:** The active view matrix must never jump from source rig to target rig in a single frame without going through the interpolator. Toggle handler must call `interpolator.interpolate(source, target, duration)` and then drive view from `interpolator.update(dt)` until `done`.

### Pseudo-code (DM view update)

```text
each frame:
  if interpolator.done:
    active_rig = (current_mode == ORTHO) ? ortho_rig : free_cam_rig
    view_matrix = active_rig.get_view_matrix()
  else:
    state = interpolator.update(dt)
    view_matrix = state_to_view_matrix(state)
```

### Edge cases

- **Rapid toggle:** If user toggles again before transition completes, either (a) cancel and start new transition from current interpolated state to the other rig, or (b) queue the toggle and apply when current transition finishes. Document chosen behavior (recommend (a) for responsiveness).
- **Min duration:** Ensure `duration_sec >= 0.05` so at least one or two frames of interpolation run; avoids "snap" when frame rate is very high.
