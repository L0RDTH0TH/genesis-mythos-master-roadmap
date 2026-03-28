---
title: Phase 1.1.4 — Input-Handling Abstraction
roadmap-level: tertiary
phase-number: 1
subphase-index: 1.1.4
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

## Phase 1.1.4 — Input-Handling Abstraction

Define the input-handling abstraction (player vs DM, intent parser) so role-based input flows into world state and intent resolution without coupling to rendering or simulation.

- [ ] Specify player input path (WASD, look, interaction raycasts → intent/state updates)
- [ ] Specify DM input path (free-cam, orthographic toggle, token/lore commands)
- [ ] Define intent parser: raw input → structured intents (move, interact, overwrite, re-gen request)
- [ ] Document extensibility for new input types (voice, forms, chat)
