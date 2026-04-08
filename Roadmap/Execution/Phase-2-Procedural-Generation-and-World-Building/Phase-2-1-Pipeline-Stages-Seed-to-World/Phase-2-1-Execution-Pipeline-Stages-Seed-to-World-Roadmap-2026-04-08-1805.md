---
title: Phase 2.1 — Execution pipeline stages seed-to-world (Godot lane)
roadmap-level: secondary
phase-number: 2
subphase-index: "2.1"
project-id: godot-genesis-mythos-master
roadmap_track: execution
status: complete
priority: high
progress: 100
handoff_readiness: 87
handoff_gaps: []
created: 2026-04-08
tags:
  - roadmap
  - execution
  - godot-genesis-mythos-master
  - phase-2
para-type: Project
conceptual_counterpart: "[[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-03-30-2205]]"
links:
  - "[[../Phase-2-Execution-Procedural-Generation-and-World-Building-Roadmap-2026-04-08-1227]]"
---

## Phase 2.1 — Execution seed-to-world pipeline (parallel spine)

Execution mirror for conceptual **2.1** under the required parallel spine. This slice binds **seed bundle → staged deltas → dry-run gate → commit boundary** into stage-family contracts, explicit `G-2.1-*` pass/fail rows with owner signoff tokens, and lane A/B comparand parity hooks for junior implementation.

## Scope

**In scope:** deterministic stage ordering (0–5), typed stage I/O envelopes, intent hook registry rows, dry-run vs commit boundary pseudocode, execution roll-up gate table, and propagation tokens into Phase 2 primary (`rollup_2_primary_from_2_1`).

**Out of scope:** tertiary **2.1.3–2.1.5** mints (future deepens), CI proof bundles, registry/HR closure, and full simulation-phase semantics (deferred per dual-track execution policy).

## Lane comparand — godot (A) vs sandbox (B)

| Concern | **Lane godot (A)** | **Lane sandbox (B)** |
| --- | --- | --- |
| Stage runner | Resource-backed `StageRegistry` + topological materialize | In-memory harness with identical stage IDs |
| Seed bundle identity | Stable manifest IDs + file-backed bundle hash | Synthetic bundle object with same ID namespace |
| Dry-run gate | `pipeline.dry_run(manifest)` returns typed reject + trace ID | Same API surface; returns harness-local trace |
| Commit boundary | `world_gateway.commit` after HardValidate only | Commit noop with version token for parity |

## Stage-family matrix (seed → world)

| Stage family | Order key | Inputs (typed) | Outputs (typed) | Failure surface |
| --- | --- | --- | --- | --- |
| S0 — Seed expansion | 0 | `SeedBundle`, profile | `ExpandedSeedIdentity`, derived sub-keys | `seed_shape_invalid` |
| S1 — Intent resolve | 1 | `IntentEnvelope`, hooks | `ResolvedHookBatch` | `intent_unauthorized`, `hook_collision` |
| S2 — Pipeline evaluation | 2 | Expanded seed + hooks | `StagedWorldDelta` (pre-commit) | `stage_eval_failed`, `ordering_violation` |
| S3 — Sim bootstrap packaging | 3 | Staged deltas | `SimBootstrapPackage` | `bootstrap_shape_invalid` |
| S4 — Dry-run validation | 4 | Package + manifest | `DryRunVerdict` | `dry_run_reject` |
| S5 — Commit boundary | 5 | Validated package | `CommitReceipt` | `commit_reject` (hard stop) |

## Pseudocode — spine orchestration (execution)

```pseudo
func seed_to_world(seed_bundle, profile, intents):
  expanded = stages.expand_seed(seed_bundle, profile)
  hooks = stages.resolve_intents(intents, expanded)
  staged = stages.evaluate_pipeline(expanded, hooks)
  bootstrap = stages.package_sim_bootstrap(staged)
  dry = pipeline.dry_run(bootstrap.manifest, intents)
  if not dry.ok:
    return reject(dry.reason, dry.trace_id)
  return world_gateway.commit(bootstrap.staged_delta, HardValidate)
```

## Roll-up gates (execution_v1) — `G-2.1-*` pass/fail + owner signoff

| Gate ID | Verdict | Evidence in this note | Owner signoff token |
| --- | --- | --- | --- |
| `G-2.1-Stage-Spine-Order` | **PASS** | Stage-family matrix + order keys 0–5 | `owner_signoff_G-2.1-Stage-Spine-Order_2026-04-08` |
| `G-2.1-Intent-Hook-Registry` | **PASS** | Intent resolve row + hook collision failure surface | `owner_signoff_G-2.1-Intent-Hook-Registry_2026-04-08` |
| `G-2.1-DryRun-Boundary` | **PASS** | Pseudocode shows dry-run before commit; AC-2.1-3 | `owner_signoff_G-2.1-DryRun-Boundary_2026-04-08` |
| `G-2.1-Lane-Comparand-Parity` | **PASS** | Lane A/B table covers runner, bundle ID, dry-run, commit | `owner_signoff_G-2.1-Lane-Comparand-Parity_2026-04-08` |
| `G-2.1-Tertiary-Chain-Deferred` | **FAIL (explicit, non-blocking)** | Tertiaries **2.1.1** — [[Phase-2-1-1-Execution-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-04-08-2215]], **2.1.2** — [[Phase-2-1-2-Execution-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-04-08-2230]], **2.1.3** — [[Phase-2-1-3-Execution-Staged-Delta-Bundles-Merge-Seams-and-Apply-Ordering-Roadmap-2026-04-10-1810]] minted; **2.1.4–2.1.5** still pending | `owner_defer_G-2.1-Tertiary-Chain-Deferred_2026-04-10` — partial chain; remaining tertiaries scheduled |

> [!note] FAIL row semantics
> **`G-2.1-Tertiary-Chain-Deferred`** is an explicit **execution-deferred** FAIL token (evidence missing), not a silent gap. It **does not** block `rollup_2_primary_from_2_1` propagation for the **secondary 2.1** roll-up row in Phase 2 primary — primary gate map records the deferral and routes next structural work to tertiaries when scheduled.

## Acceptance criteria

1. **AC-2.1-1:** Mirrored path matches conceptual subtree `Phase-2-1-Pipeline-Stages-Seed-to-World/` (no flat Execution-root heap).
2. **AC-2.1-2:** Every `G-2.1-*` row has a **PASS** or **explicit FAIL** verdict plus an owner token.
3. **AC-2.1-3:** Dry-run boundary is mandatory before commit in pseudocode.
4. **AC-2.1-4:** Phase 2 primary receives propagated `rollup_2_primary_from_2_1` closure row in the same run (see primary note).

## Risk register v0 (Phase 2.1 execution)

| Risk | Mitigation | Gate impact |
| --- | --- | --- |
| Tertiary chain lag | Explicit deferred FAIL row + token | See `G-2.1-Tertiary-Chain-Deferred` |
| Lane drift | Comparand table required on secondary | `G-2.1-Lane-Comparand-Parity` |

## Related

- Tertiary **2.1.1** (validation parity): [[Phase-2-1-1-Execution-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-04-08-2215]]
- Tertiary **2.1.2** (label / boundary hooks): [[Phase-2-1-2-Execution-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-04-08-2230]]
- Tertiary **2.1.3** (staged bundles + stage seams): [[Phase-2-1-3-Execution-Staged-Delta-Bundles-Merge-Seams-and-Apply-Ordering-Roadmap-2026-04-10-1810]]
- Execution primary (propagation target): [[../Phase-2-Execution-Procedural-Generation-and-World-Building-Roadmap-2026-04-08-1227]]
- Conceptual authority: [[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-03-30-2205]]
- Execution state: [[../../workflow_state-execution]]
