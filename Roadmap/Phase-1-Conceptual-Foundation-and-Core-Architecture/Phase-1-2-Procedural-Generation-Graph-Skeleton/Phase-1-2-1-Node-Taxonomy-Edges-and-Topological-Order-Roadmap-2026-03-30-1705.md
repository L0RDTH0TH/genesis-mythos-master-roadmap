---
title: Phase 1.2.1 — Node taxonomy, edges, and topological order
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.2.1"
project-id: sandbox-genesis-mythos-master
status: active
priority: high
progress: 40
handoff_readiness: 77
created: 2026-03-30
tags:
  - roadmap
  - sandbox-genesis-mythos-master
  - phase-1
para-type: Project
links:
  - "[[Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-03-30-1605]]"
  - "[[Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-03-30-0430]]"
---

## Phase 1.2.1 — Node taxonomy, edges, and topological order

This tertiary slice pins **what counts as a graph node**, what **edge kinds** mean for data flow and ordering, and how **topological evaluation** is defined so the secondary **1.2** skeleton stays implementable without fixing concrete stage bodies yet.

## Scope

**In scope:** Classification of **stage nodes** (generator, transform, validation gate, world-commit boundary); **edge kinds** (data dependency, ordering-only, intent-hook attachment); **topological sort** as the canonical evaluation rule; **layer-touch tags** per node (which 1.1 layers may be read or written). **Out of scope:** Per-stage algorithms, asset IDs, plugin manifests, and CI graph serialization. **Execution-deferred:** machine-readable graph schema, cycle detection in CI, performance profiling per edge.

## Behavior (natural language)

- **Nodes** are **typed stages**. Each node declares **inputs** (from seeds, prior nodes, or read-only world queries) and **outputs** (staged deltas, overlays, or validation results). Nodes are **not** arbitrary code blobs at this tier—they are **named roles** (e.g. `expand-seed`, `assign-biome-mask`, `place-entities`, `validate-graph`, `commit-world`).
- **Edges** connect an output **port** of one node to an input **port** of another. **Dependency edges** require the upstream output before downstream runs. **Ordering-only edges** constrain schedule when no strict data dependency exists but side-effect order matters (e.g. logging before commit). **Intent-hook edges** attach DM/player intent to a **named hook** on a node or on the boundary between two nodes (priority resolution deferred to execution).
- **Topological order** is a linear order consistent with all **dependency edges**; **ordering-only** edges refine ties without adding data prerequisites. The default spine is **acyclic**; any **feedback** path is explicitly modeled as a separate macro-pass or labeled feedback edge set, not as an implicit cycle in the default DAG.
- **Evaluation** walks the sorted list once per “generation pass”; nodes skipped after partial failure still respect **downstream empty-output** policy from secondary **1.2**.

## Interfaces

- **Upstream (secondary 1.2):** Inherits DAG + dry-run + injection-point vocabulary; this note refines **node/edge semantics** only.
- **Upstream (1.1):** Each node may carry **layer-touch** metadata: which layer boundaries it may cross on read vs write (aligns with layering contracts).
- **Downstream ([[Phase-1-2-2-Graph-Execution-Semantics-and-Subgraph-Runs-Roadmap-2026-03-30-1805]] / 1.2.3+):** **1.2.2** pins execution semantics and subgraph runs; later tertiaries can specialize **stage families** (e.g. biome vs entity pipelines) using this taxonomy without redefining edges.
- **Cross-slice:** Phase 1 primary **safety** hooks apply at **commit**-class nodes; this slice names where those nodes sit in the sort order relative to **validation** nodes.

## Edge cases

- **Multiple valid topological orders:** Allowed if all dependency constraints are satisfied; **determinism for replay** is execution’s job (stable tie-break via declared **ordering-only** edges or node IDs)—conceptual default: **stable ID order** as fallback.
- **Empty subgraph:** Regeneration selects a **prefix** or **subgraph**; nodes outside the subgraph are **no-op** or **not invoked**—must be stated in execution; NL default: **skip with explicit “not in subgraph”** semantics.
- **Validation vs commit ordering:** A **validation** node may sit **before** the **commit** node; failed validation **blocks** commit downstream without mutating authoritative state (aligns with dry-run).

## Open questions

- Whether **minimum vertical slice** uses a **strict linear** chain vs parallel branches—left for **1.2.2+** / Phase 2 when MVP scope locks.
- **Port naming** convention (stable vs human-readable only)—registry on execution track unless PMG forces earlier lock-in.

## Pseudo-code readiness

Readers can sketch **adjacency lists**, **Kahn-style topological walk**, and **node-type enums** without a repo. Per-stage **pseudo-code** and **GPU/asset** detail belong in later tertiaries or Phase 2; this note stops at **taxonomy + ordering semantics**.

## Research integration

> [!note] External grounding
> No `Ingest/Agent-Research/` notes were bound this run; alignment is **pattern-only** from DAG pipelines and build-graph practice.
