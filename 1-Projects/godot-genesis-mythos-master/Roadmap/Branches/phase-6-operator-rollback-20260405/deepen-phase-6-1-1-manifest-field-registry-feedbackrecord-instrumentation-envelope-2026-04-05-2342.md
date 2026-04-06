---
title: "CDR — Phase 6.1.1 manifest registry + FeedbackRecord taxonomy + instrumentation envelope"
created: 2026-04-05
tags:
  - roadmap
  - conceptual-decision-record
  - godot-genesis-mythos-master
para-type: Project
project-id: godot-genesis-mythos-master
parent_roadmap_note: "[[Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-05-1510]]"
decision_kind: deepen
queue_entry_id: followup-deepen-phase611-mint-first-tertiary-godot-gmm-20260405T224800Z
master_goal: "[[Source-godot-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# CDR — Phase 6.1.1 manifest registry + FeedbackRecord taxonomy + instrumentation envelope

## Summary

Minted tertiary **6.1.1** with three NL contracts: **VerticalSliceManifest field registry**, **FeedbackRecord taxonomy** (slice-local routing without upstream overwrite), and **InstrumentationIntentEnvelope** rows binding **II-6.1-*** to a single comparable envelope shape — closing secondary **6.1** open questions at conceptual depth.

## PMG alignment

Makes **Horizon-Q3** iteration **legible** to operators: manifest columns, feedback classification, and instrumentation intents share explicit NL structure before execution adds wires, profilers, or dashboards.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| --- | --- | --- | --- |
| **Three separate tertiaries** | Smaller notes | Extra queue churn; user scoped one **6.1.1** deepen | Single note per queue contract |
| **Free-text FeedbackRecord only** | Faster to write | Fails **GWT-6.1-H** traceability | Named **record_kind** rows |
| **Per-subsystem instrumentation cards now** | Earlier packaging | Violates conceptual “single envelope” deferral on secondary | One envelope shape; execution splits later |

## Validation evidence

- Pattern-only: follows **5.1.1** / **5.2.1** tertiary patterns (registry tables + GWT narrowing).
- Links: [[Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-05-1510]], [[workflow_state]], [[decisions-log]].

## Links

- **Parent secondary:** [[Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-05-1510]]
- **Tertiary minted:** [[Phase-6-1-1-Manifest-Field-Registry-FeedbackRecord-Taxonomy-and-Instrumentation-Envelope-Roadmap-2026-04-05-2342]]
- **Workflow anchor:** [[workflow_state]] — deepen row **2026-04-05 23:42** (`queue_entry_id: followup-deepen-phase611-mint-first-tertiary-godot-gmm-20260405T224800Z`)
- **Queue:** `followup-deepen-phase611-mint-first-tertiary-godot-gmm-20260405T224800Z`
