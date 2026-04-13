---
title: Phase 2 (Execution) — Procedural Generation and World Building
created: 2026-04-11
tags:
  - roadmap
  - execution
  - sandbox
  - procedural-generation
project-id: sandbox-genesis-mythos-master
roadmap_track: execution
phase: 2
subphase: "2"
status: in-progress
handoff_readiness: 85
conceptual_counterpart: "[[../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-03-30-0430]]"
---

# Phase 2 (Execution) — Procedural Generation and World Building

Execution remint anchor for Phase 2 on the parallel spine. Conceptual counterpart: [[../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-03-30-0430]].

## Scope

- Mirror the conceptual **forge** contract as **implementation-facing** seams: staged seed-to-world pipeline, intent-to-hook resolution, dry-run vs commit boundaries, and collaborative dialogue scaffolding — without claiming engine-specific APIs or CI/registry closure.
- Bind upstream to execution Phase **1.2** graph skeleton ([[../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-04-10-2355]]) for topo/subgraph/determinism vocabulary; defer `GMM-2.4.5-*` compare-table / HR-style proof rows unless evidenced later.

## Interface seams (execution mint — text-only this pass)

| Interface | Owner | Contract | Deferral |
| --- | --- | --- | --- |
| `IStagePipelineRunner` | Generation core | Executes ordered stage list with typed empty-output propagation on failure | Long-run perf harness deferred |
| `IIntentResolver` | Orchestration | Maps DM/player hooks to deterministic merge policy inputs | Registry closure deferred |
| `IDryRunValidator` | Validation gate | Evaluates staged deltas pre-commit; blocks partial commits | CI matrix deferred |
| `ISimulationBootstrapper` | Bootstrap seam | Packages sim-entry artifacts after validation clears | Consumer replay suite deferred |

## Pseudocode sketch (text — no verbatim C++ this pass)

```text
function run_generation_pass(seed_bundle, intent_hooks, stage_plan):
  staged = stage_pipeline_runner.expand_seed(seed_bundle)
  intents = intent_resolver.resolve(intent_hooks, staged)
  staged = stage_pipeline_runner.apply_intents(staged, intents)
  for stage in stage_plan.order:
    staged = stage_pipeline_runner.run_stage(stage, staged)
    if staged.failed:
      return blocked_result(empty_delta=true)
  if not dry_run_validator.ok(staged):
    return blocked_result(empty_delta=true)
  return commit_ready_bundle(staged)
```

## Roll-up gates (Phase 2 closure — execution)

| Secondary slice | Gate (must be true for Phase 2 exit) | Primary AC / hook |
| --- | --- | --- |
| **2.1** Pipeline stages | Stage spine + validation hooks minted; empty-output semantics explicit | AC-2.1-A–D hooks |
| **2.2** Intent resolver + hook mapping | Resolver spine + hook emit seams minted; replay/diff alignment to **2.1.5** explicit | AC-2.2.E1–E4 hooks |
| *TBD* | Remaining secondaries **2.3–2.7** as execution parallel spine progresses | Populate as secondaries land |

## Acceptance criteria (execution-first)

| ID | Criterion | Evidence target | Status |
| --- | --- | --- | --- |
| AC-2-P-A | Stage order is deterministic for identical seed bundles and intent sets | Matching stage trace hash across replays | Planned |
| AC-2-P-B | Dry-run validator blocks commit when any stage reports failure | Commit never observed with `failed=true` | Planned |
| AC-2-P-C | Intent resolution outputs are stable under declared merge policy | Deterministic intent resolution digest | Planned |
| AC-2-P-D | Bootstrap package references only validated staged outputs | Bootstrap manifest matches last validated snapshot | Planned |

## Lane comparand rows

| Row | Lane B (Sandbox) | Lane A (Godot) | Common contract |
| --- | --- | --- | --- |
| Stage driver | C++-oriented pipeline runner seams | GDScript/scene driver analog | Deterministic ordering + empty-output propagation |
| Intent mapping | Typed hook merge inputs | Signal/binding analog | Stable merge digest |
| Validation gate | Dry-run bundle vs commit boundary | Editor/runner preview analog | No commit on failure |

## Intent Mapping

| Design intent target | Inspiration anchors | Execution mechanism | Validation signal |
| --- | --- | --- | --- |
| Staged forge pipeline with safe commit boundary | Conceptual Phase 2 **Behavior** ordering + Phase **1.2** graph skeleton | `IStagePipelineRunner` + `IDryRunValidator` gate before `ISimulationBootstrapper` | AC-2-P-A trace hash; AC-2-P-B commit blocked on failure |
| Intent loops without hardcoded narrative | Conceptual **Intent resolver** + collaboration loop | `IIntentResolver` produces merge-policy inputs consumed by stage runner | AC-2-P-C stable intent digest |
| Simulation bootstrap only after validation | Conceptual simulation-entry chain (**2.7**) authority | `ISimulationBootstrapper` receives only validator-cleared bundles | AC-2-P-D manifest parity |

## Explicit deferrals

- `GMM-2.4.5-*` / registry–CI / compare-table closure rows remain **execution-deferred** unless a later slice evidences them.
- This primary mint is intentionally **text-only** for C/C++ precision; tertiary/secondary mints may add allowlisted verbatim citations with nested `Task(research)` when required by **sandbox_code_precision**.

## Related

- Upstream graph skeleton: [[../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-04-10-2355]]
- Conceptual authority: [[../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-03-30-0430]]
