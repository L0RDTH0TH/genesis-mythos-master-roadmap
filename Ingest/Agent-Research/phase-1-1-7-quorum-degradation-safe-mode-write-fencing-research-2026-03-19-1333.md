---
title: Phase 1.1.7 research — Quorum Degradation Safe Mode and Write Fencing
created: 2026-03-19
tags: [research, agent-research, genesis-mythos-master, phase]
para-type: Resource
status: active
project-id: genesis-mythos-master
linked_phase: Phase-1-1-7
research_query: quorum degradation safe mode epoch-scoped write fencing deterministic recovery replay harness
research_tools_used: [web_search]
agent-generated: true
source: research-agent-run
---

## Summary
This synthesis strengthens `Phase-1.1.7` by mapping your v1 write-fence gate to a standard distributed-systems safety pattern: fencing tokens (epoch/lease sequence) validated at the resource boundary, combined with deterministic recovery that is replayable and idempotent.

## 1. Fencing tokens as the safety boundary (not just leader election)
Key failure mode during quorum degradation is the “zombie writer”: a node that believes it still has authority after a pause, timeout, or membership change, and then attempts state-changing writes after a new epoch has already been adopted.

Modern designs address this by using a monotonically increasing fencing token (often derived from a leader lease sequence, generation clock, or transaction/epoch id) and requiring that **every state-changing write** present that token; the storage/resource boundary rejects stale tokens even if the client believes its lease is still valid.

- [Source: How to do distributed locking (Martin Kleppmann)](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html)
- [Source: FencedLock documentation (Hazelcast CP)](https://docs.hazelcast.com/imdg/3.12/cp-subsystem/fencedlock)
- [Source: Spanner paper (leader leases + sequence validation at storage)](https://www.cs.cornell.edu/courses/cs5414/2017fa/papers/Spanner.pdf)

## 2. Mapping this to your v1 gate fields
Your write-fence contract already has the right shape: `activation_epoch`, `cluster_epoch`, `quorum_proof_hash`, `node_role`, and `state_hash`, producing `{allow_write, allow_read, reason_code}`.

To align with fencing-token patterns, treat `activation_epoch` (and/or a derived generation clock for the shard/resource) as the “fencing epoch”, and require that:

- The **resource boundary** (whatever enforces the write gate) compares the incoming fencing epoch against the highest accepted epoch in the local durable state for that resource/shard.
- `quorum_proof_hash` and `state_hash` play the role of “proof that this epoch is actually the one you are recovering to”, so that replay cannot accidentally re-enable writes for a divergent state.
- Denials are deterministic: given the same `activation_epoch` + `cluster_epoch` + `state_hash` + `quorum_proof_hash`, all nodes must converge on the same `reason_code` and terminal state.

Practical implication for your pseudocode: ensure the deny decisions are made before any side effects (including any “optimistic” local state mutations), and include a stable link between the incoming `command_id` / event id and the denial event so operators can audit and re-run safely.

## 3. Deterministic recovery: replayable, idempotent, and checkpoint anchored
Your recovery pseudocode and state machine emphasize deterministic freeze/demote/re-entry gates. The extra research-aligned constraint is to anchor recovery strictly to verified checkpoints:

- replay boundaries are keyed to `last_applied_index` + `state_hash` (your phase note calls out state hash matching); and
- side effects (like “deny event emitted exactly once” and “fence-lift events”) must be idempotent under replay, meaning repeated evaluation with identical inputs must not create conflicting terminal states.

This is the same engineering principle behind reliable retry loops: persistence of the decision + idempotent execution of the decision’s effects.

- [Source: Idempotence is not a medical condition](https://queue.acm.org/detail.cfm?id=2187821)
- [Source: Designing Data-Intensive Applications (fencing / safety concepts)](https://dataintensive.net/)

## 4. Suggested test additions for fencing correctness
To complement your existing matrix, add adversarial scenarios that specifically target fencing and stale writes:

1. Pause/rejoin: simulate a node that times out during `DEGRADED_READ_ONLY` and then reconnects with an old `activation_epoch` and mismatched proof; assert deterministic `EPOCH_MISMATCH` (or `QUORUM_PROOF_MISSING`) and that **no** write-side effects occur.
2. Split-brain attempt: have two “writer candidates” with different epochs both attempt writes; assert the resource boundary rejects the lower fencing epoch and only transitions via your deterministic `QUORUM_RESTORED -> REACTIVATED` lift.
3. Replay idempotence: re-run `evaluate_write_gate` and recovery transition evaluation N times over identical inputs; assert:
   - identical terminal state,
   - stable `reason_code`,
   - exactly one denial or one lift decision per stable event id / command id linkage.

## 5. Step-by-step deterministic dry-run replay procedure (write gate + recovery)
Use a canonical “dry-run” harness that never mutates persistent state; it only computes the next deterministic decision and a decision event record.

1. Inputs (per test run)
   - Select a fixed `{activation_epoch, cluster_epoch, quorum_proof_hash, state_hash}` tuple.
   - Select an ordered sequence of command/event identities: `{command_id, correlation_id, emitted_at_utc}`.
   - Select node role: `leader_candidate | follower | fenced`.
2. Canonical serialization for evaluation
   - Serialize inputs to a canonical byte representation (stable key ordering; fixed number encoding; identical across platforms).
   - Hash the canonical bytes into `inputs_hash`.
3. Dry-run evaluation (idempotent, no side effects)
   - Call `evaluate_write_gate(node_ctx, cluster_ctx)` with the exact input tuple.
   - Record the returned `{allow_write, allow_read, reason_code}` plus the terminal state.
   - Record `decision_event_id` derived deterministically from `{inputs_hash, command_id, event_version}`.
4. Replay N times
   - Re-run the same dry-run evaluation N times.
   - Assert all of the following are identical across replays:
     - `inputs_hash`,
     - `reason_code` + terminal_state,
     - `decision_event_id`,
     - and the computed “side-effect plan” is the same (empty for denials; explicit list for lifts).
5. Divergence check (multi-node)
   - Run the same tuple across multiple nodes (or simulated roles).
   - Assert convergence: every node produces the same decision event record for identical input.
6. Persistence boundary test (resource boundary enforcement)
   - After dry-run, apply only the decision record to the boundary state in a controlled way.
   - Attempt the same write again with an older epoch token; boundary must reject without consulting client-side beliefs.

## 6. Determinism ban/control list (implementers must prohibit or control)
Inside simulation/recovery evaluation code paths, prohibit or tightly control:

- Unseeded randomness (`new Random()`, `System.currentTimeMillis()`, time-based seeds).
- Float operations without canonicalization (see Section 7).
- Iterating over unordered containers (hash maps / sets) without stable ordering guarantees.
- Implicit concurrency ordering (threads/tasks where evaluation outcome depends on scheduling).
- Reading environment-dependent state (locale/timezone, non-deterministic I/O, host CPU feature variability) during gate evaluation.

Every prohibited item should be either:
- removed from evaluation paths, or
- replaced with deterministic equivalents, or
- explicitly captured into the provenance record and normalized.

## 7. Canonical float/serialization policy (concrete, not abstract)
To ensure canonical serialization is stable across languages and platforms:

1. Represent floating state as quantized fixed-point at serialization time
   - Choose a quantization unit `Q` (example: `Q = 1e-6`).
   - Store serialized numeric as `int64(round(value / Q))`.
2. Canonical byte layout
   - Use a single endianness (e.g. little-endian) and fixed-width integer encodings for quantized values.
   - Encode strings in UTF-8 with explicit lengths.
3. Canonical ordering for structures
   - Always sort map keys and arrays deterministically prior to hashing/serialization.
4. Stable event record schema
   - Version the decision-event format (`event_version`) and include it in `decision_event_id` derivation.

This gives you a deterministic `inputs_hash` suitable for replay/idempotence checks.

## 8. Minimal provenance record template (seed + mapping + hashes + diffs)
Use a provenance record attached to every dry-run decision and every applied recovery decision:

- `random_seed` / `stage_seed`: seed used for generation stages (if any).
- `dt_ms`: the fixed timestep used for evaluation (if applicable).
- `intents_hash`: hash of the high-level intent (e.g. requested transition / evaluation intent).
- `from_snapshot_id`: snapshot identifier and version.
- `activation_epoch`, `cluster_epoch`, `quorum_proof_hash`, `state_hash`.
- `inputs_hash` (canonical bytes hash from Section 5).
- `command_id` / `correlation_id` linkage.
- `output_hashes`: hash of computed decision outputs:
  - `decision_event_id`,
  - `allow_write`, `allow_read`,
  - `reason_code`,
  - `terminal_state`.
- `diff_pointers`: pointers to any computed deltas that would be applied (empty for denials).

## Sources
- [Source: How to do distributed locking (Martin Kleppmann)](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html)
- [Source: FencedLock documentation (Hazelcast CP)](https://docs.hazelcast.com/imdg/3.12/cp-subsystem/fencedlock)
- [Source: Spanner paper (leader leases + sequence validation at storage)](https://www.cs.cornell.edu/courses/cs5414/2017fa/papers/Spanner.pdf)
- [Source: Idempotence is not a medical condition](https://queue.acm.org/detail.cfm?id=2187821)
- [Source: Designing Data-Intensive Applications](https://dataintensive.net/)

