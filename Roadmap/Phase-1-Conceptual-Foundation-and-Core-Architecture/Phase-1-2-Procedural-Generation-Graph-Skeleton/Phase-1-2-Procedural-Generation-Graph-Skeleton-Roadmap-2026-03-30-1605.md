---
title: Phase 1.2 — Procedural Generation Graph Skeleton
roadmap-level: secondary
phase-number: 1
subphase-index: "1.2"
project-id: genesis-mythos-master
status: active
priority: high
progress: 35
handoff_readiness: 76
created: 2026-03-30
tags:
  - roadmap
  - genesis-mythos-master
  - phase-1
para-type: Project
links:
  - "[[Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-03-30-0430]]"
---

## Phase 1.2 — Procedural generation graph skeleton

This secondary slice defines the **directed graph** of procedural-generation **stages**: what each stage consumes and produces, how **intent injection points** attach to nodes or edges, and how evaluation order stays **deterministic enough** for save/reload and DM overrides without binding a concrete engine. It complements **1.1** (layering and interfaces) by describing **where** generation sits relative to world state and simulation.

## Scope

**In scope:** Stage taxonomy (e.g. seed expansion, biome assignment, entity spawn, narrative glue); **edges** as data dependencies; **topological evaluation order**; explicit **injection points** for DM/player intents and seeds; failure propagation along the graph; **dry-run** as a graph-level mode that does not commit world state.

**Out of scope:** Concrete node implementations, GPU terrain, asset pipeline IDs, plugin load order, and execution-track graph serialization formats. **Execution-deferred:** CI proving acyclicity, performance budgets, and registry closure for stage IDs.

## Behavior (natural language)

- The **generation graph** is a **DAG** by default; each **node** is a stage that reads typed inputs (seed bundle, prior stage outputs, world-state queries) and emits typed outputs (mutations, overlays, or **staged deltas** pending commit).
- **Evaluation** runs in topological order; stages may not read outputs of nodes that appear later in that order. **Feedback** or iterative refinement, if needed later, is modeled as **explicit feedback edges** or a separate “macro-pass” — not hidden cycles in the default skeleton.
- **Intent injection points** are **named hooks** on specific nodes or on the edges between world state and a stage (e.g. “after biome mask, before entity placement”). DM/player intents attach to these hooks with priority rules deferred to execution track.
- **Ordering vs live loop:** Offline or pre-session generation runs the full graph (or a prefix) **before** the live **input → simulation → world state → render** loop from **1.1**; mid-campaign regeneration invokes a **subgraph** with snapshot + dry-run invariants from the Phase 1 primary.

## Interfaces

- **Upstream:** Seeds, master config, and **layering contracts** from **1.1** (generation never bypasses world-state commit APIs when mutating authoritative state).
- **Downstream:** Phase 2 deepens **node bodies** and asset-level detail; this slice only supplies **graph shape** and **hook names**.
- **Adjacent slices:** Primary Phase 1 lists safety hooks; **1.1** defines layers — this slice states which **stages** may touch which **layer boundaries** (e.g. render-only previews vs committed world state).

## Edge cases

- **Partial graph failure:** A stage fails validation — downstream nodes are skipped or receive **empty typed outputs** per policy; no commit until dry-run clears (aligns with Phase 1 primary **partial generation failure**).
- **Non-deterministic sources:** External APIs or clocks must be isolated in explicitly labeled stages so save/replay policy can exclude or snapshot them (TBD execution detail; conceptual default: **no hidden nondeterminism** in core spine stages).
- **Scope creep:** Stages must not silently expand into full simulation; anything that looks like “tick rules” routes to **simulation** after generation commits.

## Open questions

- Whether **minimum viable** graph for vertical slice is a **linear** pipeline vs full branching (to be resolved when Phase 2 scopes MVP).
- Exact **hook naming** convention (topic-like vs path-like) — defer to execution registry unless PMG forces earlier lock-in.

## Pseudo-code readiness

Readers can sketch **node lists and edges** as bullet graphs and **ordered stage lists** without a codebase. Algorithm-shaped **pseudo-code for individual stages** belongs in **tertiary** notes (**1.2.1+**) or Phase 2; this secondary stops at **graph skeleton + contracts**.

## Research integration

> [!note] External grounding
> No `Ingest/Agent-Research/` notes were bound this run; alignment is **pattern-only** from DAG-shaped procedural pipelines and staged world-build practice.

## Risk register v0

| Risk | Mitigation (conceptual; execution may add CI/tooling) |
|------|--------------------------------------------------------|
| **DAG violated in practice** | Topological validation before run; cycles only via explicit feedback edges — **execution-deferred:** CI acyclicity check |
| **Nondeterminism leaks into spine** | Isolate clocks/APIs in labeled stages (see Edge cases); replay policy TBD execution |
| **Stage scope creeps into simulation** | Routing rule: tick rules stay in simulation after generation commits |
| **Intent-hook naming ambiguous** | Registry + stable IDs — **execution-deferred**; hooks named at NL level here |
| **Partial graph failure corrupts state** | Dry-run + no commit until validation clears (aligns with Phase 1 primary) |

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton"
WHERE roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
