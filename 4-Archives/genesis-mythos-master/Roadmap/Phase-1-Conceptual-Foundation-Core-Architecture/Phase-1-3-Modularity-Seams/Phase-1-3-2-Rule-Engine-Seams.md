---
title: Phase 1.3.2 — Rule Engine Seams
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.3.2"
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

## Phase 1.3.2 — Rule Engine Seams

Core rule primitives only; rulesets as plugins declaring hooks and resolving conflicts. Ensures multiple RPG systems can plug in without hardcoding one ruleset.

### Tasks

- [ ] Define core rule engine primitives (dice, checks, modifiers, outcomes)
- [ ] Define plugin contract: rulesets declare hooks (e.g. initiative, damage, skill checks) and conflict resolution
- [ ] Document how to add or swap a ruleset (e.g. D&D-style vs PbtA-style) without breaking simulation
