---
name: Conceptual Spin-Break Enforcement
overview: Add a narrow conceptual-track escalation for repeated medium-gap churn so Layer 1 forces named artifact materialization and movement, while preserving existing hard-block safety and execution-track strictness.
todos:
  - id: patch-queue-rule
    content: Add repeated-medium-gap escalation in A.5b to force named artifact build on conceptual
    status: completed
  - id: tune-config-thresholds
    content: Add config knobs for medium-gap escalation threshold and conceptual force-build toggle
    status: completed
  - id: docs-targeted-update
    content: Update Queue-Sources and Parameters with the new escalation branch and defaults
    status: completed
  - id: optional-followup
    content: Defer broader roadmap/doc-sync rewrites unless escalation alone fails in practice
    status: completed
isProject: false
---

# Conceptual Spin-Break Enforcement Plan (Narrow Escalation)

## Goal

Break repeated conceptual medium-gap churn by forcing targeted materialization of named missing artifacts, instead of generic recal loops.

## Scope

- Global for conceptual track only.
- Keep execution-track behavior unchanged (manual/strict gate closure remains).
- Target only repeated medium-gap cases (`safety_unknown_gap`, `missing_roll_up_gates`) with no true hard block.

## Implementation Steps

- Update A.5b in [.cursor/rules/agents/queue.mdc](/home/darth/Documents/Second-Brain/.cursor/rules/agents/queue.mdc):
  - Add a new branch (e.g. `A.5b.5`) for conceptual repeated-medium-gap escalation.
  - Trigger when all hold: `effective_track == conceptual`, primary_code in `safety_unknown_gap|missing_roll_up_gates`, same-spine streak `>= threshold`, and no hard-block code.
  - Override generic repair context to force named materialization from validator report (`G-P4.1-ROLLUP-GATE-02` class artifacts + CI stub evidence + witness appendix), set `queue_priority: repair`, and suppress generic recal-only fallback.
- Tune config in [3-Resources/Second-Brain-Config.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain-Config.md):
  - Add `queue.conceptual_force_build_on_repeated_gap: true`.
  - Add `queue.medium_gap_escalation_threshold: 4` (default), with local override option for stricter operation.
  - Keep existing hard-block/tiered-validator settings unchanged.
- Minimal docs update (only behavior surface touched):
  - [3-Resources/Second-Brain/Queue-Sources.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Queue-Sources.md): document repeated-medium-gap escalation path and fields.
  - [3-Resources/Second-Brain/Parameters.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Parameters.md): document new config knobs and trigger semantics.
- Defer broader roadmap-rule rewrites and sync churn unless this narrow fix fails in smoke tests.

## Validation

- Contract checks:
  - Medium-gap repeats on conceptual no longer generate generic recal churn once threshold is met.
  - Hard-block set still follows existing block/repair semantics with no relaxation.
- Queue behavior checks:
  - Escalation line includes explicit named-artifact build intent from validator context.
  - Follow-up is repair-priority and avoids same-locus recal-only recursion.
- Smoke checks:
  - Repeated `missing_roll_up_gates` / `safety_unknown_gap` on the same spine triggers force-build escalation by threshold.
  - Execution-track behavior remains unchanged.

