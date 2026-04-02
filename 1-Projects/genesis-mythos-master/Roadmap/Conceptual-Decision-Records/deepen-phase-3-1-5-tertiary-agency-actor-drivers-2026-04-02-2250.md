---
title: "CDR — deepen Phase 3.1.5 agency, actor drivers, and intent scheduling"
created: 2026-04-02
tags:
  - roadmap
  - conceptual-decision-record
  - genesis-mythos-master
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-3-1-5-Agency-Actor-Drivers-and-Intent-Scheduling-Roadmap-2026-04-02-2250]]"
decision_kind: deepen
queue_entry_id: followup-deepen-phase3-315-gmm-20260402T224500Z
master_goal: "[[Source-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# Decision record — Phase 3.1.5 agency, actor drivers, and intent scheduling

## Summary

Minted tertiary **3.1.5** to bind **actor lanes** and **agency drivers** to **WorkItem** admission into tick `T`, consuming **2.2.x** resolver outputs as logical upstream while delegating **merge closure** to **3.1.2**, **bus ordering** to **3.1.1**, **classification** to **3.1.3**, and **durability** to **3.1.4**. Positions **3.1** tertiary chain **3.1.1–3.1.5** as structurally complete; next deepen targets **3.2** (new secondary).

## PMG alignment

Advances the Phase 3 goal of **living simulation** by naming **who schedules what into a tick** and how that interacts with **DM overwrite** and **persistence** stories—without execution APIs.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| --- | --- | --- | --- |
| **Single undifferentiated “actor”** | Simpler prose | Cannot express DM vs system vs operator precedence | Breaks **3.1.2** merge story + **3.1.3** DM classes |
| **Embed full 2.4 commit tables here** | Local completeness | Re-derives execution orchestration | Violates Phase 3 layering; **2.4** stays reference-only via lineage |

## Validation evidence

- Pattern-only: continuity from **2.2.x**, **3.1.1–3.1.4**; no new `Ingest/Agent-Research/` synthesis notes this run.

## Links

- Roadmap note: [[Phase-3-1-5-Agency-Actor-Drivers-and-Intent-Scheduling-Roadmap-2026-04-02-2250]]
- Workflow anchor: `2026-04-02 22:45` deepen / `followup-deepen-phase3-315-gmm-20260402T224500Z`
