---
name: internal-repair-agent-design
overview: Introduce a dedicated internal repair agent that pipelines can call once per run, after little val fails, to propose safe structural fixes without involving the queue.
todos:
  - id: ira-contract
    content: Define the Internal Repair Agent’s exact input/output schema and invariants (read-only, one call per run).
    status: pending
  - id: ira-roadmap-use
    content: Specify how roadmap subagent invokes IRA after little val failures and how suggested fixes are applied and re-checked.
    status: pending
  - id: ira-other-pipelines
    content: Outline how ingest, archive, organize, distill, and express use IRA for structural repair planning.
    status: pending
  - id: ira-observability
    content: Describe telemetry and logging conventions for IRA invocations and their interaction with pipeline logs.
    status: pending
isProject: false
---

## Internal Repair Agent (IRA) Design

### Role and scope

- **Purpose**: Act as a **dedicated internal repair agent** that pipeline subagents can call **once per run** when little val cannot achieve structural `ok` after its 3 attempts.
- **Focus**: Structural repair planning only (files, logs, snapshots, state notes); **no content-quality judgment**, no queue orchestration, no wrapper creation.
- **Callers**: Roadmap, Ingest, Archive, Organize, Distill, Express subagents.
- **Non-callers**: Queue agent (still orchestrates pipelines/validators), big Validator subagents (may remain queue-driven only).

### Contract and invariants

- **Inputs (from calling pipeline subagent)**
  - Run context:
    - `pipeline`: e.g. `roadmap`, `ingest`, `archive`, `organize`, `distill`, `express`.
    - `mode` and `params` for this run (e.g. `RESUME_ROADMAP` + `action: deepen`).
    - IDs: `queue_entry_id`, `project_id`, optional `parent_run_id`.
    - A short narrative of what the pipeline *intended* to do and what steps it has already taken.
  - Artifact pointers:
    - Paths to relevant notes/logs/state files (e.g. `workflow_state.md`, `roadmap-state.md`, `Ingest-Log.md`, target note path, snapshot paths).
    - The last little val verdict: `{ ok: false, missing: [...], hint: ... }` and any prior repair attempts.
- **Outputs (back to caller)**
  - A **repair plan object**, e.g.:
    - `status: "repair_plan" | "unrepairable"`.
    - `suggested_fixes:` structured steps (e.g. "append workflow_state row with fields X", "recompute context metrics for last entry", "insert missing Express-Log line with summary Y").
    - `rationale: string` explaining why these fixes are safe and sufficient.
    - Optional `risk_level` field (`low` / `medium` / `high`) so callers can decide whether to apply automatically or escalate.
  - A concise summary string for logs.
- **Hard invariants**
  - **Read-only on user artifacts**:
    - Internal Repair Agent (IRA) **must not** directly mutate notes, logs, roadmap-state, workflow_state, snapshots, or queues.
    - It can only: read those files and write its own **repair report note** (under a safe technical or roadmap-specific location) plus optional Run-Telemetry.
  - **No queue or wrapper manipulation**:
    - IRA never appends to `.technical/prompt-queue.jsonl`, `Task-Queue.md`, or `Watcher-Result.md`.
    - It never creates or modifies Decision Wrappers.
  - **Single invocation per pipeline run**:
    - Each pipeline run may call IRA at most **once**, and only after little val has failed all 3 of its attempts.
  - **Subagent nesting exception**:
    - Pipelines may call **only** this Internal Repair Agent as a nested subagent.
    - IRA itself may not call any other subagents; it may use skills (including little val core) internally.

### Interaction with little val and pipelines

- **Pipeline + little val loop**
  - Pipelines run their normal work, then:
    - Call little val skill and attempt up to **3 repairs** guided by `missing`/`hint`.
    - If little val eventually returns `ok: true` → pipeline returns `Success`.
    - If, after 3 attempts, little val still returns `ok: false` → pipeline labels the run as structurally problematic and may invoke IRA.
- **Pipeline + Internal Repair Agent flow**
  - When little val fails after its 3 attempts:
    - Pipeline calls IRA with full context and artifact paths.
    - IRA:
      - Re-runs the shared little val core logic in its own context to confirm the mismatch.
      - Analyses logs/state to suggest a minimal **repair plan** (usually 1–3 steps) tailored to this pipeline.
      - Returns `status: "repair_plan"` with `suggested_fixes` or `status: "unrepairable"`.
  - Pipeline receives the repair plan and decides:
    - For **low-risk, precise fixes** (e.g. writing a missing log line, recomputing missing metrics, updating a flag):
      - Apply them under existing safety gates (backups, snapshots) within the same run.
      - Call little val once more to confirm `ok: true`; on success, return `Success`.
    - For **medium/high-risk or ambiguous fixes**:
      - Do **not** auto-apply.
      - Mark run as `review needed`, attach IRA’s plan, and let you decide or re-queue with explicit params.
  - If, after applying IRA’s low-risk plan and one more little val check, the structure is still not `ok`:
    - Pipeline marks the run as `**true failure` / `unrepairable`** and logs a clear explanation referencing the IRA report.

### Per-pipeline use patterns

- **Roadmap**
  - IRA focuses on:
    - malformed or missing `workflow_state` rows,
    - context-tracking fields inconsistencies,
    - roadmap-state phase mismatches.
  - Suggested fixes might include:
    - recomputing and rewriting the last Log entry,
    - adding missing metrics from workflow_state context,
    - recommending rollback to the last safe phase if state is too tangled.
- **Ingest / Archive / Organize**
  - IRA helps when:
    - logs do not match actual moves/renames,
    - snapshots/backup flags are missing for destructive actions,
    - para-type or path metadata and actual locations disagree.
- **Distill / Express**
  - IRA proposes repairs when:
    - distill layers or TL;DR are partially written,
    - version snapshot exists but logs don’t, or vice versa,
    - Related/outline sections are inconsistent with frontmatter or markers.

### Relationship to big Validator and audits

- **Big Validator (quality)**
  - Remains queue-dispatched and focuses on content quality (handoff readiness, readability, express summary quality).
  - May **consult little val core** to ensure structural soundness before rating quality.
  - Does not handle structural repair; it can, however, point to IRA reports when structure is blocking quality.
- **Audit flows**
  - For runs that ended as **true failure/unrepairable**, you can:
    - Use a dedicated audit mode that:
      - Reads IRA’s report,
      - Performs a higher-level review,
      - Possibly enqueues follow-up work or manual remediation tasks.

### Observability and safety

- **Telemetry**
  - IRA writes its own Run-Telemetry notes (`actor: internal-repair-agent`) for each invocation, linked via `parent_run_id` to the pipeline run.
  - Pipelines annotate their logs with flags such as:
    - `ira_invoked: true`, `ira_plan_applied: true|false`, `ira_status: repair_plan|unrepairable`.
- **Error handling**
  - If IRA cannot produce a coherent repair plan, it returns `status: "unrepairable"` with a detailed rationale; the pipeline treats this as a strong signal to mark the run as **true failure**.
  - IRA must never silently ignore structural inconsistencies; all non-`ok` outcomes should be explained in its report.

### Summary of the tiered repair architecture

- **Tier 1**: Pipeline logic (normal steps).
- **Tier 2**: little val skill (up to 3 self-repair attempts per run).
- **Tier 3**: Internal Repair Agent (once per run, proposes low-risk fixes; pipeline may apply and re-check with little val).
- **Tier 4**: If structure is still not `ok`, mark as **true failure/unrepairable** and rely on human or future audit flows.

This keeps subagent orchestration simple (only a single nested repair agent), preserves queue as the sole owner of queues/wrappers/watcher logs, and cleanly separates structural repair (pipeline + IRA) from quality validation (big Validator).