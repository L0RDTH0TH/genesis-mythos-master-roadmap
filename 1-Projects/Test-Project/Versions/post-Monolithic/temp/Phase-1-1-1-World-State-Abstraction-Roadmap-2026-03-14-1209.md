---
title: Phase 1.1.1 — World-State Abstraction
roadmap-level: tertiary
phase-number: 1
subphase-index: 1.1.1
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
  - "[[Phase-1-1-Key-Abstractions-Roadmap-2026-03-14-1201]]"
---

## Phase 1.1.1 — World-State Abstraction

Define the world-state abstraction: persistent game state, session state, and intent state so simulation, rendering, and input can read/write through a single coherent layer.

- [ ] Specify persistent game state schema (world seed, terrain, entities, faction state)
- [ ] Specify session state (active players, DM view, transient UI state)
- [ ] Specify intent state (pending lore injections, overrides, re-generation requests)
- [ ] Define read/write interfaces and invalidation boundaries
