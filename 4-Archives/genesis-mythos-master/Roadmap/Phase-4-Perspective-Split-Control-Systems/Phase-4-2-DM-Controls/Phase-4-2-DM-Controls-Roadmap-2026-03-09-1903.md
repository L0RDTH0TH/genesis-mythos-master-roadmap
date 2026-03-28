---
title: Phase 4.2 — DM Controls
roadmap-level: secondary
phase-number: 4
subphase-index: "4.2"
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

## Phase 4.2 — DM Controls

Free-cam god-view (Sparky-style flight, orbiting, panning, zooming) and orthographic tabletop toggle for tactical precision. DMs command with effortless dominion; mode switches use smooth interpolation. High-level: interfaces and contracts for the DM rig and input path.

- [ ] **Free-cam god-view** — Single DM camera rig: free-flight (orbit, pan, zoom, tilt, soar, dive). Halo Forge–style or Sparky-inspired input mapping. No first-person lock; full 3D navigation.
- [ ] **Orthographic tabletop toggle** — Instant seamless transition to orthographic / top-down view for tactical work (token placement, measurements, fog, line-of-sight). Clean, flat, ruler-precise.
- [ ] **Mode interpolation** — Smooth transitions (position, rotation, FOV) with natural easing when switching between free-cam and orthographic. Keep flow unbroken.
- [ ] **Input loop seam** — DM input (flight, toggle, tools) flows into DM intent path only; isolated from player intent (Phase 4.1.5). Document boundary.

## Tertiary notes

```dataview
TABLE WITHOUT ID
  roadmap-level AS "Level",
  file.link AS "Note",
  subphase-index AS "Index",
  status,
  progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-Control-Systems/Phase-4-2-DM-Controls"
WHERE roadmap-level = "secondary" OR roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
