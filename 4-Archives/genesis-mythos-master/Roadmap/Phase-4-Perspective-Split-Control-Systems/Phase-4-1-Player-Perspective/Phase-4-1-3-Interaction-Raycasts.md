---
title: Phase 4.1.3 — Interaction Raycasts
roadmap-level: tertiary
phase-number: 4
subphase-index: "4.1.3"
project-id: genesis-mythos-master
status: archived
priority: high
progress: 0
created: 2026-03-09
tags: [roadmap, genesis-mythos-master, phase, subphase]
para-type: Archive
links:
  - "[[Phase-4-1-Player-Perspective-Roadmap-2026-03-09-1854]]"
---

## Phase 4.1.3 — Interaction Raycasts

Raycast from camera/view for "use" or "inspect"; hit detection against interactables (entities, objects, POIs). Define max range, layer mask, and feedback (highlight, prompt). Mid-technical: interfaces and algorithm sketches.

### Tasks

- [ ] **Raycast origin and direction** — From camera position, through view center (or crosshair). Direction = camera forward. Length = max interaction range (e.g. 3–5 m; configurable).
- [ ] **Layer mask / interactables** — Only hit objects on "interactable" layer (or tag). Filter: entities, objects, POI triggers. Ignore terrain-only or decorative by default.
- [ ] **Hit result** — Return hit entity/id, distance, optional surface normal. Consumed by interaction system to show prompt ("Use", "Inspect") and trigger action on key press.
- [ ] **Feedback** — Highlight hit target (outline, glow) and show contextual prompt UI. Optional: distance-based fade of prompt.

### Interface sketch

- **InteractionRaycast**: `cast(origin: Vec3, direction: Vec3, max_dist: float, layer_mask: int) -> Hit?`. Hit: `entity_id`, `distance`, `point`, `normal`.
- **InteractionUI**: `show_prompt(text, target_entity?)`, `hide_prompt()`, `set_highlight(entity_id?)`. Called when raycast hit changes or on interact key.
