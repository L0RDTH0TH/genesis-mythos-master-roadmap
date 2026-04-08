---
title: Phase 1.2.2 - Execution (Graph execution semantics and subgraph runs)
roadmap-level: tertiary
roadmap_track: execution
conceptual_counterpart: "[[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-2-Graph-Execution-Semantics-and-Subgraph-Runs-Roadmap-2026-03-30-1805]]"
phase-number: 1
subphase-index: "1.2.2"
project-id: sandbox-genesis-mythos-master
status: in-progress
handoff_readiness: 88
progress: 58
created: 2026-04-08
tags:
  - roadmap
  - execution
  - sandbox-genesis-mythos-master
  - phase-1
para-type: Project
links:
  - "[[Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-03-30-1605]]"
  - "[[Phase-1-2-1-Node-Taxonomy-Edges-and-Topological-Order-Roadmap-2026-03-30-1705]]"
  - "[[../../roadmap-state-execution]]"
---

## Phase 1.2.2 - Execution mirror (graph execution semantics and subgraph runs)

> **Authority:** This tertiary execution mirror converts conceptual 1.2.2 into implementation-ready scheduling and subgraph-run contracts (typed execution interfaces, deterministic subgraph-closure pseudocode, and testable AC rows). Deferred closure artifacts remain explicit: **DEF-REG-CI** and **DEF-GMM-245**.

## Execution scope

| In scope | Deferred on this slice |
| --- | --- |
| Deterministic graph-pass semantics (serial baseline + bounded wave parallel option) | Registry and CI closure artifacts (DEF-REG-CI) |
| Subgraph closure rules for dependency predecessor expansion | GMM-2.4.5-* compare automation (DEF-GMM-245) |
| Prefix-run boundaries and explicit carry-forward policy constraints | Runtime scheduling telemetry and benchmark packs |
| Failure/typed-empty propagation up to commit boundary constraints | Worker-pool/job-queue implementation details |

## Typed interfaces (tertiary-level contracts)

```typescript
type StageId = string & { __brand: "StageId" };
type EdgeKind = "dependency" | "ordering_only" | "intent_hook";

interface SubgraphSelection {
  readonly targetStageIds: readonly StageId[];
  readonly includeDependencyClosure: true;
  readonly allowPrefixRun: boolean;
}

interface ExecutionPolicy {
  readonly mode: "serial" | "wave_parallel";
  readonly deterministicTieBreak: "stable_stage_id";
  readonly allowOrderingOnlyEdgeReorder: false;
}

interface GraphPassRequest {
  readonly selection: SubgraphSelection;
  readonly policy: ExecutionPolicy;
}

interface GraphPassOutcome {
  readonly executedStages: readonly StageId[];
  readonly skippedStages: readonly StageId[];
  readonly blockedByValidation: boolean;
  readonly commitAllowed: boolean;
}
```

## Pseudocode (subgraph closure and deterministic pass)

```pseudo
function resolveSubgraph(selection, edges):
  assert selection.targetStageIds is not empty
  closure = expandDependencyPredecessors(selection.targetStageIds, edges)
  return stableByStageId(closure)

function runDeterministicPass(graph, request):
  subgraph = resolveSubgraph(request.selection, graph.edges)
  ordered = stableTopologicalSort(subgraph, graph.edges)
  if request.policy.mode == "wave_parallel":
    waves = partitionIndependentWaves(ordered, graph.edges)
    ordered = enforceOrderingOnlyConstraints(waves, graph.edges)
  for stage in ordered:
    result = executeStage(stage)
    if result.validationFailed or result.typedEmpty:
      return GraphPassOutcome(orderedSoFar, remainingStages, true, false)
  return GraphPassOutcome(ordered, [], false, true)
```

## Testable acceptance criteria (AC)

| ID | Given | When | Then |
| --- | --- | --- | --- |
| **AC-P1.2.2-001** | Non-empty target stage set and dependency edges | Subgraph closure resolves | All dependency predecessors are included exactly once in stable stage-id order |
| **AC-P1.2.2-002** | Two independent branches and one ordering-only edge | Wave partition executes | Branches may share a wave but ordering-only relation is still respected deterministically |
| **AC-P1.2.2-003** | Prefix-run flag enabled for early stages | Pass executes | Stages outside selected prefix are explicitly skipped, not implicitly committed |
| **AC-P1.2.2-004** | Stage emits typed-empty output before commit boundary | Pass proceeds | Downstream stages are skipped/propagated per policy and `commitAllowed` is false |
| **AC-P1.2.2-005** | Same graph, seeds, and request policy across reruns | Pass executes twice | Executed stage sequence and skipped-stage sequence are byte-for-byte deterministic |

## Explicit deferrals

| ID | Deferred artifact | Reason |
| --- | --- | --- |
| **DEF-REG-CI** | Registry and CI closure proof for execution graph policy contracts | Reserved for execution roll-up closure artifacts |
| **DEF-GMM-245** | Automated compare-table closure for GMM-2.4.5-* references | Deferred to execution-tail validation bundle |

## Next structural targets

1. Mint tertiary execution mirror **1.2.3** under this folder for stage-family specialization and pipeline role boundaries.
2. Re-run Phase 1 roll-up evidence reconciliation after 1.2.3 and tertiary chain linkage.

## Related

- Conceptual tertiary: [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-2-Graph-Execution-Semantics-and-Subgraph-Runs-Roadmap-2026-03-30-1805]]
- Execution sibling: [[Phase-1-2-1-Node-Taxonomy-Edges-and-Topological-Order-Roadmap-2026-03-30-1705]]
- Execution state: [[../../roadmap-state-execution]] · [[../../workflow_state-execution]]
