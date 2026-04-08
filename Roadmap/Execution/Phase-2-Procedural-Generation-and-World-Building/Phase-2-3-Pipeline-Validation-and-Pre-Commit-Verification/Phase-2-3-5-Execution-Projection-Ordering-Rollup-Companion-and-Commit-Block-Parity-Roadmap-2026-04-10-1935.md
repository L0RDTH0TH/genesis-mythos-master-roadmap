---
title: Phase 2.3.5 — Execution projection ordering, rollup companion, and commit-block parity (Godot lane)
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.3.5"
project-id: godot-genesis-mythos-master
roadmap_track: execution
status: complete
priority: high
progress: 100
handoff_readiness: 87
handoff_gaps: []
created: 2026-04-10
tags:
  - roadmap
  - execution
  - godot-genesis-mythos-master
  - phase-2
para-type: Project
conceptual_counterpart: "[[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-3-Pipeline-Validation-and-Pre-Commit-Verification/Phase-2-3-5-Projection-Ordering-Rollup-Companion-and-Commit-Block-Parity-Roadmap-2026-03-31-0218]]"
links:
  - "[[Phase-2-3-Execution-Pipeline-Validation-and-Pre-Commit-Verification-Roadmap-2026-04-10-1805]]"
  - "[[Phase-2-3-1-Execution-Validation-Test-Plan-and-Acceptance-Criteria-Scaffold-Roadmap-2026-04-10-2105]]"
  - "[[Phase-2-3-2-Execution-Verification-Task-Decomposition-and-Failure-Payload-Contracts-Roadmap-2026-04-10-2145]]"
  - "[[Phase-2-3-3-Execution-Projection-Contract-Branch-Warm-Cache-Guardrails-and-Operator-Pick-Traceability-Roadmap-2026-04-10-2206]]"
  - "[[Phase-2-3-4-Execution-Bound-Projection-Contract-Continuation-Warm-Cache-Validation-Trace-Roadmap-2026-04-10-2230]]"
  - "[[../Phase-2-Execution-Procedural-Generation-and-World-Building-Roadmap-2026-04-08-1227]]"
---

## Phase 2.3.5 — Projection ordering, rollup companion, commit-block parity

Execution tertiary mirror for conceptual **2.3.5**. Closes the **2.3.x** chain: **deterministic ordering** for `OrderedGateFailurePayload[]`, **ValidationRollupCompanion** as non-authoritative companion only, and **CommitEligibilityVerdict** parity across warm-cache vs cold-path (**O-2.3.5-01/02**, **C-2.3.5-01**). Composes **2.3.4** trace schema + **2.3.2** task decomposition. Lane **godot (A)** vs **sandbox (B)** comparand preserved.

> [!note] Queue reconcile — stale **2.2.3** target vs live cursor **`2.3.5`**
> Queue `followup-deepen-exec-p223-tertiary-godot-20260410T193500Z` / `user_guidance` requested mint **execution tertiary 2.2.3** under `Phase-2-2-Intent-Resolver-and-Hook-Mapping/`. **Tertiary 2.2.3** is already **complete** on disk — [[../Phase-2-2-Intent-Resolver-and-Hook-Mapping/Phase-2-2-3-Execution-Conflict-Resolution-Priority-Ordering-and-Merge-Policy-Roadmap-2026-04-08-2350]] (**[[../../workflow_state-execution]]** Iter **22**). Authoritative pre-read cursor in [[../../workflow_state-execution]] was **`current_subphase_index: "2.3.5"`** (after **2.3.4** Iter **29**). **stale_queue_target_reconciled: true** — this run mints **tertiary 2.3.5** (not a duplicate **2.2.3**). Theme alignment: user-requested **G-2.2.3-*** / conflict-merge patterns are **already satisfied** on the **2.2.3** note; this mint completes **2.3** validation projection closure per conceptual **2.3.5**.

## Scope

**In scope:** `T-2.3.5-01`–`T-2.3.5-04` binding tables; `G-2.3.5-*` dry-run vs execute parity rows; `V-2.3.5-A–D` harness stubs; junior stub pseudocode for ordering + rollup companion + commit verdict parity check.

**Draft / not execution proof:** Task and harness tables below are **scaffold placeholders** until replay/fixture ids exist — do not treat as machine-verified CI harness proof without a dedicated hardening queue entry.

**Out of scope:** UI surfaces, storage engines, `GMM-2.4.5-*` / full **CI-deferrals** closure (explicit non-blocking FAIL rows only).

## Lane comparand — godot (A) vs sandbox (B)

| Concern | **Lane godot (A)** | **Lane sandbox (B)** |
| --- | --- | --- |
| Ordering keys | `GateKeyOrdinal` resource table pinned per session | In-memory table; identical tuple ordering |
| Rollup companion | Derived view; cannot override authoritative payloads | Same derivation rule |
| Commit verdict | `CommitEligibilityVerdict` resource | Harness enum with identical transitions |
| Trace closure | `projection_ordering_version` + `decision_id` backlinks | Synthetic ids; same invariants |

## Pipeline seams — 2.3.4 → 2.3.5 → secondary 2.3 rollup

| Seam | Upstream | This slice (2.3.5) | Downstream |
| --- | --- | --- | --- |
| Trace + warm-cache | [[Phase-2-3-4-Execution-Bound-Projection-Contract-Continuation-Warm-Cache-Validation-Trace-Roadmap-2026-04-10-2230]] | Ordering + rollup companion + commit parity closes **2.3.x** structural chain | **Secondary 2.3 rollup** (`G-2.3-*` PASS propagation + `rollup_2_primary_from_2_3`) |
| Tasks | [[Phase-2-3-2-Execution-Verification-Task-Decomposition-and-Failure-Payload-Contracts-Roadmap-2026-04-10-2145]] | `T-2.3.5-*` rows cite `T-2.3.2-*` payload fields | Rollup rows on secondary **2.3** |
| Matrix | [[Phase-2-3-1-Execution-Validation-Test-Plan-and-Acceptance-Criteria-Scaffold-Roadmap-2026-04-10-2105]] | `V-2.3.5-*` binds to `V-2.3-*` columns | No schema fork |

## Invariants (execution binding)

### **O-2.3.5-01** — Deterministic projection ordering

1. Sort `OrderedGateFailurePayload[]` by stable gate key + deterministic stage order **before** any rollup companion.
2. Rollup companion is generated **only** from finalized authoritative payloads.
3. Warm-cache vs cold-path runs use **identical** ordering keys (parity check emits trace row on mismatch).

### **O-2.3.5-02** — Rollup non-authority

Rollup may summarize or group; it **must not** delete, merge away, or override any mandatory gate payload row.

### **C-2.3.5-01** — Commit-block parity

Mandatory gate failure ⇒ `deny_commit`; cache hit/miss does not change verdict; operator-facing summary may differ in readability, **never** in outcome.

## `G-2.3.5-*` gate rows (execution)

| Gate ID | Check | Evidence | Verdict | Owner token |
| --- | --- | --- | --- | --- |
| `G-2.3.5-Ordering-Determinism` | **O-2.3.5-01** satisfied | [[#**O-2.3.5-01** — Deterministic projection ordering]] | **PASS** | `owner_signoff_G-2.3.5-Ordering-Determinism_2026-04-10` |
| `G-2.3.5-Rollup-Non-Authority` | **O-2.3.5-02** satisfied | [[#**O-2.3.5-02** — Rollup non-authority]] | **PASS** | `owner_signoff_G-2.3.5-Rollup-Non-Authority_2026-04-10` |
| `G-2.3.5-Commit-Parity` | **C-2.3.5-01** satisfied | [[#**C-2.3.5-01** — Commit-block parity]] | **PASS** | `owner_signoff_G-2.3.5-Commit-Parity_2026-04-10` |
| `G-2.3.5-Lane-Comparand-Parity` | godot vs sandbox tables | [[#Lane comparand — godot (A) vs sandbox (B)]] | **PASS** | `owner_signoff_G-2.3.5-Lane-Comparand-Parity_2026-04-10` |
| `G-2.3.5-GMM-CI-Deferred` | No registry/CI closure | [[#Deferred registry / CI]] | **FAIL (explicit, non-blocking)** | `owner_defer_G-2.3.5-GMM-CI-Deferred_2026-04-10` |

## Task table — `T-2.3.5-*` (draft stubs — not execution proof)

| Task ID | Owner stage | Binding |
| --- | --- | --- |
| `T-2.3.5-01` | validation projection | Normalize payloads → stable ordering keys (`V-2.3.5-A` / `V-2.3.5-B`) |
| `T-2.3.5-02` | diagnostics aggregation | Build rollup companion from ordered rows only |
| `T-2.3.5-03` | commit gate | Warm vs cold parity check → trace (`V-2.3.5-B`) |
| `T-2.3.5-04` | trace sink | Persist operator-pick backlinks (`V-2.3.5-D`) |

## Harness matrix — `V-2.3.5-*` (draft stubs — not execution proof)

| ID | Scenario | Expected |
| --- | --- | --- |
| `V-2.3.5-A` | Cold-path mandatory fail | ordered payloads + `deny_commit` |
| `V-2.3.5-B` | Warm-cache same frame | identical ordering keys + `deny_commit` |
| `V-2.3.5-C` | Rollup generation fails | commit derived from payloads only |
| `V-2.3.5-D` | Operator pick changes | new frame uses latest pick; prior trace immutable |

## Deferred registry / CI

| Seam | State | Notes |
| --- | --- | --- |
| `GMM-2.4.5-*` | open | Review `2026-04-22` per [[../../workflow_state-execution#Deferred safety seam closure map]] |
| `CI-deferrals` | open | Review `2026-04-29` |

## Pseudocode — ordering + rollup + verdict (junior-dev stubs)

```pseudo
func finalize_projection(frame: ValidationFrame) -> ProjectionOrderingResult:
  ordered = stable_sort_by_gate_key(frame.mandatory_failures)
  companion = build_rollup_companion(ordered)  // non-authoritative
  verdict = commit_eligibility(ordered)         // identical warm/cold
  return ProjectionOrderingResult(ordered, companion, verdict)

func commit_eligibility(ordered: OrderedGateFailurePayload[]) -> CommitEligibilityVerdict:
  if any_mandatory_failed(ordered):
    return deny_commit
  return allow_commit
```

## Conflict / merge stubs (cross-slice alignment)

| Topic | Execution hook | Notes |
| --- | --- | --- |
| Intent conflicts | Consumes **2.2.3** `ResolvedIntentSet` semantics only as **non-authoritative** context for validation framing | **2.2.3** already minted — no duplicate work this run |
| Merge policy | Ordering layer **does not** re-resolve merge matrix — uses classified gate keys only | Parity with **2.2.3** reducer outputs via stable ids |

## Related

- Conceptual authority: [[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-3-Pipeline-Validation-and-Pre-Commit-Verification/Phase-2-3-5-Projection-Ordering-Rollup-Companion-and-Commit-Block-Parity-Roadmap-2026-03-31-0218]]
- Prior tertiary: [[Phase-2-3-4-Execution-Bound-Projection-Contract-Continuation-Warm-Cache-Validation-Trace-Roadmap-2026-04-10-2230]]
- Secondary parent: [[Phase-2-3-Execution-Pipeline-Validation-and-Pre-Commit-Verification-Roadmap-2026-04-10-1805]]
