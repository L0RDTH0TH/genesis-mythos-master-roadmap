---
title: Phase 1.2.2 — Graph execution semantics and subgraph runs
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.2.2"
project-id: sandbox-genesis-mythos-master
status: active
priority: high
progress: 42
handoff_readiness: 77
created: 2026-03-30
tags:
  - roadmap
  - sandbox-genesis-mythos-master
  - phase-1
para-type: Project
links:
  - "[[Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-03-30-1605]]"
  - "[[Phase-1-2-1-Node-Taxonomy-Edges-and-Topological-Order-Roadmap-2026-03-30-1705]]"
  - "[[Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-03-30-0430]]"
---

## Phase 1.2.2 — Graph execution semantics and subgraph runs

This tertiary slice defines **how** a topological order is **executed** as a generation pass: **waves vs strict serial**, how a **subgraph** is selected for regeneration, and how **empty or skipped outputs** propagate—without choosing a concrete scheduler, thread pool, or CI graph format.

## Scope

**In scope:** Single-pass vs multi-wave execution; **subgraph closure** (nodes + dependency predecessors); **prefix** and **intent-scoped** partial runs; **deterministic tie-break** when multiple topological orders exist; **parallelism policy** at NL level (only when branches are dependency-independent). **Out of scope:** Worker pools, job queues, asset-level staging, and machine-readable graph IR. **Execution-deferred:** profiling hooks, exact replay manifests, and registry of stable node IDs for tie-break.

## Behavior (natural language)

- **Execution pass:** One **generation pass** walks nodes in a **valid topological order** derived from **1.2.1**. Default MVP posture: **serial** execution in that order—simple to reason about and matches dry-run narrative.
- **Parallelism (optional):** When two or more nodes share **no unresolved dependency** between them (after expanding dependency edges only—not ordering-only edges as hard prerequisites), an implementation **may** schedule them **in parallel** in the same **wave**; **ordering-only** edges still constrain **relative order** within the wave when they would otherwise race. If parallel and serial schedules could diverge, **deterministic replay** requires a documented **tie-break** (**stable node ID** after **1.2.1** defaults).
- **Subgraph selection:** Regeneration selects a **non-empty** set of **target** nodes; the engine expands to the **transitive closure** of **dependency predecessors** so inputs exist. Nodes outside the subgraph are **not invoked** or are **no-op** with explicit **“out of subgraph”** semantics (aligns with **1.2.1** empty-subgraph case).
- **Prefix runs:** A **prefix** of the topological list runs when only early pipeline stages need re-execution (e.g. seed change before biome); downstream nodes are skipped or receive **carried-forward** state per policy—stated at execution, NL default: **no implicit reuse** without a snapshot boundary.
- **Failure / empty propagation:** If a node **fails validation** or emits **typed empty** output, downstream nodes behave per **secondary 1.2** and **1.2.1**: typically **skip** or **propagate empty** until a **commit** boundary; **no authoritative world commit** on failed validation.

## Interfaces

- **Upstream (1.2.1):** Consumes **node taxonomy**, **edge kinds**, and **topological ordering** definitions; this note adds **schedule semantics** only.
- **Upstream (secondary 1.2):** Aligns **dry-run**, **injection hooks**, and **partial failure** language with executable schedule.
- **Downstream (1.2.3+):** May specialize **stage families** (biome vs entity pipelines) using both taxonomy (**1.2.1**) and **execution semantics** here — see [[Phase-1-2-3-Stage-Families-Specialization-and-Pipeline-Roles-Roadmap-2026-03-30-1905]].
- **Cross-slice:** **Commit** and **validation** nodes remain ordered per **1.2.1**; execution waves must not reorder **dependency** constraints.

## Edge cases

- **Wave + ordering-only conflict:** If parallel wave would violate an **ordering-only** edge, **serialize** those two nodes or split waves—conceptual default: **respect ordering-only** over maximum parallelism.
- **Nondeterministic external inputs:** Stages that depend on **live** or **external** sources remain **explicitly labeled** in **1.2** / Phase 2; subgraph runs **exclude** them from deterministic replay unless snapshotted (**execution-deferred**).
- **Feedback / macro-pass:** Iterative refinement stays **outside** the default single-pass DAG; a second pass is a **new** invocation with updated inputs, not an implicit cycle.

## Open questions

- Whether the **first vertical slice** pins **strict serial** only vs allows **one parallel wave** for independent branches—**Phase 2 MVP** scope.
- **Prefix carry-forward** policy for large worlds (incremental vs full recompute)—**simulation** interaction; NL deferred.

## Pseudo-code readiness

Readers can sketch **wave partitioning** (independent sets), **subgraph closure** (BFS/DFS on reversed edges), and **prefix truncation** of a sorted node list. Threading and IO scheduling are **execution** artifacts.

## Research integration

> [!note] External grounding
> No `Ingest/Agent-Research/` notes were bound this run; alignment is **pattern-only** from DAG execution, build systems, and staged data pipelines.
