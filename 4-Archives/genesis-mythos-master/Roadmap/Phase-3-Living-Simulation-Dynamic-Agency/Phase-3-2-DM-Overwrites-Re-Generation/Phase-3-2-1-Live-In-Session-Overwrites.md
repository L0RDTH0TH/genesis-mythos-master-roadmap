---
title: Phase 3.2.1 — Live In-Session Overwrites
roadmap-level: tertiary
phase-number: 3
subphase-index: "3.2.1"
project-id: genesis-mythos-master
status: archived
priority: high
progress: 0
created: 2026-03-09
tags: [roadmap, genesis-mythos-master, phase, subphase]
para-type: Archive
links:
  - "[[Phase-3-2-DM-Overwrites-Re-Generation-Roadmap-2026-03-09-1515]]"
---

## Phase 3.2.1 — Live In-Session Overwrites

Define which simulation state is writable by the DM in-session without triggering re-generation. Contracts and APIs for tokens, weather, events, and NPC whispers. Mid-technical: interfaces and algorithm sketches.

### Tasks

- [ ] **Writable state surface**
  - [ ] Enumerate DM-writable state: token positions, weather overrides (current conditions), one-off event triggers, NPC whisper / directive injection. Document what is **not** writable (terrain, biomes, POI layout, generation seeds).
  - [ ] Define per-domain contracts: e.g. token move = position + rotation only; weather = override mask + expiry; events = id + payload; NPC = entity id + directive enum + optional params.
  - [ ] Specify persistence: overwrites as patch layer (applied on load, not baked into world gen); rollback = revert patch layer to last commit.
- [ ] **APIs and hooks**
  - [ ] DM overwrite API: `apply_overwrite(domain, key, value)` or domain-specific (e.g. `move_token(id, position)`). All overwrites timestamped and attributed to session/DM.
  - [ ] Simulation read path: sim state = base_gen_state + overlay(overwrites). Order: base from last gen/load, then overlay applied in deterministic order (e.g. by domain, then by timestamp).
  - [ ] Hooks for UI/tools: list overwrites by domain; support "revert this overwrite" and "commit overwrites to checkpoint" (saves overlay as new baseline for replay).
- [ ] **Replay and persistence boundaries**
  - [ ] Overwrites are part of session state: saved with save-game; replay replays base + overlay so DM tweaks are visible in VOD/replay.
  - [ ] Distinguish "live overlay" (current session) vs "committed overlay" (checkpoint): committed can be used as baseline for next session; live is ephemeral until commit.
  - [ ] Integration with Phase 3.1.5: replay boundary = tick index; overwrites before that tick are part of replay; overwrites after are "live" and not replayed (or replayed as post-session edits per spec).

### Interface sketch

- **OverwriteStore** (session-scoped):
  - `apply(domain, id, payload): void` — add or update one overwrite; domain ∈ { token, weather, event, npc_directive }.
  - `revert(domain, id): void` — remove one overwrite.
  - `list(domain?): Overwrite[]` — list overwrites, optionally by domain.
  - `commit(): void` — promote current overlay to committed baseline; clear live overlay (or merge per policy).
- **SimStateView** (read-only for simulation):
  - `get_token_position(id): Vec3` — base + overlay.
  - `get_weather(): WeatherState` — base + overlay (override mask).
  - `get_npc_directive(id): Directive?` — from overlay if present.
- **Persistence**: OverwriteStore serialized with save; on load, overlay applied after base; replay uses same overlay up to replay boundary tick.
