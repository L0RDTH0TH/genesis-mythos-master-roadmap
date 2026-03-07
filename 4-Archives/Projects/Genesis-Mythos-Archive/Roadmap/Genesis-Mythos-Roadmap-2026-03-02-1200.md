---
title: Genesis Mythos Roadmap
created: 2026-03-02
tags: [genesis-mythos, roadmap]
para-type: Project
status: active
roadmap-level: master
phase-number: 1
priority: high
dependencies: []
progress: 0
highlight_perspective: geosynchronous-view
project-id: genesis-mythos
links: ["[[Genesis-Mythos-Roadmap-MOC]]", "[[Genesis-Docs-Timeline]]", "[[Genesis-Mythos-README]]", "[[Terrain3D-Integration-Guide-2026-03-02-1059]]", "[[World-Building]]", "[[Mythos Tabletop]]"]
---

# Genesis Mythos — Master Roadmap

Geosynchronous flow: **Maps → Terrain3D → Lore → Combat & Equipment → Politics → Wizard & Rendering**. MVP: Phases 1–2 (maps + terrain) with DM editor and first-playable 3D slice. Source: [[3-Resources/Genesis-Mythos/Genesis-Living-Roadmap-2026-03-02-1100]].

## Phase 1 — Maps

```dataview
TABLE WITHOUT ID
    file.link AS "Sub-Phase",
    status,
    priority,
    progress AS "%",
    deadline
FROM "1-Projects/Genesis-Mythos/Roadmap/Phase-1-Maps"
WHERE roadmap-level = "phase" OR roadmap-level = "subphase"
SORT priority DESC, file.name ASC
```

## Phase 2 — Terrain3D

```dataview
TABLE WITHOUT ID
    file.link AS "Sub-Phase",
    status,
    priority,
    progress AS "%",
    deadline
FROM "1-Projects/Genesis-Mythos/Roadmap/Phase-2-Terrain3D"
WHERE roadmap-level = "phase" OR roadmap-level = "subphase"
SORT priority DESC, file.name ASC
```

## Phase 3 — Lore

```dataview
TABLE WITHOUT ID
    file.link AS "Sub-Phase",
    status,
    priority,
    progress AS "%",
    deadline
FROM "1-Projects/Genesis-Mythos/Roadmap/Phase-3-Lore"
WHERE roadmap-level = "phase" OR roadmap-level = "subphase"
SORT priority DESC, file.name ASC
```

## Phase 4 — Combat & equipment

```dataview
TABLE WITHOUT ID
    file.link AS "Sub-Phase",
    status,
    priority,
    progress AS "%",
    deadline
FROM "1-Projects/Genesis-Mythos/Roadmap/Phase-4-Combat"
WHERE roadmap-level = "phase" OR roadmap-level = "subphase"
SORT priority DESC, file.name ASC
```

## Phase 5 — Politics & factions

```dataview
TABLE WITHOUT ID
    file.link AS "Sub-Phase",
    status,
    priority,
    progress AS "%",
    deadline
FROM "1-Projects/Genesis-Mythos/Roadmap/Phase-5-Politics"
WHERE roadmap-level = "phase" OR roadmap-level = "subphase"
SORT priority DESC, file.name ASC
```

## Phase 6 — World-builder wizard & rendering

```dataview
TABLE WITHOUT ID
    file.link AS "Sub-Phase",
    status,
    priority,
    progress AS "%",
    deadline
FROM "1-Projects/Genesis-Mythos/Roadmap/Phase-6-Wizard"
WHERE roadmap-level = "phase" OR roadmap-level = "subphase"
SORT priority DESC, file.name ASC
```

## Related

- [[Genesis-Mythos-Roadmap-MOC]] — Aggregates all phase and sub-phase roadmaps
- [[Genesis-Docs-Timeline]] — Chronological backbone
- [[Genesis-Mythos-README]] — Project rules, singletons
- [[Terrain3D-Integration-Guide-2026-03-02-1059]] — Terrain3D setup
- [[World-Building]] — Tile-based editor, biomes, city generator, 37 km²
- [[Mythos Tabletop]] — PRD: first-person, DM cam, combat, NPCs, modding
