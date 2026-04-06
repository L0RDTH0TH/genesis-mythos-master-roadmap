---
title: "CDR — Phase 6.1.3 remint (ObservationChannel readout / 4.1.3 co-display, sandbox)"
created: 2026-04-07
tags:
  - roadmap
  - conceptual-decision-record
  - sandbox-genesis-mythos-master
para-type: Project
project-id: sandbox-genesis-mythos-master
parent_roadmap_note: "[[Phase-6-1-3-ObservationChannel-Lane-Readout-and-Presentation-Time-Co-Display-Roadmap-2026-04-07-1015]]"
decision_kind: deepen
queue_entry_id: pool-remint-613-sandbox-gmm-20260406120002Z
master_goal: "[[Source-sandbox-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

## Summary

Operator-scoped **out-of-order** remint of tertiary **6.1.3** on the **active** post-rollback tree (`pool-remint-613-sandbox-gmm-20260406120002Z`), carrying forward the **ObservationChannel → PresentationEnvelope** readout catalog + matrix from the branch reference note without overwriting frozen archive bodies.

## PMG alignment

Keeps **Horizon-Q3** vertical-slice **operator readout** composable from upstream **3.2.1** / **4.1.3** truth only, preserving **GWT-6-C** delegation evidence for the **InstrumentationIntent** bundle narrative on **6.1**.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| --- | --- | --- | --- |
| Wait for active **6.1.1** mint first | Strict sibling order | Blocks **6.1.3** readout design while **6.1.2** + manifest pins are already live | Operator explicitly queued **6.1.3** remint after **6.1.2** (same pattern as **612**) |
| Edit branch/archive **6.1.3** in place | Single file | Violates frozen conceptual subtree + dual-track guardrails | **New** active-tree file; branch remains audit-only |

## Validation evidence

- Pattern-only: parity check against [[Branches/phase-6-operator-rollback-20260405/Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle/Phase-6-1-3-ObservationChannel-Lane-Readout-and-Presentation-Time-Co-Display-Roadmap-2026-04-06-2130]] (pre-rollback); wikilinks retargeted to active **6.1** / **6.1.2** basenames.

## Links

- **Workflow anchor:** [[workflow_state]] ## Log **2026-04-07 10:15** — Target **Phase-6-1-3** remint (`pool-remint-613-sandbox-gmm-20260406120002Z`).
- **Parent run:** `eat-sandbox-20260406T000002Z-613`
