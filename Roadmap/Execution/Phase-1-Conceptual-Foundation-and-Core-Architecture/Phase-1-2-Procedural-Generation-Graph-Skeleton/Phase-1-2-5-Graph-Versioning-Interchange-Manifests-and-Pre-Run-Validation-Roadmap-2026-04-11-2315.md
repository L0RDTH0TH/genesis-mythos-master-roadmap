---
title: Phase 1.2.5 (Execution) — Graph versioning, interchange manifests, pre-run validation
created: 2026-04-11
tags:
  - roadmap
  - execution
  - sandbox
  - procedural-generation
  - graph
  - versioning
project-id: sandbox-genesis-mythos-master
roadmap_track: execution
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.2.5"
status: in-progress
handoff_readiness: 87
handoff_readiness_basis: design_traceability_pre_evidence
handoff_readiness_note: "Slice minted on execution spine with Intent Mapping + AC table; text-only validation/manifest seams (no verbatim C++ this pass — Research-backed precision deferred)."
conceptual_counterpart: "[[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-5-Graph-Versioning-Interchange-Manifests-and-Pre-Run-Validation-Roadmap-2026-03-30-2015]]"
---

# Phase 1.2.5 (Execution) — Graph versioning, interchange manifests, pre-run validation

Execution tertiary **1.2.5** on the **parallel spine**, aligned to conceptual [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-5-Graph-Versioning-Interchange-Manifests-and-Pre-Run-Validation-Roadmap-2026-03-30-2015]]. Focus: **schema generation** labels for graph definitions, **interchange manifest** fields (closure, seed refs, stage-family tags, hook IDs), and **pre-run static validation** before committed execution — consistent with **1.2.1–1.2.4** upstream seams. **File formats**, **hashing**, and **CI/registry closure** remain **explicitly deferred** unless evidenced later.

Upstream **1.2.4** execution: [[Phase-1-2-4-Determinism-Seed-Bundles-Stable-Identity-and-Replay-Contracts-Roadmap-2026-04-11-2240]] · Parent secondary **1.2**: [[Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-04-10-2355]] · Phase 1 execution primary: [[../Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-04-10-2100]]

## Handoff readiness vs evidence

**Handoff readiness** is **design- and traceability-first** (versioning rules, manifest rows, validation predicates). **AC** rows begin **Planned** until repo artifacts attach. Automation **next** structural target after Phase **1.2** chain completion: **Phase 2 execution** mirror — see [[../../workflow_state-execution]].

## Alignment to conceptual Phase-1-2-5

| Conceptual contract | Execution mechanism (this note) | Validation signal |
| --- | --- | --- |
| Schema generation / breaking vs additive | `graph_schema_generation` + compatibility policy text | AC-1.2.5.E1 |
| Interchange manifest minimal bundle | `interchange_manifest` field list + binding to **1.2.4** seed refs | AC-1.2.5.E2 |
| Pre-run static validation (DAG, hooks, families) | `validate_graph_static` text predicate suite | AC-1.2.5.E3 |

## Mid-technical seams (text-only)

**Depth 3:** sketches in **`text`** blocks only — same deferral as **1.2.2–1.2.4**: no committed C++ standard-library claims in this slice; a future **nested `Task(research)`** pass with **sandbox allowlisted** URLs may attach verbatim citations when implementation binds to concrete `std::` or ABI surfaces.

```text
validate_graph_static(gdef) -> Diagnostic[]:
  diags := []
  diags += acyclicity_check(gdef)           // 1.2.2 closure
  diags += topo_feasibility_check(gdef)     // waves/prefix vs 1.2.2
  diags += edge_kind_shape_check(gdef)     // 1.2.1 taxonomy
  diags += hook_resolution_check(gdef)      // named hooks from secondary 1.2
  diags += stage_family_consistency(gdef)   // 1.2.3 tags vs commit families
  diags += nondeterminism_labels_check(gdef) // 1.2.4 tags
  return diags
```

```text
InterchangeManifest.from(graph, seed_bundle_ref):
  manifest.schema_generation = graph.schema_generation
  manifest.subgraph_closure = subgraph_closure(graph)    // 1.2.2
  manifest.seed_bundle_ref = seed_bundle_ref               // 1.2.4
  manifest.stage_families = stage_family_tags(graph)      // 1.2.3
  manifest.hook_ids = declared_hooks(graph)
  return manifest
```

```text
compatibility_ok(consumer_gen, producer_gen, node_kind):
  return matrix_allows(consumer_gen, producer_gen, node_kind)  // doc-first until registry
```

## Interfaces

| Direction | Contract |
| --- | --- |
| Upstream **1.2.4** | Manifest preserves **seed bundle identity** and replay class for exchange equivalence. |
| Upstream **1.2.3** | **Stage family** / pipeline-role tags feed validation and compatibility rows. |
| Upstream **1.2.1–1.2.2** | Taxonomy + subgraph semantics define **static** predicates. |
| Downstream **Phase 2** | Serialization, golden manifests, registry IDs **bind** these NL contracts to artifacts. |

## Tasks (tertiary execution breakdown)

| Task | Owner | Depends on | Target artifact |
| --- | --- | --- | --- |
| T-1.2.5-a | Roadmap agent / operator | **1.2.1–1.2.2** | `graph_schema_generation_policy.md` (E1) |
| T-1.2.5-b | Roadmap agent | T-1.2.5-a + **1.2.4** | `interchange_manifest_fields.tsv` (E2) |
| T-1.2.5-c | Roadmap agent | **1.2.3** + T-1.2.5-b | `static_validation_predicates.md` (E3) |

## Acceptance criteria — evidence hooks

| ID | Criterion | Evidence artifact (planned) | Status |
| --- | --- | --- | --- |
| AC-1.2.5.E1 | Schema generation + compatibility policy documented | `graph_schema_generation_policy.md` | Planned |
| AC-1.2.5.E2 | Interchange manifest enumerates closure, seeds, families, hooks | `interchange_manifest_fields.tsv` | Planned |
| AC-1.2.5.E3 | Static validation predicates cover DAG, hooks, families, nondeterminism labels | `static_validation_predicates.md` | Planned |

## Intent Mapping

- **Design intent:** Make **graph evolution** and **tool-to-tool exchange** safe by versioning schema generations, bundling **minimal reconstructable** metadata with each fragment, and **rejecting invalid graphs before run** — mirroring conceptual Phase-1-2-5 authority.
- **Inspiration anchor(s):**
  - **Package / manifest patterns (npm, cargo):** semver-ish **breaking vs additive** mental model for schema generations (pattern only — no format lock).
  - **Build-graph static checks:** fail-fast validation before expensive execution (pattern only).
- **Execution implementation:** `validate_graph_static` diagnostic bundle; `InterchangeManifest.from` tying **1.2.2** closure + **1.2.4** seeds + **1.2.3** tags; compatibility matrix as **documentation-first** until registry.
- **Validation signal:** AC table remains **Planned** until repo paths exist — explicit deferral for **binary hashes / CI** unchanged.

## Risks (v0)

- **Version skew** — mitigate with default **disallow mixed-generation** unless adapter stages exist (execution-deferred).
- **Thin manifest** — mitigate with explicit **context required** diagnostics for partial imports (conceptual edge case).

## Related (execution spine)

- Prior **1.2.4**: [[Phase-1-2-4-Determinism-Seed-Bundles-Stable-Identity-and-Replay-Contracts-Roadmap-2026-04-11-2240]]
- Phase **1.2** chain **complete** on execution spine — next: **Phase 2** execution mirror per [[../../workflow_state-execution]]

## Research integration

> [!note] External grounding
> This mint uses **text-only** sketches (no verbatim C++ / headers). A future **nested `Task(research)`** pass with **sandbox allowlisted** URLs may attach standard-library citations if implementation binds to concrete facilities — per [[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Sandbox-Execution|Roadmap-Gate-Catalog-Sandbox-Execution]].
