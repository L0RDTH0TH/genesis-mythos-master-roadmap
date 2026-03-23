---
title: genesis-mythos-master Roadmap MOC
created: 2026-03-19
tags: [roadmap, moc, genesis-mythos-master]
para-type: Project
status: active
project-id: genesis-mythos-master
links: ["[[genesis-mythos-master-roadmap-2026-03-19-1101]]"]
---

# genesis-mythos-master — Roadmap MOC

## Master roadmap

- [[genesis-mythos-master-roadmap-2026-03-19-1101]]

## All phase roadmaps

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Roadmap", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap"
WHERE roadmap-level = "master" OR roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary" OR roadmap-level = "task"
SORT phase-number ASC, subphase-index ASC, file.name ASC
```
