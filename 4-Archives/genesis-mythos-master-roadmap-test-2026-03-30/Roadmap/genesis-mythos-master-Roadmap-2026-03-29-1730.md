---
title: genesis-mythos-master Roadmap
roadmap-level: master
phase-number: 0
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-29
tags: [roadmap, project, genesis-mythos-master]
para-type: Project
links:
  - "[[4-Archives/genesis-mythos-master-roadmap-test-2026-03-30/genesis-mythos-master-Roadmap-MOC|genesis-mythos-master-Roadmap-MOC (archived)]]"
roadmap_generation_status: complete
---

# genesis-mythos-master Roadmap

> [!info] Generation provenance
> Generated from `[[Genesis-mythos-master-goal]]` on 2026-03-29T17:30:00Z (queue `roadmap-setup-gmm-restart-20260329T160000Z`).
> **Operator constraint:** PMG remains at project root as read-only seed; not moved into `Roadmap/`.
> Prior roadmap tree lives under `4-Archives/genesis-mythos-master-restart-2026-03-29/Roadmap/` for reference only — not auto-merged.
> **Guidance:** Restart after full Roadmap archive — Phase 0 + fresh tree from PMG only.
> Intent confidence: high

Source: [[Genesis-mythos-master-goal]]

## Phase 1 — Conceptual Foundation and Core Architecture

Establish the high-level blueprint and modular skeleton: decoupled layers, procedural generation graph and intent pipeline interfaces, modularity seams, and early safety invariants (snapshots, dry-run).

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```

## Phase 2 — Procedural Generation and World Building

Implement the collaborative forge: seed through simulation bootstrap, intent loops into systemic hooks, scaffold dialogue, and validate emergent world behavior over simulated sessions.

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```

## Phase 3 — Living Simulation and Dynamic Agency

Tick-based simulation (weather, NPCs, factions, persistence), DM overwrite vs re-generation policy, vitality and consequence, simulation decoupled from rendering for lightweight previews.

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```

## Phase 4 — Perspective Split and Control Systems

Player first-person lock; DM free-cam plus orthographic tabletop; unified scene graph and camera interpolator; role-appropriate agency.

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```

## Phase 5 — Rule System Integration and Extensibility

Rule engine primitives, first ruleset as plugin, modularity demos (swap generators, event types), ecosystem documentation for community seams.

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-and-Extensibility"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```

## Phase 6 — Prototype Assembly, Testing, and Iteration

MVP assembly (Q3 2026 horizon per PMG): single-player world, one ruleset, perspective split, simulation basics, one intent loop, DM overwrites; testing, provenance, feedback loop.

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```

## Related

- [[4-Archives/genesis-mythos-master-roadmap-test-2026-03-30/genesis-mythos-master-Roadmap-MOC|genesis-mythos-master-Roadmap-MOC (archived)]]
- [[Genesis-mythos-master-goal]]
- [[roadmap-state]]
- [[workflow_state]]
