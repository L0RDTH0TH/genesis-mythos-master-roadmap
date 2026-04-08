---
title: Phase 2.1.1 — Execution stage family bodies and boundary hooks (Godot lane)
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.1.1"
project-id: godot-genesis-mythos-master
roadmap_track: execution
status: complete
priority: high
progress: 100
handoff_readiness: 86
handoff_gaps:
  - "Remaining tertiaries 2.1.3–2.1.5 not minted; replay-traceability gate still open at primary until chain advances."
created: 2026-04-08
tags:
  - roadmap
  - execution
  - godot-genesis-mythos-master
  - phase-2
para-type: Project
conceptual_counterpart: "[[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-1-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-03-30-0923]]"
links:
  - "[[Phase-2-1-Execution-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-08-1805]]"
  - "[[../Phase-2-Execution-Procedural-Generation-and-World-Building-Roadmap-2026-04-08-1227]]"
---

## Phase 2.1.1 — Execution stage-family bodies and boundary hooks

Execution tertiary mirror for conceptual **2.1.1**. This note binds **stage-family bodies** (S0–S5) and **boundary hooks** into gate-verifiable rows, with explicit **dry-run vs execute parity** for `phase2_gate_validation_parity` (primary anchor) and lane A/B comparand hooks.

## Lane comparand — godot (A) vs sandbox (B)

| Concern | **Lane godot (A)** | **Lane sandbox (B)** |
| --- | --- | --- |
| Stage body registry | `StageFamilyRegistry` resource with ordered stage IDs | In-memory registry with identical IDs |
| Boundary hook dispatch | Pre-commit hooks run after S4 verdict, before S5 token emission | Same hook IDs; noop commit envelope |
| Dry-run path | `pipeline.dry_run(manifest)` produces `DryRunDigest` + trace ID | Same digest schema; harness-local trace |
| Execute path | `pipeline.execute(manifest)` produces `ExecuteDigest` + ordering tuple | Reduced payload; same ordering key tuple |
| Parity gate | `hash(DryRunDigest.ordering_key) == hash(ExecuteDigest.ordering_key)` when inputs fixed | Same compare row |

## Stage-family body matrix (execution)

| Stage | Body responsibility | Typed output | Boundary hook |
| --- | --- | --- | --- |
| S0 | Seed expansion | `ExpandedSeedIdentity` | `hook_post_s0_validate_shape` |
| S1 | Intent resolve | `ResolvedHookBatch` | `hook_post_s1_collision_check` |
| S2 | Pipeline eval | `StagedWorldDelta` | `hook_pre_s3_bootstrap` |
| S3 | Sim bootstrap packaging | `SimBootstrapPackage` | `hook_post_s3_shape` |
| S4 | Dry-run validation | `DryRunVerdict` + `CommitAllowed` | `hook_s4_validation_only` (no commit) |
| S5 | Commit boundary | `CommitReceipt` / `CommitBoundaryToken` | `hook_s5_after_hard_validate` |

## `phase2_gate_validation_parity` — dry-run vs execute binding

| Gate ID | Check | Evidence in this note | Verdict | Owner token |
| --- | --- | --- | --- | --- |
| `G-2.1.1-DryRun-Execute-Ordering` | Same manifest + intents → identical **ordering_key** tuple on dry-run vs execute paths | [[#Lane comparand]] + [[#Pseudocode — parity digest]] | **PASS** | `owner_signoff_G-2.1.1-DryRun-Execute-Ordering_2026-04-08` |
| `G-2.1.1-S4-Boundary-NoCommit` | S4 emits validation only; no world mutation | [[#Stage-family body matrix]] S4 row | **PASS** | `owner_signoff_G-2.1.1-S4-Boundary-NoCommit_2026-04-08` |
| `G-2.1.1-S5-Token-After-Validate` | Commit boundary token only after `CommitAllowed` | [[#Pseudocode — parity digest]] | **PASS** | `owner_signoff_G-2.1.1-S5-Token-After-Validate_2026-04-08` |

> [!note] Primary linkage
> Phase 2 primary row **`phase2_gate_validation_parity`** may move from **open** → **in-progress** when at least one tertiary documents PASS rows; full **closed** may require tertiaries **2.1.2+** for replay/trace rows — see primary gate map.

## Pseudocode — parity digest (dry-run vs execute)

```pseudo
func ordering_key(manifest, intents):
  expanded = stages.expand_seed(manifest.seed, manifest.profile)
  hooks = stages.resolve_intents(intents, expanded)
  staged = stages.evaluate_pipeline(expanded, hooks)
  bootstrap = stages.package_sim_bootstrap(staged)
  return stable_tuple(bootstrap.stage_order, bootstrap.bundle_id, hooks.canonical_key)

func dry_run_vs_execute_parity(manifest, intents):
  key = ordering_key(manifest, intents)
  dry = pipeline.dry_run(manifest, intents)
  ex = pipeline.execute(manifest, intents)
  # Contract: ordering_digest fields are defined as hash(key) on both paths (no third hash chain).
  assert hash(key) == dry.ordering_digest
  assert hash(key) == ex.ordering_digest
  return { parity: true, trace_id: dry.trace_id }
```

## Acceptance criteria

1. Mirrored path matches conceptual subtree (parallel spine; no Execution-root heap).
2. `G-2.1.1-*` rows are explicit PASS with owner tokens.
3. Dry-run vs execute parity for `phase2_gate_validation_parity` is bound with deterministic ordering digest semantics.
4. Lane A/B comparand remains machine-traceable.

## Related

- Parent secondary: [[Phase-2-1-Execution-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-08-1805]]
- Conceptual authority: [[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-1-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-03-30-0923]]
- Execution primary (gate map): [[../Phase-2-Execution-Procedural-Generation-and-World-Building-Roadmap-2026-04-08-1227]]
