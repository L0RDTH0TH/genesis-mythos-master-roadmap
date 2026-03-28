---
name: Conceptual Forward Lube Patch
overview: Aggressively harden conceptual-track behavior so runs default to forward structural progress and must emit a concrete scaffold fallback when hard-blocked, while keeping execution gates advisory and preserving safety invariants.
todos:
  - id: patch-roadmap-rule
    content: Implement forward-first conceptual + mandatory scaffold fallback in roadmap rule
    status: completed
  - id: patch-queue-rule
    content: Adjust queue synthesis/repair policy to reduce conceptual recal churn
    status: completed
  - id: tune-config
    content: Add/tune conceptual-forward config knobs while preserving required decision records
    status: completed
  - id: update-docs
    content: Align Parameters, Queue-Sources, and Dual-Roadmap-Track docs with new behavior
    status: completed
  - id: sync-backbone
    content: Update .cursor/sync mirrors and changelog for modified rules
    status: completed
isProject: false
---

# Conceptual Forward-Lube Patch

## Goal

Make conceptual runs reliably move the roadmap forward (or produce a concrete scaffold in-note when blocked), instead of drifting into repeated hygiene/recal churn.

## Scope

- Behavioral policy hardening in queue + roadmap orchestration.
- Config defaults tuned toward conceptual forward momentum.
- Docs/rule-sync updates so behavior and reference stay aligned.

## Planned Changes

- Update [/.cursor/rules/agents/roadmap.mdc](/home/darth/Documents/Second-Brain/.cursor/rules/agents/roadmap.mdc)
  - Add explicit **forward-first conceptual** branching rule in smart dispatch:
    - Prefer `deepen` structural advancement for `effective_track: conceptual` unless true hard coherence blocker.
    - Prevent conceptual low-confidence from defaulting to repair loops.
  - Add **required fallback contract** for conceptual deepen:
    - If structural write is blocked by hard gate, must append a **mock scaffold** in the active phase note (sections, task list, acceptance criteria, artifact names).
    - Mark scaffold as conversion-ready for next run.
  - Add no-churn guard:
    - If repeated non-cursor-advance conceptual runs exceed threshold, force structural deepen attempt + scaffold fallback.
- Update [/.cursor/rules/agents/queue.mdc](/home/darth/Documents/Second-Brain/.cursor/rules/agents/queue.mdc)
  - Strengthen Layer-1 follow-up synthesis for conceptual track:
    - Avoid synthesizing recal/handoff-audit tails when `need_class` is structural and no hard blocker.
    - Bias synthesized `next_entry` toward structural deepen on conceptual.
  - Expand conceptual advisory skip behavior:
    - Ensure execution-debt primary codes remain advisory and do not trigger auto-repair churn on conceptual.
  - Add enforcement hook for scaffold fallback expectation in roadmap returns (message/rationale consistency checks before consumption in strict mode path).
- Update [/3-Resources/Second-Brain-Config.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain-Config.md)
  - Add/tune conceptual-forward knobs (new keys under `queue`/`roadmap`), e.g.:
    - max consecutive conceptual non-advance runs before forced structural/scaffold mode.
    - explicit conceptual forward-preference switch for follow-up synthesis.
  - Keep current `roadmap.conceptual_decision_record_mode: required`.
- Update docs to match behavior
  - [/3-Resources/Second-Brain/Parameters.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Parameters.md)
  - [/3-Resources/Second-Brain/Queue-Sources.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Queue-Sources.md)
  - [/3-Resources/Second-Brain/Docs/Dual-Roadmap-Track.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Docs/Dual-Roadmap-Track.md)
  - Document the new conceptual-forward/scaffold guarantees and anti-churn thresholds.
- Backbone sync obligations
  - Mirror rule edits to sync copies:
    - [/.cursor/sync/rules/agents/roadmap.md](/home/darth/Documents/Second-Brain/.cursor/sync/rules/agents/roadmap.md)
    - [/.cursor/sync/rules/agents/queue.md](/home/darth/Documents/Second-Brain/.cursor/sync/rules/agents/queue.md)
  - Add concise changelog entry in [/.cursor/sync/changelog.md](/home/darth/Documents/Second-Brain/.cursor/sync/changelog.md).

## Validation Plan

- Static validation:
  - Verify rule/docs language consistently states: conceptual = forward-first; execution debt advisory; scaffold fallback mandatory when blocked.
- Behavioral smoke-check (dry run by inspection):
  - Confirm a conceptual RESUME_ROADMAP with structural `need_class` would synthesize/return deepen-first continuation.
  - Confirm hard-block path requires scaffold emission contract rather than no-op repair churn.
- Queue consistency:
  - Ensure no conflict with `queue_next` contract and terminal suppress reasons.

## Risks & Mitigations

- Risk: Overriding legitimate coherence repairs.
  - Mitigation: Keep hard blocker set unchanged (`incoherence`, `contradictions_detected`, `state_hygiene_failure`, `safety_critical_ambiguity`) and only force forward behavior outside that set.
- Risk: Documentation drift after rule edits.
  - Mitigation: Update Parameters/Queue-Sources/Dual-Roadmap-Track + sync files in same patch.

