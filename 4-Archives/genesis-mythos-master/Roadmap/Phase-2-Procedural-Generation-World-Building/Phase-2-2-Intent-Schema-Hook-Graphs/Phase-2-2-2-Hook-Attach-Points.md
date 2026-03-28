---
title: Phase 2.2.2 — Hook Attach Points into Pipeline & Simulation
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.2.2"
project-id: genesis-mythos-master
status: archived
priority: high
progress: 0
created: 2026-03-09
tags: [roadmap, genesis-mythos-master, phase, subphase]
para-type: Archive
links:
  - "[[Phase-2-2-Intent-Schema-Hook-Graphs-Roadmap-2026-03-09-1335]]"
---

## Phase 2.2.2 — Hook Attach Points into Pipeline & Simulation

Describe exactly where and how normalized intents attach into the generation pipeline stages and the living simulation state, so every hook has a clear, testable integration point.

Mid-technical: interfaces and algorithm sketches, not full pseudo-code — focus on surfaces, data flow, and invariants.

### Tasks

- [ ] Define hook taxonomy and ownership
  - [ ] Enumerate hook categories: generation-stage, entity-local, region-local, campaign/global, UI/debug-only
  - [ ] For each category, specify owner type (entity, region, world, rule-module), id scheme, and cardinality (one vs many hooks per owner)
  - [ ] Capture concrete examples for each (e.g. "region.weather_bias", "npc.loyalty_to_faction", "world.prophecy_pressure")
- [ ] Specify hook data model and lookup surfaces
  - [ ] Draft a canonical `HookAttachPoint` record (fields: id, owner_ref, category, trigger_phase, trigger_condition, payload, provenance, status)
  - [ ] Define how hooks are indexed for fast lookup by owner, category, and trigger_phase
  - [ ] Decide which parts live in immutable generation artifacts vs mutable simulation state
- [ ] Map hooks to generation pipeline stages
  - [ ] For each pipeline stage from Phase 2.1 (seed parsing → terrain → biome → POI → entities → simulation bootstrap), list:
    - [ ] Which hook categories it can read/attach
    - [ ] Which intent fields it consumes to create or modify hooks
    - [ ] Whether it is allowed to delete or deactivate hooks
  - [ ] Define per-stage contracts: required inputs, produced hooks, and guarantees for downstream consumers
- [ ] Define simulation integration and evolution rules
  - [ ] Describe how hooks project into long-lived simulation constructs (e.g. reputation graphs, event queues, environmental weights)
  - [ ] Specify update rules over time: decay, cooldowns, reinforcement, and conflict resolution when multiple hooks touch the same target
  - [ ] Identify which updates are atomic transactions vs eventual-consistency updates
- [ ] Design observability and control surfaces for hooks
  - [ ] Enumerate DM-facing views: per-entity hook inspector, region overlay, global hook dashboard
  - [ ] Define safe operations: enable/disable, override weight, annotate with notes, snapshot/rollback for debugging
  - [ ] Specify what metadata is logged for each hook change (who/what created it, which intents and rulesets contributed)

### Data model sketch (interfaces, not full implementation)

- Hook attach point record (conceptual):
  - `id`: stable identifier (phase-local unique, with project-wide prefix)
  - `owner_ref`: pointer to entity/region/global scope (type + id)
  - `category`: enum (e.g. `GEN_STAGE`, `ENTITY_TRAIT`, `REGION_ENV`, `GLOBAL_PRESSURE`, `DEBUG_ONLY`)
  - `trigger_phase`: which pipeline stage or simulation phase evaluates this hook
  - `trigger_condition`: predicate or reference to a rule condition
  - `payload`: structured data (weights, tags, thresholds, references to intents)
  - `provenance`: source intents, rulesets, and generation run id
  - `status`: active | disabled | deprecated

- Read/write surfaces:
  - Generation-side API (conceptual):
    - `register_hook(owner_ref, category, trigger_phase, trigger_condition, payload, provenance) -> hook_id`
    - `get_hooks_for_stage(stage_id, filter) -> [HookAttachPoint]`
    - `deprecate_hooks(filter) -> count`
  - Simulation-side API (conceptual):
    - `project_hooks_into_sim_state(tick_context) -> side_effects`
    - `query_hooks_for_entity(entity_id, filter) -> [HookAttachPoint]`

### Integration with pipeline stages (algorithm sketches)

- Seed parsing:
  - Scan normalized intents for hook-worthy structures (e.g. vows, rivalries, sacred sites).
  - Create high-level hooks tagged with minimal payload and broad categories (entity/faction/region).
  - Mark provenance so later stages can refine rather than duplicate.

- World layout stages (terrain/biome/POI/entities):
  - When placing regions and POIs, attach hooks to concrete locations and entities using owner_ref.
  - Adjust payloads with spatial context (e.g. biome danger level, travel distance, visibility).
  - Ensure idempotency: repeated generation runs with same seeds + overrides produce stable hook ids and placements unless overrides change.

- Simulation bootstrap:
  - Convert hooks into initial simulation state seeds (e.g. edges in reputation graph, scheduled events).
  - Validate that every hook is either:
    - Consumed into sim state, or
    - Explicitly marked as deferred/debug-only.

### Test surface (what "done" looks like)

- Minimal test scenarios:
  - [ ] Given a single faction rivalry intent, generation yields:
    - [ ] Hooks attached to the two factions and relevant regions
    - [ ] Simulation bootstrap projects these into a rivalry edge and tension events
  - [ ] Given multiple overlapping intents targeting the same region, hooks:
    - [ ] Remain uniquely identifiable and traceable back to their intents
    - [ ] Resolve conflicts according to defined precedence rules
  - [ ] Disabling a hook via DM UI:
    - [ ] Prevents it from influencing subsequent simulation ticks
    - [ ] Leaves provenance intact for later inspection or re-enable

- Definition-of-done for this subphase:
  - [ ] Hook taxonomy, data model, and APIs are stable enough to implement in code without re-opening higher-level Phase 2.1/2.2 decisions
  - [ ] At least three end-to-end examples are written that walk from intents → hooks → sim state → DM observability

