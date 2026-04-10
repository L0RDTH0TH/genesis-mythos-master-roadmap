---
title: Phase 6.2.2 - Transition and rule-outcome closure classification matrix
roadmap-level: tertiary
phase-number: 6
subphase-index: "6.2.2"
project-id: godot-genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 87
created: 2026-04-08
tags:
  - roadmap
  - godot-genesis-mythos-master
  - phase-6
para-type: Project
links:
  - "[[Phase-6-2-Scenario-Matrix-and-Feedback-Closure-Bundle-Roadmap-2026-04-08-1605]]"
  - "[[Phase-6-1-3-ObservationChannel-Lane-Readout-and-Presentation-Time-Co-Display-Roadmap-2026-04-07-1015]]"
  - "[[Phase-5-1-3-Precedence-Conflict-Matrix-and-Cross-Seam-Resolution-Roadmap-2026-04-04-1209]]"
  - "[[workflow_state]]"
  - "[[decisions-log]]"
---

## Phase 6.2.2 - Transition and rule-outcome closure classification matrix

Second tertiary under 6.2. Defines deterministic closure classes for transition outcomes and rule-evaluation results so scenario rows can be graded without ambiguity.

## Scope

In scope:
- Closure classification matrix crossing transition outcome families with rule-outcome families.
- Deterministic class labels (`stable`, `needs_clarification`, `contradiction_risk`) and required evidence fields per class.
- Tie-break and precedence wording when transition and rule outcomes point to different closure classes.

Out of scope:
- Escalation/promotion templates for contradiction-risk outcomes (handled in 6.2.3).
- Runtime implementation of scoring or CI assertions.

## Behavior (natural language)

1. For each scenario row, classify transition outcomes and rule outcomes independently using canonical family labels.
2. Project the pair into the closure matrix to produce one provisional class.
3. Apply deterministic tie-break ordering so conflicting signals resolve to one final closure class.
4. Emit required evidence pointers and unresolved ambiguity tags before any "stable" classification is accepted.

## Interfaces

- Consumes `scenario_row_id` and baseline bindings from [[Phase-6-2-1-Scenario-Row-Identity-and-Admission-Tick-Baseline-Mapping-Roadmap-2026-04-08-1705]].
- Uses precedence vocabulary from [[Phase-5-1-3-Precedence-Conflict-Matrix-and-Cross-Seam-Resolution-Roadmap-2026-04-04-1209]] for rule-outcome conflict handling.
- Feeds closure class outputs into 6.2.3 promotion/escalation templates and decisions-log promotion thresholds.

## Edge cases

- Transition appears stable while rule outcome indicates nondeterministic ordering: classify as `contradiction_risk` unless tie-break evidence closes the gap.
- Missing evidence pointer for either dimension prevents `stable` and forces `needs_clarification`.
- Multi-lane observation disagreement with matching rule class still requires `needs_clarification` until lane parity evidence is attached.

## Open questions

- Should `needs_clarification` rows auto-expire to `contradiction_risk` after one unresolved rerun?
- Is a three-class matrix sufficient for late-phase closure, or is a fourth "blocked_by_missing_data" class needed?

## Pseudo-code readiness

Tertiary conceptual depth: matrix keys, tie-break order, and closure outputs are implementation-ready in natural language; executable scoring remains execution-track scope.

## Handoff gate status

This note is complete for the 6.2.2 scope only. Overall 6.2 closure handoff remains gated by [[Phase-6-2-Scenario-Matrix-and-Feedback-Closure-Bundle-Roadmap-2026-04-08-1605]] item `6.2.3`, which must define promotion and escalation templates before 6.2 can be treated as closure-ready.
