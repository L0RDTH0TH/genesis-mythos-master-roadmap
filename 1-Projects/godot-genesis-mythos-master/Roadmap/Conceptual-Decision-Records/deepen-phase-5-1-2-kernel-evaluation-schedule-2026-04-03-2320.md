---
title: "CDR — Phase 5.1.2 kernel evaluation schedule and rule ordering"
created: 2026-04-03
tags:
  - conceptual-decision-record
  - godot-genesis-mythos-master
  - phase-5
para-type: Project
project-id: godot-genesis-mythos-master
parent_roadmap_note: "[[Phase-5-1-2-Kernel-Evaluation-Schedule-and-Rule-Ordering-Roadmap-2026-04-03-2320]]"
decision_kind: deepen
queue_entry_id: followup-deepen-phase4-41-rollup-gmm-20260403T211500Z
master_goal: "[[Source-godot-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# CDR — Phase 5.1.2 kernel evaluation schedule and rule ordering

## Summary

Minted tertiary **5.1.2** as **kernel evaluation schedule** and **deterministic rule ordering** after **5.1.1** admission, so **RuleOutcome** streams are **replay-stable** and **orchestration-aware** without claiming commit authority. **Conflict matrix** detail remains in **5.1.3**.

## PMG alignment

Preserves **deterministic / auditable** behavior: evaluation order is a **first-class** design object tied to **tick** and **transition** boundaries—consistent with the PMG’s simulation + orchestration integration story.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| --- | --- | --- | --- |
| Merge schedule + conflict matrix in **5.1.2** | One fewer file | Blurs ordering vs winner resolution | Keep **5.1.3** per secondary **5.1** canonical order |
| Per-rule dynamic priority at runtime | Flexible | Non-deterministic replay risk | Rejected—tie-break + **5.1.3** matrix |

## Validation evidence

- Pattern-only: parent [[Phase-5-1-Rule-Primitives-Plugin-Host-and-Conflict-Precedence-Roadmap-2026-04-03-2310]], prior tertiary [[Phase-5-1-1-Ruleset-Manifest-Admission-and-Seam-Binding-Roadmap-2026-03-31-1200]], scheduling context [[Phase-3-1-2-Tick-Scheduling-Defer-Merge-Work-Queue-Roadmap-2026-04-02-0020]].

## Links

- **Workflow anchor:** `2026-04-03 23:25` — `Phase-5-1-2-Kernel-Evaluation-Schedule-and-Rule-Ordering` — `queue_entry_id: followup-deepen-phase4-41-rollup-gmm-20260403T211500Z`
- **Resolver:** `gate_signature: stale-queue-4-1-vs-vault-5-1-2`, `effective_track: conceptual`, `gate_catalog_id: conceptual_v1`
