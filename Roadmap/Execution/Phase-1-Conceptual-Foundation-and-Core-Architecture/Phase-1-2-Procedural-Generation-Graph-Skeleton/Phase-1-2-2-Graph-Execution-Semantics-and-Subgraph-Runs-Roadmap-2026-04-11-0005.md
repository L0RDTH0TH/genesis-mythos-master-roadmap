---
title: Phase 1.2.2 (Execution) — Graph execution semantics and subgraph runs
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
subphase-index: "1.2.2"
status: in-progress
handoff_readiness: 86
handoff_readiness_basis: design_traceability_pre_evidence
handoff_readiness_note: "Score reflects NL alignment to conceptual 1.2.2, waves/subgraph seams, and intent mapping; AC rows remain Planned until evidence attaches."
state_hygiene_reconcile_2026_04_11: "Repaired stale automation-next prose vs execution cursor: authoritative next-target is [[../../workflow_state-execution]] `current_subphase_index` (repair run `handoff-audit-repair-sandbox-dual-truth-20260411T143000Z`)."
conceptual_counterpart: "[[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-2-Graph-Execution-Semantics-and-Subgraph-Runs-Roadmap-2026-03-30-1805]]"
---

# Phase 1.2.2 (Execution) — Graph execution semantics and subgraph runs

Execution tertiary **1.2.2** on the **parallel spine** under `Phase-1-2-Procedural-Generation-Graph-Skeleton/`, aligned to conceptual [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-2-Graph-Execution-Semantics-and-Subgraph-Runs-Roadmap-2026-03-30-1805]]. Focus: **serial vs wave execution**, **subgraph closure** for regeneration, **prefix / intent-scoped** partial runs, **deterministic tie-break** when multiple topological orders exist, and **failure / empty propagation** — consistent with **1.2.1** taxonomy and **secondary 1.2** dry-run vs commit posture. **GMM-2.4.5** lineage/compare harnesses and **CI** graph proofs remain **explicitly deferred** unless evidenced later.

Upstream **1.2.1** execution: [[Phase-1-2-1-Node-Taxonomy-Edges-and-Topological-Order-Roadmap-2026-04-11-0005]] · Parent secondary **1.2**: [[Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-04-10-2355]] · Phase 1 execution primary: [[../Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-04-10-2100]]

## Handoff readiness vs evidence

**Handoff readiness** on this slice is **design- and traceability-first**: conceptual alignment, execution-schedule seams, and intent mapping. It does **not** claim execution evidence until at least one AC row advances beyond **Planned**. **`status: in-progress`** means this tertiary’s spec and hooks are not closed in-repo.

**Automation cursor (authoritative):** Execution sequencing and “what deepen runs next” are **only** stated in [[../../workflow_state-execution]] (`current_subphase_index`, latest ## Log row). This note’s historical “next tertiary after **1.2.2**” chain was **1.2.3 → 1.2.4 → 1.2.5**; do **not** treat the sentence that used to say “next target **`1.2.3`**” as current routing — after **2026-04-11** repair, live cursor is **`1.2.5`** (see workflow state frontmatter + last log row).

## Alignment to conceptual Phase-1-2-2

| Conceptual contract | Execution mechanism (this note) | Validation signal |
| --- | --- | --- |
| Serial pass vs waves; parallelism only when dependency-independent | `execute_pass` + `wave_partition` seams (text sketches) | AC-1.2.2.E1 |
| Subgraph selection + transitive predecessor closure | `subgraph_closure` + “out of subgraph” no-op semantics | AC-1.2.2.E2 |
| Prefix runs and carry-forward policy at NL boundary | `prefix_run` seam + explicit snapshot boundary hook | AC-1.2.2.E3 |
| Failure / typed-empty propagation vs commit | Align to **1.2** + **1.2.1** skip/propagate vocabulary | AC-1.2.2.E4 |

## Execution schedule seams (mid-technical)

**Depth 3:** interfaces and algorithm sketches in **`text`** blocks only — no committed C++ standard-library claims; verbatim std citations belong in a **Research-backed** pass if/when C++ surfaces are introduced.

```text
execute_pass(graph, mode, scope):
  order = graph.topological_order_stable()   # from 1.2.1
  active = scope_select(scope, order)      # full | prefix | subgraph
  for wave in wave_partition(active, graph):
    for node_id in wave:
      if not in_subgraph(node_id, scope): mark_no_op(node_id); continue
      run_node(node_id, mode)
```

```text
subgraph_closure(target_ids, graph):
  // Expand to all dependency predecessors so inputs exist (conceptual 1.2.2)
  return transitive_predecessors(target_ids, graph.data_dependency_edges)
```

```text
wave_partition(nodes_in_order, graph):
  // Greedy: pack consecutive nodes into one wave when pairwise
  // dependency-independent per conceptual NL; ordering-only edges
  // still enforce relative order within a wave when they would race.
  waves = []
  // ... stable greedy split; tie-break: stable node id (1.2.1)
  return waves
```

## Interfaces

| Direction | Contract |
| --- | --- |
| Upstream **1.2.1** | Consumes `topological_order_stable`, `EdgeKind`, `NodeRole`; this note adds **schedule** and **scope** only. |
| Upstream **secondary 1.2** | **Dry-run** vs **commit**, injection hooks, partial failure — must stay consistent with `execute_pass` and **no authoritative commit on failed validation**. |
| Downstream **1.2.3+** | Stage families may specialize waves using **1.2.1** + **1.2.2** — see conceptual [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-3-Stage-Families-Specialization-and-Pipeline-Roles-Roadmap-2026-03-30-1905]]. |

## Tasks (tertiary execution breakdown)

| Task | Owner | Depends on | Target artifact |
| --- | --- | --- | --- |
| T-1.2.2-a | Roadmap agent / operator | **1.2.1** topo seam | `schedule_trace.txt` (E1 wave list or serial) |
| T-1.2.2-b | Roadmap agent | T-1.2.2-a | `subgraph_closure.json` (E2 node sets) |
| T-1.2.2-c | Roadmap agent | **1.2** | `prefix_run_policy.md` (E3 snapshot boundary) |
| T-1.2.2-d | Roadmap agent | T-1.2.2-b | `empty_propagation_log.txt` (E4) |

**GMM-2.4.5** / **CI** closure: **out of scope** for this slice (explicit deferral unchanged).

## Acceptance criteria — evidence hooks

| ID | Criterion | Evidence artifact (planned) | Status |
| --- | --- | --- | --- |
| AC-1.2.2.E1 | Waves respect dependency edges; ordering-only serialized when needed | `schedule_trace.txt` | Planned |
| AC-1.2.2.E2 | Subgraph closure matches reversed-edge reachability | `subgraph_closure.json` | Planned |
| AC-1.2.2.E3 | Prefix policy documented; no implicit carry-forward without boundary | `prefix_run_policy.md` | Planned |
| AC-1.2.2.E4 | Empty/fail propagation matches **1.2** / **1.2.1** | `empty_propagation_log.txt` | Planned |

## Intent Mapping

| Design intent target | Inspiration anchors | Execution mechanism | Validation signal |
| --- | --- | --- | --- |
| Serial MVP + optional parallelism when independent | Conceptual 1.2.2 NL | `execute_pass` + `wave_partition` | AC-1.2.2.E1 |
| Subgraph regeneration closure | Conceptual subgraph selection | `subgraph_closure` | AC-1.2.2.E2 |
| Prefix / partial runs | Conceptual prefix + carry-forward | `prefix_run` + boundary hook | AC-1.2.2.E3 |
| Failure and typed-empty propagation | **1.2** + **1.2.1** | Skip / propagate until commit seam | AC-1.2.2.E4 |
| **GMM-2.4.5 / CI closure** | N/A this slice | — | **Deferred** (explicit) |

## Risks (v0)

- **Over-binding waves** before **1.2.3** stage families — mitigate by keeping **wave_partition** as a **trace** artifact, not a thread model.
- **Ordering-only vs parallelism** misclassified — mitigate with **schedule_trace** audit (E1).

## Related (execution spine)

- Prior **1.2.1**: [[Phase-1-2-1-Node-Taxonomy-Edges-and-Topological-Order-Roadmap-2026-04-11-0005]]
- **Structural sibling “next” on the tertiary chain (not automation routing):** tertiary **1.2.3** (stage families) — execution [[Phase-1-2-3-Stage-Families-Specialization-and-Pipeline-Roles-Roadmap-2026-04-11-1415]] · conceptual [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-3-Stage-Families-Specialization-and-Pipeline-Roles-Roadmap-2026-03-30-1905]]. **Automation “what runs next”** remains **only** in [[../../workflow_state-execution]] (may be past **1.2.3** when this slice was authored).

## Research integration

> [!note] External grounding
> No `Ingest/Agent-Research/` notes bound this run; alignment is **vault-first** to conceptual **1.2.2** and execution **1.2.1** / **1.2**. Mid-technical seams use **`text`** blocks only (no std C++ citations) to avoid **sandbox_code_precision** without a Research pass.
