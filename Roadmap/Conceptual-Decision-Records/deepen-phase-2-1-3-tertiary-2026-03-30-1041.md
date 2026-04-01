---
title: "CDR — Phase 2.1.3 staged delta bundles and merge seams"
created: 2026-03-30
tags:
  - roadmap
  - conceptual-decision-record
  - genesis-mythos-master
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-2-1-3-Staged-Delta-Bundles-Merge-Seams-and-Apply-Ordering-Roadmap-2026-03-30-1041]]"
decision_kind: deepen
queue_entry_id: empty-bootstrap-gmm-20260330T104148Z
master_goal: "[[Source-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# Conceptual decision record — Phase 2.1.3

## Summary

Minted tertiary **2.1.3** defining **StagedDeltaBundle**, **merge seams** with explicit resolution policies (no silent last-writer-wins), and **apply ordering** aligned with the Stage 0→5 spine — bridging typed outputs from **2.1.1**/**2.1.2** into a single pre-commit validation unit.

## PMG alignment

Advances the Phase 2 goal of a **staged procedural worldgen pipeline** with safe dry-run before commit: bundles give Stage 4 a single coherent artifact to judge, preserving determinism and explainability through **ValidationDecisionLabels** across merges.

## Alternatives and tradeoffs

| Alternative | Upside | Downide | Why not chosen |
|-------------|--------|---------|----------------|
| Per-stage validation only (no bundle) | Simpler stories | Inconsistent global state at commit | Fails “single dry-run gate” contract |
| Implicit merge by stage priority | Less prose | Hidden nondeterminism | Violates explicit merge seam rule |
| Deferred ordering to execution only | Shorter conceptual note | Gaps handoff for replay | Ordering is design authority on conceptual track |

## Validation evidence

- Pattern-only: deterministic build/merge-point practice; no external citations this run.

## Links

- Parent roadmap note: [[Phase-2-1-3-Staged-Delta-Bundles-Merge-Seams-and-Apply-Ordering-Roadmap-2026-03-30-1041]]
- Workflow anchor: `2026-03-30 10:41` — `Phase-2-1-3-Staged-Delta-Bundles-Merge-Seams`
