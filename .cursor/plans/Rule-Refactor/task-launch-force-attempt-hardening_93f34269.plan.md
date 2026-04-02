---
name: task-launch-force-attempt-hardening
overview: Harden Task-based subagent launching so that required subagents are always actually invoked (or produce explicit task_error), focusing on Layer 0→Queue, Queue→pipeline, and Roadmap→nested helpers.
todos:
  - id: define-global-attempt-before-skip
    content: Add a concise attempt-before-skip invariant and reusable Task preamble to Subagent-Safety-Contract, referenced by other docs.
    status: completed
  - id: tighten-layer0-to-queue-contract
    content: Update dispatcher and queue agent docs so EAT-QUEUE/PROCESS TASK QUEUE always use Task(subagent_type="queue") with no inline fallback.
    status: completed
  - id: harden-queue-to-pipeline-dispatch
    content: Update queue rules/agent to require real Task calls for all pipeline modes and tie them to Task-Handoff-Comms entries.
    status: completed
  - id: harden-roadmap-nested-helpers
    content: Update roadmap agent + Nested-Subagent-Ledger-Spec so required helper steps must issue Task calls and record task_error on failure.
    status: completed
  - id: extend-task-handoff-comms-audit
    content: Extend Task-Handoff-Comms-Spec with compliance checks linking mandated Task calls to comms records.
    status: completed
  - id: phase-rollout-and-tests
    content: Plan phased rollout (roadmap + queue first) and manual EAT-QUEUE tests to verify Task calls are always attempted and logged.
    status: completed
isProject: false
---

# Task Launch Force-Attempt Hardening

### Goal

Make runs more consistent by **forcing real Task invocations** for required subagents (queue, roadmap, validator, internal-repair-agent, research), and by wiring those attempts into existing logging so "we thought it was unavailable" cannot silently skip work.

### 1. Add a global "attempt-before-skip" invariant

- **Update** `3-Resources/Second-Brain/Docs/Subagent-Safety-Contract.md` with a short, normative section:
  - When a run contract says a subagent **must** be called (Queue→pipeline, Roadmap→validator/IRA/research, etc.), callers **must attempt** a real `Task` call with the intended `subagent_type`.
  - It is **forbidden** to skip a mandated helper based on schema introspection alone; the only allowed non-call outcome is a real Task error, surfaced as `task_error` with `host_error_class` and logged.
  - Make this invariant reference `Task-Handoff-Comms-Spec` and `Nested-Subagent-Ledger-Spec` so audits can rely on it.

### 2. Standardize a force-attempt preamble for Task prompts

- **Define once** in Subagent-Safety-Contract a reusable snippet for Task prompts, e.g.:
  - "You MUST treat yourself as having been launched via Cursor Task with `subagent_type: <X>`. Do NOT claim Task or this subagent type is unavailable; if anything fails, report a concrete error instead of pretending the call never happened."
- **Do not** duplicate the full text everywhere; instead, have each agent file refer to this standard preamble when describing its Task hand-offs.

### 3. Tighten Layer 0 → QueueSubagent contract

- **Dispatcher rule** (`.cursor/rules/always/dispatcher.mdc`):
  - Explicitly require that EAT-QUEUE / PROCESS TASK QUEUE always call `Task(subagent_type="queue")` with a full hand-off and never run queue logic inline.
  - State that Layer 0 must not conclude that `subagent_type: queue` is unavailable; it must attempt Task and handle only real errors.
- **Queue agent doc** (`.cursor/agents/queue.md`):
  - Under "Entry conditions and hand-off contract", add a short "Task launch contract" bullet that mirrors the dispatcher language and references the global preamble.

### 4. Harden QueueSubagent → pipeline Task dispatch

- **Queue rules** (`.cursor/rules/agents/queue.mdc` A.5.0/A.5c) and `queue.md`:
  - For each pipeline mode (INGEST_MODE, ROADMAP_MODE, RESUME_ROADMAP, DISTILL_MODE, EXPRESS_MODE, ARCHIVE MODE, ORGANIZE MODE, RESEARCH_AGENT, VALIDATE, ROADMAP_HANDOFF_VALIDATE):
    - Require a real `Task` invocation with the matching `subagent_type` (ingest, roadmap, distill, express, archive, organize, research, validator).
    - Forbid skipping these calls based on perceived schema limits; any real Task failure must be surfaced as a Watcher-Result failure + Errors.md entry, leaving the queue line unconsumed.
  - Tie dispatch compliance to **Task-Handoff-Comms**:
    - For each processed queue entry with pipeline mode, there **must** be a `handoff_out`/`return_in` pair in `.technical/task-handoff-comms.jsonl` with `subagent_type` equal to the intended pipeline name and a `task_correlation_id` recorded as `pipeline_task_correlation_id` in the roadmap/other subagent hand-off.

### 5. Harden RoadmapSubagent → nested helper Task calls

- **Roadmap agent doc** (`.cursor/agents/roadmap.md`):
  - In the sections for `research_pre_deepen`, `nested validator (roadmap_handoff_auto)`, and `internal-repair-agent`:
    - Add a concise rule: when a helper step is **required** by the run contract, Roadmap **must** call `Task` with `subagent_type: research|validator|internal-repair-agent`.
    - Forbid ledger entries like `outcome: skipped` with `task_tool_invoked: false` on mandated steps; require `outcome: task_error` with concrete `host_error_class` when Task fails.
  - Reuse the global preamble by name so the nested helper prompts contain the same force-attempt semantics.
- **Nested-Subagent-Ledger-Spec**:
  - Clarify that certain step IDs (research_pre_deepen, nested_validator_first, nested_validator_second, ira_post_first_validator) are "must-attempt" when active, and that compliance requires a corresponding Task-Handoff-Comms pair.

### 6. Make Task-Handoff-Comms the audit spine

- **Task-Handoff-Comms-Spec**:
  - Add a "Compliance checks" section:
    - For any run where a Task call is mandated, there must be at least one `handoff_out`/`return_in` record in `.technical/task-handoff-comms.jsonl` with the correct `subagent_type` and matching `task_correlation_id`/`parent_task_correlation_id`.
    - Absence of such records when a ledger step claims `task_tool_invoked: true` is a structural contract violation.
  - Optionally define simple helper queries or fields (`host_error_class`) to distinguish genuine Task failures from missing attempts.

### 7. Rollout order and verification

- **Phase 1 — Roadmap and Queue only**:
  - Implement the above changes for:
    - Layer 0 → Queue, Queue → Roadmap, Roadmap → validator/IRA/research.
  - Run a few controlled EAT-QUEUE passes and manually inspect:
    - That every RESUME_ROADMAP entry that claims to have run nested helpers has matching Task-Handoff-Comms rows.
    - That no run reports conceptual deepen success without a corresponding Task record for roadmap and required helpers.
- **Phase 2 — Extend to other pipelines**:
  - Apply the same pattern to ingest, distill, express, archive, organize subagents where they spawn validator/IRA/research helpers.
- **Phase 3 — Add lightweight error surfacing**:
  - When a run fails solely because Task calls errored (e.g. missing subagent type), ensure Errors.md entries clearly name `host_error_class` and recommend operator fixes, without silently consuming queue entries.

### 8. Keep the plan small and enforceable

- Focus edits on **three doc clusters** only:
  - Subagent-Safety-Contract (global invariant + preamble),
  - Queue + roadmap agent/rule files (concrete callers),
  - Task-Handoff-Comms-Spec + Nested-Subagent-Ledger-Spec (audit and attestation).
- Avoid broad refactors elsewhere; rely on these tightened contracts and logging to make "we skipped the Task call" practically impossible without being caught.

