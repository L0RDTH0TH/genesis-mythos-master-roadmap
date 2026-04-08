---
title: Phase 2.2.3 — Execution conflict resolution, priority ordering, and merge policy (Godot lane)
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.2.3"
project-id: godot-genesis-mythos-master
roadmap_track: execution
status: complete
priority: high
progress: 100
handoff_readiness: 86
handoff_gaps: []
created: 2026-04-08
tags:
  - roadmap
  - execution
  - godot-genesis-mythos-master
  - phase-2
para-type: Project
conceptual_counterpart: "[[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-2-Intent-Resolver-and-Hook-Mapping/Phase-2-2-3-Conflict-Resolution-Priority-Ordering-and-Merge-Policy-Roadmap-2026-03-31-0002]]"
links:
  - "[[Phase-2-2-Execution-Intent-Resolver-and-Hook-Mapping-Roadmap-2026-04-10-1900]]"
  - "[[../Phase-2-Execution-Procedural-Generation-and-World-Building-Roadmap-2026-04-08-1227]]"
  - "[[Phase-2-2-2-Execution-Validate-Classify-Schema-and-Hook-Mapping-Roadmap-2026-04-08-2330]]"
  - "[[Phase-2-2-1-Execution-Intent-Envelope-Normalization-and-Identity-Binding-Roadmap-2026-04-08-2315]]"
---

## Phase 2.2.3 — Execution conflict resolution, priority ordering, and merge policy

Execution tertiary mirror for conceptual **2.2.3**. Third resolver stage after **2.2.2** validate/classify: **detect** conflicts across classified intents, **order** by precedence ladder (actor lane × operation kind), **merge** via deterministic policy matrix (`compose` / `override` / `defer` / `reject`), emit **`ResolvedIntentSet`** + **`ConflictDecisionLog`** for pre-emit handoff to **2.2.4**. Composes **2.2.2** `ClassifiedIntent` + `HookPayloadOutline` outputs. Lane **godot (A)** vs **sandbox (B)** comparand parity preserved.

> [!note] Queue reconcile
> Queue `followup-deepen-exec-p222-tertiary-godot-20260408T232000Z` requested **2.2.2** mint; **2.2.2** is already on disk (**[[../../workflow_state-execution]]** Iter **21**, **2026-04-08 23:30**). Authoritative pre-read cursor in [[../../workflow_state-execution]] was **`2.2.3`**. This run mints **tertiary 2.2.3** (stale **2.2.2** target reconciled forward per Layer 1 / cursor authority).

## Scope

**In scope:** conflict domain keys, priority ladder tables, merge policy matrix versioning, rationale codes, `G-2.2.3-*` dry-run vs execute parity rows, junior stub pseudocode for merge reducer.

**Out of scope:** deterministic hook **emission** into runtime slots (**2.2.4+**), `GMM-2.4.5-*` / full CI registry proof (explicit defer rows only).

## Lane comparand — godot (A) vs sandbox (B)

| Concern | **Lane godot (A)** | **Lane sandbox (B)** |
| --- | --- | --- |
| Policy host | Resource `MergePolicyMatrix` + revision pin per session | In-memory matrix clone; identical revision namespace |
| Precedence | `ActorLanePrecedenceLadder` resource | Same ladder table in harness |
| Conflict log | `ConflictDecisionLog` append-only with stable ids | Harness log with identical tuple ordering |
| Replay | Digest joins **2.2.2** outlines + **2.1.5** replay cursor when frame tokens participate | Harness fixtures |

## Pipeline seam — 2.2.2 → 2.2.3 → 2.2.4

| Seam | Upstream | This slice (2.2.3) | Downstream |
| --- | --- | --- | --- |
| Classified intents in | [[Phase-2-2-2-Execution-Validate-Classify-Schema-and-Hook-Mapping-Roadmap-2026-04-08-2330]] | Conflict resolution + merge | **2.2.4** deterministic hook emission envelope |
| Policy revision | `mergePolicyRevision` | Binds to `catalogRevision` + `normalizationRevision` compatibility | Pre-emit payload contract only after PASS |

## Pseudocode — conflict detect / precedence / merge (junior-dev stubs)

```pseudo
func resolve_conflicts(classified: ClassifiedIntent[], policy: MergePolicyMatrix) -> ResolvedIntentSet:
  candidates = partition_by_conflict_domain(classified)
  ordered = apply_precedence_ladder(candidates, policy.precedence)
  resolved = []
  log = ConflictDecisionLog.empty()
  for group in ordered.groups:
    decision = policy.mergeMatrix.decide(group.a, group.b)
    resolved.append(apply_merge_decision(group, decision, log))
  return ResolvedIntentSet(resolved=stable_sort(resolved), log=log)
```

## Roll-up gates — `G-2.2.3-*` (execution_v1)

| Gate ID | Verdict | Evidence in this note | Owner signoff token |
| --- | --- | --- | --- |
| `G-2.2.3-Conflict-Domain-Partition` | **PASS** | Conflict key semantics + stable partitioning | `owner_signoff_G-2.2.3-Conflict-Domain-Partition_2026-04-08` |
| `G-2.2.3-Precedence-Determinism` | **PASS** | Precedence ladder + tie-break tuple | `owner_signoff_G-2.2.3-Precedence-Determinism_2026-04-08` |
| `G-2.2.3-Merge-Matrix-Coverage` | **PASS** | Matrix rows for compose/override/defer/reject | `owner_signoff_G-2.2.3-Merge-Matrix-Coverage_2026-04-08` |
| `G-2.2.3-Lane-Comparand-Parity` | **PASS** | Comparand table | `owner_signoff_G-2.2.3-Lane-Comparand-Parity_2026-04-08` |
| `G-2.2.3-GMM-CI-Deferred` | **FAIL (explicit, non-blocking)** | `GMM-2.4.5-*` / CI closure | `owner_defer_G-2.2.3-GMM-CI-Deferred_2026-04-08` |

## Deferred safety / CI seams (explicit)

| Seam | State | Notes |
| --- | --- | --- |
| `GMM-2.4.5-*` | deferred | Owner/timebox: see [[../../workflow_state-execution#Deferred safety seam closure map]] |
| Registry / CI proof | deferred | Non-blocking FAIL row; execution track evidence path TBD |

## Test plan

| Mode | Harness / fixture | Scope |
| --- | --- | --- |
| Dry-run | `fixtures/harness_intent_conflict_merge_v1` (sandbox B) + `res://test/intent/conflict_merge_dryrun.tres` (godot A) | Precedence + merge matrix paths |
| Execute | Same harness with `execute=true`; digest joins **2.2.2** + **2.1.5** when frame tokens used | Parity: identical `ResolvedIntentSet` bytes |
| Failure injection | `fixture_equal_priority_tie`, `fixture_policy_row_missing`, `fixture_cascade_conflict` | Forces tie-break, `policy_row_missing`, multi-pass resolution |

## Executable acceptance criteria

| Gate ID | Observable evidence (must pass in harness) |
| --- | --- |
| `G-2.2.3-Conflict-Domain-Partition` | Same classified set → same conflict groups |
| `G-2.2.3-Precedence-Determinism` | Repeated run → same winners and rationale codes |
| `G-2.2.3-Merge-Matrix-Coverage` | Every merge class pair either decided or explicit reject |
| `G-2.2.3-Lane-Comparand-Parity` | Godot vs sandbox produce bit-identical resolved sets for shared fixtures |
| `G-2.2.3-GMM-CI-Deferred` | Explicit FAIL row; no silent promotion |

## Related

- Parent secondary: [[Phase-2-2-Execution-Intent-Resolver-and-Hook-Mapping-Roadmap-2026-04-10-1900]]
- Prior tertiary: [[Phase-2-2-2-Execution-Validate-Classify-Schema-and-Hook-Mapping-Roadmap-2026-04-08-2330]]
- Next tertiary: **2.2.4** — deterministic hook emission envelope / pre-commit handoff (conceptual: Phase-2-2-4-…)
