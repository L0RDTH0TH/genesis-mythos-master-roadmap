---
title: genesis-mythos-master Roadmap
roadmap-level: master
phase-number: 0
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-07
tags: [roadmap, project, genesis-mythos]
para-type: Project
links: ["[[genesis-mythos-master-Roadmap-MOC]]"]
roadmap_generation_status: complete
---

# genesis-mythos-master Roadmap

> [!info] Generation provenance
> Generated from `[[Source-genesis-mythos-master-goal-2026-03-07-0033-2026-03-07-1200]]` on 2026-03-07T12:00:00Z
> Trigger: ROADMAP MODE – generate from outline (no wrapper).
> Guidance: No additional guidance provided.
> Intent confidence: high (Master Goal v2.0 with clear thematic phases).

- Source: [[Source-genesis-mythos-master-goal-2026-03-07-0033-2026-03-07-1200]]

## Phase 1 — Perspective split

Player-first immersion and DM control: players stay in first-person; DMs get Sparky-style free-cam plus orthographic tabletop view with smooth mode transitions. Goal: no escape to top-down for players; effortless dominion and surgical tactical tools for DMs.

```dataview
TABLE WITHOUT ID file.link AS "Sub-Phase", status, priority, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-1-Perspective-Split"
WHERE roadmap-level = "phase" OR roadmap-level = "subphase"
SORT file.name ASC
```

## Phase 2 — Shared creation

Worlds emerge from shared creation: player lore intents feed systemic hooks (reputation, events, environment). Systems enable emergence without hardcoding narrative. Result: co-authored world with player intent woven into procedural depth.

```dataview
TABLE WITHOUT ID file.link AS "Sub-Phase", status, priority, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-2-Shared-Creation"
WHERE roadmap-level = "phase" OR roadmap-level = "subphase"
SORT file.name ASC
```

## Phase 3 — Living world

The world pulses with life: layered simulation (weather, NPCs, persistent scars), DM overwrites that respect cost and intent, and extensibility for remixing simulation flavors and rule behaviors. Rewards long campaigns with meaningful evolution.

```dataview
TABLE WITHOUT ID file.link AS "Sub-Phase", status, priority, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-World"
WHERE roadmap-level = "phase" OR roadmap-level = "subphase"
SORT file.name ASC
```

## Phase 4 — Modularity

Open source and aggressive modularity: every system (generation stages, simulation ticks, camera controllers, input loops) replaceable via clear interfaces. Built for remixing and communal growth; tool as living ecosystem.

```dataview
TABLE WITHOUT ID file.link AS "Sub-Phase", status, priority, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-4-Modularity"
WHERE roadmap-level = "phase" OR roadmap-level = "subphase"
SORT file.name ASC
```

## Phase 5 — Technical integration

Concrete architecture: procedural core + intent population pipeline, living simulation decoupled from rendering, perspective & control abstraction (unified scene graph, camera rigs), modularity boundaries (world gen, rule engine, simulation, input, visuals), and safety & iteration invariants (snapshots, dry-run, provenance).

```dataview
TABLE WITHOUT ID file.link AS "Sub-Phase", status, priority, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-5-Technical-Integration"
WHERE roadmap-level = "phase" OR roadmap-level = "subphase"
SORT file.name ASC
```

## Phase 6 — Prototype scope (Q3 2026)

Target deliverable: single-player playable world with one ruleset, full perspective split, live DM overwrites, one round-trip player intent loop, basic living simulation (weather + simple NPC schedules), and demonstrated modding seams (e.g. swap biome generator or add event type).

```dataview
TABLE WITHOUT ID file.link AS "Sub-Phase", status, priority, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Scope"
WHERE roadmap-level = "phase" OR roadmap-level = "subphase"
SORT file.name ASC
```

## Related

- [[genesis-mythos-master-Roadmap-MOC]]
- [[Source-genesis-mythos-master-goal-2026-03-07-0033-2026-03-07-1200]]
