---
title: Phase 4 — Modularity
roadmap-level: phase
phase-number: 4
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-07
tags: [roadmap, genesis-mythos, phase]
para-type: Project
links: ["[[genesis-mythos-master-Roadmap-2026-03-07-1200]]"]
---

# Phase 4 — Modularity

Built from the ground up for remixing: every system (generation stages, simulation ticks, camera controllers, input loops) is replaceable via clear interfaces. Key seams: world gen pipeline (stage-by-stage replaceable), rule engine (core primitives only; rulesets as plugins), simulation (event bus + state graph; script components), input loop (intent parser + population resolver; extensible for voice, forms, chat), visuals & UI (overlay layers as enable/disable modules). Intent: tool as living ecosystem for communal growth.

- [ ] World gen pipeline: stage-by-stage, each stage replaceable
- [ ] Rule engine: core primitives only; rulesets as plugins (hooks & conflicts)
- [ ] Simulation: event bus + state graph; new behaviors via script components
- [ ] Input loop: intent parser + population resolver; extensible for new input types
- [ ] Visuals & UI: overlay layers (grids, tokens, fog) as enable/disable modules
