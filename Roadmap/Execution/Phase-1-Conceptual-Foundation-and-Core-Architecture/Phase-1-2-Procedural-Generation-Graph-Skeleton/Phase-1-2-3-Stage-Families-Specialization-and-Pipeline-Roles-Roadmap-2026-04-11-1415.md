---
title: Phase 1.2.3 (Execution) — Stage families, specialization, and pipeline roles
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
subphase-index: "1.2.3"
status: in-progress
handoff_readiness: 88
handoff_readiness_basis: design_traceability_pre_evidence
handoff_readiness_note: "Post-recal: Intent Mapping uses catalog bullet format with studied inspiration anchors; AC-1.2.3.E1 has inline TSV scaffold evidence. Remaining AC rows Planned until repo artifacts land."
conceptual_counterpart: "[[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-3-Stage-Families-Specialization-and-Pipeline-Roles-Roadmap-2026-03-30-1905]]"
---

# Phase 1.2.3 (Execution) — Stage families, specialization, and pipeline roles

Execution tertiary **1.2.3** on the **parallel spine** under `Phase-1-2-Procedural-Generation-Graph-Skeleton/`, aligned to conceptual [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-3-Stage-Families-Specialization-and-Pipeline-Roles-Roadmap-2026-03-30-1905]]. Focus: **stage family** labels (**structure**, **entities**, **glue**, **commit**), **pipeline roles** compatible with **1.2.1** node kinds, **specialization** / sub-families, and **cross-family dependency** rules — consistent with **1.2.2** schedule/subgraph semantics and **secondary 1.2** dry-run vs commit. **GMM-2.4.5** lineage/compare harnesses and **CI** graph proofs remain **explicitly deferred** unless evidenced later.

Upstream **1.2.2** execution: [[Phase-1-2-2-Graph-Execution-Semantics-and-Subgraph-Runs-Roadmap-2026-04-11-0005]] · Parent secondary **1.2**: [[Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-04-10-2355]] · Phase 1 execution primary: [[../Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-04-10-2100]]

## Handoff readiness vs evidence

**Handoff readiness** on this slice is **design- and traceability-first**: conceptual alignment, family/role seams, and intent mapping. **AC-1.2.3.E1** now has **Scaffolded (inline evidence)** (TSV registry in this note) — the first AC row to advance beyond **Planned**; **E2–E4** remain **Planned** until repo artifacts land. **`status: in-progress`** means this tertiary’s spec and hooks are not fully closed in-repo; automation **next** target is **`1.2.4`** — see [[../../workflow_state-execution]].

## Alignment to conceptual Phase-1-2-3

| Conceptual contract | Execution mechanism (this note) | Validation signal |
| --- | --- | --- |
| Minimum family set + role tags on nodes | `family_tag` + `primary_family` seams (tables / text) | AC-1.2.3.E1 |
| Cross-family edges: allowed vs disallowed patterns | `cross_family_rules.md` + dependency matrix sketch | AC-1.2.3.E2 |
| Specialization as optional sub-families | `specialization_overlay` without overriding **1.2.1** `EdgeKind` | AC-1.2.3.E3 |
| Commit family ordered after inputs (non–dry-run) | Tie to **1.2.2** waves + **1.2** commit seam | AC-1.2.3.E4 |

## Family and role seams (mid-technical, text-only)

**Depth 3:** interfaces and algorithm sketches in **`text`** blocks only — same deferral as **1.2.2**: no committed C++ standard-library claims in this slice.

```text
annotate_families(graph):
  for node_id in graph.nodes:
    assert primary_family(node_id) in {structure, entities, glue, commit}
    // secondary roles are documentation-only tags; do not replace EdgeKind
```

```text
cross_family_allowed(src_family, dst_family, edge_kind):
  // entities may depend on structure; glue may depend on entities/structure;
  // commit consumes prior outputs; entities -> structure disallowed unless
  // modeled as explicit second-pass / feedback (conceptual 1.2.3)
  return family_matrix[src_family][dst_family][edge_kind]  // planned artifact
```

```text
commit_wave_placement(waves, graph):
  // Commit-family nodes must not precede inputs they validate (1.2.2 schedule)
  // Reuse wave_partition output; assert commit nodes only after predecessors
  return validate_commit_ordering(waves, graph)
```

## Interfaces

| Direction | Contract |
| --- | --- |
| Upstream **1.2.1** | Families are **orthogonal labels** on `NodeRole` / node records; **EdgeKind** remains authoritative for DAG shape. |
| Upstream **1.2.2** | `execute_pass` / `wave_partition` / `subgraph_closure` apply unchanged; families constrain **documentation hooks** and **ordering assertions** for **commit**. |
| Upstream **secondary 1.2** | Injection hooks may be **family-scoped** in docs (e.g. post-structure, pre-entities); dry-run vs commit unchanged. |
| Downstream **1.2.4+** | Determinism / seed bundles may reference family-tagged stages — see conceptual [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-4-Determinism-Seed-Bundles-Stable-Identity-and-Replay-Contracts-Roadmap-2026-03-30-1930]]. |

## Tasks (tertiary execution breakdown)

| Task | Owner | Depends on | Target artifact |
| --- | --- | --- | --- |
| T-1.2.3-a | Roadmap agent / operator | **1.2.1** taxonomy | `family_tag_table.tsv` (E1) |
| T-1.2.3-b | Roadmap agent | T-1.2.3-a | `cross_family_rules.md` (E2) |
| T-1.2.3-c | Roadmap agent | **1.2.2** schedule | `commit_wave_placement.txt` (E3/E4) |
| T-1.2.3-d | Roadmap agent | T-1.2.3-b | `specialization_overlay.md` (E3) |

**GMM-2.4.5** / **CI** closure: **out of scope** for this slice (explicit deferral unchanged).

## Acceptance criteria — evidence hooks

| ID | Criterion | Evidence artifact (planned) | Status |
| --- | --- | --- | --- |
| AC-1.2.3.E1 | Every node has exactly one **primary** family in planned registry | Inline scaffold `family_tag_table.tsv` (see below) + export path `family_tag_table.tsv` | Scaffolded (inline evidence) |
| AC-1.2.3.E2 | Cross-family deps match conceptual allow/deny table | `cross_family_rules.md` | Planned |
| AC-1.2.3.E3 | Specialization overlays do not redefine edge kinds | `specialization_overlay.md` | Planned |
| AC-1.2.3.E4 | Commit-family ordering consistent with **1.2.2** waves | `commit_wave_placement.txt` | Planned |

## Intent Mapping

- **Design intent:** Keep **structure / entities / glue / commit** as a **minimum orchestration vocabulary** for procedural graph stages so specialization and cross-family rules stay legible against **1.2.1** taxonomy and **1.2.2** wave schedules — mirroring conceptual Phase-1-2-3 authority without smuggling edge-kind changes through “families.”
- **Inspiration anchor(s):**
  - **Halo 3–era encounter scripting (Bungie):** wave-based activation and layer staging as the mental model for “commit after prerequisites” (studied: public GDC/postmortem summaries of scripted wave orchestration in FPS encounters — used here only as **cadence**, not engine-specific API).
  - **Dwarf Fortress (Bay 12):** tick-ordered commits and rollback discipline as the analogy for **commit-family** nodes trailing inputs (studied: widely documented tick/update ordering mental model from DF dev logs / Classic community primers — **pattern only**, no DF code claims).
  - **Baldur’s Gate 3 / Larian-style pipeline staging:** modular system layers with explicit dependency staging (studied: high-level Larian pipeline postmortems / interviews on RPG system build order — used as **dependency-layer** inspiration for cross-family allow/deny).
- **Execution implementation:** `annotate_families` / `primary_family` invariants, `cross_family_allowed` matrix sketch, and `commit_wave_placement` checks tied to **1.2.2** `wave_partition` outputs; families remain **labels** on top of authoritative **EdgeKind** from **1.2.1**.
- **Validation signal:** At least one AC row carries **non-Planned** evidence (E1 scaffold below); remaining rows stay **Planned** until repo paths exist — explicit deferral contract preserved for **GMM-2.4.5 / CI** (out of scope this slice).

### Evidence scaffold — AC-1.2.3.E1 (inline)

Minimal tab-separated registry (v0; expands when implementation lands):

```tsv
node_id	primary_family	secondary_roles_note
example_structure_node_01	structure	—
example_entities_node_02	entities	validation-heavy tagging allowed (docs-only)
example_glue_node_03	glue	bridges entities→commit handoff
example_commit_node_04	commit	must follow predecessors per 1.2.2 waves
```

## Risks (v0)

- **Family explosion** before tooling exists — mitigate with **minimum set** (structure, entities, glue, commit) and optional sub-families only where PMG demands.
- **Dual-role ambiguity** — mitigate with single **primary** family + prose for validation-heavy nodes (conceptual 1.2.3).

## Related (execution spine)

- Prior **1.2.2**: [[Phase-1-2-2-Graph-Execution-Semantics-and-Subgraph-Runs-Roadmap-2026-04-11-0005]]
- Next tertiary **1.2.4** (determinism / replay): conceptual [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-4-Determinism-Seed-Bundles-Stable-Identity-and-Replay-Contracts-Roadmap-2026-03-30-1930]]

## Research integration

> [!note] External grounding
> **Recal remediation (queue `layer1-a5b-repair-recal-tertiary123-sandbox-20260411T151500Z`):** Intent Mapping now cites **studied design inspirations** (Halo-style wave cadence, DF tick-ordering analogy, Larian-style pipeline staging) per [[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Design-Intent-Alignment|Roadmap-Gate-Catalog-Design-Intent-Alignment]] — **pattern-level**, not engine API claims. No `Ingest/Agent-Research/` synthesis notes were required for this slice; verbatim **C/C++** citations remain for a future **Research-backed** pass when std/toolchain claims appear.
