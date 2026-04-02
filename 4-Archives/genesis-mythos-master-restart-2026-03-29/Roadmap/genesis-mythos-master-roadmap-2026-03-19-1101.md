---
title: genesis-mythos-master Roadmap
roadmap-level: master
phase-number: 0
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-19
tags: [roadmap, project, genesis-mythos-master]
para-type: Project
links:
  - "[[genesis-mythos-master-roadmap-moc]]"
roadmap_generation_status: complete
---

# genesis-mythos-master Roadmap

> [!info] Generation provenance
> Generated from [[Genesis-mythos-master-goal]] on 2026-03-19T11:01:51Z.
> Guidance: No additional guidance provided.
> Intent confidence: medium.

Source: [[Genesis-mythos-master-goal]]

## Phase 1 — Conceptual Foundation and Core Architecture
Define the architecture seams for generation, simulation, rendering, and control so later implementation stays modular and replaceable. This phase prioritizes interface contracts and safety invariants over feature breadth.

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```

## Phase 2 — Procedural Generation and World Building
Implement the world generation pipeline and intent injection flow so DM and player inputs become systemic world state rather than static narrative. The outcome is a reproducible world scaffold with collaborative hooks.

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```

## Phase 3 — Living Simulation and Dynamic Agency
Build a simulation layer that keeps weather, NPC routines, and faction consequences evolving between sessions. This phase establishes the balance between DM live edits and deliberate regeneration boundaries.

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```

## Phase 4 — Perspective Split and Control Systems
Deliver the dual-view experience: immersive first-person for players and fluid DM command controls with seamless transitions. This phase secures interaction quality and role-specific usability.

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```

## Phase 5 — Rule System Integration and Extensibility
Integrate one baseline RPG ruleset while proving plugin seams for future rules, visuals, and behavior modules. The core goal is extensibility without architectural breakage.

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-and-Extensibility"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```

## Phase 6 — Prototype Assembly, Testing, and Iteration
Assemble a playable vertical slice and validate immersion, systemic responsiveness, and modular maintainability under realistic usage. This closes the setup roadmap with a testable baseline and iteration loop.

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```

## Related

- [[genesis-mythos-master-roadmap-moc]]
- [[Genesis-mythos-master-goal]]
