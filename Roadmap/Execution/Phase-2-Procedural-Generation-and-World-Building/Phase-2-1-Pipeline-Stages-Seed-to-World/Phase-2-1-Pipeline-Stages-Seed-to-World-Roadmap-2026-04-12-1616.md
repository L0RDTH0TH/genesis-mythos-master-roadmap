---
title: Phase 2.1 (Execution) — Pipeline Stages Seed-to-World
created: 2026-04-12
tags:
  - roadmap
  - execution
  - godot
  - sandbox-comparand
project-id: godot-genesis-mythos-master
roadmap_track: execution
phase: 2
subphase: "2.1"
roadmap-level: secondary
status: in-progress
handoff_readiness: 85
handoff_gaps:
  - "Rollup / registry / CI / HR-style proof rows (`missing_roll_up_gates`, `GMM-2.4.5-*`) remain execution-deferred per D-Exec-rollup-deferral — no fabricated `ci_run_id` or closed rollup verdicts in this mint."
handoff_audit_last: "2026-04-12T16:16:00Z"
conceptual_counterpart: "[[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-03-30-2205]]"
---

# Phase 2.1 (Execution) — Pipeline stages (seed → world)

Execution remint for **Phase 2 secondary 2.1** on the parallel spine. Mirrors conceptual ordering and typed I/O from [[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-03-30-2205]]; binds those NL stage boundaries to the Phase 2 primary execution seams (`IPipelineStage`, `IIntentResolver`, `IDryRunValidator`, `ICommitBoundary`) on [[../Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-04-12-1515]].

## Intent mapping

| Intent target | Inspiration anchors | Execution mechanism | Validation signal |
| --- | --- | --- | --- |
| Canonical stage spine (0–5) | Conceptual **Ordering** + **Behavior** rows | Ordered `IPipelineStage` list + deterministic `stage_registry.ordering()` | Trace hash over `(stage_id, input_fingerprint, output_fingerprint)` |
| Intent injection before pipeline body | Conceptual **intent resolve** stage | `IIntentResolver` output fed as frozen hook table into stages 2+ | Resolver decision log + hook collision matrix |
| Pre-commit safety | Conceptual dry-run / commit boundary | `IDryRunValidator` after stage 4 packaging; `ICommitBoundary` only on pass | Blocked-commit trace; no partial world mutation |
| Godot vs Sandbox parity | Dual-lane policy | Callable / signal metaphors for stage boundaries (A) vs C++ executor (B) | Hostile validator + **D-Exec-rollup-deferral** (no premature rollup closure) |

## Scope

- Instantiate the **six-stage spine** as an execution-facing contract: **expand seed → resolve intents → evaluate pipeline stages → package simulation bootstrap → dry-run validate → commit boundary**, aligned to conceptual Phase 2.1.
- Define **typed stage I/O** references (handles/snapshots, not asset IDs) and where each stage reads the `IIntentResolver` output.
- Keep **registry / CI / HR / compare-table** closure explicitly **open**; only stub evidence pointers where needed.

## Stage spine (execution binding)

| Stage | Role | Reads | Produces |
| --- | --- | --- | --- |
| 0 | Seed expansion | Seed bundle identity | Derived sub-identities / expanded bundle snapshot |
| 1 | Intent resolve | DM/player hooks | Hook table for downstream stages |
| 2 | Pipeline evaluation | Hook table + prior stage outputs | Staged world deltas (typed) |
| 3 | Simulation bootstrap packaging | Staged deltas | Sim-input package (non-authoritative) |
| 4 | Dry-run validation | Sim-input + staged deltas | Validation artifact (`ok` / reasons) |
| 5 | Commit boundary | Validation pass | Atomic commit token or rollback |

Regeneration semantics match conceptual: **same bundle identity** for unchanged subcomponents; **deterministic** alternate seeds only where intent/regeneration requires.

## Runner sketch (non-authoritative)

```text
function run_seed_to_world(seed_bundle, intents, stage_registry, intent_resolver, dry_run_validator, commit_boundary):
  state0 = stage_registry.get("expand_seed").apply(seed_bundle, empty_hooks)
  hooks = intent_resolver.resolve(intents, state0.hook_table)
  state = state0
  for stage_id in ("terrain", "biomes", "pois", "entities"):  # conceptual labels; implementation in tertiaries
    state = stage_registry.get(stage_id).apply(state, hooks)
  bootstrap = stage_registry.get("sim_bootstrap").package(state, hooks)
  dry = dry_run_validator.validate(bootstrap)
  if not dry.ok:
    return commit_boundary.abort(reason=dry.reason)
  return commit_boundary.commit(bootstrap)
```

## Godot stable citations (lane A)

Use only allowlisted prefixes (stable docs). These ground **stage boundary / callable** metaphors without claiming closed CI IDs:

- Callable indirection for stage hooks — [Callable](https://docs.godotengine.org/en/stable/classes/class_callable.html) (`bind`, `call`, `is_valid`).
- Signal-style notification at stage edges (optional host pattern) — [Object](https://docs.godotengine.org/en/stable/classes/class_object.html) (`emit_signal`, `connect`).
- Reference-counted handles for staged payloads — [RefCounted](https://docs.godotengine.org/en/stable/classes/class_refcounted.html) (lifetime discipline for staged deltas).
- Main loop / frame integration (orchestration metaphor, inherited from primary) — [MainLoop](https://docs.godotengine.org/en/stable/classes/class_mainloop.html), [SceneTree](https://docs.godotengine.org/en/stable/classes/class_scenetree.html).

## Acceptance criteria (execution-first)

| ID | Criterion | Evidence target | Status |
| --- | --- | --- | --- |
| AC-2.1-A | Stage ordering matches conceptual 0–5 spine; registry ordering is deterministic | Stage trace + ordering key | Planned |
| AC-2.1-B | Intent resolve precedes body stages; hooks are frozen for a single pipeline run | Resolver log + frozen-hook flag | Planned |
| AC-2.1-C | Dry-run gate blocks commit on validation failure | Blocked-commit trace | Planned |
| AC-2.1-D | No partial commit on stage failure; downstream receives empty typed outputs | Rollback / empty-delta path | Planned |

## Lane comparand rows

| Row | Lane A (Godot) | Lane B (Sandbox) | Common contract |
| --- | --- | --- | --- |
| Stage edge dispatch | Callable + Object signal patterns (documentation-backed) | Virtual stage interface + explicit C++ calls | Deterministic ordering + typed I/O |
| Staged payload lifetime | RefCounted / Resource handles | `shared_ptr` / arena rules | No use-after-free across commit boundary |
| Validation gate | Dry-run validator seam | Static + runtime checks | Fail-closed before commit |

## Explicit deferrals (D-Exec-rollup-deferral)

- **`GMM-2.4.5-*`**, manifest-hash CI, registry IDs, and rollup **HR** closures remain **open** — **do not** fabricate IDs in this note.
- **Tertiary 2.1.x** notes will refine stage-family bodies; this secondary defines spine + interfaces only.

## Related

- Phase 2 execution primary (interfaces): [[../Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-04-12-1515]]
- Tertiary 2.1.1 (stage bodies / hooks): [[Phase-2-1-1-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-04-12-1830]]
- Conceptual Phase 2.1 (design authority): [[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-03-30-2205]]
- Phase 1 execution graph skeleton (upstream patterns): [[../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-Procedural-Generation-Graph-Skeleton-Roadmap-2026-04-11-2230]]
