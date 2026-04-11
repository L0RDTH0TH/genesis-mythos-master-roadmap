---
title: Phase 2 (Execution) — Procedural Generation and World Building
created: 2026-04-12
tags:
  - roadmap
  - execution
  - godot
  - sandbox-comparand
project-id: godot-genesis-mythos-master
roadmap_track: execution
phase: 2
subphase: "2"
roadmap-level: primary
status: in-progress
handoff_readiness: 86
handoff_gaps:
  - "Rollup / registry / CI / HR-style proof rows (`missing_roll_up_gates`, `GMM-2.4.5-*`) remain execution-deferred per D-Exec-rollup-deferral — no fabricated `ci_run_id` or closed rollup verdicts in this mint."
handoff_audit_last: "2026-04-12T15:15:00Z"
conceptual_counterpart: "[[../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-03-30-0430]]"
---

# Phase 2 (Execution) — Procedural Generation and World Building

Execution remint anchor for Phase 2 on the parallel spine. Conceptual counterpart: [[../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-03-30-0430]].

## Intent mapping

| Intent target | Inspiration anchors | Execution mechanism | Validation signal |
| --- | --- | --- | --- |
| Staged forge pipeline (seed → world) | Phase 2 primary **Behavior** + **Ordering** | `IPipelineStage` registry + deterministic stage runner seam | AC table + stage-boundary traces |
| Intent → hook resolution | Conceptual **Intent resolver** row | `IIntentResolver` + hook namespace table | Resolver unit tests / dry-run traces |
| Collaborative dialogue / commit gate | Conceptual **Glue / integration** task | `IDialogueScaffold` + commit boundary after dry-run | Validator + execution gate packets (deferred IDs) |
| Godot vs Sandbox parity | Dual-lane policy | Comparand rows + Godot doc anchors below | Hostile validator + **D-Exec-rollup-deferral** (no premature rollup closure) |

## Scope

- Bind execution-facing seams for the Phase 2 **forge**: seed expansion → intent resolve → staged pipeline → simulation bootstrap packaging → dry-run validation → commit boundary (aligned to conceptual primary ordering).
- Provide pseudocode skeletons for **runner**, **intent resolver**, and **commit gate** surfaces; keep registry/CI/compare-table/HR proofs **explicitly deferred**.
- Capture acceptance-criteria tables with lane comparand rows (Godot A vs Sandbox B) and **stable Godot documentation citations only** (whitelist per execution-research-whitelist).

## Interface seams (execution mint)

| Interface | Owner | Contract | Deferral |
| --- | --- | --- | --- |
| `IPipelineStage` | Pipeline core | Typed stage inputs/outputs + deterministic ordering key | Perf budgets + CI matrix deferred |
| `IIntentResolver` | Intent layer | Maps DM/player intents to hook targets with priority rules | Registry closure deferred |
| `IDryRunValidator` | Safety | Runs validation gate; blocks partial commit on failure | Full stress suite deferred |
| `ICommitBoundary` | Orchestration | Atomic commit or rollback of staged deltas | External audit bundle closure deferred |

## Pseudocode sketch

```text
function run_stage_pipeline(seed_bundle, intents, stage_registry):
  state = expand_seed(seed_bundle)
  resolved = intent_resolver.resolve(intents, state.hook_table)
  for stage_id in stage_registry.ordering():
    state = stage_registry.get(stage_id).apply(state, resolved)
  dry = dry_run_validator.validate(state)
  if not dry.ok:
    return CommitResult(blocked=true, reason=dry.reason)
  return commit_boundary.commit(state)
```

## Godot stable citations (lane A)

Authoritative anchors for hosting/orchestration metaphors (verbatim paths; **do not** substitute non-whitelisted domains):

- Main loop contract — [MainLoop](https://docs.godotengine.org/en/stable/classes/class_mainloop.html) (`_initialize`, `_process`, `_finalize`).
- Frame / idle integration — [SceneTree](https://docs.godotengine.org/en/stable/classes/class_scenetree.html) (`process_frame`, `physics_frame`, group iteration via `get_nodes_in_group`).
- Deterministic RNG streams for staged variation — [RandomNumberGenerator](https://docs.godotengine.org/en/stable/classes/class_randomnumbergenerator.html) (`seed`, `randf`, `randi`).
- Resource load / parse boundaries for staged asset handoff — [ResourceLoader](https://docs.godotengine.org/en/stable/classes/class_resourceloader.html) (`load`, `exists`).

These citations ground **lane A** rows in the comparand table; they **do not** claim closed CI or rollup IDs.

## Acceptance criteria (execution-first)

| ID | Criterion | Evidence target | Status |
| --- | --- | --- | --- |
| AC-2.0-A | Stage ordering is deterministic for a fixed seed bundle and registry snapshot | Hash-stable stage trace | Planned |
| AC-2.0-B | Intent resolution respects hook priority rules; collisions are explicit | Resolver decision log | Planned |
| AC-2.0-C | Dry-run gate blocks commit on validation failure | Blocked-commit trace | Planned |
| AC-2.0-D | Commit boundary is atomic; no partial world state after failed commit | Rollback / snapshot seam | Planned |

## Lane comparand rows

| Row | Lane A (Godot) | Lane B (Sandbox) | Common contract |
| --- | --- | --- | --- |
| Main driver | `MainLoop` / `SceneTree` frame callbacks | C++ scheduler + manual pump | Deterministic ordering of stage evaluation |
| Grouping / discovery | `Node.add_to_group` + `SceneTree.get_nodes_in_group` | Typed registry lookup | Stable discovery of stage/hook participants |
| Resource staging | `ResourceLoader.load` + parse errors surfaced | File/memory loaders | Typed load boundaries before stage apply |
| RNG discipline | `RandomNumberGenerator` seeded per stage session | Seeded STL / custom RNG | Reproducible variation under seed bundle |

## Explicit deferrals (D-Exec-rollup-deferral)

- **`GMM-2.4.5-*`** comparator rows, manifest-hash CI, and rollup **HR** closures remain **open** until attested run IDs exist — **do not** fabricate IDs in this note.
- **Registry / CI / compare-table** closure is **execution-deferred**; advisory `missing_roll_up_gates` is expected until downstream slices attach evidence.
- Secondary **2.1** mint is the next structural deepen target on the execution spine (`current_subphase_index: "2.1"`).

## Related

- Upstream Phase 1 execution primary (graph skeleton + safety hooks): [[../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-04-10-2100]]
- Conceptual Phase 2 primary (design authority): [[../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-03-30-0430]]
