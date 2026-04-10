---
title: Phase 1 (Execution) — Conceptual Foundation and Core Architecture
created: 2026-04-10
tags:
  - roadmap
  - execution
  - sandbox
  - godot-comparand
project-id: sandbox-genesis-mythos-master
roadmap_track: execution
phase: 1
subphase: "1"
status: in-progress
handoff_readiness: 85
conceptual_counterpart: "[[../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-03-30-0430]]"
---

# Phase 1 (Execution) — Conceptual Foundation and Core Architecture

Execution remint anchor for Phase 1 on the parallel spine. Conceptual counterpart: [[../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-03-30-0430]].

## Scope

- Implement execution-facing interface seams for the first runnable vertical foundation.
- Define pseudocode skeleton for deterministic tick and handoff boundaries.
- Capture acceptance-criteria tables with lane comparand rows (Sandbox B vs Godot A).
- Keep GMM-2.4.5 and CI closure explicitly deferred to later execution slices.

## Interface seams (execution mint)

| Interface | Owner | Contract | Deferral |
| --- | --- | --- | --- |
| `IExecutionScheduler` | Runtime core | Owns fixed-step tick window, pause/resume controls, and deterministic seed handoff | CI instrumentation coverage deferred |
| `IStateLedgerStore` | State layer | Persists immutable checkpoint deltas keyed by tick index | GMM-2.4.5 replay diff harness deferred |
| `IOrderedDispatchBus` | Orchestration | Publishes domain events with causal ordering and idempotency key guard | CI concurrency stress suite deferred |
| `IPresentationPacketBridge` | Presentation seam | Projects sim-visible rows into renderer-agnostic packets | Consumer contract closure deferred |

## Pseudocode sketch

```text
function run_tick_window(seed_bundle, tick_budget):
  state = state_ledger_store.load(seed_bundle.root_state_id)
  for tick in 1..tick_budget:
    intents = ordered_dispatch_bus.collect_intents(tick)
    state = execution_scheduler.step(state, intents, seed_bundle)
    packet = presentation_bridge.project(state, tick)
    ordered_dispatch_bus.publish_projection(packet, tick)
  state_ledger_store.persist(state, seed_bundle.session_id)
  return state
```

## Roll-up gates (Phase 1 closure)

| Secondary slice | Gate (must be true for Phase 1 exit) | Primary AC / hook |
| --- | --- | --- |
| **1.1** Layering + interface contracts | Boundary matrix + pseudocode seams + AC evidence hooks minted; deferrals explicit | AC-1.1-A–D + secondary AC-1.1.E1–E4 hooks |
| *TBD* | Additional secondaries as remint progresses | TBD — populate when next execution secondaries land |

## Handoff readiness basis

- Interface seams table + pseudocode sketch cover **scheduler → ledger → dispatch → presentation** ordering.
- AC table rows map to **determinism**, **checkpoint restore**, **dispatch order**, and **packet schema** targets.
- Intent Mapping + lane comparand document **sandbox vs godot** without claiming GMM-2.4.5 or CI closure.
- Code precision block cites **allowlisted** C++ references only (reuse path for tertiary mints).

## Acceptance criteria (execution-first)

| ID | Criterion | Evidence target | Status |
| --- | --- | --- | --- |
| AC-1.1-A | Tick window stays deterministic across two replay runs with the same seed bundle | Matching state digest at final tick | Planned |
| AC-1.1-B | State checkpoint deltas restore without ordering drift | Restore succeeds at boundary tick with identical packet set | Planned |
| AC-1.1-C | Dispatch bus keeps causal ordering through projection handoff | Ordered event trace with no inversion | Planned |
| AC-1.1-D | Presentation bridge emits schema-conformant packets per tick | Packet schema validation + replay sample | Planned |

## Lane comparand rows

| Row | Lane B (Sandbox) | Lane A (Godot) | Common contract |
| --- | --- | --- | --- |
| Runtime tick primitive | C++ fixed-step scheduler loop | `_physics_process` bounded-step orchestration | Stable tick budget and deterministic ordering |
| Event dispatch seam | Typed queue + dispatcher | Signal/event-channel envelope | Ordered publish/apply boundary |
| Projection surface | Renderer-agnostic packet schema | Node/scene-bound presentation payload | Sim-visible projection schema |
| Replay verification | Seeded replay + state digest check | Seeded replay path + frame checkpoints | Equivalent replay hash contract |

## Intent Mapping

| Design intent target | Inspiration anchors | Execution mechanism | Validation signal |
| --- | --- | --- | --- |
| Deterministic tick window under explicit layer seams | Conceptual Phase 1 layering + generation skeleton contracts | `IExecutionScheduler` drives fixed-step loop; `IStateLedgerStore` binds checkpoint commit boundaries | AC-1.1-A deterministic digest parity; AC-1.1-B checkpoint restore parity |
| Ordered intent dispatch before projection publication | Conceptual ordering contract: input -> simulation -> commit -> render read | `IOrderedDispatchBus` gathers intents and publishes projection packets with idempotency keys | AC-1.1-C event-order trace with inversion count = 0 |
| Renderer-agnostic output packets for downstream consumers | Conceptual outward guarantee for presentation surfaces | `IPresentationPacketBridge` normalizes sim-visible rows into packet schema | AC-1.1-D schema checks and replay sample match |

## Explicit deferrals

- `GMM-2.4.5-*` comparator and lineage closure rows are execution-deferred in this mint.
- CI seam expansion (cross-lane stress, long-run replay matrix, report automation) is deferred.
- These deferrals are intentional and tracked for downstream execution slices, not conceptual rewrites.

## Code precision authority

### Scheduler monotonic timing basis

> "steady_clock is specifically designed to calculate time intervals."
>
> "Its member now never returns a lower value than in a previous call."

Source: [cplusplus.com — std::chrono::steady_clock](https://cplusplus.com/reference/chrono/steady_clock/)

### Ordered dispatch heap contract

> "its first element is always the greatest of the elements it contains, according to some strict weak ordering criterion."
>
> "This is done automatically by the container adaptor by automatically calling the algorithm functions make_heap, push_heap and pop_heap when needed."

Source: [cplusplus.com — std::priority_queue](https://cplusplus.com/reference/queue/priority_queue/)

### Checkpoint key-value persistence contract

> "`std::unordered_map` is an associative container that contains key-value pairs with unique keys. Search, insertion, and removal of elements have average constant-time complexity."
>
> "References and pointers to either key or data stored in the container are only invalidated by erasing that element, even when the corresponding iterator is invalidated."

Source: [cppreference — std::unordered_map](https://en.cppreference.com/w/cpp/container/unordered_map)

## Next structural intent

Secondary **1.1** minted — [[Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-04-10-2205]]. Next: deepen execution tertiary **`1.1.1`** on the mirrored spine (commit pipeline / layer boundary).
