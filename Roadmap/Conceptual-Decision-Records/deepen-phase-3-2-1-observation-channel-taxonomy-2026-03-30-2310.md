---
title: "CDR — Phase 3.2.1 tertiary (observation channel taxonomy)"
created: 2026-03-30
tags:
  - conceptual-decision-record
  - roadmap
  - godot-genesis-mythos-master
para-type: Project
project-id: godot-genesis-mythos-master
parent_roadmap_note: "[[Phase-3-2-1-Observation-Channel-Taxonomy-Roadmap-2026-03-30-2310]]"
decision_kind: deepen
queue_entry_id: followup-deepen-phase3-321-gmm-20260402T231000Z
master_goal: "[[Source-godot-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# Conceptual decision record — Phase 3.2.1 tertiary

## Summary

Minted **tertiary 3.2.1** under secondary **3.2**: **ObservationChannel** taxonomy **aligned** to **3.1.1** **lane + subscription_pattern** materialization, explicit **authority_class** (**committed_session** vs **preview_shadow**) tied to **3.1.2**/**3.1.4** checkpoint story and **3.1.3** classification, plus **GWT** rows **A–C** — without new bus semantics or resolving **D-3.1.5-***.

## PMG alignment

Supports **living simulation** by making **rendering and operator tooling** consume **simulation state** through **named, replay-consistent** observation paths that **cannot** silently **override** **3.1** authority — **preview** stays **non-authoritative**; **committed** stays **checkpoint-gated**.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| --- | --- | --- | --- |
| **Observation as independent topic graph** | Flexible UX | Breaks **3.1.1** replay + ordering contract | **Channels** **map** to **(lane, pattern)** — **reuse** bus ordering. |
| **Merge preview + committed in one channel** | Fewer subscriptions | Hides **authority** and risks **shadow** mistaken for **live** | **Split** by **authority_class**; **composite** overview is **explicit** edge case. |
| **Resolve D-3.1.5-* in this slice** | Fewer open rows | **Execution-deferred** scope; would violate **conceptual** track waiver | **Reference** only; **binding** stays **3.2+** / [[decisions-log]]. |

## Validation evidence

- Pattern continuity from [[Phase-3-1-1-Event-Bus-Ordering-and-Pub-Sub-Lanes-Roadmap-2026-03-30-1830]], [[Phase-3-1-3-Sim-Visible-Classification-and-DM-Overwrite-Channel-Mapping-Roadmap-2026-04-02-0035]], [[Phase-3-1-4-Persistence-Checkpoint-Boundaries-Roadmap-2026-04-02-2240]], and parent [[Phase-3-2-Simulation-Rendering-Decoupling-and-Observation-Channels-Roadmap-2026-04-02-2300]]; no external research synth notes.

## Links

- Parent roadmap note: [[Phase-3-2-1-Observation-Channel-Taxonomy-Roadmap-2026-03-30-2310]]
- Workflow log anchor: `2026-04-02 23:10` — deepen — Phase-3-2-1 — `queue_entry_id: followup-deepen-phase3-321-gmm-20260402T231000Z`
