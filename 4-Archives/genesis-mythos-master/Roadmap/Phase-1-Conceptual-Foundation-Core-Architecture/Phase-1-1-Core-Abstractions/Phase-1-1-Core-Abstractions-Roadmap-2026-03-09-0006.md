---
title: Phase 1.1 — Core Abstractions
roadmap-level: secondary
phase-number: 1
subphase-index: "1.1"
project-id: genesis-mythos-master
status: archived
priority: high
progress: 0
created: 2026-03-09
tags: [roadmap, genesis-mythos-master, phase, subphase]
para-type: Archive
links:
  - "[[Phase-1-Conceptual-Foundation-Core-Architecture-Roadmap-2026-03-08-2358]]"
---

## Phase 1.1 — Core Abstractions

Separate world state, simulation logic, rendering, and input handling into decoupled layers. Define clear boundaries and interfaces so the procedural generation graph and intent population pipeline can plug in without coupling. This secondary sets the architectural skeleton for Phase 1.

- [ ] Define world-state dimensions, ownership, and sync points
- [ ] Define simulation tick contract and headless boundaries
- [ ] Define rendering and input abstraction boundaries

## Tertiary notes

```dataview
TABLE WITHOUT ID
  roadmap-level AS "Level",
  file.link AS "Note",
  subphase-index AS "Index",
  status,
  progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-Core-Architecture/Phase-1-1-Core-Abstractions"
WHERE roadmap-level = "secondary" OR roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
