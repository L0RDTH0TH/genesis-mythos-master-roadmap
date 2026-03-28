---
title: Phase 3 — Living Simulation and Dynamic Agency
roadmap-level: primary
phase-number: 3
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-19
tags: [roadmap, genesis-mythos-master, phase]
para-type: Project
subphase-index: "3"
links:
  - "[[genesis-mythos-master-roadmap-2026-03-19-1101]]"
---

## Phase 3 — Living Simulation and Dynamic Agency

Build a decoupled simulation loop for weather, NPC schedules, and faction-level consequences that persist over time. Introduce explicit boundaries for DM live edits versus structural regeneration to preserve both control and systemic integrity.

- [ ] Implement core simulation tick scheduler
- [ ] Add DM overwrite controls with regeneration gates
- [ ] Validate persistence and consequence propagation across sessions

## Subphases & notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```
