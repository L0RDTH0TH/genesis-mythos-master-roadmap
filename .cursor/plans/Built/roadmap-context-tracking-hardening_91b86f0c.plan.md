---
name: roadmap-context-tracking-hardening
overview: Ensure context tracking is reliably on-by-default for roadmap deepen runs and that workflow_state always records context utilization metrics unless explicitly disabled via queue params.
todos:
  - id: verify-current-workflow_state-rows
    content: Verify recent workflow_state log rows and matching RESUME-ROADMAP queue entries to characterize where context columns are using dashes unexpectedly.
    status: completed
  - id: tighten-auto-roadmap-default-and-postcondition
    content: Tighten auto-roadmap’s effective enable_context_tracking default and its postcondition so any missing context metrics with tracking on are hard failures.
    status: completed
  - id: reinforce-roadmap-deepen-metric-invariants
    content: Reinforce roadmap-deepen’s invariant that when tracking is enabled it must compute and write all context metrics or fail cleanly without partial writes.
    status: completed
  - id: update-second-brain-docs-and-queue-aliases
    content: Update Second-Brain docs and Queue-Alias-Table so they consistently describe workflow_state’s context columns and default-on tracking semantics.
    status: completed
  - id: design-and-run-roadmap-validation-tests
    content: Design and later run a small set of RESUME-ROADMAP deepen tests (default, opt-out, and simulated failure) to verify reliable context tracking behavior.
    status: completed
isProject: false
---

## Roadmap context tracking hardening

### 1. Reconfirm current workflow_state behavior

- **Inspect live workflow_state logs**: Open `[1-Projects/genesis-mythos-master/Roadmap/workflow_state.md](/home/darth/Documents/Second-Brain/1-Projects/genesis-mythos-master/Roadmap/workflow_state.md)` and verify the `## Log` table schema matches the 11-column spec (`Ctx Util %`, `Leftover %`, `Threshold`, `Est. Tokens / Window`, `Util Delta %`). Note any recent rows where these context columns are `"-"` despite the run being a `deepen` action.
- **Cross-check queue inputs**: In `[.technical/prompt-queue.jsonl](/home/darth/Documents/Second-Brain/.technical/prompt-queue.jsonl)`, find the corresponding `RESUME-ROADMAP` entries and confirm what `params.enable_context_tracking` was (true, false, or unset) for each run that produced dashes.
- **Compare with archived copy**: Briefly compare with `[4-Archives/test-2-genesis-mythos-master/Roadmap/workflow_state.md](/home/darth/Documents/Second-Brain/4-Archives/test-2-genesis-mythos-master/Roadmap/workflow_state.md)` to confirm that the default schema and expected columns are stable across copies.

### 2. Enforce default-on semantics at dispatch and auto-roadmap

- **Auto-eat-queue dispatch contract**: In `[.cursor/rules/context/auto-eat-queue.mdc](/home/darth/Documents/Second-Brain/.cursor/rules/context/auto-eat-queue.mdc)`, verify that when dispatching a `RESUME-ROADMAP` entry with `action: deepen` and no explicit `enable_context_tracking: false`, the dispatcher always sets `params.enable_context_tracking = true` before calling auto-roadmap. Adjust the rule text if needed to make this mandatory and unambiguous.
- **Auto-roadmap effective flag and postcondition**: In `[.cursor/rules/context/auto-roadmap.mdc](/home/darth/Documents/Second-Brain/.cursor/rules/context/auto-roadmap.mdc)`, tighten the description so that:
  - It derives a single `effective_enable_context_tracking` flag (default true unless the queue params explicitly set it to false).
  - After each successful `deepen`, it *must* re-read the last `workflow_state ## Log` row and, when `effective_enable_context_tracking` is true, treat any `"-"` in the four context columns as a hard error (log `context-tracking-missing`, mark the queue entry `queue_failed: true`, append `#review-needed` on the project roadmap, and do not clear the queue entry).
- **Document interaction with roadmap-state**: In `[1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md](/home/darth/Documents/Second-Brain/1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md)` and the relevant Second-Brain docs, note that deepen runs that advance state but lack context metrics should be considered contract violations, not successes.

### 3. Clarify roadmap-deepen’s responsibility for metrics

- **Align SKILL spec with behavior**: In `[.cursor/skills/roadmap-deepen/SKILL.md](/home/darth/Documents/Second-Brain/.cursor/skills/roadmap-deepen/SKILL.md)`, keep the invariant explicit that when `params.enable_context_tracking` is true, the skill must compute `estimated_tokens`, `context_util_pct`, `leftover_pct`, and `context_util_threshold` and write non-`"-"` values into `Ctx Util %`, `Leftover %`, `Threshold`, and `Est. Tokens / Window` in the new 11-column log row, plus update `last_ctx_util_pct` in frontmatter.
- **No partial success with tracking on**: Specify that if metric computation fails while `params.enable_context_tracking` is true, roadmap-deepen should not append a log row with `"-"` in these columns; instead it should surface an error (for auto-roadmap to record as `context-tracking-missing`) and avoid writing new roadmap content for that iteration.
- **Disabled-tracking behavior**: Reiterate that only when `params.enable_context_tracking` is explicitly false should roadmap-deepen write `"-"` in the four context columns and `Util Delta %`, so dashes are reserved for intentional opt-outs.

### 4. Sync documentation and queue aliases

- **Second-Brain docs alignment**: Update `[3-Resources/Second-Brain/Parameters.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Parameters.md)` and `[3-Resources/Second-Brain/Vault-Layout.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Vault-Layout.md)` to clearly state that context tracking is default-on for `RESUME-ROADMAP` deepen, that workflow_state’s `## Log` always includes the four context columns, and that dashes in those fields are only valid when the queue entry explicitly disabled tracking.
- **Roadmap upgrade / audit docs**: In `[3-Resources/Second-Brain/Roadmap-Upgrade-Plan.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Roadmap-Upgrade-Plan.md)` and any mode-success docs, add a short note that “state advanced + context metrics missing” should be treated as an error path, not a success, to reinforce the contract.
- **Queue alias visibility**: Ensure `[3-Resources/Second-Brain/Queue-Alias-Table.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Queue-Alias-Table.md)` mentions any relevant aliases or modes (e.g. `RESUME-ROADMAP`, `RECAL-ROAD`, `AUDIT-CONTEXT`) in relation to context tracking so you can see at a glance which modes depend on workflow_state metrics.

### 5. Plan validation runs for reliability

- **Happy-path deepen with default tracking**: After changes, plan to run a `RESUME-ROADMAP` deepen (no explicit tracking flag) and confirm that the new row in `workflow_state ## Log` has numeric `Ctx Util %`, `Leftover %`, `Threshold`, `Est. Tokens / Window`, and `Util Delta %`, and that `last_ctx_util_pct` is updated.
- **Explicit opt-out**: Plan a second test where the queue entry sets `"enable_context_tracking": false` and verify that deepen still advances roadmap content but writes `"-"` into the context columns and does not raise a context-tracking error.
- **Simulated failure path**: Design a temporary test variant (or mental harness) where roadmap-deepen is assumed to fail metric computation; verify that, under the new contracts, such a run would:
  - Avoid writing new workflow_state rows with `"-"` context fields when tracking is on.
  - Cause auto-roadmap to treat the run as `context-tracking-missing`, keep the queue entry with `queue_failed: true`, and surface `#review-needed` in `Errors.md` and/or roadmap-state.

This plan keeps the implementation changes narrowly focused on the RESUME-ROADMAP / roadmap-deepen path and the workflow_state schema, so context tracking becomes a reliable default without impacting ingest, organize, archive, or express pipelines.