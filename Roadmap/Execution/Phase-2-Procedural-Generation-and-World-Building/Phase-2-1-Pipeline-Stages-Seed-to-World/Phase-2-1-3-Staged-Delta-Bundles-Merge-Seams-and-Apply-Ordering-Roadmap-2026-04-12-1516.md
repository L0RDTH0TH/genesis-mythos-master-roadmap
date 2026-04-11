---
title: Phase 2.1.3 (Execution) — Staged delta bundles, merge seams, and apply ordering
created: 2026-04-12
tags:
  - roadmap
  - execution
  - sandbox
  - procedural-generation
  - phase-2-1-3
project-id: sandbox-genesis-mythos-master
roadmap_track: execution
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.1.3"
status: in-progress
handoff_readiness: 85
priority: high
progress: 40
conceptual_counterpart: "[[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-3-Staged-Delta-Bundles-Merge-Seams-and-Apply-Ordering-Roadmap-2026-03-30-1041]]"
para-type: Project
links:
  - "[[Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-11-2359]]"
  - "[[Phase-2-1-1-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-04-12-1825]]"
  - "[[Phase-2-1-2-Boundary-Hook-Labels-and-Staged-Delta-Merge-Seams-Roadmap-2026-04-11-2100]]"
---

# Phase 2.1.3 (Execution) — Staged delta bundles, merge seams, and apply ordering

Execution tertiary **2.1.3** on the parallel spine under `Phase-2-1-Pipeline-Stages-Seed-to-World/`, mirroring conceptual **2.1.3** ([[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-3-Staged-Delta-Bundles-Merge-Seams-and-Apply-Ordering-Roadmap-2026-03-30-1041]]). This slice makes **StagedDeltaBundle** assembly, **merge seam** fan-in, and **canonical apply ordering** explicit for execution—**text-only** interface contracts and `text` pseudocode only (no verbatim C++; **sandbox_code_precision** deferred). Aligns to Phase **2** primary + Phase **1.2.x** graph vocabulary + **2.1.1**/**2.1.2** seams.

## Scope (execution)

**In scope:**

- **StagedDeltaBundle** as the single pre-commit container aggregating typed fragments from Stages **0–3** (evaluated through **2.1.1** stage-family bodies) before Stage **4** validation and **2.1.2** label + merge-seam story.
- **Merge seam catalog:** named **MergeSeamId** fan-in points with explicit rule families (no silent last-writer-wins)—consistent with **2.1.2** “no silent winner” merge seam semantics.
- **Apply ordering:** total or partial order over **ApplyOp** entries inside the bundle: default **topological over stage spine** (Stage **0→5**), then within-stage ordering for disjoint domains (named **domainTag** / **orderingKey**).
- **ValidationDecisionLabels** (from **2.1.2**) attach at **bundle** level and optionally per seam so explainability survives aggregation.

**Out of scope:**

- Verbatim C++, `static_assert`, or allowlisted URL citations (**sandbox_code_precision** — future slice with nested **Task(research)**).
- **GMM-2.4.5** / registry–CI closure rows (**execution-deferred** unless evidenced).
- Binary patch formats, CRDT/ECS storage schemas, asset pipeline IDs (per conceptual **Out of scope**).

## Behavior (execution contract)

Actors: **pipeline runner** (assembles bundle), **stage evaluators** (typed fragments), **dry-run validator (Stage 4)** (evaluates **whole bundle + labels**), **commit boundary (Stage 5)** (consumes **one** allowed bundle).

**Bundle assembly story (execution):**

1. Collect **typed stage fragments** after Stage **2/3** evaluation into a working set keyed by **stageIndex** + **domainTag**.
2. For each **MergeSeamId** in **topological_seam_order(seamCatalog)**, apply declared merge rule → append **seamRecords[]** with explicit **resolution record** when conflicts arise (else Stage **4** denies).
3. Emit **applyOpsOrdered[]** via **total_order** defaulting to **stage spine order**; allow partial order only when fragments are provably disjoint (named disjointness in bundle).
4. Attach **ValidationDecisionLabels** at bundle level; **CommitAllowed** false collapses bundle to empty / no-op apply list (consistent with **2.1.2**).

**Regeneration:** Same **seed bundle identity** + **intent hook set** + **seam catalog** → same **bundleIdentity** digest and seam-level resolution records (aligns **1.2.4** replay vocabulary).

## Interfaces (text — depth-3 tertiary)

Natural-language shapes (not APIs):

- **`StagedDeltaBundle`:** `{ bundleIdentity, seamRecords[], applyOpsOrdered[], validationLabels, sourceStages[] }`
- **`MergeSeamId`:** stable string (e.g. `terrain+biome@regionA`)
- **`ApplyOp`:** `{ opId, stageIndex, seamId?, domainTag, fragmentRef, orderingKey }`
- **`SeamResolutionRecord`:** explicit policy outcome when two fragments touch the same conceptual key (never implicit pick)

Upstream:

- **2.1.1** — stage-family bodies and boundary hooks feed fragment shapes.
- **2.1.2** — **ValidationDecisionLabels** + merge seam inputs before Stage **5** token.

Downstream:

- Stage **5** consumes **one** validated bundle (or rejects); **sharded commit** remains out of scope unless PMG adds (per conceptual open question).

## Edge cases (execution)

- **Empty bundle:** valid no-op; Stage **4** still evaluates so labels can read **no-op** (per conceptual).
- **Conflicting fragments without resolution record:** Stage **4** denies; no partial application.
- **Label/bundle hash mismatch:** fail closed—block commit (extends **2.1.2** label vs delta mismatch story to **whole-bundle** identity).

## Pseudocode readiness (text — no verbatim C++)

```text
assemble_bundle(stage_fragments[], seam_catalog, intent_context):
  bundle = empty StagedDeltaBundle
  for seam_id in topological_seam_order(seam_catalog):
    merged = apply_merge_rule(seam_id, fragments_touching(seam_id), intent_context)
    if merged.conflict_unresolved:
      return blocked_bundle(validation_labels=deny_labels)
    bundle.seamRecords.append(merged)
  bundle.applyOpsOrdered = total_order(bundle, default=stage_spine_order)
  bundle.validationLabels = attach_labels(bundle)
  return bundle
```

Verbatim C++ / standard quotes → later slice with **Task(research)** + allowlisted citations per **sandbox_code_precision**.

## Acceptance criteria (execution-first)

| ID | Criterion | Evidence target | Status |
| --- | --- | --- | --- |
| AC-2.1.3.E1 | Bundle identity is stable hash of seam records + apply op list + seed/intent inputs | `bundle_identity_digest` | Scaffolded (inline) — receipt: [[../../../workflow_state-execution]] log row **2026-04-12 15:16** (`queue_entry_id: followup-deepen-exec-phase2-tertiary213-sandbox-20260412T151600Z`) |
| AC-2.1.3.E2 | Merge seams never apply implicit LWW; conflicts require resolution record or Stage **4** deny | `seam_resolution_or_deny_trace` | Planned |
| AC-2.1.3.E3 | Apply ordering defaults to stage spine; partial order only when disjointness named | `apply_order_graph_export` | Planned |
| AC-2.1.3.E4 | Replay: same inputs → same bundleIdentity + seam records | `replay_bundle_digest` | Planned |

## Intent Mapping

| Design intent target | Inspiration anchors | Execution mechanism | Validation signal |
| --- | --- | --- | --- |
| Single pre-commit bundle | Conceptual **2.1.3** NL + deterministic pipelines | `assemble_bundle` + `StagedDeltaBundle` | AC-2.1.3.E1 |
| Explicit merge seams | **2.1.2** merge seam + **1.2** skip semantics | `seam_catalog` + `seamRecords` | AC-2.1.3.E2 |
| Ordering for replay/tooling | Topological stage order + disjoint partial order | `applyOpsOrdered` | AC-2.1.3.E3–E4 |

## Lane comparand

| Concern | Sandbox (this lane) | Godot (reference) | Shared contract |
| --- | --- | --- | --- |
| Bundle assembly | Typed fragments + seam catalog | Resource staging / import bundles | Deterministic replay |
| Apply order | Stage spine first | Scene tree / dependency order | No implicit ordering |

## Related

- Parent secondary **2.1:** [[Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-11-2359]]
- Upstream tertiaries: [[Phase-2-1-1-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-04-12-1825]], [[Phase-2-1-2-Boundary-Hook-Labels-and-Staged-Delta-Merge-Seams-Roadmap-2026-04-11-2100]]
- Phase **2** primary: [[../../Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-04-11-1432]]
- Phase **1.2** graph: [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-04-10-2355]]
