---
title: Phase 1.2.3 — Stage families, specialization, and pipeline roles
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.2.3"
project-id: godot-genesis-mythos-master
status: active
priority: high
progress: 40
handoff_readiness: 78
created: 2026-03-30
tags:
  - roadmap
  - godot-genesis-mythos-master
  - phase-1
para-type: Project
links:
  - "[[Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-03-30-1605]]"
  - "[[Phase-1-2-2-Graph-Execution-Semantics-and-Subgraph-Runs-Roadmap-2026-03-30-1805]]"
  - "[[Phase-1-2-1-Node-Taxonomy-Edges-and-Topological-Order-Roadmap-2026-03-30-1705]]"
  - "[[Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-03-30-0430]]"
---

## Phase 1.2.3 — Stage families, specialization, and pipeline roles

This tertiary slice assigns **stage families** and **pipeline roles** so implementation teams can group nodes consistently: which stages belong to **world-structure** pipelines (e.g. biome / terrain masks), which to **entity / population** pipelines, which are **glue or narrative overlay**, and which are **commit / validation** gates—using **1.2.1** taxonomy and **1.2.2** execution semantics without fixing engine-specific modules.

## Scope

**In scope:** Family definitions (minimum set: **structure**, **entities**, **glue**, **commit**); **role tags** compatible with **1.2.1** node kinds; **cross-family edges** rules (what may depend on what); **specialization** as optional sub-families (e.g. biome vs cave vs weather under **structure**). **Out of scope:** Asset IDs, shader stages, simulation ticks. **Execution-deferred:** registry of stable family IDs, CI lint that every node declares exactly one primary family.

## Behavior (natural language)

- Each **stage** declares a **primary family** and optionally **secondary roles** (e.g. “structure + validation-lite”) for documentation; **execution** may collapse to a single authoritative family per node.
- **Structure family:** Stages that derive **spatial / mask / field** outputs consumed by later world-structure or entity stages (seed expansion, biome assignment, heightfield or mask passes that are not yet entity spawn).
- **Entities family:** Stages that **spawn, parameterize, or batch** entities and props from structure outputs; may not run before required structure inputs exist (per **1.2.2** subgraph closure).
- **Glue family:** Narrative, quest, or **overlay** stages that attach to hooks from **1.2** but must not silently mutate authoritative world state without passing through **commit**-family stages.
- **Commit family:** Validation, snapshot, and **authoritative world commit** boundaries—ordered last among consumers of a subgraph when the run is not dry-run; aligns with **1.2.2** failure/empty propagation.
- **Specialization:** Sub-families (e.g. **biome** vs **prop placement** under **entities**) refine **scheduling and dependency** expectations but **do not** override **1.2.1** edge kinds—only annotate nodes for humans and tooling.

## Interfaces

- **Upstream (1.2.1):** Node taxonomy and edge kinds; families are **orthogonal labels** on nodes, not a replacement for edge types.
- **Upstream (1.2.2):** Execution passes and subgraph closure apply **per family** only insofar as **commit** stages must remain ordered after their inputs; parallel waves still respect **1.2.2** tie-break rules.
- **Upstream (secondary 1.2):** Injection hooks may be **family-scoped** in documentation (e.g. “hook after structure.biome, before entities.spawn”).
- **Downstream (1.2.4+):** May map families to **Phase 2** module boundaries or vertical-slice scope lists.

## Edge cases

- **Cross-family dependency:** Allowed when **1.2.1** dependency edges justify it; **glue** → **entities** is common; **entities** → **structure** is **disallowed** unless modeled as explicit **feedback** or a **second pass** (see **1.2** macro-pass).
- **Dual role nodes:** A node that both **prepares** and **validates** should still declare **one** primary family; validation-heavy behavior is called out in body text to avoid ambiguous **commit** ordering.
- **Empty specialization:** If a vertical slice uses only **structure + commit**, **entities** / **glue** families may be **explicitly empty** with a one-line contract—no silent omission.

## Open questions

- Whether **simulation-facing** generation (post-commit loops) gets its own family or stays **glue** until Phase 3—**design choice** when Phase 2 scopes MVP.
- **Minimum family set** for first playable: likely **structure + commit**; **entities** optional for empty-world tests—**PMG** alignment TBD.

## Pseudo-code readiness

Readers can sketch **tables** mapping node names → family + specialization and **lint rules** (“no entity before structure output X”). No runtime code.

## Research integration

> [!note] External grounding
> No `Ingest/Agent-Research/` notes were bound this run; alignment is **pattern-only** from build pipelines (e.g. codegen families), game layer cake, and staged content pipelines.
