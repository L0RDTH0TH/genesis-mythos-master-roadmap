---
title: Phase 4.2.2.2 — Tactical Tools in Ortho Mode
roadmap-level: task
phase-number: 4
subphase-index: "4.2.2.2"
project-id: genesis-mythos-master
status: archived
progress: 0
created: 2026-03-09
tags: [roadmap, genesis-mythos-master, phase, task]
para-type: Archive
links:
  - "[[Phase-4-2-2-Orthographic-Tabletop-Toggle]]"
---

## Phase 4.2.2.2 — Tactical Tools in Ortho Mode

Wire token placement, rulers, fog-of-war, and LOS tools to orthographic view. Depth-4: interaction pseudo-code.

### Token placement

```text
on_left_click_ortho(position_screen):
  world = ortho_unproject(position_screen)
  if tool == PLACE_TOKEN:
    place_token(world)
```

- `ortho_unproject` uses DMOrthoRig view/projection to map screen coords to world XZ.

### Ruler / measurement

```text
on_drag_ortho(start_screen, end_screen):
  if tool == RULER:
    a = ortho_unproject(start_screen)
    b = ortho_unproject(end_screen)
    distance = length(a - b)
    show_ruler(a, b, distance)
```

### Fog-of-war and LOS

- **Fog brush:** Map brush radius in world units via ortho projection; apply to fog mask texture or tile grid.
- **LOS:** Cast rays in world space from token position over heightmap/obstacles, but present result as shaded shapes in ortho view.

### Edge cases

- Tool input is ignored when not in ortho mode; free-cam uses different tools or none.
