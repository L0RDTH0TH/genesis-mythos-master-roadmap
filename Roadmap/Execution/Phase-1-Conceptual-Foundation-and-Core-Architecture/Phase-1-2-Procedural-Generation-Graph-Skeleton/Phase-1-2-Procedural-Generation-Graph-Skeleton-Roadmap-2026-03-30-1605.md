---
title: Phase 1.2 - Execution (Procedural generation graph skeleton)
roadmap-level: secondary
roadmap_track: execution
conceptual_counterpart: "[[1-Projects/sandbox-genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-03-30-1605]]"
phase-number: 1
subphase-index: "1.2"
project-id: sandbox-genesis-mythos-master
status: in-progress
handoff_readiness: 86
progress: 48
created: 2026-04-07
tags:
  - roadmap
  - execution
  - sandbox-genesis-mythos-master
  - phase-1
para-type: Project
links:
  - "[[../Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-03-30-0430]]"
  - "[[../../roadmap-state-execution]]"
---

## Phase 1.2 - Execution mirror (procedural generation graph skeleton)

> **Authority:** This secondary execution mirror translates conceptual 1.2 into implementation-ready graph contracts (typed stage interfaces, deterministic ordering pseudocode, and testable AC rows). Deferred execution closure artifacts remain explicit: **DEF-REG-CI** and **DEF-GMM-245**.

## Execution scope

| In scope | Deferred on this slice |
| --- | --- |
| Deterministic DAG-oriented stage graph for generation | Registry and CI closure artifacts (DEF-REG-CI) |
| Named intent injection hooks before/after selected stages | GMM-2.4.5-* compare automation (DEF-GMM-245) |
| Typed stage IO contracts and ordered graph execution semantics | Performance/soak benchmarks and plugin ABI wiring |
| Graph-level dry-run behavior with no authoritative commits | Cross-session replay certification artifacts |

## Typed interfaces (secondary-level normative)

```typescript
type StageId = string & { __brand: "StageId" };
type HookId = string & { __brand: "HookId" };
type WorldVersion = number & { __brand: "WorldVersion" };

interface StageInput {
  readonly worldVersion: WorldVersion;
  readonly seedBundle: Readonly<Record<string, unknown>>;
  readonly upstream: Readonly<Record<string, unknown>>;
}

interface StageOutput {
  readonly stageId: StageId;
  readonly stagedDelta: ReadonlyArray<unknown>;
  readonly emittedFacts: Readonly<Record<string, unknown>>;
}

interface GenerationStage {
  readonly id: StageId;
  readonly dependsOn: readonly StageId[];
  run(input: StageInput): Result<StageOutput, StageFailure>;
}

interface IntentHook {
  readonly id: HookId;
  readonly attachTo: StageId;
  apply(input: StageInput): StageInput;
}
```

## Pseudocode (ordered graph execution)

```pseudo
function runGenerationGraph(graph, hooks, baseInput):
  ordered = topoSort(graph)
  ctx = baseInput
  staged = []
  for stage in ordered:
    ctx = applyHooks(hooks.before(stage.id), ctx)
    result = stage.run(ctx)
    if !result.ok:
      return reject(result.error)
    staged.push(result.value.stagedDelta)
    ctx = mergeOutputs(ctx, result.value.emittedFacts)
    ctx = applyHooks(hooks.after(stage.id), ctx)
  return accept(staged)
```

## Testable acceptance criteria (AC)

| ID | Given | When | Then |
| --- | --- | --- | --- |
| **AC-P1.2-001** | Graph with explicit dependencies | `topoSort` executes | Every stage executes after all declared dependencies |
| **AC-P1.2-002** | Hook mapped to stage pre-run | Stage executes | Hook-adjusted input is used for stage run |
| **AC-P1.2-003** | One stage returns failure | Graph run continues | Run stops immediately; no authoritative commit occurs |
| **AC-P1.2-004** | Dry-run mode enabled | Graph completes | Staged outputs produced without world-state commit side effects |
| **AC-P1.2-005** | Same seed bundle and graph | Run executed twice | Ordered stage list and staged output signatures remain deterministic |

## Explicit deferrals

| ID | Deferred artifact | Reason |
| --- | --- | --- |
| **DEF-REG-CI** | Stage registry + CI closure proof | Reserved for execution roll-up pass after 1.2 tertiaries |
| **DEF-GMM-245** | GMM-2.4.5-* compare-table automation | Deferred to execution-tail validation bundle |

## Next structural targets

1. Tertiary execution mirrors **1.2.1-1.2.3** are now minted under this folder; keep link parity and role-boundary contracts synchronized.
2. Re-run Phase 1 roll-up evidence gating and attestation now that the 1.2 tertiary chain is complete.

## Related

- Conceptual secondary: [[1-Projects/sandbox-genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-03-30-1605]]
- Execution primary: [[../Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-03-30-0430]]
- Execution state: [[../../roadmap-state-execution]] · [[../../workflow_state-execution]]
