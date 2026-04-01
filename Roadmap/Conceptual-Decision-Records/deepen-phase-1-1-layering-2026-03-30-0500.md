---
title: "CDR — Phase 1.1 layering and interface contracts"
created: 2026-03-30
tags:
  - conceptual-decision-record
  - roadmap
  - genesis-mythos-master
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-03-30-0500]]"
decision_kind: deepen
queue_entry_id: resume-deepen-gmm-20260330T043100Z
master_goal: "[[Source-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# Conceptual decision record — Phase 1.1 layering

## Summary

Minted the **first Phase 1 secondary** at subphase **1.1**, documenting a four-layer separation (world state, simulation, rendering, input), directional flow, and interface contracts between layers. Positioned generation injection as orthogonal to the live tick loop, consistent with the PMG and Phase 1 primary note.

## PMG alignment

Supports immersion-safe iteration (clear boundaries, no silent cross-layer mutation), collaboration-friendly overrides (intents routed through simulation), and extensibility (named injection points and commit discipline) without locking an engine or API surface.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| --- | --- | --- | --- |
| **Three-layer** (merge input into render) | Fewer named boxes | Blurs device/UI vs game-intent concerns | Conflicts with DM tool UX and deterministic sim testing |
| **Simulation owns render** (tight coupling) | Simpler data path for small demos | Hard to swap renderers or run headless sim | Violates modularity and later Phase 4 perspective split |
| **ECS-only spine** (no “layers”) | Matches some engines | Overfits one pattern; obscures intent/commit story for designers | PMG emphasizes seams non-technical readers can track — layers first |

**Chosen path:** Four named layers with explicit commit and read boundaries; tertiaries (1.1.1+) can add interface sketches without rewriting this contract.

## Validation evidence

- Pattern alignment with common **game architecture layering** and **ports-and-adapters** style boundaries (no external paper citations in-vault for this run).
- Parent alignment: [[Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-03-30-0430]], distilled core: [[distilled-core]].

## Links

- Parent roadmap note: [[Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-03-30-0500]]
- Workflow log row: `2026-03-30 05:00 | deepen | Phase-1-1-Layering-Contracts | … | 1.1 | …`
