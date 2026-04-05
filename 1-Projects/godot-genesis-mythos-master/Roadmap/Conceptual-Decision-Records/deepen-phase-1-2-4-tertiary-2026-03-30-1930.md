---
title: CDR — Deepen Phase 1.2.4 determinism and replay contracts
created: 2026-03-30
tags:
  - roadmap
  - conceptual-decision-record
  - godot-genesis-mythos-master
para-type: Project
project-id: godot-genesis-mythos-master
parent_roadmap_note: "[[Phase-1-2-4-Determinism-Seed-Bundles-Stable-Identity-and-Replay-Contracts-Roadmap-2026-03-30-1930]]"
decision_kind: deepen
queue_entry_id: resume-gmm-deepen-124-20260330T193000Z
master_goal: "[[Source-godot-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# Conceptual decision record — Phase 1.2.4

## Summary

Chose to structure **1.2.4** around **seed bundles, stable node identity, determinism contracts, and replay intent** as the next procedural-graph tertiary after **1.2.3** pipeline roles—so reproducibility stays explicit before Phase 2 serialization and CI.

## PMG alignment

Keeps generation **inspectable and debuggable**: teams can reason about **what must match** across runs before investing in engine-specific hashes or capture formats.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|---------------|--------|----------|------------------|
| **1.2.4 = graph optimization / fusion** | Performance narrative early | Skips reproducibility foundation | After **1.2.2** execution and **1.2.3** roles, determinism is the tighter gap |
| **1.2.4 = IR export / codegen** | Closer to implementation | Too execution-shaped for conceptual slice | Deferred to **1.2.5+** or Phase 2 |
| **Merge determinism into 1.2.2** | Fewer files | Overloads execution semantics note | Separation kept for checklist clarity |

## Validation evidence

- Pattern-only: reproducible pipelines, seeded procedural content, DAG eval practice.
- No external research notes attached this run.

## Links

- Parent: [[Phase-1-2-4-Determinism-Seed-Bundles-Stable-Identity-and-Replay-Contracts-Roadmap-2026-03-30-1930]]
- Workflow anchor: 2026-03-30 19:30 — Phase-1-2-4-Determinism-Seed-Bundles-Stable-Identity-and-Replay-Contracts
