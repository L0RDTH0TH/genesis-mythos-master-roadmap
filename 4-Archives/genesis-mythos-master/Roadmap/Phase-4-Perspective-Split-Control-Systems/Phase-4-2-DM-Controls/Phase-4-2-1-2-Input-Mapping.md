---
title: Phase 4.2.1.2 — Input Mapping (Free-Cam)
roadmap-level: task
phase-number: 4
subphase-index: "4.2.1.2"
project-id: genesis-mythos-master
status: archived
progress: 0
created: 2026-03-09
tags: [roadmap, genesis-mythos-master, phase, task]
para-type: Archive
links:
  - "[[Phase-4-2-1-Free-Cam-God-View]]"
---

## Phase 4.2.1.2 — Input Mapping (Free-Cam)

Map keyboard/mouse/gamepad to flight axes and speeds. Document default bindings and allow remapping via config or UI. Depth-4: pseudo-code and edge cases.

### Default binding table (Halo Forge–style)

| Action   | KB default | Mouse     | Gamepad   |
|----------|------------|-----------|-----------|
| Orbit    | -          | LMB drag  | Right stick |
| Pan      | -          | MMB drag  | Left stick  |
| Zoom     | Scroll     | Scroll    | Triggers    |
| Soar     | W          | -         | A (fwd)     |
| Dive     | S          | -         | A (back)    |
| Tilt     | Q / E      | -         | D-pad U/D   |

- **Config:** Bindings stored in a map `action -> input_source_id + axis/button`. Load/save via project or user config file; UI exposes "Remap" for each action.

### Pseudo-code (tick)

```text
each frame:
  if role != DM: skip
  for each action in [orbit, pan, zoom, tilt, soar, dive]:
    raw = input_system.get_axis_or_button(bindings[action])
    apply deadzone(raw) -> value
    dm_rig[action](value * sensitivity[action] * dt)
```

### Edge cases

- **Remap conflict:** Two actions bound to same key → last-saved wins; warn in UI. No runtime conflict resolution (single-owner model).
- **Sensitivity:** Per-action sensitivity (and optional acceleration curve) in config; default 1.0. Clamp to [0.01, 10] to avoid runaway.
