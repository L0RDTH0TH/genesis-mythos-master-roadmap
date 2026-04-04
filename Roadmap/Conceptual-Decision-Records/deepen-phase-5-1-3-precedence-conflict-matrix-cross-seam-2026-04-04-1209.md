---
title: "CDR — Phase 5.1.3 precedence conflict matrix and cross-seam resolution"
created: 2026-04-04
tags:
  - roadmap
  - conceptual-decision-record
  - genesis-mythos-master
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-5-1-3-Precedence-Conflict-Matrix-and-Cross-Seam-Resolution-Roadmap-2026-04-04-1209]]"
decision_kind: deepen
queue_entry_id: followup-deepen-phase5-513-precedence-matrix-gmm-20260404T120700Z
master_goal: "[[Source-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# CDR — deepen Phase 5.1.3 (precedence conflict matrix / cross-seam)

## Summary

Minted tertiary **5.1.3** to define a unified **precedence conflict matrix** for **same-seam** and **cross-seam** **conflict_class** groups, canonical seam-pair keys, matrix revision binding to **5.1.1**/**5.1.2**, and **GWT-5.1.3-A–K** narrowed vs **GWT-5.1.2**. Closes the **5.1.1–5.1.3** tertiary chain; next structural target is **secondary 5.1 rollup**.

## PMG alignment

Completes the Phase **5.1** conceptual spine for deterministic rule conflict resolution and operator legibility (**4.1.3**) without bypassing Phase **2** commit semantics or Phase **3** tick/defer authority.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| --- | --- | --- | --- |
| Per-seam matrices only | Simpler tables | Cannot express cross-seam interlocks | Cross-seam rows required for **3.4.1** multi-seam consumption |
| Embed matrix in **5.1.2** | One fewer note | Overloads schedule + policy dimensions | **5.1.3** keeps matrix as explicit authority |
| Host-only cross-seam policy | Smaller manifests | Opaque mod determinism | Manifest-carried **matrix_revision** preserves packager intent |

## Validation evidence

- Pattern: matrix + ordered seam keys align with **2.2.3** merge-policy and **2.4.1** precedence vocabulary already in vault.
- On-disk: [[Phase-5-1-3-Precedence-Conflict-Matrix-and-Cross-Seam-Resolution-Roadmap-2026-04-04-1209]], upstream [[Phase-5-1-2-Kernel-Evaluation-Schedule-and-Rule-Ordering-Roadmap-2026-04-04-0715]].

## Links

- Workflow anchor: [[workflow_state]] ## Log — **2026-04-04 12:09** — Target `Phase-5-1-3-Precedence-Conflict-Matrix`
- Queue: `followup-deepen-phase5-513-precedence-matrix-gmm-20260404T120700Z`
