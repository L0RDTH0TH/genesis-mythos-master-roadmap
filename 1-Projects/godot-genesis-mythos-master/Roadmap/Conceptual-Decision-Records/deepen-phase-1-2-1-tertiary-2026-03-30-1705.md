---
title: "CDR — Deepen Phase 1.2.1 (node taxonomy and topological order)"
created: 2026-03-30
tags:
  - roadmap
  - conceptual-decision-record
  - godot-genesis-mythos-master
para-type: Project
project-id: godot-genesis-mythos-master
parent_roadmap_note: "[[Phase-1-2-1-Node-Taxonomy-Edges-and-Topological-Order-Roadmap-2026-03-30-1705]]"
decision_kind: deepen
queue_entry_id: resume-gmm-deepen-121-20260330T170500Z
master_goal: "[[Source-godot-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# Decision record — Phase 1.2.1 tertiary

## Summary

Minted tertiary **1.2.1** defining **stage node taxonomy**, **edge kinds** (dependency vs ordering-only vs intent-hook), and **topological evaluation** rules so the procedural-generation graph remains a coherent DAG before deeper stage-specific notes.

## PMG alignment

Supports the master goal’s **ordered procedural pipeline** with **intent injection** and **deterministic enough** evaluation: naming node roles and edge semantics makes the graph **reviewable** and **replayable** in principle without prematurely fixing implementation.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|-------------|--------|---------|----------------|
| Skip 1.2.1; jump to concrete stage bodies in 1.2.2 | Faster narrative | Risks inconsistent edge meaning | Would weaken secondary **1.2** skeleton |
| Encode only “linear list of stages” (no edge taxonomy) | Simpler doc | Hides branching and hook attachment | Conflicts with stated DAG + injection model |
| Full schema + IDs at conceptual tier | Precise | Execution-owned; premature here | Deferred per dual-track contract |

## Validation evidence

- Pattern-only alignment with common **DAG build** and **topological sort** practice; no external synth notes linked.

## Links

- Roadmap note: [[Phase-1-2-1-Node-Taxonomy-Edges-and-Topological-Order-Roadmap-2026-03-30-1705]]
- Parent secondary: [[Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-03-30-1605]]
- Workflow anchor: `2026-03-30 17:05 | deepen | Phase-1-2-1-Node-Taxonomy-… | 1.2.1`
