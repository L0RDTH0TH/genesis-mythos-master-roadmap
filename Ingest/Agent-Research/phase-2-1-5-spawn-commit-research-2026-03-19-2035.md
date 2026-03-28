---
title: Pre-deepen research — Phase 2.1.5 SpawnCommit / idempotent apply
research_query: "ECS entity command buffer deterministic sort key spawn replay"
linked_phase: Phase-2-1-5
project_id: genesis-mythos-master
created: 2026-03-19
tags: [research, agent-research]
research_tools_used: [web_search]
agent-generated: true
---

# Phase 2.1.5 — deterministic SpawnCommit apply & replay-safe idempotency

Vault context: Phase 2.1.3 defines terminal **ManifestEmit** → **SpawnCommit** barrier; 2.1.4 binds **manifest_hash** to sorted **EntityManifest**. This note adds **industry patterns** for deterministic playback + replay-safe idempotency — **ledger rules in project notes remain authoritative**.

## Synthesis

- **Deferred command buffers (ECS):** Unity’s Entity Command Buffer playback is non-deterministic when recording in parallel jobs, unless you explicitly record **sort keys** and sort commands on playback. Tie-in: SpawnCommit must apply in a single canonical order derived from the phase’s **manifest sort key discipline** (never job schedule order).
- **Deterministic playback:** Unity states that sort keys make playback order deterministic when the recorded keys are independent from scheduling; Unity also plays back commands with larger sort keys after smaller ones. Tie-in: Phase 2.1.5’s “apply order follows **manifest sort key** row-by-row” is the ledger-authored equivalent of ECB sort-key ordering.
- **Idempotent spawn (replay-safe):** Phase 2.1.5 defines replay-safe apply using `spawn_row_stable_id` and `spawn_idempotency_key` (including `spawn_commit_semver`). On a second apply, the expected outcome is **ledger-hit** with **zero new entities** and an identical reason_code `SPAWN_IDEMPOTENCY_REPLAY`. Tie-in: Event replay guidance emphasizes that replay-safe logic should be **idempotent and isolated**, and that side-effecting components must avoid duplicating actions.

## Raw sources (vault)

- [[Ingest/Agent-Research/Raw/phase-2-1-5-unity-entity-command-buffer-playback-sort-keys-raw-2026-03-20-2346.md]]
- [[Ingest/Agent-Research/Raw/phase-2-1-5-event-sourcing-replay-idempotent-side-effects-raw-2026-03-20-2346.md]]

## Terminology mapping (external patterns -> Phase 2.1.5 contract)

| External concept | Phase 2.1.5 exact field/event name | How it informs SpawnCommit |
|---|---|---|
| ECB sort keys for deterministic playback | `manifest_hash` + manifest sort key apply order | Canonical ordering: recorded order must not depend on parallel schedule; SpawnCommit should follow manifest order explicitly. |
| “Larger sort keys after smaller” playback guarantee | `apply_rows_in_manifest_order(...)` | Enforces a single monotonic apply sequence for deterministic structural mutation. |
| Replay-safe, idempotent + isolated side effects | `spawn_idempotency_key` + `SPAWN_IDEMPOTENCY_REPLAY` | Second apply must converge: no duplicate entities, stable reason_code, and replay isolation. |

## Command / event schema sketch (for deepen)

**SpawnCommit ledger record payload (shape):**
- `{ barrier_id, manifest_hash, spawn_batch_id, applied_row_count, terminal_state, reason_code? }`

**Deterministic identity (stable keys):**
- `spawn_row_stable_id := H(stream_id ‖ manifest_hash ‖ cell_coord ‖ entity_type_id ‖ row_index)`
- `spawn_idempotency_key := (stream_id, spawn_batch_id, spawn_row_stable_id, spawn_commit_semver)`

**Deterministic events (reason codes):**
- `spawn_commit_applied.event` on successful apply
- `spawn_commit_denied.event` on precondition failure
- Reason code expectation on second apply: `SPAWN_IDEMPOTENCY_REPLAY` (or silent no-op per the phase note’s semantics)

## Replay harness patterns (tie-in to `replay_spawn_commit`)

- **Golden vectors per `spawn_batch_id`:** record `cold_world.entity_fingerprint()` (and/or component fingerprint tuples) as the expected “golden” output for deterministic comparison.
- **Ordered commit replay:** the harness must apply commit records in ledger order and assert the terminal `manifest_hash` matches the expected value before applying rows.
- **Double-apply regression:** apply the same `SpawnCommit` twice; the second pass must produce a **ledger-hit** outcome with **zero new entities** and the expected `SPAWN_IDEMPOTENCY_REPLAY` reason_code.
- **Replay-safe side effects:** the harness should treat entity construction as pure w.r.t. test assertions; any side effects should be replay-isolated and deduplicated to avoid inconsistent external effects during the second pass.

## Task decomposition (external -> engineering checklist)

1. Add an explicit deterministic ordering key for deferred structural commands (tie it to Phase 2.1.5 manifest order rather than job scheduling).
2. Implement / document stable identity + ledger-hit behavior using:
   - `spawn_row_stable_id`
   - `spawn_idempotency_key` (including `spawn_commit_semver`)
   - `SPAWN_IDEMPOTENCY_REPLAY` expectation
3. Add replay harness coverage focused on:
   - ordered commit replay assertions (manifest_hash check + apply ordering)
   - golden vector matching (entity identity tuple/component fingerprint comparison)
   - double-apply regression (ledger-hit + zero new entities)

## Sources

- [Unity — Entity Command Buffer playback (sort keys + deterministic ordering)](https://docs.unity3d.com/Packages/com.unity.entities@1.0/manual/systems-entity-command-buffer-playback.html)
- [EventSourcingDB — Optimizing Event Replays (replay-safe idempotent + isolated logic)](https://docs.eventsourcingdb.io/best-practices/optimizing-event-replays/)
- [Bevy — idempotent singleton spawn discussion (background / not authoritative for schema)](https://github.com/bevyengine/bevy/issues/20321)
