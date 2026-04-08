---
title: Phase 1.1 — Execution layering and interface contracts (Godot lane)
roadmap-level: secondary
phase-number: 1
subphase-index: "1.1"
project-id: godot-genesis-mythos-master
roadmap_track: execution
status: active
priority: high
progress: 34
handoff_readiness: 85
created: 2026-04-10
tags:
  - roadmap
  - execution
  - godot-genesis-mythos-master
  - phase-1
para-type: Project
conceptual_counterpart: "[[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-03-30-0500]]"
links:
  - "[[../Phase-1-Execution-Foundation-and-Core-Architecture-Roadmap-2026-04-10-1315]]"
---

## Phase 1.1 — Execution layering contracts (parallel spine)

Execution mirror for conceptual **1.1** under the required parallel spine path. This slice converts layer boundaries into module-facing interfaces and junior-dev-ready pseudocode seams for the commit pipeline, while keeping `GMM-2.4.5-*` and CI closure explicitly deferred.

## Scope

**In scope:** module boundaries for world/simulation/render/input, Godot-facing interface stubs, commit pipeline seam contracts, acceptance criteria for a first implementation pass, and lane comparand deltas.

**Out of scope:** persistence engines, threaded scheduling, netcode replication, CI/HR proofs, and registry closure artifacts.

## Lane comparand — godot (A) vs sandbox (B)

| Concern | **Lane godot (A)** | **Lane sandbox (B)** |
| --- | --- | --- |
| Boundary packaging | `Scripts/World`, `Scripts/Sim`, `Scripts/Render`, `Scripts/Input` with interface-only cross-layer refs | Flat in-memory modules with same interface names for parity checks |
| Commit seam | `IWorldCommitGateway.Commit(stagedDelta)` returns `CommitResult` and `version_token` | `commit(staged_delta)` returns tuple status/version in harness runtime |
| Event bridge | Godot signal adapters emit post-commit notifications for render refresh | Callback bus emits text trace only |
| Failure handling | Typed reject reason enum mapped to tooling/UI toast hooks | String reason and debug log only |

## Interface contracts (signature-level)

| Interface | Signature sketch | Failure enums / invariants |
| --- | --- | --- |
| `IWorldReadModel` | `GetSnapshot(versionHint: int?) -> WorldSnapshot` | Returns immutable snapshot; `versionHint` mismatch must still return latest stable snapshot. |
| `IWorldCommitGateway` | `Commit(staged: WorldDelta, mode: CommitMode = HardValidate) -> CommitResult` | `CommitResult` has `{ ok: bool, version_token: int, reason: CommitRejectReason }`; only authority path to mutate world state. |
| `ISimulationStepper` | `Step(intents: IntentBatch, view: WorldSnapshot) -> StagedDeltaResult` | Never mutates world directly; emits staged delta or typed rejection. |
| `IRenderViewAdapter` | `Refresh(snapshot: WorldSnapshot, versionToken: int) -> RenderRefreshResult` | Read-only on authoritative state; stale token triggers re-query not mutation. |
| `IIntentIngress` | `Normalize(raw: RawIntentEnvelope) -> IntentBatch` | Must include authorization and source metadata; invalid envelope returns `IntentRejectReason`. |

**Commit reject enum sketch:** `CommitRejectReason = { shape_invalid, hard_invariant, authorization_failed, stale_version, dependency_missing, unknown }`.

## Pseudocode for commit pipeline seams

```pseudo
func run_tick(intents):
  staged = simulation.step(intents, world.read_model())
  if staged.invalid_shape:
    return reject("shape_invalid")

  commit = world.commit_gateway().commit(staged)
  if not commit.ok:
    simulation.rollback_ephemeral(commit.reason)
    return reject(commit.reason)

  render.refresh(world.read_model(), commit.version_token)
  return ok(commit.version_token)
```

## Acceptance criteria

1. **AC-1:** Boundary modules are declared and reference only interface contracts across layers.
2. **AC-2:** One commit seam (`IWorldCommitGateway`) is the exclusive authoritative mutation path.
3. **AC-3:** Pseudocode maps directly to at least one concrete stub per layer (`world`, `simulation`, `render`, `input`).
4. **AC-4:** Godot/sandbox comparand rows are present on this secondary and carried forward to execution tertiaries.

## Roll-up gates (execution_v1)

| Gate | Pass criteria | Evidence artifact | Owner |
| --- | --- | --- | --- |
| `G-1.1-Commit-Seam` | `IWorldCommitGateway` signature + reject enum documented and used by pseudocode path | This note + next tertiary signature matrix | lane godot implementation owner |
| `G-1.1-Boundary-Isolation` | No cross-layer concrete type dependency in boundary map | module-boundary table in tertiary `1.1.1` | architecture reviewer |
| `G-1.1-Comparand-Parity` | Godot/sandbox comparand rows remain aligned for boundary + failure handling | secondary + tertiary comparand blocks | lane A/B maintainer |
| `G-1.1-Risk-Baseline` | Risk register v0 present with mitigations and fallback owners | risk table below | roadmap maintainer |

## Risk register v0 (Phase 1.1)

| Risk | Trigger | Mitigation | Owner | Fallback | Gate impact |
| --- | --- | --- | --- | --- | --- |
| Commit seam drift from interfaces | Tertiary draft adds direct world mutation path | Enforce `IWorldCommitGateway` as single mutation seam in review checklist | lane godot implementation owner | Block merge of tertiary until seam is restored | Blocks `G-1.1-Commit-Seam` |
| Boundary leakage between layers | Cross-layer imports appear in module mapping | Boundary matrix review before tertiary acceptance | architecture reviewer | Move offending calls behind adapter and re-run review | Blocks `G-1.1-Boundary-Isolation` |
| Comparand divergence | Godot/sandbox rows no longer match behavior claims | Maintain parity checklist per slice | lane A/B maintainer | Mark mismatch and gate tertiary readiness | Blocks `G-1.1-Comparand-Parity` |

## Deferred (explicit)

- `GMM-2.4.5-*` registry closure: deferred to later execution phases, but gated prep is now tracked by `G-1.1-*` roll-up gates above.
- CI and HR rollup proofs: deferred and non-blocking for this structural mirror mint; attach once execution tertiaries are merged.

## Next structural execution target

- **1.1.1** — execution tertiary for layer-boundary commit ordering, failure propagation edge cases, and stricter API signature sketching.

## 1.1 roll-up hardening from 1.1.1 evidence

| Roll-up anchor | Evidence source | Current verdict | Remaining work |
| --- | --- | --- | --- |
| `rollup_1_1_from_1_1_1` | [[Phase-1-1-1-Execution-Layer-Boundary-and-Commit-Pipeline-Roadmap-2026-04-10-1316]] sections: boundary matrix, comparand parity, failure pseudocode | in-progress | Add explicit pass/fail statement for each `G-1.1-*` gate in this 1.1 note after implementation owner review. |
| `rollup_1_primary_from_1_1` | This secondary gate register + phase-1 primary note gate table | open | Promote to in-progress only after `rollup_1_1_from_1_1_1` is closed with evidence links. |
