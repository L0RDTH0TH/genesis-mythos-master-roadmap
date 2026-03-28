---
title: Phase 3.1.5 — Persistent State Storage and Replay Boundaries
roadmap-level: tertiary
phase-number: 3
subphase-index: "3.1.5"
project-id: genesis-mythos-master
status: archived
priority: high
progress: 0
created: 2026-03-09
tags: [roadmap, genesis-mythos-master, phase, subphase]
para-type: Archive
links:
  - "[[Phase-3-1-Tick-Based-Simulation-Layer-Roadmap-2026-03-09-1405]]"
---

## Phase 3.1.5 — Persistent State Storage and Replay Boundaries

Define what is committed each tick, rollback scope, and replay boundaries so the simulation layer supports deterministic replay and safe save/load. Mid-technical: interfaces and algorithm sketches; runs after tick Phase 4 (persistence flush) or as part of it.

### Tasks

- [ ] **What is committed each tick**
  - [ ] Define the minimal state blob written per tick: clock (tick index, sim time, session id), environment snapshot (weather, region state), NPC/schedule state, faction/reputation deltas or full snapshot. No full world dump — only deltas or compressed summary where possible.
  - [ ] Commit boundary: after tick Phase 4 (or async after N ticks); one commit = one atomic write (e.g. append to log or overwrite checkpoint). Contract: consumers see consistent state at tick boundaries only.
  - [ ] Read-only API for "state at tick T": `get_state_at_tick(tick_index)` returns immutable snapshot for replay or inspection; no direct write from game logic.
- [ ] **Rollback scope**
  - [ ] Define rollback granularity: full world to tick T, or per-system (e.g. rollback only faction state). Document scope and cost; prefer narrow rollback (e.g. last N ticks) for UX (undo) vs full replay for validation.
  - [ ] Rollback contract: restore state from committed snapshot at T; re-run tick driver from T+1 with same inputs ⇒ same outcome (determinism). If inputs (e.g. DM overwrites) are not logged, rollback may be partial or undefined.
  - [ ] DM overwrites: if applied mid-session, define whether they are appended to a "patch" layer (replay = base state + patches) or baked into next commit; affects rollback semantics.
- [ ] **Replay boundaries**
  - [ ] Replay = run simulation from tick 0 (or from last full checkpoint) with same seed and same event stream. Boundary: replay stops at "last committed tick" or at a user-chosen tick for debugging.
  - [ ] Event stream: optional ordered log of non-deterministic inputs (e.g. player actions, DM commands) so replay can re-apply them. Without it, replay is deterministic only for the portion that has no external input.
  - [ ] Lightweight preview (2D map, headless): consumes same committed state; no need to re-run full 3D. Document that simulation state is the source of truth; rendering is a consumer.
- [ ] **Integration with tick phases**
  - [ ] Persistence flush runs as tick Phase 4 (after environment, NPCs, factions). Same tick boundary as Phase 3.1.1; all Phase 3.1 subsystems contribute read-only state to the commit.

### Interface sketch

- **PersistenceCommit** (internal):
  - `commit_after_tick(tick_index, state_blob): void` — called by tick driver at Phase 4; atomic write.
  - `get_state_at_tick(tick_index): StateSnapshot` — read-only; for replay or rollback.
- **Rollback** (optional API):
  - `rollback_to_tick(tick_index): void` — restore state from snapshot; caller must re-invoke tick driver from T+1 if continuing.
- **Replay**: run tick driver from 0 (or checkpoint) with same seed; optionally feed event stream; stop at boundary tick.

### Invariants

- Commits occur only at tick boundaries (after Phase 4); no mid-tick commit from game logic.
- Same seed + same event stream up to tick T ⇒ same state at T (deterministic replay).
- State at tick T is immutable after commit; no in-place mutation of committed snapshots.
