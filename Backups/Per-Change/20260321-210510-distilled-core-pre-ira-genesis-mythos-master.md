---
title: Distilled Core — genesis-mythos-master
created: 2026-03-19
tags: [roadmap, distilled-core, genesis-mythos-master]
para-type: Project
project-id: genesis-mythos-master
status: active
core_decisions:
  - "Phase 1.1.8 (lift_write_fence): deterministic quorum restoration + activation_epoch consistency gate write-fence lift; allow outputs emit write_fence_lifted.event and denied outputs emit write_fence_denied.event with deterministic reason codes."
  - "Phase 1.1.9 (deterministic_replay_harness): deterministic replay harness checksum + seed-based determinism test matrix closure; dual-hash reconciliation with fail-closed divergence handling; idempotent dry-run/apply side-effect plan under stable ledger keys."
  - "Phase 1.1.10 (secondary_closure_rollup): boundary→interface→evidence inventory + measurable stage-gate package + advance readiness decision wiring toward advance-phase; rollup handoff_readiness targets ≥93 with delegatable gate criteria."
  - "Phase 2.1 (stage_pipeline_skeleton): Acyclic stage graph from seed envelope through spawn-ready manifests; per-stage immutable outputs, hierarchical RNG streams, single commit barrier for async generation; integrates external ECS/pipeline patterns without relaxing Phase 1 replay/snapshot gates."
  - "Phase 2.1.2 (intent_rng_order): IntentAnnotate attaches only at cycle-safe DAG points; intent and stage RNG namespaces are isolated; optional stage skips cannot desynchronize mandatory streams; splittable/multi-stream PRNG patterns inform runtime without changing ledger hash rules."
  - "Phase 2.1.3 (async_commit_barrier): Async shard work lands in private buffers keyed by barrier_id; coordinator reconciles with stable shard_sequence + semver reconcile_plan_version; only one terminal ManifestEmit publish feeds SpawnCommit; duplicate publish / partial divergence are replay fail-closed events."
  - "Phase 2.1.4 (entity_spawn_manifest): ENTITY_SPAWN consumes DensityLattice + SpawnPolicy; emits EntityManifest sorted by canonical CellCoord/type/row_index; manifest_hash binds lattice_hash + policy_hash + row bytes; Poisson-style placement allowed only under deterministic traversal + isolated RNG streams; SpawnCommit unchanged (terminal publish only)."
  - "Phase 2.1.5 (spawn_commit_apply): SpawnCommit consumes only terminal ManifestEmit + manifest_hash match; row-stable spawn_idempotency_key; double-apply yields ledger-hit; replay harness asserts entity_fingerprint vs golden; fail-closed denied events on precondition breach."
  - "Phase 2.1.7 (p21_secondary_rollup): Authoritative G-P2.1-* closure table with PASS + evidence per row; rollup handoff_readiness 94 gates advance-phase to Phase 2.2 under handoff_gate min_handoff_conf 93; implementation debt on harness vectors does not HOLD closure when contracts are normatively complete."
  - "Phase 2.2.3 (ci_golden_registry): G1–G3/F1–F2 vectors are versioned golden fixtures; CI runs ReplayAndVerify on boundary-touching changes; golden refresh is PR-reviewed only (no auto-update); deterministic_gate_version_id stays aligned with DETERMINISTIC_GATE_V1 unless explicitly bumped."
  - "Phase 2.2.4 (p22_secondary_rollup): G-P2.2-CANON / HARNESS / CI inventory 3/3 PASS (contract/spec) with wiki-linked evidence; G-P2.2-CI PASS labels normative CI policy + goldens in notes, not green CI in repo until fixtures/workflow land; rollup handoff_readiness 94 gates advance-phase for Phase 2.2 macro boundary under handoff_gate min_handoff_conf 93."
  - "Phase 2.3 (world_emergence_seeds): EMG-1..3 emergence metrics extend ReplayAndVerify / golden registry; seed matrix + float/GPU fence before hashing derived emergence state; lore/sim alignment and denial-invariant closure scoped to deterministic bands (field bindings TBD in 2.3.x tertiaries)."
---

# Distilled core — genesis-mythos-master

## Phase 0 anchors

- Master goal: [[Genesis-mythos-master-goal]]
- Roadmap state: [[roadmap-state]]
- Workflow state: [[workflow_state]]
- Decisions log: [[decisions-log]]

## Core decisions (🔵)

_(Append one bullet per phase as the roadmap evolves.)_

- Phase 1.1.8 (lift_write_fence): deterministic quorum restoration + activation_epoch consistency gate write-fence lift; allow outputs emit `write_fence_lifted.event` (reason_code `WRITE_FENCE_LIFTED` or `IDEMPOTENCY_REPLAY`, terminal_state `REACTIVATED`), denied outputs emit `write_fence_denied.event` (reason_code `QUORUM_PROOF_MISSING`, `RECOVERY_NOT_PREPARED`, `EPOCH_MISMATCH`, `HASH_DIVERGENCE`, terminal_state `DEGRADED_READ_ONLY` or `FENCED_RECOVERY`).
- Phase 1.1.9 (deterministic_replay_harness): deterministic replay harness checksum + seed-based determinism test matrix closure; dual-hash reconciliation with fail-closed divergence handling; idempotent dry-run/apply side-effect plan under stable ledger keys.
- Phase 1.1.10 (secondary_closure_rollup): boundary→interface→evidence inventory + measurable stage-gate package + advance readiness decision wiring toward advance-phase; rollup handoff_readiness targets ≥93 with delegatable gate criteria.
- Phase 2.1 (stage_pipeline_skeleton): Directed generation stages with immutable outputs, hierarchical RNG stream policy, deterministic manifest emission order, and replay-safe failure events; defers full intent-parser hook decision to tertiary breakdown.
- Phase 2.1.2 (intent_rng_order): Intent stream vs lattice/policy/manifest streams are namespaced; DAG options A/B/C for `IntentAnnotate` with default flag-off v0; publish `IntentEnvelope` → `AnnotatedIntent` without mutating `ParsedSeed`/`DensityLattice` handles.
- Phase 2.1.3 (async_commit_barrier): Single ledger tail publish for manifest completion under async workers; deterministic reconcile before `manifest_hash`; SpawnCommit gated on terminal `ManifestEmit` record; barrier/race/divergence reason codes align with Phase 1 event taxonomy.
- Phase 2.1.4 (entity_spawn_manifest): `ENTITY_SPAWN` builds sorted `EntityManifest` from `DensityLattice` + versioned `SpawnPolicy`; `manifest_hash` commits lattice + policy + canonical row serialization; placement algorithms (e.g. Poisson-style) must close on sort-key order, not discovery order; links to 2.1.2 streams and 2.1.3 barrier.
- Phase 2.1.5 (spawn_commit_apply): `SpawnCommit` verifies terminal emit + hash, applies rows in manifest sort order, records `spawn_idempotency_key` per row; second pass is no-op ledger-hit; replay harness uses golden **entity_fingerprint**; ECB-style external patterns inform ordering only — ledger is normative.
- Phase 2.1.7 (secondary_closure_rollup): G-P2.1-\* inventory **6/6 PASS** with wiki-linked evidence; rollup note holds **`handoff_readiness: 94`** for **advance-phase** eligibility (Phase 2.1 → 2.2) under `handoff_gate: true` / `min_handoff_conf: 93`; aligns with stage-gate **evidence package** pattern from external PM practice.
- Phase 2.2.3 (ci_golden_registry): Golden vectors from 2.2.2 are mirrored as machine fixtures; CI fails on drift; promotion requires explicit PR + review; volatile fields normalized per stable-subset rules.

## Dependency graph

```mermaid
flowchart TD
  Phase0[Phase0] --> Phase1[Phase1]
  Phase1 --> Phase1_1_7[Phase 1.1.7 Quorum degradation safe mode]
  Phase1 --> Phase1_1_8[Phase 1.1.8 Quorum restoration + deterministic write fence lift]
  Phase1 --> Phase1_1_9[Phase 1.1.9 Deterministic replay harness + Phase 1 gate closure]
  Phase1 --> Phase1_1_10[Phase 1.1.10 Secondary closure + advance readiness]
  Phase1 --> Phase2[Phase2]
  Phase2 --> Phase2_2[Phase 2.2 Intent parser integration (generation hooks)]
  Phase2_2 --> Phase2_2_1[Phase 2.2.1 Intent canonicalization + denial taxonomy]
  Phase2_2_1 --> Phase2_2_2[Phase 2.2.2 IntentPlan consumption boundary + deterministic verification harness]
  Phase2_2_2 --> Phase2_2_3[Phase 2.2.3 CI golden registry + boundary regression gates]
  Phase2_2_3 --> Phase2_2_4[Phase 2.2.4 Secondary closure rollup + advance readiness]
```
