---
title: "Decision record — Phase 3 primary checklist (living simulation)"
created: 2026-03-30
tags:
  - roadmap
  - conceptual-decision-record
  - sandbox-genesis-mythos-master
para-type: Project
project-id: sandbox-genesis-mythos-master
parent_roadmap_note: "[[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-03-30-0430]]"
decision_kind: deepen
queue_entry_id: resume-deepen-phase3-post-recal-repair-gmm-20260401T221500Z
master_goal: "[[Source-sandbox-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# Decision record — Phase 3 primary checklist (living simulation)

## Summary

Established the **Phase 3 primary** natural-language contract: tick-based living simulation with explicit **DM overwrite semantics** (live tweak vs structural re-generation), **simulation vs rendering** decoupling for previews vs full sessions, and **determinism** continuity with Phase 2’s committed-tick / admission story. Primary depth stays **NL-first**; pseudo-code is deferred to secondaries (**3.1+**).

## PMG alignment

Advances the master goal toward a **playable, inspectable** simulation loop: time advances in **ticks**, agency (NPCs/factions) produces observable consequences, and operators can intervene without silently breaking replay contracts—aligned with **Genesis Mythos**’ collaborative forge + safety posture.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|-------------|--------|----------|----------------|
| **Event-only simulation** (no layered tick) | Simpler mental model | Harder to reason about ordering, previews, and DM overrides | Ticks match Phase 2 first-tick / admission narrative and give a stable cadence for agency + weather + persistence |
| **Unified sim+render loop** | Fewer seams | Breaks preview vs session separation; couples DM tweaks to frame policy | Explicit decoupling preserves Phase 1 layering and supports “what-if” previews |
| **Deep pseudo-code at primary** | Implementation-ready | Wrong depth for conceptual primary; blocks fast secondary decomposition | Kept primary at checklist depth; bodies belong under **3.x** |

## Validation evidence

- **Pattern-only:** Continuity with Phase 2 **2.7.x** simulation-entry / first-tick / shadow-to-live contracts ([[Phase-2-7-3-Shadow-to-Live-Parity-Admission-Ticket-Redemption-and-First-Committed-Tick-Trace-Roadmap-2026-03-30-1800]]), without claiming execution CI or registry closure (`GMM-2.4.5-*` remain reference-only).

## Links

- Parent: [[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-03-30-0430]]
- Workflow anchor: `2026-03-30 12:00` — Phase-3-Primary-Checklist deepen row in [[workflow_state]]
- Queue: `resume-deepen-phase3-post-recal-repair-gmm-20260401T221500Z`
