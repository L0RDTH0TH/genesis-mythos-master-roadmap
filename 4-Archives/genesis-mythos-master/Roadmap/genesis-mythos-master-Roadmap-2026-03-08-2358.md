---
title: Genesis Mythos Master Roadmap
roadmap-level: master
phase-number: 0
project-id: genesis-mythos-master
status: archived
priority: high
progress: 0
created: 2026-03-08
tags:
  - roadmap
  - project
  - genesis-mythos-master
para-type: Archive
links:
  - "[[1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation/genesis-mythos-master-Roadmap-MOC]]"
roadmap_generation_status: complete
---

# Genesis Mythos Master Roadmap

> [!info] Generation provenance
> Generated from `[[Source-genesis-mythos-master-goal-unaltered-capture-2026-03-07-0033-2026-03-08-0900]]` on 2026-03-08T23:58:00Z
> ROADMAP MODE – multi-run setup (Phase 0 + workflow_state + master + phases).
> Guidance: No additional guidance provided.
> Intent confidence: high

Source: [[Source-genesis-mythos-master-goal-unaltered-capture-2026-03-07-0033-2026-03-08-0900]]

## Phase 1 — Conceptual Foundation and Core Architecture

Establish the high-level blueprint and modular skeleton for immersion, collaboration, and extensibility. Key abstractions: world state, simulation, rendering, input; procedural generation graph and intent population pipeline; modularity seams and safety invariants.

```dataview
TABLE WITHOUT ID
  roadmap-level AS "Level",
  file.link AS "Note",
  subphase-index AS "Index",
  status,
  progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-Core-Architecture"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```

## Phase 2 — Procedural Generation and World Building

Develop the collaborative forge for emergent worlds: generation pipeline (seed → terrain → biomes → POIs → entities → bootstrap), player/DM intent loops, and initial world emergence.

```dataview
TABLE WITHOUT ID
  roadmap-level AS "Level",
  file.link AS "Note",
  subphase-index AS "Index",
  status,
  progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-World-Building"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```

## Phase 3 — Living Simulation and Dynamic Agency

Tick-based simulation (weather, NPCs, factions, persistent state), DM overwrites vs re-generation, vitality features and decoupled simulation from visuals.

```dataview
TABLE WITHOUT ID
  roadmap-level AS "Level",
  file.link AS "Note",
  subphase-index AS "Index",
  status,
  progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-Dynamic-Agency"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```

## Phase 4 — Perspective Split and Control Systems

Player first-person immersion; DM free-cam god-view and orthographic tabletop toggle; camera abstraction and interpolator; role-based agency.

```dataview
TABLE WITHOUT ID
  roadmap-level AS "Level",
  file.link AS "Note",
  subphase-index AS "Index",
  status,
  progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-Control-Systems"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```

## Phase 5 — Rule System Integration and Extensibility

Core rule engine + one ruleset plugin; modularity demo (swap biome/event types); customization and ecosystem seams.

```dataview
TABLE WITHOUT ID
  roadmap-level AS "Level",
  file.link AS "Note",
  subphase-index AS "Index",
  status,
  progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-Extensibility"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```

## Phase 6 — Prototype Assembly, Testing, and Iteration

Single-player world: one ruleset, perspective split, basic simulation, one intent loop, DM overwrites; testing and provenance.

```dataview
TABLE WITHOUT ID
  roadmap-level AS "Level",
  file.link AS "Note",
  subphase-index AS "Index",
  status,
  progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-Iteration"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```

## Related

- [[1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation/genesis-mythos-master-Roadmap-MOC]]
- [[Source-genesis-mythos-master-goal-unaltered-capture-2026-03-07-0033-2026-03-08-0900]]
- [[4-Archives/genesis-mythos-master/Roadmap/roadmap-state]]
- [[4-Archives/genesis-mythos-master/Roadmap/workflow_state]]
