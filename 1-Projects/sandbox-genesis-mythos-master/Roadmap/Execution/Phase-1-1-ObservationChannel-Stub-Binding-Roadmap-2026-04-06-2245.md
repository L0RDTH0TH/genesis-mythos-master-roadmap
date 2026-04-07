---
title: Phase 1.1 (Execution) — ObservationChannel stub binding
created: 2026-04-06
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
subphase-index: "1.1"
conceptual_counterpart: "[[../Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle/Phase-6-1-3-ObservationChannel-Lane-Readout-and-Presentation-Time-Co-Display-Roadmap-2026-04-07-1015]]"
status: in-progress
progress: 10
handoff_readiness: 88
---

# Phase 1.1 (Execution) — ObservationChannel stub binding

First **execution-local** secondary (**`1.1`**) under Phase 1 spine, per [[../decisions-log]] **D-Exec-1-numbering-policy** — cross-link only to conceptual **6.1.3**; indices are **not** mirrored until PMG/MOC explicitly aligns them.

## Scope

- **In scope:** Define the **stub contract** for one **ObservationChannel** sample row shape (labels, tick id, lane id, payload envelope reference) that the vertical-slice happy path in parent [[Phase-1-Execution-Vertical-Slice-Instrumentation-Spine-Roadmap-2026-04-08-2145]] can cite — **checklist + acceptance lines**, no host binary or CI.
- **Out of scope:** Registry row materialization (`GMM-2.4.5-*`), compare tables, PresentationEnvelope rendering implementation — **execution-deferred** with same deferral language as parent.

## NL checklist (1.1)

- [x] Name the **conceptual import** (6.1.3 readout lane) and keep it a **wikilink** only — no overwrite of frozen conceptual bodies.
- [x] **Sample row schema (stub):** minimum fields documented below (execution-deferred: no binary / CI).
- [x] State **one** acceptance line: “Operator can trace from this note to parent happy path and to 6.1.3 without contradiction.”

### Sample row schema (stub fields)

| Field | Role |
| --- | --- |
| `tick_commit_id` | Committed tick identifier for correlation |
| `channel_lane` | ObservationChannel lane label |
| `sample_label` | Human-readable sample id |
| `envelope_ref` | Pointer to instrumentation envelope / manifest row (stub) |
| `observed_at_tick` | Tick index at observation |

### Sample rows (operator table) — concrete stubs

Two **deterministic** rows that **populate every** schema column and feed **1.2** `stubMapSampleToReadout` / **1.2.1** `drillReadout` without field invention (execution-deferred: no host binary).

| Row | `tick_commit_id` | `channel_lane` | `sample_label` | `envelope_ref` | `observed_at_tick` | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| **Happy** | `tick-exec-0007` | `lane.obs.vs.happy` | `sample-vs-01` | `env.stub.vs#row-01` | `7` | Matches **1.2.1** happy drill input class; `readout_text` in **1.2** stub **must** embed `string(observed_at_tick)` |
| **Edge (non-PreCommit)** | `tick-exec-0008` | `lane.obs.vs.edge` | `sample-vs-02` | `env.stub.vs#row-02` | `8` | Same shape; used only to prove **schema stability** — **1.2.1** negative path is **gate**-blocked, not row-shape-blocked |

## Stub type (pseudocode) — parity with 1.2 `ObservationChannelSample`

Execution-local **fenced type** matches the five fields used in [[Phase-1-2-PresentationEnvelope-Stub-Roadmap-2026-04-06-1200]] § Stub binding (pseudocode) (`ObservationChannelSample`). The § Sample row schema table above is the operator-facing view of this same shape.

```pseudo
// Byte-aligned with 1.2 stubMapSampleToReadout input type (five fields).
type ObservationChannelSample = {
  tick_commit_id: string
  channel_lane: string
  sample_label: string
  envelope_ref: string
  observed_at_tick: number
}
```

### Wire-up pseudocode (1.1 → 1.2 / 1.2.1)

**Polish pass:** explicit **construction** from the § Sample rows table into `ObservationChannelSample`, then **delegation** to **1.2** / **1.2.1** entry points (same symbols as [[Phase-1-2-PresentationEnvelope-Stub-Roadmap-2026-04-06-1200]] § Stub binding and [[Phase-1-2-1-PresentationEnvelope-Tertiary-Readout-Detail-Roadmap-2026-04-09-1521]] § Drill pseudocode).

```pseudo
// Literal constructors — values match § Sample rows (operator table) exactly.
function sampleHappy(): ObservationChannelSample
  return {
    tick_commit_id: "tick-exec-0007",
    channel_lane: "lane.obs.vs.happy",
    sample_label: "sample-vs-01",
    envelope_ref: "env.stub.vs#row-01",
    observed_at_tick: 7
  }

function sampleEdge(): ObservationChannelSample
  return {
    tick_commit_id: "tick-exec-0008",
    channel_lane: "lane.obs.vs.edge",
    sample_label: "sample-vs-02",
    envelope_ref: "env.stub.vs#row-02",
    observed_at_tick: 8
  }

// Parity: downstream only sees ObservationChannelSample — no extra columns.
function toPresentationStub(s: ObservationChannelSample, g: PresentationCoDisplayGate): ReadoutDrillResult
  return drillReadout(s, g)
```

## GWT-1-1-Exec (local)

| ID | Claim | Evidence hook |
| --- | --- | --- |
| GWT-1-1-Exec-A | **1.1** exists as first **1.x** child under Phase 1 execution spine | Parent § Execution spine — 1.x children + [[workflow_state-execution]] frontmatter `current_subphase_index` (**`1.1`** post–**2026-04-09 18:05Z** deepen — sample-row table + § Wire-up pseudocode vs **1.2**/**1.2.1**; rollup cursor **`1.2`** / **`1.2.1`** history retained in **1.2** § Rollup completion) |
| GWT-1-1-Exec-B | Conceptual counterpart is explicit and read-only | Frontmatter `conceptual_counterpart` + § Scope |

## Related

- Parent spine: [[Phase-1-Execution-Vertical-Slice-Instrumentation-Spine-Roadmap-2026-04-08-2145]]
- [[roadmap-state-execution]]
- [[workflow_state-execution]]
- Policy: [[../decisions-log]]
