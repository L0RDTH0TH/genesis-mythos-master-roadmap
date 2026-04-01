---
title: "CDR — Phase 3.1.1 tertiary (event bus ordering + pub/sub lanes)"
created: 2026-03-30
tags:
  - conceptual-decision-record
  - roadmap
  - genesis-mythos-master
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-3-1-1-Event-Bus-Ordering-and-Pub-Sub-Lanes-Roadmap-2026-03-30-1830]]"
decision_kind: deepen
queue_entry_id: resume-deepen-phase3-311-followup-gmm-20260402T001000Z
master_goal: "[[Source-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# Conceptual decision record — Phase 3.1.1 tertiary

## Summary

Minted **tertiary 3.1.1** under secondary **3.1**: **lane-scoped total order** for `SimEvent`, **pub/sub registration** NL + lightweight sketches, **GWT** rows **D–F** extending secondary acceptance **A–C**, and explicit **preview vs authoritative** replay exclusion—without API/transport commitments.

## PMG alignment

Supports **living simulation** by making the **bus** mechanically understandable for juniors: deterministic **ordering** per lane, **subscription-filtered** streams, and **replay parity** language compatible with **FirstCommittedTickTrace** lineage from Phase 2.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| --- | --- | --- | --- |
| **Global total order across all lanes** | Simplest mental model | Misrepresents intentional parallelism across unrelated lanes | **Partial order** across lanes + **total** within lane matches Phase 3 primary **decoupling** story. |
| **Pub/sub as pure topic graph (no lane)** | Flexible | Collides with **DM overwrite** + replay lane semantics already in **3.1** | Kept **lane** as primary partition; **topic_pattern** lives inside subscription. |
| **Full pseudo-code / API signatures now** | Implementation-ready | Depth-3 slice; would violate conceptual escalation | **Sketches only**; execution formats deferred. |

## Validation evidence

- Pattern continuity from [[Phase-3-1-Sim-Tick-and-Event-Bus-Spine-Roadmap-2026-03-30-2213]] and [[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-03-30-0430]]; no external research synth notes.

## Links

- Parent roadmap note: [[Phase-3-1-1-Event-Bus-Ordering-and-Pub-Sub-Lanes-Roadmap-2026-03-30-1830]]
- Workflow log anchor: `2026-04-02 00:10` — deepen — Phase-3-1-1 — `queue_entry_id: resume-deepen-phase3-311-followup-gmm-20260402T001000Z` (human Timestamp monotonic after `2026-04-02 00:05`)
