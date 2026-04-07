---
title: Phase 1.3 (Execution) — First committed tick stub binding
created: 2026-04-09
tags:
  - roadmap
  - execution
  - sandbox-genesis-mythos-master
  - phase-1
para-type: Project
project-id: sandbox-genesis-mythos-master
roadmap_track: execution
roadmap-level: secondary
phase-number: 1
subphase-index: "1.3"
conceptual_counterpart: "[[../Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle/Phase-6-1-2-Bounded-Tick-Window-Scenarios-and-Sim-Visible-Classification-Matrix-Roadmap-2026-04-06-1215]]"
status: in-progress
progress: 5
handoff_readiness: 86
---

# Phase 1.3 (Execution) — First committed tick stub binding

Third **execution-local** secondary (**`1.3`**) under Phase 1 spine, per [[../decisions-log]] **D-Exec-1-numbering-policy** — cross-link only to conceptual **6.1.2** (bounded tick / sim-visible matrix); indices are **not** mirrored until PMG/MOC explicitly aligns them.

## Scope

- **In scope:** Define the **stub contract** for the **first committed tick** in the vertical-slice happy path ([[Phase-1-Execution-Vertical-Slice-Instrumentation-Spine-Roadmap-2026-04-08-2145]]): operator **seed bundle** identity → **tick commit id** that **correlates** with [[Phase-1-1-ObservationChannel-Stub-Binding-Roadmap-2026-04-06-2245]] § Sample rows (`tick-exec-0007` / `tick-exec-0008`) — **checklist + pseudocode constructors**, no host binary or CI.
- **Out of scope:** Full sim-visible matrix materialization, compare tables, engine scheduling — **execution-deferred** with same deferral language as parent.

## NL checklist (1.3)

- [x] Name the **conceptual import** (6.1.2 bounded tick / matrix) and keep it a **wikilink** only — no overwrite of frozen conceptual bodies.
- [x] Declare **tick correlation (happy + edge):** for each **1.1** operator sample row (**Happy** / **Edge**), the row’s `tick_commit_id` is **constructible** from a **`CommittedTickStub`** returned by **`firstCommittedTickFromSeed`** / **`edgeCommittedTickFromSeed`** below (execution-local vocabulary).
- [x] State **one** acceptance line: “Operator can trace seed → first committed tick id → **1.1** sample rows without contradiction.”

## Stub binding (pseudocode)

**CommittedTickStub** — minimal shape aligned with **1.1** `tick_commit_id` string namespace (`tick-exec-*`).

```pseudo
type CommittedTickStub = {
  tick_commit_id: string       // e.g. "tick-exec-0007" — must match 1.1 sample table
  seed_bundle_ref: string      // operator-visible seed handle (stub pointer)
  committed_at_index: number   // tick index at commit (correlates to 1.1 observed_at_tick)
}

function firstCommittedTickFromSeed(seed: string): CommittedTickStub
  return {
    tick_commit_id: "tick-exec-0007",
    seed_bundle_ref: "seed.stub.vs#bundle-01",
    committed_at_index: 7
  }

function edgeCommittedTickFromSeed(seed: string): CommittedTickStub
  return {
    tick_commit_id: "tick-exec-0008",
    seed_bundle_ref: "seed.stub.vs#bundle-01",
    committed_at_index: 8
  }
```

### Happy-path wire-up (stub)

- **Seed → tick:** `firstCommittedTickFromSeed` yields **`tick_commit_id`** matching **1.1** **Happy** row; **`edgeCommittedTickFromSeed`** yields **`tick-exec-0008`** for the **Edge** row.
- **Tick → observation:** **1.1** `sampleHappy()` / `sampleEdge()` use the same **`tick_commit_id`** / `observed_at_tick` pairings as these stubs (no invented ids).

## GWT-1-3-Exec (local)

| ID | Claim | Evidence hook |
| --- | --- | --- |
| GWT-1-3-Exec-A | **1.3** exists as **next** **1.x** child extending the instrumentation spine after **1.1** / **1.2** / **1.2.1** | Parent § Execution spine — 1.x children + [[workflow_state-execution]] `current_subphase_index` |
| GWT-1-3-Exec-B | **Committed tick** stubs (happy + edge constructors) correlate to **1.1** sample rows without new columns | § Stub binding + § Happy-path wire-up |

## Related

- Parent spine: [[Phase-1-Execution-Vertical-Slice-Instrumentation-Spine-Roadmap-2026-04-08-2145]]
- Upstream observation stub: [[Phase-1-1-ObservationChannel-Stub-Binding-Roadmap-2026-04-06-2245]]
- [[roadmap-state-execution]]
- [[workflow_state-execution]]
- Policy: [[../decisions-log]]
