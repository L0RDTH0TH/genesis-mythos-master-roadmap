---
title: Phase 6.2.3 - Feedback promotion policy and contradiction-risk escalation templates
roadmap-level: tertiary
phase-number: 6
subphase-index: "6.2.3"
project-id: godot-genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 88
created: 2026-04-08
tags:
  - roadmap
  - godot-genesis-mythos-master
  - phase-6
para-type: Project
links:
  - "[[Phase-6-2-Scenario-Matrix-and-Feedback-Closure-Bundle-Roadmap-2026-04-08-1605]]"
  - "[[Phase-6-2-2-Transition-and-Rule-Outcome-Closure-Classification-Matrix-Roadmap-2026-04-08-1706]]"
  - "[[decisions-log]]"
  - "[[workflow_state]]"
---

## Phase 6.2.3 - Feedback promotion policy and contradiction-risk escalation templates

Third tertiary under 6.2. Defines the policy boundary between local clarification feedback and decisions-log promotion, including deterministic contradiction-risk escalation templates.

## Scope

In scope:
- Promotion policy from closure classes (`stable`, `needs_clarification`, `contradiction_risk`) into local note updates vs decisions-log entries.
- Contradiction-risk escalation templates with required fields, evidence minimums, and escalation ownership.
- Threshold wiring for 6.2 policy rows in decisions-log so policy choices are explicit and grep-stable.

Out of scope:
- Runtime queue automation for escalation handling.
- Execution-track CI enforcement of escalation deadlines.

## Behavior (natural language)

1. Every scenario-row outcome is classified via 6.2.2 before promotion decisions are evaluated.
2. `stable` outcomes remain local unless they change policy-level assumptions.
3. `needs_clarification` outcomes remain local for one bounded refinement pass; unresolved follow-up then escalates per threshold policy.
4. `contradiction_risk` outcomes immediately produce a decisions-log promotion using the escalation template.
5. Promotion entries always include source row id, evidence links, owning slice, and explicit next-action deadline.

## Interfaces

- Consumes closure classes and evidence requirements from [[Phase-6-2-2-Transition-and-Rule-Outcome-Closure-Classification-Matrix-Roadmap-2026-04-08-1706]].
- Writes promotion-ready decision rows into [[decisions-log]] with D-6.2 policy linkage.
- Feeds secondary 6.2 rollup criteria: all three tertiaries complete and policy thresholds wired.

## Edge cases

- A row marked `needs_clarification` with missing mandatory evidence is treated as `contradiction_risk` for promotion purposes.
- If transition and rule evidence disagree on closure confidence, escalation template must include both branches and the tie-break reference.
- Policy-row updates that alter thresholds require an explicit "Operator pick logged" amendment entry, not silent replacement.

## Open questions

None. Policy thresholds and escalation templates are now explicit for this conceptual slice.

## Pseudo-code readiness

Tertiary conceptual depth: escalation templates and thresholds are implementation-ready in natural language; executable workflow automation remains execution-track scope.

## Promotion and escalation template (canonical)

| Field | Requirement | Applies to |
| --- | --- | --- |
| `scenario_row_id` | required | all promoted rows |
| `closure_class` | required (`needs_clarification` or `contradiction_risk`) | all promoted rows |
| `evidence_links` | at least 2 links, one from 6.1.x or 6.2.x note | all promoted rows |
| `owner_slice` | required subphase index | all promoted rows |
| `next_action_deadline` | required for `contradiction_risk`; optional for first-pass `needs_clarification` | escalations |
| `threshold_trigger` | required when escalation is threshold-driven | escalations |

## Threshold policy (6.2 closure)

- `needs_clarification` may remain local for one rerun when evidence completeness is >= 80%.
- Any second unresolved `needs_clarification` rerun escalates as `contradiction_risk`.
- `blocked_by_missing_data` is treated as a constrained subclass of `needs_clarification` and escalates on first unresolved rerun.
