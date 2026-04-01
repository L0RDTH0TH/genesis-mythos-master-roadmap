---
title: "CDR — Phase 4.2.1 session orchestration hooks + perspective transition graph"
created: 2026-04-03
tags:
  - roadmap
  - conceptual-decision-record
  - genesis-mythos-master
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-4-2-1-Session-Scoped-Orchestration-Hooks-and-Perspective-Transition-Graph-Roadmap-2026-04-03-2125]]"
decision_kind: deepen
queue_entry_id: followup-deepen-phase4-41-rollup-gmm-20260403T211500Z
master_goal: "[[Source-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# CDR — Phase 4.2.1 — Session-scoped orchestration hooks

## Summary

Minted tertiary **4.2.1** to bind **perspective control** changes to **session-scoped orchestration** (single ingress envelope) and a **PerspectiveTransitionGraph** aligned with Phase **4 primary** modes, with explicit **3.1.2** defer-merge and **3.1.4** checkpoint ordering — preserving **one authority lane** after **4.1** dual consumer lanes.

## PMG alignment

Advances the **perspective split + control systems** arc without introducing a second simulation or commit authority: control mutations funnel through orchestration + graph validation before **4.1** adapters project to narrative/rendering.

## Alternatives and tradeoffs

| Alternative | Upside | Downide | Why not chosen |
| --- | --- | --- | --- |
| Per-lane control stacks (narrative vs rendering) | Flexible UX tuning | Two writers risk divergence | Violates secondary **4.2** single-lane contract |
| Implicit transitions (no graph) | Simpler spec | Harder replay + audit | Conflicts with **2.x** deterministic lineage discipline |
| Immediate apply (no defer-merge gate) | Lower latency | Race with **3.1.2** | Breaks Phase **3** scheduling authority |

## Validation evidence

- Pattern-only: vault continuity with [[Phase-4-2-Session-Orchestration-and-Perspective-Control-Coherence-Roadmap-2026-04-03-2120]], [[Phase-3-1-2-Tick-Scheduling-Defer-Merge-and-Work-Queue-Policy-Roadmap-2026-04-02-0020]], [[Phase-3-1-4-Persistence-Checkpoint-Boundaries-Roadmap-2026-04-02-2240]].

## Links

- Parent roadmap note: [[Phase-4-2-1-Session-Scoped-Orchestration-Hooks-and-Perspective-Transition-Graph-Roadmap-2026-04-03-2125]]
- Workflow anchor: `2026-04-03 21:25` — **Phase-4-2-1-...** deepen row in [[workflow_state]]
