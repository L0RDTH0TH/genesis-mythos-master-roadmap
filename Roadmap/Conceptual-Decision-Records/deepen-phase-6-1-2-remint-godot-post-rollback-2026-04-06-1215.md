---
title: "CDR — Phase 6.1.2 remint (bounded tick scenarios + sim-visible matrix, godot)"
created: 2026-04-06
tags:
  - roadmap
  - conceptual-decision-record
  - godot-genesis-mythos-master
para-type: Project
project-id: godot-genesis-mythos-master
parent_roadmap_note: "[[Phase-6-1-2-Bounded-Tick-Window-Scenarios-and-Sim-Visible-Classification-Matrix-Roadmap-2026-04-06-1215]]"
decision_kind: deepen
queue_entry_id: pool-remint-612-godot-gmm-20260406120001Z
master_goal: "[[Source-godot-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# Conceptual decision record — Phase 6.1.2 remint (godot)

## Summary

Re-minted tertiary **6.1.2** on the **active** post-rollback tree under [[Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-06-1200]], carrying forward **`mar.*`** join keys from the **archived branch 6.1.1** catalog until active **6.1.1** exists, per operator queue `pool-remint-612-godot-gmm-20260406120001Z`.

## PMG alignment

Keeps **Horizon-Q3** slice stories traceable to Phase **3** bus/checkpoint notes without duplicating sim semantics, supporting the PMG’s prototype-assembly and instrumentation narrative for the godot vertical slice.

## Alternatives and tradeoffs

| Alternative | Upside | Downide | Why not chosen |
| --- | --- | --- | --- |
| Mint **6.1.1** before **6.1.2** | Clean `mar.*` authority on active tree | Delays operator-scoped **6.1.2** remint | Queue explicitly targeted **6.1.2** remint first |
| Rewrite **`mar.*`** in this note without branch cite | Avoids archive wikilinks | Risks ID drift vs prior catalog | Rejected — stability over cosmetic purity |

## Validation evidence

- Pattern-only: branch catalog [[Branches/phase-6-operator-rollback-20260405/Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle/Phase-6-1-1-Manifest-Admission-Row-Bindings-and-Admission-Ticket-Vocabulary-Roadmap-2026-04-05-1918]] for `mar.*` IDs; active **6.1.1** pending.

## Links

- [[workflow_state]] ## Log **2026-04-07 09:15** (terminal row for this decision — post `pool-remint-611` remint)
- Parent: [[Phase-6-1-2-Bounded-Tick-Window-Scenarios-and-Sim-Visible-Classification-Matrix-Roadmap-2026-04-06-1215]]
