---
name: Trace and fix workflow_state silent failures
overview: "Trace why the last two (and recent) RESUME-ROADMAP deepen runs left context tracking as \"-\" and timestamps wrong; then fix the silent failures by making the postcondition mandatory and unambiguous, defining the canonical ## Log table, and requiring local timestamps and metric computation before write."
todos: []
isProject: false
---

# Trace and fix workflow_state silent failures

## 1. Root-cause trace (why the last runs failed)

### Evidence from current state

- **workflow_state.md** at `1-Projects/genesis-mythos-master/Roadmap/workflow_state.md`:
  - Contains **three** YAML frontmatter blocks and **three** `## Log` tables (lines 1–18 + 20–31, then 32–51, then 52–75).
  - The **first** table has 8 deepen rows (12:10–13:20) with **all** context columns (`Ctx Util %`, `Leftover %`, `Threshold`, `Est. Tokens / Window`, `Util Delta %`) set to `"-"`.
  - Frontmatter `last_ctx_util_pct: "-"` and `last_auto_iteration: "2026-03-10T13:20:00Z"` (Z = UTC).
- **Specs already in place**: [auto-eat-queue.mdc](.cursor/rules/context/auto-eat-queue.mdc) pre-dispatch sets `params.enable_context_tracking = true` when not explicitly false; [auto-roadmap.mdc](.cursor/rules/context/auto-roadmap.mdc) defines the postcondition (re-read last row, parse four columns, fail if "-" when effective flag true); [roadmap-deepen/SKILL.md](.cursor/skills/roadmap-deepen/SKILL.md) requires computing and writing numeric metrics when tracking is on.

### Why tracking is absent (silent failure)

1. **Metrics never computed before write**
  The agent following the skill can append a row without actually running the context-util math (sum chars → estimated_tokens → context_util_pct, etc.). The skill says "MUST compute" but there is no hard gate (e.g. "do not call update_note until you have numeric values"). So the agent writes "-" and continues.
2. **Postcondition not executed or wrong table**
  Auto-roadmap says: after roadmap-deepen, "Read the **last line** of workflow_state (last data row of the ## Log table)". It does **not** say which of multiple `## Log` tables to use. So:
  - If the agent re-reads and parses the **third** table (one Phase 0 row with "-"), it might mis-attribute that row or get confused.
  - More likely: the agent **never re-reads** the file after appending and therefore never runs the postcondition, so the run is reported successful even when the new row has "-".
3. **No explicit "you MUST run this step"**
  The postcondition is buried in a long bullet; it is easy for the agent to treat "append row" as the end of the deepen step and skip the validation.

### Why timestamps are wrong

- The table uses a single **Timestamp** column (e.g. `2026-03-10 12:10`). Frontmatter `last_auto_iteration` is explicitly UTC (`...T13:20:00Z`).
- The agent has no specified way to get **local** time. The skill says "timestamps are local" and "normalize on write" but does not say how (e.g. "run `datetime.now()` and use that string"). So the writer uses whatever default the environment provides (often UTC), which matches the user’s "2 hours behind" if they are in a UTC+2 or similar timezone.

### Summary of silent failures


| Failure                         | Cause                                                                     |
| ------------------------------- | ------------------------------------------------------------------------- |
| Context columns stay "-"        | Agent does not compute metrics before append; no pre-write gate.          |
| Postcondition does not catch it | Agent skips re-read/parse step, or parses the wrong ## Log table.         |
| Timestamps wrong                | No defined way to obtain local time; UTC or server time is used.          |
| Ambiguous "last row"            | Multiple ## Log tables; "last data row of the ## Log table" is undefined. |


---

## 2. Fixes (eliminate silent failures)

### 2.1 Define canonical ## Log table and normalize file

- **Rules and docs**: State explicitly that the **canonical** log is the **first** `## Log` table in the file (the one that immediately follows the **first** YAML frontmatter block). All appends go there; all "last data row" parsing uses only that table.
- **Where to update**: [auto-roadmap.mdc](.cursor/rules/context/auto-roadmap.mdc) (postcondition and any reference to "last row"); [roadmap-deepen/SKILL.md](.cursor/skills/roadmap-deepen/SKILL.md) (step "Update workflow_state"); [Vault-Layout.md](3-Resources/Second-Brain/Vault-Layout.md) (workflow_state schema).
- **workflow_state.md cleanup**: In a one-time, forward-only change: keep only the **first** frontmatter block and the **first** `## Log` table (with all its current rows). Delete the second and third YAML blocks and the second and third `## Log` sections so the file has a single frontmatter and a single table. This removes ambiguity and ensures the next run appends to and reads from the same table.

### 2.2 Make the postcondition mandatory and unambiguous

- In [auto-roadmap.mdc](.cursor/rules/context/auto-roadmap.mdc), turn the context-tracking check into a **numbered sub-step** that must be completed before the deepen is considered successful:
  - **Step 3b (mandatory, immediately after roadmap-deepen returns):**  
  (1) Re-read `workflow_state.md`.  
  (2) Locate the **first** `## Log` table (right after the first frontmatter).  
  (3) Take that table’s **last data row** (last pipe-delimited row, not the header).  
  (4) Parse the four context columns: Ctx Util %, Leftover %, Threshold, Est. Tokens / Window.  
  (5) If **effective_enable_context_tracking** was **true** for this run **and** any of those four is `"-"` or empty or not a valid number: treat the run as **failed**: append to [Errors.md](3-Resources/Errors.md) (error_type **context-tracking-missing**, include full row in Trace/Summary), set **queue_failed: true** for this entry when rewriting the queue, append **failure** to Watcher-Result, add **#review-needed** to the project’s roadmap-state.md, and **do not** clear the queue entry.  
  (6) Only if the check passes (or tracking was false) consider the deepen successful and proceed.  
  - Add a short line: "You MUST complete step 3b before considering the deepen step successful; skipping it is a pipeline violation."

### 2.3 Pre-write gate in roadmap-deepen (no row with "-" when tracking on)

- In [roadmap-deepen/SKILL.md](.cursor/skills/roadmap-deepen/SKILL.md), add a **"Before appending the log row"** block (e.g. just before the "Update workflow_state" step):
  - When **params.enable_context_tracking === true**:
    1. You **MUST** compute: `estimated_tokens` (sum character counts of: deepen prompt, workflow_state.md, roadmap-state.md, distilled-core.md, and any phase/secondary/tertiary notes read this iteration; multiply by `context_token_per_char`), then `context_util_pct`, `leftover_pct`, `context_util_threshold`, and Util Delta % (from previous row or `last_ctx_util_pct`).
    2. If you have **not** performed this computation, do **not** append the row; do **not** advance workflow_state. Return a clear error to the caller (e.g. `context-metrics-failed` or `context-tracking-missing`) and surface it (Errors.md, #review-needed) so auto-roadmap can mark the run failed.
    3. When you append the row, use the **computed numeric values** in the four context columns and Util Delta %; writing `"-"` in those columns when tracking is true is **forbidden**.
  - When **params.enable_context_tracking === false**: writing `"-"` in those columns is allowed.
- Optionally add: "If you are unsure how to compute character counts from the assembled context, list the sources and estimate; the key is to never write '-' in the tracked columns when tracking is enabled."

### 2.4 Local timestamps (how to obtain and write)

- In [roadmap-deepen/SKILL.md](.cursor/skills/roadmap-deepen/SKILL.md), in the same "Update workflow_state" / row-append section:
  - Require **Start Local** and **Completion Local** (or the single Timestamp for legacy schema) to be **local** time, not UTC.
  - Add: "To obtain local timestamps: run a one-line code snippet that prints the current local datetime (e.g. Python: `from datetime import datetime; print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))`) and use the **output** as the timestamp string for the row. If the environment is UTC-only, convert UTC to local when writing (e.g. apply a known offset or use a timezone-aware now()). Do not write raw UTC into the Log table if the user expects local time."
  - Keep the existing diagnostic note (log `datetime.now()` vs `utcnow()` and offset to Context-Debug-Log.md or Errors.md) for one-shot debugging if needed.

### 2.5 Sync and docs

- Update [.cursor/sync/skills/roadmap-deepen.md](.cursor/sync/skills/roadmap-deepen.md) and [.cursor/sync/rules/context/auto-roadmap.md](.cursor/sync/rules/context/auto-roadmap.md) to match the rule and skill changes.
- In [Vault-Layout.md](3-Resources/Second-Brain/Vault-Layout.md) (workflow_state schema): state that the **first** `## Log` table after the first frontmatter is the **canonical** log; only one such table should exist (duplicate sections are legacy and should be removed in a one-time cleanup).
- Optionally in [Parameters.md](3-Resources/Second-Brain/Parameters.md): one line that "the context-tracking postcondition is mandatory after every deepen; the canonical log is the first ## Log table in workflow_state."

---

## 3. Implementation order

1. **Canonical table + cleanup**: Update auto-roadmap and roadmap-deepen (and Vault-Layout) to define "first ## Log table" as canonical. Then normalize `workflow_state.md` to a single frontmatter and single ## Log table (remove duplicate blocks/sections).
2. **Mandatory postcondition**: Edit auto-roadmap to add explicit Step 3b and the "MUST complete" language.
3. **Pre-write gate**: Edit roadmap-deepen to add the "Before appending the log row" block and the forbidden "-" when tracking is true.
4. **Local timestamps**: Edit roadmap-deepen to require local time and the code-snippet (or equivalent) method for obtaining it.
5. **Sync and docs**: Update sync copies and Vault-Layout/Parameters as above.

---

## 4. Validation (after fixes)

- Run one RESUME-ROADMAP deepen with default tracking (no `enable_context_tracking: false`). Confirm:
  - The new row is in the **first** (and only) ## Log table.
  - Ctx Util %, Leftover %, Threshold, Est. Tokens / Window, and Util Delta % are **numeric**.
  - Timestamps match local wall-clock (or documented timezone).
- Optionally: run a deepen with `enable_context_tracking: false` and confirm the new row has "-" in context columns and the run is still considered successful (no context-tracking-missing error).
- If possible: simulate a run where the agent would write "-" with tracking on (e.g. instruct to skip metric computation once) and confirm the postcondition fails the run and logs to Errors.md with queue_failed and #review-needed.

---

## 5. Diagram (current vs fixed flow)

```mermaid
flowchart LR
  subgraph current [Current - silent failures]
    A1[Dispatch] --> A2[roadmap-deepen]
    A2 --> A3[Append row often with "-"]
    A3 --> A4[Report success]
    A4 -.->|skipped| A5[Postcondition]
  end

  subgraph fixed [Fixed]
    B1[Dispatch] --> B2[roadmap-deepen]
    B2 --> B3{Pre-write: computed metrics?}
    B3 -->|No| B4[Return error, no row]
    B3 -->|Yes| B5[Append row with numbers + local time]
    B5 --> B6[Step 3b: Re-read first ## Log]
    B6 --> B7{Last row has "-" and tracking on?}
    B7 -->|Yes| B8[Fail: Errors.md, queue_failed, #review-needed]
    B7 -->|No| B9[Success]
  end
```



This plan traces the last runs to: (1) metrics not computed before write, (2) postcondition skipped or wrong table, (3) no defined local-time source, (4) multiple ## Log tables. It then fixes them by defining the canonical table, normalizing the file, making the postcondition a mandatory step, adding a pre-write gate in the skill, and requiring a concrete method for local timestamps.