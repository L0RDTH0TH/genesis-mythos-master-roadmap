---
title: Phase 2.1.5 — SpawnCommit binding, idempotent entity apply & replay harness
roadmap-level: tertiary
phase-number: 2
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-19
tags: [roadmap, genesis-mythos-master, phase]
para-type: Project
subphase-index: "2.1.5"
handoff_readiness: 91
links:
  - "[[phase-2-1-4-entity-spawn-manifest-density-lattice-spawn-policy-roadmap-2026-03-19-2030]]"
  - "[[phase-2-1-3-deterministic-async-commit-barrier-and-stage-ledger-reconciliation-roadmap-2026-03-19-2000]]"
  - "[[phase-2-1-stage-pipeline-skeleton-seed-to-entity-contracts-roadmap-2026-03-19-1912]]"
  - "[[phase-2-procedural-generation-and-world-building-roadmap-2026-03-19-1101]]"
---

## Phase 2.1.5 — SpawnCommit binding, idempotent entity apply & replay harness

> [!summary] TL;DR
> Define **`SpawnCommit`** as the **only** runtime path that materializes entities from a **terminal** `ManifestEmit` + matching **`manifest_hash`**. Specify **idempotent apply** via **`spawn_idempotency_key`** per manifest row (stable under replay) and a **replay harness** that replays commit records into a cold world and compares **entity identity tuples** + **component fingerprint** to golden vectors.

### Scope

- **Inputs:** `published_output_ref` → terminal `ManifestEmit` ledger row; `EntityManifest` bytes or canonical row iterator; optional `SpawnPolicy` handle for validation-only checks.
- **Outputs:** `SpawnCommit` ledger record(s): `{ barrier_id, manifest_hash, spawn_batch_id, applied_row_count, terminal_state, reason_code? }`; runtime **entity graph** mutations are **side effects** captured only through **post-commit snapshot** hooks (Phase 1 lineage), not ad-hoc spawns.
- **Determinism:** Apply order follows **manifest sort key** (2.1.4) row-by-row; no parallel structural mutation without **ordered commit barrier** equivalent to ECB sort-key discipline from external ECS patterns.

### SpawnCommit preconditions (normative)

1. `manifest_hash` equals `ManifestEmit.manifest_hash` on the referenced terminal row (2.1.3).
2. `barrier_id` matches the reconciled barrier for that emit (2.1.3).
3. No prior `SpawnCommit` exists for the same `(stream_id, spawn_batch_id)` unless **idempotent replay** mode (harness or ledger-hit).

### Idempotent entity apply

- **Row key:** `spawn_row_stable_id := H(stream_id ‖ manifest_hash ‖ cell_coord ‖ entity_type_id ‖ row_index)` (hash algorithm frozen per project crypto suite).
- **Ledger key:** `spawn_idempotency_key := (stream_id, spawn_batch_id, spawn_row_stable_id, spawn_commit_semver)` — semver bumps when apply semantics change.
- **Second apply:** must yield **ledger-hit**, **zero new entities**, identical **reason_code** `SPAWN_IDEMPOTENCY_REPLAY` (or silent no-op per D-004 event taxonomy).

### Replay harness (v1 sketch)

```
function replay_spawn_commit(ledger_tail, cold_world):
  for record in ledger_tail.spawn_commits_ordered_by_seq:
    assert record.manifest_hash == expected_terminal_emit_hash
    apply_rows_in_manifest_order(record, cold_world)
  assert cold_world.entity_fingerprint() == golden_fingerprint[record.spawn_batch_id]
```

- **Golden vectors:** stored beside Phase 2.1 harness notes; include **dual-hash** world snapshot after commit when Phase 1 hooks are active.

### Handoff gate note

- **`handoff_readiness: 91`** is **slice-local**. **`advance-phase`** for Phase 2 still requires **rollup ≥ `min_handoff_conf` (93)** on the authored secondary closure artifact (`handoff_gate: true`).

### Tasks

- [ ] Add **`SpawnCommit`** row type to stage ledger schema appendix (cross-link 2.1.3 reason codes).
- [ ] Harness: **double apply** same `SpawnCommit` → second pass **ledger-hit only**, entity count unchanged.
- [ ] Event: emit `spawn_commit_applied.event` or deterministic `spawn_commit_denied.event` with frozen reason codes on precondition failure.

## Research integration

### Key takeaways

- **ECB / command buffers:** deferred structural changes benefit from **explicit sort keys** so playback does not depend on parallel schedule — maps to **manifest row order** as the canonical apply sequence.
- **Deterministic playback** across machines requires ordering independence from thread scheduling — reinforces **no wall-clock / thread id** in spawn path.
- **Idempotent spawn** patterns (singleton / ledger-hit) support **replay-safe** second passes without duplicate entities.

### Decisions / constraints

- **Constraint:** `SpawnCommit` must not accept partial manifests or non-terminal `ManifestEmit` refs (fail-closed; align with D-016).
- **Constraint:** `spawn_row_stable_id` must not include volatile runtime entity ids — only manifest-stable fields.
- **Pending decisions:** whether **multi-cell entity footprints** (2.1.4 pending) allocate **one row vs many** before hash closure; document in 2.1.6 or expand task.

### Links

- [[Ingest/Agent-Research/phase-2-1-5-spawn-commit-research-2026-03-19-2035|Pre-deepen synthesis note]]
- [[phase-2-1-4-entity-spawn-manifest-density-lattice-spawn-policy-roadmap-2026-03-19-2030|Entity manifest parent]]
- [[phase-2-1-3-deterministic-async-commit-barrier-and-stage-ledger-reconciliation-roadmap-2026-03-19-2000|Async barrier]]

### Sources

- [Source: Unity Entities — Entity Command Buffer](https://docs.unity3d.com/Packages/com.unity.entities@1.0/manual/systems-entity-command-buffer.html)
- [Source: Bevy — idempotent spawn discussion](https://github.com/bevyengine/bevy/issues/20321)
