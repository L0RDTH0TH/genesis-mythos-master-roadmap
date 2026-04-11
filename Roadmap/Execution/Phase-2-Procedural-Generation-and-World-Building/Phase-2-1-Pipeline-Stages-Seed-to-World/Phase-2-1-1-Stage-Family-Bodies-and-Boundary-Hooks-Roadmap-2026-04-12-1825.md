---
title: Phase 2.1.1 (Execution) — Stage family bodies and boundary hooks
created: 2026-04-12
tags:
  - roadmap
  - execution
  - sandbox
  - procedural-generation
  - phase-2-1-1
project-id: sandbox-genesis-mythos-master
roadmap_track: execution
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.1.1"
status: in-progress
handoff_readiness: 85
priority: high
progress: 40
conceptual_counterpart: "[[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-1-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-03-30-0923]]"
para-type: Project
links:
  - "[[Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-11-2359]]"
---

# Phase 2.1.1 (Execution) — Stage family bodies and boundary hooks

Execution tertiary **2.1.1** on the parallel spine under `Phase-2-1-Pipeline-Stages-Seed-to-World/`, mirroring conceptual **2.1.1** ([[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-1-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-03-30-0923]]). Binds parent secondary **2.1** ([[Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-11-2359]]) to concrete **stage-family body** seams and **boundary hook** surfaces expressed as **interface contracts and text pseudocode only** this pass (no verbatim C++; **sandbox_code_precision** deferred until a later entry with allowlisted Research).

## Scope (execution)

**In scope:**

- C++-oriented **interface seams** for stage-family bodies Stages **0..5** aligned to secondary **2.1** stage table (seed expansion → intent resolve → staged evaluation → sim-bootstrap packaging → dry-run validation → commit boundary).
- **Boundary hooks** between stage evaluation output and the commit boundary token path (`dry_run_validator` / `commit_ready` from Phase **2** primary vocabulary).
- Typed output **names** and **ownership roles** at the seam (structs/interfaces as NL bullets + `text` blocks — not engine APIs).
- Regeneration / replay semantics at the execution contract level: deterministic inputs → deterministic typed outputs; **empty-output / skip-downstream** parity with Phase **1.2** graph story.

**Out of scope:**

- Verbatim headers, `static_assert`, or standard-library quotes (**sandbox_code_precision** — requires nested Research + allowlisted URLs on a future slice).
- Registry–CI / **GMM-2.4.5** closure rows (execution-deferred unless evidenced).

## Behavior (execution contract)

Actors: **pipeline runner** (stage list + validation gate), **DM/player** intent hooks, **dry-run / commit** modes from Phase **2** primary.

Canonical stage-family **body** responsibilities (aligns to conceptual NL + secondary **2.1** table):

| Stage | Body responsibility | Failure / empty semantics |
| --- | --- | --- |
| 0 | Seed expansion — derive stable sub-identities from `seed_bundle` | Propagate typed empty; no external I/O |
| 1 | Intent resolve — merge hooks into deterministic merge inputs | Conflicts isolated to merge policy inputs |
| 2 | Pipeline evaluation — run ordered stage list over staged state | `failed` → block commit; skip downstream |
| 3 | Simulation bootstrap packaging — package validator-cleared bundles only | No bootstrap on invalid staged snapshot |
| 4 | Dry-run validation gate | Deny commit → no `CommitBoundaryToken` |
| 5 | Commit boundary hook | Emit token only if Stage **4** allows |

**Regeneration:** Re-enter stage bodies with the same **seed bundle identity** and **intent hook set**; only user-intent deltas change. Merge collisions use explicit priority inputs — stage bodies do not invent policy.

## Interfaces (text — depth-3 tertiary)

Natural-language type shapes (not API signatures):

- **`StageInput`:** `{ seed_bundle_id, intent_hook_set, prior_typed_outputs }`
- **`StageOutput`:** `{ typed_outputs, validation_labels }` (labels are lightweight; execution detail deferred)
- **`CommitBoundaryToken`:** opaque handle emitted only when dry-run validation clears

Per-stage seam sketch (execution):

- **Stage 0:** consumes `seed_bundle_id` → produces `SeedExpansionResult` (derived ids + stable naming token).
- **Stage 1:** consumes `intent_hook_set` + seed naming token → `IntentResolvedSet`.
- **Stage 2:** consumes expansion + resolved intents → `TypedStageDeltaBundle` (pre-commit).
- **Stage 3:** consumes staged deltas → `SimBootstrapPayload` (pre-commit).
- **Stage 4:** consumes bootstrap payload → `ValidationArtifact` + `commit_allowed`.
- **Stage 5:** consumes validation + bootstrap → `CommitBoundaryToken` iff `commit_allowed`.

Adjacent slices: parent secondary **[[Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-11-2359]]**; conceptual peer **[[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-1-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-03-30-0923]]**.

## Edge cases (execution)

- **Partial validation failure:** If Stage **4** denies commit, consumers must treat staged deltas as non-authoritative for mutation (no partial commit).
- **Deterministic replay:** Typed outputs depend only on `seed_bundle_id`, `intent_hook_set`, and prior stage outputs (matches **1.2.4** replay contracts).
- **Intent collisions:** Resolved via merge policy inputs — stage bodies surface conflicts, do not pick arbitrary winners.

## Pseudocode readiness (text — no verbatim C++)

```text
seam stage_pipeline_text(seed_bundle_id, intent_hook_set, stage_plan, mode):
  s0 = stage0_seed_expand(seed_bundle_id)
  s1 = stage1_intent_resolve(intent_hook_set, s0)
  s2 = stage2_evaluate_stages(stage_plan.order, s0, s1)
  if s2.failed:
    return blocked(empty_delta=true, skip_downstream=true)
  s3 = stage3_sim_bootstrap(s2)
  v  = stage4_dry_run_validate(s3)
  if not v.commit_allowed:
    return blocked(empty_delta=true)
  if mode == dry_run:
    return preview_only(s2, v)
  token = stage5_commit_boundary(v, s3)
  return commit_ready(staged=s2, token=token, validation=v)
```

Verbatim C++ / standard quotes → later slice with **Task(research)** + allowlisted citations per **sandbox_code_precision**.

## Acceptance criteria (execution-first)

| ID | Criterion | Evidence target | Status |
| --- | --- | --- | --- |
| AC-2.1.1.E1 | Stage-family body ordering matches secondary **2.1** table for identical seed + intents | `stage_family_order_trace` | Planned |
| AC-2.1.1.E2 | Commit boundary token only after dry-run allows commit | `commit_token_present_iff_validate_ok` | Planned |
| AC-2.1.1.E3 | Intent collision surfaces merge inputs (no silent winner) | `intent_collision_manifest` | Planned |
| AC-2.1.1.E4 | Regeneration uses stable `seed_bundle_id` + hook set as canonical inputs | `replay_input_digest` | Planned |

## Intent Mapping

| Design intent target | Inspiration anchors | Execution mechanism | Validation signal |
| --- | --- | --- | --- |
| Stage-body contracts | Conceptual **2.1.1** stage spine + secondary **2.1** table | `stage_pipeline_text` + stage table | AC-2.1.1.E1 |
| Safe commit boundary | Phase **2** primary dry-run / commit tables | Stages **4–5** gate + token | AC-2.1.1.E2 |
| Deterministic replay | **1.2.4** replay / identity story | Stable inputs → stable typed outputs | AC-2.1.1.E4 |

## Lane comparand

| Concern | Sandbox (this lane) | Godot (reference) | Shared contract |
| --- | --- | --- | --- |
| Stage bodies | C++-oriented seams (text this pass) | Scene/resource staging | Deterministic ordering |
| Boundary hooks | Pre-commit validation + token | Editor preview | No commit on failure |

## Related

- Parent execution secondary: [[Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-11-2359]]
- Phase **2** execution primary: [[../Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-04-11-1432]]
- Conceptual **2.1.1**: [[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-1-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-03-30-0923]]
- Next structural target: tertiary **2.1.2** (mirrors conceptual **2.1.2** under the same folder).
