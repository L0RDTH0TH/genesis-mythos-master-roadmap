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
  - "Phase 2.3 (world_emergence_seeds): EMG-1..3 extend ReplayAndVerify / golden registry; EMG-2 normative contract (RFC 6901 pointers for lore flags + sim counters, AlignmentFn_v0 → AlignmentOutcome, provisional floor F) in [[phase-2-3-2-emg-2-floor-frozen-json-pointers-and-alignmentfn-v0-roadmap-2026-03-21-2245]]; CI registry wiring + `fixtures/emg2_alignment/v0/` schema + WA matrix in [[phase-2-3-3-emg-2-ci-golden-registry-row-and-fixture-hardening-roadmap-2026-03-21-2249]] (dual **normative** vs **execution** readiness per D-026); **execution-closure tranche** (fixtures PR + workflow/CODEOWNERS + WA log + wiki row + freeze) in [[phase-2-3-4-emg-2-execution-closure-vcs-promotion-and-floor-freeze-roadmap-2026-03-21-2339]] per **D-028**; wiki G-EMG2 row + fixture-frozen F still open until VCS merge; EMG-1/EMG-3 + PBT alphabet in [[phase-2-3-1-emg-normative-schema-bindings-and-seed-matrix-v0-roadmap-2026-03-21-2205]]."
  - "Phase 3.1 (simulation_tick_scheduler): Secondary spine for deterministic ticks vs Phase 2 barrier / registry; **rollup HR 93** on **3.1.7** (**D-038**) for **advance-phase** **3.1→3.2**; composite **EHR 68** until goldens — [[phase-3-1-simulation-tick-scheduler-and-time-quanta-roadmap-2026-03-21-2346]]."
  - "Phase 3.1.1 (tick_epoch_preimage): Tertiary contract for `tick_epoch`, `TickCommitRecord_v0`, preimage allow-list, float-free preimage policy, replay log v0 schema + stub row, desync taxonomy — normative HR 93 / execution HR 72 until repo golden — [[phase-3-1-1-deterministic-tick-epoch-and-hash-preimage-boundaries-roadmap-2026-03-22-0015]]."
  - "Phase 3.1.2 (catchup_fairness): `CatchUpPolicy_v0` (max steps, clamp, slow/drop/coalesce), sub-step visibility optional, `WithinTickWorkOrder_v0` vs 2.1.2 RNG namespaces — normative HR 93 / execution HR 74 until policy bits in golden replay — [[phase-3-1-2-deterministic-catch-up-caps-multirate-fairness-roadmap-2026-03-22-0016]]."
  - "Phase 3.1.3 (pause_time_scale): `SimulationRunControl_v0` draft — pause = no `tick_epoch` advance; time-scale serialized or session-fixed; input latch + replay header coupling vs D-031 — normative HR **91** / execution HR 72 until control bits in golden — [[phase-3-1-3-deterministic-pause-time-scale-sim-clock-coupling-roadmap-2026-03-22-0022]]; **D-032** / **D-033**."
  - "Phase 3.1.4 (agency_slices): `AgencySliceSchedule_v0` — ordered slices per `tick_epoch`, tie-break + starvation credits, RNG order after schedule vs **2.1.2** — normative HR **92** / execution HR **71** until replay sequence in golden — [[phase-3-1-4-deterministic-agency-tick-slices-starvation-guards-roadmap-2026-03-22-0030]]; **D-034**."
  - "Phase 3.1.5 (slice_apply_ledger): `MutationIntent_v0` + `AgencySliceApplyLedger_v0` — ordered mutation stream per `tick_epoch` from **3.1.4** schedule, idempotent `mutation_id`, last-writer / conflict policy, catch-up + pause coupling — normative HR **91** / execution HR **70** until merge matrix + golden checksum — [[phase-3-1-5-deterministic-agency-slice-outcomes-mutation-ledger-replay-roadmap-2026-03-22-0045]]; **D-035** / **D-036**."
  - "Phase 3.1.6 (observable_bundle): `SimObservableBundleTelemetry_v0` + post-apply observable barrier — `post_apply_observable_root` / `apply_ledger_checksum` bridge to **3.1.1** `TickCommitRecord_v0`, facet manifest + serialization profile TBD — normative HR **92** / execution HR **69** — [[phase-3-1-6-tick-scoped-observable-bundle-post-apply-replay-bridge-roadmap-2026-03-22-0047]]; **D-037**."
  - "Phase 3.1.7 (p31_secondary_rollup): **G-P3.1-*** **6/6 PASS** vault-normative inventory; rollup **HR 93** gates **advance-phase** **3.1→3.2** under `min_handoff_conf` **93**; composite **EHR 68** until goldens — [[phase-3-1-7-phase-3-1-secondary-closure-rollup-and-advance-readiness-roadmap-2026-03-22-0122]]; **D-038**."
  - "Phase 3.2.1 (dm_override_regen_taxonomy): `DmOverrideIntent_v0` vs `RegenRequest_v0`, regen gate versioning, fail-closed codes vs **2.2.1**/**2.2.2** — normative HR **92** / execution HR **64** until goldens + registry reconcile — [[phase-3-2-1-dm-override-intent-envelope-and-regeneration-gate-taxonomy-roadmap-2026-03-22-0210]]; **D-041**."
  - "Phase 3.2.2 (regen_preconditions_ordering): `RegenRequest_v0` P1–P6 table, **regen-before-merge** vs **StableMergeKey_v0**, **2.2.2** boundary + regen ledger idempotency sketch — normative HR **92** / execution HR **63** until goldens — [[phase-3-2-2-regen-request-preconditions-and-gated-subgraph-contract-roadmap-2026-03-22-1735]]; **D-042**."
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
- Phase 2.3 (world_emergence_seeds): EMG-1 replay hash + EMG-3 denial closure sketches in 2.3.1; **EMG-2** frozen JSON Pointers (`/lore/flags`, `/sim/counters`), `AlignmentFn_v0`, provisional **F=85** in [[phase-2-3-2-emg-2-floor-frozen-json-pointers-and-alignmentfn-v0-roadmap-2026-03-21-2245]]; **2.3.3** wires `fixtures/emg2_alignment/v0/`, registry row schema, and WA matrix toward CI; **2.3.4** (D-028) sequences the single-tranche PR that materializes wiki **G-EMG2-*** + WA log closure + `AlignAndVerify` green — wiki row in 2.2.3 still pending until that merge (see `handoff_gaps`).
- Phase 3.1 (simulation_tick_scheduler): Deterministic tick spine aligned to **2.1.3** barrier ordering; **3.1.7** rollup (**D-038**) holds **G-P3.1-*** closure + **HR 93** vs **EHR 68** split (**D-039**).
- Phase 3.1.1 (tick_epoch_preimage): `TickCommitRecord_v0`, float-free preimage, replay log v0 + stub row, desync codes — **D-030** covers synthesis §6–7 deferral.
- Phase 3.1.2 (catchup_fairness): catch-up caps, clamp, fairness ordering — **D-031** pins replay-live parity obligation for policy enum.
- Phase 3.1.3 (pause_time_scale): pause + dilation + replay header — **D-032** draft; execution closure waits golden control encoding.
- Phase 3.1.4 (agency_slices): per-`tick_epoch` agency slice order, tie-break, starvation — **D-034** draft; execution closure waits slice sequence in replay row + **D-032** header.
- Phase 3.1.5 (slice_apply_ledger): ordered mutation intents + idempotent apply + conflict codes — **D-035** draft; checklist items **deferred** per **D-036** until header/`replay_row_version`/merge policy unblock.
- Phase 3.1.6 (observable_bundle): post-apply observable barrier + telemetry v0 + tick commit bridge — **D-037** draft; `serialization_profile_id` + golden observable **TBD**.
- Phase 3.1.7 (p31_secondary_rollup): **G-P3.1-*** closure table + advance readiness — **D-038**; rollup **HR 93** vs composite **EHR 68** until repo goldens.
- Phase 3.2.1 (dm_override_regen_taxonomy): DM override envelope + regen subgraph gates + denial codes — **D-041** draft; merge ordering + golden rows **TBD**.
- Phase 3.2.2 (regen_preconditions_ordering): Regen precondition table + **regen-before-merge** policy + **2.2.2** coupling — **D-042** draft; golden vectors **TBD**.

## Dependency graph

```mermaid
flowchart TD
  Phase0[Phase0] --> Phase1[Phase1]
  Phase1 --> Phase1_1_7[Phase 1.1.7 Quorum degradation safe mode]
  Phase1 --> Phase1_1_8[Phase 1.1.8 Quorum restoration + deterministic write fence lift]
  Phase1 --> Phase1_1_9[Phase 1.1.9 Deterministic replay harness + Phase 1 gate closure]
  Phase1 --> Phase1_1_10[Phase 1.1.10 Secondary closure + advance readiness]
  Phase1 --> Phase2[Phase2]
  Phase2 --> Phase2_1_3[Phase 2.1.3 Async commit barrier]
  Phase2 --> Phase2_2[Phase 2.2 Intent parser integration (generation hooks)]
  Phase2_2 --> Phase2_2_1[Phase 2.2.1 Intent canonicalization + denial taxonomy]
  Phase2_2_1 --> Phase2_2_2[Phase 2.2.2 IntentPlan consumption boundary + deterministic verification harness]
  Phase2_2_2 --> Phase2_2_3[Phase 2.2.3 CI golden registry + boundary regression gates]
  Phase2_2_3 --> Phase2_2_4[Phase 2.2.4 Secondary closure rollup + advance readiness]
  Phase2_2_4 --> Phase2_3[Phase 2.3 World emergence + test seeds validation]
  Phase2_1_3 -.-> Phase3_1[Phase 3.1 Sim tick scheduler]
  Phase2_3 --> Phase3[Phase 3 Living simulation + agency]
  Phase3 --> Phase3_1
  Phase2_2_4 --> Phase3
  Phase2_3 --> Phase3
  Phase2_3_4[Phase 2.3.4 EMG-2 execution closure] -.-> Phase3
```
