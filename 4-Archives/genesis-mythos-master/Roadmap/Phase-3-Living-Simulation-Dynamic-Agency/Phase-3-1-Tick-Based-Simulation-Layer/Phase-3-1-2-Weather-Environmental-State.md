---
title: Phase 3.1.2 — Weather and Environmental State
roadmap-level: tertiary
phase-number: 3
subphase-index: "3.1.2"
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

## Phase 3.1.2 — Weather and Environmental State

Specify weather and environmental state so the simulation layer can drive cycles, region-scoped variables, and effects on paths and mood. Mid-technical: interfaces and algorithm sketches aligned with the tick model (Phase 3.1.1).

### Tasks

- [ ] **Weather cycles**
  - [ ] Define weather state per region: type (clear, rain, storm, snow, fog), intensity, duration; optional seasonal modifiers.
  - [ ] Tick-driven updates: advance weather phase each tick (or every N ticks); transitions (e.g. clear → rain) use simple state machine or probability table.
  - [ ] Expose read-only API for consumers (rendering, pathfinding, NPC mood): `get_weather(region_id)`, `get_weather_at(tick_index)` for replay.
- [ ] **Region-scoped variables**
  - [ ] Environmental state: temperature, humidity, time-of-day (from sim clock); per-region or global with region overrides.
  - [ ] Persist only what is needed for replay: last tick index + compact state blob; avoid storing full history per region.
- [ ] **Effect on paths and mood**
  - [ ] Path cost modifiers: e.g. rain increases cost on unpaved tiles; snow blocks or slows certain paths. Document as additive/multiplicative modifiers to a pathfinding cost function.
  - [ ] Mood/atmosphere: map weather + time-of-day to a scalar or enum (e.g. tense, calm, bleak) for NPC behavior or ambient triggers; optional link to intent hooks.
- [ ] **Integration with tick phases**
  - [ ] Weather and environmental state advance in tick Phase 1 (environment), before NPC and faction phases. Same tick boundary contract as Phase 3.1.1.

### Interface sketch

- **WeatherState** (per region, read-only view):
  - `weather_type(): enum` (clear, rain, storm, snow, fog)
  - `intensity(): float`
  - `region_id(): string`
- **EnvironmentState** (optional global or per-region):
  - `temperature(): float`
  - `time_of_day(): SimTime` (from SimClock)
- **Path cost hook**: `get_weather_path_modifier(region_id, segment): float` — consumed by pathfinding; 1.0 = no modifier.

### Invariants

- Weather and environment advance only in tick Phase 1; no writes from game logic outside the tick driver.
- Same tick index ⇒ same weather/environment state for deterministic replay.
