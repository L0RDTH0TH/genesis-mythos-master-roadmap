---
title: "CDR — Phase 3.2.3 UX / D-3.1.5 binding surfaces"
created: 2026-03-30
tags:
  - roadmap
  - conceptual-decision-record
  - genesis-mythos-master
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-3-2-3-UX-D3-1-5-Binding-Surfaces-Roadmap-2026-03-30-2319]]"
queue_entry_id: followup-deepen-phase3-323-gmm-20260402T235100Z
validation_status: pattern_only
status: active
---

# Conceptual decision record — Phase 3.2.3

## Chosen direction

Bind **operator-facing UX** to **ObservationChannel** records (**3.2.1**) enriched by **freshness_class** + **drift_class** (**3.2.2**) so **preview_shadow** vs **committed_session** is **legible in UI** without inventing a second bus (**3.1.1**) or mutating tick authority. **D-3.1.5-*** rows (**faction cohort lane vs shard**, **forge-sourced preview default**) receive **explicit NL binding surfaces** (labels, routing hints, disclosure strings) while remaining **execution-deferred** for wire formats and engine types.

## PMG alignment

Keeps **simulation vs rendering** separation from Phase 3 primary: renderers and forge surfaces **read** observation contracts and **admit** work through **3.1.5** / **3.1.2**, never silent kernel mutation.

## Alternatives considered

- **Defer all UX to execution track** — rejected for this slice: conceptual team needs **named binding surfaces** so **3.2** secondary rollup does not stay ambiguous on **D-3.1.5** loci.
- **Resolve D-3.1.5 fully here** — rejected: remains **execution-deferred** per [[decisions-log]]; this slice only **pins** where UX and cohort routing **meet** **ObservationChannel** + policy classes.

## Validation evidence

- **pattern_only:** No new Agent-Research synth; cross-links to **3.2.1**, **3.2.2**, **3.1.3**, **3.1.5**, and **decisions-log** **D-3.1.5-*** rows.

## Links

- Slice: [[Phase-3-2-3-UX-D3-1-5-Binding-Surfaces-Roadmap-2026-03-30-2319]]
- Parent secondary: [[Phase-3-2-Simulation-Rendering-Decoupling-and-Observation-Channels-Roadmap-2026-04-02-2300]]
