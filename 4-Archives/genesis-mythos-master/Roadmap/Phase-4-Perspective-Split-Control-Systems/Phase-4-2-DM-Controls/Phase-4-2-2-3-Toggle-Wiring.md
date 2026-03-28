---
title: Phase 4.2.2.3 — Toggle Wiring & UX
roadmap-level: task
phase-number: 4
subphase-index: "4.2.2.3"
project-id: genesis-mythos-master
status: archived
progress: 0
created: 2026-03-09
tags: [roadmap, genesis-mythos-master, phase, task]
para-type: Archive
links:
  - "[[Phase-4-2-2-Orthographic-Tabletop-Toggle]]"
---

## Phase 4.2.2.3 — Toggle Wiring & UX

Wire a single input/UI toggle between free-cam and ortho, using the interpolator (Phase 4.2.3). Depth-4: state machine and pseudo-code.

### State machine

States: `FREE_CAM`, `TRANSITION_TO_ORTHO`, `ORTHO`, `TRANSITION_TO_FREE`.

```text
on_toggle_pressed():
  if state == FREE_CAM:
    start_transition(free_cam_rig, ortho_rig)
    state = TRANSITION_TO_ORTHO
  elif state == ORTHO:
    start_transition(ortho_rig, free_cam_rig)
    state = TRANSITION_TO_FREE
```

- During transition, input is still accepted but applied cautiously (e.g. disable big jumps).

### Interpolator usage

```text
update(dt):
  if state in [TRANSITION_TO_ORTHO, TRANSITION_TO_FREE]:
    camera_state = interpolator.update(dt)
    if interpolator.done:
      state = ORTHO if state == TRANSITION_TO_ORTHO else FREE_CAM
  else:
    camera_state = (free_cam_rig or ortho_rig).get_view_matrix()
```

### UX details

- Show subtle on-screen hint when in ortho (icon or label).
- Debounce toggle input (e.g. min 0.2s between presses) to avoid rapid flipping.
