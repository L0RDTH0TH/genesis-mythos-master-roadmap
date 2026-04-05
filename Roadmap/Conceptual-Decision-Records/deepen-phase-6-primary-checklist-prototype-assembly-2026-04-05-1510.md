---
title: "CDR — Phase 6 primary checklist (prototype assembly)"
created: 2026-04-05
tags:
  - roadmap
  - conceptual-decision-record
  - sandbox-genesis-mythos-master
para-type: Project
project-id: sandbox-genesis-mythos-master
parent_roadmap_note: "[[Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-03-30-0430]]"
decision_kind: deepen
queue_entry_id: followup-deepen-phase6-primary-gmm-post-distilled-repair-20260405T130500Z
master_goal: "[[Source-sandbox-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# Phase 6 primary — prototype assembly scope

## Summary

Locked **Phase 6** as the **vertical-slice integration** phase: one replay-stable **Q3 2026** horizon that **assembles** Phases **2–5** into an operator-legible **end-to-end session path**, with **instrumentation** and **feedback capture**—without claiming marketplace CI, perf SLAs, or full production hardening (**execution-deferred**).

## PMG alignment

Advances the master goal by naming the **smallest shippable narrative** that proves **worldgen → sim → rules → perspective/orchestration → operator readout** coheres under the existing conceptual contracts, so execution can prototype without re-litigating upstream seams.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|-------------|--------|----------|----------------|
| **Breadth-first** (many thin slices) | Covers more surface area early | Weak integration story; hides seam failures | Fails the “assemble” intent of Phase 6 |
| **Engine-first** (implementation-led) | Faster code motion | Risks bypassing **2.x** commit / **4.x** orchestration authority | Violates upstream **non-bypass** invariants |
| **Research spike before checklist** | External benchmarks | Slows conceptual closure; not required at primary depth | Primary checklist is NL authority first |

## Validation evidence

- **Pattern-only:** Aligns with **Phase 5** primary rollup closure + **Phase 4.2** orchestration vocabulary as **labels** (not new truth).
- **Vault links:** [[Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-03-30-0430]], [[Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-03-30-0430]], [[Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-03-30-0430]], [[distilled-core]].

## Links

- **Workflow anchor:** `2026-04-05 15:05` — **Target:** `Phase-6-Primary-Checklist` — `queue_entry_id: followup-deepen-phase6-primary-gmm-post-distilled-repair-20260405T130500Z`
