---
title: Conceptual Decision Record - deepen phase 2.4.2 scenario lineage parity
created: 2026-03-31
tags:
  - roadmap
  - conceptual-decision-record
  - genesis-mythos-master
project-id: genesis-mythos-master
para-type: Project
roadmap_track: conceptual
decision_type: deepen
queue_entry_id: resume-deepen-gmm-2422-20260330T124000Z-forward
parent_roadmap_note: 1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/Phase-2-4-Post-Validation-Commit-Orchestration/Phase-2-4-2-Scenario-Id-to-Decision-Reason-Code-Lineage-Parity-Roadmap-2026-03-31-0315.md
validation_status: pattern_only
---

## Decision

Selected a dedicated tertiary slice that binds canonical `S-2.4.1-*` scenario IDs to deterministic `decision_reason_code` outputs with explicit lineage parity requirements.

## PMG alignment

This keeps post-validation commit orchestration deterministic and operator-traceable, preventing branch drift between replay paths and preserving gate-first authority.

## Alternatives considered

- Keep scenario mapping implicit inside `2.4.1`: rejected because validator-facing closure mapping and parity checks stayed under-specified.
- Delay scenario mapping to execution track only: rejected because conceptual authority must define deterministic outcome mapping before implementation details.

## Why this was chosen

The 2.4.2 slice creates a stable, auditable contract where each canonical scenario has one branch/reason outcome and mandatory lineage refs to `2.3.2` and `2.3.5`.

## Validation evidence

- Parent roadmap note: [[Phase-2-4-2-Scenario-Id-to-Decision-Reason-Code-Lineage-Parity-Roadmap-2026-03-31-0315]]
- Prior tertiary authority: [[Phase-2-4-1-Deterministic-Commit-Deny-Defer-Precedence-and-Envelope-Lineage-Roadmap-2026-03-31-0240]]
- Upstream payload authority: [[Phase-2-3-2-Verification-Task-Decomposition-and-Failure-Payload-Contracts-Roadmap-2026-03-31-0215]]
- Upstream ordering/parity authority: [[Phase-2-3-5-Projection-Ordering-Rollup-Companion-and-Commit-Block-Parity-Roadmap-2026-03-31-0218]]
- Decision trace hub: [[decisions-log]]
