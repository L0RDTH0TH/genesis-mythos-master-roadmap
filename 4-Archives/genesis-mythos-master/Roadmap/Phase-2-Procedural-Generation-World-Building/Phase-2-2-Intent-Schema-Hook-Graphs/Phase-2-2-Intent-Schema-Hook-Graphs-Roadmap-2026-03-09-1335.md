---
title: Phase 2.2 — Intent Schema and Hook Graphs
roadmap-level: secondary
phase-number: 2
subphase-index: "2.2"
project-id: genesis-mythos-master
status: archived
priority: high
progress: 0
created: 2026-03-09
tags: [roadmap, genesis-mythos-master, phase, subphase]
para-type: Archive
links:
  - "[[Phase-2-Procedural-Generation-World-Building-Roadmap-2026-03-08-2358]]"
---

## Phase 2.2 — Intent Schema and Hook Graphs

Specify how DM/player intents (backstories, quests, factions, artifacts, themes) are represented as data and wired into systemic hooks such as reputation graphs, event triggers, and environmental modifiers.

- [ ] Define canonical intent types and fields (per-entity, per-faction, per-region, campaign-level)
- [ ] Map intents into hook structures (reputation nodes, relationship edges, event conditions, environment weights)
- [ ] Define lifecycle of intents (creation, update, deprecation) and how they stay in sync with generated content

## Tertiary notes

```dataview
TABLE WITHOUT ID
  roadmap-level AS "Level",
  file.link AS "Note",
  subphase-index AS "Index",
  status,
  progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-World-Building/Phase-2-2-Intent-Schema-Hook-Graphs"
WHERE roadmap-level = "secondary" OR roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```

