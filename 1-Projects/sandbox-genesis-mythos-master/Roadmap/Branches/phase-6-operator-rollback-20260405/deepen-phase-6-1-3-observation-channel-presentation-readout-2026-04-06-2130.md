---
title: "CDR — deepen Phase 6.1.3 ObservationChannel readout + 4.1.3 presentation-time co-display"
created: 2026-04-06
tags:
  - conceptual-decision-record
  - roadmap
  - sandbox-genesis-mythos-master
project-id: sandbox-genesis-mythos-master
parent_roadmap_note: "[[Phase-6-1-3-ObservationChannel-Lane-Readout-and-Presentation-Time-Co-Display-Roadmap-2026-04-06-2130]]"
queue_entry_id: followup-deepen-phase613-sandbox-gmm-20260406T213000Z
validation_status: pattern_only
---

# CDR — Phase 6.1.3 deepen (ObservationChannel + presentation-time co-display)

## Decision

Minted tertiary **6.1.3** implementing **GWT-6-C** delegation: **`slice_operator_readout_id`** catalog joined to **`slice_tick_window_scenario_id`** (**6.1.2**) plus **3.2.1** / **4.1.3** read-only anchors; **channel → PresentationEnvelope** matrix with explicit heading anchors for audit grep.

## Alternatives considered

- **Fold into 6.1.2:** Rejected — tick-window + sim-visible matrix stays narrow; operator readout + presentation envelope binding deserves its own GWT table (**GWT-6.1.3-***).
- **Defer until secondary 6.1 rollup:** Rejected — rollup requires **6.1.1–6.1.3** chain complete per manifest delegation table.

## Validation / evidence

- **GWT-6.1.3-A–K** table on slice note; `handoff_readiness` **88** (pattern_only — vault continuity only).
- Queue: `followup-deepen-phase613-sandbox-gmm-20260406T213000Z` \| `parent_run_id: eat-queue-sandbox-2026-04-05T1345Z` \| `queue_lane: sandbox`.

## Links

- Slice: [[Phase-6-1-3-ObservationChannel-Lane-Readout-and-Presentation-Time-Co-Display-Roadmap-2026-04-06-2130]]
- Secondary: [[Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-05-1615]]
- Prior tertiary: [[Phase-6-1-2-Bounded-Tick-Window-Scenarios-and-Sim-Visible-Classification-Matrix-Roadmap-2026-04-06-0800]]
