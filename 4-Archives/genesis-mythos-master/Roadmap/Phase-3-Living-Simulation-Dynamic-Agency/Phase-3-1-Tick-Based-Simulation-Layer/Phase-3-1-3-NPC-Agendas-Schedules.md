---
title: Phase 3.1.3 — NPC Agendas and Schedules
roadmap-level: tertiary
phase-number: 3
subphase-index: "3.1.3"
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

## Phase 3.1.3 — NPC Agendas and Schedules

Specify NPC agendas and schedules: availability, goals, interaction windows, and links to intent hooks. Mid-technical: interfaces and algorithm sketches; runs in tick Phase 2 (after environment).

### Tasks

- [ ] **Availability and schedules**
  - [ ] Per-entity or per-archetype schedule: active time windows (e.g. ticks or sim-time ranges), location constraints, state (idle, busy, in-dialogue).
  - [ ] Tick-driven update: each tick Phase 2, advance schedule state; availability recomputed from current sim time and location.
  - [ ] Expose read-only API for systems that need "can this NPC be interacted with now?": e.g. `is_available(entity_id, tick)`, `get_next_window(entity_id)`.
- [ ] **Goals and agendas**
  - [ ] Lightweight goal representation: current goal id or enum, priority, optional target (location, entity); no full AI stack — just state that drives behavior hooks.
  - [ ] Agendas as ordered or weighted list of goal templates; current goal selected by rules (e.g. time of day, weather, reputation). Link to intent hooks where relevant (player/DM intents that inject or modify goals).
- [ ] **Interaction windows**
  - [ ] Define when an NPC can enter dialogue or scripted interaction: time window, cooldown after last interaction, preconditions (e.g. reputation threshold). Stored as contract per entity type or instance.
  - [ ] Link to intent hooks: player backstory/quest intents can attach "interaction window modifiers" (e.g. this NPC is available during quest X). Resolver merges base schedule with intent-derived overrides.
- [ ] **Integration with tick phases**
  - [ ] NPC and agenda updates run in tick Phase 2 (after environment). Same tick boundary as Phase 3.1.1; consume WeatherState/EnvironmentState as read-only.

### Interface sketch

- **NPCSchedule** (read-only view):
  - `is_available(entity_id, at_tick?): bool`
  - `get_current_goal(entity_id): GoalRef`
  - `get_interaction_window(entity_id): TimeWindow | null`
- **AgendaState**: current goal stack or single goal + metadata; written only by tick Phase 2 logic.
- **Intent hook attachment points**: e.g. `register_availability_modifier(entity_id, modifier)` — applied when resolving `is_available`.

### Invariants

- Agenda and schedule state advance only in tick Phase 2; no writes from game logic outside the tick driver.
- Same tick index ⇒ same NPC availability and current goal for deterministic replay (modulo intent overrides that are themselves deterministic from seed + inputs).
