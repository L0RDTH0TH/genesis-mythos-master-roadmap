---
title: "Decision record — deepen Phase 4.1.3 post–D-087 shallow (2026-03-26)"
created: 2026-03-26
tags: [roadmap, conceptual-decision-record, genesis-mythos-master, phase-4-1-3]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[phase-4-1-3-control-contracts-and-presentation-golden-placeholder-roadmap-2026-03-26-2100]]"
decision_kind: deepen
queue_entry_id: followup-deepen-post-recal-empty-bootstrap-413-gmm-20260326T231900Z
master_goal: "[[Genesis-mythos-master-goal]]"
validation_status: pattern_only
related_research: []
---

# Decision record — deepen Phase 4.1.3 (post–D-087 shallow)

## Summary

One **narrow** conceptual **`deepen`** at **`4.1.3`** after **D-087** **`recal`** parity: added an explicit **read-model staleness** rule tying golden-row selection to **`tick_epoch`** / rig consume order, plus a second **non-claiming** placeholder row sketch (**`G-P4.1.3-CTRL-002`**) for camera/binding defer — **no** rollup/CI closure claims.

## PMG alignment

Keeps the player-first presentation/control thread honest: read paths stay pure and tick-scoped, and golden placeholders remain **`OPEN_STUB`** until **D-032**/**D-043** literals exist — consistent with deterministic replay posture in the PMG.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| --- | --- | --- | --- |
| Heavy expansion (new quaternary notes) | More surface area | **Ctx 89%** — violates **D-060** narrow deepen | User + resolver requested **shallow** in-place refinement |
| **`recal`** only (no deepen) | Drift-only pass | Does not thicken thin narrative on **4.1.3** | Queue locked **`deepen`** with **`effective_action: deepen`** |
| Pre-deepen **Research** `Task` | External citations | Not requested; adds latency | **`research_pre_deepen`**: skipped |

## Validation evidence

- Pattern-only: vault-first contract text; no new `Ingest/Agent-Research/` notes.
- **Queue / state:** [[workflow_state]] **`## Log`** row **2026-03-26 23:35** · `queue_entry_id` **`followup-deepen-post-recal-empty-bootstrap-413-gmm-20260326T231900Z`**.

## Links

- [[workflow_state]]
- [[roadmap-state]]
- [[decisions-log]]
