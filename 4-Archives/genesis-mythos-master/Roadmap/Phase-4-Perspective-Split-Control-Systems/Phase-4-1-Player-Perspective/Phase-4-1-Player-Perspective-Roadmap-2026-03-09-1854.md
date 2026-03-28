---
title: Phase 4.1 — Player Perspective
roadmap-level: secondary
phase-number: 4
subphase-index: "4.1"
project-id: genesis-mythos-master
status: archived
priority: high
progress: 0
created: 2026-03-09
tags: [roadmap, genesis-mythos-master, phase, subphase]
para-type: Archive
links:
  - "[[Phase-4-Perspective-Split-Control-Systems-Roadmap-2026-03-08-2358]]"
---

## Phase 4.1 — Player Perspective

Locked first-person immersion so players experience the world personally—no escape to top-down or third-person. Interaction mechanics: raycasts, sensory feedback, and role-based agency. High-level: interfaces and contracts for the player rig and input loop.

- [ ] **First-person camera lock** — Single active camera rig: fixed first-person (no orbit, no god-view). Position and orientation bound to player entity; no toggle to other perspectives for players.
- [ ] **Movement and look** — WASD (or configurable) + look (mouse/gamepad); movement respects simulation (collision, terrain). Look drives camera orientation only; no decoupled free-cam.
- [ ] **Interaction raycasts** — Raycast from camera/view for "use" or "inspect"; hit detection against interactables (entities, objects, POIs). Define max range, layer mask, and feedback (highlight, prompt).
- [ ] **Sensory and feedback** — Visual/audio feedback for interactions and proximity (e.g. ambient, cues). Optional: simple feedback channel so simulation or narrative can push "sense" events to the player view.
- [ ] **Input loop seam** — Player input flows into a single intent/command path consumed by simulation and rendering; document the seam so DM and player inputs stay isolated (Phase 4.2 consumes DM-side).

## Tertiary notes

```dataview
TABLE WITHOUT ID
  roadmap-level AS "Level",
  file.link AS "Note",
  subphase-index AS "Index",
  status,
  progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-Control-Systems/Phase-4-1-Player-Perspective"
WHERE roadmap-level = "secondary" OR roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
