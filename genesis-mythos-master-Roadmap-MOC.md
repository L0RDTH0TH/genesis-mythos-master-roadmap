---
title: genesis-mythos-master Roadmap MOC
created: 2026-03-29
tags: [roadmap, moc, genesis-mythos-master]
para-type: Project
status: active
project-id: genesis-mythos-master
links:
  - "[[genesis-mythos-master-Roadmap-2026-03-29-1730]]"
---

# genesis-mythos-master — Roadmap MOC

## Master roadmap

- [[genesis-mythos-master-Roadmap-2026-03-29-1730]]

## All phase roadmaps

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Roadmap", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap"
WHERE roadmap-level = "master" OR roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary" OR roadmap-level = "task"
SORT phase-number ASC, subphase-index ASC, file.name ASC
```

## State & logs

- [[Roadmap/roadmap-state]]
- [[Roadmap/workflow_state]]
- [[Roadmap/decisions-log]]
- [[Roadmap/distilled-core]]
