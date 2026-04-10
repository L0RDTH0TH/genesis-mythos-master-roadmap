---
title: Phase 1 (Execution) — Conceptual Foundation and Core Architecture
created: 2026-04-10
tags:
  - roadmap
  - execution
  - godot
  - sandbox-comparand
project-id: godot-genesis-mythos-master
roadmap_track: execution
phase: 1
subphase: "1"
roadmap-level: primary
status: in-progress
handoff_readiness: 85
handoff_gaps:
  - "GMM-2.4.5-replay-diff / lineage-closure / CI-seam-expansion packets remain open until verdict rows + CI run IDs land"
handoff_audit_last: "2026-04-10T21:07:00Z"
conceptual_counterpart: "[[../../Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-03-30-0430]]"
---

# Phase 1 (Execution) — Conceptual Foundation and Core Architecture

Execution remint anchor for Phase 1 on the parallel spine. Conceptual counterpart: [[../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-03-30-0430]].

## Intent mapping

| Intent target | Inspiration anchors | Execution mechanism | Validation signal |
| --- | --- | --- | --- |
| Runnable vertical foundation with deterministic tick | PMG modularity + layered-game patterns | `IGameLoopKernel` + `IWorldStateStore` seams from this note | AC table + lane comparand rows |
| Godot vs Sandbox parity | Dual-lane Second-Brain policy | Comparand table + deferrals | Hostile validator + execution gate packets |

## Scope

- Implement execution-facing interface seams for the first runnable vertical foundation.
- Define pseudocode skeleton for deterministic tick and handoff boundaries.
- Capture acceptance-criteria tables with lane comparand rows (Godot A vs Sandbox B).
- Keep GMM-2.4.5 and CI closure explicitly deferred to later execution slices.

## Interface seams (execution mint)

| Interface | Owner | Contract | Deferral |
| --- | --- | --- | --- |
| `IGameLoopKernel` | Runtime core | Owns fixed-step tick, pause/resume, and deterministic seed handoff | CI instrumentation coverage deferred |
| `IWorldStateStore` | State layer | Snapshot/apply immutable frame deltas by tick index | GMM-2.4.5 replay diff harness deferred |
| `IEventBus` | Orchestration | Publish ordered domain events with idempotency keys | CI concurrency stress suite deferred |
| `IRenderProjectionBridge` | Presentation seam | Convert sim-visible rows into presentation payloads | Consumer contract closure deferred |

## Pseudocode sketch

```text
function run_tick_window(seed_bundle, tick_budget):
  state = world_store.load(seed_bundle.root_state_id)
  for tick in 1..tick_budget:
    intents = event_bus.collect_intents(tick)
    state = game_loop_kernel.step(state, intents, seed_bundle)
    projection = render_bridge.project(state, tick)
    event_bus.publish_projection(projection, tick)
  world_store.persist(state, seed_bundle.session_id)
  return state
```

## Acceptance criteria (execution-first)

| ID | Criterion | Evidence target | Status |
| --- | --- | --- | --- |
| AC-1.1-A | Tick loop remains deterministic across two replay runs with same seed bundle | Matching state hash at final tick | Evidence-backed (provisional) |
| AC-1.1-B | World-state deltas persist and restore at checkpoint boundary | Restore succeeds without ordering drift | Planned |
| AC-1.1-C | Event bus preserves causal ordering through projection handoff | Ordered event trace with no inversion | Planned |
| AC-1.1-D | Presentation bridge emits schema-conformant rows for each tick | Row schema validation + sample replay | Planned |

## Lane comparand rows

| Row | Lane A (Godot) | Lane B (Sandbox) | Common contract |
| --- | --- | --- | --- |
| Runtime tick primitive | `_physics_process` bounded-step orchestration | C++ fixed-step scheduler loop | Stable tick budget and deterministic ordering |
| Event dispatch seam | Signal/event-channel envelope | Typed queue + dispatcher | Ordered publish/apply boundary |
| Projection surface | Node/scene-bound presentation payload | Renderer-agnostic data packet | Sim-visible projection schema |
| Replay verification | Seeded replay path + frame checkpoints | Seeded replay with state digest | Equivalent replay hash contract |

## Explicit deferrals

- `GMM-2.4.5-*` comparator and lineage closure rows are execution-deferred in this mint.
- CI seam expansion (cross-lane stress, long-run replay matrix, report automation) is deferred.
- These deferrals are intentional and tracked for downstream execution slices, not conceptual rewrites.

## Roll-up closure map (execution gate reconciliation)

| Gate ID | Owner | Artifact target | Completion check | Current state |
| --- | --- | --- | --- | --- |
| `GMM-2.4.5-replay-diff` | Runtime + state | `3-Resources/Second-Brain/Validator-Reports/Execution-Gates/godot-phase1-gmm-245-replay-diff.md` | Two-run final hash equivalence with seed lineage annotation | Open (stub packet on disk; verdict rows TBD) |
| `GMM-2.4.5-lineage-closure` | Architecture | `3-Resources/Second-Brain/Validator-Reports/Execution-Gates/godot-phase1-gmm-245-lineage-closure.md` | Comparator rows resolved with explicit pass/fail marks | Open (stub packet on disk; verdict rows TBD) |
| `CI-seam-expansion` | CI + runtime | `3-Resources/Second-Brain/Validator-Reports/Execution-Gates/godot-phase1-ci-seam-expansion.md` | Cross-lane stress, long-run replay, and report automation run IDs recorded | Open (stub packet on disk; CI run IDs TBD) |

Execution gate deferment remains active until the listed completion checks are met and linked.

## Handoff-audit reconciliation (2026-04-10)

Repair queue `repair-handoff-audit-godot-exec-phase1-rollup-20260410T210700Z` **does not close** L1 `missing_roll_up_gates`; it binds the closure map to **on-disk stub packets** (see `3-Resources/Second-Brain/Validator-Reports/Execution-Gates/`) plus owner accountability until real verdict rows exist.

| Gate ID | Evidence packet status | Blocking condition before deepen `1.1` | Owner note |
| --- | --- | --- | --- |
| `GMM-2.4.5-replay-diff` | Determinism seed/hash pair logged (`AC-1.1-A`) but full replay-diff matrix still open | Attach replay-diff matrix artifact with comparator verdict rows | Runtime + state |
| `GMM-2.4.5-lineage-closure` | Schema path reserved, no closure verdict rows yet | Add lineage closure matrix with pass/fail and unresolved-item notes | Architecture |
| `CI-seam-expansion` | Scope documented, CI run IDs not yet attached | Record CI run IDs and cross-lane stress artifacts | CI + runtime |

This note remains eligible for execution follow-up with `handoff_readiness` below hard-close threshold until the three gate packets are linked and verified.

### AC-1.1-A evidence

Canonical record (including placeholder digests pending CI attestation): [[3-Resources/Second-Brain/Validator-Reports/Execution-Gates/godot-phase1-ac-1-1-a-determinism-check|godot-phase1-ac-1-1-a-determinism-check]]. Evidence-backed scope is **provisional** stub parity only; CI seam expansion remains open per roll-up closure map.

## Next structural intent

Mint **tertiary 1.1.1** execution slice after secondary **1.1** — see [[../Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-04-10-2110]] (completed 2026-04-10).
