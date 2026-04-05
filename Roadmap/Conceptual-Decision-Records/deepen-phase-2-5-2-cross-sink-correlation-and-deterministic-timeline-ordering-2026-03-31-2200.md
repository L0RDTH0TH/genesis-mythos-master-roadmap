---
title: "CDR — Phase 2.5.2 cross-sink correlation + deterministic timeline ordering"
created: 2026-03-31
tags:
  - roadmap
  - conceptual-decision-record
  - sandbox-genesis-mythos-master
para-type: Project
project-id: sandbox-genesis-mythos-master
parent_roadmap_note: "[[Phase-2-5-2-Cross-Sink-Correlation-and-Deterministic-Timeline-Ordering-Roadmap-2026-03-31-2200]]"
decision_kind: deepen
queue_entry_id: resume-deepen-gmm-252-20260330T132654Z-forward
master_goal: "[[Source-sandbox-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# Decision record — Phase 2.5.2 deepen

## Summary

Chose explicit **cross-sink correlation keys** plus **deterministic timeline ordering** (lane priority matrix, replay-stable merge) so multi-sink telemetry from **2.5.1** composes into one audit narrative without losing **2.4.5** branch semantics. **GMM-2.4.5-*** identifiers remain reference-only authority pointers for execution closure artifacts.

## PMG alignment

Advances the procedural-generation / world-building roadmap toward traceable post-commit audit without pretending execution schemas or retention exist; keeps conceptual authority on **what must be ordered and correlated**, not **how infra stores it**.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|-------------|--------|----------|----------------|
| Single unified sink only | Simpler ordering | Loses separation of operator vs validator surfaces | Contradicts **2.5.1** sink binding contract |
| Wall-clock primary ordering | Familiar ops model | Non-deterministic across replay | Violates replay-stable audit story from **2.4.5** |
| Per-sink independent timelines | Easier sharding | Breaks cross-sink audit coherence | Fails operator audit bridge goal |

## Validation evidence

- Pattern-only continuity from **2.5.1**, **2.5** secondary, and **2.4.5** finalization contracts; no new `Ingest/Agent-Research/` notes this run.

## Links

- Roadmap note: [[Phase-2-5-2-Cross-Sink-Correlation-and-Deterministic-Timeline-Ordering-Roadmap-2026-03-31-2200]]
- Workflow anchor: last deepen row `2026-03-31 22:00`, Target `Phase-2-5-2-Cross-Sink-Correlation-and-Deterministic-Timeline-Ordering`, queue_entry_id `resume-deepen-gmm-252-20260330T132654Z-forward`
