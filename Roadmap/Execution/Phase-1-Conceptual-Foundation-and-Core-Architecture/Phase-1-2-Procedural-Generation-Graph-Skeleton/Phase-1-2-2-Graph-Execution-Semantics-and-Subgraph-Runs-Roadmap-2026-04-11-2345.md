---
title: Phase 1.2.2 (Execution) — Graph execution semantics and subgraph runs
created: 2026-04-11
tags:
  - roadmap
  - execution
  - godot
  - sandbox-comparand
project-id: godot-genesis-mythos-master
roadmap_track: execution
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.2.2"
status: in-progress
handoff_readiness: 85
conceptual_counterpart: "[[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-2-Graph-Execution-Semantics-and-Subgraph-Runs-Roadmap-2026-03-30-1805]]"
execution_mirror_of: "Phase-1-2-2-Graph-Execution-Semantics-and-Subgraph-Runs-Roadmap-2026-03-30-1805"
---

# Phase 1.2.2 (Execution) — Graph execution semantics and subgraph runs

Execution remint for **tertiary 1.2.2** on the parallel spine. Binds conceptual **serial vs wave** execution, **subgraph closure**, **prefix** runs, and **failure / empty propagation** to lane-neutral runner contracts, with **Godot stable** `Node` **process_mode** + **process_priority** verbatim anchors for **hosting metaphors** (subtree enable/disable and callback ordering). **`missing_roll_up_gates`**, stress **CI** IDs, and rollup **verdict closure** remain **execution-deferred** per **D-Exec-rollup-deferral-missing-roll-up-gates-20260411** — **not** claimed closed in-doc.

Parent secondary: [[Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-04-11-2230]] · Prior tertiary: [[Phase-1-2-1-Node-Taxonomy-Edges-and-Topological-Order-Roadmap-2026-04-11-2245]] · Decisions: [[../../../decisions-log]].

## Intent mapping

| Intent target | Inspiration anchors | Execution mechanism | Validation signal |
| --- | --- | --- | --- |
| Serial single-pass vs wave-parallel schedule | Conceptual 1.2.2 NL | Partition topo-ordered stages into **waves** of mutually dependency-ready stages; **ordering-only** edges serialize within a wave when they would race | AC-1.2.2-* + deterministic replay uses stable `StageId` tie-break from **1.2.1** |
| Subgraph regeneration | Conceptual subgraph closure | **Target** stages → expand **dependency predecessors** (reverse dep graph) → **invoke only** closed set; outside nodes **no-op** or **explicit out-of-subgraph** | Closure size + boundary audit row |
| Prefix / truncated runs | Conceptual prefix | Run **first k** stages of the topo list; downstream **skipped** unless policy attaches **snapshot / carry-forward** (execution-deferred) | Dry-run runner flag + skip ledger |
| Godot hosting metaphor | Scene tree subtrees + process ordering | **Subgraph** modeled as a **subtree** of stage hosts; **process_mode** / **priority** cite below as **metaphor** for gating and ordering — **not** a claim the proc-gen kernel is implemented via `_process` | Verbatim citations block |

## Scope

- **In:** Lane-neutral **evaluate_schedule** + **subgraph_closure** + **wave_partition** pseudocode; parallelism only when **no unresolved dependency** between peers (dependency edges only for readiness; ordering-only for tie/race rules per conceptual 1.2.2).
- **Out:** Worker pools, CI graph IR, perf proofs, or **claims** that **`missing_roll_up_gates`** / rollup HR / registry closure are satisfied.

## Lane-neutral execution schedule

### Serial default (MVP)

```text
function evaluate_serial(order, kernel, store, mode):
  for stage_id in order:  # order from 1.2.1 Kahn + tie-break
    run_stage(stage_id, kernel, store, mode)
```

### Wave partition (optional parallelism)

```text
function partition_waves(order, dep_edges, ordering_only_edges):
  waves = []
  remaining = set(order)
  while remaining not empty:
    ready = { s in remaining | predecessors_dep(s, dep_edges) subset (set(order) - remaining) }
    if ready empty: signal_deadlock_or_cycle()
    wave = ready  # may be >1 → parallel-eligible
    for (a,b) in ordering_only_edges where a in wave and b in wave:
      serialize_pair(a,b,wave)  # conceptual default: respect ordering-only over max parallelism
    append(waves, stable_sort(wave, stage_id_compare))
    remaining -= wave
  return waves
```

**Determinism:** Any parallel wave must still emit a **total order** for replay via **stable `StageId`** when committing results (matches **1.2.1** tie-break).

### Subgraph closure

```text
function subgraph_closure(targets, dep_edges):
  need = copy(targets)
  stack = copy(targets)
  while stack not empty:
    t = pop(stack)
    for p in upstream_dep_nodes(t, dep_edges):
      if p not in need: push(stack, p); add(need, p)
  return topological_sort_induced_subgraph(need, dep_edges)
```

Nodes **outside** `need` are **not invoked** for this run (conceptual **out of subgraph** semantics).

### Prefix run

```text
function evaluate_prefix(order, k, kernel, store, mode):
  for stage_id in order[0:k]:
    run_stage(stage_id, kernel, store, mode)
  # order[k:] skipped unless carry-forward policy (execution-deferred)
```

## Failure / empty propagation (lane-neutral)

- Aligns with **secondary 1.2** + **1.2.1**: validation failure or typed **empty** output → downstream **skip** or **propagate empty** until a **CommitBoundary**; **no** authoritative world commit on failed validation (cross-ref **1.1** commit seams).

## Godot lane (A) — verbatim anchors (stable docs)

**Processing behavior / subgraph metaphor** — `Node.process_mode` documents how a **node and its subtree** participate in processing; use as **hosting analogy** for “enable this subgraph of stages” vs “rest no-op”:

> The node's processing behavior. To check if the node can process in its current mode, use [can_process()](https://docs.godotengine.org/en/stable/classes/class_node.html#class-node-method-can-process).

Source: [Node — process_mode — Godot Engine stable class reference](https://docs.godotengine.org/en/stable/classes/class_node.html#class-node-property-process-mode)

**Callback ordering inside a frame** — when multiple stage hosts could run in the same **wave**, **process_priority** documents **deterministic ordering** independent of tree order:

> The node's execution order of the process callbacks ([_process()](https://docs.godotengine.org/en/stable/classes/class_node.html#class-node-private-method-process), [NOTIFICATION_PROCESS](https://docs.godotengine.org/en/stable/classes/class_node.html#class-node-constant-notification-process), and [NOTIFICATION_INTERNAL_PROCESS](https://docs.godotengine.org/en/stable/classes/class_node.html#class-node-constant-notification-internal-process)). Nodes whose priority value is lower call their process callbacks first, regardless of tree order.

Source: [Node — process_priority — Godot Engine stable class reference](https://docs.godotengine.org/en/stable/classes/class_node.html#class-node-property-process-priority)

**Binding:** Runtime **proc-gen** evaluation remains the **lane-neutral kernel + topo order** from **1.2.1**/**1.2**; these Godot quotes justify **subtree gating** and **intra-wave ordering** metaphors — **not** a claim that generation stages are implemented as `_process` callbacks.

## Sandbox lane (B) — comparand

| Element | B-lane stand-in |
| --- | --- |
| Subgraph | `std::unordered_set<StageId>` closure + induced edge list |
| Waves | `std::vector<std::vector<StageId>>` batches with explicit mutex on ordering-only pairs |
| Prefix | Truncate ordered `std::vector<StageId>` to first **k** |

## Acceptance criteria

| ID | Criterion | Evidence | Status |
| --- | --- | --- | --- |
| AC-1.2.2-A | Serial + wave + subgraph + prefix semantics documented | Pseudocode sections | Met |
| AC-1.2.2-B | Ordering-only vs parallelism conflict called out | `partition_waves` note | Met |
| AC-1.2.2-C | Godot verbatim citations present (`process_mode`, `process_priority`) | Blockquotes + stable URLs | Met |
| AC-1.2.2-D | Rollup / CI / verdict closure **not** claimed | Deferral callout | Met |

## Roll-up / CI / acyclicity (explicit deferral)

Open **`GMM-2.4.5-*`**, graph **`missing_roll_up_gates`**, and **wave stress** proofs remain **execution-deferred** until real **CI run IDs** and verdict tables land — per **D-Exec-rollup-deferral-missing-roll-up-gates-20260411**.

## Next structural intent

Tertiary **1.2.3** — **minted** on execution spine: [[Phase-1-2-3-Stage-Families-Specialization-and-Pipeline-Roles-Roadmap-2026-04-12-0015]]. Queue follow-up should target **`next_subphase_index: "1.2.4"`** unless operator overrides.

## Related

- Conceptual authority: [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-2-Graph-Execution-Semantics-and-Subgraph-Runs-Roadmap-2026-03-30-1805]]
- Upstream topo / taxonomy: [[Phase-1-2-1-Node-Taxonomy-Edges-and-Topological-Order-Roadmap-2026-04-11-2245]]
