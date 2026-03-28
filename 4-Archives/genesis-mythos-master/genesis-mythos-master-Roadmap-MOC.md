---
title: Genesis Mythos Master Roadmap MOC
created: 2026-03-08
tags:
  - roadmap
  - moc
  - genesis-mythos-master
para-type: Archive
status: archived
project-id: genesis-mythos-master
links:
  - "[[Roadmap/genesis-mythos-master-Roadmap-2026-03-08-2358]]"
  - "[[4-Archives/genesis-mythos-master/Roadmap/roadmap-state]]"
  - "[[4-Archives/genesis-mythos-master/Roadmap/decisions-log]]"
  - "[[4-Archives/genesis-mythos-master/Roadmap/distilled-core]]"
  - "[[Source-genesis-mythos-master-goal-unaltered-capture-2026-03-07-0033-2026-03-08-0900]]"
---

# Genesis Mythos Master — Roadmap MOC

## Master roadmap

- [[Roadmap/genesis-mythos-master-Roadmap-2026-03-08-2358]]

## State & resumption

- [[4-Archives/genesis-mythos-master/Roadmap/roadmap-state]]
- [[4-Archives/genesis-mythos-master/Roadmap/workflow_state]]
- [[4-Archives/genesis-mythos-master/Roadmap/decisions-log]]
- [[4-Archives/genesis-mythos-master/Roadmap/distilled-core]]
- [[Source-genesis-mythos-master-goal-unaltered-capture-2026-03-07-0033-2026-03-08-0900]]

## All phase roadmaps

```dataview
TABLE WITHOUT ID
  roadmap-level AS "Level",
  file.link AS "Roadmap",
  subphase-index AS "Index",
  status,
  progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap"
WHERE roadmap-level = "master" OR roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary" OR roadmap-level = "task"
SORT phase-number ASC, subphase-index ASC, file.name ASC
```
