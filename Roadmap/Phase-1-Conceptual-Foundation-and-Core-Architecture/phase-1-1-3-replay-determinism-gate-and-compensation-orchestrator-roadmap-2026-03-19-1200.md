---
title: Phase 1.1.3 - Replay Determinism Gate and Compensation Orchestrator
roadmap-level: tertiary
phase-number: 1
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-19
tags: [roadmap, genesis-mythos-master, phase]
para-type: Project
subphase-index: "1.1.3"
links:
  - "[[phase-1-1-core-architecture-contracts-roadmap-2026-03-19-0001]]"
  - "[[phase-1-1-2-command-stream-validation-and-fault-recovery-roadmap-2026-03-19-1142]]"
---

## Phase 1.1.3 - Replay Determinism Gate and Compensation Orchestrator

Build the deterministic recovery gate that sits between validated command intake and authoritative state mutation. This phase turns rejection/defer metadata into replay-safe recovery behavior with explicit rollback and compensation checks.

### Objectives

- [ ] Implement terminal command lifecycle statuses and stable reason-code taxonomy.
- [ ] Add idempotency conflict handling with payload-hash verification.
- [ ] Introduce checkpoint hash validation across rollback and replay windows.
- [ ] Define compensation orchestration states with deterministic transitions.

## Determinism gate contract (v1)

```text
interface ReplayDeterminismGate {
  evaluate(cmd: CommandEnvelope, ctx: ReplayContext) -> GateDecision;
  verify_idempotency(cmd: CommandEnvelope, ledger: IdempotencyLedger) -> IdempotencyDecision;
  begin_recovery(stream_id: string, reason_code: string) -> RecoveryPlan;
  verify_checkpoint(expected_hash: string, actual_hash: string) -> VerificationResult;
}

GateDecision:
- proceed: command advances to mutation stage.
- reject: terminal failure, deterministic reason_code required.
- defer: retryable only with deterministic prerequisite key.
- compensate: rollback/undo plan required before replay.
```

### Reason code baseline

- `VAL_SCHEMA`
- `VAL_AUTH`
- `PRECONDITION_MISSING`
- `DUPLICATE_SAME`
- `DUPLICATE_CONFLICT`
- `DEPENDENCY_TIMEOUT`
- `ROLLBACK_WINDOW_EXCEEDED`
- `COMPENSATION_FAILED`

## Implementation notes for deepen

- Persist idempotency keys as `(stream_id, idempotency_key, payload_hash, result_hash)`.
- Treat same-key/same-hash as replay-safe deterministic return; same-key/different-hash is conflict reject.
- Use canonical ordering for replay verification to avoid non-deterministic collection traversal.
- Make compensation steps idempotent and correlation-linked to original command IDs.
- Emit verification events whenever post-recovery checkpoint hashes diverge.

## Research integration

### Key takeaways

- Deterministic simulation quality depends on stable ordering and explicit non-success outcomes.
- Replay safety improves when command handlers are pure before commit barriers.
- Rejection and deferral must be explicit, replay-visible outcomes with stable reason codes.
- Fault isolation should be stream-scoped with bulkheads and per-stream breakers.
- Rollback validity needs both compensation completeness and post-replay hash checks.

### Decisions / constraints

- Keep a finite reason-code set and version it intentionally.
- Require deterministic idempotency conflict rules tied to payload hash checks.
- Enforce a bounded rollback window with explicit breach reason codes.
- Route recovery through a state machine (`recovering -> compensating -> replaying -> verified -> resumed`).
- Fail the gate when replay hash mismatches expected checkpoint.

### Sources

- [Source: Deterministic Lockstep | Gaffer On Games](https://gafferongames.com/post/deterministic_lockstep/)
- [Source: Rollback Networking in INVERSUS](https://blog.hypersect.com/rollback-networking-in-inversus/)
- [Source: Netcode Architectures Part 2: Rollback | SnapNet](https://www.snapnet.dev/blog/netcode-architectures-part-2-rollback/)
- [Source: Idempotent Command Handling | Event-Driven.io](https://event-driven.io/en/idempotent_command_handling/)
- [Source: Timeouts, Retries, and Idempotency Keys](https://blog.lbenicio.dev/blog/timeouts-retries-and-idempotency-keys-a-practical-guide/)
- [Source: Compensating Actions / Saga Pattern | Temporal](https://temporal.io/blog/compensating-actions-part-of-a-complete-breakfast-with-sagas)

## Task decomposition (v1)

- [ ] **T1 - Lifecycle state model**
  - owner_surface: command-ingest + replay-gate
  - inputs: command envelope, validation result, prior stream status
  - outputs: terminal status + reason_code + reason_detail
  - done_condition: all lifecycle terminal states are emitted with deterministic ordering keys
- [ ] **T2 - Reason code registry**
  - owner_surface: shared contracts package
  - inputs: validation/fault categories and recovery outcomes
  - outputs: versioned reason-code map with strict enum checks
  - done_condition: runtime rejects unknown reason codes at compile-time or startup validation
- [ ] **T3 - Idempotency ledger enforcement**
  - owner_surface: command gateway persistence
  - inputs: stream_id, idempotency_key, payload_hash
  - outputs: replay-safe prior result or conflict rejection
  - done_condition: duplicate same-hash and duplicate conflict paths are deterministic
- [ ] **T4 - Checkpoint hash verifier**
  - owner_surface: replay and state checkpoint service
  - inputs: expected checkpoint hash, actual post-replay hash
  - outputs: verification event + divergence alert status
  - done_condition: mismatch always blocks commit and produces deterministic recovery branch
- [ ] **T5 - Recovery state machine**
  - owner_surface: recovery orchestrator
  - inputs: terminal reason code, stream context, checkpoint availability
  - outputs: recovering/compensating/replaying/verified/resumed transitions
  - done_condition: every transition is idempotent and correlation-linked
- [ ] **T6 - Bulkhead and breaker policy**
  - owner_surface: stream workers + dependency adapters
  - inputs: stream load and dependency health signals
  - outputs: isolated defer/fail behavior per stream
  - done_condition: one poisoned stream cannot starve global processing
- [ ] **T7 - Determinism telemetry**
  - owner_surface: observability + replay audit
  - inputs: gate decisions, reason codes, hash outcomes
  - outputs: deterministic trace records suitable for replay audits
  - done_condition: replay trace reconstruction is possible without inference
- [ ] **T8 - Handoff artifact bundle**
  - owner_surface: roadmap + docs handoff
  - inputs: task outputs T1-T7
  - outputs: explicit handoff pack checklist for junior implementation
  - done_condition: handoff bundle is link-complete and validator-readable

## Determinism gate execution plan

1. **S1 -> T1/T2:** lock lifecycle + reason-code registry before mutation gates.
2. **S2 -> T3:** implement idempotency lookup and conflict enforcement at command ingress.
3. **S3 -> T4:** wire checkpoint verification around replay and rollback windows.
4. **S4 -> T5:** add orchestration transitions for compensation and replay resumption.
5. **S5 -> T6/T7:** enforce isolation policies and emit deterministic telemetry traces.
6. **S6 -> T8:** package handoff-ready artifacts and cross-link test evidence.

## Reason code mapping table (v1)

| reason_code | trigger | expected terminal_state |
| --- | --- | --- |
| VAL_SCHEMA | schema invalid or field missing | rejected |
| VAL_AUTH | authority check fails | rejected |
| PRECONDITION_MISSING | causal prerequisite not met | deferred |
| DUPLICATE_SAME | duplicate idempotency key with same payload hash | replayed |
| DUPLICATE_CONFLICT | duplicate idempotency key with different payload hash | rejected |
| DEPENDENCY_TIMEOUT | downstream dependency exceeds timeout budget | deferred |
| ROLLBACK_WINDOW_EXCEEDED | required rollback depth exceeds bounded window | rejected |
| COMPENSATION_FAILED | compensation action fails verification | compensated |

## Executable test plan (v0)

- [ ] **R1 - Replay determinism baseline:** same seed + ordered commands => identical post-checkpoint hash.
- [ ] **R2 - Replay divergence block:** hash mismatch after replay produces deterministic block + reason code.
- [ ] **R3 - Duplicate same-hash path:** same `(stream_id,idempotency_key,payload_hash)` returns prior deterministic result (`replayed`).
- [ ] **R4 - Duplicate conflict path:** same key with changed hash returns `DUPLICATE_CONFLICT` and no mutation.
- [ ] **R5 - Deferred dependency timeout:** transient timeout produces `DEPENDENCY_TIMEOUT` and deterministic retry envelope.
- [ ] **R6 - Rollback window breach:** forced deep rollback returns `ROLLBACK_WINDOW_EXCEEDED` and blocks replay continuation.
- [ ] **R7 - Compensation chain success:** compensation transition reaches `verified` with stable correlation IDs.
- [ ] **R8 - Compensation chain failure:** failed compensation produces `COMPENSATION_FAILED` and deterministic terminal event.

## Acceptance criteria (gated)

- [ ] **A1:** Lifecycle and reason-code registry implemented (T1/T2) and validated by R3/R4/R5.
- [ ] **A2:** Idempotency + checkpoint verification enforce deterministic replay safety (T3/T4) validated by R1/R2/R6.
- [ ] **A3:** Recovery orchestration and isolation prevent global corruption (T5/T6/T7) validated by R5/R7/R8.
- [ ] **A4:** Handoff pack complete and linkable for junior implementation (T8) with traceable test matrix references.

## Handoff pack

- [ ] Decomposition present: `Task decomposition (v1)` (T1-T8).
- [ ] Ordered implementation sequence present: `Determinism gate execution plan` (S1-S6).
- [ ] Test matrix present: `Executable test plan (v0)` (R1-R8).
- [ ] Objective-to-acceptance linkage present: `Acceptance criteria (gated)` (A1-A4).
