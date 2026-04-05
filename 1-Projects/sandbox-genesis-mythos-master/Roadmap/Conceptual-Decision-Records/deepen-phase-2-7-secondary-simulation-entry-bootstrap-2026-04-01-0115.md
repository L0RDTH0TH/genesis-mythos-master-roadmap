---
title: "CDR — Phase 2.7 secondary simulation-entry bootstrap"
created: 2026-04-01
tags:
  - roadmap
  - conceptual-decision-record
  - sandbox-genesis-mythos-master
para-type: Project
project-id: sandbox-genesis-mythos-master
parent_roadmap_note: "[[Phase-2-7-Simulation-Entry-Bootstrap-and-Deterministic-First-Tick-Roadmap-2026-04-01-0115]]"
decision_kind: deepen
queue_entry_id: resume-deepen-gmm-27-mint-followup-20260401T011500Z
master_goal: "[[Source-sandbox-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# CDR — Phase 2.7 secondary simulation-entry bootstrap

## Summary

Minted **secondary 2.7** as **simulation-entry bootstrap + deterministic first-tick contract**, bridging **2.6.3** replay anchor / cold-start into a named **SimulationEntryBootstrap** admission step before the first simulation tick, without re-deriving **2.4** branch semantics.

## PMG alignment

Advances the forge toward a **playable** world loop by stating how committed state **enters** simulation deterministically after audit/replay surfaces close — matching the master goal’s staged pipeline + safe commit boundary.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|-------------|--------|----------|----------------|
| Merge 2.7 into Phase 3 primary only | Fewer Phase 2 notes | Loses explicit **2.6 → sim** handoff traceability | Phase 2 still owns worldgen→sim boundary in this vault’s spine |
| Specify full subsystem pseudo-code at secondary | Faster execution handoff | Violates conceptual secondary depth; execution-deferred | Kept NL-only at **2.7**; tertiaries carry depth |

## Validation evidence

- Pattern-only continuity from [[Phase-2-6-3-Consumer-Replay-Cold-Start-and-Secondary-2-6-Rollup-Closure-Roadmap-2026-03-30-2109]] and [[Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-03-30-0430]]; no external research notes for this mint.

## Links

- Parent: [[Phase-2-7-Simulation-Entry-Bootstrap-and-Deterministic-First-Tick-Roadmap-2026-04-01-0115]]
- Workflow anchor: `2026-04-01 01:16 | deepen | Phase-2-7-Simulation-Entry-Bootstrap-and-Deterministic-First-Tick | queue_entry_id: resume-deepen-gmm-27-mint-followup-20260401T011500Z`
