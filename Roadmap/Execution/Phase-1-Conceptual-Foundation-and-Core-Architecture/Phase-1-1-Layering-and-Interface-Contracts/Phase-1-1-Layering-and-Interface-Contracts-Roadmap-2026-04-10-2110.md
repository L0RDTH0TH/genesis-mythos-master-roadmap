---
title: Phase 1.1 (Execution) — Layering and Interface Contracts
created: 2026-04-10
tags:
  - roadmap
  - execution
  - godot
  - sandbox-comparand
project-id: godot-genesis-mythos-master
roadmap_track: execution
roadmap-level: secondary
phase-number: 1
subphase-index: "1.1"
status: in-progress
handoff_readiness: 85
conceptual_counterpart: "[[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-03-30-0500]]"
execution_mirror_of: "Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-03-30-0500"
---

# Phase 1.1 (Execution) — Layering and interface contracts

Execution remint for **secondary 1.1** on the parallel spine. Anchors the four-layer stack from the conceptual slice to **Godot 4.x** call surfaces (`SceneTree`, node callbacks, signals) and the **Sandbox** comparand lane, without collapsing deferrals on `GMM-2.4.5-*` or CI seams.

Parent execution context: [[../Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-04-10-2100]].

## Intent Mapping

| Intent target | Inspiration anchors | Execution mechanism | Validation signal |
| --- | --- | --- | --- |
| Four-layer stack with explicit commits | Conceptual 1.1 NL + PMG invariants | Layer table + interface contracts + pseudocode | AC-1.1.1-* + closure-map progressive rows |
| Godot lane specificity | Godot scene tree / process docs (whitelist-safe) | `_physics_process` orchestration + signal seams | Tertiary 1.1.x test hooks |

## Scope (execution)

- Bind **world / sim / render / input** boundaries to concrete **owner objects** and **commit points** suitable for GDScript and C++ lane stubs.
- Specify **interface-shaped** contracts (methods + ordering) that tertiary **1.1.x** notes can refine into signatures and tests.
- **Progress** closure-map evidence for `GMM-2.4.5-*` and `CI-seam-expansion` without claiming full gate closure.

## Layer mapping (Godot lane A)

| Conceptual layer | Godot ownership sketch | Commit / read rule |
| --- | --- | --- |
| World state | `Resource`-backed or custom datastore behind a single **WorldStateSession** facade | Mutations go through `apply_delta(DeltaBundle)`; no direct node field writes from render |
| Simulation | `_physics_process` orchestration + intent queue drain | Emits **staged** deltas; fixed step owns authoritative time |
| Rendering | Viewport / presentation nodes consuming **read-only** projection packets | Never calls `apply_delta`; may schedule read-only queries |
| Input | `Input` → intent normalization (`InputEvent` → domain intent) | Intents validated in sim step; DM tools route through same commit API |

Sandbox lane B keeps the same **contract names** but swaps the tick primitive for a C++ fixed-step scheduler (see comparand table in parent Phase 1 execution note).

## Interface contracts (execution-first)

| Contract | Responsibility | Ordering |
| --- | --- | --- |
| `IGameLoopKernel` | Drains intents, advances sim one tick, publishes projection envelope | Called once per physics frame after input dispatch |
| `IWorldStateStore` | `snapshot()` / `apply_delta()` for tick-scoped mutations | Single writer per tick |
| `IEventBus` | Ordered publish with idempotency keys | Subscribers may not mutate world state during dispatch |
| `IRenderProjectionBridge` | Maps sim-visible rows to presentation DTO | Invoked after commit for the tick |

## Pseudocode sketch (lane-neutral)

```text
function tick_once(kernel, bus, store, clock):
  intents = bus.pull_intents(clock.now())
  staged = kernel.step(store.snapshot(), intents, clock)
  store.apply_delta(staged.delta, clock.tick_index)
  bus.publish_projection(staged.projection, clock.tick_index)
```

## Acceptance criteria (secondary 1.1)

| ID | Criterion | Evidence target | Status |
| --- | --- | --- | --- |
| AC-1.1.1-A | Layer boundaries documented with explicit commit owner | Table + pseudocode alignment to parent AC rows | Met (this note) |
| AC-1.1.1-B | Godot vs Sandbox comparand rows for tick + dispatch | Parent comparand table extended with 1.1-specific hooks | Planned (tertiary) |
| AC-1.1.1-C | No render-path writes to authoritative state | Checklist + negative test hooks | Planned |

## Roll-up closure map (progressive evidence, queue `followup-deepen-exec-phase1-1-godot-20260410T210701Z`)

Open rows for **`GMM-2.4.5-*`** and **`CI-seam-expansion`** are **execution-deferred** pending CI/verdict evidence; they do **not** block the next tertiary execution deepen (**1.1.4**) unless a separate hard gate applies.

| Gate ID | Evidence packet | This-run progress | Next evidence |
| --- | --- | --- | --- |
| `GMM-2.4.5-replay-diff` | `.../godot-phase1-gmm-245-replay-diff.md` | Linked deterministic hash pair from parent `AC-1.1-A`; **matrix rows** still open | Attach two-run diff matrix + lane labels |
| `GMM-2.4.5-lineage-closure` | `.../godot-phase1-gmm-245-lineage-closure.md` | Schema path reserved; **closure verdict table** empty | Add pass/fail rows + seed lineage IDs |
| `CI-seam-expansion` | `.../godot-phase1-ci-seam-expansion.md` | Scope + owners restated; **CI run IDs** absent | Record stress run IDs + artifact links |

Statuses remain **open** until packets carry verdict rows; this slice advances **traceability** only.

## Godot documentation anchors (whitelist-safe)

- Scene tree / process order: see official Godot docs **MainLoop** / **Node** lifecycle (use in-repo cross-links; avoid non-vetted URLs in automated exports).

> [!note] Lane naming vs proof
> Godot class/API names in layer tables (`_physics_process`, `Input`, `SceneTree`, …) are **contract shorthand** for execution planning. Verbatim whitelist-backed citations for code-precision proofs are **deferred** to tertiary **1.1.x** deepens with `Task(research)` + allowlisted docs per godot-execution-guard.

## Next structural intent

Tertiary **1.1.1** minted: [[Phase-1-1-1-Layer-Boundary-and-Commit-Pipeline-Roadmap-2026-04-10-2359]]. Tertiary **1.1.2** minted: [[Phase-1-1-2-Observation-Cache-and-Invalidation-Roadmap-2026-04-11-0012]]. Tertiary **1.1.3** minted: [[Phase-1-1-3-Dependency-Direction-and-Lifecycle-Roadmap-2026-04-11-0015]]. Next: **tertiary 1.1.4** — error boundaries / failure propagation (conceptual mirror `Phase-1-1-4-*`).
