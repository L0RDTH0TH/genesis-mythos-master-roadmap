---
title: Phase 1.1.3 (Execution) — Dependency direction and lifecycle
created: 2026-04-10
tags:
  - roadmap
  - execution
  - sandbox
  - layering
  - dependency
  - lifecycle
project-id: sandbox-genesis-mythos-master
roadmap_track: execution
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.1.3"
status: in-progress
handoff_readiness: 85
handoff_readiness_basis: design_traceability_pre_evidence
handoff_readiness_note: "Score reflects NL alignment to conceptual 1.1.3, DAG/lifecycle seams, and intent mapping; not evidence closure while AC rows remain Planned."
conceptual_counterpart: "[[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-3-Dependency-Direction-and-Lifecycle-Roadmap-2026-03-30-1420]]"
---

# Phase 1.1.3 (Execution) — Dependency direction and lifecycle

Execution tertiary **1.1.3** on the **parallel spine** under `Phase-1-1-Layering-and-Interface-Contracts/`, aligned to conceptual [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-3-Dependency-Direction-and-Lifecycle-Roadmap-2026-03-30-1420]]. Focus: **cross-layer dependency DAG** (no authority inversion), **injection seam registry** (named stages, ordering), **bootstrap / quiesce / teardown** ordering vs commit pipeline ([[Phase-1-1-1-Layer-Boundary-and-Commit-Pipeline-Roadmap-2026-04-10-2306]]) and epoch barriers from [[Phase-1-1-2-Observation-Cache-and-Invalidation-Roadmap-2026-04-10-2315]]. **GMM-2.4.5** cross-lane harnesses and **CI / registry closure** remain **explicitly deferred** unless evidenced later.

Parent execution secondary: [[Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-04-10-2205]] · Phase 1 execution primary: [[../Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-04-10-2100]] · Prior tertiary: [[Phase-1-1-2-Observation-Cache-and-Invalidation-Roadmap-2026-04-10-2315]]

## Handoff readiness vs evidence

**Handoff readiness** on this slice is **design- and traceability-first**: conceptual alignment, dependency/lifecycle seams, and intent mapping. It does **not** claim execution evidence until at least one AC row advances beyond **Planned**.

## Slice status vs execution cursor

- This note is the **1.1.3** execution spec slice (dependency direction / injection / lifecycle).
- After this mint, **`workflow_state-execution`** **`current_subphase_index`** advances to **`1.1.4`** (next deepen target).

## Alignment to conceptual Phase-1-1-3

| Conceptual contract | Execution mechanism (this note) | Validation signal |
| --- | --- | --- |
| Cross-layer DAG; no reverse authoritative edges | Layer projection table + forbidden edge list | AC-1.1.3.E1 |
| Named injection stages + total order within band | `injection_registry` schema + conflict policy | AC-1.1.3.E2 |
| Boot: contracts → registry → minimal world → sim → observers | `boot_graph` ordered steps | AC-1.1.3.E3 |
| Shutdown / swap: quiesce → epoch barrier → teardown order | Integrates 1.1.2 `swap_coordinator` + dependency declarations | AC-1.1.3.E4 |

## Dependency projection (execution)

**Rule:** Project runtime modules onto **layer IDs** (`input`, `sim`, `world`, `render`, `tools`). **Cross-layer** edges must be a **DAG** when projected; same-layer may retain bounded internal cycles (documented elsewhere).

```text
allowed_cross_layer_edge(from_layer, to_layer):
  # Authority flows downward: input→sim→world→(render|tools); no cache/observer feeds world except via commit ingress from 1.1.1
  return edge_in_allowlist(from_layer, to_layer) and not violates_commit_ingress(from_layer, to_layer)
```

## Injection seam registry

| Stage band | Registration API (logical) | Ordering | Conflict resolution |
| --- | --- | --- | --- |
| pre-world | `register_stage("pre_world", order, handler)` | Total order per band | Explicit priority; fail-fast in tooling if duplicate order |
| post-commit | `register_stage("post_commit", order, handler)` | After successful commit envelope | Same |
| tooling overlay | `register_stage("tools", order, handler)` | Non-authoritative | Cannot enqueue commits |

## Lifecycle harness (pseudocode)

```text
boot():
  load_contracts()
  build_injection_registry()        # acyclic w.r.t. declared handler dependencies
  world = minimal_consistent_snapshot()
  sim.start(world.version)
  observers.subscribe_all()

quiesce_for_swap():
  swap_coordinator.request_quiesce()   # from 1.1.2
  drain_in_flight_intents()
  epoch_barrier(current_epoch)

teardown_ordered():
  for module in reverse_dependency_order(registered_modules):
    module.shutdown()
```

## Boundary matrix (tertiary tightening)

| Seam | Upstream | Downstream | Forbidden |
| --- | --- | --- | --- |
| Dependency declarations | Module graph | `teardown_ordered` | Teardown before quiesce |
| Injection registry | Named stages | Handlers | Hidden globals bypassing registry |
| Epoch / swap | 1.1.2 version path | 1.1.3 lifecycle | Swap without barrier |
| Commit ingress | 1.1.1 pipeline | World authority | Observer → world write |

## Acceptance criteria — evidence hooks

| ID | Criterion | Evidence artifact (planned) | Status |
| --- | --- | --- | --- |
| AC-1.1.3.E1 | Cross-layer projection is a DAG; forbidden edges rejected at tooling | `layer_dag_audit.dot` | Planned |
| AC-1.1.3.E2 | Every injection stage has name, order, and dependency list | `injection_registry.json` | Planned |
| AC-1.1.3.E3 | Boot ordering documented and traceable to contracts | `boot_trace.jsonl` | Planned |
| AC-1.1.3.E4 | Quiesce + epoch barrier precede teardown on swap path | `swap_lifecycle_log.txt` | Planned |

## Intent Mapping

| Design intent target | Inspiration anchors | Execution mechanism | Validation signal |
| --- | --- | --- | --- |
| Dependency direction + acyclicity (conceptual 1.1.3) | Conceptual NL + 1.1.1 commit authority | `allowed_cross_layer_edge` + layer matrix | AC-1.1.3.E1 |
| Injection seams | Conceptual registry narrative | Stage bands + registration table | AC-1.1.3.E2 |
| Lifecycle hooks | Conceptual boot / quiesce / teardown | `boot()` / `quiesce_for_swap` / `teardown_ordered` pseudocode | AC-1.1.3.E3–E4 |

## Risks (v0)

| Risk | Mitigation | Linked AC |
| --- | --- | --- |
| Peer mod bundles vs linear order | Flag in registry schema; defer resolution to plugin spec | AC-1.1.3.E2 |
| Per-seam vs global swap coordinator | Start global; split only if scale requires | AC-1.1.3.E4 |
| Scope creep into GMM-2.4.5 / CI | Explicit deferrals | Deferrals |

## Explicit deferrals

- **GMM-2.4.5-*** comparator / cross-lane harness: not claimed.
- **CI** gates (coverage, stress matrices): not claimed.
- **New** verbatim C/C++ standard API citations: deferred to a future Research-backed pass with allowlisted URLs; this slice uses **pseudocode** and **reuse-only** references to sibling execution notes (same pattern as execution **1.1.2**).

## Code precision (reuse-only)

No new C/C++ standard library API surfaces in this slice. **Code precision authority** for verbatim standard citations remains on the Phase 1 execution primary ([[../Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-04-10-2100]]) until a lane Research pass adds allowlisted citations.

## Next structural intent

Deepen execution tertiary **1.1.4** (error boundaries / failure propagation) on the mirrored spine — conceptual [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-4-Error-Boundaries-and-Failure-Propagation-Roadmap-2026-03-30-1430]].
