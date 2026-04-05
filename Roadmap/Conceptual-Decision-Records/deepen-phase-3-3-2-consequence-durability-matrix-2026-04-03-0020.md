---
title: "CDR — Phase 3.3.2 consequence durability matrix and persistence invariants"
created: 2026-04-03
tags:
  - roadmap
  - conceptual-decision-record
  - godot-genesis-mythos-master
para-type: Project
project-id: godot-genesis-mythos-master
parent_roadmap_note: "[[Phase-3-3-2-Consequence-Durability-Matrix-and-Persistence-Invariants-Roadmap-2026-04-03-0020]]"
decision_kind: deepen
queue_entry_id: followup-deepen-phase3-332-gmm-20260403T002000Z
master_goal: "[[Source-godot-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# CDR — Phase 3.3.2 — Consequence durability matrix and persistence invariants

## Summary

Minted tertiary **3.3.2** with an NL **consequence durability matrix** (durability_class × merge × checkpoint × observation) and **five persistence invariants** (**I-3.3-A–E**) plus **GWT-3.3-G–K**, closing the gap between **3.3.1** seam sketches and operator-auditable **single durability story** routing toward **secondary 3.3 rollup**.

## PMG alignment

Advances the **living simulation** spine by making **which facts persist** and **where they may appear** explicit **before** execution wire formats — reducing duplicate authority between **3.1.4**, **3.1.5**, and **3.2.x** observation surfaces.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| --- | --- | --- | --- |
| **A — Matrix deferred to execution track only** | Shorter conceptual tree | Loses design-team **delegation** contract | **3.3** is the cohesion slice — matrix belongs here |
| **B — Four durability classes** | Finer control | Overlaps **3.1.3** classification | Stay with **3.3.1** **three-class** model |
| **C — Merge matrix only (no invariants)** | Smaller note | Harder to audit compliance | **Invariants** give **checklist** closure for rollup |

## Validation evidence

- **pattern_only** — extends **3.3.1** **ConsequenceRecord** / **VitalitySnapshot** sketches; no external research synth this run.
- Parent note: [[Phase-3-3-2-Consequence-Durability-Matrix-and-Persistence-Invariants-Roadmap-2026-04-03-0020]].

## Links

- **Workflow anchor:** `2026-04-03 00:20` — deepen — **Phase-3-3-2-Consequence-Durability-Matrix** — `queue_entry_id: followup-deepen-phase3-332-gmm-20260403T002000Z`
- **Decisions log:** [[decisions-log]]
