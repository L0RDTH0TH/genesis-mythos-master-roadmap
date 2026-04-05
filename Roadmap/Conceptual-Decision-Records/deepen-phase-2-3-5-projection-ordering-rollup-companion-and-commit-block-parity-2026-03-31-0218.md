---
title: Conceptual Decision Record - deepen phase 2.3.5 projection ordering rollup companion and commit-block parity
created: 2026-03-31
tags:
  - roadmap
  - conceptual-decision-record
  - godot-genesis-mythos-master
project-id: godot-genesis-mythos-master
para-type: Project
roadmap_track: conceptual
decision_type: deepen
queue_entry_id: resume-deepen-gmm-235-20260331T021800Z-forward
parent_roadmap_note: 1-Projects/godot-genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/Phase-2-3-Pipeline-Validation-and-Pre-Commit-Verification/Phase-2-3-5-Projection-Ordering-Rollup-Companion-and-Commit-Block-Parity-Roadmap-2026-03-31-0218.md
validation_status: pattern_only
---

## Decision

Selected a gate-first projection ordering contract for `2.3.5` where authoritative failure payloads are sorted deterministically before generating a readable rollup companion.

## PMG alignment

This keeps Phase 2 conceptual authority deterministic and traceable while preserving pre-commit safety boundaries required by the master goal's world-state integrity direction.

## Alternatives considered

- Rollup-first rendering with payload backfill: rejected because it can hide ordering authority and blur commit-block causality.
- Per-gate local ordering only: rejected because cross-gate replay and operator trace comparison would drift between frames.

## Why this was chosen

The selected approach carries the existing branch decisions from `2.3.3` and `2.3.4` into a closure slice that maintains warm-cache non-bypass parity and explicit operator-pick evidence links, while still deferring execution-level implementation choices.

## Validation evidence

- Parent roadmap note: [[Phase-2-3-5-Projection-Ordering-Rollup-Companion-and-Commit-Block-Parity-Roadmap-2026-03-31-0218]]
- Prior branch context: [[Phase-2-3-4-Bound-Projection-Contract-Continuation-with-Warm-Cache-Non-Bypass-and-Operator-Pick-Validation-Trace-Roadmap-2026-03-31-0217]]
- Decision trace hub: [[decisions-log]]
