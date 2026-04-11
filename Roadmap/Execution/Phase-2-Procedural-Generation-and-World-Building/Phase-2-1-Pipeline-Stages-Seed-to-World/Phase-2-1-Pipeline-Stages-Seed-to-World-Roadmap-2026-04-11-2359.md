---
title: Phase 2.1 (Execution) — Pipeline Stages Seed-to-World
created: 2026-04-11
tags:
  - roadmap
  - execution
  - sandbox
  - procedural-generation
  - phase-2-1
project-id: sandbox-genesis-mythos-master
roadmap_track: execution
roadmap-level: secondary
phase-number: 2
subphase-index: "2.1"
status: in-progress
handoff_readiness: 85
conceptual_counterpart: "[[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-03-30-2205]]"
---

# Phase 2.1 (Execution) — Pipeline stages seed-to-world

Execution secondary **2.1** on the parallel spine under `Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/`, mirroring the conceptual tree. Binds Phase **2** execution primary ([[../Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-04-11-1432]]) to upstream Phase **1.2** graph vocabulary ([[../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-04-10-2355]]).

Conceptual authority: [[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-03-30-2205]]

## Scope (execution)

- Ordered **seed-to-world** stage spine: seed expansion → intent resolve → staged evaluation waves → simulation-bootstrap packaging → dry-run validation gate → commit boundary — expressed as **interface seams** and **text** pseudocode only this pass (no verbatim C++; precision deferred to **2.1.x** tertiaries with allowlisted Research).
- Determinism and **empty-output / skip-downstream** semantics align with Phase **1.2** execution graph story and Phase **2** primary `IStagePipelineRunner` / `IDryRunValidator` table.

## Stage spine (execution contract — text)

| Stage | Role | Failure semantics |
| --- | --- | --- |
| 0 | Seed expansion — stable derived identities from `seed_bundle` | Typed empty outputs; no external calls |
| 1 | Intent resolve — map DM/player hooks to merge inputs | Conflicts isolated; merge policy inputs only |
| 2 | Pipeline evaluation — ordered stage list (terrain/biome/POI/entity shaped) | Propagate `failed=true`; block commit |
| 3 | Simulation bootstrap packaging — validator-cleared bundles only | No bootstrap on invalid staged state |
| 4 | Dry-run validation gate | Blocks partial commits |
| 5 | Commit boundary | Authoritative mutation only after gate clears |

## Pseudocode seams (text — depth-2 secondary)

```text
seam run_seed_to_world_pipeline(seed_bundle, intent_hooks, stage_plan, mode):
  staged = seed_expand(seed_bundle)
  intents = intent_resolve(intent_hooks, staged)
  staged = apply_intents(staged, intents)
  for stage in stage_plan.order:
    staged = run_stage(stage, staged)
    if staged.failed:
      return blocked_result(empty_delta=true, skip_downstream=true)
  if mode == dry_run:
    return preview_bundle(staged)
  if not dry_run_validator.ok(staged):
    return blocked_result(empty_delta=true)
  return commit_ready_bundle(staged)
```

## Acceptance criteria (execution-first)

| ID | Criterion | Evidence target | Status |
| --- | --- | --- | --- |
| AC-2.1.E1 | Declared stage order is stable for identical seed + intents | `stage_order_trace` hash | Planned |
| AC-2.1.E2 | Dry-run never emits commit without validator-cleared bundle | `dry_run_commit_diff.empty` | Planned |
| AC-2.1.E3 | Intent resolution outputs feed merge policy inputs deterministically | `intent_resolution_digest` | Planned |
| AC-2.1.E4 | Bootstrap receives only last validated staged snapshot | `bootstrap_manifest` parity | Planned |

> [!note] Deferred
> **GMM-2.4.5** / registry–CI / compare-table closure rows remain **execution-deferred** unless a later slice evidences them. Tertiary **2.1.1+** mints may attach stubs or allowlisted citations per **sandbox_code_precision**.

## Intent Mapping

| Design intent target | Inspiration anchors | Execution mechanism | Validation signal |
| --- | --- | --- | --- |
| Staged forge spine | Conceptual 2.1 ordering + Phase 2 primary forge | `run_seed_to_world_pipeline` + stage table | AC-2.1.E1 trace hash |
| Safe commit boundary | Phase 2 primary dry-run / bootstrap table | `dry_run_validator` gate before commit token | AC-2.1.E2 |
| Graph vocabulary reuse | Phase 1.2 DAG/topo + skip-on-failure | Stage list consumes **1.2** node/stage semantics | AC-2.1.E3–E4 |

## Lane comparand

| Concern | Sandbox (this lane) | Godot (reference) | Shared contract |
| --- | --- | --- | --- |
| Stage driver | C++-oriented pipeline seams | Scene/resource staging | Deterministic ordering |
| Validation | Pre-commit dry-run gate | Editor preview | No commit on failure |

## Related

- Phase 2 execution primary: [[../Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-04-11-1432]]
- Upstream graph skeleton: [[../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-04-10-2355]]
- Next structural target: tertiary **2.1.1** (conceptual peers under conceptual `Phase-2-1-Pipeline-Stages-Seed-to-World/`).
