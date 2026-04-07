---
title: Phase 1.2 (Execution) — PresentationEnvelope stub
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
subphase-index: "1.2"
conceptual_counterpart: "[[../../../Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle/Phase-6-1-3-ObservationChannel-Lane-Readout-and-Presentation-Time-Co-Display-Roadmap-2026-04-07-1015]]"
status: complete
progress: 100
handoff_readiness: 86
---

# Phase 1.2 (Execution) — PresentationEnvelope stub

Second **execution-local** secondary (**`1.2`**) under Phase 1 spine, per [[../../../decisions-log]] **D-Exec-1-numbering-policy** — defines the **stub contract** for **PresentationEnvelope** readout that consumes **ObservationChannel** sample rows from [[Phase-1-1-ObservationChannel-Stub-Binding-Roadmap-2026-04-06-2245]], aligned with parent happy path in [[Phase-1-Execution-Vertical-Slice-Instrumentation-Spine-Roadmap-2026-04-08-2145]].

## Scope

- **In scope:** **PresentationEnvelope stub** — operator-visible **readout row** shape (labels, correlation to `tick_commit_id` / `sample_label`, lane framing) that maps **one** ObservationChannel sample to a **single** presentation line — **checklist + acceptance**, no host binary or CI.
- **Out of scope:** Real rendering engine, persistence proofs, registry materialization (`GMM-2.4.5-*`), compare tables — **execution-deferred** with same deferral language as **1.1** and parent.

## NL checklist (1.2)

- [x] Name the **conceptual import** (6.1.3 presentation-time co-display) and keep it a **wikilink** only — no overwrite of frozen conceptual bodies.
- [x] **Readout row schema (stub):** minimum fields documented below (execution-deferred: no binary / CI).
- [x] State **one** acceptance line: “Operator can trace from **1.2** readout stub to **1.1** sample row and to parent happy path without contradiction.”
- [x] **Stub binding (pseudocode):** fenced mapping from **1.1** sample shape → **1.2** readout row (implementation-shaped, host-deferred).

### Readout row schema (stub fields)

| Field | Role |
| --- | --- |
| `presentation_tick_ref` | Correlates to `tick_commit_id` from **1.1** sample |
| `lane_framing` | Mirrors `channel_lane` / operator-visible lane label |
| `readout_text` | Single-line operator-visible summary (stub string) |
| `source_sample_ref` | Pointer to **1.1** `sample_label` + `envelope_ref` |
| `co_display_note` | Explicit “presentation-time only” disclaimer (not PreCommit) |
| *(projection)* | `observed_at_tick` is **not** a separate `PresentationReadoutRow` column; it is **embedded in `readout_text`** per § Stub binding (matches **1.1** sample field parity). |

## Stub binding (pseudocode)

Execution-local **stub only** — **`ObservationChannelSample` field-for-field matches** [[Phase-1-1-ObservationChannel-Stub-Binding-Roadmap-2026-04-06-2245]] § Sample row schema; no host binary, no persistence.

```pseudo
// Byte-aligned with 1.1 stub table (five columns).
type ObservationChannelSample = {
  tick_commit_id: string
  channel_lane: string
  sample_label: string
  envelope_ref: string
  observed_at_tick: number
}

// 1.2-only boundary flag — NOT a duplicate 1.1 column; co-display path guard at PresentationEnvelope.
type PresentationCoDisplayGate = { presentation_time_only: bool }

type PresentationReadoutRow = {
  presentation_tick_ref: string  // := sample.tick_commit_id
  lane_framing: string           // := sample.channel_lane
  readout_text: string           // operator-visible one-liner (stub)
  source_sample_ref: string      // := sample.sample_label + "|" + sample.envelope_ref
  co_display_note: string        // := "presentation-time only; not PreCommit"
}

function stubMapSampleToReadout(s: ObservationChannelSample, g: PresentationCoDisplayGate): PresentationReadoutRow
  precondition: g.presentation_time_only == true
  // Stub traceability: observed_at_tick is surfaced inside readout_text (operator-visible) and correlates with tick_commit_id via presentation_tick_ref — not dropped; no separate column by design (§ Field parity).
  return {
    presentation_tick_ref: s.tick_commit_id,
    lane_framing: s.channel_lane,
    readout_text: "[stub] lane=" + s.channel_lane + " label=" + s.sample_label + " @tick=" + string(s.observed_at_tick),
    source_sample_ref: s.sample_label + "|" + s.envelope_ref,
    co_display_note: "presentation-time only; not PreCommit"
  }
```

### Field parity: 1.1 sample row ↔ 1.2 `ObservationChannelSample`

| 1.1 field | In `ObservationChannelSample` | Match |
| --- | --- | --- |
| `tick_commit_id` | `tick_commit_id` | ✓ |
| `channel_lane` | `channel_lane` | ✓ |
| `sample_label` | `sample_label` | ✓ |
| `envelope_ref` | `envelope_ref` | ✓ |
| `observed_at_tick` | `observed_at_tick` | ✓ |

**Handoff evidence (2026-04-09):** Stub binding + § Field parity vs **1.1** are complete; `handoff_readiness` **86** with residual execution-deferred risks in § Risk register (v0). **1.2.1** tertiary minted — [[Phase-1-2-1-PresentationEnvelope-Tertiary-Readout-Detail-Roadmap-2026-04-09-1521]] (drill rows + co-display guard drills).

## Tertiary children (1.2.x)

- [[Phase-1-2-1-PresentationEnvelope-Tertiary-Readout-Detail-Roadmap-2026-04-09-1521]] — **1.2.1** readout edge / co-display drills (mid-technical; **D-Exec-1**).

## Risk register (v0)

| Risk | Mitigation (stub) |
| --- | --- |
| Schema drift vs **1.1** after future edits | Gate merges on § Field parity table; re-run validator on any **1.x** sample shape change. |
| Misuse of **1.2** readout as PreCommit evidence | `co_display_note` + `PresentationCoDisplayGate` precondition; parent spine defers registry/CI. |
| Lane framing over-claims authority | `lane_framing` mirrors **1.1** `channel_lane` only; no new lane ids introduced in **1.2**. |
| `observed_at_tick` projection | **Testable stub rule:** happy-path `readout_text` **must** include `string(s.observed_at_tick)` (see § Stub binding); negative `drillReadout` path returns `{ blocked: true, ... }` — no `PresentationReadoutRow`. |

## GWT-1-2-Exec (local)

| ID | Claim | Evidence hook |
| --- | --- | --- |
| GWT-1-2-Exec-A | **1.2** exists as second **1.x** child under Phase 1 execution spine | Parent § Execution spine — 1.x children + [[workflow_state-execution]] + § Stub binding (pseudocode) + § Tertiary children (**[[Phase-1-2-1-PresentationEnvelope-Tertiary-Readout-Detail-Roadmap-2026-04-09-1521]]** on disk). **Rollup (2026-04-09):** spine links + **1.2.1** mint + § Rollup completion below. |
| GWT-1-2-Exec-B | **PresentationEnvelope** stub is explicitly **downstream of ObservationChannel** stub | § Readout row schema + wikilink to **1.1** + **1.2.1** § Drill rows proving `stubMapSampleToReadout` / `drillReadout` consume the same types as § Stub binding |
| GWT-1-2-Exec-C | Conceptual counterpart is explicit and read-only | Frontmatter `conceptual_counterpart` + § Scope |

## Rollup completion (secondary 1.2 — execution)

- **NL checklist (1.2):** All rows in § NL checklist (1.2) remain satisfied; **1.2.1** provides drill-backed evidence for readout edge cases (happy + blocked) aligned with § Stub binding pseudocode.
- **GWT parity vs 1.2.1:** **GWT-1-2-Exec-A** cites **1.2.1** on-disk + spine; **GWT-1-2-Exec-B** cites **1.2.1** § Drill rows + § Drill pseudocode ↔ parent `stubMapSampleToReadout`; **GWT-1-2-Exec-C** unchanged.
- **Execution track:** Roll-up narrative here is **authoritative for secondary 1.2**; registry/CI/host closure remains **execution-deferred** per parent spine — not framed as an open **1.2** gate blocking this secondary’s rollup language.

### Automation / machine-read contract (secondary 1.2)

- **`status: complete` + `progress: 100`** on **this** note = **secondary 1.2 rollup closed** for execution handoff automation.
- **Phase 1** execution spine / [[roadmap-state-execution]] may still show **Phase 1: in-progress** until later secondaries or operator sign-off — that does **not** reopen **1.2** unless a new queue entry says so.
- **`[[workflow_state-execution]]` `current_subphase_index: "1.1"`** after ## Log **2026-04-09 16:10** = **next deepen scope** (1.1 polish), not an unfinished **1.2** gate.

## Related

- Parent spine: [[Phase-1-Execution-Vertical-Slice-Instrumentation-Spine-Roadmap-2026-04-08-2145]]
- Upstream stub: [[Phase-1-1-ObservationChannel-Stub-Binding-Roadmap-2026-04-06-2245]]
- [[roadmap-state-execution]]
- [[workflow_state-execution]]
- Policy: [[../../../decisions-log]]
