---
title: Phase 2.1 — Generation Pipeline Stages
roadmap-level: secondary
phase-number: 2
subphase-index: "2.1"
project-id: genesis-mythos-master
status: archived
priority: high
progress: 0
created: 2026-03-09
tags: [roadmap, genesis-mythos-master, phase, subphase]
para-type: Archive
links:
  - "[[Phase-2-Procedural-Generation-World-Building-Roadmap-2026-03-08-2358]]"
---

## Phase 2.1 — Generation Pipeline Stages

Turn the high-level Phase 2 goal into a concrete, swappable generation pipeline: seed parsing → terrain → biome → POI → entities → simulation bootstrap, wired for later simulation and rule engine integration but not implementing those concerns here.

- [ ] Define each generation stage’s responsibility and I/O (inputs, outputs, extension seams)
- [ ] Specify how DM/player seeds and overrides are threaded through the stages without hardcoding narrative
- [ ] Define handoff contract from simulation bootstrap into the Phase 3 living simulation layer

## Tertiary notes

```dataview
TABLE WITHOUT ID
  roadmap-level AS "Level",
  file.link AS "Note",
  subphase-index AS "Index",
  status,
  progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-World-Building/Phase-2-1-Generation-Pipeline-Stages"
WHERE roadmap-level = "secondary" OR roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```

