---
title: "CDR — Phase 2.7.2 tertiary: dry-run shadow + hook matrix + operator preview"
created: 2026-04-01
tags:
  - roadmap
  - conceptual-decision-record
  - genesis-mythos-master
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-2-7-2-First-Tick-Dry-Run-Shadow-Hook-Matrix-and-Operator-Bootstrap-Preview-Roadmap-2026-04-01-1200]]"
decision_kind: deepen
queue_entry_id: resume-deepen-gmm-272-followup-20260401T013000Z
master_goal: "[[Source-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# Summary

Minted tertiary **2.7.2** defining **first-tick dry-run shadow** policy (`mandatory` / `optional_operator` / `off`), a **hook matrix** refining **2.7.1** lanes without reordering, **operator-visible bootstrap preview** (read-only), and **multi-operator admission** minimum fields (`admission_ticket_id`, tie-break). Preserves **GMM-2.4.5-*** as reference-only.

## PMG alignment

Extends simulation-entry design toward **inspectable, replay-stable** first-tick behavior and **operator clarity** before observable sim frames — consistent with staged pipeline + collaboration goals without claiming execution closure.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|-------------|--------|----------|----------------|
| Mandatory dry-run for all sessions | Maximum safety | Higher latency story | Default **optional_operator** preserves **2.7.1** admission simplicity; tooling can force mandatory |
| Collapse matrix into **2.7.1** only | Fewer files | Loses sub-hook traceability | Matrix is the explicit refinement layer for replay ids |

## Validation evidence

- Pattern-only continuity from [[Phase-2-7-1-Simulation-Entry-Bootstrap-and-Deterministic-First-Tick-Contract-Roadmap-2026-04-01-0116]], [[Phase-2-7-Simulation-Entry-Bootstrap-and-Deterministic-First-Tick-Roadmap-2026-04-01-0115]], [[Phase-2-6-2-Operator-Session-Escalation-Surfaces-and-Forge-Continuity-Roadmap-2026-03-30-1200]].

## Links

- Parent: [[Phase-2-7-2-First-Tick-Dry-Run-Shadow-Hook-Matrix-and-Operator-Bootstrap-Preview-Roadmap-2026-04-01-1200]]
- Workflow anchor: `2026-04-01 12:00 | deepen | Phase-2-7-2-... | queue_entry_id: resume-deepen-gmm-272-followup-20260401T013000Z`
