---
title: Phase 1.1.9 - Deterministic Replay Harness and Phase 1 Gate Closure
roadmap-level: tertiary
phase-number: 1
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-19
tags: [roadmap, genesis-mythos-master, phase]
para-type: Project
subphase-index: "1.1.9"
handoff_readiness: 85
handoff_gaps: []
links:
  - "[[phase-1-1-core-architecture-contracts-roadmap-2026-03-19-0001]]"
  - "[[phase-1-1-8-quorum-restoration-and-deterministic-write-fence-lift-roadmap-2026-03-19-1726]]"
---

## Phase 1.1.9 - Deterministic Replay Harness and Phase 1 Gate Closure

Define a deterministic replay harness that computes a canonical inputs checksum, executes seed-based replays, and reconciles end-state using dual-hash comparison (`state_hash` + `metadata_hash`) with a fail-closed policy. This closes Phase 1 gating so later phases can safely depend on replay determinism as an architecture invariant.

### Delegatable task decomposition (v1)

1. T1 - Define harness interface + deterministic checksum scope
   - Owner/sequence: Junior-dev implements this before any test/verification work.
   - Inputs: the `IDeterministicReplayHarness` interface (already present) and the `seed_set`, `replay_slice`, `ordered_identity_sequence` definitions.
   - Outputs: (a) the harness interface signature (must remain consistent), (b) explicit checksum-scope bullet list under `## Canonical inputs checksum (scope)`.
   - Completion signal: `## Canonical inputs checksum (scope)` contains all of: `seed_set`, `replay_slice (from_tick/to_tick bounds)`, `ordered_identity_sequence`, and deterministic gate/version identifiers.

2. T2 - Specify canonical ordering key + evaluation determinism ban
   - Owner/sequence: Junior-dev implements this immediately after T1 and before test fixtures.
   - Inputs: the ordering constraint already described in `## Replay slice ordering invariant (v1)`.
   - Outputs: (a) a single canonical ordering tuple definition, (b) an explicit "no unordered iteration" rule.
   - Completion signal: `## Replay slice ordering invariant (v1)` includes a concrete `ordering_key = (stream_id, replay_tick, ordering_index, event_id)` and a deterministic `event_id` derivation formula.

3. T3 - Define idempotent dry-run/apply contract + ledger key tuple
   - Owner/sequence: Junior-dev implements this after T2.
   - Inputs: the dry-run vs apply split described in `## Idempotent dry-run/apply side-effect plan (v1)`.
   - Outputs: (a) the stable ledger key tuple format, (b) explicit dry-run purity requirement, (c) explicit apply gating condition.
   - Completion signal: `## Idempotent dry-run/apply side-effect plan (v1)` includes a ledger key recommendation tuple and states that apply is gated on ledger-key absence.

4. T4 - Build executable seed-based determinism matrix (>=3 seeds, >=3 replays/seed)
   - Owner/sequence: Junior-dev implements this after T3.
   - Inputs: seed set definition, replay slice bounds, ordered identity sequence, and deterministic gate identifiers.
   - Outputs: (a) concrete fixture values, (b) explicit expected pass conditions for determinism.
   - Completion signal: `## Verification and test matrix closure (executable assertions, v1)` contains a concrete executable fixture block defining seeds A/B/C, slice bounds, and the ordering tuple.

5. T5 - Specify drift test + fail-closed divergence evidence traces
   - Owner/sequence: Junior-dev implements this immediately after T4.
   - Inputs: a controlled input perturbation definition (deterministic gate/version identifier change) and the dual-hash reconciliation policy.
   - Outputs: (a) expected deny reason code on mismatch, (b) evidence fields to capture, (c) fail-closed rule that prevents apply.
   - Completion signal: the verification block defines the drift scenario, states mismatch triggers denial, and lists exact evidence fields (inputs_hash + both dual hashes + ordering tuple evidence).

## Deterministic replay harness (v1)

```text
interface IDeterministicReplayHarness {
  compute_inputs_hash(canonical_inputs) -> inputs_hash;
  run_seed_replays(seed_set, replay_slice, ordered_identity_sequence) -> replay_runs[];
  reconcile_end_state(replay_runs[]) -> dual_hash_reconciliation_result;
  make_apply_side_effect_plan(reconciliation_result, idempotency_ledger_key) -> side_effect_plan;
}
```

### Canonical inputs checksum (scope)
- `seed_set`: explicit seed identifiers (or seed hashes) used for replay determinism.
- `replay_slice`: `from_tick` and `to_tick` bounds.
- `ordered_identity_sequence`: the ordered command/event identity list used by the replay executor.
- Deterministic gate version/table identifiers that affect the deterministic outcome.

## Harness algorithm sketch

```text
function deterministic_replay_harness(run_ctx):
  inputs_hash = compute_inputs_hash(canonical_inputs(run_ctx))

  for each seed in run_ctx.seed_set:
    replay = execute_replay(seed, run_ctx.replay_slice, run_ctx.ordered_identity_sequence)
    record end_state_dual_hash = { state_hash, metadata_hash }

  reconciliation = fail_closed_reconcile(end_state_dual_hashes)
  if reconciliation.ok != true:
    return deny("REPLAY_DETERMINISM_VIOLATION", evidence={inputs_hash, end_state_dual_hashes})

  side_effect_plan = make_apply_side_effect_plan(reconciliation, idempotency_ledger_key)
  return allow("REPLAY_CONVERGED", evidence={inputs_hash, side_effect_plan})
```

## Replay slice ordering invariant (v1)

All replay evaluation must use a single canonical ordering key; the harness must reject or normalize any replay inputs that cannot be mapped into that canonical ordering deterministically.

```text
ordering_key = (stream_id, replay_tick, ordering_index, event_id)
event_id := deterministic_from(command_id, command_version, event_version)
```

Invariant:
- No unordered iteration over sets/maps during replay execution and checksum computation.
- The harness serializes identity sequences in stable key order before hashing.

## Idempotent dry-run/apply side-effect plan (v1)

1) Dry-run (pure):
- Compute the dual-hash end state from deterministic replay.
- Compute deterministic side-effect plan for gated application.
- Produce a stable result summary keyed by dual hashes and `inputs_hash`.

2) Apply (gated):
- Apply side effects only when the idempotency ledger key is not already present for the stable replay identity tuple.

Ledger key recommendation:
- `idempotency_ledger_key = (stream_id, idempotency_key, payload_hash, result_hash)`

## Seed-based determinism test matrix (>=3 seeds)

Minimum matrix (execute `N` replays per seed; `N >= 3`):
- Seed A: `seed_id=A` with identical `replay_slice` and `ordered_identity_sequence` -> expect identical `end_state_dual_hash` across N replays.
- Seed B: `seed_id=B` with identical `replay_slice` and `ordered_identity_sequence` -> expect identical `end_state_dual_hash` across N replays.
- Seed C: `seed_id=C` with identical `replay_slice` and `ordered_identity_sequence` -> expect identical `end_state_dual_hash` across N replays.

Drift scenario (one controlled input perturbation):
- Modify one deterministic gate input identifier (e.g. gate version) or event identity ordering -> harness must produce a fail-closed divergence outcome and record deterministic evidence (inputs hash + observed dual hashes).

## Verification and test matrix closure (executable assertions, v1)

### Fixtures (concrete)

- Seed set (3 seeds):
  - Seed A: `seed_id: "A"`
  - Seed B: `seed_id: "B"`
  - Seed C: `seed_id: "C"`

- Replay slice bounds:
  - `from_tick: 1000`
  - `to_tick: 1050`

- Canonical ordering tuple used by evaluation/hashing:
  - `ordering_key = (stream_id, replay_tick, ordering_index, event_id)`
  - `event_id := deterministic_from(command_id, command_version, event_version)`

- Deterministic gate/version identifiers:
  - Baseline gate id: `deterministic_gate_version_id: "DETERMINISTIC_GATE_V1"`
  - Drift gate id: `deterministic_gate_version_id: "DETERMINISTIC_GATE_V2"`

- Ordered identity sequence (explicit constant list representation, length 4):
  - identity_0: `{command_id: "CMD_ALPHA", command_version: 1, event_version: 1}`
  - identity_1: `{command_id: "CMD_BETA", command_version: 1, event_version: 1}`
  - identity_2: `{command_id: "CMD_GAMMA", command_version: 1, event_version: 1}`
  - identity_3: `{command_id: "CMD_DELTA", command_version: 1, event_version: 1}`

### Test matrix (N replays per seed)

Use `N = 3` replays per seed.

For each seed in `{A,B,C}`:
1. Run deterministic replay harness dry-run for `seed_id = <seed>`, `replay_slice = {from_tick: 1000, to_tick: 1050}`, and the exact `ordered_identity_sequence` above with `deterministic_gate_version_id = "DETERMINISTIC_GATE_V1"`.
2. Capture evidence deterministically from reconciliation output:
   - `inputs_hash`
   - `end_state_dual_hash = { state_hash, metadata_hash }`
   - `ordering_key` evidence (any deterministic serialization acceptable, but it must be derived from the ordering tuple components)
3. Assertions (pass):
   - Across the three replays for the same seed, `inputs_hash` must match exactly.
   - Across the three replays for the same seed, `end_state_dual_hash.state_hash` must match exactly.
   - Across the three replays for the same seed, `end_state_dual_hash.metadata_hash` must match exactly.

### Drift scenario (fail-closed divergence)

1. Use the same replay fixtures with `seed_id = "A"` and the same identity sequence.
2. Apply exactly one controlled perturbation:
   - Change only `deterministic_gate_version_id` from `DETERMINISTIC_GATE_V1` to `DETERMINISTIC_GATE_V2`.
3. Run reconciliation and require fail-closed behavior.

Assertions (fail-closed deny):
- The harness must return a deterministic reconciliation/denial mismatch outcome (not "close enough").
- The denial must include:
  - `reason_code: "PAYLOAD_HASH_DRIFT"`
  - evidence containing `inputs_hash` and both baseline vs divergent dual hashes (`state_hash` + `metadata_hash`).
- The harness must not produce/allow an apply-side-effect plan that mutates persistent state for this mismatch.

### Idempotent dry-run/apply apply-phase assertions

1. After the determinism pass (seed A baseline), generate a side-effect plan via `make_apply_side_effect_plan` using the ledger key tuple:
   - `idempotency_ledger_key = (stream_id, idempotency_key, payload_hash, result_hash)`
2. Apply side effects once.
3. Re-run apply for the exact same replay identity tuple and require ledger-hit gating.

Assertions (idempotency):
- The second apply must detect the ledger key presence and perform zero state mutations.
- Evidence captured for both applies must include the ledger-key tuple used and the gating result (present/not-present).

## Research integration

### Key takeaways
- A deterministic replay harness should compute an explicit **checksum over canonical inputs** (seed + ordered command/event identities + relevant parameters) and then verify that **replays converge to the same end-state dual-hash**.
- Event sourcing determinism requires a **canonical ordering key** and a ban/control list for non-deterministic evaluation paths.
- Idempotence must be implemented as a **dry-run (pure) decision phase** plus an **apply phase** gated by an “already applied” ledger keyed to stable identifiers.
- Reconciliation across runs should compare both `state_hash` and `metadata_hash`, and on mismatch emit a deterministic divergence outcome using **frozen reason-code enums**.

### Decisions / constraints (must be enforced)
- [D-004] Treat validation rejections/deferrals as **deterministic replay events with stable reason codes** (no implicit/inferential “errors”).
- [D-005] Snapshot commit requires **dual-hash**: `state_hash` + `metadata_hash` (the harness must validate both).
- [D-006] Parent lineage links are **append-only and immutable post-commit**; lineage verification is part of the restore/replay preflight.
- [D-011] For distributed continuation, reuse the **canonical reason-code enum** exactly (do not invent new codes without versioning). Canonical enum strings:
  - `STALE_EPOCH`
  - `QUORUM_MISMATCH`
  - `SESSION_NOT_PREPARED`
  - `IDEMPOTENCY_REPLAY`
  - `PAYLOAD_HASH_DRIFT`

### Deterministic replay harness (what Phase 1.1.9 should formalize)

#### 1) Harness inputs + deterministic checksum
- **Inputs (per run):**
  - `seed_id` (and/or `seed_hash`), `stream_id` or `stream_set`, replay slice bounds (`from_tick`, `to_tick`), and a **fully specified ordered command/event identity sequence**.
  - The relevant deterministic gate parameters that affect outcomes.
- **Canonical serialization rule:**
  - Use stable key ordering, fixed-width numeric encoding (including a quantized float policy), and deterministic byte layout.
  - Compute `inputs_hash = H(canonical_inputs_bytes)`.
- **Harness checksum scope (recommendation):**
  - Include at minimum: `inputs_hash`, ordered identity list representation, and the relevant deterministic gate version/table identifiers.

#### 2) Event sourcing deterministic replay ordering
- Define a single canonical ordering key for the replay slice, e.g.:
  - `(stream_id, replay_tick, ordering_index, event_id)`
  - where `event_id` (or derived ordering_index) is deterministic from `{command_id, event_version}`.
- Assert an ordering invariant:
  - the harness must never “iterate unordered containers” (maps/sets) in a way that changes evaluation order.

#### 3) Test matrix: seed-based replay determinism
- Implement a minimal test matrix that guarantees determinism across:
  - Multiple seeds (at least 3) with identical replay slice bounds + ordered identity sequence.
  - Duplicate replay of the same idempotency tuple (same keys, same `payload_hash`/computed deterministic payload hash).
  - A drift scenario where deterministic payload changes and the harness must produce a deterministic divergence outcome.
- Acceptance condition (gate completion):
  - For each seed in the matrix, `end_state_dual_hash` matches the baseline across N replays.

#### 4) Idempotent replay side-effect plan
- Split the harness into two phases:
  - **Dry-run (pure):** evaluate determinism gate and compute the **side-effect plan** without mutating persistent state.
  - **Apply (gated):** apply side effects only after the idempotency ledger confirms “not already applied” for the stable idempotency tuple.
- Idempotency ledger key recommendation (aligning to Phase 1.1.3):
  - `(stream_id, idempotency_key, payload_hash, result_hash)`
- Deterministic replay rule:
  - repeated dry-run must yield identical `{inputs_hash, reason_code, terminal_state}` and identical side-effect plan.

#### 5) Reconciliation: end-state hash across runs
- After replay application, compute and compare:
  - `end_state_dual_hash = { state_hash, metadata_hash }`.
- On mismatch:
  - fail closed (do not treat as “close enough”).
  - emit a deterministic divergence reason code; for distributed-continuation-related drift, prefer `PAYLOAD_HASH_DRIFT` from the frozen enum.
  - record reconciliation evidence deterministically: `inputs_hash`, ordering checksum, and lineage verification result.

### Sources (for wiring into Phase 1.1.9)
- `[[decisions-log#Decisions]]` (D-004/D-005/D-006/D-011)
- `[[phase-1-1-3-replay-determinism-gate-and-compensation-orchestrator-roadmap-2026-03-19-1200]]` (reason-code baseline + deterministic gate framing)
- `[[phase-1-1-4-state-snapshot-lineage-and-authoritative-rollback-ledger-roadmap-2026-03-19-1201]]` (dual-hash + lineage verification)
- `[[phase-1-1-5-idempotent-state-rehydration-contract-and-cold-start-consistency-roadmap-2026-03-19-1208]]` (idempotent restore + ordering invariants)
- `[[phase-1-1-6-distributed-rehydration-continuation-coordinator-and-quorum-activation-roadmap-2026-03-19-1216]]` (frozen distributed continuation reason-code enum)
- `[[Ingest/Agent-Research/phase-1-1-7-quorum-degradation-safe-mode-write-fencing-research-2026-03-19-1333.md]]` (dry-run replay procedure + serialization policy details)

