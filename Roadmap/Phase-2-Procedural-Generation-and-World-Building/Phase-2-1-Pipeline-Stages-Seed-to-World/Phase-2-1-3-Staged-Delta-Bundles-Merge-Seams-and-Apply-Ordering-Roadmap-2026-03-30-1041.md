---
title: Phase 2.1.3 — Staged delta bundles, merge seams, and apply ordering
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.1.3"
project-id: sandbox-genesis-mythos-master
status: active
priority: high
progress: 38
handoff_readiness: 76
created: 2026-03-30
tags:
  - roadmap
  - sandbox-genesis-mythos-master
  - phase-2
para-type: Project
links:
  - "[[Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-03-30-2205]]"
---

## Phase 2.1.3 — Staged delta bundles, merge seams, and apply ordering

This tertiary closes the **composition** gap left after **2.1.1** (typed staged outputs + commit boundary token) and **2.1.2** (validation labels + boundary-hook surfaces): it defines how multiple stage outputs are **bundled**, where **merge seams** sit in the spine, and the **canonical apply ordering** for staged deltas **before** the commit boundary consumes them.

## Scope

**In scope:**
- **StagedDeltaBundle** as the conceptual container for all pre-commit mutations produced by Stages 0–3 (and validated by Stage 4) — a single logical artifact the dry-run gate can evaluate as a whole.
- **Merge seams**: named fan-in points where outputs from earlier stages (or parallel stage-family subgraphs, when used) combine into one bundle with deterministic merge rules.
- **Apply ordering**: total or partial order over staged operations inside the bundle so replay and tooling can reason about “what would happen first” without execution APIs.
- Consistency with **ValidationDecisionLabels** (2.1.2): bundles carry labels through merge seams so explainability survives aggregation.

**Out of scope:**
- Concrete CRDT / ECS storage schemas, binary patch formats, or asset pipeline IDs.
- Execution-track registry closure, CI proofs, and performance budgets for merge hot paths.

## Behavior (natural language)

Actors: **pipeline runner** (assembles bundles), **stage evaluators** (produce typed fragments), **validation gate (Stage 4)** (evaluates bundle + labels), **commit boundary (Stage 5)** (consumes allowed bundle only).

Inputs: per-stage **typed fragments** after Stage 2/3 evaluation (terrain/biome/POI/entity/sim-bootstrap pieces), plus **intent hook context** and **seed bundle identity**.

Outputs: a single **StagedDeltaBundle** containing ordered or partially ordered **apply ops**, each tagged with source stage and optional **merge seam id**; **ValidationDecisionLabels** attached at bundle level and optionally per seam; **CommitAllowed** false collapses bundle to empty / no-op apply list.

Merge semantics:
- **Last-writer-wins** is forbidden as a silent default; every merge seam declares an explicit rule family (e.g. disjoint domains, additive composition, explicit override list).
- When two fragments touch the same conceptual key, the bundle either **fails validation** (Stage 4 denies) or carries an explicit **resolution record** in the bundle (named policy), never an implicit pick.

Apply ordering:
- **Topological over stage spine first**: fragments are grouped by originating stage index; default ordering follows Stage 0 → 5 pipeline order for overlapping world domains.
- **Within-stage partial order** is allowed when fragments are provably disjoint (different layers or namespaces named in the bundle).

Regeneration:
- Rebuilding the bundle uses the same merge seams and ordering rules; diffing two bundles for replay compares **bundle identity + seam-level resolution records**, not raw text.

## Interfaces

- **StagedDeltaBundle:** `{ bundleIdentity, seamRecords[], applyOpsOrdered[], validationLabels, sourceStages[] }` (natural-language types; execution refines).
- **MergeSeamId:** stable string identifier for each fan-in point (e.g. `terrain+biome@regionA`).
- **ApplyOp:** `{ opId, stageIndex, seamId?, domainTag, fragmentRef, orderingKey }` — enough for juniors to sketch ordering graphs.

Upstream (from 2.1.1 / 2.1.2):
- Typed staged outputs and **CommitBoundaryToken** remain; bundles are the **only** artifact Stage 4 validates before emitting **CommitAllowed** and labels.

Downstream:
- Commit boundary consumes **one** validated bundle (or rejects); no partial application of a subset unless validation explicitly allows **sharded commit** (out of scope unless PMG adds).

## Edge cases

- **Empty bundle:** valid when no mutations are required; Stage 4 still runs (trivial pass) so **ValidationDecisionLabels** can state “no-op”.
- **Conflicting fragments:** Stage 4 must reject unless a seam produced a **resolution record**; silent merge is a contract violation.
- **Subgraph / partial regeneration:** prefix bundles must use the same merge seam catalog so replay compares like-for-like (execution may add tooling).

## Open questions

- Whether **sharded commit** (multiple smaller bundles per region) is ever allowed on the conceptual spine, or remains a single-bundle invariant until execution.
- Minimum granularity for **domainTag** so disjointness proofs stay tractable for validation.

## Pseudo-code readiness

```
assemble_bundle(stageFragments[], seamCatalog):
  bundle = empty StagedDeltaBundle
  for seam in topological_seam_order(seamCatalog):
    merged = apply_merge_rule(seam, fragments_touching(seam))
    bundle.append(merged)
  bundle.applyOpsOrdered = total_order(bundle, default=stage_spine_order)
  return bundle
```

Execution will replace placeholders with real data structures; the conceptual contract is **deterministic seam catalog + ordered apply list + validation on the whole**.

## Research integration

> [!note] External grounding
> No `Ingest/Agent-Research/` notes were bound this run; alignment is **pattern-only** from deterministic build pipelines and explicit merge-point practice.
