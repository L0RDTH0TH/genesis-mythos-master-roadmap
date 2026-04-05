---
title: CDR — Phase 2.1.2 tertiary (stage family bodies and boundary hooks)
created: 2026-03-30
tags:
  - roadmap
  - conceptual-decision-record
  - godot-genesis-mythos-master
para-type: Project
project-id: godot-genesis-mythos-master
parent_roadmap_note: "[[Phase-2-1-2-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-03-30-1015]]"
decision_kind: deepen
queue_entry_id: resume-deepen-2-2-20260330T101039Z-01
master_goal: "[[Source-godot-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# Decision record — tertiary 2.1.2 (stage family bodies and boundary hooks)

## Summary

Minted tertiary **2.1.2** under secondary **2.1** as an interface refinement over the earlier stage-family contract: it makes **boundary hooks** explicit by wiring **validation outcome label mapping** into the conceptual commit-boundary token flow.

## PMG alignment

Supports the master goal's emphasis on deterministic, inspectable generation by ensuring the “dry-run validation -> commit boundary” split is represented as a stable conceptual API surface. This lets later execution-track work expand detail without weakening the pre-commit safety boundary.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|-------------|--------|-----------|----------------|
| Bind boundary hooks only at the narrative level | Minimal conceptual churn | Consumers must re-derive “why” from narrative, not typed labels | Typed interface surfaces are the conceptual contract here |
| Skip explicit validation label mapping | Less interface surface area | Validation explanations become hard to route downstream | Label mapping keeps dry-run outcomes usable at the boundary layer |
| Move token/label semantics into execution track now | Better immediate implementability | Locks naming and coupling too early | Execution details belong in the execution branch |

**Chosen path:** Extend the boundary-hook surface with explicit `ValidationDecisionLabels` mapping and keep the commit boundary token opaque/authoritative.

## Validation evidence

- Pattern-only: aligned with staged procedural generation practice and deterministic replay conventions; no new `Ingest/Agent-Research/` notes were bound this run.

## Links

- Roadmap note: [[Phase-2-1-2-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-03-30-1015]]
- Workflow anchor: `2026-03-30 10:15` — Target `Phase-2-1-2-Stage-Family-Bodies-and-Boundary-Hooks`

