---
name: workflow_state-fix-forward-only
overview: Fix the roadmap context tracking pipeline so all future RESUME-ROADMAP deepen runs write correct local timestamps and context metrics into workflow_state, without retro-editing existing log rows.
todos:
  - id: ws-fix-reconfirm-state
    content: Reconfirm current workflow_state and prompt-queue state to characterize the latest incorrect rows.
    status: completed
  - id: ws-fix-timestamps-forward
    content: Adjust roadmap-deepen/auto-roadmap implementation so workflow_state logs local Start/Completion/Duration timestamps for each future deepen run.
    status: completed
  - id: ws-fix-context-metrics-forward
    content: Ensure default-on context tracking and hard postconditions so future deepen rows always have valid metrics when tracking is enabled, or hard-fail when metrics are missing.
    status: completed
  - id: ws-fix-forward-validation
    content: Run forward-only validation tests (happy path, opt-out, forced metric failure, timezone sanity) to confirm future workflow_state rows are correct without retro-editing existing rows.
    status: completed
isProject: false
---

## Forward-only fix for workflow_state timestamps and context tracking

### 1. Reconfirm current state and failure pattern

- **Inspect live workflow_state**: Re-read `[1-Projects/genesis-mythos-master/Roadmap/workflow_state.md](/home/darth/Documents/Second-Brain/1-Projects/genesis-mythos-master/Roadmap/workflow_state.md)` to see the latest `## Log` rows that were appended after the recent changes, noting:
  - Whether `Timestamp` (or Start/Completion if already extended) is off from your local wall-clock time (e.g. consistently −2h).
  - Whether the four context columns (`Ctx Util %`, `Leftover %`, `Threshold`, `Est. Tokens / Window`) and `Util Delta %` are `"-"` or missing for recent `deepen` actions despite `enable_context_tracking` being true.
- **Cross-check queue inputs**: Confirm that corresponding `RESUME-ROADMAP` entries in `[.technical/prompt-queue.jsonl](/home/darth/Documents/Second-Brain/.technical/prompt-queue.jsonl)` either:
  - Explicitly set `"enable_context_tracking": true`, or
  - Omit the flag so default-on rules should have applied.
- **Verify rules vs behavior**: Compare this to the specs in `[.cursor/rules/context/auto-eat-queue.mdc](/home/darth/Documents/Second-Brain/.cursor/rules/context/auto-eat-queue.mdc)` and `[.cursor/rules/context/auto-roadmap.mdc](/home/darth/Documents/Second-Brain/.cursor/rules/context/auto-roadmap.mdc)` to see whether the observed failures are due to implementation gaps (e.g. timestamps written in UTC, metrics not computed in roadmap-deepen) vs misconfiguration.

### 2. Fix timestamps at the source (non-negotiable, forward-only)

- **Add a one-shot timezone diagnostic** in the implementation of `roadmap-deepen` (or a temporary helper) so that on a test run it logs:
  - `datetime.now()` (local), `datetime.utcnow()`, `time.tzname`, and `tm_gmtoff/3600` to a debug note (e.g. `3-Resources/Context-Debug-Log.md`) or Errors.md.
  - Use this once to confirm whether the environment is running in UTC or a different TZ, and what the local offset is (likely −4h for EDT).
- **Normalize on write for future rows**:
  - In the code path that appends new rows to `workflow_state ## Log` (currently driven by auto-roadmap + roadmap-deepen), ensure that:
    - The **start timestamp** used for each iteration row is derived from a **local time object**, either by:
      - Capturing local time at **RESUME-ROADMAP dispatch** (EAT-QUEUE / auto-roadmap) and passing it through, or
      - Converting any UTC timestamp to local just before formatting.
    - The **completion timestamp** is likewise taken or converted to local at the end of the run.
  - Keep the underlying runtime free to use UTC internally; the key is that what is **written to `workflow_state.md` is local**, matching your mental model and Obsidian.
- **Document the contract** (already partially in `Parameters.md` and `Vault-Layout.md`):
  - Re-affirm that `workflow_state` timestamps are local and that any new implementation must convert from UTC → local at the write boundary when necessary.

### 3. Enforce default-on metrics and timing for all future deepen runs

- **Dispatch: default-on flag** (already specified, verify/enforce implementation):
  - In `auto-eat-queue` dispatch for `RESUME-ROADMAP` entries with `action: deepen` (or auto/empty action), ensure implementation always:
    - Sets `params.enable_context_tracking = true` **unless** the queue entry explicitly sets it to `false`.
    - Logs this effective flag in a debug/Prompt-Log or Watcher-Result line for audit.
- **Auto-roadmap: effective flag and postcondition** (align implementation with rule text):
  - Derive a single `effective_enable_context_tracking` from `params.enable_context_tracking` after merges, ignoring any config-level attempt to disable tracking globally.
  - Always pass this effective flag into `roadmap-deepen` and any code that appends rows to `workflow_state`.
  - After `roadmap-deepen` returns and the state is ready to be appended:
    - If `effective_enable_context_tracking == true`, expect **numeric** values for the four context metrics and `Util Delta %`.
    - If any of those fields are `"-"`, empty, or invalid **for the new row**:
      - Treat the run as **failed** (`context-tracking-missing`), not a success.
      - Log to `3-Resources/Errors.md`, mark the queue entry `queue_failed: true`, leave it in the queue, and surface `#review-needed` on `roadmap-state.md`.
- **Roadmap-deepen: metrics + timing invariant** (forward-looking behavior):
  - Ensure the implementation of `roadmap-deepen` matches the updated spec in `[.cursor/skills/roadmap-deepen/SKILL.md](/home/darth/Documents/Second-Brain/.cursor/skills/roadmap-deepen/SKILL.md)`:
    - When `enable_context_tracking == true`:
      - Compute **estimated_tokens**, **context_util_pct**, **leftover_pct**, **context_util_threshold**, and **Util Delta %**.
      - Return those values together with any identifiers needed for the log row.
      - Do **not** write `"-"` into context metrics or Util Delta %, and do **not** advance `workflow_state` if metrics fail; instead return a recognizable error for auto-roadmap.
    - When `enable_context_tracking == false`:
      - It is allowed to write `"-"` into the four context columns and Util Delta, but timing and iteration fields must still be filled.
  - Extend or refactor the log-append code so that **one atomic write** per iteration appends a single row containing:
    - **Start Local**, **Completion Local**, and **Duration sec** (local start & finish, plus elapsed seconds), and
    - The full set of context metrics and `Status / Next`.

### 4. Leave existing rows intact, but make future ones clearly correct

- **No retroactive edits** to current `workflow_state.md`:
  - Do not mass-edit the existing log rows, even if timestamps and metrics are wrong.
  - Optionally, add a **brief banner** or comment (manually, outside this plan) above the log noting the date from which the new, hardened behavior started.
- **Future rows as the new ground truth**:
  - After implementing the fixes, treat **rows appended from that point onward** as the reliable source for:
    - Accurate local timestamps (start/completion/duration), and
    - Correct context tracking metrics when tracking is enabled.
  - Older rows can be interpreted as “pre-hardening” data and, if necessary, filtered in Dataview by date or by the presence of new columns.

### 5. Validate with forward-only tests

- **Happy-path deepen (default tracking)**:
  - Queue a `RESUME-ROADMAP` deepen entry with no explicit `enable_context_tracking` flag and run EAT-QUEUE.
  - Confirm the new `workflow_state ## Log` row has:
    - Local-timestamp start/completion fields close to your actual clock.
    - Numeric values in `Ctx Util %`, `Leftover %`, `Threshold`, `Est. Tokens / Window`, and `Util Delta %`.
- **Explicit opt-out**:
  - Queue a second deepen entry with `"enable_context_tracking": false` and run it.
  - Confirm the new row:
    - Has correct local start/completion/duration and iteration fields.
    - Has `"-"` in the four context columns and Util Delta %, and does **not** trigger a context-tracking error.
- **Simulated metric failure (tracking on)**:
  - Temporarily tweak or stub the implementation of `roadmap-deepen` so it pretends metric computation fails when `enable_context_tracking == true`.
  - Run a deepen and check that:
    - No new row is appended (or, if you choose to log a diagnostic row, it is clearly marked and consistent with the spec).
    - Auto-roadmap logs `context-tracking-missing`, marks the queue entry `queue_failed: true`, and surfaces `#review-needed` without advancing roadmap state.
- **Timezone sanity check**:
  - After the fixes, run one more deepen and verify that the logged timestamps match your **local** time, not UTC or an offset (no more consistent −2h lag).

With this plan, implementation will not touch existing `workflow_state` history, but all **future** RESUME-ROADMAP deepen runs will produce rows whose timestamps and context tracking metrics are both correct and enforced by the pipeline’s invariants.