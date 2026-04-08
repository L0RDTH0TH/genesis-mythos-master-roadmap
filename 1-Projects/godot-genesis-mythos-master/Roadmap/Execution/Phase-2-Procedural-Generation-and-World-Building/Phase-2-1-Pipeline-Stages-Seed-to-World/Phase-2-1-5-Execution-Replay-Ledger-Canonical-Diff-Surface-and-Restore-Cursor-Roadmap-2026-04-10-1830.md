---
title: Phase 2.1.5 — Execution replay ledger, canonical diff surface, restore cursor (Godot lane)
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.1.5"
project-id: godot-genesis-mythos-master
roadmap_track: execution
status: complete
priority: high
progress: 100
handoff_readiness: 86
handoff_gaps: []
execution_stub_binding: advisory_vault_anchors_only
created: 2026-04-10
tags:
  - roadmap
  - execution
  - godot-genesis-mythos-master
  - phase-2
para-type: Project
conceptual_counterpart: "[[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-5-Replay-Ledger-Canonical-Diff-Surface-and-Restore-Cursor-Roadmap-2026-03-30-2310]]"
links:
  - "[[Phase-2-1-Execution-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-08-1805]]"
  - "[[../Phase-2-Execution-Procedural-Generation-and-World-Building-Roadmap-2026-04-08-1227]]"
  - "[[Phase-2-1-4-Execution-Bundle-Identity-Seam-Catalog-Stability-and-Replay-Diff-Roadmap-2026-04-08-2241]]"
  - "[[Phase-2-1-3-Execution-Staged-Delta-Bundles-Merge-Seams-and-Apply-Ordering-Roadmap-2026-04-10-1810]]"
---

## Phase 2.1.5 — Execution replay ledger / diff / restore cursor

Execution tertiary mirror for conceptual **2.1.5**. This slice closes the **2.1.x** chain by binding **ReplayLedgerEntry**, **CanonicalDiffSurface**, and **ResumeCursor** semantics to gate rows (`G-2.1.5-*`), composing upstream **2.1.4** bundle identity + replay/diff without re-deriving **2.1.3** stage seams. Lane **godot (A)** vs **sandbox (B)** comparand parity preserved. **`GMM-2.4.5-*`** / **CI** remain **execution-deferred** (explicit non-blocking FAIL) per [[../../workflow_state-execution#Deferred safety seam closure map]].

## Lane comparand — godot (A) vs sandbox (B)

| Concern | **Lane godot (A)** | **Lane sandbox (B)** |
| --- | --- | --- |
| Replay ledger host | `ReplayLedgerEntry` resource; persisted logical record + engine trace hook | In-memory ledger tuple; identical field names |
| Canonical diff | `CanonicalDiffSurface` export for tooling/tests | Same schema; harness diff |
| Restore cursor | `ResumeCursor` binds to last trusted seam + apply ordinal from **2.1.3** ordering digest | Same resume semantics |
| Validation labels | Snapshot of `validationLabelSet` at Stage 4 boundary | Identical label namespace |

> [!note] Gate semantics (execution track)
> **`PASS`** on **`G-2.1.5-*`** means **documentation completeness + explicit deferrals** for junior-dev stubs — **not** shipped storage engines, encryption, or CI proofs.

## Pipeline stage seams (seed → world) — composition

| Seam | Upstream owner | Binding |
| --- | --- | --- |
| S0→S1 | **2.1** secondary stage matrix | Ledger records `stageWindow` spanning attempted stages |
| S4 dry-run / S5 commit | **2.1** + **2.1.3** | `resumeCursor` points to last trusted seam or apply ordinal on `restore-required` |
| Bundle / catalog | **2.1.4** | `bundleIdentity`, `seamCatalogRevision` copied into ledger entry |

## `G-2.1.5-*` gate rows (execution)

| Gate ID | Check | Evidence in this note | Verdict | Owner token |
| --- | --- | --- | --- | --- |
| `G-2.1.5-Ledger-Shape` | **ReplayLedgerEntry** fields populated; ties to **2.1.4** identity + catalog rev | [[#Replay ledger shape (stub)]] | **PASS** | `owner_signoff_G-2.1.5-Ledger-Shape_2026-04-10` |
| `G-2.1.5-Diff-Surface` | **CanonicalDiffSurface** exposes seam/op/label/cursor deltas deterministically | [[#Canonical diff surface (stub)]] | **PASS** | `owner_signoff_G-2.1.5-Diff-Surface_2026-04-10` |
| `G-2.1.5-Restore-Cursor` | **ResumeCursor** deterministic on pass vs fail; rejects stale labels | [[#Restore cursor rules]] | **PASS** | `owner_signoff_G-2.1.5-Restore-Cursor_2026-04-10` |
| `G-2.1.5-Trace-Chain` | Bidirectional hooks to **2.1.3** seams + **2.1.4** diff for replay traceability | [[#Replay traceability hooks]] | **PASS** | `owner_signoff_G-2.1.5-Trace-Chain_2026-04-10` |
| `G-2.1.5-Registry-CI-Deferred` | No claim of registry/CI closure | [[#Deferred registry / CI]] | **FAIL (explicit, non-blocking)** | `owner_defer_G-2.1.5-Registry-CI-Deferred_2026-04-10` |

## Replay ledger shape (stub)

| Field | Role | Notes |
| --- | --- | --- |
| `bundleIdentity` | From **2.1.4** | Stable logical key |
| `seamCatalogRevision` | From **2.1.4** | Monotonic with migration rules |
| `validationLabelSet` | Stage 4 snapshot | Reject stale labels on restore |
| `resumeCursor` | [[#Restore cursor rules]] | `commit-ready` vs `restore-required` |
| `stageWindow` | S0–S5 coverage | Links **2.1** matrix |
| `timestampLogical` | Deterministic ordering token | Not wall-clock authority |

## Canonical diff surface (stub)

| Delta class | Description |
| --- | --- |
| `seamDelta[]` | Add/remove/move seam records |
| `opDelta[]` | Ordered apply op changes |
| `labelDelta[]` | Validation label drift |
| `cursorDelta` | Movement of `resumeCursor` |

## Restore cursor rules

- **Pass path:** cursor `commit-ready`; references Stage 5 boundary token from **2.1** pseudocode seam.
- **Fail path:** cursor `restore-required`; `resumeFromSeam` + `resumeFromApplyOrdinal` from **2.1.3** merge/apply ordering digest; **rejects** stale labels.
- **Catalog mismatch:** restore valid only with explicit migration policy (**2.1.4** rules).

## Replay traceability hooks

- **Seed → world lineage:** ledger entry links `bundleIdentity` + `manifest_digest` stub (execution-deferred) for [[../Phase-2-Execution-Procedural-Generation-and-World-Building-Roadmap-2026-04-08-1227#Pending replay lineage — `phase2_gate_replay_traceability`]].
- **Chain evidence:** closes tertiary gap **2.1.3–2.1.5** for `phase2_gate_replay_traceability` primary row when combined with **2.1.4** diff contracts.

## Pseudocode (junior-dev stub)

```pseudo
func build_replay_ledger(bundle, validation_result):
  cursor = derive_resume_cursor(bundle, validation_result)
  return ReplayLedgerEntry(
    bundle.identity,
    bundle.catalog_rev,
    validation_result.labels,
    cursor,
    stage_window_from_matrix(),
    logical_timestamp(bundle, validation_result)
  )

func diff_replay_ledger(a, b):
  return CanonicalDiffSurface(
    seam_delta(a.bundle, b.bundle),
    op_delta(a.applyOrdinal, b.applyOrdinal),
    label_delta(a.labels, b.labels),
    cursor_delta(a.resumeCursor, b.resumeCursor)
  )
```

## Deferred registry / CI

| Item | Owner role | Timebox | Evidence path (planned) |
| --- | --- | --- | --- |
| `GMM-2.4.5-*` | registry/tech lead | **2026-04-22** | [[../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-1-Execution-Node-Taxonomy-Edges-and-Topological-Order-Roadmap-2026-04-10-1416]] |
| `CI-deferrals` | build/CI owner | **2026-04-29** | [[../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-Execution-Procedural-Generation-Graph-Skeleton-Roadmap-2026-04-10-1415]] |

## Test matrix (executable sketch)

| Case ID | Fixture | Expected | Pass ties to |
| --- | --- | --- | --- |
| TM-2.1.5-01 | Pass validation | Ledger `commit-ready`; cursor at S5 | `G-2.1.5-Restore-Cursor` |
| TM-2.1.5-02 | Fail validation | `restore-required`; resume ordinal rewinds | `G-2.1.5-Restore-Cursor` |
| TM-2.1.5-03 | Two ledgers, same bundle id, drifted labels | `labelDelta` non-empty | `G-2.1.5-Diff-Surface` |

## Acceptance criteria

1. Mirrored path matches conceptual subtree (parallel spine).
2. `G-2.1.5-*` rows are explicit PASS or explicit non-blocking FAIL for deferrals.
3. Replay ledger + diff + restore semantics compose **2.1.4** without duplicating **2.1.3** seam tables.
4. Lane A/B comparand remains machine-traceable.

## Related

- Prior tertiary **2.1.4**: [[Phase-2-1-4-Execution-Bundle-Identity-Seam-Catalog-Stability-and-Replay-Diff-Roadmap-2026-04-08-2241]]
- Prior tertiary **2.1.3**: [[Phase-2-1-3-Execution-Staged-Delta-Bundles-Merge-Seams-and-Apply-Ordering-Roadmap-2026-04-10-1810]]
- Parent secondary: [[Phase-2-1-Execution-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-08-1805]]
- Phase 2 primary: [[../Phase-2-Execution-Procedural-Generation-and-World-Building-Roadmap-2026-04-08-1227]]
