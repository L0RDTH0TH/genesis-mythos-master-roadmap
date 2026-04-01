---
title: CDR — Phase 2.6.3 consumer replay + cold-start + secondary 2.6 rollup closure
created: 2026-03-30
tags:
  - roadmap
  - conceptual-decision-record
  - genesis-mythos-master
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-2-6-3-Consumer-Replay-Cold-Start-and-Secondary-2-6-Rollup-Closure-Roadmap-2026-03-30-2109]]"
decision_kind: deepen
queue_entry_id: resume-deepen-gmm-263-followup-20260401T010800Z
master_goal: "[[Source-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# Summary

Chose **replay anchor + cold-start minimum + secondary 2.6 rollup closure** as the tertiary **2.6.3** slice so the **2.6** chain closes after **2.6.1** (bindings/citation) and **2.6.2** (session/escalation/forge drill-down), advancing the workflow cursor to **2.7** without claiming any `GMM-2.4.5-*` execution closure.

## PMG alignment

Binds post-audit consumer read paths to the forge collaboration story: operators and dialogue can **resume** and **cold-start** deterministically against the same audit surfaces defined upstream, preserving design authority on the conceptual track.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|-------------|--------|----------|------------------|
| Add **2.6.4–2.6.5** before closure | More granular replay UX | Delays Phase 2 spine progress; **2.6.2** already set forge drill-down defaults | **2.6.3** closes **2.6** chain per **2.6.2** downstream hint and operator guidance |
| Merge replay into **2.6.2** | Fewer files | Would overload session note; replay/cold-start is a distinct consumer contract | **2.6.3** keeps separation of concerns |
| Stop at **2.6.2** without closure row | Less writing | No explicit **2.6** rollup mirror of **2.5.5** pattern | Rollup closure improves traceability and MOC handoff |

## Validation evidence

- Pattern-only: extends **2.6.1**/**2.6.2** and **2.5.2** contracts already in-tree; no new external citations.

## Links

- Workflow anchor (last deepen row): `2026-04-01 01:07` — `Phase-2-6-2-...` / cursor advance to **2.6.3** (pre-this-run).
- Phase note: [[Phase-2-6-3-Consumer-Replay-Cold-Start-and-Secondary-2-6-Rollup-Closure-Roadmap-2026-03-30-2109]]
