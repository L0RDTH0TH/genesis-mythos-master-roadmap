---
title: "CDR — Phase 6.1.1 manifest admission row IDs ↔ admission ticket vocabulary"
created: 2026-04-05
tags:
  - roadmap
  - conceptual-decision-record
  - sandbox-genesis-mythos-master
para-type: Project
project-id: sandbox-genesis-mythos-master
parent_roadmap_note: "[[Phase-6-1-1-Manifest-Admission-Row-Bindings-and-Admission-Ticket-Vocabulary-Roadmap-2026-04-05-1918]]"
decision_kind: deepen
queue_entry_id: followup-deepen-phase611-mint-sandbox-gmm-20260405T191800Z
master_goal: "[[Source-sandbox-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: cited
related_research: []
---

# Summary

Minted **Phase 6 tertiary 6.1.1** with a stable **`manifest_admission_row_id`** catalog and NL binding table to **2.7.x** `admission_ticket_id`, **SimulationEntryBootstrap**, and **FirstCommittedTickTrace**, satisfying **GWT-6-A** via narrowed **GWT-6.1.1-A–K** rows and wiring parent **6.1** manifest **Admission** + delegation table.

# PMG alignment

Keeps the **Q3 vertical slice** manifest honest: every admission-facing manifest row has an explicit ticket/trace vocabulary binding so execution-track tooling and compare tables can cite stable IDs without re-deriving names from prose.

# Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| --- | --- | --- | --- |
| Encode bindings only in **6.1** secondary body | One file | Tertiary depth-3 pattern broken; **6.1** already wide | Operator queue scoped **6.1.1** mint |
| Reuse **5.1.1** seam admission vocabulary verbatim | Less new text | Blurs ruleset seam vs simulation-entry admission | Chose **2.7.x**-native vocabulary per **GWT-6-A** |

# Validation evidence

- Parent secondary: [[Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-05-1615]] § Admission + **GWT-6 → 6.1** row **GWT-6-A**.
- Upstream tickets: [[Phase-2-7-3-Shadow-to-Live-Parity-Admission-Ticket-Redemption-and-First-Committed-Tick-Trace-Roadmap-2026-03-30-1800]], [[Phase-2-7-1-Simulation-Entry-Bootstrap-and-Deterministic-First-Tick-Contract-Roadmap-2026-04-01-0116]].

# Links

- Parent roadmap: [[Phase-6-1-1-Manifest-Admission-Row-Bindings-and-Admission-Ticket-Vocabulary-Roadmap-2026-04-05-1918]]
- Workflow anchor: [[workflow_state]] — deepen **2026-04-05 19:18Z** row, `queue_entry_id: followup-deepen-phase611-mint-sandbox-gmm-20260405T191800Z`
