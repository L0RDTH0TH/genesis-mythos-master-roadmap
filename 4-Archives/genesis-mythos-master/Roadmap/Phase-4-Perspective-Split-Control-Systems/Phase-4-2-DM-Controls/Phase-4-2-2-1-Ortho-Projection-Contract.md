---
title: Phase 4.2.2.1 — Ortho Projection Contract
roadmap-level: task
phase-number: 4
subphase-index: "4.2.2.1"
project-id: genesis-mythos-master
status: archived
progress: 0
created: 2026-03-09
tags: [roadmap, genesis-mythos-master, phase, task]
para-type: Archive
links:
  - "[[Phase-4-2-2-Orthographic-Tabletop-Toggle]]"
---

## Phase 4.2.2.1 — Ortho Projection Contract

Define orthographic camera parameters and constraints. Depth-4: pseudo-code/API.

### API sketch

```ts
interface DMOrthoRig {
  position: Vec3;        // world-space focus point (XZ plane)
  height: number;        // distance above plane
  ortho_size: number;    // half-extent in world units
  rotation: Quat;        // usually straight-down, optionally tilted

  set_focus(point: Vec3): void;
  set_height(meters: number): void;
  set_ortho_size(units: number): void;
  get_view_matrix(): Mat4;
}
```

- **Constraint:** When in ortho mode, projection is orthographic with no perspective; grid lines should maintain constant spacing on screen (no foreshortening).

### Edge cases

- **Zoom limits:** Clamp `ortho_size` to a safe range (e.g. `min_size` for close tactical work, `max_size` to avoid huge single tiles).
- **Tilted ortho:** If a slight tilt is allowed (for style), preserve near top-down axis; do not allow free pitch/roll that turns it into pseudo-perspective.
