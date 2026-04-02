---
title: Conceptual decision record — deepen phase 2.2.3 tertiary
created: 2026-03-31
tags:
  - roadmap
  - conceptual-decision-record
  - genesis-mythos-master
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-2-2-3-Conflict-Resolution-Priority-Ordering-and-Merge-Policy-Roadmap-2026-03-31-0002]]"
decision_kind: deepen
queue_entry_id: resume-deepen-gmm-223-20260331T000200Z-forward
master_goal: "[[Source-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

## Summary

Selected a deterministic conflict-resolution tertiary for the 2.2 resolver chain before hook emission. This keeps merge behavior explicit and replay-safe by defining precedence, merge policy classes, and stable ordering in one focused slice.

## PMG alignment

The project master goal requires a collaborative generation pipeline that accepts multi-actor intent without narrative hardcoding. This decision formalizes how competing intents are resolved safely and predictably before emission, which is necessary for trustable DM/player collaboration.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| --- | --- | --- | --- |
| Fold conflict policy into 2.2.2 | Fewer notes, faster short-term drafting | Blurs validate/classify and resolve responsibilities | Chosen split keeps deterministic resolver stages auditable and easier to hand off |
| Defer conflict policy to 2.2.4 emit stage | Simplifies current step | Emission would need implicit conflict behavior, risking nondeterministic coupling | Needed explicit pre-emit policy boundary first |
| Introduce weighted heuristic resolver now | Flexible tie-breaking | Reduces replay determinism and increases hidden policy drift | Deterministic rule matrix is safer at conceptual stage |

## Validation evidence

- Pattern evidence: deterministic policy-engine conflict routers with explicit precedence ladders and reason codes are a standard approach in staged intent systems.
- Internal artifact continuity: follows directly from [[Phase-2-2-2-Validate-Classify-Schema-and-Hook-Mapping-Roadmap-2026-03-31-0001]] outputs and parent [[Phase-2-2-Intent-Resolver-and-Hook-Mapping-Roadmap-2026-03-30-2310]] sequencing.

## Links

- Parent roadmap note: [[Phase-2-2-3-Conflict-Resolution-Priority-Ordering-and-Merge-Policy-Roadmap-2026-03-31-0002]]
- Prior slice: [[Phase-2-2-2-Validate-Classify-Schema-and-Hook-Mapping-Roadmap-2026-03-31-0001]]
- Queue entry: `resume-deepen-gmm-223-20260331T000200Z-forward`
