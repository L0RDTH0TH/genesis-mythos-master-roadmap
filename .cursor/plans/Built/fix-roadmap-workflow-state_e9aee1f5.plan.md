---
name: fix-roadmap-workflow-state
overview: Diagnose why RESUME-ROADMAP deepen created new roadmap notes but did not update workflow_state.md, ensure research-agent integration behaves per specs, and harden roadmap automation against silent failures.
todos:
  - id: inspect-current-roadmap-state
    content: Inspect current workflow_state.md and roadmap-state.md for genesis-mythos-master and compare with created Phase-1.1 notes.
    status: completed
  - id: map-deepen-responsibilities
    content: Map roadmap-deepen and auto-roadmap specs to the required workflow_state updates and postconditions.
    status: completed
  - id: design-deepen-state-fix
    content: Design concrete changes so roadmap-deepen always updates workflow_state (iterations, subphase index, context metrics, log row) or logs an explicit error instead of silently succeeding.
    status: completed
  - id: strengthen-resume-roadmap-contract
    content: Define and apply an end-of-run self-audit for RESUME-ROADMAP to detect and log silent failures.
    status: completed
  - id: audit-research-agent-integration
    content: Confirm when research-agent-run should execute, why it has not run yet in this project, and plan tests to validate its behavior at depth ≥ 2.
    status: completed
  - id: scan-related-roadmap-actions
    content: Scan other roadmap actions (advance-phase, recal, expand, etc.) for similar silent-failure risk and summarize required safeguards.
    status: completed
isProject: false
---

## Fix roadmap workflow_state & research integration

### 1. Confirm current state and failure pattern

- **Inspect workflow_state.md** at `1-Projects/genesis-mythos-master/Roadmap/workflow_state.md` to verify it only contains the initial Phase 0 log row and unchanged `iterations_per_phase` / `current_subphase_index` despite new Phase 1.1 notes.
- **Inspect roadmap-state.md** at `1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md` to confirm Phase/Status frontmatter and see whether it advanced or logged runs correctly.
- **Cross-check created notes** (e.g. `Phase-1-1-Core-Abstractions-Roadmap-2026-03-10-1200.md` and the `Phase-1-1-{1,2,3}-*.md` tertiaries) to ensure the deepen step really executed and matches `Roadmap Structure.md`.
- **Verify logs and errors** in `3-Resources/Backup-Log.md` and `3-Resources/Second-Brain/Mode-Success-Contracts.md` to confirm that snapshots ran but no error entry was recorded for this RESUME-ROADMAP run.

### 2. Identify the missing workflow_state update responsibilities

- **Re-read `roadmap-deepen` skill** to list its explicit responsibilities for state: updating `iterations_per_phase`, `current_subphase_index`, `last_ctx_util_pct`, and appending a new 11-column log row in `workflow_state.md` for every successful deepen.
- **Re-read `auto-roadmap` rule (RESUME-ROADMAP section)** to confirm the postcondition that every deepen run must end in exactly one of: state advance, queue append, Decision Wrapper, or high-severity error.
- **Compare these specs to observed behavior** (notes created with no workflow_state changes and no errors) and document this as a "silent failure" per Mode-Success-Contracts.

### 3. Plan concrete fixes to roadmap-deepen behavior

- **Ensure workflow_state writes are mandatory for successful deepens**: after creating secondary/tertiary/task notes, always:
  - Increment `iterations_per_phase[current_phase]`.
  - Set `current_subphase_index` to the new target (e.g. `"1.1"`, `"1.1.1"`).
  - Compute context utilization (`context_util_pct`, `leftover_pct`, `Threshold`, `Est. Tokens / Window`) when `params.enable_context_tracking` is true and write them into the new log row.
  - Append the 11-column log row under `## Log` with an appropriate `Status / Next` description (including gaps / research_used when applicable).
  - Update workflow_state frontmatter `last_ctx_util_pct` to match the new row.
- **Add explicit error behavior when state cannot be updated**:
  - If any of the required metrics cannot be computed while `enable_context_tracking` is true, do not append a partial row with `"-"`; instead, log an `error_type: context-tracking-missing` entry in `3-Resources/Errors.md` and surface `#review-needed`, then treat the deepen as failed so auto-roadmap can mark the queue entry as `queue_failed: true`.
  - Ensure that in this failure path, no new roadmap content is written (or at minimum, document and guard against partial writes), keeping state and content in sync.

### 4. Harden RESUME-ROADMAP success contract and self-audit

- **Implement an end-of-run self-audit for RESUME-ROADMAP**:
  - After each RESUME-ROADMAP run, re-read `roadmap-state.md` and `workflow_state.md` and verify that the run ended in one of the allowed outcomes (advance, follow-up queue, wrapper, or error).
  - When roadmap content changed (new notes/folders) but neither state nor queue nor wrappers nor errors changed, log an explicit error entry in `Errors.md` referencing this as a silent failure and tag it `#review-needed`.
- **Align any existing automation code with `Mode-Success-Contracts.md`** to avoid future silent failures for roadmap actions.

### 5. Verify research-agent integration behavior

- **Confirm that research-agent-run has not yet executed** by checking for an `Ingest/Agent-Research/` folder and any `#research-failed` / `#research-empty` entries; this should explain why no research notes exist yet.
- **Cross-check Parameters and auto-roadmap gating** to verify that:
  - Util-based pre-deepen research and gap-fill research only run when `current_depth ≥ 2`.
  - Primary phase containers at depth 1 (your current position) do not auto-trigger research, so the absence of research is expected unless `enable_research` was explicitly set.
- **Plan explicit tests** for later (outside Plan mode): issue RESUME-ROADMAP deepen runs with `enable_research: true` at depth ≥ 2 and ensure that:
  - `research-agent-run` writes notes under `Ingest/Agent-Research/`.
  - Those paths or summaries are propagated into roadmap-deepen and reflected in workflow_state (e.g. via `research_used` and gap summaries in the log).

### 6. Scan for similar failure points in roadmap pipelines

- **Review roadmap-related specs** (`Roadmap-Upgrade-Plan.md`, `Pipelines.md`, `Mode-Success-Contracts.md`) to identify other places where content changes are allowed but state/queue/wrapper/error updates are mandatory (e.g. `advance-phase`, `recal`, `expand`).
- **List each roadmap action (deepen, advance-phase, recal, expand, handoff-audit, revert-phase, sync-outputs)** with its required state/logging side effects and verify that their current descriptions avoid silent failure patterns.
- **Document a short checklist** to use when implementing or debugging roadmap actions: "Did state advance? Did we queue follow-up? Did we create/update a wrapper? Did we log a high-severity error?" to make future regressions less likely.

