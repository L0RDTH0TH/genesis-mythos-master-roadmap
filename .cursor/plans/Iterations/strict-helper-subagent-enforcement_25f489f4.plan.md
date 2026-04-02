---
name: strict-helper-subagent-enforcement
overview: Tighten helper subagent enforcement so mandatory nested Task calls can never be skipped or misreported as success, and add bounded retry behavior to avoid false successes when helper channels are flaky.
todos:
  - id: tighten-contract
    content: Update Subagent-Safety-Contract and Nested-Subagent-Ledger-Spec to enforce mandatory helpers must end as invoked_ok or task_error, define helper retry semantics, and forbid Success when required helpers failed or were never attempted.
    status: pending
  - id: roadmap-helpers-enforce
    content: "Update RoadmapSubagent (agent and rule) to route all helper calls through a bounded-retry wrapper, record task_error for host failures, and downgrade overall status to #review-needed/failure whenever a mandatory helper cannot run."
    status: pending
  - id: other-pipelines-helpers-enforce
    content: Apply the same mandatory-helper enforcement pattern to ingest, archive, organize, distill, express, and research subagents, including pre-return helper integrity checks.
    status: pending
  - id: queue-gates-and-retries
    content: Tighten Layer1 queue strict_nested_return_gates to refuse Success when helper contracts are unsatisfied, and add helper-failure retry behavior with per-entry retry counters and clear Watcher/Errors logging.
    status: pending
  - id: config-and-docs
    content: Add and document configuration knobs for helper retry limits and strict helper enforcement, and update Queue-Sources and related docs to describe the new behavior.
    status: pending
isProject: false
---

## Goal

Ensure that when mandatory helper subagents (validator, internal-repair-agent, research) cannot run, pipeline subagents never report Success, and the queue never consumes those entries as successful, while adding bounded retries to ride out flaky Task environments.

## Key design decisions

- **Single source of truth**: Keep the **Subagent-Safety-Contract** as the authoritative place that defines "no helpers ⇒ no Success" and the helper retry semantics.
- **Two enforcement layers**:
  - **Layer 2 (pipeline subagents)**: must never emit green `little_val_ok: true` + Success when mandatory helper steps didn’t actually run as real `Task` calls.
  - **Layer 1 (queue)**: must refuse to mark entries as processed_success when nested ledger / `task_harden_result` indicate missing or failed mandatory helpers.
- **Retry semantics**:
  - **Within a single Task run**: helper subagent calls may be retried a small, bounded number of times when the failure is clearly transient (e.g. transport / timeout), but **not** when the host rejects the subagent type.
  - **Across queue runs**: queue may re-dispatch the same entry when the only failure cause was helper unavailability, using explicit retry counters and clear Watcher/Errors logs; never silently consume.

## Files to update

- **Contract & docs**
  - `[3-Resources/Second-Brain/Subagent-Safety-Contract.md]`: tighten language around mandatory helpers, outcome encoding (`task_error` vs `not_applicable`), and introduce explicit helper retry policy.
  - `[3-Resources/Second-Brain/Docs/Nested-Subagent-Ledger-Spec]`: clarify allowed `reason_code` values for `not_applicable` / `nested_cycle_exempt` and explicitly forbid using them for host Task failures.
  - `[3-Resources/Second-Brain/Queue-Sources.md]` and, if needed, `Pipeline-Validator-Profiles` docs: describe strict nested-return gates and helper-failure retry behavior.
- **Roadmap pipeline subagent**
  - `[.cursor/agents/roadmap.md]` and `[.cursor/rules/agents/roadmap.mdc]`:
    - Make the **pre-return honesty checklist** explicitly fail the run (status `#review-needed`/`failure`) when:
      - Any mandatory helper step (`nested_validator_first`, `nested_validator_second`, `ira_post_first_validator`, `research_pre_deepen`) lacks a ledger row, or
      - Has `outcome: not_applicable` / `nested_cycle_exempt` without an allowlisted `reason_code`, or
      - Has `outcome: skipped` with `task_tool_invoked: false` on a mandatory step.
    - Replace the current use of `nested_cycle_exempt` / `not_applicable` for host Task failures with `**task_error`** rows that must carry `host_error_class` and `host_error_raw`.
    - Add a small **helper-call retry loop** wrapper:
      - For each nested helper `Task` invocation, retry up to `N` times (configurable, e.g. 2–3) when the error class is transient (`resource_exhausted`, `unavailable`, `deadline_exceeded`), with short sleeps between attempts.
      - Do **not** retry when the host rejects the subagent type (`invalid_enum`, `nested_task_unavailable`); treat that as permanent and immediately mark `task_error`.
    - Ensure that when any mandatory helper ends in `task_error`, roadmap returns `#review-needed`/`failure` and **never** Success, even if filesystem work completed inline.
- **Other pipelines (ingest, archive, organize, distill, express, research)**
  - For each of `[.cursor/rules/agents/archive.mdc]`, `[.../organize.mdc]`, `[.../distill.mdc]`, `[.../express.mdc]`, `[.../ingest.mdc]`, `[.../research.mdc]` and the matching agent files under `.cursor/agents/`:
    - Mirror the roadmap tightening: mandatory helper steps must either be `invoked_ok` with `task_tool_invoked: true` or `task_error`; `not_applicable` / `skipped` are allowed only with allowlisted `reason_code`s.
    - Add a thin helper-call retry helper or reuse a shared pattern (pseudo-code referenced from Subagent-Safety-Contract) so each pipeline gets the same bounded-retry behavior.
    - Update each pipeline’s **pre-return check** to block Success when mandatory helper ledger rows are missing/invalid.
- **Queue subagent (Layer 1) strict gates & retries**
  - `[.cursor/rules/agents/queue.mdc]` and `[.cursor/agents/queue.md]`:
    - Strengthen `**queue.strict_nested_return_gates`** behavior to:
      - Treat any pipeline return as **non-success** when `task_harden_result.contract_satisfied === false` for a mandatory helper contract, or when nested ledger shows a forbidden `skipped` / `not_applicable` / missing row for a mandatory helper.
      - Explicitly refuse to add such entries to `processed_success_ids`, regardless of prose `status: Success`.
    - Add a **helper-failure retry policy** at the queue layer:
      - Detect runs whose only failure reason is helper unavailability (`host_error_class` like `nested_task_unavailable` / `invalid_enum` on helpers; primary pipeline work otherwise complete).
      - Keep those entries on disk with an incremented `helper_retries_used` (new JSONL field), bounded by `max_helper_retries_per_entry` in `Second-Brain-Config` (e.g. 2–3).
      - Log clear Watcher-Result and Errors.md entries when retries are scheduled and when the cap is exhausted.
    - Ensure that when retry caps are exceeded, the queue leaves the entry present but marked for manual intervention (e.g. `queue_failed: true` plus an Errors.md Decision Wrapper), never silently treating it as Success.
- **Config knobs**
  - Update `[3-Resources/Second-Brain/Second-Brain-Config.md]` and/or `[3-Resources/Second-Brain/Parameters.md]` to add:
    - `pipeline.helper_task_max_retries_per_run` (int, default small, e.g. 2).
    - `queue.max_helper_retries_per_entry` (int, default small, e.g. 2–3).
    - Optionally a feature flag like `queue.enforce_helper_failure_as_hard_error: true` (default on) to guard the rollout.

## Implementation steps

- **Step 1 – Tighten contract language**
  - Edit **Subagent-Safety-Contract** to:
    - Explicitly state that **required helpers must end as either `invoked_ok` or `task_error`**; `not_applicable`/`nested_cycle_exempt` are limited to concrete, pre-enumerated reasons that are never “Task tool unavailable”.
    - Define the **per-run helper retry policy** and map error classes (`invalid_enum`, `resource_exhausted`, etc.) to either permanent failure or transient retry.
    - Clarify that whenever a required helper finishes in `task_error`, the pipeline’s overall status must be `#review-needed`/`failure` and `little_val_ok: true` + Success is forbidden.
- **Step 2 – RoadmapSubagent enforcement & helper retry wrapper**
  - In `agents/roadmap.md`:
    - Introduce a small internal helper (conceptual or described in comments) that wraps nested `Task` invocations and implements the bounded-retry policy, annotating `host_error_class` / `host_error_raw` into the ledger.
    - Update all helper call sites (`nested_validator_first`, `ira_post_first_validator`, `nested_validator_second`, `research_pre_deepen`) to go through this wrapper.
    - Strengthen the **pre-return honesty checklist** so that any violation of the helper contract downgrades the run to `#review-needed`/`failure` regardless of prior behavior.
  - Mirror those enforcement bullets into `rules/agents/roadmap.mdc` so the rule file matches the agent behavior.
- **Step 3 – Extend the same pattern to other pipelines**
  - For ingest, archive, organize, distill, express, research:
    - Add a short **“Pre-return helper integrity”** subsection that says Success is illegal if mandatory helpers have missing/forbidden ledger states.
    - Require helper calls to go through the same bounded-retry wrapper defined at the contract level (even if just conceptually described there).
- **Step 4 – Queue strict nested-return gates & helper-failure retries**
  - In `rules/agents/queue.mdc`:
    - Expand the strict gates section so it checks both `task_harden_result` and `nested_subagent_ledger` for mandatory helper satisfaction before adding any id to `processed_success_ids`.
    - Document how to detect “pure helper failure” entries and how to increment retry counters / preserve them on disk.
  - In `agents/queue.md`:
    - Make the narrative for Pass 1/2/3 explicitly mention that helper-failure entries are never consumed, only retried or flagged.
- **Step 5 – Config and observability**
  - Add new config keys and briefly document them in `Second-Brain-Config` and `Parameters`.
  - Ensure that when helper failures or retry caps occur, the behavior is observable via:
    - Errors.md entries with `error_type: task_dispatch_failure` or `helper_unavailable`,
    - Watcher-Result `trace` tags like `mandatory_helper_unavailable=validator`,
    - `.technical/task-handoff-comms.jsonl` rows for the failed helper `Task` calls.

## Optional mermaid sketch (flow overview)

```mermaid
flowchart TD
  qEntry[queueEntry] --> l1Queue[Layer1 Queue]
  l1Queue -->|Task(roadmap)| l2Roadmap[RoadmapSubagent]
  l2Roadmap -->|nested Task(helper)| helper[Validator/IRA/Research]
  helper --> l2Roadmap
  l2Roadmap -->|ledger + task_harden_result| l1Queue
  l1Queue -->|if helpers ok| consume[mark processed_success]
  l1Queue -->|if helper task_error| retryOrFail[retry or leave entry]
```



## Todos

- **tighten-contract**: Update Subagent-Safety-Contract and Nested-Subagent-Ledger-Spec with strict helper requirements and retry semantics.
- **roadmap-helpers-enforce**: Apply the stricter helper handling and bounded retries to RoadmapSubagent (agent + rule).
- **other-pipelines-helpers-enforce**: Mirror the same enforcement pattern into ingest, archive, organize, distill, express, and research subagent rules/agents.
- **queue-gates-and-retries**: Strengthen queue strict nested-return gates and implement helper-failure retry behavior with clear logging.
- **config-and-docs**: Add config knobs and update reference docs (Queue-Sources, Parameters, Second-Brain-Config) to describe the new behavior.

