---
title: CDR — Phase 2.1.1 tertiary (stage family bodies and boundary hooks)
created: 2026-03-30
tags:
  - roadmap
  - conceptual-decision-record
  - genesis-mythos-master
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-2-1-1-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-03-30-0923]]"
decision_kind: deepen
queue_entry_id: pb-craft-20260330T050422Z-8f7e7e5c-7a9c-4c55-9e2e-5c2e3b7f1c0a
master_goal: "[[Source-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# Decision record — tertiary 2.1.1 (stage family bodies and boundary hooks)

## Summary

Minted tertiary **2.1.1** under secondary **2.1** as the **stage-family body contracts** plus **boundary hooks** that define typed staged outputs and the commit-boundary token required for Phase 2's conceptual safety posture. The slice keeps stage bodies pre-commit and treats dry-run validation as the explicit precondition for authoritative mutation.

## PMG alignment

Supports the master goal's emphasis on deterministic, inspectable generation by making stage outputs and validation artifacts explicit at the contract level, so later work can refine concrete engine behavior without weakening the dry-run -> commit separation.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|-------------|--------|-----------|----------------|
| Bind stage behavior directly to execution APIs here | Earlier implementability | Locks conceptual naming too early and collapses dry-run vs commit boundaries | Execution details belong in execution track / later technical depth |
| Merge stage-body contracts with validation logic | Fewer surfaces | Increases coupling; makes replay and boundary reasoning harder | Keeps validation artifacts as explicit pre-commit outputs |
| Omit commit boundary token and rely on convention | Less ceremony | Raises risk of silent misuse and ambiguous safety boundaries | Token is the explicit hook boundary |

## Validation evidence

- Pattern-only: aligned with staged procedural generation practice and deterministic replay conventions; no new `Ingest/Agent-Research/` notes were bound this run.

## Links

- Roadmap note: [[Phase-2-1-1-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-03-30-0923]]
- Workflow anchor: `2026-03-30 09:23` — Target `Phase-2-1-1-Stage-Family-Bodies-and-Boundary-Hooks`

