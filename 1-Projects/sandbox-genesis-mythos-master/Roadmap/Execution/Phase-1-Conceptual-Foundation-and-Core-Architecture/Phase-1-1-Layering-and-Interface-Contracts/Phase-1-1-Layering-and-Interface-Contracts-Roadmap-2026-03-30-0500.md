---
title: Phase 1.1 — Execution (Layering and Interface Contracts)
roadmap-level: secondary
roadmap_track: execution
conceptual_counterpart: "[[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-03-30-0500]]"
phase-number: 1
subphase-index: "1.1"
project-id: sandbox-genesis-mythos-master
status: in-progress
handoff_readiness: 85
progress: 45
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

## Phase 1.1 — Execution mirror (layering and interface contracts)

> **Authority:** This note mirrors conceptual **1.1** and converts it into implementation-ready seams: typed interfaces, pseudocode flow, and testable AC tables. Execution closure artifacts (**registry/CI** and **GMM-2.4.5-\*** compare proof) remain explicitly deferred on this pass per [[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]].

## Execution scope

| In scope | Deferred on this slice |
| --- | --- |
| Four-layer contract boundaries (world, simulation, render, input) | Registry + CI closure rows |
| Single committer path for authoritative writes | GMM-2.4.5-* automated compare tables |
| Injection-stage contract for generation handoff into runtime | Plugin ABI / cross-thread runtime wiring |
| AC matrix for pass/fail invariants at the 1.1 seam | Soak/perf certification |

## Typed interfaces (secondary-level normative)

```typescript
type TickId = string & { __brand: "TickId" };
type LayerName = "input" | "simulation" | "world_state" | "render";

interface IntentEnvelope {
  readonly tickId: TickId;
  readonly source: "dm" | "player" | "system";
  readonly payload: unknown;
}

interface SimulationStage {
  evaluate(intents: readonly IntentEnvelope[], world: WorldSnapshot): StagedDelta;
}

interface WorldCommitGateway {
  /** The only authoritative write seam for 1.1. */
  commit(delta: StagedDelta, policy: CommitPolicy): Result<CommitReceipt, CommitError>;
}

interface RenderReadModel {
  read(version: WorldVersion): ViewModel;
}
```

## Pseudocode (ordered execution seam)

```pseudo
function frameCycle(rawInput, worldVersion):
  intents = input.normalize(rawInput)
  staged = simulation.evaluate(intents, world.read(worldVersion))
  commit = worldGateway.commit(staged, policy=single_committer)
  if !commit.ok:
    simulation.clearEphemeral(staged)
    return reject(commit.error)
  view = render.read(commit.value.version)
  return present(view)
```

## Testable acceptance criteria (AC)

| ID | Given | When | Then |
| --- | --- | --- | --- |
| **AC-P1.1-001** | Mixed DM/player intents in same tick | `simulation.evaluate` runs | Produces one deterministic `StagedDelta` ordering; no direct world writes |
| **AC-P1.1-002** | Valid staged delta | `worldGateway.commit` called | Exactly one authoritative commit receipt with incremented world version |
| **AC-P1.1-003** | Invalid transition in staged delta | commit invoked | Entire batch rejected; world version unchanged |
| **AC-P1.1-004** | Render polls after commit | `render.read` executes | View model reflects post-commit snapshot only |
| **AC-P1.1-005** | Generation injection is configured | pre-sim stage executes | Injection output enters via named seam, not via render loop side effect |

## Deferrals (explicit)

| ID | Deferred artifact | Reason |
| --- | --- | --- |
| **DEF-REG-CI** | Registry and CI closure records | Execution QA pass after 1.1/1.2 mirrors stabilize |
| **DEF-GMM-245** | GMM-2.4.5-* compare-table automation | Remains execution-tail evidence, not this structural mint |

## Next structural targets

1. Tertiary **1.1.1** mirror minted: [[Phase-1-1-1-Layer-Boundary-and-Commit-Pipeline-Roadmap-2026-03-30-0431]].
2. Keep sibling secondary **1.2** mint pending under parallel spine, then return for primary Phase 1 roll-up gate review.

## Related

- Conceptual secondary: [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-03-30-0500]]
- Execution primary: [[../Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-03-30-0430]]
- Execution state: [[../../roadmap-state-execution]] · [[../../workflow_state-execution]]

> [!note] State sync authority
> This mirror is minted and valid for execution seam work. Routing authority for the next structural target stays in [[../../roadmap-state-execution]] and [[../../workflow_state-execution]] (current next: tertiary **1.1.1**).
