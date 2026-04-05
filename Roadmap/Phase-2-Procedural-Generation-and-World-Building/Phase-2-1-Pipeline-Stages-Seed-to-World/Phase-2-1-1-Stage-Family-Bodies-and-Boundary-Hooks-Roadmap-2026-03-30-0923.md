---
title: Phase 2.1.1 — Stage family bodies and boundary hooks
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.1.1"
project-id: godot-genesis-mythos-master
status: active
priority: high
progress: 30
handoff_readiness: 76
created: 2026-03-30
tags:
  - roadmap
  - godot-genesis-mythos-master
  - phase-2
para-type: Project
links:
  - "[[Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-03-30-2205]]"
---

## Phase 2.1.1 — Stage family bodies and boundary hooks

This tertiary defines the **stage-family bodies** and the **boundary hooks** that later slices consume as typed interfaces, while keeping Phase 2's conceptual contract: **dry-run validation gates commit** and **typed staged deltas stay pre-commit**.

## Scope

**In scope:**
- Stage-family body contracts for the Phase 2.1 spine (Stages 0..5).
- Explicit boundary hooks between stage evaluation and the commit boundary.
- The typed outputs produced by each stage family (seed expansion artifacts, intent hook sets, staged deltas, validation artifacts, commit boundary tokens).
- Regeneration replay semantics at the contract level (deterministic inputs -> deterministic typed outputs).

**Out of scope:**
- Concrete engine integrations (specific APIs, file formats, asset IDs).
- Execution-track CI/perf budgets/registry closure.

## Behavior (natural language)

Actors: **systems** (stage bodies + validation gates), **DM** (regen + intent overrides), **players** (intent inputs).  
Inputs: a stable seed bundle identity, DM/player intent hooks, and prior-stage typed outputs.  
Outputs: typed stage outputs (pre-commit), a validation artifact, and a commit boundary token that downstream world mutation must obey.

Stage body ordering (canonical spine):
- Stage 0 body: seed expansion -> derived seeds / bundle sub-identities.
- Stage 1 body: intent resolution -> intent hook set (typed).
- Stage 2 body: stage pipeline evaluation -> typed staged delta bundle.
- Stage 3 body: simulation bootstrap packaging -> sim bootstrap payload (pre-commit).
- Stage 4 body: dry-run validation gate -> validation artifact + decision.
- Stage 5 body: commit boundary hook -> commit boundary token (authoritative mutation allowed only after validation).

Regeneration semantics:
- Regeneration re-runs stage bodies with the same seed bundle identity and intent hook set, changing only where the user intent requires it.
- Conflicting intents resolve via explicit hook priority rules; stage bodies do not invent merge policy.

## Interfaces

Use these as *natural-language type contracts* (not engine APIs):

- **StageInput:** `{ seedBundleIdentity, intentHookSet, priorStageTypedOutputs }`
- **StageOutput (common wrapper):**
  - `typedOutputs` (stage-specific typed data)
  - `validationLabels` (lightweight labels for downstream consumers; execution details deferred)
- **Commit boundary token:** `CommitBoundaryToken` emitted only when dry-run validation permits commit.

Per-stage contract sketch:
- Stage 0 body:
  - Input: `seedBundleIdentity`
  - Output: `SeedExpansionResult` (derived seeds + stable identity token)
- Stage 1 body:
  - Input: `intentHookSet` (+ seed expansion identity for stable naming)
  - Output: `IntentResolvedSet` (typed hook values)
- Stage 2 body:
  - Input: `SeedExpansionResult` + `IntentResolvedSet`
  - Output: `TypedStageDeltaBundle` (staged deltas, still pre-commit)
- Stage 3 body:
  - Input: `TypedStageDeltaBundle`
  - Output: `SimBootstrapPayload` (inputs to simulation bootstrap; pre-commit)
- Stage 4 body:
  - Input: `SimBootstrapPayload`
  - Output: `ValidationArtifact` and `CommitAllowed` (boolean/enum decision)
- Stage 5 body:
  - Input: `ValidationArtifact` + `SimBootstrapPayload`
  - Output: `CommitBoundaryToken` (if and only if `CommitAllowed`)

Adjacent slices:
- Parent secondary **[[Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-03-30-2205]]** defines the overall stage spine and boundary intent; this tertiary binds the **stage-body** contracts and **hook surfaces** so downstream simulation and later phases attach without re-litigating ordering.

## Edge cases

- Partial stage failure: if Stage 4 validation denies commit, downstream consumers must treat typed staged deltas as empty (no partial commit).
- Deterministic replay: stage body outputs must depend only on typed inputs (seed identity + intent hook set + prior stage typed outputs).
- Intent collisions: when intent hooks collide, priority rules decide; stage bodies must not silently pick an arbitrary winner.

## Open questions

- Hook naming convention granularity (per-domain vs per-stage vs per-entity basis).
- Which validation artifacts should be exposed for tooling/debug vs which stay internal (execution-track detail deferred).

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

Full API signatures and engine-bound error enums belong in execution track / deeper technical notes.

## Research integration

> [!note] External grounding
> No `Ingest/Agent-Research/` notes were bound this run; alignment is pattern-only from staged pipeline contracts and deterministic replay conventions.

