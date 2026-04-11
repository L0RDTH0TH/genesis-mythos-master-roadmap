---
title: Phase 1.1.2 (Execution) — Observation, cache, and invalidation
created: 2026-04-10
tags:
  - roadmap
  - execution
  - sandbox
  - layering
  - observation
  - cache
project-id: sandbox-genesis-mythos-master
roadmap_track: execution
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.1.2"
status: in-progress
handoff_readiness: 86
handoff_readiness_basis: design_traceability_pre_evidence
handoff_readiness_note: "Score reflects NL alignment to conceptual 1.1.2, seam tables, and intent mapping; not evidence closure while AC rows remain Planned."
conceptual_counterpart: "[[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-2-Observation-Cache-and-Invalidation-Roadmap-2026-03-30-1325]]"
---

# Phase 1.1.2 (Execution) — Observation, cache, and invalidation

Execution tertiary **1.1.2** on the **parallel spine** under `Phase-1-1-Layering-and-Interface-Contracts/`, aligned to conceptual [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-2-Observation-Cache-and-Invalidation-Roadmap-2026-03-30-1325]]. Focus: **read-only observation paths**, **derived caches** keyed by commit **version/epoch**, **hard invalidation** after successful commits, and **swap-coordinator** hooks consistent with 1.1.1 commit ordering. **GMM-2.4.5** lineage/compare harnesses and **CI closure** remain **explicitly deferred** unless evidenced later.

Parent execution secondary: [[Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-04-10-2205]] · Phase 1 execution primary: [[../Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-04-10-2100]] · Prior tertiary: [[Phase-1-1-1-Layer-Boundary-and-Commit-Pipeline-Roadmap-2026-04-10-2306]]

## Handoff readiness vs evidence

**Handoff readiness** on this slice is **design- and traceability-first**: conceptual alignment, observation/cache seams, and intent mapping. It does **not** claim execution evidence until at least one AC row advances beyond **Planned**. **`status: in-progress`** means this tertiary’s spec and hooks are not closed out in-repo; it does **not** mean the automation cursor is still on `1.1.2` — see [[../../workflow_state-execution]] (`current_subphase_index` points at the **next** deepen target).

## Slice status vs execution cursor

- This note is the **1.1.2** execution spec slice (observation / cache / invalidation).
- **`workflow_state-execution`** **`current_subphase_index: 1.1.3`** is the **next** structural deepen step after this mint; the cursor has already advanced past 1.1.2 in automation state.

## Alignment to conceptual Phase-1-1-2

| Conceptual contract | Execution mechanism (this note) | Validation signal |
| --- | --- | --- |
| Observation without authority inversion | `observe` / `subscribe` seams + poll vs push labeling | AC-1.1.2.E1–E2 |
| Derived caches keyed by `(interest, commit version)` | `cache_key` table + version bump rules | AC-1.1.2.E3 |
| Invalidation ordering after commit | `on_commit_success` hook ordering vs `tick_commit` from 1.1.1 | AC-1.1.2.E4 |
| Hot-swap / tooling behind stable contracts | `swap_coordinator` single hook + quiesce barrier | AC-1.1.2.E5 |

## Observation and cache seam (execution)

**Ordering (hard):** Successful `world.commit` from [[Phase-1-1-1-Layer-Boundary-and-Commit-Pipeline-Roadmap-2026-04-10-2306]] **must** bump **epoch/version** before any consumer claims an authoritative read for gameplay; render/UI may lag one frame with explicit **stale** labeling only for non-authoritative presentation.

```text
on_commit_success(tick_id, new_version, committed_delta):
  broadcast_version(new_version)                    # push path; poll path uses read_version()
  for cache in registered_derived_caches:
    if cache.key_space overlaps committed_delta:
      cache.invalidate_or_rebuild()
  presentation.set_last_authoritative_version(new_version)
  swap_coordinator.notify_epoch_if_quiesced(new_version)
```

## Boundary matrix (tertiary tightening)

| Seam | Upstream | Downstream | Forbidden |
| --- | --- | --- | --- |
| World → Observers | `version`, `subscribe` | Read models, tooling | Downstream feeding back into `commit` except via ingress |
| World → Derived caches | Commit envelope + delta footprint | Cache rebuild / dirty | Serving authoritative gameplay from pre-invalidation cache |
| Presentation → Player | Frames tagged with `version` | UX | Silent stale gameplay state without stale flag when version lags |
| Swap coordinator | Quiesce signal | Replacement behind interface | Partial teardown mid-commit |

## Acceptance criteria — evidence hooks

| ID | Criterion | Evidence artifact (planned) | Status |
| --- | --- | --- | --- |
| AC-1.1.2.E1 | Observation paths are read-only w.r.t. authoritative state | `observer_audit.tsv` (seam, mode poll/push) | Planned |
| AC-1.1.2.E2 | Pre-commit staging is not a gameplay authority surface | `staging_visibility.json` (debug-only matrix) | Planned |
| AC-1.1.2.E3 | Every derived cache declares key space + invalidation trigger | `cache_registry.md` | Planned |
| AC-1.1.2.E4 | Version monotonicity: no consumer sees skipped epochs for authority | `version_trace.jsonl` | Planned |
| AC-1.1.2.E5 | Swap coordinator serializes replace after quiesce or deferred activation | `swap_coordinator_log.txt` | Planned |

## Intent Mapping

| Design intent target | Inspiration anchors | Execution mechanism | Validation signal |
| --- | --- | --- | --- |
| Observation + cache NL (conceptual 1.1.2) | Conceptual behavior + 1.1.1 commit ordering (**vault-only** — no external URL anchor in this slice) | `on_commit_success` + seam table | AC-1.1.2.E3–E4 |
| Epoch / version as invalidation driver | Conceptual “bump on commit” | `broadcast_version` + cache overlap rule | AC-1.1.2.E4 |
| Hot-swap without split brain | Conceptual swap coordinator | Single `swap_coordinator` hook + quiesce | AC-1.1.2.E5 |

## Risks (v0)

| Risk | Mitigation | Linked AC |
| --- | --- | --- |
| Fine-grained vs batched epoch bumps | Document policy; default batched per tick | AC-1.1.2.E4 |
| Predictive render vs authority | Keep extrapolation non-authoritative | AC-1.1.2.E2 |
| Scope creep into GMM-2.4.5 / CI | Explicit deferrals in note + ledger | Deferrals |

## Explicit deferrals

- **GMM-2.4.5-*** comparator / cross-lane harness: not claimed.
- **CI** gates (coverage, stress matrices): not claimed.
- **New** verbatim C/C++ standard API citations: deferred to a future run that invokes lane Research with allowlisted URLs; this slice uses **pseudocode** and **reuse-only** references to parent execution notes (same pattern as execution **1.1.1**).

## Code precision (reuse-only)

No new C/C++ standard API surfaces in this slice. **Code precision authority** remains on the Phase 1 execution primary ([[../Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-04-10-2100]]) until a Research-backed pass adds allowlisted citations.

## Next structural intent

Deepen execution tertiary **1.1.3** (dependency direction / lifecycle) on the mirrored spine — conceptual [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-3-Dependency-Direction-and-Lifecycle-Roadmap-2026-03-30-1420]].
