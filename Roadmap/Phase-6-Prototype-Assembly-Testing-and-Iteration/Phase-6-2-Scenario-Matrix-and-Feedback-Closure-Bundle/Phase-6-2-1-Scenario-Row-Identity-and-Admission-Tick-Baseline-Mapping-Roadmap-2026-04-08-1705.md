---
title: Phase 6.2.1 - Scenario row identity and admission/tick baseline mapping
roadmap-level: tertiary
phase-number: 6
subphase-index: "6.2.1"
project-id: godot-genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 86
created: 2026-04-08
tags:
  - roadmap
  - godot-genesis-mythos-master
  - phase-6
para-type: Project
links:
  - "[[Phase-6-2-Scenario-Matrix-and-Feedback-Closure-Bundle-Roadmap-2026-04-08-1605]]"
  - "[[Phase-6-1-1-Manifest-Field-Registry-FeedbackRecord-and-Instrumentation-Envelope-Roadmap-2026-04-07-1245]]"
  - "[[workflow_state]]"
  - "[[decisions-log]]"
---

## Phase 6.2.1 - Scenario row identity and admission/tick baseline mapping

First tertiary under 6.2. Establishes deterministic row identity and a shared admission-plus-tick baseline so every scenario run has the same vocabulary before closure classification.

## Scope

In scope:
- Scenario row identity tuple (`scenario_row_id`, admission path family, tick-window shape, transition class seed).
- Baseline mapping rules from each row into existing 6.1.x evidence references.
- Minimum row metadata required before a run may be marked closure-candidate.

Out of scope:
- Rule-outcome closure matrix decisions (handled in 6.2.2).
- Promotion/escalation policy wording for contradiction-risk outcomes (handled in 6.2.3).

## Behavior (natural language)

1. Define each scenario row using a stable identity tuple and a deterministic baseline field order.
2. Bind row identity to admission and tick-window baseline anchors so replay starts from a known state.
3. Require explicit evidence pointers before the row can participate in closure classification.

## Interfaces

- Consumes 6.1.x manifest and instrumentation vocabulary as reference anchors; does not redefine those terms.
- Provides deterministic row keys consumed by 6.2.2 classification and 6.2.3 escalation templates.
- Exposes read-only scenario descriptors for execution-track acceptance test intent.

## Edge cases

- Rows missing a tick baseline cannot be closure-candidate, even if operator notes look stable.
- Duplicate semantic rows with different labels must collapse to one canonical `scenario_row_id`.
- Admission paths that diverge from 2.7 assumptions require explicit contradiction-risk tagging.

## Open questions

- Should equivalent rows across neighboring tick windows share one canonical row id or remain separate?
- How much aliasing is acceptable before row identity becomes ambiguous for replay narratives?

## Pseudo-code readiness

Tertiary depth (mid-technical) only: deterministic interfaces and mapping rules are explicit enough for implementation sketching; executable pseudo-code remains execution-track work.
