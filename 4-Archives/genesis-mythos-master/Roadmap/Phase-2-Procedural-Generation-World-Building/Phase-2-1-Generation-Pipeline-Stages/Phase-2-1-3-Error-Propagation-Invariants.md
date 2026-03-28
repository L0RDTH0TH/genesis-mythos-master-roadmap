---
title: Phase 2.1.3 — Error Propagation and Invariants
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.1.3"
project-id: genesis-mythos-master
status: archived
priority: high
progress: 0
created: 2026-03-09
tags: [roadmap, genesis-mythos-master, phase, tertiary]
para-type: Archive
links:
  - "[[Phase-2-1-Generation-Pipeline-Stages-Roadmap-2026-03-09-1315]]"
---

## Phase 2.1.3 — Error Propagation and Invariants

Define how errors, warnings, and validation results move through the generation pipeline, and what invariants must always hold at each stage boundary.

### Checklist

- [ ] Enumerate error categories (validation failure, missing assets, rule conflict, performance guardrails) and how they are represented
- [ ] Describe how each stage reports errors/warnings upstream and downstream (e.g., accumulated context vs short-circuiting)
- [ ] Define invariants that must hold before and after each stage (e.g., no NaNs in heightfields, connected navmesh regions, valid IDs)
- [ ] Specify what gets logged for later replay/debug (including seed IDs, override sources, and stage traces)
- [ ] Clarify which failures should trigger regeneration vs soft degradation vs user-facing prompts

