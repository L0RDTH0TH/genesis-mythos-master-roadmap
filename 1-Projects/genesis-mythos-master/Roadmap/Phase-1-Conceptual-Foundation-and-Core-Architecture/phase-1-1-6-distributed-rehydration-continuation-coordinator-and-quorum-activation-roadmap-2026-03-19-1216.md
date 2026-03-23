---
title: Phase 1.1.6 - Distributed Rehydration Continuation Coordinator and Quorum Activation
roadmap-level: tertiary
phase-number: 1
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-19
tags: [roadmap, genesis-mythos-master, phase]
para-type: Project
subphase-index: "1.1.6"
links:
  - "[[phase-1-1-core-architecture-contracts-roadmap-2026-03-19-0001]]"
  - "[[phase-1-1-5-idempotent-state-rehydration-contract-and-cold-start-consistency-roadmap-2026-03-19-1208]]"
---

## Phase 1.1.6 - Distributed Rehydration Continuation Coordinator and Quorum Activation

Extend single-stream idempotent rehydration into deterministic multi-stream continuation so resume can safely unlock writes only after cross-stream quorum checks pass.

### Objectives

- [ ] Define coordinator contract for prepare/activate rehydration across stream sets.
- [ ] Add resume-epoch fencing to block stale leaders and duplicate activations.
- [ ] Enforce all-or-nothing activation semantics for cross-stream rehydration.
- [ ] Produce deterministic reason-code outcomes for quorum failures.

## Continuation coordinator contract (v1)

```text
interface RehydrationContinuationCoordinator {
  prepare_rehydrate(stream_set: string[], checkpoint_hash_family: string, resume_epoch: int, idempotency_key: string) -> PrepareResult;
  verify_quorum(stream_set: string[], rehydrate_session_id: string) -> QuorumResult;
  activate_resume(rehydrate_session_id: string, resume_epoch: int) -> ActivationResult;
  fence_stale_epoch(stream_id: string, observed_epoch: int, active_epoch: int) -> FenceResult;
}

PrepareResult:
- session_id
- stream_set_valid
- hash_family_compatible
- quorum_required
- blocker_reason_code
```

## Event and command contracts (v1)

```yaml
rehydrate.prepare.command:
  command_id: string
  stream_set: [string]
  expected_checkpoint_family: string
  resume_epoch: integer
  idempotency_key: string

rehydrate.quorum_verified.event:
  event_id: string
  correlation_id: string
  rehydrate_session_id: string
  stream_count: integer
  hash_family: string
  deterministic_payload_hash: string

rehydrate.activate.command:
  command_id: string
  rehydrate_session_id: string
  resume_epoch: integer
  idempotency_key: string

rehydrate.fenced.event:
  event_id: string
  correlation_id: string
  observed_epoch: integer
  active_epoch: integer
  blocker_reason_code: string
```

### Canonical reason-code enum (v1)

```text
STALE_EPOCH
  meaning: observed coordinator epoch is behind active epoch; request fenced.
QUORUM_MISMATCH
  meaning: one or more streams failed checkpoint hash-family compatibility.
SESSION_NOT_PREPARED
  meaning: activate attempted without successful prepare + quorum_verified phase.
IDEMPOTENCY_REPLAY
  meaning: duplicate activate/prepare tuple; return canonical prior outcome.
PAYLOAD_HASH_DRIFT
  meaning: deterministic payload hash changed between prepare and activate.
```

### Field constraints (execution-grade)

- `resume_epoch` is required, integer, and monotonically increasing per stream set.
- `idempotency_key` is required UUID-like string and must be reused for retries.
- `rehydrate_session_id` is required for `activate` and must map to a successful `prepare`.
- `deterministic_payload_hash` is required on all emitted events and must be stable for same input tuple.
- `expected_checkpoint_family` is required on prepare and immutable through activation.

## End-to-end message flow example (deterministic)

### Success branch (prepare -> quorum_verified -> activate)

1. `rehydrate.prepare.command`
   - `command_id: cmd-801`
   - `stream_set: [world-a, world-b, world-c]`
   - `expected_checkpoint_family: chkfam-71f9`
   - `resume_epoch: 44`
   - `idempotency_key: 4a3d5e5b-2fa4-4f4a-a2d1-1e52f6f27c3a`
2. `rehydrate.quorum_verified.event`
   - `event_id: evt-802`
   - `rehydrate_session_id: rsess-44-001`
   - `deterministic_payload_hash: h-3f4a2f`
3. `rehydrate.activate.command`
   - `command_id: cmd-803`
   - `rehydrate_session_id: rsess-44-001`
   - `resume_epoch: 44`
4. Expected deterministic result
   - activation accepted
   - mutation path unlocked once
   - duplicate activate with same tuple returns `IDEMPOTENCY_REPLAY` canonical prior result

### Failure branch (fenced stale coordinator)

1. Node attempts `rehydrate.activate.command` with `resume_epoch: 43` and session `rsess-44-001`.
2. Emit `rehydrate.fenced.event` with:
   - `observed_epoch: 43`
   - `active_epoch: 44`
   - `blocker_reason_code: STALE_EPOCH`
3. Expected deterministic result
   - no activation side effects
   - write-path remains blocked for stale coordinator
   - same stale request always yields same fenced outcome hash

## Research integration

## Research injection for 1.1.6 — Distributed Consistency and Idempotent Rehydration Continuation

> [!info] Vault-first research synthesis (Phase-1-1-5 -> next deepen 1.1.6)
> **Scope:** distributed state consistency, idempotent rehydration, and continuation safety after cold start.

### Assumptions (explicit)

- A dedicated `1.1.6` note is not yet present, so this proposes a continuation target inferred from `1.1.3` to `1.1.5` contracts and `workflow_state` next-step intent.
- Current architecture remains stream-scoped with deterministic ordering and checkpoint/hash verification as hard gates.

### Proposed 1.1.6 focus

- Define a **Rehydration Continuation Coordinator** that upgrades single-stream idempotent restore (`1.1.5`) to **multi-stream/shard-safe resume**.
- Introduce a **resume barrier token** (`resume_epoch`, `checkpoint_hash_family`, `rehydrate_session_id`) that must match across participating streams before writes reopen.
- Require **two-phase resume semantics**:
  1) `rehydrate.prepare` (preflight + lineage/hash quorum)
  2) `rehydrate.activate` (side-effect enablement only after deterministic parity checks pass).
- Add **fencing + stale-leader protection**: any node/session with older `resume_epoch` is read-only and cannot publish commit events.

### Determinism and safety invariants

- Same `(stream_set, snapshot set, replay slices, resume_epoch)` always yields same activation verdict.
- No partial activation: if any stream fails preflight/quorum, all remain in blocked/read-only state.
- Duplicate `rehydrate.activate` with same idempotency tuple returns prior canonical result without side effects.
- Cross-stream drift is surfaced as deterministic reason codes (not best-effort warnings).

## Task decomposition (v1)

- [ ] **T1 - Prepare-phase coordinator**
  - owner_surface: rehydration coordinator service
  - done_condition: all prepare checks return deterministic verdict with reason code
- [ ] **T2 - Quorum verifier**
  - owner_surface: checkpoint lineage validator
  - done_condition: verify all streams before activation is eligible
- [ ] **T3 - Epoch fencing gate**
  - owner_surface: command gateway
  - done_condition: stale epochs are rejected with `STALE_EPOCH`
- [ ] **T4 - Activation gate**
  - owner_surface: runtime state gate
  - done_condition: no partial activation when any member stream fails

## Executable test plan (v0)

- [ ] **Q1:** same stream set and hashes produce identical activation verdict.
- [ ] **Q2:** stale coordinator attempt emits deterministic `STALE_EPOCH`.
- [ ] **Q3:** one-stream mismatch blocks full activation.
- [ ] **Q4:** duplicate activate command yields prior canonical result only.

## Risk register v0

| Risk ID | Failure mode | Impact | Mitigation | Rollback/fence behavior | Test mapping |
| --- | --- | --- | --- | --- | --- |
| RSK-1 | Partial quorum pass incorrectly unlocks writes | split-brain resume | enforce all-or-nothing quorum gate in coordinator | keep all streams blocked until quorum_verified | Q1, Q3 |
| RSK-2 | Stale leader bypasses epoch gate | duplicate or divergent activation | mandatory epoch comparison on activate path | emit `STALE_EPOCH` and fence stale node | Q2 |
| RSK-3 | Payload hash drifts between prepare and activate | non-deterministic activation outcomes | immutable hash-family lock + hash check at activate | reject activation with `PAYLOAD_HASH_DRIFT` | Q1, Q4 |
| RSK-4 | Retry path writes duplicate side effects | data duplication | idempotency tuple ledger + canonical replay return | treat duplicate as read-only replay of prior outcome | Q4 |

## Decision links

- [[decisions-log#Decisions]] D-010 and D-011 capture quorum activation and reason-code commitments for this phase.

## Acceptance criteria (gated)

- [ ] **A1:** prepare/quorum contracts implemented with deterministic outputs.
- [ ] **A2:** activation and fencing reject stale/partial resume paths.
- [ ] **A3:** all tests Q1-Q4 pass under replay and retry scenarios.
