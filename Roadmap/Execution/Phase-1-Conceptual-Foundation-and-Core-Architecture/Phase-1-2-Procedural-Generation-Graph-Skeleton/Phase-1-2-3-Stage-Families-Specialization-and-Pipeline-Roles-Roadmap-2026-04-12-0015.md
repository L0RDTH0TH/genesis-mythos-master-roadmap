---
title: Phase 1.2.3 (Execution) — Stage families specialization and pipeline roles
created: 2026-04-12
tags:
  - roadmap
  - execution
  - godot
  - sandbox-comparand
project-id: godot-genesis-mythos-master
roadmap_track: execution
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.2.3"
status: in-progress
handoff_readiness: 85
conceptual_counterpart: "[[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-3-Stage-Families-Specialization-and-Pipeline-Roles-Roadmap-2026-03-30-1905]]"
execution_mirror_of: "Phase-1-2-3-Stage-Families-Specialization-and-Pipeline-Roles-Roadmap-2026-03-30-1905"
---

# Phase 1.2.3 (Execution) — Stage families specialization and pipeline roles

Execution remint for **tertiary 1.2.3** on the parallel spine. Binds conceptual **stage families** (**structure**, **entities**, **glue**, **commit**), **specialization** labels, and **pipeline roles** to lane-neutral registry + validation contracts, with **Godot stable** **`Node.add_to_group`** / **`SceneTree.get_nodes_in_group`** verbatim anchors as a **hosting metaphor** for tagging and querying stages by family (not a claim that proc-gen stages are scene nodes). **`missing_roll_up_gates`**, family-ID **registry CI**, and rollup **verdict closure** remain **execution-deferred** per **D-Exec-rollup-deferral-missing-roll-up-gates-20260411** — **not** claimed closed in-doc.

Parent secondary: [[Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-04-11-2230]] · Prior tertiary: [[Phase-1-2-2-Graph-Execution-Semantics-and-Subgraph-Runs-Roadmap-2026-04-11-2345]] · Decisions: [[../../../decisions-log]].

## Intent mapping

| Intent target | Inspiration anchors | Execution mechanism | Validation signal |
| --- | --- | --- | --- |
| Primary family per stage | Conceptual 1.2.3 NL | Each `StageId` maps to **`StageFamily`** enum + optional **`SpecializationTag`** set; exactly one **primary** family for scheduling docs | Lint table: primary family column non-empty |
| Cross-family deps | Conceptual cross-family rules | **Validate** edges against allow-matrix: **entities** must not depend on **structure** feedback without **macro-pass** / explicit **ordering_only** seam from **1.2.1** | Matrix audit row + forbidden-edge detector (execution-deferred CI) |
| Commit ordering | **1.2.2** failure propagation | **Commit**-family stages ordered **after** all producers of authoritative store inputs in subgraph closure | Dry-run vs commit mode bit on `run_stage` |
| Godot hosting metaphor | Scene tree groups | Stages “join” **family groups** analogously to nodes in groups; **query all in family** for tooling — cites below | Verbatim citations block |

## Scope

- **In:** Lane-neutral **`declare_stage_family`**, **`validate_cross_family_edge`**, **`specialization_of`** pseudocode; family ↔ **1.2.1** node-kind compatibility table (orthogonal labels).
- **Out:** Stable family ID registry closure, shader/simulation families, or **claims** that **`missing_roll_up_gates`** / rollup HR are satisfied.

## Lane-neutral family registry (sketch)

```text
enum StageFamily { STRUCTURE, ENTITIES, GLUE, COMMIT }
type SpecializationTag = string  # e.g. "biome", "prop_batch"

function declare_stage_family(stage_id, primary: StageFamily, specs: Set<SpecializationTag>):
  registry[stage_id] = (primary, specs)

function validate_cross_family_edge(a, b, edge_kind_from_121, families):
  # Conceptual rule: no entities -> structure without explicit feedback/macro-pass
  if families[b].primary == STRUCTURE and families[a].primary == ENTITIES:
    if edge_kind_from_121 not in {DEP, ORDERING_ONLY_WITH_FEEDBACK}:
      signal_forbidden_cross_family(a, b)
```

**Specialization** refines human/tooling docs only; **does not** replace **1.2.1** edge kinds.

## Failure / ordering alignment

- **Commit** family stages align with **1.2.2** empty/fail propagation: a **commit** stage cannot authorize world commit if upstream **structure/entities** produced typed empty within the same subgraph policy.

## Godot lane (A) — verbatim anchors (stable docs)

**Tagging stages into named sets** — `add_to_group` documents adding a node to a named group for organization; use as **metaphor** for attaching a proc-gen **stage** to a **family** label for queries and editor tooling:

> Adds the node to the `group`. Groups can be helpful to organize a subset of nodes, for example `"enemies"` or `"collectables"`. See notes in the description, and the group methods in [SceneTree](https://docs.godotengine.org/en/stable/classes/class_scenetree.html#class-scenetree).
>
> If `persistent` is `true`, the group will be stored when saved inside a [PackedScene](https://docs.godotengine.org/en/stable/classes/class_packedscene.html#class-packedscene). All groups created and displayed in the Groups dock are persistent.
>
> Note: To improve performance, the order of group names is not guaranteed and may vary between project runs. Therefore, do not rely on the group order.

Source: [Node — add_to_group — Godot Engine stable class reference](https://docs.godotengine.org/en/stable/classes/class_node.html#class-node-method-add-to-group)

**Querying all members of a family set** — `get_nodes_in_group` returns nodes in hierarchy order; metaphor for “enumerate all stages in family X” for static analysis / graph visualization:

> Returns an [Array](https://docs.godotengine.org/en/stable/classes/class_array.html#class-array) containing all nodes inside this tree, that have been added to the given `group`, in scene hierarchy order.

Source: [SceneTree — get_nodes_in_group — Godot Engine stable class reference](https://docs.godotengine.org/en/stable/classes/class_scenetree.html#class-scenetree-method-get-nodes-in-group)

**Binding:** Runtime proc-gen remains the **lane-neutral kernel** from **1.2**/**1.2.1**/**1.2.2**; these Godot quotes justify **named-set tagging and enumeration** — **not** that generation stages are `Node` instances.

## Sandbox lane (B) — comparand

| Element | B-lane stand-in |
| --- | --- |
| Family | `enum class StageFamily` + `std::unordered_map<StageId, std::pair<StageFamily, std::set<std::string>>>` |
| Query | Iterate registry filter `primary == STRUCTURE` |

## Acceptance criteria

| ID | Criterion | Evidence | Status |
| --- | --- | --- | --- |
| AC-1.2.3-A | Four family buckets + specialization sketch documented | Sections + pseudocode | Met |
| AC-1.2.3-B | Cross-family edge rule called out | `validate_cross_family_edge` | Met |
| AC-1.2.3-C | Godot verbatim citations present (`add_to_group`, `get_nodes_in_group`) | Blockquotes + stable URLs | Met |
| AC-1.2.3-D | Rollup / CI / family-registry closure **not** claimed | Deferral callout | Met |

## Roll-up / CI / registry IDs (explicit deferral)

Open **`GMM-2.4.5-*`**, graph **`missing_roll_up_gates`**, stable **family-ID registry** CI, and rollup **verdict closure** remain **execution-deferred** until real **CI run IDs** and verdict tables land — per **D-Exec-rollup-deferral-missing-roll-up-gates-20260411**.

Advisory: matrix-audit and forbidden-edge detector signals remain **UNKNOWN** until the same execution-deferred CI bundle lands — not treated as an undocumented design gap in this note.

## Tasks

1. - [ ] Implement or document `declare_stage_family` + per-`StageId` registry map shape aligned to **1.2.1** node kinds.
2. - [ ] Implement or document `validate_cross_family_edge` against the conceptual allow-matrix (entities → structure feedback rules).
3. - [ ] Add lint / table contract: every stage row exposes a non-empty **primary family** column for tooling.
4. - [ ] Document **commit** vs **dry-run** ordering vs **1.2.2** subgraph + failure propagation for **COMMIT** family stages.
5. - [ ] Keep Godot **groups** block strictly **metaphor-only** (no claim that stages are `Node` instances).
6. - [ ] Maintain B-lane comparand parity for family enum + query patterns.

## Test plan (stub — CI deferred)

| Check | Signal / fixture | Expected | Status |
| --- | --- | --- | --- |
| Primary family lint | Table of `StageId` → family | No empty primary family | **PENDING** (execution-deferred CI) |
| Forbidden cross-family edge | Synthetic **entities → structure** dep without macro-pass | Detector flags | **PENDING** (execution-deferred CI) |
| Commit order dry-run | Subgraph with **COMMIT** last | No commit before producers | **PENDING** (execution-deferred CI) |

Rollup / registry rows remain **D-Exec**-deferred; this table defines harness shape only — **not** “tests passed.”

## Next structural intent

Tertiary **1.2.4** — determinism, seed bundles, stable identity, replay contracts (conceptual mirror: `Phase-1-2-4-*`). Queue follow-up should target **`next_subphase_index: "1.2.4"`** unless operator overrides.

## Related

- Conceptual authority: [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-3-Stage-Families-Specialization-and-Pipeline-Roles-Roadmap-2026-03-30-1905]]
- Upstream execution: [[Phase-1-2-2-Graph-Execution-Semantics-and-Subgraph-Runs-Roadmap-2026-04-11-2345]]
