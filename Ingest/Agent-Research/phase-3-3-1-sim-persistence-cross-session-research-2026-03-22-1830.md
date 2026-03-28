---
title: Research — Phase 3.3.1 persistence across sessions (simulation + lineage + tick commits)
research_query: "Deterministic simulation persistence: rollback lineage, tick commits, rehydration, session boundaries, replay migrations"
linked_phase: Phase-3-3-1
project_id: genesis-mythos-master
created: 2026-03-22
tags: [research, agent-research, genesis-mythos-master, persistence, replay]
agent-generated: true
research_tools_used: [web_search, mcp_web_fetch]
research_escalations_used: 0
raw_sources:
  - "[[Ingest/Agent-Research/Raw/phase-2-1-5-event-sourcing-replay-idempotent-side-effects-raw-2026-03-20-2346.md]]"
---

# Phase 3.3.1 — Deterministic persistence across sessions (synthesis)

**Scope:** Tie together **Phase 1.1.4** (snapshot lineage + rollback ledger), **Phase 3.1.1** (`TickCommitRecord_v0` + hash preimage), and **Phase 1.1.5** (cold-start rehydration) for **Phase 3.3** session semantics. Complements vault stubs; does not duplicate normative interfaces already in those phase notes.

## 1. Single continuity model (three layers)

| Layer | Role in cross-session story |
|-------|-----------------------------|
| **Snapshot lineage (1.1.4)** | Authoritative **anchors** in time: `snapshot_id`, `parent_snapshot_id`, dual hash (`state_hash`, `metadata_hash`). Rollback/restore is **stream-scoped** and **preflight-verified** before mutating live state. |
| **Tick commit stream (3.1.1)** | Fine-grained **logical time** inside a run: monotonic `tick_epoch`, `TickCommitRecord_v0` rows that feed replay/golden CI. This is the **primary journal** for “what the simulation admitted as committed” per tick. |
| **Rehydration (1.1.5)** | **Cold/warm boot** path: pick a **compatible** snapshot baseline, load ordered replay slice `(from_tick, to_tick)`, run `preflight_verify`, then `rehydrate` with idempotent command ids. |

**Integration rule:** Treat **session resume** as *either* “restore snapshot + replay tail of tick commits/events” *or* “continue from last `TickCommitRecord` cursor + ledger tail ref,” but **never** both ambiguously—pick one **authoritative head** per `stream_id` and record it in a **`ResumeCheckpoint`**-style structure (name aligned with 1.1.5).

[Source: Event Sourcing (Martin Fowler)](https://martinfowler.com/eaaDev/EventSourcing.html)

## 2. Session boundary semantics

- **End of session (persist):** Persist (a) last committed **snapshot pointer** *or* full snapshot payload per retention policy, (b) **last `tick_epoch`** and **tail of `TickCommitRecord_v0` / replay row version**, (c) **manifest_or_ledger_tail_ref** and **barrier_publish_ref** from 3.1.1 so async work is not “half published.”
- **Start of session (load):** Load **frozen config slice** (build id, schema versions, RNG policy) needed for determinism; reject or migrate if **compatibility matrix** fails (see §5).
- **Process boundary vs tick boundary:** OS/process exit is **not** a tick. A session may span many ticks; conversely, one tick must not span conflicting writer roles without barrier completion (per Phase 2.1.3 alignment in 3.1.1).

Industry pattern: commercial deterministic engines treat **snapshots as serialized frame/tick state** with explicit **initial tick** when resuming online play, and warn when **timer / player-count** assumptions change—useful analogy for documenting **hard rejects** when resume metadata does not match.

[Source: Quantum 3 — Starting From Snapshot](https://doc.photonengine.com/quantum/current/manual/game-session/starting-from-snapshot)

## 3. Consequence propagation without silent drift

**Goal:** No change to **hashed observable state** crosses a session without appearing in **committed** artifacts.

1. **Allow-listed preimage only** — Same as 3.1.1: only **terminal publish** surfaces enter `TickCommitRecord_v0` / observable hash. Session handoff reads **only** those commits + snapshot lineage, not ephemeral buffers.
2. **Dual-hash parity** — On resume, compare **both** `state_hash` and `metadata_hash` families (1.1.4 + 1.1.9 harness themes). Metadata drift (e.g. forgotten serialization profile) is a first-class failure, not a silent fork.
3. **Idempotent rehydration** — Repeated resume with same idempotency key must yield identical observable outcome (1.1.5 invariants). Prevents “double apply” of consequences when clients retry.
4. **Side-effect isolation on replay** — When rebuilding or migrating, replay handlers must **not** emit external side effects; distinguish **live** vs **replay** mode so consequence propagation stays **internal** to ledger + snapshots.

[Source: Optimizing Event Replays — EventSourcingDB](https://docs.eventsourcingdb.io/best-practices/optimizing-event-replays/)  
(Vault raw: [[Ingest/Agent-Research/Raw/phase-2-1-5-event-sourcing-replay-idempotent-side-effects-raw-2026-03-20-2346.md]])

## 4. Lockstep / determinism reminders (already in vault)

- **Fixed timestep** logical advance decoupled from frame delta; replay must not depend on variable `dt` display.
- **Lockstep:** identical inputs + deterministic core ⇒ identical state; checksums validate simulation during replay harnesses.

[Source: Deterministic Lockstep](https://gafferongames.com/post/deterministic_lockstep/)  
[Source: Fix Your Timestep](https://gafferongames.com/post/fix_your_timestep/)

## 5. Versioned migrations of replay / save state

Industry event-sourcing practice (summarized):

| Strategy | Use when | Risk |
|----------|----------|------|
| **Tolerant reader / weak schema** | Additive fields only | Breaks on renames/removals |
| **Upcasting (on read)** | Old events remain immutable bytes; translate to current model at replay | Must preserve bijective mapping per version |
| **Snapshot + compact** | Long streams; replay from snapshot + tail | Snapshot **schema version** must migrate in lockstep with event schema |
| **Parallel replay for projections** | Large rebuilds | Ordering assumptions across shards must match Phase 2.1.3 (`shard_sequence` from lattice, not scheduler) |

**Concrete hooks for Genesis Mythos:**

- Carry **`replay_row_version`** (already stubbed in 3.1.1) on every persisted tick row **and** on snapshot manifests.
- Define **`PersistenceBundle_v0`** (name TBD) that pins: `snapshot_lineage_head_id`, `last_tick_epoch`, `replay_row_version`, `serialization_profile_id`, `rng_namespace_map_version`.
- Migration pipeline: **detect** bundle version → **upcast** snapshot + tick tail **or** fail closed with reason code (align with `PAYLOAD_HASH_DRIFT` / `TICK_PREIMAGE_DRIFT` taxonomy).

[Source: Event Sourcing production patterns — schema evolution / snapshotting (overview)](https://www.youngju.dev/blog/architecture/2026-03-07-architecture-event-sourcing-cqrs-production-patterns.en)

## 6. Gaps / TBD for Phase 3.3 deepen

- Exact **ResumeCheckpoint** field list vs 1.1.5 `publish_resume_checkpoint` (naming + JSON shape).
- Whether **session** is 1:1 with **client process**, **dungeon instance**, or **stream_id** (likely stream-scoped).
- **Multi-writer** resume when DM + sim both mutate—ordering vs 3.1.1 barrier refs.

## Raw sources (vault)

- [[Ingest/Agent-Research/Raw/phase-2-1-5-event-sourcing-replay-idempotent-side-effects-raw-2026-03-20-2346.md]] (EventSourcingDB replay + side effects; URL normalized in Raw-Index)

## Sources

- https://martinfowler.com/eaaDev/EventSourcing.html
- https://docs.eventsourcingdb.io/best-practices/optimizing-event-replays/
- https://doc.photonengine.com/quantum/current/manual/game-session/starting-from-snapshot
- https://gafferongames.com/post/deterministic_lockstep/
- https://gafferongames.com/post/fix_your_timestep/
- https://www.youngju.dev/blog/architecture/2026-03-07-architecture-event-sourcing-cqrs-production-patterns.en
