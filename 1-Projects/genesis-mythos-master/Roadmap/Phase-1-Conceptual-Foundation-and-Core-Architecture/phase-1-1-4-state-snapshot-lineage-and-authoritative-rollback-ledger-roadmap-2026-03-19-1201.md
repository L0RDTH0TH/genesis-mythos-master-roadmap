---
title: Phase 1.1.4 - State Snapshot Lineage and Authoritative Rollback Ledger
roadmap-level: tertiary
phase-number: 1
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-19
tags: [roadmap, genesis-mythos-master, phase]
para-type: Project
subphase-index: "1.1.4"
links:
  - "[[phase-1-1-core-architecture-contracts-roadmap-2026-03-19-0001]]"
  - "[[phase-1-1-3-replay-determinism-gate-and-compensation-orchestrator-roadmap-2026-03-19-1200]]"
---

## Phase 1.1.4 - State Snapshot Lineage and Authoritative Rollback Ledger

Define the authoritative snapshot lineage that anchors deterministic rollback and replay proofing. This phase binds checkpoint capture, lineage hashes, and rollback permissions into one auditable contract for junior implementation.

### Objectives

- [ ] Define canonical snapshot manifest schema and lineage identifiers.
- [ ] Formalize rollback ledger write/read APIs and invariants.
- [ ] Enforce snapshot retention windows with deterministic pruning rules.
- [ ] Add replay-verification checkpoints around rollback restore boundaries.

## Snapshot lineage contract (v1)

```text
interface SnapshotLineageLedger {
  begin_snapshot(stream_id: string, frame_id: int, parent_snapshot_id: string | null) -> SnapshotDraft;
  commit_snapshot(draft: SnapshotDraft, state_hash: string, metadata_hash: string) -> SnapshotRecord;
  get_snapshot(snapshot_id: string) -> SnapshotRecord;
  mark_rollback_anchor(stream_id: string, snapshot_id: string, reason_code: string) -> AnchorResult;
  verify_lineage(snapshot_id: string, expected_parent_id: string | null) -> VerificationResult;
}

SnapshotRecord:
- snapshot_id
- stream_id
- frame_id
- parent_snapshot_id
- state_hash
- metadata_hash
- created_at_tick
- retention_policy
```

## Command/event schema stubs (v1)

```yaml
snapshot.commit.command:
  command_id: string
  stream_id: string
  frame_id: integer
  parent_snapshot_id: string|null
  state_hash: string
  metadata_hash: string
  idempotency_key: string
  requested_by: string
  requested_at: string

rollback.anchor.command:
  command_id: string
  stream_id: string
  snapshot_id: string
  anchor_reason_code: string
  operator_context: string
  idempotency_key: string
  requested_at: string

rollback.restore.command:
  command_id: string
  stream_id: string
  target_snapshot_id: string
  expected_parent_snapshot_id: string|null
  anchor_reason_code: string
  operator_context: string
  idempotency_key: string

snapshot.prune.command:
  command_id: string
  stream_id: string
  retention_policy_id: string
  dry_run: boolean
  idempotency_key: string
```

```yaml
snapshot.committed.event:
  event_id: string
  correlation_id: string
  causation_id: string
  reason_code: string
  emitted_at: string
  deterministic_payload_hash: string

rollback.anchor.recorded.event:
  event_id: string
  correlation_id: string
  causation_id: string
  reason_code: string
  emitted_at: string
  deterministic_payload_hash: string

rollback.restore.blocked.event:
  event_id: string
  correlation_id: string
  causation_id: string
  reason_code: string
  emitted_at: string
  deterministic_payload_hash: string

rollback.restore.committed.event:
  event_id: string
  correlation_id: string
  causation_id: string
  reason_code: string
  emitted_at: string
  deterministic_payload_hash: string

snapshot.pruned.event:
  event_id: string
  correlation_id: string
  causation_id: string
  reason_code: string
  emitted_at: string
  deterministic_payload_hash: string
```

### Ledger invariants

- Snapshot IDs are stable and collision-safe under deterministic hashing.
- Parent linkage is immutable once a snapshot is committed.
- Rollback anchors only reference committed snapshots in the same stream.
- Retention pruning cannot remove active rollback anchors.
- Replay verification must re-check lineage + hash pair before restore.

## Implementation notes for deepen

- Keep snapshot serialization canonical (sorted keys, fixed encoding).
- Store lineage edge (`parent_snapshot_id`) in every committed record.
- Require rollback requests to include `anchor_reason_code` and `operator_context`.
- Emit deterministic audit events for create/anchor/restore/prune operations.
- Treat cross-stream rollback references as hard rejects.

## End-to-end rollback message flow (example v1)

1. `rollback_request_received(stream_id, target_snapshot_id, anchor_reason_code, operator_context, idempotency_key)`
2. `validate_request_fields + idempotency_check`
3. `anchor_check(target_snapshot_id, stream_id, anchor_reason_code)`
4. `lineage_verify(target_snapshot_id, expected_parent_chain, state_hash, metadata_hash)`
5. Success branch: `restore_begin -> restore_commit -> audit_event(restore_succeeded)`
6. Fail branch: `restore_prevented(reason_code: lineage_mismatch|anchor_missing|cross_stream_reject) -> audit_event(restore_blocked)`

## Research integration

### Key takeaways

- Deterministic rollback safety depends on immutable lineage links, not just raw state dumps.
- Snapshot metadata hashes are as critical as world-state hashes for replay confidence.
- Retention rules must be explicit and policy-driven to avoid silent replay breakage.
- Restore operations need preflight lineage verification before state mutation.
- Auditability improves when rollback anchors are first-class records.

### Decisions / constraints

- Snapshot commit requires both state hash and metadata hash.
- Parent lineage edges are append-only and never rewritten.
- Rollback is stream-scoped and anchor-gated.
- Retention pruning runs only when no active anchor depends on the snapshot.
- Replay restore is blocked when lineage verification fails.

#### Decision anchors

- [D-005] Snapshot commit requires both `state_hash` and `metadata_hash`.
- [D-006] Parent lineage edges are append-only and immutable post-commit.
- [D-007] Rollback is stream-scoped and anchor-gated.
- [D-008] Prune cannot remove snapshots referenced by active anchors.
- [D-009] Restore is blocked on lineage/hash verification failure.

### Sources

- [Source: Martin Fowler - Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)
- [Source: EventSourcingDB - Event Validation and Idempotency](https://docs.eventsourcingdb.io/best-practices/common-issues/)
- [Source: Deterministic Lockstep | Gaffer On Games](https://gafferongames.com/post/deterministic_lockstep/)

## Task decomposition (v1)

- [ ] **T1 - Snapshot manifest schema**
  - owner_surface: persistence contracts package
  - inputs: stream_id, frame_id, parent_snapshot_id, state hash payload
  - outputs: versioned snapshot schema + strict validation
  - done_condition: invalid schema cannot be committed
- [ ] **T2 - Snapshot commit pipeline**
  - owner_surface: snapshot writer service
  - inputs: draft snapshot + hash bundle
  - outputs: committed snapshot record + audit event
  - done_condition: commit path is deterministic and idempotent
- [ ] **T3 - Rollback anchor registry**
  - owner_surface: rollback orchestration service
  - inputs: stream context, snapshot_id, reason_code
  - outputs: active anchor record with correlation id
  - done_condition: rollback can only target anchor-approved snapshots
- [ ] **T4 - Lineage verifier**
  - owner_surface: replay/restore validator
  - inputs: snapshot_id, expected parent chain
  - outputs: verification pass/fail with deterministic reason_code
  - done_condition: any parent mismatch blocks restore
- [ ] **T5 - Retention and prune policy**
  - owner_surface: storage maintenance job
  - inputs: retention window + anchor set
  - outputs: deterministic prune plan + safe-deletion events
  - done_condition: anchored snapshots are never pruned
- [ ] **T6 - Replay restore preflight**
  - owner_surface: replay orchestrator
  - inputs: target snapshot + lineage verification + checkpoint expectation
  - outputs: restore-ready decision
  - done_condition: restore only proceeds after lineage + hash checks

## Executable test plan (v0)

- [ ] **R1 - Snapshot commit determinism:** same input draft yields same snapshot hash and id.
- [ ] **R2 - Parent mismatch block:** lineage verifier rejects incorrect parent edge.
- [ ] **R3 - Anchor enforcement:** rollback request without active anchor is rejected.
- [ ] **R4 - Retention safety:** prune routine skips snapshots referenced by anchors.
- [ ] **R5 - Restore preflight failure:** restore blocked when metadata hash diverges.
- [ ] **R6 - Stream isolation:** cross-stream snapshot references are rejected deterministically.

## Acceptance criteria (gated)

- [ ] **A1:** Snapshot schema + commit pipeline implemented and deterministic (T1/T2).
- [ ] **A2:** Rollback anchor + lineage verifier gate all restore paths (T3/T4/T6).
- [ ] **A3:** Retention policy preserves rollback safety and auditability (T5).
