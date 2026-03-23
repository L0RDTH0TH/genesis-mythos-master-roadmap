---
title: Phase 1.1.8 - Quorum Restoration and Deterministic Write Fence Lift
roadmap-level: tertiary
phase-number: 1
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-19
tags: [roadmap, genesis-mythos-master, phase]
para-type: Project
subphase-index: "1.1.8"
links:
  - "[[phase-1-1-core-architecture-contracts-roadmap-2026-03-19-0001]]"
  - "[[phase-1-1-7-quorum-degradation-safe-mode-and-read-write-fencing-policy-roadmap-2026-03-19-1230]]"
---

## Phase 1.1.8 - Quorum Restoration and Deterministic Write Fence Lift

Define the deterministic reactivation sequence that lifts write fences only after quorum restoration is evidenced, activation epochs are consistent, and the replay plan is idempotent and auditable.

### Objectives
- [ ] Specify quorum restoration evidence requirements (majority ack + checkpoint parity).
- [ ] Define deterministic write fence lift criteria (activation epoch consensus and reason codes).
- [ ] Add command/event contracts for fence lift with stable identifiers and provenance.
- [ ] Provide an execution-grade reactivation sequence pseudocode.

## Activation quorum -> write fence lift (v1)

```text
Input:
  - activation_epoch (int)
  - cluster_epoch (int)
  - quorum_proof_hash (string)
  - state_hash (string)
  - last_applied_index (int)
  - checkpoint_hash_family (string)
  - reason_code (enum)
Output:
  - allow_write (boolean)
  - allow_read (boolean)
  - terminal_state (string)

Rule:
  - Writes are allowed only when:
    1) quorum_proof_hash is present AND
    2) activation_epoch == cluster_epoch (or explicitly allowed equality per contract) AND
    3) state_hash matches the recovery anchor state_hash AND
    4) majority ack quorum restoration has been observed deterministically for this activation epoch.
  - Otherwise, remain in a fenced recovery terminal state and emit a deterministic denial reason_code.
```

## Deterministic reactivation sequence (algorithm sketch)

```text
function lift_write_fence(recovery_ctx):
  # Phase 0: freeze
  assert recovery_ctx.mode in ["FENCED_RECOVERY", "RECOVERY_PREPARED"]

  # Phase 1: verify checkpoint parity
  if recovery_ctx.state_hash != recovery_ctx.anchor_state_hash:
    return deny("HASH_DIVERGENCE", terminal_state="FENCED_RECOVERY")

  if !recovery_ctx.quorum_proof_hash:
    return deny("QUORUM_PROOF_MISSING", terminal_state="DEGRADED_READ_ONLY")

  # Phase 2: deterministic quorum restoration evidence
  if !replay_deterministic_majority_ack(
        activation_epoch=recovery_ctx.activation_epoch,
        last_applied_index=recovery_ctx.last_applied_index,
        quorum_proof_hash=recovery_ctx.quorum_proof_hash):
    return deny("RECOVERY_NOT_PREPARED", terminal_state="FENCED_RECOVERY")

  # Phase 3: activation epoch consensus
  if recovery_ctx.activation_epoch != recovery_ctx.cluster_epoch:
    return deny("EPOCH_MISMATCH", terminal_state="FENCED_RECOVERY")

  # Phase 4: lift fence (idempotent)
  if recovery_ctx.decision_event_id_seen_before:
    return allow("IDEMPOTENCY_REPLAY", terminal_state="REACTIVATED")

  record_decision_event_id(recovery_ctx.decision_event_id)
  return allow("WRITE_FENCE_LIFTED", terminal_state="REACTIVATED")
```

## Command and event schema contracts (v1)

```yaml
lift_write_fence.command:
  identity:
    command_id: { type: string, required: true, nullable: false }
    command_version: { type: string, required: true, nullable: false, allowed: ["v1"] }
    correlation_id: { type: string, required: true, nullable: false }
    emitted_at_utc: { type: string, required: true, nullable: false, format: iso-8601 }
  payload:
    decision_event_id: { type: string, required: true, nullable: false }
    activation_epoch: { type: integer, required: true, nullable: false, min: 0 }
    cluster_epoch: { type: integer, required: true, nullable: false, min: 0 }
    quorum_proof_hash: { type: string, required: true, nullable: false }
    state_hash: { type: string, required: true, nullable: false }
    anchor_state_hash: { type: string, required: true, nullable: false }
    last_applied_index: { type: integer, required: true, nullable: false, min: 0 }
    checkpoint_hash_family: { type: string, required: true, nullable: false }
```

```yaml
write_fence_lifted.event:
  identity:
    event_id: { type: string, required: true, nullable: false }
    event_version: { type: string, required: true, nullable: false, allowed: ["v1"] }
    command_id: { type: string, required: true, nullable: false }
    correlation_id: { type: string, required: true, nullable: false }
  payload:
    allow_write: { type: boolean, required: true, nullable: false, fixed: true }
    allow_read: { type: boolean, required: true, nullable: false, fixed: true }
    reason_code:
      type: string
      required: true
      nullable: false
      allowed:
        - WRITE_FENCE_LIFTED
        - IDEMPOTENCY_REPLAY
    terminal_state:
      type: string
      required: true
      nullable: false
      allowed:
        - REACTIVATED
```

```yaml
write_fence_denied.event:
  identity:
    event_id: { type: string, required: true, nullable: false }
    event_version: { type: string, required: true, nullable: false, allowed: ["v1"] }
    command_id: { type: string, required: true, nullable: false }
    correlation_id: { type: string, required: true, nullable: false }
  payload:
    allow_write: { type: boolean, required: true, nullable: false, fixed: false }
    allow_read: { type: boolean, required: true, nullable: false }
    reason_code:
      type: string
      required: true
      nullable: false
      allowed:
        - QUORUM_PROOF_MISSING
        - RECOVERY_NOT_PREPARED
        - EPOCH_MISMATCH
        - HASH_DIVERGENCE
    terminal_state:
      type: string
      required: true
      nullable: false
      allowed:
        - DEGRADED_READ_ONLY
        - FENCED_RECOVERY
```

## Deterministic message flows (reason-code complete)

### Branch A - QUORUM_PROOF_MISSING

```yaml
input_command:
  command_id: cmd-1-1-8-101
  decision_event_id: dev-1-1-8-a
  activation_epoch: 51
  cluster_epoch: 51
  quorum_proof_hash: ""
  state_hash: h-ok-51
  anchor_state_hash: h-anchor-51
emitted_event:
  event_id: evt-1-1-8-101
  allow_write: false
  allow_read: true
  reason_code: QUORUM_PROOF_MISSING
  terminal_state: DEGRADED_READ_ONLY
side_effects:
  - keep writes fenced
  - require deterministic quorum evidence before any lift
```

### Branch B - EPOCH_MISMATCH

```yaml
input_command:
  command_id: cmd-1-1-8-102
  decision_event_id: dev-1-1-8-b
  activation_epoch: 52
  cluster_epoch: 51
emitted_event:
  event_id: evt-1-1-8-102
  allow_write: false
  allow_read: true
  reason_code: EPOCH_MISMATCH
  terminal_state: FENCED_RECOVERY
side_effects:
  - keep writes fenced
  - deny reactivation until consensus matches
```

### Branch C - WRITE_FENCE_LIFTED (idempotent allow)

```yaml
input_command:
  command_id: cmd-1-1-8-103
  decision_event_id: dev-1-1-8-c
  activation_epoch: 53
  cluster_epoch: 53
emitted_event:
  event_id: evt-1-1-8-103
  allow_write: true
  allow_read: true
  reason_code: WRITE_FENCE_LIFTED
  terminal_state: REACTIVATED
side_effects:
  - writes become deterministically unblocked
  - decision_event_id enables replay idempotency
```

### Branch D - HASH_DIVERGENCE

```yaml
input_command:
  command_id: cmd-1-1-8-104
  decision_event_id: dev-1-1-8-d
  activation_epoch: 54
  cluster_epoch: 54
  quorum_proof_hash: qp-54-a9f0
  state_hash: h-drifted-54
  anchor_state_hash: h-anchor-54
emitted_event:
  event_id: evt-1-1-8-104
  allow_write: false
  allow_read: false
  reason_code: HASH_DIVERGENCE
  terminal_state: FENCED_RECOVERY
side_effects:
  - node demoted to fenced recovery
  - operator-visible rollback path required
```

### Branch E - RECOVERY_NOT_PREPARED

```yaml
input_command:
  command_id: cmd-1-1-8-105
  decision_event_id: dev-1-1-8-e
  activation_epoch: 55
  cluster_epoch: 55
  quorum_proof_hash: qp-55-a9f0
  state_hash: h-ok-55
  anchor_state_hash: h-anchor-55
  replay_deterministic_majority_ack: false
emitted_event:
  event_id: evt-1-1-8-105
  allow_write: false
  allow_read: true
  reason_code: RECOVERY_NOT_PREPARED
  terminal_state: FENCED_RECOVERY
side_effects:
  - keep writes fenced
  - deny reactivation until deterministic quorum evidence is observed
```

### Branch F - IDEMPOTENCY_REPLAY (idempotent allow)

```yaml
input_command:
  command_id: cmd-1-1-8-106
  decision_event_id: dev-1-1-8-f
  activation_epoch: 56
  cluster_epoch: 56
  decision_event_id_seen_before: true
emitted_event:
  event_id: evt-1-1-8-106
  allow_write: true
  allow_read: true
  reason_code: IDEMPOTENCY_REPLAY
  terminal_state: REACTIVATED
side_effects:
  - idempotent reactivation confirmed without duplicating decision effects
  - replay safe: decision_event_id preserves audit trace
```

## Verification and test matrix
- [ ] Deterministic majority ack: identical quorum inputs yield identical lift verdict.
- [ ] Replay determinism: re-run `lift_write_fence` with same `decision_event_id` returns canonical idempotent outcome.
- [ ] Checkpoint parity: anchor `state_hash` mismatch always denies with HASH_DIVERGENCE.
- [ ] Epoch mismatch: stale epoch lift attempts must remain fenced and emit EPOCH_MISMATCH.
- [ ] Strict provenance: every allow/deny event includes decision_event_id for audit trace.

## Research integration

### Research integration

#### Key takeaways
- Fencing tokens/epochs validated at the **resource boundary** prevent “zombie writers” during quorum degradation (client belief != write permission).
- Map `activation_epoch` (and/or derived generation clock) + `quorum_proof_hash` + `state_hash` into your v1 write-fence gate so denials/lifts are deterministic and replayable.
- Treat the decision as an explicit, audit-friendly **decision event record** keyed to stable identifiers (e.g. `{inputs_hash, command_id}`), not an implicit local branch.
- Provide a **deterministic dry-run replay harness**: canonical serialize inputs -> hash to `inputs_hash` -> pure gate eval -> N replays assert identical outputs and identical “side-effect plan”.
- Include a concrete **determinism ban/control list** (no unseeded randomness, no unordered iteration, no schedule/env-dependent evaluation).
- Use a **canonical float/serialization policy** (quantized fixed-point -> fixed-width integer encoding -> stable key ordering -> versioned event-record formats).
- Attach a minimal **provenance record template** (`random_seed`/`stage_seed`, `dt_ms`, `intents_hash`, `from_snapshot_id`, hashes, and `diff_pointers`) so divergence can be traced.

#### Decisions / constraints
- Make `evaluate_write_gate` a pure function over the v1 gate inputs that emits `{allow_write, allow_read, reason_code, terminal_state}` with **zero** side effects during evaluation.
- Enforce fencing at the **storage/resource boundary**: reject stale fencing epochs regardless of client-side lease beliefs.
- Anchor recovery transitions to verified checkpoints (`last_applied_index` + `state_hash`) and require idempotent execution keyed to a stable `decision_event_id`.
- Standardize canonical serialization (including quantized floats) before computing hashes like `inputs_hash`.
- Require provenance + diff pointers for every dry-run decision and every applied recovery decision.
- Enforce tick/system ordering: evaluate gate decisions before any mutation; freeze writes during `DEGRADED_READ_ONLY` / `FENCED_RECOVERY`.

Links
- Synthesis note: [[Ingest/Agent-Research/phase-1-1-7-quorum-degradation-safe-mode-write-fencing-research-2026-03-19-1333.md]]

## Sources
- See `## Sources` in [[Ingest/Agent-Research/phase-1-1-7-quorum-degradation-safe-mode-write-fencing-research-2026-03-19-1333.md]]

