---
title: Phase 3.2.3 — Overwrite Application Order and Persistence
roadmap-level: tertiary
phase-number: 3
subphase-index: "3.2.3"
project-id: genesis-mythos-master
status: archived
priority: high
progress: 0
created: 2026-03-09
tags: [roadmap, genesis-mythos-master, phase, subphase]
para-type: Archive
links:
  - "[[Phase-3-2-DM-Overwrites-Re-Generation-Roadmap-2026-03-09-1515]]"
  - "[[Phase-3-1-5-Persistent-State-Replay-Boundaries]]"
---

## Phase 3.2.3 — Overwrite Application Order and Persistence

Specify overwrite application order, patch layer vs baked-into-commit semantics, and rollback/replay implications. Integrates with Phase 3.1.5 (Persistent State and Replay Boundaries). Mid-technical: interfaces and algorithm sketches.

### Tasks

- [ ] **Application order**
  - [ ] Define deterministic order for applying overwrites when resolving sim state: e.g. by domain (token → weather → event → npc_directive), then by timestamp within domain. Document so replay and rollback produce identical state.
  - [ ] Conflict policy: same key (e.g. same token id) overwritten multiple times ⇒ last-write-wins; order is defined by (domain, timestamp). No merge semantics for overwrites.
  - [ ] Read path: `SimStateView` (Phase 3.2.1) applies overlay in this order on top of base; cache or incremental apply if performance requires.
- [ ] **Patch layer vs baked commit**
  - [ ] **Patch layer (default):** Overwrites live in a separate overlay; not written into the tick-commit blob. On load: base (from last gen or checkpoint) + overlay. Rollback to tick T: base at T + overlay at T (overlay must be persisted per-tick or snapshotted at commit).
  - [ ] **Baked commit (optional policy):** On "commit overwrites", overlay is merged into a new baseline; next save stores that baseline. Replay of pre-commit ticks uses old baseline; replay of post-commit uses new. Document when to use which (e.g. commit at session end or on explicit DM "save overwrites").
  - [ ] Persistence format: overlay serialized as ordered list of (domain, id, payload, timestamp); stored with save-game or in a sidecar so base + overlay can be restored.
- [ ] **Rollback and replay implications**
  - [ ] Rollback (Phase 3.1.5): if overwrites are patch layer, rollback to tick T restores overlay state at T (requires overlay history or snapshot per tick). If overwrites are not logged per tick, rollback may reset overlay to last committed overlay only.
  - [ ] Replay: replay runs sim from tick 0 (or checkpoint) with same event stream; overlay at replay start must be applied so state matches. For "replay from tick T", overlay at T must be available (snapshot or replay of overlay edits).
  - [ ] Edge case: DM applies overwrite at tick 100; user rolls back to tick 50. Overwrites after 50 are discarded or reverted so rollback state is consistent.
- [ ] **Integration with Phase 3.1.5**
  - [ ] Tick commit: include overlay snapshot (or overlay delta) in tick commit if patch layer is used, so rollback has overlay at that tick. Alternatively, overlay committed only on explicit "commit overwrites" (fewer commits, coarser rollback).
  - [ ] Replay boundary: replay produces same base + same overlay application order; overlay content may be replayed from logged DM commands or from persisted overlay snapshot at boundary tick.

### Interface sketch

- **OverwriteLayer** (persisted):
  - `serialize(): bytes` — ordered list (domain, id, payload, timestamp) for save/load.
  - `apply_over(base_state, order): state` — apply overlay in `order` (domain + timestamp) to base; return merged state view.
- **Commit policy** (config or enum):
  - `patch_only` — overlay never baked; every tick (or every N ticks) persist overlay snapshot for rollback.
  - `commit_on_explicit` — overlay baked only when DM commits; rollback to pre-commit uses previous baseline + overlay snapshot at that time.
- **Rollback contract:** `restore(tick T)` = base_at(T) + overlay_at(T); overlay_at(T) from overlay history or from last commit before T.
