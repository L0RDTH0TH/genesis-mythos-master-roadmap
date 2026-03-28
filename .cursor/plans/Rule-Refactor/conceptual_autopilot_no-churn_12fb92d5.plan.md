---
name: Conceptual Autopilot No-Churn
overview: Implement a one-button conceptual autopilot where EAT-QUEUE can progress roadmap structure without repeated recal/repair churn unless hard blockers exist.
todos:
  - id: roadmap-policy-forward-precedence
    content: Implement conceptual forward-precedence policy in roadmap agent and roadmap rule, then sync roadmap rule copy.
    status: completed
  - id: queue-antichurn-guard
    content: Implement Layer 1 same-slice anti-churn append guard and sync queue rule copy.
    status: completed
  - id: config-defaults
    content: Set/confirm conceptual autopilot defaults and anti-churn thresholds in Second-Brain-Config.
    status: completed
  - id: docs-sync
    content: Update Parameters, Queue-Sources, Pipelines, verification checklist, and sync changelog.
    status: completed
  - id: verification-trace
    content: Validate with prompt-queue, watcher, decisions-log, and workflow_state traces against acceptance criteria.
    status: completed
isProject: false
---

# Conceptual Autopilot No-Churn Plan

## Goal

Make conceptual roadmap progression fully autonomous from EAT-QUEUE with strong forward bias: move to next structural node by default, treat recal as advisory except for hard blockers, and prevent same-slice queue churn.

## Scope

- Policy ownership in RoadmapSubagent (Layer 2).
- Enforcement guard in QueueSubagent (Layer 1).
- Config defaults aligned to forward-motion-first behavior.
- Docs/sync updates for long-term maintainability.

## Implementation Steps

1. **Codify forward-motion policy in RoadmapSubagent (primary logic)**

- Update [roadmap agent](/home/darth/Documents/Second-Brain/.cursor/agents/roadmap.md) to explicitly prioritize:
  - `deepen -> next_structural_target_hint` when conceptual slice is complete.
  - `advance-phase` when secondary completion is met.
  - recal only for hard blockers (`incoherence`, `contradictions_detected`, `state_hygiene_failure`, `safety_critical_ambiguity`).
- Ensure existing subphase-exit branch (3d) is authoritative over high-util recal tails for conceptual mode unless hard blockers exist.
- Add explicit queue continuation contract in return payload (`subphase_slice_exit_applied`, `next_subphase_index`, `suppress_followup=false` when next entry exists).

1. **Align roadmap rules to remove ambiguity**

- Update [roadmap rule](/home/darth/Documents/Second-Brain/.cursor/rules/agents/roadmap.mdc) to make conceptual forward-autopilot normative:
  - “No same-slice polish loops” rule.
  - “Advisory gaps do not block forward motion” rule.
  - Clear precedence order: hard blockers > slice-exit > high-util recal.
- Mirror changes in sync copy [sync roadmap rule](/home/darth/Documents/Second-Brain/.cursor/sync/rules/agents/roadmap.md).

1. **Add Layer 1 anti-churn enforcement guard (defense-in-depth)**

- Update [queue rule](/home/darth/Documents/Second-Brain/.cursor/rules/agents/queue.mdc) A.5c/A.5c.0:
  - Detect repeated same-subphase deepen/recal append attempts.
  - If Layer 2 already provided `next_subphase_index` or `subphase_slice_exit_applied`, preserve and prefer that over synthesized same-slice follow-ups.
  - If same-slice streak exceeds threshold and no hard blocker, reject same-slice append and synthesize next-node continuation from roadmap hints/state.
- Mirror to [sync queue rule](/home/darth/Documents/Second-Brain/.cursor/sync/rules/agents/queue.md).

1. **Tune defaults for one-button autonomy**

- Update [config](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain-Config.md) to favor movement by default on conceptual track:
  - Keep `roadmap.conceptual_subphase_exit_enabled: true`.
  - Keep `queue.conceptual_subphase_exit_l1_guard_enabled: true`.
  - Introduce/adjust conceptual anti-churn thresholds (same-subphase streak cap, recal suppression in conceptual mode unless hard blocker).
  - Ensure context-util recal settings do not override conceptual forward policy by default.

1. **Document policy contract and operator expectations**

- Update [Parameters](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Parameters.md) with a single normative precedence table for conceptual autopilot.
- Update [Queue-Sources](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Queue-Sources.md) for Layer 2 vs Layer 1 responsibility split.
- Update [Pipelines](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Pipelines.md) to state one-button EAT-QUEUE conceptual behavior.
- Update checklist [Conceptual-Autopilot-Verification-Checklist](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Docs/Conceptual-Autopilot-Verification-Checklist.md) with anti-churn acceptance tests.
- Append [sync changelog](/home/darth/Documents/Second-Brain/.cursor/sync/changelog.md).

1. **Verification plan (trace-based, no guessing)**

- Run a short controlled queue cycle and verify:
  - No same-subphase loop beyond configured limit.
  - At least one transition from current subphase to next structural target when slice predicate passes.
  - Recal appears only for hard blockers.
- Validate using:
  - [prompt queue](/home/darth/Documents/Second-Brain/.technical/prompt-queue.jsonl)
  - [watcher result](/home/darth/Documents/Second-Brain/3-Resources/Watcher-Result.md)
  - [decisions log](/home/darth/Documents/Second-Brain/1-Projects/genesis-mythos-master/Roadmap/decisions-log.md)
  - [workflow state](/home/darth/Documents/Second-Brain/1-Projects/genesis-mythos-master/Roadmap/workflow_state.md)

## Acceptance Criteria

- EAT-QUEUE-only operation advances conceptual structure without requiring user intervention for routine low/mid advisory gaps.
- Same-slice churn is bounded and automatically redirected to next structural target when eligible.
- Hard blockers still stop unsafe forward motion.
- Docs/rules/sync are aligned so behavior is stable across future edits.

