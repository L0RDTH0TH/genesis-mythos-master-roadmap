---
title: Phase 1.3.4 — Input-Loop Seams
roadmap-level: tertiary
phase-number: 1
subphase-index: 1.3.4
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
  - "[[Phase-1-3-Modularity-Seams-Roadmap-2026-03-14-1205]]"
---

## Phase 1.3.4 — Input-Loop Seams

Document input-loop seams: intent parser + population resolver; extensible for new input types (voice, forms, chat) so the VTT can accept multiple input sources without hardcoding.

- [ ] Define intent-parser contract: raw input → structured intents; pluggable parsers per input type
- [ ] Define population-resolver contract: intents → systemic hooks (feeds into generation/simulation)
- [ ] Document extension point for new input types (register parser, map to existing intent schema)
- [ ] Example: add voice or form-based input without changing simulation or rendering
