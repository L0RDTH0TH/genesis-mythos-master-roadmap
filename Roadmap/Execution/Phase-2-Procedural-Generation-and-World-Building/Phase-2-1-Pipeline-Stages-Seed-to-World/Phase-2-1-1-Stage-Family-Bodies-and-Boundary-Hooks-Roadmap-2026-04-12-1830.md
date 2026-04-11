---
title: Phase 2.1.1 (Execution) — Stage family bodies and boundary hooks
created: 2026-04-12
tags:
  - roadmap
  - execution
  - godot
  - sandbox-comparand
project-id: godot-genesis-mythos-master
roadmap_track: execution
phase: 2
subphase: "2.1.1"
roadmap-level: tertiary
status: in-progress
handoff_readiness: 86
handoff_gaps:
  - "Rollup / registry / CI proof rows remain execution-deferred per D-Exec-rollup-deferral."
handoff_audit_last: "2026-04-12T18:30:00Z"
conceptual_counterpart: "[[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-1-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-03-30-0923]]"
---

# Phase 2.1.1 (Execution) — Stage family bodies and boundary hooks

Execution remint for **Phase 2 tertiary 2.1.1** on the parallel spine. Binds conceptual NL contracts from [[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-1-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-03-30-0923]] to Godot-facing stage seams declared on [[Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-12-1616]] (secondary **2.1**).

## Intent mapping (execution)

| Conceptual contract | Execution mechanism | Godot metaphor |
| --- | --- | --- |
| `StageInput` / `StageOutput` wrappers | Typed dict-like payloads carried across `IPipelineStage.apply` | [Dictionary](https://docs.godotengine.org/en/stable/classes/class_dictionary.html) + explicit schema keys |
| Intent hook freeze | Single-run immutable `Callable` table after Stage 1 | [Callable](https://docs.godotengine.org/en/stable/classes/class_callable.html) `is_valid` guard before invoke |
| Validation artifact | `IDryRunValidator` returns structured reasons | [PackedStringArray](https://docs.godotengine.org/en/stable/classes/class_packedstringarray.html) or custom result object |
| Commit boundary token | `ICommitBoundary` emits token only on pass | Ref-counted handle ([RefCounted](https://docs.godotengine.org/en/stable/classes/class_refcounted.html)) |

## Per-stage body sketch (0–5)

| Stage | Body responsibility | Reads | Produces |
| --- | --- | --- | --- |
| 0 | Expand seed identities | `seedBundleIdentity` | `SeedExpansionResult` |
| 1 | Resolve DM/player hooks to frozen table | intents + Stage 0 | `IntentResolvedSet` |
| 2 | Evaluate pipeline stage graph | frozen hooks + Stage 0 | `TypedStageDeltaBundle` |
| 3 | Package sim bootstrap | Stage 2 output | `SimBootstrapPayload` |
| 4 | Dry-run validate | bootstrap + deltas | `ValidationArtifact`, `CommitAllowed` |
| 5 | Commit or abort | validation + payload | `CommitBoundaryToken` or rollback |

## Boundary hooks (fail-closed)

- **Stage 2→3:** empty `TypedStageDeltaBundle` short-circuits bootstrap; log hook reason (no silent success).
- **Stage 4→5:** `CommitAllowed == false` → **no** token; `ICommitBoundary` must not observe partial world writes.
- **Intent collision:** priority map evaluated in Stage 1 only; later stages consume frozen priorities.

## Runner sketch (GDScript-shaped pseudocode)

```text
func run_stage_bodies(seed_id: String, intents: Dictionary) -> StageOutput:
  var s0 = stages.expand_seed.apply(seed_id)
  var hooks = stages.intent_resolve.apply(intents, s0)
  var s2 = stages.pipeline_evaluate.apply(s0, hooks)
  var boot = stages.sim_bootstrap.package(s2)
  var v = dry_run.validate(boot)
  if not v.commit_allowed:
    return commit_boundary.abort(v)
  return commit_boundary.tokenize(v, boot)
```

## Acceptance criteria (execution-first)

| ID | Criterion | Evidence | Status |
| --- | --- | --- | --- |
| AC-2.1.1-A | Each stage body maps to a named `IPipelineStage` id in registry | Registry row + stage_id trace | Planned |
| AC-2.1.1-B | Frozen hook table documented before Stage 2 | Resolver log snapshot | Planned |
| AC-2.1.1-C | Dry-run failure produces zero commit token | Blocked-commit trace | Planned |

## Explicit deferrals (D-Exec-rollup-deferral)

- **`GMM-2.4.5-*`**, CI run IDs, registry hashes — **not** closed in this note.
- Next structural slice: **2.1.2** boundary-hook refinement — [[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-2-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-03-30-1015]].

## Related

- Parent secondary (spine): [[Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-12-1616]]
- Phase 2 execution primary: [[../Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-04-12-1515]]
