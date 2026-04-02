---
title: Phase 4 — Perspective Split and Control Systems
roadmap-level: primary
phase-number: 4
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-29
tags: [roadmap, genesis-mythos-master, phase]
para-type: Project
links:
  - "[[genesis-mythos-master-Roadmap-2026-03-29-1730]]"
handoff_readiness: 70
handoff_gaps:
  - "Primary-only slice after restart; add secondaries on deepen"
---

## Phase 4 — Perspective Split and Control Systems

Lock players to first-person interaction; give DMs Sparky-style free flight plus orthographic tabletop for tactical work; share one scene graph across rigs with a camera interpolator module for smooth FOV/position/rotation transitions and future modality (e.g. VR) as optional swaps.

- [ ] Player rig contract (movement, look, interaction ray).
- [ ] DM rig contract (free-cam + ortho toggle + input mapping).
- [ ] Interpolator module API and easing presets.
- [ ] Role-based visibility and authority rules (anti-cheat / trust model sketch).

## Subphases & notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```
