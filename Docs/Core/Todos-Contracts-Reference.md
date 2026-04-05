---
title: Todos, Nested Helpers, and Task Contracts
created: 2026-03-31
tags: [second-brain, todos, subagents, safety]
para-type: Resource
status: active
---

# Todos, Nested Helpers, and Task Contracts

### Purpose

Explain how **todo-orchestrator todos**, **nested_subagent_ledger**, and **Task-Handoff-Comms** fit together, and give a minimal audit path when a run feels wrong (e.g. RESUME_ROADMAP deepen that “did nothing”).

### 1. Mental model

- **Todos** (via `.cursor/skills/todo-orchestrator/SKILL.md`) track **run-level phases** for each subagent:
  - Queue: `parse-queue`, `dispatch-entries`, `log-watcher-result`, `rewrite-queue`.
  - Roadmap RESUME: `load-state`, `determine-action`, `apply-action`, `nested-helpers`, `snapshot-and-log`, `queue-followup-if-needed`.
  - Other pipelines: analogous small phase lists.
- **Nested helpers** (Validator, IRA, Research) are enforced by:
  - [[3-Resources/Second-Brain/Subagent-Safety-Contract|Subagent-Safety-Contract]] § Task-`attempt-before-skip` and nested-helper rules.
  - [[3-Resources/Second-Brain/Docs/Nested-Subagent-Ledger-Spec|Nested-Subagent-Ledger-Spec]] (attestation invariants; `task_tool_invoked`, `outcome`, `host_error_class`).
  - [[3-Resources/Second-Brain/Docs/Task-Handoff-Comms-Spec|Task-Handoff-Comms-Spec]] (paired `handoff_out` / `return_in` rows for each Task call).
- **Alignment**: a phase like `nested-helpers` is “done” only when the nested-helper contracts have either been satisfied (helpers really ran) or the run has been pushed into `#review-needed` / failure with honest `task_error` + ledger.

### 2. Minimal audit flow for a suspicious run

When a run seems like it lied (for example, EAT-QUEUE on a RESUME_ROADMAP deepen that reports Success but appears to have skipped helpers):

1. **Check todos for that subagent run**
   - For Queue: look for `queue-eat-queue:*` todos; for roadmap: `roadmap-resume:*`.
   - Confirm that all todos are `completed` or `cancelled`. If any are still `pending` / `in_progress`, the run exited early against todo-orchestrator’s contract.
2. **Check nested_subagent_ledger on the pipeline return**
   - For roadmap/ingest/archive/organize/distill/express/research:
     - Make sure `nested_subagent_ledger` exists when Success + `little_val_ok: true`.
     - Inspect `steps[]` for mandated helper `step` ids (`nested_validator_first`, `nested_validator_second`, `ira_post_first_validator`, `research_pre_deepen`) and verify:
       - `task_tool_invoked: true` with `outcome: invoked_ok`/`invoked_empty_ok`, **or**
       - `outcome: task_error` with non-empty `host_error_raw` / `host_error_class`.
     - Treat `outcome: skipped` + `task_tool_invoked: false` on a required helper as non-compliant unless `detail.reason_code` is one of the allowlisted material-gate / not-applicable codes.
3. **Check Task-Handoff-Comms for real Task calls**
   - In `.technical/task-handoff-comms.jsonl`, search for rows with:
     - `subagent_type: "roadmap"` for the pipeline itself, and
     - `subagent_type: "validator"`, `"internal-repair-agent"`, `"research"` for nested helpers.
   - Correlate via `task_correlation_id` / `parent_task_correlation_id` and `queue_entry_id` / `project_id` to the run you’re auditing.
   - Required helpers should have a `handoff_out` + `return_in` pair; absence of those when ledger claims `task_tool_invoked: true` is a structural bug.
4. **Interpretation**
   - If todos say `nested-helpers` is `completed` but there is:
     - no ledger, or
     - ledger shows required helpers only as `skipped` without Task attempts, and
     - Task-Handoff-Comms has no matching rows,
   - then that run violated its contracts even if it claimed Success; treat it as a target for repair (rules/agents) or for stricter `queue.strict_nested_return_gates`.

### 3. Where to look per layer

- **Layer 0 (chat)**:
  - Todos: usually not used directly; rely on queue/roadmap subagents.
  - Task-Handoff-Comms: `from_actor: "layer0_chat"`, `subagent_type: "queue"` for EAT-QUEUE / PROCESS TASK QUEUE.
- **Layer 1 (QueueSubagent)**:
  - Todos: `queue-eat-queue:parse-queue`, `:dispatch-entries`, `:log-watcher-result`, `:rewrite-queue` (see `todo-orchestrator` spec).
  - Task-Handoff-Comms: `from_actor: "layer1_queue"`, `subagent_type` = `roadmap`, `ingest`, `distill`, `express`, `archive`, `organize`, `research`, `validator`.
  - Nested-helper gates: `queue.strict_nested_return_gates` and its interaction with `processed_success_ids`.
- **Layer 2 (pipelines)**:
  - Todos: per-agent sections in `.cursor/agents/*.md`, now including `nested-helpers` for ROADMAP RESUME.
  - Nested ledger: `nested_subagent_ledger` on every run that mutates state and uses helpers.
  - Task-Handoff-Comms: `from_actor` like `layer2_roadmap`, `layer2_ingest`, etc., with `subagent_type` = helper name and `parent_task_correlation_id` = pipeline run’s `pipeline_task_correlation_id`.

Use this note as a quick checklist when you want to know “did this run really do everything it claimed?”, especially around nested helpers and EAT-QUEUE churn.

