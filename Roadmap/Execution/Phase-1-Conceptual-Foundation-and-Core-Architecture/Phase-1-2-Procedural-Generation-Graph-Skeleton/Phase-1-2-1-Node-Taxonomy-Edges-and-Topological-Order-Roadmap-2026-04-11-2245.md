---
title: Phase 1.2.1 (Execution) — Node taxonomy, edges, and topological order
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
subphase-index: "1.2.1"
status: in-progress
handoff_readiness: 85
conceptual_counterpart: "[[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-1-Node-Taxonomy-Edges-and-Topological-Order-Roadmap-2026-03-30-1705]]"
execution_mirror_of: "Phase-1-2-1-Node-Taxonomy-Edges-and-Topological-Order-Roadmap-2026-03-30-1705"
---

# Phase 1.2.1 (Execution) — Node taxonomy, edges, and topological order

Execution remint for **tertiary 1.2.1** on the parallel spine. Refines the conceptual **DAG-of-stages** taxonomy into **lane-neutral** stage roles + edge kinds + **Kahn-style** topological walk sketch, with **Godot stable** `Node` / `GraphEdit` verbatim anchors for tree vs graph editing metaphors. **`missing_roll_up_gates`**, stress **CI** IDs, and rollup **verdict closure** remain **execution-deferred** per **D-Exec-rollup-deferral-missing-roll-up-gates-20260411** — **not** claimed closed in-doc.

Parent secondary: [[Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-04-11-2230]] · Decisions: [[../../../decisions-log]].

## Intent mapping

| Intent target | Inspiration anchors | Execution mechanism | Validation signal |
| --- | --- | --- | --- |
| Typed stage nodes + ports | Conceptual 1.2.1 NL | `StageId` + `NodeKind` enum + port maps on DTOs | AC-1.2.1-* + runner consumes topo order |
| Dependency vs ordering-only edges | Conceptual edge semantics | Edge records `{from,to,kind}` with `Dependency` / `OrderingOnly` / `IntentHook` | Topo sort respects only `Dependency` for readiness |
| Topological evaluation | Secondary 1.2 kernel | Kahn queue over in-degree table built from dependency edges | Deterministic tie-break: stable `StageId` then ordering edges |
| Godot hosting metaphor | Godot `Node` tree + `GraphEdit` for editor graphs | Runtime stages hosted as `Node` shells under one orchestrator; **editor** graph tooling is **GraphEdit** + `GraphNode` (visualization / tooling), not the proc-gen kernel | Tertiary cites below |

## Scope

- **In:** Node kinds (`Generator`, `Transform`, `ValidationGate`, `CommitBoundary`), edge kinds (data **dependency**, **ordering-only**, **intent-hook**), **acyclic** default DAG + explicit feedback macro-pass (per conceptual 1.2), **Kahn**-shaped evaluation order contract, layer-touch tags crossing to **1.1**.
- **Out:** Concrete CI graph serialization, perf budgets, repository of stage bodies, or **claims** that **`missing_roll_up_gates`** / acyclicity proofs / HR closure are satisfied.

## Lane-neutral taxonomy

### Stage nodes (roles)

| Kind | Responsibility | Typical layer-touch |
| --- | --- | --- |
| `Generator` | Expands seeds / parameters into staged outputs | Read-only world + **staging** writes only |
| `Transform` | Maps staged inputs → staged outputs | May read multiple layers; writes **staging** |
| `ValidationGate` | Predicate on staged graph / world; **blocks** downstream commit on failure | Read **validation** surfaces; no authoritative commit |
| `CommitBoundary` | Invokes **1.1** `apply_delta` / store commit when upstream gates pass | **Commit**-class; pairs with dry-run runner mode |

### Edges

- **Dependency:** upstream output **required** before downstream runs (feeds Kahn in-degree).
- **Ordering-only:** refines tie-break when multiple valid topos exist (aligns with conceptual “stable ID” fallback).
- **Intent-hook:** attaches DM/player intent to a named hook; does **not** imply data readiness unless also linked by a dependency edge.

## Topological order (lane-neutral)

```text
function kahn_topological(nodes, dep_edges):
  in_degree = count_incoming_dep_edges(nodes, dep_edges)
  queue = min_heap_by_stable_stage_id({ n where in_degree[n] == 0 })
  order = []
  while queue not empty:
    n = pop(queue); append(order, n)
    for each m in downstream_dep_neighbors(n, dep_edges):
      in_degree[m] -= 1
      if in_degree[m] == 0: push(queue, m)
  if len(order) != len(nodes): signal_cycle_or_disconnected_scope()
  apply_ordering_only_ties(order, ordering_only_edges, stable_id_compare)
  return order
```

**Feedback / macro-pass:** Any **non-DAG** feedback is **out of scope** for this tertiary’s default pass; model as a **second** invocation of the runner over an explicit feedback channel (secondary **1.2**), not as a hidden cycle.

## Godot lane (A) — verbatim anchors (stable docs)

**Scene tree / node building blocks** — official class reference (`Node`):

> Nodes are Godot's building blocks. They can be assigned as the child of another node, resulting in a tree arrangement. A given node can contain any number of nodes as children with the requirement that all siblings (direct children of a node) should have unique names.

Source: [Node — Godot Engine stable class reference](https://docs.godotengine.org/en/stable/classes/class_node.html#description)

**Graph editor control** — when tooling visualizes graphs (visual shaders, user tools), **`GraphEdit`** is the container for **`GraphNode`** children:

> GraphEdit provides tools for creation, manipulation, and display of various graphs. Its main purpose in the engine is to power the visual programming systems, such as visual shaders, but it is also available for use in user projects.
>
> GraphEdit by itself is only an empty container, representing an infinite grid where GraphNodes can be placed. Each GraphNode represents a node in the graph, a single unit of data in the connected scheme. GraphEdit, in turn, helps to control various interactions with nodes and between nodes. When the user attempts to connect, disconnect, or delete a GraphNode, a signal is emitted in the GraphEdit, but no action is taken by default. It is the responsibility of the programmer utilizing this control to implement the necessary logic to determine how each request should be handled.

Source: [GraphEdit — Godot Engine stable class reference](https://docs.godotengine.org/en/stable/classes/class_graphedit.html#description)

**Binding:** Runtime **proc-gen** evaluation uses the **kernel + topo order** from this note; **GraphEdit** citations justify **editor/tooling** graphs and connection **signals** — not a claim that the gameplay proc-gen pipeline is implemented inside `GraphEdit`.

## Sandbox lane (B) — comparand

| Element | B-lane stand-in |
| --- | --- |
| Stage instance | `StageHost` / POD handle |
| Edge store | `std::vector<EdgeRecord>` with explicit `EdgeKind` |
| Topo | `std::vector<StageId>` from Kahn on dependency edges only |

## Acceptance criteria

| ID | Criterion | Evidence | Status |
| --- | --- | --- | --- |
| AC-1.2.1-A | Node kinds + edge kinds enumerated and mapped to runner inputs | Tables above | Met |
| AC-1.2.1-B | Topological evaluation contract (Kahn + ordering-only tie-break) | Pseudocode | Met |
| AC-1.2.1-C | Godot verbatim citations present for `Node` + `GraphEdit` | Blockquotes + stable URLs | Met |
| AC-1.2.1-D | Rollup / CI / acyclicity stress **not** claimed closed | This section + deferral callout | Met |

## Roll-up / CI / acyclicity (explicit deferral)

Open **`GMM-2.4.5-*`**, graph **`missing_roll_up_gates`**, and **acyclicity proof** artifacts remain **execution-deferred** until real **CI run IDs** and verdict tables land — per **D-Exec-rollup-deferral-missing-roll-up-gates-20260411**. This note adds **traceability** and **taxonomy** only.

## Next structural intent

Tertiary **1.2.2** minted — [[Phase-1-2-2-Graph-Execution-Semantics-and-Subgraph-Runs-Roadmap-2026-04-11-2345]]. Next sibling: **1.2.3** stage families (conceptual mirror: `Phase-1-2-3-*`). Queue follow-up should target **`next_subphase_index: "1.2.3"`** unless operator overrides.

## Related

- Conceptual authority: [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-1-Node-Taxonomy-Edges-and-Topological-Order-Roadmap-2026-03-30-1705]]
- Secondary **1.2**: [[Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-04-11-2230]]
- Sibling **1.2.2**: [[Phase-1-2-2-Graph-Execution-Semantics-and-Subgraph-Runs-Roadmap-2026-04-11-2345]]
