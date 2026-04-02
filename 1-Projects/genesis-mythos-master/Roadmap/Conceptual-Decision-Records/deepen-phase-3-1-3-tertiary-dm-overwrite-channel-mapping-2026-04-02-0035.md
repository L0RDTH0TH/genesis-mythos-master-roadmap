---
title: "CDR — Phase 3.1.3 sim-visible classification + DM overwrite channel mapping"
created: 2026-04-02
tags:
  - roadmap
  - conceptual-decision-record
  - genesis-mythos-master
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-3-1-3-Sim-Visible-Classification-and-DM-Overwrite-Channel-Mapping-Roadmap-2026-04-02-0035]]"
decision_kind: deepen
queue_entry_id: resume-deepen-phase3-313-followup-gmm-20260402T003000Z
master_goal: "[[Source-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# Decision record — Phase 3.1.3 (deepen)

## Summary

Minted tertiary **3.1.3** defining a **closed sim-visible classification vocabulary** for bus/observation facts and a **DM overwrite channel → merge-compatibility** map so **3.1.2** queue/defer/merge closure and **3.1.1** lane ordering stay coherent when DM or tools inject **live tweak** vs **structural regen** class work. Acceptance extended with **GWT J–L** (filterability, DM channel matrix, preview non-authoritative).

## PMG alignment

Supports the master goal’s **living simulation** + **DM overwrite** story without leaking execution APIs: operators and downstream consumers can **filter** authoritative vs preview vs replay-only streams **before** persistence and agency slices (**3.1.4+**).

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| --- | --- | --- | --- |
| Single **overwrite** bit only | Minimal vocabulary | Loses preview vs replay vs DM-class distinctions | Insufficient for Phase 3 primary decoupling |
| Per-subsystem classification taxonomies | Fine-grained | Fragmented filters across slices | Closed vocabulary at **3.1.3** first; extend later if needed |

## Validation evidence

- **pattern_only:** No `Ingest/Agent-Research/` synthesis; continuity from **3.1**, **3.1.1**, **3.1.2**, Phase 3 primary, and **2.7.3** trace handoff (NL).

## Links

- Parent roadmap note: [[Phase-3-1-3-Sim-Visible-Classification-and-DM-Overwrite-Channel-Mapping-Roadmap-2026-04-02-0035]]
- Workflow anchor: `2026-04-02 00:35` — Target `Phase-3-1-3-Sim-Visible-Classification-and-DM-Overwrite-Channel-Mapping` — `queue_entry_id: resume-deepen-phase3-313-followup-gmm-20260402T003000Z`
