---
title: Phase 1.2 (Execution) — Procedural Generation Graph Skeleton
created: 2026-04-11
tags:
  - roadmap
  - execution
  - godot
  - sandbox-comparand
project-id: godot-genesis-mythos-master
roadmap_track: execution
roadmap-level: secondary
phase-number: 1
subphase-index: "1.2"
status: in-progress
handoff_readiness: 84
conceptual_counterpart: "[[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-03-30-1605]]"
execution_mirror_of: "Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-03-30-1605"
---

# Phase 1.2 (Execution) — Procedural generation graph skeleton

Execution remint for **secondary 1.2** on the parallel spine. Binds the conceptual **DAG-of-stages** skeleton to **Godot lane (A)** orchestration seams (scene graph, signals, resource-driven stage payloads) and **Sandbox lane (B)** comparands, without inventing concrete stage bodies or claiming rollup/CI closure.

Parent execution context: [[../Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-04-10-2100]] · Sibling slice **1.1**: [[../Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-04-10-2110]].

## Intent mapping

| Intent target | Inspiration anchors | Execution mechanism | Validation signal |
| --- | --- | --- | --- |
| DAG-shaped generation with deterministic evaluation order | Conceptual 1.2 NL + PMG procedural spine | `GenerationGraphKernel` facade + ordered stage runner + explicit feedback channel (non-default) | AC-1.2-* + topological validation hooks (tertiary) |
| Godot lane graph hosting | Scene tree / signal docs (contract shorthand; verbatim citations in **1.2.x** tertiaries) | Stage nodes as `Node` shells + `signal` edges for cross-stage handoff | Tertiary test seams |
| Roll-up debt | **D-Exec-rollup-deferral-missing-roll-up-gates-20260411** | **No** CI/registry/verdict IDs claimed in-doc | Execution-Gates packets remain `structured_open` until real IDs |

## Scope (execution)

- Define **graph-level** contracts: stage identity, typed inputs/outputs, topological runner, dry-run vs commit, failure propagation along edges — aligned to **1.1** commit APIs (`apply_delta` / store seams), not a second world-state writer.
- Specify **lane-neutral** pseudocode for one evaluation pass; GDScript-shaped **verbatim** API proofs belong in **tertiary 1.2.1+** with `Task(research)` + allowlisted docs per godot-execution-guard.
- **`missing_roll_up_gates`** / acyclicity stress / performance budgets remain **execution-deferred** per decisions-log; do **not** frame them as blocking this structural mint.

## Graph kernel (lane-neutral sketch)

```text
function evaluate_graph(kernel, store, bus, graph_spec, mode):
  order = topological_sort(graph_spec.nodes, graph_spec.edges)
  for stage_id in order:
    inputs = gather_inputs(stage_id, store, graph_spec)
    outputs = kernel.run_stage(stage_id, inputs, mode)  # mode: DryRun | Commit
    if outputs.failed: propagate_failure(stage_id, graph_spec, mode)
    commit_or_stage(store, outputs, mode)
```

## Godot lane (A) — hosting sketch

| Conceptual element | Godot execution binding (shorthand) | Notes |
| --- | --- | --- |
| Stage node | `Node` or `RefCounted` shell registered on a **single** orchestrator parent | Ownership stays under the runtime graph host, not scattered `Node` mutations |
| Edge / ordering | Dataflow via **explicit** runner order + `signal` for optional notifications | **No** hidden cycles in default path; feedback uses explicit channel |
| Payloads | `Resource` or plain DTOs crossing stages | Aligns with **1.1** “no render writes to authoritative state” |
| Dry-run | Runner mode flag; no `apply_delta` on `DryRun` | Pairs with conceptual dry-run semantics |

> [!note] Code precision deferral
> New GDScript API **verbatim** citations and allowlisted URLs are **deferred** to tertiary execution deepens per **`godot_code_precision`** — this secondary stays at **interfaces + skeleton** only.

## Sandbox lane (B) — comparand

| Element | B-lane stand-in |
| --- | --- |
| Stage host | C++ `StageHost` interface (fixed-step scheduler handoff from **1.1** B row) |
| Ordering | Explicit `std::vector<StageId>` schedule from topological sort |
| Payloads | POD / arena-backed DTOs with copy discipline |

## Acceptance criteria (secondary 1.2)

| ID | Criterion | Evidence target | Status |
| --- | --- | --- | --- |
| AC-1.2-A | DAG + topological evaluation contract documented | Tables + pseudocode (this note) | Met (this note) |
| AC-1.2-B | Failure propagation + dry-run vs commit split | Runner sketch + policy bullets | Met (this note) |
| AC-1.2-C | Explicit non-default feedback path (no silent cycles) | Callout + optional `feedback_channel` stub | Met (this note) |

## Roll-up closure map (progressive evidence — **not** closed this run)

Open **`GMM-2.4.5-*`**, **`CI-seam-expansion`**, and graph-level **`missing_roll_up_gates`** rows remain **execution-deferred** until stress CI IDs and verdict tables land — consistent with **D-Exec-rollup-deferral-missing-roll-up-gates-20260411**. This mint advances **traceability** only.

| Gate family | This-run progress | Next evidence |
| --- | --- | --- |
| Acyclicity / topo proofs | Contract text only | Tertiary **1.2.1+** + CI harness IDs when available |
| Registry closure for `stage_id` | Not claimed | Execution registry slice (later phase) |

## Next structural intent

Tertiary **1.2.1** minted on parallel spine: [[Phase-1-2-1-Node-Taxonomy-Edges-and-Topological-Order-Roadmap-2026-04-11-2245]]. Next: tertiary **1.2.2** — graph execution semantics and subgraph runs (conceptual mirror: `Phase-1-2-2-*`). Queue follow-up should target **`next_subphase_index: "1.2.2"`** unless operator overrides.

## Related

- Tertiary **1.2.1** (execution): [[Phase-1-2-1-Node-Taxonomy-Edges-and-Topological-Order-Roadmap-2026-04-11-2245]]
- Conceptual authority: [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-03-30-1605]]
- Decisions (rollup deferral): [[../../../decisions-log]] (see **D-Exec-rollup-deferral-missing-roll-up-gates-20260411**)
