---
created: 2026-03-18
tags: [research, agent-research, genesis-mythos-master, roadmap]
project-id: genesis-mythos-master
linked_phase: "Phase-1"
research_query:
  - "ECS boundaries: world-state vs simulation vs rendering"
  - "Deterministic provenance + seed/snapshot schema"
research_tools_used: [web_search, web_fetch]
agent-generated: true
title: "Phase 1 — Core architecture research notes"
---

## Summary

Focused reference notes to support Phase 1 architecture decisions: (1) ECS-style separation and system/query patterns that keep simulation, rendering, and input boundaries clean; (2) a provenance schema pattern you can reuse for deterministic generation + simulation runs.

## ECS boundaries + system patterns

- **Small components, composed features**: Favor narrow components and compose behavior by adding/removing components; it keeps boundaries explicit and discourages “god objects”.  
  [Source: Meta Horizon — ECS Patterns](https://developers.meta.com/horizon/documentation/web/iwsdk-concept-ecs-patterns/)
- **Qualify/disqualify events**: Use query membership events to run expensive setup/teardown once (e.g. allocate render resources when an entity becomes renderable), rather than doing it every frame.  
  [Source: Meta Horizon — ECS Patterns](https://developers.meta.com/horizon/documentation/web/iwsdk-concept-ecs-patterns/)
- **Avoid O(N²)**: When joining sets, build indices/tags and keep hot-loop work linear.  
  [Source: Meta Horizon — ECS Patterns](https://developers.meta.com/horizon/documentation/web/iwsdk-concept-ecs-patterns/)
- **Component internals discipline**: If you must store internal/system-only fields, explicitly mark them (e.g. `_field`) so your public schema stays stable and tools/docs can hide internals.  
  [Source: Meta Horizon — ECS Patterns](https://developers.meta.com/horizon/documentation/web/iwsdk-concept-ecs-patterns/)

## Provenance schema (determinism + reproducibility)

`tskit`’s provenance spec is a good template for **what to record per run** so outputs are reproducible: software identity, parameters (including random seed), and environment details.

- **Three mandatory blocks**: `software`, `parameters`, `environment` are required.  
  [Source: Tskit manual — Provenance](https://tskit.dev/tskit/docs/stable/provenance.html)
- **Record random_seed even if auto-generated**: Store the seed in `parameters` so deterministic replay is possible.  
  [Source: Tskit manual — Provenance](https://tskit.dev/tskit/docs/stable/provenance.html)
- **CLI args as array**: If a stage is invoked via CLI, store `args: [...]` in parameters.  
  [Source: Tskit manual — Provenance](https://tskit.dev/tskit/docs/stable/provenance.html)
- **Environment capture**: Record OS + key libraries; optionally record resource usage in `resources` (elapsed_time, max_memory).  
  [Source: Tskit manual — Provenance](https://tskit.dev/tskit/docs/stable/provenance.html)

## Concrete integration guidance for Genesis Mythos

### Minimal provenance record per generation/sim “stage”

Use a small JSON object per stage execution:

- `schema_version`
- `software`: `{ name, version }`
- `parameters`: include `global_seed`, derived `stage_seed`, and stage config
- `environment`: OS + runtime versions
- optional `resources`

This maps cleanly to your vault’s “snapshot/dry-run/traceability” invariant: provenance is the **machine-readable** record, and the snapshot is the **data** record.

### Suggested boundary diagram (Phase 1)

- **World-state**: canonical data model + provenance pointers
- **Simulation**: reads world-state, produces state deltas/events (no rendering types)
- **Rendering**: consumes a read-only projection of world-state + sim events
- **Input**: produces intents/commands; never mutates world-state directly

## Sources

- [Meta Horizon — ECS Patterns](https://developers.meta.com/horizon/documentation/web/iwsdk-concept-ecs-patterns/)
- [Tskit manual — Provenance](https://tskit.dev/tskit/docs/stable/provenance.html)

