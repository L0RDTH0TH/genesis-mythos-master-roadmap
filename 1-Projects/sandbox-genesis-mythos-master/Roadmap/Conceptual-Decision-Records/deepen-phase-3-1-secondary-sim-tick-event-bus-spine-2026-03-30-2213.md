---
title: "CDR — Phase 3.1 secondary (sim tick + event bus spine)"
created: 2026-03-30
tags:
  - conceptual-decision-record
  - roadmap
  - sandbox-genesis-mythos-master
para-type: Project
project-id: sandbox-genesis-mythos-master
parent_roadmap_note: "[[Phase-3-1-Sim-Tick-and-Event-Bus-Spine-Roadmap-2026-03-30-2213]]"
decision_kind: deepen
queue_entry_id: resume-deepen-phase3-31-post-recal-p3-high-util-gmm-20260401T221800Z
master_goal: "[[Source-sandbox-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# Conceptual decision record — Phase 3.1 secondary

## Summary

Minted **Phase 3 secondary 3.1** as the **sim tick + event bus spine**: monotonic tick advance, **SimEvent**-shaped bus seam with ordering and replay-visibility contracts, and explicit continuity from **2.7.3** **FirstCommittedTickTrace** without re-deriving **2.4**/**2.5** semantics.

## PMG alignment

Advances the **living simulation** layer of the master goal: deterministic **tick cadence** and a **cross-cutting bus** let agents, weather, DM tools, and persistence share **one** narrative of world evolution while keeping **rendering** and **execution** formats deferred.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| ------------- | ------ | -------- | ---------------- |
| **Bus-first, tick-second** | Emphasizes cross-system messaging early | Risks unclear tick boundary for replay | **Tick** is the authoritative scheduler in Phase 3 primary ordering — **bus** hangs off tick closure. |
| **Merge tick + DM overwrite** into one secondary | Fewer notes | Overloads one slice; DM overwrite deserves separate secondary later | Kept **3.1** focused on **kernel + bus spine**; DM channels stay Phase 3 primary + later secondaries. |
| **Pseudo-code at secondary** | Implementation-ready | Violates conceptual depth for secondary **3.1** | **NL-only** at secondary; **3.1.1+** carry sketches. |

**Chosen path:** **Tick + event bus spine** as first Phase 3 secondary **3.1**, aligned with `workflow_state` cursor **3.1** and post-RECAL drift **0.00**.

## Validation evidence

- Pattern continuity from [[Phase-2-7-3-Shadow-to-Live-Parity-Admission-Ticket-Redemption-and-First-Committed-Tick-Trace-Roadmap-2026-03-30-1800]] and Phase 3 primary [[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-03-30-0430]]; no external research synth notes for this mint.

## Validation traceability (parent anchors)

- **First committed tick → tick ≥ 1:** CDR claims align with [[Phase-2-7-3-Shadow-to-Live-Parity-Admission-Ticket-Redemption-and-First-Committed-Tick-Trace-Roadmap-2026-03-30-1800]] **Behavior** / trace semantics (admission ticket redemption, shadow-to-live parity, **FirstCommittedTickTrace** as bridge).
- **Tick + bus ordering:** Aligns with [[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-03-30-0430]] **Behavior** (ordering: tick → intents → agency → consequences → checkpoint → bus → observation) and **Interfaces** (event bus as cross-cutting seam).
- **`GMM-2.4.5-*`:** Treated as reference-only deferment anchors per Phase 3 primary **Conceptual waiver** — no new execution closure in this CDR.

## Links

- Parent roadmap note: [[Phase-3-1-Sim-Tick-and-Event-Bus-Spine-Roadmap-2026-03-30-2213]]
- Workflow log row: `2026-04-02 00:05` — deepen — Phase-3-1-Sim-Tick-and-Event-Bus-Spine — `queue_entry_id: resume-deepen-phase3-31-post-recal-p3-high-util-gmm-20260401T221800Z`
