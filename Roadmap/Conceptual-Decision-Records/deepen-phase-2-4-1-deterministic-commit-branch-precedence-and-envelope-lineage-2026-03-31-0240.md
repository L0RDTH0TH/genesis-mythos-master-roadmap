---
title: Conceptual Decision Record - deepen phase 2.4.1 deterministic commit branch precedence and envelope lineage
created: 2026-03-31
tags:
  - roadmap
  - conceptual-decision-record
  - genesis-mythos-master
project-id: genesis-mythos-master
para-type: Project
roadmap_track: conceptual
decision_type: deepen
queue_entry_id: resume-deepen-gmm-241-20260330T122531Z-forward
parent_roadmap_note: 1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/Phase-2-4-Post-Validation-Commit-Orchestration/Phase-2-4-1-Deterministic-Commit-Deny-Defer-Precedence-and-Envelope-Lineage-Roadmap-2026-03-31-0240.md
validation_status: pattern_only
---

## Decision

Selected a dedicated tertiary slice that fixes deterministic precedence for `commit`, `deny_commit`, and `defer`, and requires a single envelope lineage contract that explicitly references 2.3 diagnostics authorities.

## PMG alignment

This decision supports deterministic, operator-traceable world-generation commits by preventing branch ambiguity and ensuring commit outcomes remain bound to gate-first payload evidence.

## Alternatives considered

- Keep branch precedence implicit in secondary 2.4 prose: rejected because tertiary-level deterministic branch order and field requirements were under-specified.
- Move precedence and lineage details fully to execution track: rejected because conceptual track must define branch authority and parity contracts before implementation decomposition.

## Why this was chosen

A dedicated 2.4.1 tertiary gives a stable handoff anchor where branch resolver precedence, envelope schema requirements, and 2.3 lineage constraints are unambiguous and replay-safe.

## Validation evidence

- Parent roadmap note: [[Phase-2-4-1-Deterministic-Commit-Deny-Defer-Precedence-and-Envelope-Lineage-Roadmap-2026-03-31-0240]]
- Upstream payload authority: [[Phase-2-3-2-Verification-Task-Decomposition-and-Failure-Payload-Contracts-Roadmap-2026-03-31-0215]]
- Upstream ordering/parity authority: [[Phase-2-3-5-Projection-Ordering-Rollup-Companion-and-Commit-Block-Parity-Roadmap-2026-03-31-0218]]
- Decision trace hub: [[decisions-log]]
