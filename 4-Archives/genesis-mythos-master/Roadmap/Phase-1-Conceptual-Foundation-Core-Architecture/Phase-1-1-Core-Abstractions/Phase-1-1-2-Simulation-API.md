---
title: Phase 1.1.2 — Simulation API
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.1.2"
project-id: genesis-mythos-master
status: archived
priority: high
progress: 0
created: 2026-03-09
tags: [roadmap, genesis-mythos-master, phase, subphase]
para-type: Archive
links:
  - "[[Phase-1-1-Core-Abstractions-Roadmap-2026-03-09-0006]]"
---

## Phase 1.1.2 — Simulation API

Tick contract, inputs/outputs, and headless boundaries for the simulation layer. Mid-technical: interfaces and algorithm sketches so simulation runs decoupled from rendering.

### Tasks

- [ ] Define simulation tick contract (input: world state snapshot; output: state delta or next snapshot)
- [ ] Define headless boundaries (simulation runnable without 3D/UI for tests and lightweight previews)
- [ ] Document I/O interface for weather, NPCs, and persistent state updates
