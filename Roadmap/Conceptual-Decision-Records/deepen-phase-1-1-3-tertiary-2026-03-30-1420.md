---
title: "CDR — Deepen 1.1.3 dependency direction and lifecycle"
created: 2026-03-30
tags:
  - conceptual-decision-record
  - godot-genesis-mythos-master
  - roadmap
para-type: Project
project-id: godot-genesis-mythos-master
parent_roadmap_note: "[[Phase-1-1-3-Dependency-Direction-and-Lifecycle-Roadmap-2026-03-30-1420]]"
decision_kind: deepen
queue_entry_id: resume-gmm-deepen-113-20260330T142000Z
master_goal: "[[Source-godot-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# Decision record — Tertiary 1.1.3 (dependency direction and lifecycle)

## Summary

Minted tertiary **1.1.3** documenting **acyclic cross-layer dependency rules**, **injection seams** for generation and mods, and **boot/teardown/swap** ordering aligned with commit and epoch semantics from **1.1.1** and **1.1.2**. Positions the next structural slice as **1.1.4** (or broader Phase 1 secondary expansion) without introducing execution-only CI/registry obligations.

## PMG alignment

Keeps the master goal’s **modular spine** honest: implementers see **where** code may plug in and **which directions** are forbidden, reducing the risk of silent reverse dependencies that break save/load and DM override stories.

## Alternatives and tradeoffs

| Alternative | Upside | Downide | Why not chosen |
|---------------|--------|---------|----------------|
| Collapse 1.1.3 into 1.1.2 | Fewer files | Mixes cache/observation with wiring concerns | Hurts navigation and handoff checklist granularity |
| Jump to Phase 2 after 1.1.2 | Faster to “generation” narrative | Skips explicit wiring story for mods/tools | Violates slice-by-slice conceptual contract for **1.1** |

## Validation evidence

- **pattern_only:** Established practice for DAG layer graphs and named injection in game engines and editor architectures; no external synth notes this run.

## Links

- Parent roadmap note: [[Phase-1-1-3-Dependency-Direction-and-Lifecycle-Roadmap-2026-03-30-1420]]
- Workflow anchor: `2026-03-30 14:20` — deepen — Phase-1-1-3-Dependency-Direction-and-Lifecycle — Iter Phase 1.1.3 — queue_entry_id `resume-gmm-deepen-113-20260330T142000Z`
