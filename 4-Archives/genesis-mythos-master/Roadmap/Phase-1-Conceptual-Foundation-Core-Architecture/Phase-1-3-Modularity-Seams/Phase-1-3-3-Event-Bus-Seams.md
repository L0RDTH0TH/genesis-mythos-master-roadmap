---
title: Phase 1.3.3 — Event Bus and Simulation Seams
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.3.3"
project-id: genesis-mythos-master
status: archived
priority: high
progress: 0
created: 2026-03-09
tags: [roadmap, genesis-mythos-master, phase, subphase]
para-type: Archive
links:
  - "[[Phase-1-3-Modularity-Seams-Roadmap-2026-03-09-0045]]"
---

## Phase 1.3.3 — Event Bus and Simulation Seams

Event bus + state graph; new behaviors plug in via script components. Ensures simulation (weather, NPCs, factions, events) is extensible without forking core.

### Tasks

- [ ] Define event bus contract (publish/subscribe; event types and payload schema)
- [ ] Define state graph integration (how events read/write simulation state; ordering guarantees)
- [ ] Document script-component plug-in: new behaviors (e.g. new event type, new NPC behavior) without core change
