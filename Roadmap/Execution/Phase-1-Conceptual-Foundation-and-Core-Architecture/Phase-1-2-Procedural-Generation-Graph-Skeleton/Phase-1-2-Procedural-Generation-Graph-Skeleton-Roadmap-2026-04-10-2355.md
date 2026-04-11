---
title: Phase 1.2 (Execution) — Procedural Generation Graph Skeleton
created: 2026-04-10
tags:
  - roadmap
  - execution
  - sandbox
  - procedural-generation
  - graph
project-id: sandbox-genesis-mythos-master
roadmap_track: execution
roadmap-level: secondary
phase-number: 1
subphase-index: "1.2"
status: in-progress
handoff_readiness: 85
conceptual_counterpart: "[[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-03-30-1605]]"
---

# Phase 1.2 (Execution) — Procedural generation graph skeleton

Execution secondary **1.2** on the parallel spine. Tightens **DAG-shaped stage contracts**, **topological evaluation order**, and **named intent-injection hooks** relative to the Phase 1 execution primary and **1.1** layering seams. **GMM-2.4.5** lineage/compare harnesses and **CI closure** (acyclicity proofs, registry IDs) remain **explicitly deferred** unless/until evidenced in a later execution slice.

Conceptual authority: [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-03-30-1605]] · Phase 1 execution primary: [[../Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-04-10-2100]] · Prior execution slice **1.1**: [[../Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-04-10-2205]]

## Graph contract (execution-tightened)

| Element | Contract | Forbidden |
| --- | --- | --- |
| **Stage node** | Typed inputs/outputs; emits **staged deltas** or **commit tokens** only via 1.1 layering APIs | Direct world mutation without ledger commit path |
| **Edge** | Data dependency; no implicit cycles in default DAG | Hidden back-edges without explicit feedback-edge label |
| **Topological order** | Scheduler consumes stages in valid topo order; dry-run may skip downstream on upstream failure | Reordering that violates declared dependencies |
| **Intent hook** | Named attachment point on node or on world-state→stage edge; priority rules TBD registry | Ad-hoc string routing without stable hook id |

## Pseudocode seams (graph-level, text)

Depth-2 slice: **structure only** — stage bodies and C/C++ precision belong in **1.2.1+** tertiaries or later execution passes.

```text
seam evaluate_generation_graph(graph, seed_bundle, mode):
  order = graph.topological_order()   # must be DAG for default spine
  for stage_id in order:
    if mode == dry_run:
      staged = stage_id.simulate(inputs_for(stage_id), seed_bundle)
      if staged.validation_failed: skip_downstream(stage_id); continue
    else:
      staged = stage_id.run(inputs_for(stage_id), seed_bundle)
    publish_staged_outputs(stage_id, staged)
  return commit_or_preview_bundle(mode)
```

```text
seam attach_intent_hook(hook_id, target_node_or_edge, intent_envelope):
  registry.assert_known_hook(hook_id)  # execution-deferred: stable IDs
  route(intent_envelope, target_node_or_edge, hook_id)
```

## Acceptance criteria — evidence rows

| ID | Criterion | Evidence artifact (planned hook) | Status |
| --- | --- | --- | --- |
| AC-1.2.E1 | Declared graph is DAG for default spine (no undeclared cycles) | [[Evidence-Stubs/graph_dag_audit.stub.txt]] (stub; replace with topo proof) | Stubbed |
| AC-1.2.E2 | Topological evaluation order matches declared dependencies | `stage_order_trace.log` | Planned |
| AC-1.2.E3 | Intent hooks are registered ids (no orphan attachments) | `hook_registry.tsv` | Planned |
| AC-1.2.E4 | Dry-run produces no committed world state | `dry_run_commit_diff.empty` | Planned |

> Deferral: **GMM-2.4.5** comparator tables, registry/CI closure, and cross-lane stress harnesses are **out of scope** for this slice unless evidence is explicitly attached later — aligns with conceptual execution-deferral waiver.

> [!note] AC evidence stubs
> Depth-2 secondary: AC rows may use **Stubbed** status with vault-resolvable stub paths until **1.2.1+** tertiaries attach real artifacts.

## Lane comparand (sandbox vs godot)

| Concern | Sandbox B (this slice) | Godot A (reference) | Shared contract |
| --- | --- | --- | --- |
| Graph shape | Explicit DAG + hook registry | Scene tree / resource deps (different metaphor) | Deterministic ordering policy documented |
| Staging | Staged deltas through ledger seam | Variant/resource commit points | No silent authoritative mutation |
| Dry-run | Graph-level preview without commit | Editor tooling previews | Operator-visible failure propagation |

## Intent Mapping

| Design intent target | Inspiration anchors | Execution mechanism | Validation signal |
| --- | --- | --- | --- |
| DAG default spine | Conceptual 1.2 NL DAG + hook story | Topo order + skip-on-failure policy | AC-1.2.E1–E2 rows |
| Intent injection | Named hooks on nodes/edges | `attach_intent_hook` seam + registry assert | AC-1.2.E3 |
| No commit in dry-run | Phase 1 primary partial-failure story | `mode == dry_run` branch in evaluate seam | AC-1.2.E4 |

## Related (execution spine)

- Tertiary chain **1.2.1–1.2.5** (conceptual tree) — next deepen targets on execution spine after this secondary.
- Layering cross-cuts: generation stages must respect **1.1** boundary matrix when touching ledger/dispatch/presentation.
