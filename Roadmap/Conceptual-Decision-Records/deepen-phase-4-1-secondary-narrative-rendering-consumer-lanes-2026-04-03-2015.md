---
title: "Deepen — Phase 4.1 secondary: narrative + rendering consumer lanes"
created: 2026-04-03
tags:
  - roadmap
  - conceptual-decision-record
  - genesis-mythos-master
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-03-30-0430]]"
decision_kind: deepen
queue_entry_id: followup-deepen-phase4-primary-post-advance-p3-p4-gmm-20260403T190000Z
master_goal: "[[Source-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# Decision record — Phase 4.1 secondary mint

## Summary

Minted **secondary 4.1** — **narrative-facing** vs **rendering-facing** **consumer surface lanes** subscribing to the same **3.4.1** **SeamId** / **3.2.x** **ObservationChannel** truth, with per-lane presentation policy (cadence, emphasis) only — **no** second sim truth. **D-3.4-narrative-rendering-split** remains the bundle-policy decision locus in [[decisions-log]].

## PMG alignment

Preserves the master goal’s separation of **simulation truth** from **presentation**: Phase 4 consumers **reflect** upstream seams without mutating **3.1.4** checkpoints or **3.1.3** overwrite semantics, keeping large-tabletop and narrative UX honest under **preview_shadow** vs **committed_session**.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| --- | --- | --- | --- |
| Single merged “UI consumer” lane | Simpler story | Hides render-budget vs narrative-refresh conflicts | Two lanes match **D-3.4-narrative-rendering-split** and real failure modes (lane skew / disclosure) |
| Execution-first API sketches at 4.1 | Faster coding | Violates conceptual depth contract for secondary container | **4.1.1+** tertiaries carry algorithm sketches |
| Defer 4.1 until all **3.2** tertiaries enumerated | Fewer moving parts | Blocks Phase 4 structural progress | **3.2.1–3.2.3** + **3.4.1** already bound; 4.1 only consumes |

## Validation evidence

- Pattern-only: continuity from [[Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-03-30-0430]], [[Phase-3-4-1-Handoff-Seam-Catalog-and-Consumer-Contract-Rows-Roadmap-2026-04-03-0115]], [[Phase-3-2-1-Observation-Channel-Taxonomy-Roadmap-2026-03-30-2310]].

## Links

- Slice: [[Phase-4-1-Narrative-Rendering-and-Consumer-Surface-Lanes-Roadmap-2026-04-03-2015]]
- Workflow anchor: **2026-04-03 20:15** — Phase 4 secondary **4.1** mint; next cursor **4.1.1**
