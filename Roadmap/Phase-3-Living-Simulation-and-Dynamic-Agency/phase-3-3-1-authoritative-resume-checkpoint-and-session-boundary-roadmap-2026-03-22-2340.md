---
title: Phase 3.3.1 — Authoritative resume checkpoint + session boundary (vs tick boundary)
roadmap-level: tertiary
phase-number: 3
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-22
tags: [roadmap, genesis-mythos-master, phase, persistence, session, checkpoint, replay]
para-type: Project
subphase-index: "3.3.1"
blocked_on_decisions:
  - D-032
  - D-043
  - D-047
handoff_readiness: 90
handoff_readiness_scope: "Opening tertiary for Phase 3.3 — unifies snapshot lineage (1.1.4), tick commit cursor (3.1.1), rehydration (1.1.5); normative draft until ResumeBundle field row + golden resume row"
execution_handoff_readiness: 58
handoff_gaps:
  - "Literal **`ResumeCheckpoint_v0` / `PersistenceBundle_v0`** field table + wikilink to **3.1.1** `TickCommitRecord_v0` columns — TBD until **D-032** replay header fork"
  - "Golden **resume preflight** row (dual-hash + row_version + profile id) — TBD until **D-043** preimage freeze"
links:
  - "[[phase-3-3-persistence-cross-session-consequence-propagation-roadmap-2026-03-21-2348]]"
  - "[[phase-1-1-4-state-snapshot-lineage-and-authoritative-rollback-ledger-roadmap-2026-03-19-1201]]"
  - "[[phase-1-1-5-idempotent-state-rehydration-contract-and-cold-start-consistency-roadmap-2026-03-19-1208]]"
  - "[[phase-3-1-1-deterministic-tick-epoch-and-hash-preimage-boundaries-roadmap-2026-03-22-0015]]"
  - "[[decisions-log]]"
  - "[[distilled-core]]"
---

## Phase 3.3.1 — Authoritative resume checkpoint + session boundary

**TL;DR:** Define how a **simulation stream** resumes across **OS/process session** boundaries without breaking Phase **1.1.4** lineage, **1.1.5** rehydration idempotency, or **3.1.1** tick-commit preimage. One **authoritative head** per `stream_id` — never two competing truths (snapshot anchor vs tick tail).

### Session vs tick (normative)

- **Tick boundary:** Logical time advance per **3.1.1**; ends in a **terminal-published** `TickCommitRecord_v0` (and barrier alignment per **2.1.3**).
- **Session boundary:** Host process / lobby / client lifecycle edge — **not** a tick. Persist must record **last committed tick** + **lineage head** + **bundle versions**; load must **preflight** before mutating live hashed observables.

### `ResumeCheckpoint_v0` (draft shape)

| Field | Role |
|--------|------|
| `stream_id` | Stable id for the simulation continuity scope (normative meaning: **one** chosen — dungeon instance vs save slot vs shard — document in **D-047**) |
| `snapshot_lineage_head_id` | Pointer into **1.1.4** DAG / latest authoritative snapshot node |
| `last_committed_tick_epoch` | Monotonic cursor from **3.1.1** |
| `replay_row_version` | Carried from **3.1.1** / registry plan (**D-043**) |
| `serialization_profile_id` | Aligns **3.1.6** / **D-037** facet manifest when present |
| `barrier_publish_ref` | Ensures no async partial publish is in preimage (**2.1.3**) |
| `ledger_tail_ref` | Optional fast path to ordered tail after snapshot baseline (**1.1.5** replay slice) |

### Algorithm sketch — resume preflight

1. Read `ResumeCheckpoint_v0` + frozen build/RNG policy slice (**D-027**).
2. Verify **compatibility matrix** (row version, profile, player cardinality if in preimage).
3. Run **dual-hash preflight** (`state_hash` / `metadata_hash` families per **1.1.4** spirit) on restored baseline + tail.
4. If mismatch: **fail-closed** with reason codes (no silent upcast of hashed observables unless explicit migration note + version bump).
5. **Rehydrate** idempotently per **1.1.5**; **suppress or idempotent-route** side effects during replay rebuild (event-sourcing hygiene).

### Interface table (upstream / downstream)

| Partner | Contract |
|---------|----------|
| **1.1.4** | Snapshot parent/child lineage + rollback preflight |
| **1.1.5** | Cold/warm boot, compatible baseline + ordered tail |
| **3.1.1** | `TickCommitRecord_v0` cursor + preimage fields |
| **3.1.5–3.1.6** | Apply ledger checksum + observable bridge at last committed tick |
| **3.2.x** | Regen lane must be **closed** before checkpointing tick (**3.2.3** ordering) |

### Tasks

- [ ] Freeze **`stream_id`** semantics (one paragraph in [[decisions-log]] — pairs **D-047**).
- [ ] Draft **fail-closed reason codes** for resume mismatch (`RESUME_PROFILE_MISMATCH`, `RESUME_TICK_CURSOR_GAP`, `RESUME_LINEAGE_BREAK` — reconcile with existing taxonomies).
- [ ] Add **golden row stub** for “resume from checkpoint + N tick tail” (blocked on **D-032** / **D-043**).
- [x] Link **secondary** [[phase-3-3-persistence-cross-session-consequence-propagation-roadmap-2026-03-21-2348]] tertiary spine + Dataview (completed queue **245**).

### Open tasks — explicit deferral (junior-dev traceability)

All four checkboxes above remain **open by design** until upstream gates clear; they are **not** silent TODOs:

| Task | Defer reason | Unblock |
| --- | --- | --- |
| `stream_id` freeze | Operator scope pick + **D-047** body | Log paragraph in [[decisions-log]] |
| Fail-closed reason codes | Taxonomy reconcile vs existing registries | After **D-047** stream_id + **3.2.x** regen codes stable |
| Golden resume row | No literal field row / CI row yet | **D-032** replay header fork + **D-043** preimage freeze |
| Secondary spine / Dataview | — | **Closed** in queue **245** (tertiary spine + Dataview on secondary) |

Until golden + literal row exist, **`execution_handoff_readiness: 58`** stays honest.

### Junior execution order (1:1 task → deferral row)

1. **Freeze `stream_id`** → deferral row “`stream_id` freeze” → unblock via **D-047** operator paragraph.
2. **Fail-closed reason codes** → row “Fail-closed reason codes” → after **D-047** + regen taxonomy stable.
3. **Golden resume row** → row “Golden resume row” → **D-032** + **D-043**.
4. **Secondary spine** → row “Secondary spine / Dataview” → closed queue **245** (task line marked `[x]`).

## Research integration

### Key takeaways

- Model resume as **one authoritative head** per `stream_id`: **snapshot lineage anchor (1.1.4)** plus **last `TickCommitRecord_v0` / replay cursor (3.1.1)**, loaded through **1.1.5 preflight + idempotent rehydrate**.
- **Consequence propagation** must only use **terminal-published** state: barrier publish refs + tick commit rows; **no** silent drift of **hashed observables** without a new committed record.
- **Cold start / resume** must verify **both** `state_hash` and `metadata_hash` families before mutating live sim state (same spirit as rollback preflight in 1.1.4).
- **Replay / migration** paths need explicit **`replay_row_version`** and a small **persistence bundle** (pinned serialization profile, RNG namespace map version, ledger tail refs) so CI and clients agree on preimage.
- **Side effects** during replay/rebuild should be **suppressed** or routed through replay-safe, idempotent handlers (event-sourced replay hygiene).
- **Fixed timestep / lockstep** framing stays the simulation clock contract; session end is **not** a tick.

### Decisions / constraints

- **Constraint:** Session handoff reads only **committed** tick rows + **lineage-valid** snapshots; partial async buffers stay out of preimage until terminal publish (3.1.1 + 2.1.3 alignment).
- **Constraint:** Any schema or row-format change requires a **versioned migration** path (upcast / tolerant reader / snapshot rewrite) — no silent compatibility.
- **Pending decisions:** Exact **ResumeCheckpoint** / **PersistenceBundle** field list; whether “session” is **stream**, **instance**, or **client process**; fail-closed vs upcast policy when bundle versions diverge.

### Links

- [[Ingest/Agent-Research/phase-3-3-1-sim-persistence-cross-session-research-2026-03-22-1830]]
- Vault raw (EventSourcingDB replay excerpt): [[Ingest/Agent-Research/Raw/phase-2-1-5-event-sourcing-replay-idempotent-side-effects-raw-2026-03-20-2346]]

### Sources

- See synthesis note **## Sources** for external URLs (Fowler Event Sourcing, EventSourcingDB replays, Photon Quantum snapshot resume, Gaffer on Games, YoungJu schema-evolution overview).
