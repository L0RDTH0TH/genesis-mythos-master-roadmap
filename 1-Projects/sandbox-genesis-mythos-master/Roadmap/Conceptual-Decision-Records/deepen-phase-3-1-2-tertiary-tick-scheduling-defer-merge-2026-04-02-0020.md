---
title: "CDR — Deepen Phase 3.1.2 tick scheduling / defer-merge"
created: 2026-04-02
tags:
  - roadmap
  - conceptual-decision-record
  - sandbox-genesis-mythos-master
para-type: Project
project-id: sandbox-genesis-mythos-master
parent_roadmap_note: "[[Phase-3-1-2-Tick-Scheduling-Defer-Merge-and-Work-Queue-Policy-Roadmap-2026-04-02-0020]]"
decision_kind: deepen
queue_entry_id: resume-deepen-phase3-312-followup-gmm-20260402T002000Z
master_goal: "[[Source-sandbox-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# Decision record — Phase 3.1.2 tick scheduling and defer-merge policy

## Summary

Minted tertiary **3.1.2** as the **work-queue + deferral ledger + merge policy** slice under secondary **3.1**, bridging **3.1.1** lane ordering with **3.1** tick closure: incompatible writes **block closure** unless defer/escalate; compatible merges emit **provenance** for replay.

## PMG alignment

Keeps living-simulation design **deterministic and inspectable**—stalls and merges are **named policies**, not hidden engine behavior—so implementation teams can map queues and audit surfaces later without re-deriving Phase 2 commit semantics.

## Alternatives and tradeoffs

| Alternative | Upside | Downide | Why not chosen |
| --- | --- | --- | --- |
| **Single global FIFO queue** | Simple narrative | Starves subsystems; hides priority | Rejected — conflicts with **3.1** multi-subsystem tick story |
| **Silent last-writer merge** | Fewer blocked ticks | Non-replay-safe | Rejected — violates **3.1** “no silent merge” edge case |
| **Always defer on conflict** | Safe | Tick never completes under load | Partially captured as **escalation** + operator visibility, not infinite defer |

## Validation evidence

- **`pattern_only`** means **no external** `Ingest/Agent-Research/` synthesis notes**; the slice still carries full NL checklist + **GWT G–I** rows at tertiary depth (peer parity with **3.1.1** `handoff_readiness`).
- Vault continuity: [[Phase-3-1-Sim-Tick-and-Event-Bus-Spine-Roadmap-2026-03-30-2213]], [[Phase-3-1-1-Event-Bus-Ordering-and-Pub-Sub-Lanes-Roadmap-2026-03-30-1830]], Phase 3 primary checklist.

## Links

- Parent roadmap note: [[Phase-3-1-2-Tick-Scheduling-Defer-Merge-and-Work-Queue-Policy-Roadmap-2026-04-02-0020]]
- Workflow anchor: last deepen row **Phase-3-1-2** / `resume-deepen-phase3-312-followup-gmm-20260402T002000Z` in [[workflow_state]]
