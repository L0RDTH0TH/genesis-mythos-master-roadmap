---
title: CDR — Phase 1.2.3 stage families and pipeline roles
created: 2026-03-30
tags:
  - roadmap
  - conceptual-decision-record
  - sandbox-genesis-mythos-master
para-type: Project
project-id: sandbox-genesis-mythos-master
parent_roadmap_note: "[[Phase-1-2-3-Stage-Families-Specialization-and-Pipeline-Roles-Roadmap-2026-03-30-1905]]"
decision_kind: deepen
queue_entry_id: resume-gmm-deepen-123-20260330T190500Z
master_goal: "[[Source-sandbox-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# CDR — Phase 1.2.3 stage families and pipeline roles

## Summary

Adopted a **four-family** model (**structure**, **entities**, **glue**, **commit**) plus optional **specialization** sub-tags under **1.2.1** / **1.2.2**, so procedural graph nodes have clear pipeline roles without binding implementation modules.

## PMG alignment

Organizes generation into **reviewable chunks** that map to **world-building vs simulation** boundaries in the master goal—**commit**-family stages remain the explicit gate before live simulation consumes outputs.

## Alternatives and tradeoffs

| Alternative | Upside | Downide | Why not chosen |
|-------------|--------|---------|------------------|
| Per-phase ad hoc labels only | Flexible | Drift across slices; weak handoff | Families give **stable vocabulary** for Phase 2 scoping |
| Fine-grained taxonomy (10+ families) | Precise | Premature; overlaps **1.2.1** node kinds | **Four families** + specialization keeps **NL** readable |
| Merge glue + entities | Fewer buckets | Blurs **overlay** vs **spawn** concerns | Split preserves **hook** vs **authoritative spawn** clarity |

## Validation evidence

- Pattern-only: DAG pipelines, layered build systems, “layer cake” world generation practice; no external synth notes this run.

## Links

- Parent: [[Phase-1-2-3-Stage-Families-Specialization-and-Pipeline-Roles-Roadmap-2026-03-30-1905]]
- Workflow anchor: `2026-03-30 19:05 | deepen | Phase-1-2-3-Stage-Families... | 11 | 1.2.3`
- Queue: `resume-gmm-deepen-123-20260330T190500Z`
