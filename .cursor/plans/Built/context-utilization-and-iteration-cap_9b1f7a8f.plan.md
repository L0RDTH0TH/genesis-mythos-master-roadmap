---
name: context-utilization-and-iteration-cap
overview: Add context utilization tracking and a configurable gating threshold to the roadmap deepen pipeline, and set/maximize a default per-phase iteration cap of 33 across roadmap artifacts.
todos:
  - id: inspect-roadmap-artifacts
    content: Review roadmap-related skills (`roadmap-deepen`, `roadmap-generate-from-outline`, `roadmap-advance-phase`), config, and docs to confirm current behavior and schemas.
    status: completed
  - id: update-config-and-parameters-docs
    content: Add roadmap context-utilization and iteration-cap keys to `Second-Brain-Config` and document them in `Parameters`, `Vault-Layout`, and `Roadmap-Upgrade-Plan`.
    status: completed
  - id: implement-roadmap-skill-changes
    content: Modify roadmap skills to support 10-column logs, context-util computation, threshold-based gating, and `max_iterations_per_phase` default alignment.
    status: completed
  - id: sync-skills-and-backbone-docs
    content: Update `.cursor/sync/skills`, `Skills.md`, `Queue-Sources.md`, and `auto-roadmap.mdc` to describe the new context-utilization tracking and gating behavior.
    status: completed
  - id: align-key-workflow-state-files
    content: "Optionally update key existing `workflow_state` files (e.g. genesis-mythos-master) to use `max_iterations_per_phase: 33`."
    status: completed
  - id: run-end-to-end-tests
    content: Run `RESUME-ROADMAP` queue entries with tracking on/off and with util above/below threshold to verify logs, queue behavior, and warning callouts.
    status: completed
isProject: false
---

# Context utilization tracking & iteration cap

## Goals

- **Track processing context utilization** for each `RESUME-ROADMAP` deepen run and log it into the roadmap `workflow_state` log table.
- **Gate deepening when utilization is high**, queueing a `RECAL-ROAD` step instead of continuing, based on configurable thresholds.
- **Standardize the per-phase iteration cap** by setting `max_iterations_per_phase: 33` as the default in config and new `workflow_state` files, and ensuring older state files are aligned.

## 1. Recon & current behavior

- **Inspect roadmap skills**:
  - Read `.cursor/skills/roadmap-deepen/SKILL.md` to understand current deepen flow, inputs/params, how the `## Log` table is written, and where queue entries are scheduled.
  - Read `.cursor/skills/roadmap-generate-from-outline/SKILL.md` to see how `workflow_state.md` is created (frontmatter + initial `## Log` table header) during ROADMAP MODE.
  - Read `.cursor/skills/roadmap-advance-phase/SKILL.md` to see how it appends log rows and how it currently formats the log columns.
- **Inspect docs & config**:
  - Read `3-Resources/Second-Brain/Vault-Layout.md` for the documented schema of `workflow_state` and its `## Log` section.
  - Read `3-Resources/Second-Brain/Parameters.md` and `3-Resources/Second-Brain-Config.md` to see existing roadmap-related keys and how `prompt_defaults.roadmap` is structured.
  - Read `3-Resources/Second-Brain/Queue-Sources.md` and `.cursor/rules/context/auto-roadmap.mdc` to confirm how `RESUME-ROADMAP` params are merged from Config and queue entries.
  - Optionally read `3-Resources/Second-Brain/Roadmap-Upgrade-Plan.md` and any `Roadmap-Log` if present to align wording/logging.

## 2. Config & parameter schema

- **Add roadmap config keys** (single source of truth) in `3-Resources/Second-Brain-Config.md`, under the existing `prompt_defaults.roadmap` (or a dedicated top-level `roadmap` block, matching current style):
  - `max_iterations_per_phase: 33`
  - `context_util_threshold: 80`
  - `context_token_per_char: 0.25` (with inline comment describing char→token heuristic)
  - `context_window_tokens: 128000`
  - `enable_context_tracking: true` (documents default-on intent; the effective flag is computed per run by auto-roadmap and can only be turned off via an explicit `enable_context_tracking: false` on a RESUME-ROADMAP queue entry).
- **Clarify override behavior**:
  - Ensure the narrative in Config explains that `RESUME-ROADMAP` queue params can override these keys per run, and that only an explicit `enable_context_tracking: false` on a queue entry disables tracking for that run.
  - Note that when tracking is disabled via queue param for a specific run, context-util columns in the corresponding log row remain `"-"` and no gate is applied.
- **Document in Parameters** (`3-Resources/Second-Brain/Parameters.md`):
  - Add a table or section describing each new key (purpose, default, override behavior).
  - Clearly document the token estimate formula: `context_util_pct = min(100, round(100 * (total_chars * context_token_per_char) / context_window_tokens))`, `leftover_pct = 100 - context_util_pct`.
  - Note the heuristic nature of `context_token_per_char` and that a future token-count skill could replace it.
  - State that new `workflow_state` frontmatter is initialized with `max_iterations_per_phase: 33`.

## 3. Log table schema (10-column format)

- **Update documentation for `workflow_state` log** (`Vault-Layout.md`, and `Roadmap-Upgrade-Plan.md` where it describes the log):
  - Define the canonical 10-column header:
    - `Timestamp | Action | Target | Iter Obj | Iter Phase | Ctx Util % | Leftover % | Threshold | Est. Tokens / Window | Status / Next`
  - Specify semantics:
    - **Ctx Util %**: input-side context utilization percentage for that deepen run (or `"-"` when tracking disabled/NA).
    - **Leftover %**: `100 - Ctx Util %` (or `"-"` when tracking disabled/NA).
    - **Threshold**: the `context_util_threshold` used for that run (or `"-"` when not tracking).
    - **Est. Tokens / Window**: `N / W` where `N` is estimated tokens and `W` is `context_window_tokens` for that run; `"-"` when not tracking.
    - **Status / Next**: textual summary of status and next queued action (e.g., `RECAL-ROAD queued`, `paused-high-util`, `next deepen`, etc.).
  - Note that existing 7-column logs remain valid, and the first write from a tracking-aware run should expand the header to 10 columns.

## 4. Skill changes – `roadmap-generate-from-outline`

- **Initialize iteration cap in frontmatter**:
  - In the step that creates `workflow_state.md`, ensure frontmatter includes `max_iterations_per_phase: 33` (read from Config rather than hard-coded, but defaulting to 33 when absent).
- **Initialize 10-column log header**:
  - Ensure the `## Log` table created in new `workflow_state` files uses the 10-column header listed above.
  - Confirm that ROADMAP MODE itself does not append body rows; it only sets up the header and frontmatter.

## 5. Skill changes – `roadmap-deepen`

- **Input parameters and config merge**:
  - Extend the SKILL doc to describe new optional params: `enable_context_tracking`, `context_util_threshold`, `context_token_per_char`, `context_window_tokens`.
  - Specify that these come from `params` (queue) with fallbacks to Config (`prompt_defaults.roadmap` block, with defaults 33/80/0.25/128000) and that there is no hard-coded value in the logic.
- **Context utilization computation** (when `enable_context_tracking === true`):
  - Identify and sum character lengths of all input-side sources for the deepen step:
    - The assembled prompt text (user prompt + any roadmap-specific rules text the SKILL composes).
    - `workflow_state` note content.
    - `roadmap-state` note content.
    - `distilled-core` note content.
    - Any phase/secondary/tertiary notes read for this deepen iteration.
  - Compute `estimated_tokens = total_chars * context_token_per_char`.
  - Compute `context_util_pct = min(100, round(100 * estimated_tokens / context_window_tokens))`.
  - Compute `leftover_pct = 100 - context_util_pct`.
  - Retain `estimated_tokens` and `context_window_tokens` for logging into `Est. Tokens / Window` as `"<estimated_tokens> / <context_window_tokens>"`.
- **Header normalization to 10 columns**:
  - When writing a log row, inspect the existing `## Log` header:
    - If a 7-column header is detected, rewrite/extend it to the 10-column version before appending the new row.
    - Ensure subsequent log rows always use 10 columns, with `"-"` in the four new columns for older actions or for actions that do not compute utilization.
- **Log row append (normal deepen)**:
  - For each deepen iteration, append a row with:
    - `Timestamp`: ISO 8601 or existing timestamp format.
    - `Action`: e.g. `deepen`.
    - `Target`: phase identifier (e.g. `Phase-5-Compute-Shader`).
    - `Iter Obj`, `Iter Phase`: existing iteration counters.
    - `Ctx Util %`: computed `context_util_pct` or `"-"` when tracking disabled.
    - `Leftover %`: `leftover_pct` or `"-"`.
    - `Threshold`: `context_util_threshold` or `"-"`.
    - `Est. Tokens / Window`: `"<estimated_tokens> / <context_window_tokens>"` or `"-"`.
    - `Status / Next`: `"next deepen"` or more specific status; will be overridden to `"RECAL-ROAD queued"` on a threshold breach.
- **Gate behavior when util exceeds threshold**:
  - Before scheduling the next deepen/expand at the end of the SKILL:
    - If `enable_context_tracking` is true **and** `context_util_pct > context_util_threshold`:
      - **Do not** enqueue the next `RESUME-ROADMAP` deepen entry.
      - Enqueue one `RECAL-ROAD` queue entry with params:
        - `{"mode":"RESUME-ROADMAP","params":{"action":"recal","reason":"high-context-utilization","util_percent": <computed>, ...project-identifiers...}}` in the standard queue format used in this vault.
      - Update the just-appended log row’s `Status / Next` cell to something like `"RECAL-ROAD queued"` and optionally `Action`/status fields to `"paused-high-util"` if that is consistent with existing conventions.
      - Optionally update `workflow_state` frontmatter `status` to `blocked` with a short note about high context utilization.
      - Append a warning callout line to the appropriate log note (`3-Resources/Roadmap-Log.md` if present, otherwise `3-Resources/Ingest-Log.md`):
        - Example: `> [!warning] High context pressure detected (82% / 80% threshold) — RECAL-ROAD queued to distill before further deepening`.
    - Else (util ≤ threshold or tracking disabled): preserve existing behavior, including iteration-cap checks, and queue the next deepen/expand action as before.
- **Iteration cap consistency (nice-to-have)**:
  - On each deepen call, check `workflow_state` frontmatter:
    - If `max_iterations_per_phase` is missing or less than the Config default (33), update it to the current Config default and mention this in an internal comment in the SKILL doc.
  - Ensure the deepen logic already respects `max_iterations_per_phase` as a hard cap; if not, add or tighten the check before scheduling additional deepens.
- **Pressure trend summary (optional)**:
  - Optionally, every N iterations (e.g. every 5) or when `|Δutil_pct| > 10`, append a `SUMMARY` row to the `## Log` table with a condensed trend (e.g. `SUMMARY | Phase-5 | Iter 8/33 | Util trend: 62→78→82% | Risk: rising | Action taken: RECAL queued`).
  - Keep this logic simple to avoid complicating the SKILL; if it adds too much complexity, defer this part.

## 6. Skill changes – `roadmap-advance-phase`

- **Normalize log rows to the 10-column format**:
  - When appending a log row for an advance-phase action, write all 10 columns in the same order as the deepen log.
  - For advance-phase rows, set `Ctx Util %`, `Leftover %`, `Threshold`, and `Est. Tokens / Window` to `"-"`.
  - Ensure compatibility when the existing header is still 7 columns by upgrading the header to 10 columns before appending the new row.

## 7. Docs, sync, and rules

- **Backbone docs sync**:
  - After editing `.cursor/skills/roadmap-deepen/SKILL.md`, update `.cursor/sync/skills/roadmap-deepen.md` to reflect the new behavior, including context-util tracking and the RECAL gate.
  - If `roadmap-generate-from-outline` or `roadmap-advance-phase` skill docs are changed, update their counterparts under `.cursor/sync/skills/` as well.
- **Skills overview doc** (`3-Resources/Second-Brain/Skills.md`):
  - Update the `roadmap-deepen` row to mention:
    - Optional context utilization logging when `enable_context_tracking` is true.
    - Configurable `context_util_threshold`, `context_token_per_char`, `context_window_tokens`.
    - The 10-column `workflow_state` log format (Ctx Util %, Leftover %, Threshold, Est. Tokens / Window, Status / Next).
    - The gate behavior: `util > threshold` → queue `RECAL-ROAD` with reason/util_percent and append a warning callout.
- **Queue sources doc** (`3-Resources/Second-Brain/Queue-Sources.md`):
  - In the `RESUME-ROADMAP` section, extend the params description to include:
    - `enable_context_tracking` (bool, optional; explicit **false** opt-out for a single run; omitted or true means tracking stays on).
    - Optional overrides: `context_util_threshold`, `context_token_per_char`, `context_window_tokens`.
  - Clarify that these are merged with Config (`prompt_defaults.roadmap`) when absent in the queue entry, and that the effective tracking flag is default-on and derived by auto-roadmap.
- **auto-roadmap rule** (`.cursor/rules/context/auto-roadmap.mdc`):
  - Add a brief note stating that `params.enable_context_tracking` (from Config or queue) enables context-util logging and the recal-at-threshold gate, and that both the threshold and the token heuristic are configurable.

## 8. Existing workflow_state updates (optional)

- **Genesis project alignment**:
  - For `1-Projects/genesis-mythos-master/Roadmap/workflow_state.md`, plan a one-time manual or scripted update to add or bump `max_iterations_per_phase: 33` in frontmatter so it uses the new default.
  - Leave other existing `workflow_state` files unchanged; rely on the consistency check in `roadmap-deepen` to upgrade their `max_iterations_per_phase` going forward.

## 9. Testing & verification

- **Happy-path deepen with tracking on**:
  - Create a test queue entry, e.g.:
    - `{"mode":"RESUME-ROADMAP","source_file":"1-Projects/genesis-mythos-master/Roadmap/workflow_state.md","id":"test-context-util","params":{"action":"deepen","enable_context_tracking":true}}`.
  - Run the queue processor and verify:
    - A new log row appears in `workflow_state ## Log` with all 10 columns populated, including `Ctx Util %`, `Leftover %`, `Threshold`, and `Est. Tokens / Window` (e.g. `104832 / 128000`).
    - When the computed utilization is below the threshold, the next queue item is the expected deepen/expand action and `Status / Next` reflects that.
- **Threshold breach path**:
  - Force a scenario where `context_util_pct > context_util_threshold` (e.g. by lowering threshold via queue params) and re-run.
  - Verify that:
    - A `RESUME-ROADMAP` entry with `action: "recal"`, `reason: "high-context-utilization"`, and `util_percent` is queued instead of another deepen.
    - No further deepens are queued until after recal.
    - The `Status / Next` column in the latest log row shows `RECAL-ROAD queued` (and optionally `paused-high-util`).
    - The warning callout is appended to `Roadmap-Log` (or `Ingest-Log` if that is the configured location).
- **Tracking disabled**:
  - Run a `RESUME-ROADMAP` deepen with `enable_context_tracking: false` set explicitly on the queue entry.
  - Confirm:
    - The log row still uses the 10-column format but `Ctx Util %`, `Leftover %`, `Threshold`, and `Est. Tokens / Window` are `"-"`.
    - Deepen behavior (including iteration caps) matches current behavior.
- **Advance-phase logging**:
  - Trigger a `roadmap-advance-phase` action and confirm its log entries use the 10-column format with the four context-related columns set to `"-"`.

## Todos

- **inspect-roadmap-artifacts**: Read roadmap-related skills, config, and docs to confirm current schema and param-merging behavior.
- **update-config-and-parameters-docs**: Add new roadmap-related keys to `Second-Brain-Config` and document them in `Parameters` and `Vault-Layout` (plus `Roadmap-Upgrade-Plan`).
- **implement-roadmap-skill-changes**: Modify `roadmap-generate-from-outline`, `roadmap-deepen`, and `roadmap-advance-phase` skills to support the 10-column log, context-util computation, gating, and iteration-cap enforcement.
- **sync-skills-and-backbone-docs**: Update `.cursor/sync/skills` and `Skills.md`, `Queue-Sources.md`, and `auto-roadmap.mdc` to reflect the new behavior, including default-on tracking semantics and explicit queue-param opt-out.
- **align-key-workflow-state-files**: Optionally update `genesis-mythos-master` `workflow_state` frontmatter to set `max_iterations_per_phase: 33`.
- **run-end-to-end-tests**: Execute `RESUME-ROADMAP` runs (with tracking on/off and with forced threshold breach) to verify logging, gating, and queue behavior.

