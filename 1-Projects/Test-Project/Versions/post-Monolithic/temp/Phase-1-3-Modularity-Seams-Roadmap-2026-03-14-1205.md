---
title: Phase 1.3 — Modularity Seams
roadmap-level: secondary
phase-number: 1
subphase-index: "1.3"
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-14
tags:
  - roadmap
  - genesis-mythos-master
  - phase
para-type: Project
links:
  - "[[Phase-1-Conceptual-Foundation-Roadmap-2026-03-14-1200]]"
---

## Phase 1.3 — Modularity Seams

Identify modularity seams (generation stages, rule hooks, event bus) so each system is replaceable from the start and the VTT remains remixable.

- [ ] Document generation-stage seams (each stage swappable: noise, erosion, settlement, etc.)
- [ ] Document rule-engine seams (core primitives; rulesets as plugins with hooks and conflicts)
- [ ] Document simulation seams (event bus + state graph; script components for new behaviors)
- [ ] Document input-loop seams (intent parser + population resolver; extensible input types)

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation/Phase-1-3-Modularity-Seams"
WHERE roadmap-level = "secondary" OR roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
