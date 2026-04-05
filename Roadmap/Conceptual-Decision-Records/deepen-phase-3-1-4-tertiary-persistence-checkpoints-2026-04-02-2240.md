---
title: "CDR — deepen Phase 3.1.4 persistence checkpoint boundaries"
created: 2026-04-02
tags:
  - roadmap
  - conceptual-decision-record
  - sandbox-genesis-mythos-master
para-type: Project
project-id: sandbox-genesis-mythos-master
parent_roadmap_note: "[[Phase-3-1-4-Persistence-Checkpoint-Boundaries-Roadmap-2026-04-02-2240]]"
decision_kind: deepen
queue_entry_id: followup-deepen-phase3-314-gmm-20260402T224000Z
master_goal: "[[Source-sandbox-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# Decision record — Phase 3.1.4 persistence checkpoint boundaries

## Summary

Minted tertiary **3.1.4** to bind **persistence checkpoints** to **tick closure** and **bus/event ordering**, with explicit **non-durability** rules for **preview_shadow** / **replay_only** classifications from **3.1.3**. Checkpoint emission stays **after** **3.1.2** merge closure and compatible with **3.1.1** lane ordering story.

## PMG alignment

Supports the Phase 3 master goal of a **tick-based living simulation** with **clear durability boundaries** vs **observation/preview**, without smuggling execution storage formats into conceptual authority.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| --- | --- | --- | --- |
| **Checkpoint only at phase boundaries** | Simpler narrative | Breaks per-tick sim closure story | Conflicts with **3.1** tick monotonicity + **3.1.2** closure |
| **Durability co-emitted with every SimEvent** | Max trace granularity | Floods conceptual contract; ordering story becomes ambiguous | **3.1.1** ordering + **3.1.2** closure must gate durability |

## Validation evidence

- Pattern-only: extends **3.1.1–3.1.3** + **2.7.3** continuity; no new `Ingest/Agent-Research/` synthesis notes this run.

## Links

- Roadmap note: [[Phase-3-1-4-Persistence-Checkpoint-Boundaries-Roadmap-2026-04-02-2240]]
- Workflow anchor: `2026-04-02 22:40` deepen / `followup-deepen-phase3-314-gmm-20260402T224000Z`
