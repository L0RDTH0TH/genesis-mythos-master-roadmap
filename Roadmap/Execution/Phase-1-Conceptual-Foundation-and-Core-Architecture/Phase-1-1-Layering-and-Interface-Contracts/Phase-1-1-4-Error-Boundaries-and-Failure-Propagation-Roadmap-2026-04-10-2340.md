---
title: Phase 1.1.4 (Execution) — Error boundaries and failure propagation
created: 2026-04-10
tags:
  - roadmap
  - execution
  - sandbox
  - layering
  - errors
  - recovery
project-id: sandbox-genesis-mythos-master
roadmap_track: execution
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.1.4"
status: in-progress
handoff_readiness: 85
handoff_readiness_basis: design_traceability_pre_evidence
handoff_readiness_note: "Score reflects NL alignment to conceptual 1.1.4, failure-class seams vs 1.1.1–1.1.3, and intent mapping; not evidence closure while AC rows remain Planned."
conceptual_counterpart: "[[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-4-Error-Boundaries-and-Failure-Propagation-Roadmap-2026-03-30-1430]]"
---

# Phase 1.1.4 (Execution) — Error boundaries and failure propagation

Execution tertiary **1.1.4** on the **parallel spine** under `Phase-1-1-Layering-and-Interface-Contracts/`, aligned to conceptual [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-4-Error-Boundaries-and-Failure-Propagation-Roadmap-2026-03-30-1430]]. Focus: **error surfaces per layer**, **propagation rules** across layer boundaries (hard stop vs degraded mode), **invariants after failure** (no partial commits; no orphaned observers), and **recovery hooks** (retry, reload snapshot, quiesce + swap) composed with **commit pipeline** ([[Phase-1-1-1-Layer-Boundary-and-Commit-Pipeline-Roadmap-2026-04-10-2306]]), **observation/cache** ([[Phase-1-1-2-Observation-Cache-and-Invalidation-Roadmap-2026-04-10-2315]]), and **dependency/lifecycle** ([[Phase-1-1-3-Dependency-Direction-and-Lifecycle-Roadmap-2026-04-10-2325]]). **GMM-2.4.5** cross-lane harnesses and **CI / registry closure** remain **explicitly deferred** unless evidenced later.

Parent execution secondary: [[Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-04-10-2205]] · Phase 1 execution primary: [[../Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-04-10-2100]] · Prior tertiary: [[Phase-1-1-3-Dependency-Direction-and-Lifecycle-Roadmap-2026-04-10-2325]]

## Handoff readiness vs evidence

**Handoff readiness** on this slice is **design- and traceability-first**: conceptual alignment, failure/propagation seams, and intent mapping. It does **not** claim execution evidence until at least one AC row advances beyond **Planned**.

## Slice status vs execution cursor

- This note is the **1.1.4** execution spec slice (error boundaries / failure propagation / recovery).
- After this mint, **`workflow_state-execution`** **`current_subphase_index`** advances to **`1.1.5`** (next deepen target).

## Alignment to conceptual Phase-1-1-4

| Conceptual contract | Execution mechanism (this note) | Validation signal |
| --- | --- | --- |
| Failure classification (authoritative / transient / presentational / tooling) | `FailureClass` enum + routing table | AC-1.1.4.E1 |
| Bounded propagation; no cross-layer “fixes” except commit API | `route_failure` + forbidden bypass list | AC-1.1.4.E2 |
| Invariants after failure (no partial commits; caches invalidate on epoch) | Integrates 1.1.1 abort + 1.1.2 invalidation | AC-1.1.4.E3 |
| Recovery: soft / hard / swap | `recover_soft` / `reload_snapshot` / `swap_coordinator` path from 1.1.3 | AC-1.1.4.E4 |

## Failure routing (execution)

**Rule:** Every layer **surfaces** failures through a **single** classification step before any cross-layer move. Higher layers **must not** write world state except via the **commit ingress** from 1.1.1.

> [!note] Notional pseudocode (dialect)
> Fenced blocks below use **language-agnostic illustrative IL** (dot/member syntax is for readability when mapping to C++ engine seams). They are **not** Python, final GDScript, or committed C++ surface APIs.

```text
route_failure(layer, failure):
  if failure.class == authoritative:
    commit_pipeline.abort_pending()           # 1.1.1
    assert world.consistent_or_reload()       # hard recovery
    bump_epoch_and_invalidate_caches()        # 1.1.2
  elif failure.class == transient:
    sim.schedule_retry(bounded=3)
  elif failure.class == presentational:
    ui.show_failure_summary(read_only=True)
  # tooling: cancel without touching play state / epoch
```

## Seams vs 1.1.1–1.1.3

| Seam | Upstream | Downstream | Forbidden |
| --- | --- | --- | --- |
| Commit abort | Authoritative failure | 1.1.1 pipeline | Partial commit after abort |
| Epoch / cache | Failed-then-retried path | 1.1.2 observers | Stale cache after epoch bump |
| Quiesce / teardown | Recovery + swap | 1.1.3 lifecycle | Teardown before quiesce on recovery |
| Intent routing | UI / tools | Simulation → commit | Direct world write on “fix” |

## Failure propagation (pseudocode)

```text
on_tick_failure(sim_failure):
  if sim_failure.implies_inconsistent_world:
    commit_pipeline.abort_pending()
    world.reload_last_consistent_snapshot_or_fail()
  else:
    sim.schedule_retry(bounded=3)
  notify_observers_non_authoritative(summary(sim_failure))
```

## Acceptance criteria — evidence hooks

| ID | Criterion | Evidence artifact (planned) | Status |
| --- | --- | --- | --- |
| AC-1.1.4.E1 | Failure classes documented and routed; no silent cross-layer repair | `failure_routing_matrix.md` | Planned |
| AC-1.1.4.E2 | Authoritative failures abort pending commit before any world mutation | `abort_before_mutate_log.jsonl` | Planned |
| AC-1.1.4.E3 | Epoch bump on authoritative failure invalidates observation caches per 1.1.2 | `epoch_invalidation_trace.txt` | Planned |
| AC-1.1.4.E4 | Soft / hard / swap recovery paths traceable to 1.1.3 coordinator | `recovery_path_trace.json` | Planned |

> [!tip] Roll-up posture (execution debt)
> While **E1–E4** remain **Planned**, project-scale **roll-up gates**, **registry/CI-shaped closure**, and **GMM-2.4.5** harness work stay **explicitly deferred** per this slice and [[../Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-04-10-2100]] — not hidden behind “done” language.

## Intent mapping

| Design intent target | Inspiration anchors | Execution mechanism | Validation signal |
| --- | --- | --- | --- |
| Classification + boundaries (conceptual 1.1.4) | Conceptual NL + 1.1.1 commit authority | `route_failure` + seam table | AC-1.1.4.E1–E2 |
| Propagation + invariants | 1.1.2 epoch / cache | Abort + invalidate + observer rules | AC-1.1.4.E3 |
| Recovery composition | 1.1.3 lifecycle | Soft/hard/swap paths | AC-1.1.4.E4 |

## Risks (v0)

| Risk | Mitigation | Linked AC |
| --- | --- | --- |
| Duplicate failure handling in sim vs commit | Single `authoritative` gate | AC-1.1.4.E2 |
| UI “fixes” bypassing intents | Route all fixes through intents → sim → commit | AC-1.1.4.E1 |
| Scope creep into GMM-2.4.5 / CI | Explicit deferrals | Deferrals |

## Explicit deferrals

- **GMM-2.4.5-*** comparator / cross-lane harness: not claimed.
- **CI** gates (coverage, stress matrices): not claimed.
- **New** verbatim C/C++ standard API citations: deferred to a future Research-backed pass with allowlisted URLs; this slice uses **pseudocode** and **reuse-only** references to sibling execution notes (same pattern as execution **1.1.3**).

## Code precision (reuse-only)

No new C/C++ standard library API surfaces in this slice. **Code precision authority** for verbatim standard citations remains on the Phase 1 execution primary ([[../Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-04-10-2100]]) until a lane Research pass adds allowlisted citations.

## Next structural intent

Deepen execution tertiary **1.1.5** on the mirrored spine — follow [[workflow_state-execution]] cursor after this run.
