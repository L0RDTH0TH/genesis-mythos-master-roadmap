---
title: Phase 1.2.5 (Execution) — Graph versioning, interchange manifests, and pre-run validation
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
subphase-index: "1.2.5"
status: in-progress
handoff_readiness: 85
conceptual_counterpart: "[[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-5-Graph-Versioning-Interchange-Manifests-and-Pre-Run-Validation-Roadmap-2026-03-30-2015]]"
execution_mirror_of: "Phase-1-2-5-Graph-Versioning-Interchange-Manifests-and-Pre-Run-Validation-Roadmap-2026-03-30-2015"
---

# Phase 1.2.5 (Execution) — Graph versioning, interchange manifests, and pre-run validation

Execution remint for **tertiary 1.2.5** on the parallel spine — closes the **1.2** procedural-graph tertiary chain on the execution mirror. Binds **schema generation** / compatibility labels, **interchange manifest** payloads (closure + seed-bundle refs + family tags + hooks), and **static pre-run validation** predicates to lane-neutral sketches, with **Godot stable** **`JSON` parse** and **`ResourceLoader` load** verbatim anchors as **hosting metaphors** for *parse-time manifest checks* and *path-resolved resource identity* — **not** a claim that interchange artifacts are Godot `Resource` subclasses. **`missing_roll_up_gates`**, manifest-hash **CI**, schema-diff **CI**, and rollup **verdict closure** remain **execution-deferred** per **D-Exec-rollup-deferral-missing-roll-up-gates-20260411** — **not** claimed closed in-doc.

Parent secondary: [[Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-04-11-2230]] · Prior tertiary: [[Phase-1-2-4-Determinism-Seed-Bundles-Stable-Identity-and-Replay-Contracts-Roadmap-2026-04-12-0205]] · Decisions: [[../../../decisions-log]].

## Intent mapping

| Intent target | Inspiration anchors | Execution mechanism | Validation signal |
| --- | --- | --- | --- |
| Graph definition version | Conceptual major/minor NL | `GraphSchemaVersion { major, minor, compat_matrix_ref }` carried on manifest | Refuse / adapt table stub |
| Interchange manifest | **1.2.2** closure + **1.2.4** bundle + **1.2.3** families | `InterchangeManifest` lists subgraph closure, `SeedBundleRef`, stage families, hook ids | Lint: manifest covers evaluation intent |
| Pre-run static validation | **1.2.1** taxonomy + **1.2.4** nondet tags | `validate_graph_static(gdef) -> Diagnostic[]` before committed run | Blocking diagnostics stub |
| Godot hosting metaphor | Parse + load docs | **`JSON.parse`** + **`ResourceLoader.load`** quotes justify *strict parse failures* and *path-based load* — cites below | Verbatim citations block |

## Scope

- **In:** Lane-neutral `GraphSchemaVersion`, `InterchangeManifest`, `validate_graph_static` signatures; compatibility refusal rules; static checks: DAG, topo feasibility, edge shapes, hook resolution, nondeterminism labels per **1.2.4**.
- **Out:** File extensions, canonical hashing, golden manifest **CI**, plugin ABI, registry-backed proofs.

## Lane-neutral versioning + manifest (sketch)

```text
type GraphSchemaVersion = { major: int, minor: int, compat_notes: string }

type InterchangeManifest = {
  schema: GraphSchemaVersion,
  subgraph_closure: Set<StageId>,     # from 1.2.2
  seed_bundle_ref: SeedBundleRef,     # from 1.2.4
  stage_families: Map<StageId, FamilyTag>,  # from 1.2.3
  hook_bindings: Map<HookId, StageId>,
}

function validate_graph_static(gdef: GraphDef) -> Diagnostic[]:
  diagnostics = []
  diagnostics += dag_checks(gdef)           # align 1.2.1 + 1.2.2
  diagnostics += hook_resolution_checks(gdef)
  diagnostics += nondeterminism_labels_ok(gdef)  # 1.2.4 policy matrix
  return diagnostics
```

**Version skew:** mixed-generation nodes default **disallowed** unless explicit adapter stages (**execution-deferred** adapter registry).

## Pre-run vs dry-run

- **Static (this slice):** Cheap predicates before any scheduling (**1.2.2** waves) — required first.
- **Dry-run (primary glue / 1.2 secondary):** May exercise more than static checks; must share determinism semantics with **1.2.4** bundles.

## Godot lane (A) — verbatim anchors (stable docs)

**Strict JSON parsing** — use as metaphor that **manifest bytes** must parse cleanly or surface **Error** (aligns with “blocking diagnostics”):

> Parses a JSON encoded string and returns the result as a **Variant**.

Source: [JSON — parse — Godot Engine stable class reference](https://docs.godotengine.org/en/stable/classes/class_json.html#class-json-method-parse)

**Load a resource from the filesystem** — use as metaphor for **resolving** a manifest / bundle **path** into a typed handle (lane-neutral manifest remains authoritative):

> Loads a resource from the given **path**.

Source: [ResourceLoader — load — Godot Engine stable class reference](https://docs.godotengine.org/en/stable/classes/class_resourceloader.html#class-resourceloader-method-load)

**Binding:** Lane-neutral `InterchangeManifest` + validation predicates remain authoritative; Godot quotes illustrate **parse-time failure surfaces** and **path load** — **not** that interchange is Godot `Resource` assets.

## Sandbox lane (B) — comparand

| Element | B-lane stand-in |
| --- | --- |
| Manifest parse | `nlohmann::json::parse` with strict exceptions |
| Version tuple | `struct Version { uint16_t major, minor; }` |
| Static validation | constexpr / build-graph lint pass before link |

## Acceptance criteria

| ID | Criterion | Evidence | Status |
| --- | --- | --- | --- |
| AC-1.2.5-A | Version + manifest structs sketched | Sections + pseudocode | Met |
| AC-1.2.5-B | Pre-run static validation signature + predicate classes | `validate_graph_static` + table | Met |
| AC-1.2.5-C | Godot verbatim citations present (`JSON.parse`, `ResourceLoader.load`) | Blockquotes + stable URLs | Met |
| AC-1.2.5-D | Rollup / CI / schema-diff closure **not** claimed | Deferral callout | Met |

## Roll-up / CI / registry IDs (explicit deferral)

Open **`GMM-2.4.5-*`**, graph **`missing_roll_up_gates`**, manifest-hash **CI**, and rollup **verdict closure** remain **execution-deferred** until real **CI run IDs** and verdict tables land — per **D-Exec-rollup-deferral-missing-roll-up-gates-20260411**.

## Tasks

1. - [ ] Align `GraphSchemaVersion` rows with conceptual compatibility NL (major/minor semantics).
2. - [ ] Bind `InterchangeManifest` fields to **1.2.2** closure + **1.2.4** refs + **1.2.3** family map.
3. - [ ] Implement or document `validate_graph_static` checklist: DAG, hooks, nondet labels.
4. - [ ] Keep Godot block strictly **metaphor** (no claim that manifests are engine `Resource`s).
5. - [ ] Maintain B-lane JSON/version parity sketches.

## Test plan (stub — CI deferred)

| Check | Signal / fixture | Expected | Status |
| --- | --- | --- | --- |
| Manifest parse failure | Invalid interchange bytes | Diagnostics, no run | **PENDING** |
| Version skew | Mixed-gen without adapter | Blocked | **PENDING** |
| Static vs dry-run | Same bundle | No divergence class | **PENDING** |

## Related

- Conceptual counterpart: [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-5-Graph-Versioning-Interchange-Manifests-and-Pre-Run-Validation-Roadmap-2026-03-30-2015]]
- Phase 1 primary glue (next structural focus): [[../../Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-04-10-2100]] — safety invariants + dry-run sections bind here.
