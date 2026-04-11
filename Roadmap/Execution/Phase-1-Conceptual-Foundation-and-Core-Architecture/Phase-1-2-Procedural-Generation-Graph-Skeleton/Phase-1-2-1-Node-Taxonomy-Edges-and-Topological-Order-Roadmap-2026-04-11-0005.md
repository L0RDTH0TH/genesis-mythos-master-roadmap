---
title: Phase 1.2.1 (Execution) — Node taxonomy, edges, and topological order
created: 2026-04-11
tags:
  - roadmap
  - execution
  - sandbox
  - procedural-generation
  - graph
project-id: sandbox-genesis-mythos-master
roadmap_track: execution
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.2.1"
status: in-progress
handoff_readiness: 86
handoff_readiness_basis: design_traceability_pre_evidence
handoff_readiness_note: "Score reflects NL alignment to conceptual 1.2.1, seams, and intent mapping; AC rows remain Planned until evidence attaches."
conceptual_counterpart: "[[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-1-Node-Taxonomy-Edges-and-Topological-Order-Roadmap-2026-03-30-1705]]"
---

# Phase 1.2.1 (Execution) — Node taxonomy, edges, and topological order

Execution tertiary **1.2.1** on the **parallel spine** under `Phase-1-2-Procedural-Generation-Graph-Skeleton/`, aligned to conceptual [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-1-Node-Taxonomy-Edges-and-Topological-Order-Roadmap-2026-03-30-1705]]. Focus: **typed stage nodes**, **edge kinds** (data dependency, ordering-only, intent-hook attachment), **topological evaluation** policy, and **layer-touch tags** vs **1.1** seams. **GMM-2.4.5** lineage/compare harnesses and **CI** acyclicity proofs remain **explicitly deferred** unless evidenced later.

Parent execution secondary **1.2**: [[Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-04-10-2355]] · Phase 1 execution primary: [[../Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-04-10-2100]]

## Handoff readiness vs evidence

**Handoff readiness** on this slice is **design- and traceability-first**: conceptual alignment, graph taxonomy seams, and intent mapping. It does **not** claim execution evidence until at least one AC row advances beyond **Planned**. **`status: in-progress`** means this tertiary’s spec and hooks are not closed in-repo; automation **next** target is **`1.2.2`** — see [[../../workflow_state-execution]].

## Alignment to conceptual Phase-1-2-1

| Conceptual contract | Execution mechanism (this note) | Validation signal |
| --- | --- | --- |
| Stage nodes as typed roles (generator, transform, validation, commit boundary) | Node-type enum + port vocabulary in seams (no concrete stage bodies) | AC-1.2.1.E1 |
| Dependency vs ordering-only vs intent-hook edges | Edge-kind table + scheduler tie-break rules | AC-1.2.1.E2 |
| Topological order consistent with dependencies; acyclic default spine | `topo_walk` seam + explicit feedback-edge deferral | AC-1.2.1.E3 |
| Layer-touch metadata per node vs **1.1** matrix | Layer-touch tag column + cross-ref to **1.1** secondary | AC-1.2.1.E4 |

## Node and edge model (execution seams)

**Mid-technical (depth 3):** interfaces and algorithm sketches only — no committed C++ standard-library claims; precision with verbatim std citations belongs in **1.2.2+** or a dedicated research-backed pass.

```text
enum NodeRole {
  generator,
  transform,
  validation_gate,
  world_commit_boundary,
  observability_only
}

enum EdgeKind {
  data_dependency,   // upstream output port -> downstream input port
  ordering_only,     // schedule tie-break without data prerequisite
  intent_hook        // named hook attachment on node or boundary
}
```

```text
seam topo_walk(graph, mode):
  order = graph.topological_order_stable()   # DAG default; tie-break: stable node id
  for node_id in order:
    if mode == dry_run and upstream_failed(node_id):
      mark_skipped(node_id); continue
    run_node(node_id, mode)
```

## Layer-touch vs 1.1

| Layer seam (from **1.1**) | Allowed on this node class | Notes |
| --- | --- | --- |
| Simulation → World | `world_commit_boundary` only | Matches **1.1.1** commit pipeline ordering |
| Ingress → Simulation | `generator` / `transform` | Intents staged before commit-class nodes |
| Presentation | `observability_only` | No authoritative writes |

## Tasks (tertiary execution breakdown)

| Task | Owner | Depends on | Target artifact |
| --- | --- | --- | --- |
| T-1.2.1-a | Roadmap agent / operator | — | [[Evidence-Stubs/node_catalog.tsv]] (E1 schema + example row) |
| T-1.2.1-b | Roadmap agent | T-1.2.1-a | `edge_kind_audit.log` (E2) |
| T-1.2.1-c | Roadmap agent | T-1.2.1-b | `trace_topo_order.txt` (E3) |
| T-1.2.1-d | Roadmap agent | **1.1** boundary matrix | `layer_touch_matrix.tsv` (E4) |

**GMM-2.4.5** / **CI** graph proofs: **out of scope** for this slice (explicit deferral unchanged).

## Acceptance criteria — evidence hooks

| ID | Criterion | Evidence artifact (planned) | Status |
| --- | --- | --- | --- |
| AC-1.2.1.E1 | Node roles + ports documented; no orphan nodes in default DAG | [[Evidence-Stubs/node_catalog.tsv]] | Stubbed |
| AC-1.2.1.E2 | Edge-kind matrix matches scheduler (dep vs ordering-only) | `edge_kind_audit.log` | Planned |
| AC-1.2.1.E3 | Topological order equals declared dependency closure | `trace_topo_order.txt` | Planned |
| AC-1.2.1.E4 | Layer-touch tags consistent with **1.1** boundary matrix | `layer_touch_matrix.tsv` | Planned |

## Intent Mapping

| Design intent target | Inspiration anchors | Execution mechanism | Validation signal |
| --- | --- | --- | --- |
| Node taxonomy + edge semantics | Conceptual 1.2.1 NL + secondary **1.2** graph contract | `NodeRole` / `EdgeKind` + `topo_walk` seam | AC-1.2.1.E1–E3 |
| Topological order + stable tie-break | Conceptual “multiple valid orders” / replay | Stable ID order in `topological_order_stable` | AC-1.2.1.E3 |
| Intent hooks on nodes/edges | Secondary **1.2** intent hook row | `intent_hook` edge kind + registry id assert (deferred) | AC-1.2.1.E2 |
| **GMM-2.4.5 / CI closure** | N/A this slice | — | **Deferred** (explicit) |

## Risks (v0)

- **Over-specifying ports** before **1.2.2** execution semantics — mitigate by keeping **port** names in a **stub TSV** until subgraph runs land.
- **Ordering-only** edges misclassified as data deps — mitigate with **edge_kind_audit** in AC.

## Related (execution spine)

- Next tertiary **1.2.2** (graph execution semantics): conceptual [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-2-Graph-Execution-Semantics-and-Subgraph-Runs-Roadmap-2026-03-30-1805]]
- Prior execution slice **1.1** chain: [[../Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-04-10-2205]]

## Research integration

> [!note] External grounding
> No `Ingest/Agent-Research/` notes bound this run; alignment is **vault-first** to conceptual **1.2.1** and execution secondary **1.2**. Mid-technical seams use **`text`** blocks only (no std C++ citations) to avoid **sandbox_code_precision** without a Research pass.
