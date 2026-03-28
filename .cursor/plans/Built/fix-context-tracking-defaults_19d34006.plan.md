---
name: fix-context-tracking-defaults
overview: Investigate why the latest RESUME-ROADMAP deepen run wrote workflow_state log rows with dashes instead of context metrics despite enable_context_tracking being true by default, and adjust roadmap-deepen plus auto-roadmap so context tracking is reliably computed and validated without breaking other roadmap behaviors.
todos:
  - id: reconfirm-failure-row
    content: Reconfirm the latest workflow_state log row and corresponding RESUME-ROADMAP queue entry to characterize the context-tracking failure pattern.
    status: completed
  - id: analyze-deepen-vs-auto-roadmap-specs
    content: Analyze roadmap-deepen and auto-roadmap specs to map who is responsible for computing context metrics vs validating them.
    status: completed
  - id: design-deepen-metric-computation-fix
    content: Design concrete changes so roadmap-deepen always computes and writes context metrics when enable_context_tracking is true or fails cleanly without writing content.
    status: completed
  - id: design-auto-roadmap-postcondition-fix
    content: Design concrete changes to auto-roadmap’s postcondition so any missing or dash context metrics with tracking enabled are always treated as errors, not silent successes.
    status: completed
  - id: audit-other-roadmap-actions
    content: Audit other roadmap actions (advance-phase, recal, expand, etc.) to ensure they are not broken by stricter context-tracking behavior and still meet Mode-Success-Contracts.
    status: completed
  - id: plan-validation-runs
    content: Plan targeted RESUME-ROADMAP tests (with tracking on/off and simulated failures) to validate that context tracking and error handling behave as expected after code changes.
    status: completed
isProject: false
---

## Fix roadmap context-tracking defaults

### 1. Confirm the failure mode

- **Inspect the latest workflow_state log row** in `[1-Projects/genesis-mythos-master/Roadmap/workflow_state.md](/home/darth/Documents/Second-Brain/1-Projects/genesis-mythos-master/Roadmap/workflow_state.md)` and note that:
  - `current_subphase_index` has advanced to `"1.1"` and `iterations_per_phase["1"]` is `1`,
  - But the corresponding `## Log` row for `2026-03-10 12:05` has `Ctx Util %`, `Leftover %`, `Threshold`, and `Est. Tokens / Window` all set to `-` even though the queue entry had `enable_context_tracking: true`.
- **Confirm the triggering queue entry** in `[.technical/prompt-queue.jsonl](/home/darth/Documents/Second-Brain/.technical/prompt-queue.jsonl)` (`id: "resume-20260310-1240"` or the most recent RESUME-ROADMAP) and verify that `params.enable_context_tracking` was true or undefined (so it defaults to true per `auto-roadmap.mdc`).
- **Verify that no error was logged** for this run in `3-Resources/Errors.md`, confirming that auto-roadmap’s postcondition check for missing context metrics did not fire even though the row contains `-`.

### 2. Map responsibilities and identify the gap

- **From `roadmap-deepen`** (`[.cursor/skills/roadmap-deepen/SKILL.md](/home/darth/Documents/Second-Brain/.cursor/skills/roadmap-deepen/SKILL.md)`):
  - Note that it declares an invariant: when `params.enable_context_tracking` is true, it *must* compute non-`"-"` values for the four context columns and append a complete 11-column log row.
  - It also defines how to estimate `estimated_tokens`, derive `context_util_pct` and `leftover_pct`, and write them into the log.
- **From `auto-roadmap*`* (`[.cursor/rules/context/auto-roadmap.mdc](/home/darth/Documents/Second-Brain/.cursor/rules/context/auto-roadmap.mdc)`):
  - Confirm that after a deepen run it re-reads the last workflow_state row and, when `effective_enable_context_tracking` is true and any of the four context fields are `"-"` or invalid, it must log `context-tracking-missing`, mark the queue entry as `queue_failed: true`, and not clear it.
- **Compare this spec to the observed state**:
  - The deepen run advanced iteration and subphase index but inserted `-` into context fields **and** auto-roadmap did not treat it as an error, so there is a coordination gap: either roadmap-deepen is not computing metrics when it should, or auto-roadmap’s postcondition check is not correctly triggered for this project.

### 3. Plan changes to roadmap-deepen to always compute metrics when tracking is enabled

- **Enforce a strict ordering in the skill implementation**:
  - After reading `workflow_state.md`, `roadmap-state.md`, and any additional context (distilled-core, decisions-log, phase notes), the code must:
    - Compute `total_chars` across the assembled prompt plus all state/docs it actually passes to the model.
    - Derive `estimated_tokens`, `context_util_pct`, and `leftover_pct` using `params.context_token_per_char` and `params.context_window_tokens`.
    - Only then proceed to create/edit roadmap notes and update `workflow_state`.
- **Disallow partial success when tracking is enabled**:
  - When `params.enable_context_tracking` is true and there is any failure in computing these metrics (e.g. missing config, bad window size), the implementation should **abort the deepen run before writing content** and surfacing a result.
  - Instead, it should return a failure outcome back to auto-roadmap so that auto-roadmap can log `context-tracking-missing` and leave the queue entry marked `queue_failed: true`.
- **Ensure the log write covers all required fields**:
  - Update the implementation so that, for any successful deepen run, it always:
    - Increments `iterations_per_phase[current_phase]`.
    - Sets `current_subphase_index` to the new target.
    - Appends an 11-column row to the workflow_state `## Log` with numeric `Ctx Util %`, `Leftover %`, `Threshold`, and `Est. Tokens / Window`.
    - Updates frontmatter `last_ctx_util_pct` to match the new Ctx Util %.
  - Only when `enable_context_tracking` is **false** should it intentionally write `"-"` for the four context columns and Util Delta %.

### 4. Plan changes to auto-roadmap’s postcondition check

- **Tighten the detection logic in auto-roadmap** for the context-tracking postcondition:
  - When RESUME-ROADMAP deepen completes, auto-roadmap should:
    - Re-read the last data row in the `## Log` table and parse the four context columns.
    - If `effective_enable_context_tracking` was true **and** the row contains `"-"` in any of those four columns, it must always:
      - Log an explicit `context-tracking-missing` error in `3-Resources/Errors.md` including the offending row.
      - Mark the queue entry as `queue_failed: true` and retain it in `.technical/prompt-queue.jsonl`.
      - Add a `#review-needed` warning callout into `roadmap-state.md`.
  - Confirm that this logic doesn’t run for actions other than `deepen` and does not misfire when `enable_context_tracking` was explicitly set to `false`.

### 5. Guard against regressions and interactions with other roadmap actions

- **Audit other roadmap actions** (`advance-phase`, `recal`, `expand`, etc.) in `auto-roadmap.mdc` and the associated skills to ensure they:
  - Don’t rely on the context utilization fields being populated for non-deepen actions, and
  - Continue to work even when context tracking is disabled or temporarily broken.
- **Add a lightweight self-audit step (for later execution)** consistent with `Mode-Success-Contracts.md`:
  - On each RESUME-ROADMAP run, verify that one and only one of the success conditions holds: state advance, follow-up queue, Decision Wrapper, or high-severity error.
  - Specifically flag cases where roadmap content has changed but context metrics are missing as a distinct error category.

### 6. Validate with targeted tests (to run after plan approval)

- **Single-project smoke tests** on `genesis-mythos-master`:
  - Run RESUME-ROADMAP deepen with default params (no explicit `enable_context_tracking`) and confirm that:
    - A new secondary/tertiary is created.
    - `workflow_state.md` gains an 11-column log row with numeric context fields and updated `last_ctx_util_pct`.
  - Run another deepen with `enable_context_tracking: false` and confirm that:
    - The content and iteration fields update.
    - The four context fields show `"-"` and auto-roadmap does **not** log a context-tracking error.
- **Negative test** (simulated failure path):
  - Temporarily (via test harness) force roadmap-deepen to skip metric computation and verify that:
    - It does not write new roadmap notes.
    - Auto-roadmap logs `context-tracking-missing` and keeps the queue entry with `queue_failed: true`.

This plan keeps changes tightly scoped to the roadmap-deepen implementation and auto-roadmap’s postcondition check, aligned with your existing contracts and without altering research-agent behavior or other roadmap pipelines.