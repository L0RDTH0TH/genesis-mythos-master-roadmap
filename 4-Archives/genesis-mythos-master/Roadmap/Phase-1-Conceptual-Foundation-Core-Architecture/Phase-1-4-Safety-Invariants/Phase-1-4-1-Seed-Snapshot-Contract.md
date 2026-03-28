---
title: Phase 1.4.1 — Seed Snapshot Contract
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.4.1"
project-id: genesis-mythos-master
status: archived
priority: high
progress: 0
created: 2026-03-09
tags: [roadmap, genesis-mythos-master, phase, subphase]
para-type: Archive
links:
  - "[[Phase-1-4-Safety-Invariants-Roadmap-2026-03-09-0110]]"
---

## Phase 1.4.1 — Seed Snapshot Contract

Define when to snapshot, what to capture, and where to store seed and override state so every generation run is traceable and recoverable (per master goal: "Every generation run snapshots seed + overrides + current intent state").

### Tasks

- [ ] Define **when to snapshot**: before first world write, after seed parsing, after intent resolution; document triggers (pre-commit, pre-region-write, on explicit user save).
- [ ] Define **what to capture**: seed payload hash, override diff, intent graph snapshot, pipeline stage checkpoint; minimal serializable state for replay or rollback.
- [ ] Define **where to store**: path convention (e.g. `Backups/Seeds/<run-id>/` or project-scoped); retention policy; exclusion from sync or publish if sensitive.
- [ ] Document interface for consumers: read-last-seed, list-runs-by-date, restore-from-seed (dry-run only in Phase 1).
