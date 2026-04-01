---
title: "CDR — Phase 2.1.5 replay ledger and restore cursor"
created: 2026-03-30
tags:
  - roadmap
  - conceptual-decision-record
  - genesis-mythos-master
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-2-1-5-Replay-Ledger-Canonical-Diff-Surface-and-Restore-Cursor-Roadmap-2026-03-30-2310]]"
decision_kind: deepen
queue_entry_id: resume-gmm-deepen-215-20260330T230500Z
master_goal: "[[Source-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# CDR — Phase 2.1.5 replay ledger and restore cursor

## Summary

Minted tertiary `2.1.5` to complete the Phase `2.1` deterministic staging slice with replay-ledger and restore-cursor contracts. This closes the gap between identity/diff (`2.1.4`) and practical deterministic resume after validation stops.

## PMG alignment

Supports the PMG requirement for explainable procedural generation by making replay and recovery paths explicit before execution-track implementation.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|-------------|--------|----------|----------------|
| Keep replay/restore details inside 2.1.4 | Fewer files | Identity and replay concerns remain mixed | Separate slice improves handoff readability |
| Defer replay cursor entirely to execution | Faster conceptual pass | Missing NL contract for recovery semantics | Needed now for deterministic design authority |

## Validation evidence

- `pattern_only`: deterministic replay and resume-ledger design patterns; no new `Ingest/Agent-Research/` notes in this run.

## Links

- Parent: [[Phase-2-1-5-Replay-Ledger-Canonical-Diff-Surface-and-Restore-Cursor-Roadmap-2026-03-30-2310]]
- Prior slice: [[Phase-2-1-4-Bundle-Identity-Seam-Catalog-Stability-and-Replay-Diff-Roadmap-2026-03-30-2305]]
