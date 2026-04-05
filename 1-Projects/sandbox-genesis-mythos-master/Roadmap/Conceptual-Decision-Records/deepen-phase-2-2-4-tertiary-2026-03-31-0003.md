---
title: Conceptual decision record — deepen phase 2.2.4 tertiary
created: 2026-03-31
tags:
  - roadmap
  - conceptual-decision-record
  - sandbox-genesis-mythos-master
para-type: Project
project-id: sandbox-genesis-mythos-master
parent_roadmap_note: "[[Phase-2-2-4-Deterministic-Hook-Emission-Envelope-and-Pre-Commit-Payload-Handoff-Roadmap-2026-03-31-0003]]"
decision_kind: deepen
queue_entry_id: resume-deepen-gmm-224-20260331T000300Z-forward
master_goal: "[[Source-sandbox-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

## Summary

Selected a deterministic hook-emission tertiary immediately after conflict-resolution policy. This keeps emission and pre-commit handoff explicit, so merge outcomes are translated into stable payload envelopes without crossing the commit boundary.

## PMG alignment

The project master goal depends on collaborative DM/player intent becoming reliable world-generation inputs. This decision formalizes the resolver-to-pre-commit handoff so collaboration remains deterministic, replay-safe, and auditable before commit-path effects.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| --- | --- | --- | --- |
| Fold emission handoff into 2.2.3 | Fewer artifacts and quicker drafting | Blurs resolve-policy and emit-envelope responsibilities | Chosen split keeps deterministic stage boundaries auditable |
| Push pre-commit handoff to execution track only | Less conceptual detail now | Leaves an ambiguity at the critical resolve -> emit boundary | Needed explicit boundary now to avoid hidden coupling |
| Emit directly to commit-ready payloads | Simpler apparent pipeline | Risks side-effect leakage and weaker validation isolation | Pre-commit bundle boundary is safer and more testable |

## Validation evidence

- Pattern evidence: staged policy pipelines use deterministic emission envelopes and pre-commit validation bundles to isolate side effects.
- Internal continuity: follows directly from [[Phase-2-2-3-Conflict-Resolution-Priority-Ordering-and-Merge-Policy-Roadmap-2026-03-31-0002]] and preserves parent [[Phase-2-2-Intent-Resolver-and-Hook-Mapping-Roadmap-2026-03-30-2310]] sequencing.

## Links

- Parent roadmap note: [[Phase-2-2-4-Deterministic-Hook-Emission-Envelope-and-Pre-Commit-Payload-Handoff-Roadmap-2026-03-31-0003]]
- Prior slice: [[Phase-2-2-3-Conflict-Resolution-Priority-Ordering-and-Merge-Policy-Roadmap-2026-03-31-0002]]
- Queue entry: `resume-deepen-gmm-224-20260331T000300Z-forward`
