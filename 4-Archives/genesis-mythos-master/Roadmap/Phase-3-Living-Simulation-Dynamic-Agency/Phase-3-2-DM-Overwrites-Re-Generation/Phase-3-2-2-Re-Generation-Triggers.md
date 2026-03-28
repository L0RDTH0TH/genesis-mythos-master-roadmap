---
title: Phase 3.2.2 — Re-Generation Triggers
roadmap-level: tertiary
phase-number: 3
subphase-index: "3.2.2"
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

## Phase 3.2.2 — Re-Generation Triggers

Define what counts as a "major structural change", when to queue or run region/full-world re-generation, and how overwrites interact with persistence and replay. Mid-technical: interfaces and algorithm sketches.

### Tasks

- [ ] **Major structural change (definition)**
  - [ ] Enumerate structural domains: terrain mesh/heights, biome assignment, POI/settlement layout, road/region graph, entity spawn tables, world seed or global parameters. Any change to these = structural.
  - [ ] Contrast with overlay domains (Phase 3.2.1): token positions, weather, events, NPC directives are non-structural; no re-gen required.
  - [ ] Document edge cases: e.g. "add one new POI" = structural (triggers region re-gen or incremental POI pass); "move a token" = non-structural.
- [ ] **Re-generation triggers and scope**
  - [ ] Trigger types: (1) explicit user/DM request ("regenerate this region", "full world re-gen"), (2) implicit from tool (e.g. terrain brush that modifies heightmap), (3) system (e.g. save/load of a different world version). All require intent; no automatic re-gen from sim ticks.
  - [ ] Scope: region (chunk, tile, or named region), vs full-world. Region re-gen: inputs = region id + seed overrides + optional intent; output = new geometry/content for that region only; overwrites outside the region unchanged.
  - [ ] Queue vs run: "queue" = schedule re-gen (e.g. after session, or in background); "run" = block until re-gen completes. Policy: optional config (sync vs async) per trigger type.
- [ ] **Overwrites and persistence across re-gen**
  - [ ] Pre re-gen: snapshot current overwrite layer (and committed baseline) so they can be re-applied or dropped by policy.
  - [ ] Post region re-gen: overwrites that target entities/state inside the region may be invalid (e.g. entity id no longer exists). Define: discard region-overwrites, or migrate by stable id if available.
  - [ ] Post full-world re-gen: treat as new world; overwrites from previous world do not apply unless explicitly exported/imported (out of scope for MVP).
  - [ ] Replay: replay uses base + overlay at replay boundary tick; if re-gen happened after that tick, replay does not re-run gen—replay is sim-only. If re-gen happened before, base already includes it.

### Interface sketch

- **ReGenTrigger** (enum or policy):
  - `explicit_region(region_id, opts?)`, `explicit_full_world(opts?)`, `implicit_from_tool(tool_id, payload)`, `system_load(world_version)`.
- **ReGenService**:
  - `queue(trigger): job_id` — enqueue re-gen; return job id for status/cancel.
  - `run(trigger): result` — run re-gen synchronously; return success + new region/world ref.
  - `get_overwrite_policy(trigger): 'preserve' | 'discard_region' | 'discard_all'` — how to handle overwrites for this trigger.
- **Persistence**: Re-gen jobs and results logged (e.g. in decisions-log or run log); overwrite snapshot stored when re-gen is queued so user can restore or diff.
