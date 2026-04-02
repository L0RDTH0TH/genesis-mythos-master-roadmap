---
title: "CDR — Phase 5.1.3 precedence conflict matrix and deterministic winner resolution"
created: 2026-04-03
tags:
  - conceptual-decision-record
  - genesis-mythos-master
  - phase-5
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-5-1-3-Precedence-Conflict-Matrix-and-Deterministic-Winner-Resolution-Roadmap-2026-03-31-2345]]"
decision_kind: deepen
queue_entry_id: followup-deepen-phase4-41-rollup-gmm-20260403T211500Z
master_goal: "[[Source-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# CDR — Phase 5.1.3 precedence conflict matrix and deterministic winner resolution

## Summary

Minted tertiary **5.1.3** as **precedence conflict matrix** + **deterministic winner resolution** after **5.1.2** scheduling, closing the **5.1.1–5.1.3** chain with replay-stable **suppressed_by** semantics and fail-closed **unknown tuple** behavior. **Secondary 5.1 rollup** is the next structural node.

## PMG alignment

Preserves **deterministic / auditable** rule integration: conflicts are **explicit**, **matrix-governed**, and **ledger-traceable**—consistent with orchestration + consumer contracts from prior phases.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| --- | --- | --- | --- |
| First-match-wins after schedule | Simple | Hides conflicts | Fails **replay audit** goals |
| Runtime negotiation between rules | Flexible | Non-deterministic | Rejected for core path |

## Validation evidence

- Pattern-only: parent [[Phase-5-1-Rule-Primitives-Plugin-Host-and-Conflict-Precedence-Roadmap-2026-04-03-2310]], [[Phase-5-1-2-Kernel-Evaluation-Schedule-and-Rule-Ordering-Roadmap-2026-04-03-2320]], ledger overlap vocabulary [[Phase-4-2-2-Transition-Outcome-Ledger-and-Lane-Projection-Parity-Roadmap-2026-03-31-1200]].

## Links

- **Workflow anchor:** `2026-03-31 23:45` — `Phase-5-1-3-Precedence-Conflict-Matrix-and-Deterministic-Winner-Resolution` — `queue_entry_id: followup-deepen-phase4-41-rollup-gmm-20260403T211500Z`
- **Resolver:** `gate_signature: stale-queue-4-1-vs-vault-5-1-3-reconcile`, `effective_track: conceptual`, `gate_catalog_id: conceptual_v1`
