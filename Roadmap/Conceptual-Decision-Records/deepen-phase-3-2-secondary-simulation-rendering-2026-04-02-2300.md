---
title: "CDR — Phase 3.2 secondary — simulation/rendering decoupling + observation channels"
created: 2026-04-02
tags:
  - conceptual-decision-record
  - sandbox-genesis-mythos-master
  - phase-3
para-type: Project
project-id: sandbox-genesis-mythos-master
parent_roadmap_note: "[[Phase-3-2-Simulation-Rendering-Decoupling-and-Observation-Channels-Roadmap-2026-04-02-2300]]"
decision_kind: deepen
queue_entry_id: followup-deepen-phase3-32-gmm-20260402T230000Z
master_goal: "[[Source-sandbox-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# CDR — Phase 3.2 secondary (simulation / rendering decoupling)

## Summary

Minted **Phase 3 secondary 3.2** as **simulation vs rendering decoupling + observation channels**, positioning **preview vs committed session** boundaries after the **3.1.1–3.1.5** sim-tick spine. **D-3.1.5-*** deferrals are **re-affirmed** as binding on **3.2+** tertiaries, not closed here.

## PMG alignment

Advances the **living simulation** master goal by separating **authoritative tick/kernel** behavior (3.1) from **read-only observation + preview UX**, preserving **deterministic replay** narrative and **DM overwrite class** discipline without expanding execution artifacts.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| --- | --- | --- | --- |
| Make **3.2** about **persistence replication** only | Narrow, implementation-shaped | Overlaps **3.1.4** checkpoint story | Would fragment checkpoint authority; observation/preview is the natural next spine after **3.1** |
| Fold **3.2** into **primary** patch | Fewer files | Violates structural roadmap discipline | Primary already checklist-complete; secondaries carry bodies |

## Validation evidence

- **Pattern-only:** NL contracts consistent with Phase 3 primary + **3.1** chain; no new external research synth this run.

## Links

- Roadmap: [[Phase-3-2-Simulation-Rendering-Decoupling-and-Observation-Channels-Roadmap-2026-04-02-2300]]
- Workflow anchor: `2026-04-02 23:00` — Target `Phase-3-2-Simulation-Rendering-Decoupling-and-Observation-Channels` — queue `followup-deepen-phase3-32-gmm-20260402T230000Z`
