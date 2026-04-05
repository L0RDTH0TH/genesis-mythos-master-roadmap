---
title: CDR — Phase 1.2 procedural generation graph skeleton
created: 2026-03-30
tags:
  - roadmap
  - conceptual-decision-record
  - godot-genesis-mythos-master
para-type: Project
project-id: godot-genesis-mythos-master
parent_roadmap_note: "[[Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-03-30-1605]]"
decision_kind: deepen
queue_entry_id: resume-gmm-deepen-12-20260330T160500Z
master_goal: "[[Source-godot-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# Decision record — Phase 1.2 secondary (procedural generation graph skeleton)

## Summary

Minted secondary **1.2** describing a **DAG-shaped** procedural generation graph with **named intent injection points**, **topological evaluation**, and **dry-run / partial failure** behavior aligned with Phase 1 primary safety hooks. Chose **default DAG** with explicit feedback deferred over allowing implicit cycles in the skeleton.

## PMG alignment

Supports the master goal’s **deterministic / staged world changes** and **major regeneration** story: generation is ordered,Inspectable, and cannot commit authoritative state until dry-run clears—consistent with immersion-preserving collaboration and safe DM overrides.

## Alternatives and tradeoffs

| Alternative | Upside | Downide | Why not chosen |
|-------------|--------|---------|----------------|
| **Implicitly cyclic graph** | Expressive iterative refinement in one graph | Harder to reason about ordering and replay | Conflicts with default **DAG** assumption in primary open questions; feedback reserved for explicit edges or macro-passes |
| **Linear pipeline only** | Simplest MVP | Under-expresses branching biomes / parallel stages | Too weak for Phase 2+; secondary names **graph** with DAG discipline |
| **Bind concrete stage IDs** | Earlier registry closure | Locks names before Phase 2 scopes MVP | **Execution-deferred** per conceptual track |

## Validation evidence

- Pattern-only: layered-game and **staged world-build** pipeline practice (no new `Ingest/Agent-Research/` notes this run).

## Links

- **Roadmap note:** [[Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-03-30-1605]]
- **Workflow last row:** 2026-03-30 16:05 — `Phase-1-2-Procedural-Generation-Graph-Skeleton`
