---
title: Phase 1 — Execution (Foundation & Core Architecture)
roadmap-level: primary
roadmap_track: execution
conceptual_counterpart: "[[../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-03-30-0430]]"
phase-number: 1
subphase-index: "1"
project-id: sandbox-genesis-mythos-master
status: in-progress
handoff_readiness: 86
handoff_gaps:
  - "Primary roll-up closure remains open until tertiary 1.2.1 is minted and audited."
progress: 40
created: 2026-04-10
tags:
  - roadmap
  - execution
  - sandbox-genesis-mythos-master
para-type: Project
links:
  - "[[../../sandbox-genesis-mythos-master-Roadmap-2026-03-30-0430]]"
  - "[[../roadmap-state-execution]]"
---

## Phase 1 — Execution mirror (parallel spine)

> **Authority:** This note is the **execution-track** counterpart to the conceptual Phase 1 primary. It translates NL design authority into **typed interfaces**, **implementation-shaped pseudocode**, and **testable acceptance criteria**. Registry/CI closure, binary artifact hashes, and **GMM-2.4.5-*** proof rows remain **explicitly deferred** per [[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]].

### Scope (execution)

| In scope | Out of scope (defer) |
| --- | --- |
| Layer graph types + commit seam contracts | Production CI wiring / registry HR closure |
| Dry-run vs live execution discriminant | **GMM-2.4.5-*** compare-table automation |
| AC tables + negative tests for invariants | Performance budgets / soak tests |

## Typed interfaces (normative sketches)

```typescript
/** Opaque handle — concrete snapshot format is execution-deferred. */
type WorldSnapshotHandle = string & { __brand: "WorldSnapshotHandle" };

interface CommitPipeline {
  /** Single commit boundary per conceptual 1.1.1 seam. */
  commitWorld(next: WorldStateV1, evidence: CommitEvidence): Result<void, CommitRejection>;
}

interface WorldStateV1 {
  readonly schemaVersion: SemVer;
  readonly seedBundleId: string;
  readonly graphDefinitionVersion: string;
}

type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };
```

## Pseudocode — dry-run vs live path

```pseudo
function executePipeline(mode: RunMode, graph: GraphDef, world: WorldStateV1):
  validateStatic(graph)                      // pre-run gate (1.2.5 class)
  if mode == DryRun:
    manifest ← planMutations(graph, world)   // no world commit
    return DryRunResult(manifest)
  else:
    snapshot ← captureSnapshot(world)        // abort if snapshot fails (Glue invariants)
    newWorld ← runStages(graph, world)
    commitPipeline.commitWorld(newWorld, evidenceFrom(snapshot, graph))
```

## Testable acceptance criteria (AC)

| ID | Given | When | Then |
| --- | --- | --- | --- |
| **AC-P1-001** | Valid `GraphDef` | `validateStatic` | Returns ok; invalid graph rejected before any stage execution |
| **AC-P1-002** | `DryRun` mode | pipeline completes | No `WorldState` mutation; manifest non-empty iff graph would mutate |
| **AC-P1-003** | Destructive path | snapshot fails | Pipeline aborts before commit; prior world unchanged |
| **AC-P1-004** | Conflicting DM/player merge | dry-run | Surfaces `PolicyConflict` — no silent merge (**GMM-EXEC-TBD-001** deferred) |

## Explicit deferrals (stable IDs)

| ID | Deferred artifact | Track |
| --- | --- | --- |
| **DEF-REG-CI** | Registry + CI proof closure | Execution (post–vertical slice) |
| **DEF-GMM-245** | **GMM-2.4.5-*** automated compare tables | Execution (reference-only on conceptual) |

## Handoff-audit evidence (2026-04-07)

- DEF roll-up closure evidence note (registry/CI): [[../../../../3-Resources/Second-Brain/Validator-Reports/roadmap_handoff_auto/sandbox-phase1-rollup-registry-ci]]
- DEF roll-up closure evidence note (GMM-2.4.5): [[../../../../3-Resources/Second-Brain/Validator-Reports/roadmap_handoff_auto/sandbox-phase1-rollup-gmm245]]
- Phase 1 primary roll-up status remains advisory-open until execution tertiary `1.2.1` is minted and a closure handoff-audit run records final gate closure.

## Next execution slices (mirror order)

1. **1.1** — [[../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-03-30-0500]] → mint under `Roadmap/Execution/.../Phase-1-1-.../` on next deepen.
2. **1.2** — graph skeleton mirror — same parallel-spine rule.

## Related

- Conceptual primary: [[../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-03-30-0430]]
- Execution state: [[../roadmap-state-execution]] · [[../workflow_state-execution]]
