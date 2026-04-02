---
title: Phase 2.1.2 — Stage family bodies and boundary hooks
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.1.2"
project-id: genesis-mythos-master
status: active
priority: high
progress: 35
handoff_readiness: 76
created: 2026-03-30
tags:
  - roadmap
  - genesis-mythos-master
  - phase-2
para-type: Project
links:
  - "[[Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-03-30-2205]]"
---

## Phase 2.1.2 — Stage family bodies and boundary hooks

This tertiary extends the Phase 2.1.1 stage-family contract by making the **boundary hooks** explicit at the interface layer: the boundary between **dry-run validation** and the **commit boundary token** now also carries a typed mapping of **validation outcome labels** into downstream typed deltas.

## Scope

**In scope:**
- Stage-family body contracts for the Phase 2.1 spine (Stages 0..5), with boundary-layer reinforcement.
- Explicit boundary hook surfaces between **Stage 4 validation artifacts** and the **commit boundary**.
- Validation-outcome label mapping as a first-class interface artifact (for consumers to reason about “why commit was allowed/denied” without reading engine-level logs).
- Deterministic replay semantics at the boundary-hook contract level (typed inputs -> typed hook outputs).

**Out of scope:**
- Concrete engine integrations (specific APIs, file formats, asset IDs, runtime registries).
- Execution-track CI/perf budgets/registry closure (conceptual naming only; execution details deferred).

## Behavior (natural language)

Actors: **systems** (stage bodies + validation gates), **DM** (regen + intent overrides), **players** (intent inputs).  
Inputs: a stable seed bundle identity, DM/player intent hooks, prior-stage typed outputs, plus boundary-layer hook surfaces derived from Stage 4.  
Outputs: typed stage outputs (pre-commit), a validation artifact, validation outcome labels, and the commit boundary token emitted only after the dry-run gate permits commit.

Stage body ordering (canonical spine):
- Stage 0 body: seed expansion -> derived seeds / bundle sub-identities.
- Stage 1 body: intent resolution -> intent hook set (typed).
- Stage 2 body: stage pipeline evaluation -> typed staged delta bundle.
- Stage 3 body: simulation bootstrap packaging -> sim bootstrap payload (pre-commit).
- Stage 4 body: dry-run validation gate -> validation artifact + `ValidationDecisionLabels` + `CommitAllowed` decision.
- Stage 5 body: commit boundary hook -> commit boundary token (authoritative mutation allowed only if `CommitAllowed` is true).

Regeneration semantics:
- Regeneration re-runs stage bodies with the same seed bundle identity and intent hook set, changing only where the user intent requires it.
- Conflicting intents resolve via explicit hook priority rules; stage bodies do not invent merge policy.
- Boundary-hook outputs are derived from typed Stage 4 artifacts (validation artifact + outcome labels), not recomputed from narrative alone.

## Interfaces

Use these as natural-language type contracts (not engine APIs):

- **StageInput:** `{ seedBundleIdentity, intentHookSet, priorStageTypedOutputs }`
- **StageOutput (common wrapper):**
  - `typedOutputs` (stage-specific typed data)
  - `validationLabels` (lightweight, typed labels for downstream consumers; execution details deferred)
  - `commitAllowed` (boolean/enum decision, produced by Stage 4)
- **Commit boundary token:** `CommitBoundaryToken` emitted only when dry-run validation permits commit; downstream world mutation must treat the token as opaque and authoritative.

Boundary hook surfaces (new interface items):
- **ValidationDecisionLabels:** typed label set emitted by Stage 4 (e.g. “commitAllowed=true” plus human/consumer-readable reasons).
- **BoundaryHookSet:** `{ ValidationDecisionLabels, CommitAllowed, CommitBoundaryToken }` (token present iff commit allowed).

## Edge cases

- Partial stage failure: if Stage 4 validation denies commit, downstream consumers must treat typed staged deltas as empty (no partial commit), while still exposing `ValidationDecisionLabels` for explanation/debug tooling.
- Deterministic replay: stage body outputs and boundary-hook outputs must depend only on typed inputs (seed identity + intent hook set + prior stage typed outputs + Stage 4 typed artifacts).
- Intent collisions: when intent hooks collide, priority rules decide; boundary-hook outputs must not silently pick an arbitrary winner.

## Open questions

- Should `ValidationDecisionLabels` be per-stage (richer traceability) or aggregated at the boundary layer (simpler consumption)?
- Which consumer-facing labels are stable enough to treat as a long-lived conceptual API surface?

## Pseudo-code readiness

Readers can sketch the staged pipeline contract without needing engine APIs:

```
stage_pipeline(seedBundleIdentity, intentHookSet):
  s0 = stage0_seed_expand(seedBundleIdentity)
  s1 = stage1_intent_resolve(intentHookSet, seedBundleIdentity)
  s2 = stage2_stage_evaluate(s0, s1)
  s3 = stage3_sim_bootstrap(s2)
  v  = stage4_dry_run_validate(s3)
  if v.commitAllowed:
    token = stage5_commit_boundary(v, s3)
    return { stagedDeltas: s2.typedDeltas, commitToken: token, validation: v }
  return { stagedDeltas: empty, commitToken: null, validation: v }
```

Full API signatures and engine-bound error enums belong in execution track / later technical depth.

## Research integration

> [!note] External grounding
> No `Ingest/Agent-Research/` notes were bound this run; alignment is **pattern-only** from the staged procedural generation contract and deterministic replay conventions.

