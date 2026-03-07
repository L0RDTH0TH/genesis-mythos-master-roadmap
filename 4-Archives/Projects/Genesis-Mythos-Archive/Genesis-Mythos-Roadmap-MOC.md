---
title: Genesis Mythos Roadmap MOC
created: 2026-03-02
tags: [genesis-mythos, roadmap, moc]
para-type: Project
status: active
links: ["[[Genesis-Mythos-Roadmap-2026-03-02-1200]]"]
---

# Genesis Mythos Roadmap MOC

Aggregates all phase and sub-phase roadmaps for the Genesis Mythos project. Master roadmap (no tasks): [[Genesis-Mythos-Roadmap-2026-03-02-1200]].

## All phase and sub-phase roadmaps

```dataview
TABLE WITHOUT ID
    file.link AS "Roadmap",
    roadmap-level,
    phase-number,
    status,
    priority,
    progress AS "%"
FROM "1-Projects/Genesis-Mythos/Roadmap"
WHERE roadmap-level = "master" OR roadmap-level = "phase" OR roadmap-level = "subphase"
SORT phase-number ASC, file.name ASC
```
