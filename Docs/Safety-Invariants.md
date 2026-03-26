# Safety Invariants

**Version: 2026-03 – post-subagent migration**

Consolidated safety invariants for all subagents and the Queue. Full logic lives in the rules; this doc is the single reference.

---

## Backups

- **Before any destructive operation** (move, rename, delete, large overwrite), ensure a recent backup: `obsidian_ensure_backup` (preferred) or `obsidian_create_backup` (when ensure indicates missing or stale).
- **If backup creation fails:** Abort destructive steps for that note; log with `#review-needed`; continue with next note in batch.
- **Reference:** core-guardrails.mdc, mcp-obsidian-integration.mdc.

---

## Per-change snapshots

- **Before:** move, rename, split, structural distill, append_to_hub, or other destructive/structural step — call obsidian-snapshot skill with **type per-change** for the target note when **confidence ≥ 85%**.
- **If snapshot fails:** Skip the destructive action; log `#review-needed`.
- **Location:** `Backups/Per-Change/`; append-only; never edit or delete from pipelines.
- **Reference:** core-guardrails, mcp-obsidian-integration.

---

## Confidence bands

| Band | Range | Behavior |
|------|-------|----------|
| **High** | ≥ 85% | Destructive actions allowed **only after** per-change snapshot; dry_run then commit for moves. |
| **Mid** | 68–84% | At most **one** non-destructive refinement loop per note per run; proceed only if post_loop_conf ≥ 85%; else create Decision Wrapper (e.g. Ingest/Decisions/Refinements/). |
| **Low** | < 68% | No destructive action; create Decision Wrapper (e.g. Ingest/Decisions/Low-Confidence/); propose only. |

- **Decay rule:** If post_loop_conf ≤ pre_loop_conf, fall back to user decision: no destructive action for that note; log best-guess and #review-needed where appropriate.
- **Loop logging:** Record in pipeline log and/or obsidian_log_action: `loop_attempted`, `loop_band`, `pre_loop_conf`, `post_loop_conf`, `loop_outcome`, `loop_type`, `loop_reason`.
- **Reference:** Parameters.md, confidence-loops.mdc.

---

## Critical invariant

**No destructive action** unless **both**:

1. Confidence for that action is in the **high band** (≥ 85%) for that pipeline, **and**
2. A **per-change snapshot** for that note has been created successfully in the current run.

If either fails: skip the destructive action; log #review-needed; continue with non-destructive alternatives.

---

## Nested subagent policy (orchestration safety)

- **Single orchestrator**: Only the **main agent + Queue rule** are allowed to orchestrate:
  - Read or write `.technical/prompt-queue.jsonl` or `3-Resources/Task-Queue.md`.
  - Decide which pipeline subagent runs.
  - Append to `3-Resources/Watcher-Result.md` or create Decision Wrappers under `Ingest/Decisions/**`.
- **Nested subagents = helpers only**:
  - Pipeline subagents may call **nested subagents** only as documented in the nested subagent whitelist (see [[3-Resources/Second-Brain/Docs/Subagent-List|Subagent-List]]). As of the Research-layer migration there are exactly **three** sanctioned helper subagents: **Internal Repair Agent (IRA)**, **Validator**, and **Research**.
  - Nested subagents must behave like **pure functions**: they read only the inputs handed to them and return **structured results** to their caller; they must not:
    - Read or write queue files or Task-Queue.
    - Append to `Watcher-Result.md`.
    - Create or apply Decision Wrappers.
    - Mutate roadmap state files (`roadmap-state.md`, `workflow_state.md`) or other global coordination artifacts.
- **Depth and fan-out limits**:
  - Recommended maximum depth: **3 levels** — main agent → Queue/Dispatcher → pipeline subagent → nested helper subagent (IRA / Validator / Research).
  - Fan-out: parents may call several nested helpers in parallel for **local analysis** (e.g. multiple research lookups), but must not chain nested agents to re-orchestrate pipelines.
- **Prompt-level safeguard**:
  - Each pipeline subagent’s high-level instructions must reinforce:
    - *“You may ONLY call the specific nested subagent types listed in your 'Subagent nesting' section, and ONLY for the narrow purposes described. NEVER write to queues, watcher logs, roadmap files, or create decision wrappers — those are RESERVED for the top-level orchestrator. Return results as structured data only.”*

---

## No shell vault ops

- **Never** use shell `cp`, `mv`, or `rm` to mutate Obsidian vault contents.
- All moves/renames/deletes go through MCP tools with backup and snapshot gates.
- **Exception:** Documented, **user-invoked** attachment-move skill (Ingest → 5-Attachments/) only; backup and logging still apply.

---

## Structure before move

- Before any `obsidian_move_note` to a new directory:
  1. Call **obsidian_ensure_structure** with `folder_path` = parent of target path.
  2. Call **obsidian_move_note** with `dry_run: true`; review effects.
  3. Then call **obsidian_move_note** with `dry_run: false` to commit.
- **Post-move:** Set **para-type** (and **project-id** when under 1-Projects/; **status: archived** when under 4-Archives/) on the note at the new path per mcp-obsidian-integration.

---

## Exclusions and protected paths

**Do not move, rename, or delete:**

- `Backups/**` (Per-Change, Batch, Archives).
- `3-Resources/Watcher-Signal.md`, `3-Resources/Watcher-Result.md`, `Ingest/watched-file.md`.
- Any note with frontmatter **watcher-protected: true**.
- MCP backup directories in `~/.cursor/mcp.json`.

**Do not process as primary pipeline input:** Notes under `Ingest/Decisions/**` (consumed by Step 0 and path-apply logic).

- **Reference:** core-guardrails, Vault-Layout.md.

---

## Error Handling Protocol

On **any** pipeline or workflow step failure:

1. **Trace:** Timestamp (ISO 8601), pipeline name, stage/step, affected note path(s), sanitized error message (no secrets).
2. **Summary:** Error type; root cause; impact; suggested fixes; recovery (e.g. restore from Backups/Per-Change/).
3. **Log (owned by top-level run):** Append one entry to **`3-Resources/Errors.md`** (heading, inline table, #### Trace, #### Summary). **Only the main agent / Queue rule** should create or update this note; nested subagents must instead return structured failure details to their caller.
4. **Pipeline log:** One-line reference in the relevant pipeline log, written from the orchestrating context (not from deeply nested helpers).
5. **Error Decision Wrapper:** When appropriate, create under **`Ingest/Decisions/Errors/`** (wrapper_type: error; options A–G recovery-focused); ensure CHECK_WRAPPERS exists; append Watcher-Result line for wrapper creation.
6. **Severity high:** Set approval pending, add #review-needed; skip destructive steps for that note; continue with next.
7. **Fallbacks first:** Before writing an error entry, attempt fallbacks (e.g. obsidian_ensure_structure then retry move); only after exhausting fallbacks, log to Errors.md.

- **Reference:** mcp-obsidian-integration § Error Handling Protocol.

---

## Watcher-Result contract

- On run finish (queue-based or direct), append **one line per requestId** to **`3-Resources/Watcher-Result.md`**:

  ```
  requestId: <id> | status: success|failure | message: "..." | trace: "..." | completed: <ISO8601>
  ```

- Create the file if missing; append only; do not overwrite.
- **Reference:** watcher-result-append.mdc.

---

## Roadmap state

- **Before mutating:** Read `roadmap-state.md` and `workflow_state.md` under `1-Projects/<project_id>/Roadmap/`.
- **Snapshot:** Snapshot state **before and after** every update (per-change).
- **Parse failure:** If roadmap-state.md or workflow_state parse fails → abort roadmap pipeline; log to Errors.md with #state-corrupt; create Decision Wrapper under Ingest/Decisions/Errors/ as appropriate.
- **Reference:** mcp-obsidian-integration, Roadmap subagent.

---

## Restore

- **Restore** from snapshots is **user-triggered only**. No auto-restore.
- **Reference:** mcp-obsidian-integration (restore-queue mode).

---

## Snapshot triggers (by pipeline)

Per-change snapshot is required **before** the following. Batch frequency is per pipeline (e.g. every 3–5 notes for ingest/distill/organize; once per archive sweep for archive). <!-- Gap filled from old Cursor-Skill-Pipelines-Reference.md -->

| Pipeline | Per-change before | Batch |
|----------|-------------------|-------|
| full-autonomous-ingest | split_atomic, distill_note rewrite, append_to_hub, task-reroute target append, move_note, rename_note | Every 5 notes |
| autonomous-distill | First structural rewrite (distill layers, layer-promote, heavy update_note) | ~Every 3 notes |
| autonomous-archive | After archive-check ≥85% but before subfolder-organize / summary-preserve / move | Once per sweep |
| autonomous-express | Large appends (related-content-pull, express-mini-outline, call-to-action-append); also version-snapshot | Optional per batch |
| autonomous-organize | obsidian_rename_note (when name-enhance), obsidian_move_note (when path_conf ≥85%) | ~Every 3 notes |
| roadmap (multi-run) | Every roadmap-state.md and workflow_state update; before phase-X-output overwrite | Per phase or RECAL run |

---

## Log format and loop fields

Pipeline log line format and loop fields (loop_attempted, loop_band, pre_loop_conf, post_loop_conf, loop_outcome, loop_type, loop_reason) are defined in **Cursor-Skill-Pipelines-Reference** § Log format, backup path, and loops. Include **backup path** in the log entry (e.g. in the `changes` string) when a backup was created. <!-- Gap filled from old Cursor-Skill-Pipelines-Reference.md -->
