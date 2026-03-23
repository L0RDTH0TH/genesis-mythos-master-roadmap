---
title: Phase 1.1.7 - Quorum Degradation Safe Mode and Read/Write Fencing Policy
roadmap-level: tertiary
phase-number: 1
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-19
tags: [roadmap, genesis-mythos-master, phase]
para-type: Project
subphase-index: "1.1.7"
links:
  - "[[phase-1-1-core-architecture-contracts-roadmap-2026-03-19-0001]]"
  - "[[phase-1-1-6-distributed-rehydration-continuation-coordinator-and-quorum-activation-roadmap-2026-03-19-1216]]"
---

## Phase 1.1.7 - Quorum Degradation Safe Mode and Read/Write Fencing Policy

Define deterministic safe-mode behavior for quorum degradation so write paths are always fenced consistently and recovery transitions are explicit, replayable, and idempotent.

### Objectives

- [ ] Formalize safe-mode state machine and legal transitions for quorum degradation.
- [ ] Specify read/write fencing policy per node role and epoch state.
- [ ] Define deterministic freeze, demote, and recovery activation gates.
- [ ] Lock audit and reason-code contracts for all quorum-loss and re-entry paths.

## Safe-mode state machine (v1)

```text
states:
  ACTIVE
  DEGRADED_READ_ONLY
  FENCED_RECOVERY
  RECOVERY_PREPARED
  QUORUM_RESTORED
  REACTIVATED

legal_transitions:
  ACTIVE -> DEGRADED_READ_ONLY          (quorum_loss_detected)
  DEGRADED_READ_ONLY -> FENCED_RECOVERY (epoch_or_hash_mismatch)
  DEGRADED_READ_ONLY -> RECOVERY_PREPARED (quorum_stable + hash_verified)
  FENCED_RECOVERY -> RECOVERY_PREPARED  (operator_recover + checkpoints_verified)
  RECOVERY_PREPARED -> QUORUM_RESTORED  (majority_ack + activation_epoch_consensus)
  QUORUM_RESTORED -> REACTIVATED        (write_fence_lifted_deterministically)
```

## Read/write fencing contract (v1)

```yaml
write_fence.policy:
  required_inputs:
    - activation_epoch
    - cluster_epoch
    - quorum_proof_hash
    - node_role
    - state_hash
  decision:
    allow_write: boolean
    allow_read: boolean
    reason_code: string

degraded_defaults:
  leader_candidate:
    allow_write: false
    allow_read: true
  followers:
    allow_write: false
    allow_read: true
  fenced_nodes:
    allow_write: false
    allow_read: false
```

### Canonical reason codes

```text
QUORUM_LOST
EPOCH_MISMATCH
HASH_DIVERGENCE
QUORUM_PROOF_MISSING
WRITE_FENCE_ACTIVE
RECOVERY_NOT_PREPARED
REACTIVATION_BLOCKED
```

## Deterministic recovery pseudocode

```text
function evaluate_write_gate(node_ctx, cluster_ctx):
  if node_ctx.activation_epoch != cluster_ctx.cluster_epoch:
    return deny("EPOCH_MISMATCH")
  if !cluster_ctx.quorum_proof_hash:
    return deny("QUORUM_PROOF_MISSING")
  if node_ctx.state_hash != cluster_ctx.state_hash:
    return deny("HASH_DIVERGENCE")
  if cluster_ctx.mode in ["DEGRADED_READ_ONLY", "FENCED_RECOVERY", "RECOVERY_PREPARED"]:
    return deny("WRITE_FENCE_ACTIVE")
  return allow()
```

## Verification and test matrix

- [ ] Simulate quorum loss mid-activation; verify deterministic transition to `DEGRADED_READ_ONLY`.
- [ ] Re-run identical recovery inputs across nodes; assert same final state and reason codes.
- [ ] Force stale epoch write attempt; assert deterministic `EPOCH_MISMATCH` denial.
- [ ] Validate write re-enable only after quorum proof and matching state hash.
- [ ] Reject `EvaluateWriteGate` requests missing required identity/version fields or with unknown reason-code domain.
- [ ] Assert exactly one deterministic denial event per failed gate evaluation with stable `command_id` linkage.

## Command and event schema contracts (v1)

```yaml
evaluate_write_gate.command:
  identity:
    command_id: { type: string, required: true, nullable: false }
    command_version: { type: string, required: true, nullable: false, allowed: ["v1"] }
    correlation_id: { type: string, required: true, nullable: false }
    emitted_at_utc: { type: string, required: true, nullable: false, format: iso-8601 }
  payload:
    node_id: { type: string, required: true, nullable: false }
    node_role: { type: string, required: true, nullable: false, allowed: ["leader_candidate", "follower", "fenced"] }
    activation_epoch: { type: integer, required: true, nullable: false, min: 0 }
    cluster_epoch: { type: integer, required: true, nullable: false, min: 0 }
    state_hash: { type: string, required: true, nullable: false }
    quorum_proof_hash: { type: string, required: true, nullable: false }
```

```yaml
write_gate_denied.event:
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
        - QUORUM_LOST
        - EPOCH_MISMATCH
        - HASH_DIVERGENCE
        - QUORUM_PROOF_MISSING
        - WRITE_FENCE_ACTIVE
        - RECOVERY_NOT_PREPARED
        - REACTIVATION_BLOCKED
    terminal_state:
      type: string
      required: true
      nullable: false
      allowed:
        - DEGRADED_READ_ONLY
        - FENCED_RECOVERY
        - RECOVERY_PREPARED
```

## Deterministic command->event message flows (reason-code complete)

### Branch A - QUORUM_PROOF_MISSING

```yaml
input_command:
  command_id: cmd-1-1-7-401
  command_version: v1
  node_role: leader_candidate
  activation_epoch: 45
  cluster_epoch: 45
  state_hash: h-a12d
  quorum_proof_hash: ""
emitted_event:
  event_id: evt-1-1-7-401
  event_version: v1
  command_id: cmd-1-1-7-401
  allow_write: false
  allow_read: true
  reason_code: QUORUM_PROOF_MISSING
  terminal_state: DEGRADED_READ_ONLY
side_effects:
  - write path remains fenced
  - activation gate stays blocked
```

### Branch B - EPOCH_MISMATCH

```yaml
input_command:
  command_id: cmd-1-1-7-402
  command_version: v1
  node_role: follower
  activation_epoch: 44
  cluster_epoch: 45
  state_hash: h-a12d
  quorum_proof_hash: qp-45-a9f0
emitted_event:
  event_id: evt-1-1-7-402
  event_version: v1
  command_id: cmd-1-1-7-402
  allow_write: false
  allow_read: true
  reason_code: EPOCH_MISMATCH
  terminal_state: FENCED_RECOVERY
side_effects:
  - stale epoch node is fenced
  - recovery preparation required before reactivation
```

### Branch C - HASH_DIVERGENCE

```yaml
input_command:
  command_id: cmd-1-1-7-403
  command_version: v1
  node_role: leader_candidate
  activation_epoch: 45
  cluster_epoch: 45
  state_hash: h-drifted
  quorum_proof_hash: qp-45-a9f0
  expected_state_hash: h-a12d
emitted_event:
  event_id: evt-1-1-7-403
  event_version: v1
  command_id: cmd-1-1-7-403
  allow_write: false
  allow_read: false
  reason_code: HASH_DIVERGENCE
  terminal_state: FENCED_RECOVERY
side_effects:
  - node demoted to fenced recovery
  - operator-visible rollback path required
```

## Research integration

### Key takeaways
- Deterministic rehydration must be driven by canonical event ordering so equivalent inputs always converge.
- Resume should only occur from verified checkpoint boundaries (`last_applied_index` + state hash).
- Quorum-safe activation is two-gated: consistency first, then majority-confirmed liveness.
- Activation must be epoch-scoped; stale nodes remain read-only or fenced.
- Replay/retry side effects must be idempotent and keyed to epoch and command identity.
- Membership/view changes must be committed before activation logic can trust them.
- Quorum or hash failure paths should freeze writes and force explicit recovery.

### Decisions / constraints
- Adopt activation flow `REHYDRATING -> CONSISTENT -> QUORUM_CONFIRMED -> ACTIVE`.
- Standardize checkpoint schema `{snapshot_hash, last_applied_index, activation_epoch}`.
- Require write-fence middleware to reject writes without valid epoch/hash/quorum proof.
- Add deterministic replay harness comparing end-state hashes across multi-node replay.
- Require operator-visible rollback/audit event when activation freeze or demotion occurs.

### Sources
- [Source: In Search of an Understandable Consensus Algorithm (Raft)](https://raft.github.io/raft.pdf)
- [Source: Paxos Made Simple](https://lamport.azurewebsites.net/pubs/paxos-simple.pdf)
- [Source: Idempotence Is Not a Medical Condition](https://queue.acm.org/detail.cfm?id=2187821)
- [Source: Designing Data-Intensive Applications](https://dataintensive.net/)
- [Source: Jepsen Analyses](https://aphyr.com/tags/jepsen)
