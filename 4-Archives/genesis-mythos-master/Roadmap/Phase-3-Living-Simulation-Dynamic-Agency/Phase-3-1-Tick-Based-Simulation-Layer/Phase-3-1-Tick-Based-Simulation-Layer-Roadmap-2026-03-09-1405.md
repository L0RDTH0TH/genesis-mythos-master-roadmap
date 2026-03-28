---
title: Phase 3.1 — Tick-Based Simulation Layer
roadmap-level: secondary
phase-number: 3
subphase-index: "3.1"
project-id: genesis-mythos-master
status: archived
priority: high
progress: 0
created: 2026-03-09
tags: [roadmap, genesis-mythos-master, phase, subphase]
para-type: Archive
links:
  - "[[Phase-3-Living-Simulation-Dynamic-Agency-Roadmap-2026-03-08-2358]]"
---

## Phase 3.1 — Tick-Based Simulation Layer

Define the tick-based simulation layer that runs independently of rendering: weather cycles, NPC agendas, faction interactions, and persistent state changes. Interfaces and contracts for consumption by Phase 2 bootstrap and by DM overwrites (Phase 3.2).

- [ ] Define tick model and global sim clock (fixed vs variable step; pause/resume; sync with session time)
- [ ] Specify weather and environmental state (cycles, region-scoped variables, effect on paths and mood)
- [ ] Specify NPC agendas and schedules (availability, goals, interaction windows; link to intent hooks where relevant)
- [ ] Specify faction and relationship state (reputation graphs, tension, events triggered by thresholds)
- [ ] Define persistent state storage and replay boundaries (what is committed each tick; rollback scope)

## Tertiary notes

```dataview
TABLE WITHOUT ID
  roadmap-level AS "Level",
  file.link AS "Note",
  subphase-index AS "Index",
  status,
  progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-Dynamic-Agency/Phase-3-1-Tick-Based-Simulation-Layer"
WHERE roadmap-level = "secondary" OR roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
