---
title: Phase 2.2.1 — Intent Schema Structure & Validation
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.2.1"
project-id: genesis-mythos-master
status: archived
priority: high
progress: 0
created: 2026-03-09
tags: [roadmap, genesis-mythos-master, phase, subphase]
para-type: Archive
links:
  - "[[Phase-2-2-Intent-Schema-Hook-Graphs-Roadmap-2026-03-09-1335]]"
---

## Phase 2.2.1 — Intent Schema Structure & Validation

Define the concrete data shape for DM/player intents and how those records are validated and versioned before they ever touch the generation pipeline or simulation state.

Mid-technical: interfaces and algorithm sketches, not full pseudo-code — enough that an implementer can design types, validators, and migration paths without guessing.

### Tasks

- [ ] Enumerate intent record types and scopes (per-entity, per-faction, per-region, campaign-level) with required/optional fields
- [ ] Define schema representation and storage model (e.g. typed objects, JSON schema, or DSL) with clear versioning strategy
- [ ] Specify validation rules and failure handling (where validation runs, how errors surface to DM/players)
- [ ] Describe how validated intents are normalized into a canonical internal form ready for hook graphs and generation stages

