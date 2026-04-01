---
title: CDR — Phase 2.1 secondary (seed to world stages)
created: 2026-03-30
tags:
  - roadmap
  - conceptual-decision-record
  - genesis-mythos-master
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-03-30-2205]]"
decision_kind: deepen
queue_entry_id: resume-gmm-deepen-2-1-realign-20260330T220000Z
master_goal: "[[Source-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# Decision record — Phase 2.1 secondary (seed to world pipeline stages)

## Summary

Minted Phase 2 **secondary 2.1** as the **stage pipeline** that turns a deterministic **seed bundle** plus DM/player intent hook values into **staged world deltas**. Defined a natural-language stage spine (seed expansion → intent resolve → stage evaluation → simulation bootstrap → dry-run gate → commit boundary) with explicit ordering and “no partial commit on failure” semantics, staying consistent with Phase 2 primary’s pre-commit vs post dry-run separation.

## PMG alignment

Aligns with the master goal’s deterministic and collaboration-first emphasis by ensuring the stage pipeline is ordered and interface-driven: regeneration replays the same pipeline contract with stable bundle identity, while authoritative world mutation remains gated behind dry-run validation.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|-------------|--------|-----------|----------------|
| Treat generation as a single monolithic step | Simple execution model | Blurs commit boundary and weakens interface seams | Conflicts with the dry-run gate safety posture |
| Bind concrete engine stage IDs in this secondary | Earlier implementability | Locks conceptual naming too early | Conceptual track defers concrete registry closure |
| Skip explicit dry-run gate and trust errors later | Faster prototyping | Risks partial commit / corrupted state | Violates the “dry-run before commit” contract |

## Validation evidence

- Pattern-only: aligned with staged procedural generation practice and the project’s dry-run safety posture (no `Ingest/Agent-Research/` notes bound this run).

## Links

- **Roadmap note:** [[Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-03-30-2205]]

