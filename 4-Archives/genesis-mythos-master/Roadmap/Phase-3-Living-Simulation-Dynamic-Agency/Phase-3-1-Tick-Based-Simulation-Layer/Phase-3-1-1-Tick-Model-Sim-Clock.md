---
title: Phase 3.1.1 — Tick Model and Global Sim Clock
roadmap-level: tertiary
phase-number: 3
subphase-index: "3.1.1"
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

## Phase 3.1.1 — Tick Model and Global Sim Clock

Define the global simulation clock and tick model so the simulation layer runs independently of rendering, supports pause/resume, and can sync with session or campaign time. Mid-technical: interfaces and algorithm sketches.

### Tasks

- [ ] **Tick model**
  - [ ] Choose fixed vs variable step: fixed (e.g. 100 ms per tick) for deterministic replay; variable for catch-up or performance throttling. Document trade-offs and default.
  - [ ] Define tick boundary contract: what runs in one tick (all subsystems, or phased); ordering guarantees (e.g. weather → NPCs → factions → persistence).
  - [ ] Specify tick id / sequence number: globally monotonic, used for ordering events and replay.
- [ ] **Global sim clock**
  - [ ] Single source of truth: clock value (wall or in-world time), tick index, and session id. No drift between consumers.
  - [ ] Expose read-only API: `get_current_tick()`, `get_sim_time()`, `get_session_id()`. No direct write from game logic; advances only via tick driver.
  - [ ] Pause/resume: clock can be paused (e.g. DM in menu); tick driver skips advance; resume continues from same tick index.
- [ ] **Session and campaign time**
  - [ ] Map tick index to in-world time (e.g. N ticks = 1 day; configurable scale). Optional: separate "session time" (real elapsed) vs "campaign time" (in-world).
  - [ ] Define how time is persisted: last tick index and last campaign timestamp per save; on load, clock restores and tick driver continues.
- [ ] **Integration**
  - [ ] Tick driver: who invokes "tick" (main loop, dedicated thread, or event from render loop). Contract: one tick = one atomic advance of clock + all tick-phase systems.
  - [ ] Decoupling from rendering: simulation must run without frame updates; support headless or lightweight preview (e.g. 2D map) that only consumes sim state.

### Interface sketch

- **SimClock** (read-only view):
  - `current_tick(): int`
  - `sim_time(): SimTime` (e.g. campaign day/hour or epoch ms)
  - `session_id(): string`
  - `is_paused(): bool`
- **TickDriver** (internal):
  - `advance_one_tick(): void` — advances clock, then runs phased tick logic in order; only called when not paused.
  - `pause() / resume(): void`
- **Tick phases** (order of execution within one tick):
  - Phase 1: environment (weather, time-of-day effects)
  - Phase 2: NPCs and entities (agendas, movement, interactions)
  - Phase 3: factions and relationships (reputation updates, events)
  - Phase 4: persistence flush (optional; or async after N ticks)

### Invariants

- Tick index never decreases; sim_time is monotonic in tick order.
- Paused state: no tick advances; all read APIs still valid.
- Replay: given same initial state and same tick count, same deterministic outcome (when using fixed step and ordered phases).
