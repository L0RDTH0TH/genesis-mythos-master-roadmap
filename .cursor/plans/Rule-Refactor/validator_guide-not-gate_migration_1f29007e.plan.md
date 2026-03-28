---
name: Validator guide-not-gate migration
overview: Reclassify roadmap handoff validator output so missing artifacts produce non-blocking guidance (`needs_work`) and only true incoherence/safety failures trigger `block_destructive` (hard gate). Add structured reason codes + next-artifacts checklists so the validator expresses what it sees and what to do next.
todos:
  - id: contract-docs
    content: Update Validator-Reference contract to add needs_work and narrow block_destructive rubric.
    status: completed
  - id: validator-logic
    content: Update validator rule/prompt to emit needs_work for missing artifacts and reserve block_destructive for incoherence/safety/contradictions; add reason_codes + next_artifacts.
    status: completed
  - id: consumers
    content: Update roadmap/queue downstream wording and handling so needs_work is non-blocking; only high/block_destructive hard-gates.
    status: completed
  - id: tests
    content: Add/adjust validator tests for needs_work vs true block scenarios.
    status: completed
  - id: sync
    content: Sync changed rules into .cursor/sync and update any impacted docs references.
    status: completed
isProject: false
---

## Goals

- Make **validator a guide, not a gate** for roadmap handoff.
- Ensure `**block_destructive` is reserved** for true BLOCKs only: incoherence, contradictions, safety risk, or “validator has no clue what’s going on”.
- For coherent-but-incomplete plans (like your example), emit **non-blocking guidance** with explicit “what to write next” artifacts.

## Current behavior (what we’re migrating from)

- `roadmap_handoff_auto` is currently allowed to output `severity: high` + `recommended_action: block_destructive`, and downstream rules treat this as a hard stop (`#review-needed` / failure) even when the report is essentially “missing concrete artifacts”.
- Relevant references:
  - Validator contract: [3-Resources/Second-Brain/Validator-Reference.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Validator-Reference.md)
  - Validator implementation rule: [.cursor/rules/agents/validator.mdc](/home/darth/Documents/Second-Brain/.cursor/rules/agents/validator.mdc)
  - Example reports showing the problem: [.technical/Validator/roadmap-auto-validation-2026-03-18T103435Z.md](/home/darth/Documents/Second-Brain/.technical/Validator/roadmap-auto-validation-2026-03-18T103435Z.md), [.technical/Validator/roadmap-auto-validation-2026-03-18T103435Z--v2.md](/home/darth/Documents/Second-Brain/.technical/Validator/roadmap-auto-validation-2026-03-18T103435Z--v2.md)
  - Downstream “hard block” mapping appears in roadmap + pipeline rules (e.g. [.cursor/rules/agents/roadmap.mdc](/home/darth/Documents/Second-Brain/.cursor/rules/agents/roadmap.mdc)) and queue orchestration ([.cursor/rules/agents/queue.mdc](/home/darth/Documents/Second-Brain/.cursor/rules/agents/queue.mdc)).

## Target semantics (what we’re migrating to)

### 1) New action: `recommended_action: needs_work`

- Meaning: “Coherent, but not delegatable yet; next run should produce concrete artifacts.”
- Downstream behavior: treat as **severity: medium** equivalent (non-blocking), but it should **strongly guide** next steps.

### 2) Narrow definition for `block_destructive`

Per your selection (A): allow `severity: high` / `block_destructive` **only** when validator detects:

- Contradictions between phase notes/state/claims
- Safety-critical ambiguity / risk of destructive thrash
- Incoherent or un-restatable architecture (validator can’t reliably restate the system)
- Broken state hygiene severe enough to invalidate automation (e.g. metrics/data are inconsistent such that the system cannot safely progress)

Missing artifacts alone (ports/schemas/examples/tasks) must **not** trigger a block; it becomes `needs_work`.

### 3) Structured output for “express what it sees”

Add required structured sections to validator reports for roadmap handoff types:

- `reason_codes`: stable identifiers like `missing_port_signatures`, `missing_message_flow_example`, `missing_command_event_schemas`, `missing_task_decomposition`, `contradictions_detected`, `state_hygiene_failure`.
- `next_artifacts`: checklist items with “definition of done” that can be directly pasted into a roadmap note.

## Implementation work (files and changes)

### A) Update the canonical contract docs

- Update [3-Resources/Second-Brain/Validator-Reference.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Validator-Reference.md)
  - Add `needs_work` to the allowed `recommended_action` set.
  - Document the new rubric: `block_destructive` = true block only.
  - Specify `reason_codes` + `next_artifacts` as required fields for roadmap handoff reports.

### B) Update ValidatorSubagent behavior/spec

- Update [.cursor/rules/agents/validator.mdc](/home/darth/Documents/Second-Brain/.cursor/rules/agents/validator.mdc) and [.cursor/agents/validator.md](/home/darth/Documents/Second-Brain/.cursor/agents/validator.md)
  - In `roadmap_handoff` and `roadmap_handoff_auto` branches, explicitly map:
    - “missing concrete artifacts” → `severity: medium`, `recommended_action: needs_work`
    - “incoherent/contradiction/safety/state-hygiene failure” → `severity: high`, `recommended_action: block_destructive`
  - Require inclusion of `reason_codes` + `next_artifacts` in the written report.
  - Keep altitude-awareness, but treat altitude as affecting *what artifacts are demanded*, not whether it blocks.

### C) Update downstream consumers to understand `needs_work`

- Update roadmap + queue logic docs/rules so they don’t treat `needs_work` as a hard gate:
  - Roadmap rules: [.cursor/rules/agents/roadmap.mdc](/home/darth/Documents/Second-Brain/.cursor/rules/agents/roadmap.mdc) (and any mirrored agent docs) should state:
    - Only (`severity: high` OR `recommended_action: block_destructive`) stops “success”.
    - `needs_work` results in `#review-needed` (or success-with-review) but does **not** cause “block destructive roadmap actions” messaging.
  - Queue orchestration: [.cursor/rules/agents/queue.mdc](/home/darth/Documents/Second-Brain/.cursor/rules/agents/queue.mdc)
    - Ensure Watcher-Result messages differentiate:
      - BLOCK: “hard block due to incoherence/safety/contradictions”
      - NEEDS_WORK: “guidance: add artifacts X/Y/Z; continue non-destructive steps”

### D) Update tests and fixtures

- Update/extend [3-Resources/Second-Brain/Tests-Validator.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Tests-Validator.md)
  - Add a contract test scenario: coherent but underspecified roadmap → expect `needs_work` + reason_codes + next_artifacts.
  - Add a true-block scenario: contradiction/state-hygiene failure → expect `block_destructive`.

### E) Docs sync

Because this touches backbone components, sync updated rule text to:

- `.cursor/sync/rules/agents/validator.md` (from `.cursor/rules/agents/validator.mdc`)
- Any other changed rule mirrors under `.cursor/sync/…`

## Rollout / safety

- Ship as backward-compatible:
  - Consumers that don’t know `needs_work` can still treat it as “medium” by default.
  - Keep `create_wrapper` and `log_only` semantics unchanged.
- Validate by re-running a `roadmap_handoff_auto` check on `genesis-mythos-master`:
  - The same missing-artifact findings should now produce `needs_work` (non-blocking) and a concrete checklist.
  - Only if contradictions/safety issues exist should it block.

## Success criteria

- The same situation as your sample report no longer emits `block_destructive`.
- Watcher-Result and queue_failed_reason stop calling these “blocks”; they become “needs work” guidance.
- Validator reports consistently include `reason_codes` and `next_artifacts`, making next actions unambiguous.

