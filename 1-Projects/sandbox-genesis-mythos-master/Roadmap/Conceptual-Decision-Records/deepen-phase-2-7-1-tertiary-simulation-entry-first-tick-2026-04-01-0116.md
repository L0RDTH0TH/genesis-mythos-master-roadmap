---
title: "CDR — Phase 2.7.1 tertiary: simulation-entry bootstrap + first-tick order"
created: 2026-04-01
tags:
  - roadmap
  - conceptual-decision-record
  - sandbox-genesis-mythos-master
para-type: Project
project-id: sandbox-genesis-mythos-master
parent_roadmap_note: "[[Phase-2-7-1-Simulation-Entry-Bootstrap-and-Deterministic-First-Tick-Contract-Roadmap-2026-04-01-0116]]"
decision_kind: deepen
queue_entry_id: resume-deepen-gmm-271-followup-20260401T011600Z
master_goal: "[[Source-sandbox-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# Summary

Minted tertiary **2.7.1** defining **SimulationEntryBootstrap** field bindings (commit envelope, telemetry head, replay anchor + cold-start) and a **deterministic first-tick hook order** (input → world application → observation) aligned with secondary **2.7** and **2.6.3** replay surfaces. Preserves **2.4** authority and **GMM-2.4.5-*** as reference-only.

## PMG alignment

Advances the Phase 2 procedural-generation spine from **committed world** to **first simulation tick** with explicit NL contracts — matching the master goal’s staged pipeline and collaboration story without claiming execution closure artifacts.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|-------------|--------|----------|----------------|
| Single monolithic bootstrap blob without ordered first-tick hooks | Simpler doc | Harder to test/replay determinism | Ordered hooks match downstream validation and audit traceability |
| Defer bootstrap shape to execution-only | Shorter conceptual note | Breaks handoff from **2.6.3** | Secondary **2.7** already committed to admission record — field list needed here |

## Validation evidence

- Pattern-only continuity from [[Phase-2-7-Simulation-Entry-Bootstrap-and-Deterministic-First-Tick-Roadmap-2026-04-01-0115]], [[Phase-2-6-3-Consumer-Replay-Cold-Start-and-Secondary-2-6-Rollup-Closure-Roadmap-2026-03-30-2109]], [[Phase-2-4-5-Commit-Decision-Finalization-Replay-Safety-and-Audit-Handoff-Roadmap-2026-03-31-0345]], [[Phase-2-5-2-Cross-Sink-Correlation-and-Deterministic-Timeline-Ordering-Roadmap-2026-03-31-2200]].

## Links

- Parent: [[Phase-2-7-1-Simulation-Entry-Bootstrap-and-Deterministic-First-Tick-Contract-Roadmap-2026-04-01-0116]]
- Workflow anchor: `2026-04-01 01:18 | deepen | Phase-2-7-1-... | queue_entry_id: resume-deepen-gmm-271-followup-20260401T011600Z`
