---
title: Phase 1.1.3 — Dependency direction, injection seams, and lifecycle hooks
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.1.3"
project-id: sandbox-genesis-mythos-master
status: active
priority: high
progress: 28
handoff_readiness: 77
created: 2026-03-30
tags:
  - roadmap
  - sandbox-genesis-mythos-master
  - phase-1
para-type: Project
links:
  - "[[Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-03-30-0500]]"
---

## Phase 1.1.3 — Dependency direction, injection seams, and lifecycle hooks

This tertiary closes the **structural wiring** part of the **1.1 layering slice**: which layers may depend on which (acyclicity), where **injection seams** live for generators and mod tools, and how **startup / shutdown / hot-swap** interact with the commit pipeline ([[Phase-1-1-1-Layer-Boundary-and-Commit-Pipeline-Roadmap-2026-03-30-0431]]) and the swap coordinator introduced in [[Phase-1-1-2-Observation-Cache-and-Invalidation-Roadmap-2026-03-30-1325]].

## Scope

**In scope:** Allowed dependency edges between world state, simulation, rendering, and input; prohibition of reverse authoritative edges; **named injection points** for procedural stages and plugins; **initialization order** (bootstrap graph) and **teardown / quiesce** before swap; relationship between **epoch/version** from 1.1.2 and “safe to tear down” signals.

**Out of scope:** Concrete DI frameworks, thread pools, async runtimes, network RPC, asset hot-reload file watchers. **Execution-deferred:** CI, registry closure, HR rollup artifacts.

## Behavior (natural language)

- **Dependency direction:** Edges follow **data authority** flow: input → simulation → world state → observers (render, tools); **no** layer that holds derived or cached truth may feed back into world state except through the single commit path from 1.1.1. Rendering may **read** simulation queries only through declared **read APIs**, never as hidden globals.
- **Acyclicity:** The runtime dependency graph of **modules** inside a layer may have internal cycles only where bounded (e.g. UI widget graphs); **cross-layer** dependencies must form a DAG when projected onto the four layer IDs.
- **Injection seams:** Procedural generation attaches at **named stages** (pre-world, post-commit hooks, tooling overlays) with explicit **contract surfaces**; mods use the same seams so replacement does not fork the spine.
- **Lifecycle:** **Boot:** load contracts → wire injection points → bring world state to minimal consistent snapshot → start simulation clock → subscribe observers. **Shutdown / swap:** **quiesce** in-flight intents (from 1.1.2) → optional **epoch barrier** → replace implementation behind seam → resume with version bump.

## Interfaces

- **Layer → layer (authorized):** Documented allow-list of calls (e.g. `sim.step(intents)`, `world.apply_commit(delta)`, `render.prepare(view_model, version)`).
- **Injection point API:** `register_stage(name, order, handler)` / `unregister` — order is total within a stage band; conflicts resolve by **explicit priority** or fail-fast in tooling.
- **Swap coordinator:** Same logical hook as 1.1.2; this slice adds **dependency declarations** so swap order respects “dependents before dependencies” on teardown.
- **Adjacent slices:** Parent [[Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-03-30-0500]]; commit pipeline 1.1.1; observation/cache 1.1.2; Phase 2 binds **graph nodes** to these injection names.

## Edge cases

- **Circular tool ↔ sim calls:** Editor tools that trigger simulation preview must use **non-authoritative** or **staged** paths so commits do not interleave with preview unless explicitly allowed.
- **Partial boot after crash:** Restore world state first; simulation may reject intents until **injection registry** matches saved epoch (execution detail; hook named here).
- **Optional layers:** Headless sim or batch jobs may omit render if **dependency graph** marks render as optional consumer only.

## Open questions

- Whether **mod load order** is strictly linear or may declare **peer bundles** (affects conflict resolution).
- Single **global** swap coordinator vs **per-seam** coordinators for large mods (deferred to execution plugin spec).

## Pseudo-code readiness

```
// Cross-layer projection: edges only downward in authority
allowed_edge(from_layer, to_layer):
  return from_layer in {input} and to_layer in {sim}
      or from_layer in {sim} and to_layer in {world}
      or from_layer in {world} and to_layer in {render, tools}
      or from_layer in {sim, world} and to_layer in {sim, world}  // same-layer module graph only

on_injection_register(name, order, handler):
  assert acyclic_with_existing(name, dependencies(handler))
  registry.add(InjectionPoint(name, order, handler))
```

## Research integration

> [!note] External grounding
> No `Ingest/Agent-Research/` notes were bound this run; alignment is **pattern-only** from layered architecture and explicit dependency-injection practice for games and editors.
