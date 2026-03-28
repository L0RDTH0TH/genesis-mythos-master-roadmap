---
title: Phase 1.1.2 — Simulation-Logic Interface
roadmap-level: tertiary
phase-number: 1
subphase-index: 1.1.2
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

## Phase 1.1.2 — Simulation-Logic Interface

Define the simulation-logic interface (tick, events, hooks) so the tick-based layer can run independently of rendering and accept pluggable behaviors.

- [ ] Specify tick contract (input: world state delta; output: state updates, events emitted)
- [ ] Define event bus / event types (weather, NPC, faction, persistence)
- [ ] Define hooks for script components and replaceable behaviors
- [ ] Document decoupling from visuals (lightweight preview vs full session)
