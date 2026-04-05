---
title: "CDR — Phase 6 primary rollup (NL + GWT-6 vs rolled-up 6.1)"
created: 2026-04-06
tags:
  - roadmap
  - conceptual-decision-record
  - sandbox-genesis-mythos-master
para-type: Project
project-id: sandbox-genesis-mythos-master
parent_roadmap_note: "[[Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-03-30-0430]]"
decision_kind: deepen
queue_entry_id: followup-deepen-phase6-primary-rollup-sandbox-gmm-20260406T230000Z
master_goal: "[[Source-sandbox-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

## Summary

Closed **Phase 6 primary rollup** on the primary roadmap note: **NL checklist** reaffirmed and **GWT-6-A–K** **Evidence** columns explicitly bound to the **rolled-up secondary 6.1** story (**GWT-6.1-A–K** vs **6.1.1–6.1.3**) and rollup CDR [[Conceptual-Decision-Records/deepen-phase-6-1-secondary-rollup-nl-gwt-2026-04-06-2145]], with **`phase6_primary_rollup_nl_gwt: complete`** and `handoff_readiness` **86**. **Ctx/token preflight** logged in [[workflow_state]] **## Log** (staged rollup, optional RECAL, tighter `token_cap` on future rows, fresh chat at ceiling).

## PMG alignment

Locks the **Horizon-Q3** vertical-slice design authority for **sandbox-genesis-mythos-master**: one end-to-end NL path **2.7 → 3 → 4 → 5** with **InstrumentationIntent** + **FeedbackRecord** routing, without claiming execution benchmarks or CI closure (**execution-deferred**).

## Alternatives and tradeoffs

| Alternative | Upside | Downide | Why not chosen |
| --- | --- | --- | --- |
| **RECAL-ROAD before rollup** | Hygiene sweep at high ctx | Delays primary rollup closure | Rollup is NL/evidence sync; **optional** RECAL if Layer 1 surfaces stale surfaces |
| **Split primary rollup across two queue rows** | Lower per-run tokens | More operator overhead | Single row with **scoped** edits + logged **token_cap** guidance for follow-ups |
| **Mint secondary 6.2 before primary rollup** | More structure first | Violates resolver **structural-phase6-primary-rollup-pending** | Resolver + queue locked **deepen** on **primary rollup** first |

## Validation evidence

- [[Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-03-30-0430]] — primary **GWT-6** table + rollup closure callout
- [[Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-05-1615]] — secondary rollup + **GWT-6 → 6.1** delegation **closed**
- [[Conceptual-Decision-Records/deepen-phase-6-1-secondary-rollup-nl-gwt-2026-04-06-2145]] — secondary rollup CDR
- Tertiary chain: [[Phase-6-1-1-Manifest-Admission-Row-Bindings-and-Admission-Ticket-Vocabulary-Roadmap-2026-04-05-1918]], [[Phase-6-1-2-Bounded-Tick-Window-Scenarios-and-Sim-Visible-Classification-Matrix-Roadmap-2026-04-06-0800]], [[Phase-6-1-3-ObservationChannel-Lane-Readout-and-Presentation-Time-Co-Display-Roadmap-2026-04-06-2130]]

## Links

- **Workflow anchor:** [[workflow_state]] **## Log** — Timestamp **2026-04-06 23:00** (`monotonic_log_timestamp` strictly after **2026-04-06 22:45**; handoff `telemetry_utc: 2026-04-06T16:05:00.000Z`) — Phase 6 primary rollup deepen (`followup-deepen-phase6-primary-rollup-sandbox-gmm-20260406T230000Z`)
