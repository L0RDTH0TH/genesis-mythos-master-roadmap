---
title: Phase 1.1.3 — Rendering Interface
roadmap-level: tertiary
phase-number: 1
subphase-index: 1.1.3
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

## Phase 1.1.3 — Rendering Interface

Define the rendering interface (scene graph, camera rigs, overlay layers) so the visual layer reads from world state and supports multiple view modes without coupling to simulation.

- [ ] Specify scene-graph contract (world state → drawables; no simulation write)
- [ ] Define camera rigs: player first-person, DM free-cam, orthographic tabletop
- [ ] Define overlay layers (grids, tokens, fog) as enable/disable modules
- [ ] Document semantic highlighting / post-process pass with lens switching
