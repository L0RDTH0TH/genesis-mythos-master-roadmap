---
description: MCP Obsidian integration — tool chaining, logging, safety, and fallbacks
globs: "*"
alwaysApply: true
---

# MCP Obsidian integration

## Folder blacklist & canonical names (this vault only)

**BLACKLIST — never use or reference:** `00 Inbox`, `10 Zettelkasten`, `99 Attachments`, `99 Templates`. Do not create or propose any new PARA or folder patterns; use only what is defined here and in [[3-Resources/Second-Brain/Vault-Layout]].

| Use (correct) | Never use |
|---------------|-----------|
| **Ingest** | 00 Inbox |
| **Templates** | 99 Templates |
| **5-Attachments** or **Attach** | 99 Attachments |
| *(no such folder)* | 10 Zettelkasten — use PARA roots and subfolders only |

All path proposals, `obsidian_ensure_structure`, classify/subfolder outputs, and logs: **Ingest**, **Templates**, **5-Attachments** (or **Attach**), **1-Projects**, **2-Areas**, **3-Resources**, **4-Archives** only.

---

- Use **obsidian-mcp-server** from **global config only** (`~/.cursor/mcp.json`); do not use project-level setup scripts.
- **Ingest processing**: Follow para-zettel-autopilot; chain MCP tools: **obsidian_create_backup** (first), then `obsidian_classify_para`, `obsidian_split_atomic`, `obsidian_distill_note`, `obsidian_append_to_hub`, `obsidian_move_note`, `obsidian_log_action`; verify after each step. For destructive steps, also call the **obsidian-snapshot** skill (see `.cursor/skills/obsidian-snapshot/SKILL.md`) to create a per-change snapshot before proceeding. **Non-markdown in Ingest:** handle per ingest-processing and non-markdown-handling rules; create companion .md then attempt move of original to 5-Attachments/[subtype]/ via obsidian_ensure_structure + obsidian_create_backup + obsidian_move_note (backup required first; on success omit #needs-manual-move; on failure leave in Ingest/ with #needs-manual-move and log). Exception: the optional move-attachment-to-99 skill may run `mv` only for Ingest → 5-Attachments/ when explicitly invoked by the user.
- **Option C – Zero-Manual**: Every ingest starts with a backup; destructive MCP calls use internal ensure_backup gate; never propose cp/mv/rm shell commands except the move-attachment-to-99 skill (narrow exception: Ingest → 5-Attachments/ only, user-invoked); log backup_path(s) from create_backup in Ingest-Log.md. Snapshots add an additional, in-vault safety layer and must never replace external backups.
- **ensure_backup vs create_backup**: Before long batches or after a gap (e.g. >15 minutes), call **`obsidian_ensure_backup`**(path, max_age_minutes) to confirm a recent backup exists; only call **`obsidian_create_backup`** when ensure_backup indicates one is needed or missing. Suggested default: `max_age_minutes: 1440` (24 hours) for most users/batches; allow tighter values (e.g. 60–180 min) for very active ingest runs. Keeps the "no destructive action until backup exists" invariant while reducing redundant backups.
- **Prompt → action**: read note → `obsidian_read_note`; move → classify then propose path; search → `obsidian_global_search`; list folder → `obsidian_list_notes`; update/append → `obsidian_update_note` / `obsidian_search_replace`; frontmatter/tags → `obsidian_manage_frontmatter` / `obsidian_manage_tags`.
- **Queue-aware tools**: When processing queue (EAT-QUEUE), dispatch by mode (BATCH-DISTILL, BATCH-EXPRESS, SEEDED-ENHANCE, ASYNC-LOOP, etc.); use batch snapshot when batch size > batch_size_for_snapshot. Gradients/layers are applied by skills (e.g. highlight-perspective-layer) + CSS + frontmatter unless a dedicated MCP tool is added later.
- **Logging**: Append short entries to mcp-setup-log.md or Ingest-Log.md after MCP calls. Include backup path in the `changes` string or log line when available. Snapshot calls should also be logged to `3-Resources/Backup-Log.md` with original note path, snapshot path, pipeline, confidence, and any `#review-needed` flags.
- **Safety**: Prefer read and propose over delete/overwrite; no hardcoded API keys.

## Snapshot configuration

- The Obsidian MCP server uses three filesystem roots for safety:
  - `BACKUP_DIR` — external, immutable-like backups created by `obsidian_create_backup` (e.g. `/home/darth/Documents/Second-Brain-oops-Backups`). Treat this as the last-resort recovery location and store it on encrypted or otherwise protected storage when the vault is synced or shared.
  - `SNAPSHOT_DIR` — in-vault per-change snapshots for human-visible, Dataview-friendly rollbacks (e.g. `/home/darth/Documents/Second-Brain/Backups/Per-Change`). Files here are append-only and should never be edited by skills or rules.
  - `BATCH_SNAPSHOT_DIR` — in-vault batch checkpoint notes summarizing groups of changes (e.g. `/home/darth/Documents/Second-Brain/Backups/Batch`).
- Always ensure that `SNAPSHOT_DIR` and `BATCH_SNAPSHOT_DIR`:
  - Live **inside the vault** but **outside** any globbed rule scopes like `Ingest/*` to avoid recursive processing.
  - Are not used as working directories for other tools; only snapshot and restore-related logic should touch them.

### Version-snapshot create behavior (2026-02-25 update)

- **`obsidian_update_note` with `mode: "create"`** is used by the version-snapshot skill when writing a **new** version file under `Versions/`. The server **skips the destination backup gate** for this mode (no backup required for the target path, since it does not exist yet). The **source note** is always backed up at pipeline start via `obsidian_create_backup`, and the obsidian-snapshot skill can create a per-change snapshot of the source before any appends; the version file is an additional narrative copy, not a substitute for source backup/snapshot.
- Version paths use timestamped filenames `<original_slug>--<YYYYMMDD-HHMMSS>.md` so each run targets a non-existent path and the create succeeds. If the path already exists, the server fails the create (no overwrite); the skill uses a fresh timestamp per run to avoid collisions.

### Integrate snapshots into external backups

- **External backups** (e.g. rsync, restic, Obsidian Sync, or a local backup plugin) **SHOULD** include `SNAPSHOT_DIR` and `BATCH_SNAPSHOT_DIR` for full point-in-time recovery. These paths are exposed as environment variables for the Obsidian MCP server in `~/.cursor/mcp.json` (under `obsidian-para-zettel-autopilot` → `env`). Backup scripts or tools can read the same paths from that config to include in vault-wide backups.
- If using naive full backups, consider **incremental or deduplicating** tools (e.g. restic, Borg, rclone with versioning) so that repeated snapshot runs do not bloat backup storage; per-change and batch snapshots accumulate over time.
- See `3-Resources/enhanced-snapshots.md` for a short reference and tool suggestions.

### Batch snapshot threshold

- **batch_size_for_snapshot**: Read from [3-Resources/Second-Brain-Config](3-Resources/Second-Brain-Config.md) (e.g. default 5). When **queue length or batch size > this value**, use **BATCH_SNAPSHOT_DIR** for the run (one batch snapshot for the group). When **≤ this value**, use **per-change** snapshots per note as usual. Fine-tunes overhead: large batches get one batch snapshot; small/mobile single-item runs stay per-change.

### Snapshot chaining guidelines

- Before any destructive MCP call (moves, renames, deletes, or substantial overwrites), the agent should:
  1. Confirm **confidence ≥85%** for the underlying action.
  2. Call the **obsidian-snapshot** skill with `type: "per-change"` for the target note.
  3. If snapshot creation succeeds, proceed with the destructive step.
  4. If snapshot creation fails (misconfigured directories, write failure, integrity issues):
     - Skip the destructive action for that note.
     - Log the error and snapshot failure in `3-Resources/Backup-Log.md` with `#review-needed`.
     - Continue with the next note in the batch.
- **Path before every move**: Before any **`obsidian_move_note`**, call **`obsidian_ensure_structure`**(folder_path: *parent directory of new_path*) so the target path exists (create if missing). This applies to all pipelines (ingest apply-mode, organize, archive, non-md move). Idempotent when the path already exists.
- **Remove empty folder**: Use **`obsidian_remove_empty_folder`**(folder_path, dry_run: true then false) for post-archive (and optionally post-organize) ghost-folder cleanup. All vault mutations via MCP only—no shell rmdir. See archive-ghost-folder-sweep skill and MCP-Tools.md Folder ops.
- **Dry-run before every move**: For any **`obsidian_move_note`** at ≥85% confidence, the agent must first call **`obsidian_move_note`**(path, new_path, `dry_run: true`), review returned effects (path, new_path, backup status, risks e.g. dangling links), then call again with `dry_run: false` to commit. No move commit without a prior successful dry_run review.
- **Post-move frontmatter sync**: After every successful **`obsidian_move_note`**(..., `dry_run: false`): (1) If new_path is under a PARA root (1-Projects, 2-Areas, 3-Resources, 4-Archives), set **para-type** on the note at new_path from the first segment (1-Projects→Project, 2-Areas→Area, 3-Resources→Resource, 4-Archives→Archive) via **`obsidian_manage_frontmatter`**. (2) If new_path is under **1-Projects/** and has a second path segment (project folder), set **project-id** to that segment (slugified). (3) If new_path is under **4-Archives/**, set **status** to **archived**. If destination is not under a PARA root (e.g. 5-Attachments), skip all.
- Destructive MCP calls covered by this rule include at least:
  - `obsidian_split_atomic`
  - `obsidian_distill_note` when it rewrites content
  - `obsidian_append_to_hub` when it appends into other notes
  - **task-reroute** (per-change snapshot of **target** note before `append_tasks`)
  - `obsidian_move_note`
  - `obsidian_rename_note` (including when **name-enhance** skill applies a rename in organize or NAME-REVIEW)
  - `obsidian_delete_note`

### Security considerations

- Snapshots in `Backups/` are copies of note content. When the vault is synced or published:
  - Prefer to keep `Backups/` and `BACKUP_DIR` on encrypted storage or excluded from any public repos.
  - Do not rely on snapshots as an access-control boundary; treat them as additional history, not as a security feature.

### Roadmap state invariants (multi-run)

When reading or writing **roadmap-state.md** under `1-Projects/<project_id>/Roadmap/`:

- **Never advance `current_phase`** unless ALL prior phases have confidence ≥ 85% (per Parameters roadmap.conf_phase_complete_threshold).
- **Snapshot roadmap-state.md before AND after every update** (obsidian-snapshot skill with type per-change). State is versioned and snapshotted like phase notes.
- **If roadmap-state.md parse fails** (invalid YAML, missing required frontmatter such as `current_phase`, `status`) → abort the roadmap pipeline, log to [Errors](3-Resources/Errors.md) with **#state-corrupt**, and create a Decision Wrapper under `Ingest/Decisions/Errors/`: "Fix state.md or revert?" with options to repair state or reset. Do not proceed with resume or phase generation.

See [Vault-Layout](3-Resources/Second-Brain/Vault-Layout.md) § Roadmap state artifacts for the roadmap-state.md schema.

## MCP fallback table

When an MCP call fails due to path or structure issues, use the following behavior:

| Scenario | Action |
|----------|--------|
| **obsidian_move_note** fails (e.g. "parent does not exist" or target directory missing) | Call **obsidian_ensure_structure** with **folder_path** set to the target parent (e.g. `4-Archives/Test-Project-Archive/Subtheme`), then retry **obsidian_move_note**. If ensure_structure is not available or fails, log the error and propose the user create the parent directory manually; do not proceed with move. |
| **obsidian_move_note** `dry_run` reports high-risk items (dangling links, overwrite conflicts, missing parents) **or** the actual move fails later | Trigger **`propose_alternative_paths`** (backed by `propose_para_paths` on the MCP server) → obtain ranked PARA path candidates with reasons, feed top-1 or top-2 into **`calibrate_confidence`** (single retry) → **`verify_classification`** → `dry_run` again → commit; else append full `dry_run` output + error trace to log with `#review-needed` and pause that note. All pipelines (ingest, organize, archive) reference this same chain; do not duplicate fallback logic per pipeline. |
| **obsidian_update_note** to a **new path** fails (e.g. file does not exist and parent dir missing) | For **version-snapshot** (new file under `Versions/`): use `obsidian_update_note(path, content, mode: "create")` so the server skips the destination backup gate. For other new-file cases: use `obsidian_read_note` + `obsidian_update_note(path, content, mode: overwrite)` or `mode: "create"` if the server supports it. If the server does not create parent dirs, call **obsidian_ensure_structure** for the parent path first; otherwise propose creating the parent path manually. |
| **obsidian_create_backup** fails | Abort the pipeline. Do not proceed with any destructive or move operations. Log the failure and flag #review-needed. |

Document actual MCP server behavior (e.g. whether parent dirs are created automatically) in this rule or in the pipelines reference when confirmed.

## Documented behavior (verified 2026-02-25)

Deep-nested PARA move behavior verified from MCP server and Obsidian Local REST API plugin code; pipelines and skills rely on the following.

### obsidian_move_note + obsidian_ensure_structure (deep-nested PARA)

| Observation | Result |
|-------------|--------|
| Does `obsidian_move_note` create parent directories automatically? | **No.** The REST API plugin calls `vault.createFolder(dirname(filepath))` once; Obsidian's `createFolder` does not create parent folders recursively. Deep moves (3–4 levels) can fail if intermediate folders are missing. |
| Does `obsidian_ensure_structure` create full path (3–4 levels) in one call? | **Yes (with `folder_path`).** Call `obsidian_ensure_structure` with optional **folder_path** set to the target parent (e.g. `4-Archives/Test-Project-Archive/Subtheme`). The server creates that path recursively with `os.makedirs(..., exist_ok=True)`. Without `folder_path`, only top-level PARA folders are created. |
| If target path already exists (file at `new_path`), what happens? | **Overwrite.** Move is copy-then-delete; PUT overwrites existing file. Backup gate and per-change snapshot (before move) are the safety net; no separate "target exists" check. |
| Already-exists folders when using `obsidian_ensure_structure`? | **Idempotent.** Existing directories are skipped; safe to call multiple times. |
| Case-sensitivity / invalid characters in path? | Paths are used as-is; no normalization. Invalid filesystem characters can cause errors. |

**Required flow for every move:** Backup → (optional) per-change snapshot → **obsidian_ensure_structure**(folder_path: *parent of new_path*) → **obsidian_move_note**(path, new_path, `dry_run: true`) → review effects → **obsidian_move_note**(path, new_path, `dry_run: false`) → **then** set para-type (and when under 1-Projects/ project-id, when under 4-Archives/ status: archived) on the note at new_path (see "Post-move frontmatter sync" above). The ensure_structure step is mandatory so synthetic or non-existent target paths are created before the move.

### Health check and observability

- Every N notes (e.g. 10) in a batch, or on first error in a run, call **`health_check`** and log result (status, metrics, serverIdentifier). Prefer a dedicated note **`3-Resources/MCP-Health-YYYY-MM.md`** (monthly rotation); fallback to Backup-Log.md or `3-Resources/MCP-Observability.md` if preferred.
- When **`health_check`** returns non-OK status, automatically call **`obsidian_ensure_backup`** as a defensive measure before continuing the batch.

## Error Handling Protocol (all pipelines)

When **any** pipeline or workflow step fails (MCP call error, classification failure, I/O or plugin error, heuristic/scoring exception, or unexpected state):

1. **Trace**
   - Capture: timestamp (ISO 8601), pipeline name, pipeline stage/step name, affected note path(s), raw error message or stack trace (sanitize: no API keys or secrets).
   - Optional context: Obsidian/MCP server status if available (e.g. from `health_check`), plugin state only if relevant (e.g. "Highlightr unavailable").

2. **Summarize**
   - Produce a short **summary** (2–4 sentences) with:
     - **Error type/category**: Quick classifier for filtering/grouping — one of: `io-failure`, `mcp-api`, `classification-empty`, `plugin-unavailable`, `confidence-below-threshold`, `state-inconsistent` (or similar; extend as needed).
     - **Root cause** (if detectable): e.g. "Parent directory missing", "Classification returned empty", "Backup write failed".
     - **Impact**: Which note(s) were partially processed; which steps were skipped.
     - **Suggested fixes**: From heuristics (e.g. "Run obsidian_ensure_structure for target parent"; "Retry after ensure_backup"; "Manual move required").
     - **Recovery**: e.g. "Rollback: restore from Backups/Per-Change/<snapshot>"; "Retry with dry_run only"; "No destructive action was taken."

3. **Log and notify**
   - Append a **single error entry** to **`3-Resources/Errors.md`** (create the note if it does not exist). Entry format (no fenced YAML per entry; Dataview-friendly):
     - Heading: **`### YYYY-MM-DD HH:MM — Short Title`**
     - Immediately below: a small **inline table** for metadata: `pipeline`, `severity`, `approval`, `timestamp`, `error_type`.
     - Then **`#### Trace`** (bullet list or code block).
     - Then **`#### Summary`** with bold subheadings: **Root cause**, **Impact**, **Suggested fixes**, **Recovery**.
  - Also append a **one-line reference** in the **pipeline-specific log** (Ingest-Log, Distill-Log, Archive-Log, Express-Log, Organize-Log, or Backup-Log as appropriate), e.g. `Error logged: [[3-Resources/Errors.md]] (entry YYYY-MM-DD HH:MM)`.
  - **Create an error Decision Wrapper** under **`Ingest/Decisions/Errors/`** so the user has a single touchpoint for recovery. Set `wrapper_type: error`, `pipeline` (from the failed pipeline), `original_path` (affected note), `clunk_severity: high` when severity is high (e.g. backup/snapshot failed) or `clunk_severity: medium` when severity is medium (e.g. dry_run risk). In the wrapper body, link to the Errors.md entry (e.g. `Error entry: [[3-Resources/Errors.md#YYYY-MM-DD HH:MM — Short Title]]` or `error_entry: "### YYYY-MM-DD HH:MM — Short Title"`). Fill options A–G with recovery-focused choices: e.g. "Force backup then retry", "Use alternative path", "Pause this note", "Log full trace and skip", "Retry dry_run only", "Manual move", "Ignore". Use `Templates/Decision-Wrapper.md`; ensure `obsidian_ensure_structure`(folder_path: "Ingest/Decisions/Errors"); ensure CHECK_WRAPPERS entry exists; append Watcher-Result line `message: "created wrapper → Decisions/Errors/<basename>"`.
  - If **severity is high** or **confidence is low** and the error is **critical** (e.g. backup failed, snapshot failed before destructive step):
     - Set `approval: pending` in the entry table and add `#review-needed` in the entry text (flag for user review). A dedicated Inbox Review hub can be added later via Dataview if needed.
     - **Pause the pipeline for the current note**: skip all remaining destructive steps for that note, continue with the next note in the batch (do not halt the entire batch unless it is a global failure such as `obsidian_create_backup` at run start).

4. **Integrate with existing safeguards**
   - **Rollback**: Do **not** auto-restore. If a per-change snapshot was created **before** the failing step, document its path in the error entry under "Recovery" so the user can run RESTORE MODE. If no snapshot exists (e.g. failure before snapshot), state "No snapshot; backup at BACKUP_DIR may be used if available."
   - **Progressive fallbacks**: Before writing an error entry, the agent MUST have attempted the fallbacks already defined in this rule (e.g. `obsidian_ensure_structure` then retry move; `propose_alternative_paths` → calibrate → verify → dry_run again). Only after fallbacks are exhausted, log to Errors.md.
   - **Severity threshold**: Treat as **high** when: backup creation failed; snapshot creation failed immediately before a destructive step; move/rename/delete failed after dry_run was approved; or any error that could leave a note in an inconsistent state. Treat as **medium** when a non-destructive step failed (e.g. classify returned low confidence). Treat as **low** when the failure is cosmetic or recoverable without user action (e.g. optional step skipped).

This protocol does not replace pipeline-specific "On failure" bullets; it standardizes **what** to write to Errors.md and **when** to escalate. Each pipeline rule references this section and adds pipeline-specific stage names.

**Deepen-specific (roadmap-deepen):** When **estimated_tokens > context_window_tokens × 0.9** (90% of window), treat as failure: **error_type: context-overflow**; log to Errors.md with #review-needed; append Watcher-Result failure; queue RECAL-ROAD (RESUME-ROADMAP action recal). Do not queue another deepen until recal has run. See roadmap-deepen skill § Overflow check.

*Test path used for verification:* `4-Archives/Test-Project-Archive/Subtheme/2026-02-25-archive-test.md` (4 segments).

## Restore-queue mode

**Restore** from snapshots is always **user-triggered**. **restore-queue** mode: user maintains a list (e.g. in Errors.md or a dedicated `3-Resources/Restore-Queue.md`) of snapshot paths to restore. Format: one path per line or a table with columns `snapshot_path`, `original_path` (optional). Processor reads the list and runs restore steps one-by-one: read snapshot content → write to original path (or specified target). No auto-restore; no automatic deletion of snapshots. Document the list format in Logs.md or Backup-Log so users know how to enqueue restores.
