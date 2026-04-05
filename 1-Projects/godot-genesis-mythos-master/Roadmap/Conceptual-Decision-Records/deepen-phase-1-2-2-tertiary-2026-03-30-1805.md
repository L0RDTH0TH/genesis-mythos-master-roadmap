---
title: "CDR — Deepen Phase 1.2.2 (graph execution semantics and subgraph runs)"
created: 2026-03-30
tags:
  - roadmap
  - conceptual-decision-record
  - godot-genesis-mythos-master
para-type: Project
project-id: godot-genesis-mythos-master
parent_roadmap_note: "[[Phase-1-2-2-Graph-Execution-Semantics-and-Subgraph-Runs-Roadmap-2026-03-30-1805]]"
decision_kind: deepen
queue_entry_id: resume-gmm-deepen-122-20260330T180500Z
master_goal: "[[Source-godot-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# Decision record — Phase 1.2.2 tertiary

## Summary

Minted tertiary **1.2.2** defining **graph execution semantics**: serial-by-default topological walk, optional **wave-level parallelism** under dependency independence, **subgraph closure** for regeneration, **prefix** partial runs, and **empty/failure propagation**—bridging **1.2.1** taxonomy to schedulable behavior without fixing an engine.

## PMG alignment

Supports **modular procedural generation** and **deterministic enough** replay: explicit schedule rules and subgraph selection make **regeneration** and **DM overrides** **predictable** at the design layer, matching the master goal’s **staged world build** and **intent injection** story.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|-------------|--------|---------|----------------|
| Mandate full parallel execution everywhere | Theoretical throughput | Conflicts with ordering-only edges | Too strong for conceptual tier |
| Subgraph = targets only (no dependency closure) | Smaller runs | Broken inputs | Violates DAG semantics |
| Encode thread-pool and IO in Phase 1 | Concrete | Execution-owned | Deferred per dual-track contract |

## Validation evidence

- Pattern-only alignment with **DAG execution**, **build-graph waves**, and **incremental rebuild** practice; no external synth notes linked.

## Links

- Roadmap note: [[Phase-1-2-2-Graph-Execution-Semantics-and-Subgraph-Runs-Roadmap-2026-03-30-1805]]
- Parent secondary: [[Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-03-30-1605]]
- Prior tertiary: [[Phase-1-2-1-Node-Taxonomy-Edges-and-Topological-Order-Roadmap-2026-03-30-1705]]
- Workflow anchor: `2026-03-30 18:05 | deepen | Phase-1-2-2-Graph-Execution… | 1.2.2`
