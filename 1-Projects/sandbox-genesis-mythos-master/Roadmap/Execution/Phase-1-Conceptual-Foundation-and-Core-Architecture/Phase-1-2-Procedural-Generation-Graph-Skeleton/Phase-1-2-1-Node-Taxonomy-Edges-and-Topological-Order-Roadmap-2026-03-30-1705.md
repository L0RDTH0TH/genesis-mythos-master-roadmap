---
title: Phase 1.2.1 - Execution (Node taxonomy, edges, and topological order)
roadmap-level: tertiary
roadmap_track: execution
conceptual_counterpart: "[[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-1-Node-Taxonomy-Edges-and-Topological-Order-Roadmap-2026-03-30-1705]]"
phase-number: 1
subphase-index: "1.2.1"
project-id: sandbox-genesis-mythos-master
status: in-progress
handoff_readiness: 87
handoff_gaps:
  - "Primary Phase 1 roll-up remains open until execution tertiary 1.2.2 (subgraph-run semantics); DEF-* evidence notes refreshed 2026-04-08"
progress: 54
created: 2026-04-07
tags:
  - roadmap
  - execution
  - sandbox-genesis-mythos-master
  - phase-1
para-type: Project
links:
  - "[[Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-03-30-1605]]"
  - "[[../../roadmap-state-execution]]"
---

## Phase 1.2.1 - Execution mirror (node taxonomy, edges, and topological order)

> **Authority:** This tertiary execution mirror converts conceptual 1.2.1 into implementation-ready graph taxonomy contracts (typed node and edge descriptors, deterministic topological ordering pseudocode, and testable AC rows). Deferred execution closure artifacts remain explicit: **DEF-REG-CI** and **DEF-GMM-245**.

## Execution scope

| In scope | Deferred on this slice |
| --- | --- |
| Typed stage node taxonomy with stable category tags | Registry and CI closure artifacts (DEF-REG-CI) |
| Edge-kind semantics for dependency, ordering-only, and intent-hook flows | GMM-2.4.5-* compare automation (DEF-GMM-245) |
| Deterministic topological order contract and tie-break policy | Runtime cycle proofing telemetry |
| Layer-touch metadata for read/write boundaries per node | Plugin ABI/runtime packaging details |

## Typed interfaces (tertiary-level contracts)

```typescript
type StageId = string & { __brand: "StageId" };
type EdgeId = string & { __brand: "EdgeId" };
type HookId = string & { __brand: "HookId" };

type NodeKind = "generator" | "transform" | "validator" | "commit_boundary";
type EdgeKind = "dependency" | "ordering_only" | "intent_hook";

interface LayerTouch {
  readonly reads: readonly string[];
  readonly writes: readonly string[];
}

interface GraphNode {
  readonly id: StageId;
  readonly kind: NodeKind;
  readonly layerTouch: LayerTouch;
  readonly inputPorts: readonly string[];
  readonly outputPorts: readonly string[];
}

interface GraphEdge {
  readonly id: EdgeId;
  readonly kind: EdgeKind;
  readonly from: StageId;
  readonly to: StageId;
  readonly fromPort?: string;
  readonly toPort?: string;
  readonly hookId?: HookId;
}
```

## Pseudocode (deterministic topological ordering)

```pseudo
function resolveExecutionOrder(nodes, edges):
  deps = filter(edges, kind == dependency)
  orderHints = filter(edges, kind == ordering_only)
  sorted = kahnTopologicalSort(nodes, deps)
  stable = applyOrderingHints(sorted, orderHints)
  return stableByNodeId(stable)

function runGraphPass(nodes, edges, hooks):
  ordered = resolveExecutionOrder(nodes, edges)
  for node in ordered:
    ctx = applyIntentHooksBefore(node, hooks)
    result = executeNode(node, ctx)
    if result.failed:
      return reject(result.error)
    publishNodeOutputs(node, result)
    applyIntentHooksAfter(node, hooks)
  return accept("graph-pass-complete")
```

## Testable acceptance criteria (AC)

| ID | Given | When | Then |
| --- | --- | --- | --- |
| **AC-P1.2.1-001** | Graph nodes carry declared `NodeKind` and layer-touch metadata | Validation pass executes | Every node has allowed read/write layer boundaries and non-empty port sets |
| **AC-P1.2.1-002** | Mixed dependency and ordering-only edges | Resolver computes execution order | Dependency constraints are satisfied and ordering-only edges break ties deterministically |
| **AC-P1.2.1-003** | Two valid dependency-preserving orders | Stable tie-break applied | Output order is identical across identical inputs and node ids |
| **AC-P1.2.1-004** | Intent-hook edge attached to a node boundary | Pass executes for that node | Hook context is applied at the declared boundary only, without mutating unrelated nodes |
| **AC-P1.2.1-005** | Validator node fails before commit boundary node | Graph pass continues | Commit boundary is never executed and no authoritative world-state commit occurs |

## Explicit deferrals

| ID | Deferred artifact | Reason |
| --- | --- | --- |
| **DEF-REG-CI** | Registry and CI closure records for node/edge schemas | Reserved for execution roll-up pass after tertiary 1.2 chain |
| **DEF-GMM-245** | GMM-2.4.5-* compare-table automation | Deliberately postponed until execution-tail validation bundle |

## Next structural targets

1. Mint execution tertiary **1.2.2** under this folder for subgraph execution semantics and deterministic subgraph-run boundaries.
2. Re-run Phase 1 roll-up evidence reconciliation after 1.2.2 is linked and validated.

## Related

- Conceptual tertiary: [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-1-Node-Taxonomy-Edges-and-Topological-Order-Roadmap-2026-03-30-1705]]
- Execution secondary parent: [[Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-03-30-1605]]
- Execution state: [[../../roadmap-state-execution]] · [[../../workflow_state-execution]]
