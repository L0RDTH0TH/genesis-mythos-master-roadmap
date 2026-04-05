---
title: "CDR — deepen Phase 6.1.2 bounded tick window + sim-visible matrix"
created: 2026-04-06
tags:
  - conceptual-decision-record
  - roadmap
  - sandbox-genesis-mythos-master
project-id: sandbox-genesis-mythos-master
parent_roadmap_note: "[[Phase-6-1-2-Bounded-Tick-Window-Scenarios-and-Sim-Visible-Classification-Matrix-Roadmap-2026-04-06-0800]]"
---

# CDR — Phase 6.1.2 deepen (bounded tick scenarios + sim-visible matrix)

## Decision

Minted tertiary **6.1.2** implementing **GWT-6-B** delegation: **`slice_tick_window_scenario_id`** catalog joined to **`manifest_admission_row_id`** (**6.1.1**) plus **3.1.2** / **3.1.3** / **3.1.4** read-only anchors; **sim-visible × checkpoint** matrix with explicit heading anchors for audit grep.

## Alternatives considered

- **Fold into 6.1.1:** Rejected — admission vocabulary slice stays narrow; tick window + classification binding deserves its own GWT table.
- **Defer until secondary 6.1 rollup:** Rejected — rollup remains deferred until **6.1.x** chain advances per conceptual policy; **6.1.2** is required structural mint before rollup closure.

## Validation / evidence

- **GWT-6.1.2-A–K** table on slice note; `handoff_readiness` **87**.
- Queue: `followup-deepen-phase612-sandbox-gmm-20260406T004500Z` \| `parent_run_id: l1-sandbox-eatq-20260406T150000Z` \| `queue_lane: sandbox`.

## Links

- Slice: [[Phase-6-1-2-Bounded-Tick-Window-Scenarios-and-Sim-Visible-Classification-Matrix-Roadmap-2026-04-06-0800]]
- Secondary: [[Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-05-1615]]
- Prior tertiary: [[Phase-6-1-1-Manifest-Admission-Row-Bindings-and-Admission-Ticket-Vocabulary-Roadmap-2026-04-05-1918]]
