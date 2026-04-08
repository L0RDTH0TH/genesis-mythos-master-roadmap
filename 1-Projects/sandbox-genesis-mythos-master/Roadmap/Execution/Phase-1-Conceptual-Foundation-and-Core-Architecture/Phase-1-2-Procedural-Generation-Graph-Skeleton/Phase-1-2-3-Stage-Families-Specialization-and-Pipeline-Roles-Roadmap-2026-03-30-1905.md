---
title: Phase 1.2.3 - Execution (Stage families specialization and pipeline roles)
roadmap-level: tertiary
roadmap_track: execution
conceptual_counterpart: "[[1-Projects/sandbox-genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-3-Stage-Families-Specialization-and-Pipeline-Roles-Roadmap-2026-03-30-1905]]"
phase-number: 1
subphase-index: "1.2.3"
project-id: sandbox-genesis-mythos-master
status: in-progress
handoff_readiness: 89
progress: 64
created: 2026-04-08
tags:
  - roadmap
  - execution
  - sandbox-genesis-mythos-master
  - phase-1
para-type: Project
links:
  - "[[Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-03-30-1605]]"
  - "[[Phase-1-2-2-Graph-Execution-Semantics-and-Subgraph-Runs-Roadmap-2026-03-30-1805]]"
  - "[[Phase-1-2-1-Node-Taxonomy-Edges-and-Topological-Order-Roadmap-2026-03-30-1705]]"
  - "[[../../roadmap-state-execution]]"
---

## Phase 1.2.3 - Execution mirror (stage families specialization and pipeline roles)

> **Authority:** This tertiary execution mirror converts conceptual 1.2.3 into implementation-ready stage-family contracts and role boundaries (typed family/role interfaces, deterministic role-order pseudocode, and testable AC rows). Explicit deferrals remain visible: **DEF-REG-CI** and **DEF-GMM-245**.

## Execution scope

| In scope | Deferred on this slice |
| --- | --- |
| Stage-family taxonomy (`structure`, `entities`, `glue`, `commit`) with one primary family per stage | Registry + CI closure artifacts for role declarations (DEF-REG-CI) |
| Deterministic family transition constraints across graph passes | GMM-2.4.5-* compare-table automation (DEF-GMM-245) |
| Typed specialization tags and role-boundary contracts | Runtime plugin ABI checks for family-role registration |
| Family-aware acceptance checks at commit boundaries | Long-run drift benchmarks for role rebalance heuristics |

## Typed interfaces (tertiary-level contracts)

```typescript
type StageId = string & { __brand: "StageId" };
type StageFamily = "structure" | "entities" | "glue" | "commit";
type RoleTag = string & { __brand: "RoleTag" };

interface StageRoleSpec {
  readonly stageId: StageId;
  readonly primaryFamily: StageFamily;
  readonly specialization: readonly RoleTag[];
  readonly secondaryRoles: readonly RoleTag[];
}

interface FamilyTransitionRule {
  readonly from: StageFamily;
  readonly to: StageFamily;
  readonly allowed: boolean;
  readonly rationale: string;
}

interface RoleValidationResult {
  readonly duplicatePrimaryFamily: boolean;
  readonly disallowedTransitionEdges: readonly StageId[];
  readonly commitBoundaryViolations: readonly StageId[];
}
```

## Pseudocode (family-role validation and ordered execution)

```pseudo
function validateRoleSpecs(stageSpecs):
  for spec in stageSpecs:
    assert spec.primaryFamily in {"structure","entities","glue","commit"}
  assert noStageHasMultiplePrimaryFamilies(stageSpecs)

function enforceFamilyTransitions(orderedStages, stageSpecs, transitionRules):
  for (a, b) in consecutivePairs(orderedStages):
    familyA = stageSpecs[a].primaryFamily
    familyB = stageSpecs[b].primaryFamily
    rule = lookupRule(transitionRules, familyA, familyB)
    if rule exists and !rule.allowed:
      return rejectTransition(a, b, rule.rationale)
  return ok

function runFamilyAwarePass(graph, stageSpecs, transitionRules):
  validateRoleSpecs(stageSpecs)
  ordered = stableTopologicalSort(graph)
  enforceFamilyTransitions(ordered, stageSpecs, transitionRules)
  return executeOrderedPass(ordered)
```

## Testable acceptance criteria (AC)

| ID | Given | When | Then |
| --- | --- | --- | --- |
| **AC-P1.2.3-001** | Stage-role spec set for all nodes | Validation runs | Every stage has exactly one `primaryFamily` |
| **AC-P1.2.3-002** | `entities` stage depends on unresolved `structure` output | Ordered pass resolves | `entities` stage cannot execute before required `structure` producers |
| **AC-P1.2.3-003** | `glue` stage attempts to bypass `commit` boundary | Family transitions checked | Transition is rejected with explicit rationale |
| **AC-P1.2.3-004** | Stage has valid primary family and specialization tags | Validation runs | Spec is accepted without changing topological ordering semantics |
| **AC-P1.2.3-005** | Same graph + role specs + transition rules | Pass runs twice | Role-validation and final execution order remain deterministic |

## Explicit deferrals

| ID | Deferred artifact | Reason |
| --- | --- | --- |
| **DEF-REG-CI** | Registry and CI closure proof for stage-family role declarations | Deferred to execution roll-up closure pass |
| **DEF-GMM-245** | Automated compare-table closure for role-boundary assertions | Deferred to execution-tail validation bundle |

## Next structural targets

1. Run execution roll-up reconciliation for Phase 1.2 chain closure (`1.2.1` -> `1.2.3`) and update gate language in `roadmap-state-execution`.
2. Keep DEF evidence explicit until roll-up closure artifacts are attached and validated.

## Related

- Conceptual tertiary: [[1-Projects/sandbox-genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-3-Stage-Families-Specialization-and-Pipeline-Roles-Roadmap-2026-03-30-1905]]
- Execution sibling: [[Phase-1-2-2-Graph-Execution-Semantics-and-Subgraph-Runs-Roadmap-2026-03-30-1805]]
- Execution state: [[../../roadmap-state-execution]] · [[../../workflow_state-execution]]
