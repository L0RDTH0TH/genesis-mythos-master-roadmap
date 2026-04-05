---
title: "CDR — Phase 5.1.2 kernel evaluation schedule and rule ordering"
created: 2026-04-04
tags:
  - roadmap
  - conceptual-decision-record
  - godot-genesis-mythos-master
para-type: Project
project-id: godot-genesis-mythos-master
parent_roadmap_note: "[[Phase-5-1-2-Kernel-Evaluation-Schedule-and-Rule-Ordering-Roadmap-2026-04-04-0715]]"
decision_kind: deepen
queue_entry_id: followup-deepen-phase5-512-kernel-eval-gmm-20260404T071500Z
master_goal: "[[Source-godot-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# CDR — deepen Phase 5.1.2 (kernel evaluation schedule / rule ordering)

## Summary

Minted tertiary **5.1.2** to define **EvaluationFrame** scheduling, **tuple-first then precedence_class** pass order, and deterministic winner selection per **(seam_id, conflict_class)** group aligned with **5.1.1** ordering and **3.1.2** defer boundaries. Cross-seam matrix and rich explanation payloads remain **5.1.3+**.

## PMG alignment

Advances the Genesis Mythos **rules engine** design: replay-stable evaluation semantics bridge manifest admission (**5.1.1**) to future conflict matrices (**5.1.3**) without bypassing Phase **2** commit or Phase **3** tick authority.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| --- | --- | --- | --- |
| Merge precedence into **5.1.1** single pass | Fewer named passes | Blurs admission vs schedule concerns | Keeps **5.1.1** focused on manifest + tuple; **5.1.2** owns schedule |
| Define full matrix here | Richer single note | Violates tertiary chain plan; overloads ctx | Reserved for **5.1.3** |
| Host-only schedule (no manifest ordinal) | Simpler manifest | Weak mod/ecosystem determinism | Manifest **precedence_ordinal** hook preserves packager intent |

## Validation evidence

- Pattern: deterministic ordering + replay-stable frames align with prior Phase **2.4.1** / **2.7** commit and trace vocabulary in this vault.
- On-disk: [[Phase-5-1-2-Kernel-Evaluation-Schedule-and-Rule-Ordering-Roadmap-2026-04-04-0715]], parent [[Phase-5-1-1-Ruleset-Manifest-Seam-Admission-and-Deterministic-Evaluation-Order-Roadmap-2026-04-04-0010]].

## Links

- Workflow anchor: [[workflow_state]] ## Log — **2026-04-04 07:18** — Target `Phase-5-1-2-Kernel-Eval-Schedule`
- Queue: `followup-deepen-phase5-512-kernel-eval-gmm-20260404T071500Z`
