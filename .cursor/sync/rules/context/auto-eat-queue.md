---
description: "Process the Watcher prompt queue: read queue (or pasted EAT-CACHE payload), validate, dedup, sort by pipeline order, dispatch by mode, log to Watcher-Result, clear passed entries only and tag failed with queue_failed."
globs: []
alwaysApply: false
---

# Auto EAT-QUEUE (context rule)

- **Pipeline**: Queue processor — read `.technical/prompt-queue.jsonl` (or pasted EAT-CACHE YAML), apply protections and ordering, dispatch each entry to the correct autonomous pipeline by `mode`, append results to Watcher-Result, clear passed entries only and tag failed/skipped with `queue_failed: true`.
- **Reference**: See `[3-Resources/Cursor-Skill-Pipelines-Reference.md](3-Resources/Cursor-Skill-Pipelines-Reference.md)` and the plan "Queue funnel and EAT-QUEUE" (sections 2b–2e).
- **MCP safety**: Always obey `[.cursor/rules/always/mcp-obsidian-integration.mdc](.cursor/rules/always/mcp-obsidian-integration.mdc)` for backups, snapshots, and fallbacks.

## How to activate

Use any of these triggers (case-insensitive):

- **EAT-QUEUE** *(canonical)*
- **Process queue**
- **EAT-CACHE** / **eat cache** *(parallel kickoff — same as EAT-QUEUE)*  
  When the user says "eat cache" (or "EAT-CACHE") without pasting content, run the queue processor and read from `.technical/prompt-queue.jsonl`. When the user **pastes** YAML with `mode: EAT-CACHE` and `queued_prompts`, use that as the queue source instead of reading the file.

When the instruction contains one of these, run the queue processor flow below. If the user pasted YAML with `mode: EAT-CACHE` and `queued_prompts`, use that as the queue source instead of reading the file.

**Optional pre-dispatch (approved proposals and Decision Wrappers — canonical ingest apply path)**: Before or after reading the queue, you may still scan for **Decision Wrappers under `Ingest/Decisions/**`** (e.g. `Ingest-Decisions/`) with `decision_candidate: true` and `approved: true` (and, optionally, `user_guidance` or `#guidance-aware`). For each such wrapper, you MAY inject a queue entry into the in-memory queue (do not write to prompt-queue.jsonl) with `mode: "INGEST MODE"`, `source_file` set to the wrapper path, and `prompt` populated from the wrapper’s `user_guidance` / “Thoughts” block; however, the **primary, persistent driver** for wrapper consumption is now the `CHECK_WRAPPERS` queue entry described below. This injected entry is still a valid route for applying ingest moves/renames, but no `obsidian_move_note` / `obsidian_rename_note` for Ingest notes should run unless it ultimately comes from an approved Decision Wrapper via either this mechanism or the `CHECK_WRAPPERS` entry. You may also scan for other notes with `approved: true` and a matching proposal id/tag to inject non-ingest entries (e.g. for organize/archive proposals). **Safety:** Only inject if the original file still exists at the path (wrapper or source note) and is not excluded (e.g. not under Backups/, not watcher-protected). Document in Queue-Sources and Templates (re-queue after edit).

### Wrapper-check requeue semantics (`CHECK_WRAPPERS` entry)

- **Purpose**: Ensure that approved Decision Wrappers are always processed **first** whenever EAT-QUEUE runs, and that wrapper checks are re-queued until all approved wrappers have been applied.
- **Queue entry shape**: A wrapper-check entry is a line in `.technical/prompt-queue.jsonl` with at least:  
  `{"mode":"INGEST MODE","prompt":"CHECK_WRAPPERS","source_file":"Ingest/Decisions/","id":"check-wrappers-<timestamp>"}`  
  Other fields (e.g. `commander_source`) are optional. Ingest Phase 1 (see para-zettel-autopilot) is responsible for **ensuring at least one such entry exists** whenever a new Decision Wrapper is created and none is present.
- **Ordering**: During step 4 (Ordering), treat any entry whose `mode` is `INGEST MODE` and whose `prompt` starts with or equals `"CHECK_WRAPPERS"` as a **meta-entry that must be processed before all other modes**, including other INGEST MODE entries. When sorting, pin these entries to the front of the queue (stable among themselves by timestamp), then apply the canonical pipeline order to the remaining entries.
- **Processed-wrapper archive**: After a wrapper is applied, it is moved to **`4-Archives/Ingest-Decisions/`** (with subfolders mirroring the live structure, e.g. `4-Archives/Ingest-Decisions/Ingest-Decisions/`) so `Ingest/Decisions/**` stays uncluttered. Wrappers are kept for training/history and are never auto-deleted. Step 0 only enumerates notes under `Ingest/Decisions/` (not the archive), so moved wrappers are no longer scanned.
- **Execution semantics**:
  - When dispatching a `CHECK_WRAPPERS` entry:
    1. **Scan wrappers**: Enumerate all markdown notes under `Ingest/Decisions/` (including subfolders such as `Ingest-Decisions/`). For each wrapper:
       - Skip if `approved: false` or explicitly marked `processed: true` (or equivalent flag such as `used_at` already set by a prior apply run).
       - If `approved: true` and not processed:
         - Use `feedback-incorporate` to resolve `approved_option` / `approved_path` into `hard_target_path` plus `guidance_text`.
         - Run an **apply-mode INGEST** pipeline for the original Ingest note (see para-zettel-autopilot “Apply-mode ingest”) using `hard_target_path` and guidance; this run may perform `obsidian_move_note` / `obsidian_rename_note` subject to confidence + snapshot gates.
         - Update the wrapper (e.g. set `used_at` and/or `processed: true`) and log in Ingest-Log that the decision was applied.
         - **Move the wrapper to the archive**: Call `obsidian_ensure_structure` with `folder_path: "4-Archives/Ingest-Decisions"`. Create a per-change snapshot of the wrapper note (obsidian-snapshot skill). Then call `obsidian_move_note`(wrapper_path, `4-Archives/Ingest-Decisions/<basename>.md`) with `dry_run: true`, review effects, then `dry_run: false` to commit. This keeps `Ingest/Decisions/` for pending wrappers only.
  - **Internal note placement and idempotency** (when adding a Wrapper state block for orphan/true-orphan wrappers): Before inserting the `## Wrapper state` block (or equivalent reserved callout), the agent must **skip appending** if (1) frontmatter already contains tag `#orphan` or `#true-orphan` (or `tags` array includes `orphan` / `true-orphan`), or (2) the note body already contains the section header `## Wrapper state` (or the reserved callout title used for the internal note). If either check fails, do not append; prevents duplicate notes on repeated EAT-QUEUE runs.
  - **Orphan tag definitions**: **#orphan** = companion (original note) is missing from expected path but still somewhere in the vault (found at P ≠ target_path). **#true-orphan** = companion is missing from expected path and from entire vault (search negative).
  - **Vault search implementation** (when resolving companion location for stale/orphan wrappers): Companion search is not magic — use an explicit call. **Primary:** Call **`obsidian_global_search`** with a query derived from the original note (e.g. filename or title from `original_path` basename). Filter results to the vault; exclude the wrapper path. Treat a single path match as "found at P"; multiple candidates may be listed in the trace. **Fallback:** If global search is unavailable or returns nothing, use **`obsidian_list_notes`** (or equivalent) and filter by **basename** of `original_path` (and optionally by note title from the wrapper). Document in the rule for future readers: "Companion search: `obsidian_global_search` with query from original_path basename (and optionally title); fallback: list_notes + basename filter." If found at P and P equals resolved `target_path` → original at target (archive wrapper). If found at P ≠ target_path → Orphan (#orphan); if not found → True Orphan (#true-orphan).
  - **CHECK_WRAPPERS Ingest-Log format**: All CHECK_WRAPPERS-related lines in Ingest-Log must follow the existing format `timestamp | Excerpt | PARA | Changes | Confidence | Proposed MV | Flag` and be **prefixed with** `CHECK_WRAPPERS: ` for greppability (e.g. `grep "CHECK_WRAPPERS:" 3-Resources/Ingest-Log.md`). Examples: apply/retry — `CHECK_WRAPPERS: <timestamp> | Retry apply (stale; original still in Ingest): <original_path> | Resource | <changes> | <conf>% | <proposed_mv or target_path> | `; stale archived — `CHECK_WRAPPERS: <timestamp> | Stale wrapper archived; original at target | ... | ... | ... | 4-Archives/Ingest-Decisions/<basename>.md | `; orphan — `CHECK_WRAPPERS: <timestamp> | Orphan; companion at P, expected at target_path | ... | ... | | | #orphan`; true orphan — `CHECK_WRAPPERS: <timestamp> | True Orphan; companion not found in vault | ... | ... | | | #true-orphan`.
    2. **Determine requeue**:
       - After scanning all wrappers, check whether **any wrappers remain** with `decision_candidate: true`, `approved: true`, and **not** marked processed.
       - If such wrappers remain, ensure that **a fresh `CHECK_WRAPPERS` entry** exists in the queue that will be written back at step 8 (Clear passed entries). This can reuse the same `source_file` (`"Ingest/Decisions/"`) and a new `id`.
       - If no unprocessed, approved wrappers remain, do **not** re-add the `CHECK_WRAPPERS` entry; wrapper checking will resume automatically when ingest creates a new wrapper and para-zettel-autopilot appends a new `CHECK_WRAPPERS` line.
  - Treat the current `CHECK_WRAPPERS` entry itself as **successful** once this scan-and-apply cycle completes; it should be removed from the queue on this run and only re-inserted when needed as above.

### Always-check wrappers (Option A — reliability)

- **Runs first, every EAT-QUEUE run**, before reading the queue. No dependency on the queue file containing a `CHECK_WRAPPERS` entry; approved wrappers are never stuck.
- **Step 0 (always-run)**:
  1. Enumerate all markdown notes under `Ingest/Decisions/` **recursively** (including subfolders such as `Ingest-Decisions/`). If this folder tree is missing or empty, proceed to step 1 (Read queue) with no further action.
  2. For each wrapper, read frontmatter. Skip if `approved: false` **and** `re-wrap` is not true (so wrappers with `re-wrap: true` are always considered for the re-wrap branch).
  3. **Branch A — approved or re-wrap, not processed:** For each wrapper with (`approved: true` **or** `re-wrap: true`) and neither `processed: true` nor `used_at` set:
     - Read wrapper frontmatter (at least `wrapper_type`, `approved_option`, `approved_path`, `original_path`, `re-wrap`, `suggested_project_name` when present).
     - Use `feedback-incorporate` to resolve `approved_option` / `approved_path` into `hard_target_path` and `guidance_text`. Treat `re-wrap: true` or `approved_option: 0` as re-wrap intent (no `hard_target_path`).
     - **Re-wrap branch (re-wrap: true or approved_option: 0 or no hard_target_path):** When the user is unhappy with options and requested re-wrap (or chose "reject all"):
       - Pull seed from wrapper: "Thoughts / corrections / why this location?" block → `guidance_text`; keep `original_path`, optional `previous_choice` (previous `approved_option` + path for traceability). Create backup (obsidian_create_backup) for the wrapper path. Create per-change snapshot of the wrapper (obsidian-snapshot skill). Call `obsidian_ensure_structure`(folder_path: `4-Archives/Ingest-Decisions/Re-Wrap/Ingest-Decisions`). Move current wrapper to `4-Archives/Ingest-Decisions/Re-Wrap/Ingest-Decisions/<basename>.md` via `obsidian_move_note`(wrapper_path, new_path) with `dry_run: true` then `dry_run: false`. Create a **new** Decision Wrapper under `Ingest/Decisions/Ingest-Decisions/` for the same `original_path` using the same template and creation logic as para-zettel-autopilot (e.g. call `propose_para_paths` in wrapper mode to get A–G candidates, fill `Templates/Decision-Wrapper.md`). Set on the new wrapper: `approved: false`; do **not** set `approved_option` or `approved_path`. Add in the new wrapper body a line linking to the archived wrapper, e.g. `Archived previous: [[4-Archives/Ingest-Decisions/Re-Wrap/Ingest-Decisions/<basename>.md]]`. Optionally set `previous_choice` in frontmatter (previous option + path). Log to Ingest-Log: `CHECK_WRAPPERS: <timestamp> | Re-wrapping <original_path> → archived <archived_path>; new wrapper at <new_wrapper_path> | ... | ... | ... | `.
     - **Path-apply (when hard_target_path is present):**
     - **Roadmap wrappers (wrapper_type: roadmap, Option A)**  
       - When `wrapper_type: roadmap` (or the original note has `is_roadmap: true`) **and** the chosen option is **A** (the synthetic “New project + full roadmap tree” choice from the wrapper), **do not** run a simple apply-mode move. Instead:
         - Treat this as “create project + roadmap tree from ingest”.
         - Call the **`roadmap-generate-from-outline`** skill with:
           - `original_note` = wrapper `original_path` (seed in Ingest/…).
           - `suggested_project_name` from wrapper/frontmatter (or from the seed title as a fallback).
           - `guidance_text` from the wrapper Thoughts / `user_guidance` block.
         - Follow the skill instructions to:
           - Ensure structure under `1-Projects/<ProjectName>/Roadmap/`.
           - Create master roadmap, phase notes, and project MOC.
           - Move the original seed into `Roadmap/Source-…` after snapshots and backup.
           - Set `roadmap_generation_status: complete` on the master roadmap.
         - On success, update the wrapper (set `used_at`, `processed: true`) and log a `CHECK_WRAPPERS` line in Ingest-Log.md noting that Option A (roadmap) was applied.
     - **All other wrappers (default apply-mode ingest)**  
       - For non-roadmap wrappers (no `wrapper_type: roadmap` or Option A not chosen), run **apply-mode INGEST** for the original Ingest note (para-zettel-autopilot “Apply-mode ingest”): backup/snapshot gates and `obsidian_move_note` (dry_run then commit) / `obsidian_rename_note` as per pipeline using `hard_target_path`.
     - In all cases, after a successful apply:
       - Update the wrapper (e.g. set `used_at`, `processed: true`) and log to Ingest-Log.md.
       - **Move the wrapper to the archive**: Call `obsidian_ensure_structure` with `folder_path: "4-Archives/Ingest-Decisions"`. Create a per-change snapshot of the wrapper note (obsidian-snapshot skill). Then `obsidian_move_note`(wrapper_path, `4-Archives/Ingest-Decisions/<basename>.md`) with `dry_run: true` then `dry_run: false`. Processed wrappers are kept in `4-Archives/Ingest-Decisions/` for training/history and never auto-deleted; `Ingest/Decisions/` stays for pending only.
  4. **Branch B — approved and processed but still in Decisions (location check required):** For each wrapper with `approved: true` and (`processed: true` or `used_at` set) and whose path is under `Ingest/Decisions/` (i.e. not already under `4-Archives/Ingest-Decisions/`), the agent **must** run a location check — do not skip. Resolve `target_path` from the wrapper (`approved_option` / `approved_path`). Run companion search: **primary** `obsidian_global_search` with query from `original_path` basename (and optionally title); **fallback** `obsidian_list_notes` + filter by basename; exclude the wrapper path. Then:
     - **If companion found at P and P equals `target_path`:** Treat as "original at target". Archive the wrapper: `obsidian_ensure_structure`(folder_path: `4-Archives/Ingest-Decisions`), per-change snapshot of wrapper (obsidian-snapshot skill), then `obsidian_move_note`(wrapper_path, `4-Archives/Ingest-Decisions/<basename>.md`) with `dry_run: true` then `dry_run: false`. Log CHECK_WRAPPERS: "Stale wrapper archived; original at target" with path `4-Archives/Ingest-Decisions/<basename>.md`.
     - **If companion found at P and P ≠ `target_path`:** Tag wrapper **#orphan** (missing from expected path but still in vault). Add `## Wrapper state` block (or equivalent reserved callout) only if not already present per idempotency (see "Internal note placement and idempotency" above). Log CHECK_WRAPPERS line with `#orphan`. Optionally move wrapper to `4-Archives/Ingest-Decisions/` with tag so Decisions stays clean.
     - **If companion not found (search negative):** Tag wrapper **#true-orphan** (missing from expected path and from entire vault). Add `## Wrapper state` block only if not already present per idempotency. Log CHECK_WRAPPERS line with `#true-orphan`. Optionally move wrapper to `4-Archives/Ingest-Decisions/` with tag.
  5. After the scan, determine **approved_wrappers_remaining**: re-enumerate `Ingest/Decisions/*.md` and set to true if any note has `decision_candidate: true`, `approved: true`, and is **not** marked processed (and has no `used_at`). This flag is used at step 8.
  6. Optionally append one line to Watcher-Result.md for this step, e.g. `requestId: check-wrappers-always | status: success | message: "Scanned N wrappers; applied M." | trace: "" | completed: <ISO8601>`.
  7. Proceed to step 1 (Read queue). Do **not** exit or skip the rest of the flow based on queue contents until after step 2.
- **When a `CHECK_WRAPPERS` entry appears in the queue** (steps 6–7): Do **not** run the wrapper execution semantics again; they were already run in step 0. Treat the entry as **successful** and remove it at step 8 (no double-apply).
- **Step 8 (Clear passed entries)**: When rewriting `.technical/prompt-queue.jsonl`, if **approved_wrappers_remaining** is true, **include one `CHECK_WRAPPERS` entry** (e.g. `{"mode":"INGEST MODE","prompt":"CHECK_WRAPPERS","source_file":"Ingest/Decisions/","id":"check-wrappers-<timestamp>"}`) in the set of lines written, so the next run has it for visibility and the always-check in step 0 will process any remaining approved wrappers.

## Queue processor flow

### 0. Always-check wrappers (runs first)

- Run the **Always-check wrappers** logic above (enumerate `Ingest/Decisions/`, Branch A: apply approved unprocessed wrappers, Branch B: location check and archive or tag #orphan/#true-orphan for processed wrappers still in Decisions, set **approved_wrappers_remaining**). Then continue to step 1.

### 1. Read queue

- **From file**: Read `.technical/prompt-queue.jsonl` from the workspace. If the file is missing or unreadable, treat as empty queue: do not run any pipeline; optionally append one line to `3-Resources/Watcher-Result.md`: `requestId: (none) | status: success | message: "Queue file missing or empty; nothing to process." | trace: "" | completed: <ISO8601>`. Exit gracefully.
- **From pasted payload**: If the user pasted YAML with `mode: EAT-CACHE` and `queued_prompts`, parse `queued_prompts` (array of objects with `id`, `timestamp`, `mode`, `prompt`, `source_file`). If missing or not an array, treat as empty and exit. If pasted content is not valid YAML, treat as empty and optionally reply that the payload could not be parsed.

### 2. Parse and validate (§2d)

- Parse the queue line-by-line (or use the parsed `queued_prompts`). For each line, try `JSON.parse(line)`. If parse fails, skip that line and count skipped (invalid) lines.
- Require each object to have at least `mode` (string). If missing or not a string, treat as invalid: skip and count.
- **Filter out past failures (§2e)**: Remove any entry where `queue_failed === true` (or `tags` includes `"queue-failed"`). Do not process these; optionally log how many were skipped as past failures.
- If after parsing and filtering there are **zero valid entries**, treat as empty/malformed: do not run pipelines; optionally append to Watcher-Result that no work was done; exit. Do not crash.
- **Fast-path for single entry**: If **valid entry count === 1**, skip steps 3 and 4 (dedup, sort) and go directly to step 5 (Dispatch).

### 3. Clean-up (dedup §2b)

- Deduplicate: same `(mode, prompt, source_file)` → keep first occurrence (by timestamp), drop later. Log collapsed count (e.g. "2 duplicate INGEST entries collapsed into 1").
- Do **not** drop entries that share the same `source_file` but have different modes (e.g. INGEST + TASK-ROADMAP for the same file); keep both and rely on ordering.
- **Queue-cleanup (slot after dedup)**: When `auto_cleanup_after_process: true` in Second-Brain-Config, after step 8 (Clear passed entries) run the **queue-cleanup** skill (see `.cursor/skills/queue-cleanup/SKILL.md`): mark failed/skipped entries `queue_failed: true`, append short summary to `3-Resources/Errors.md`.

### 4. Ordering (safety §2c)

- **Canonical pipeline order**: (after pulling any `CHECK_WRAPPERS` meta-entries to the front as described above) INGEST MODE (1) → ORGANIZE MODE (2) → TASK-ROADMAP (3) → DISTILL MODE (4) → EXPRESS MODE (5) → ARCHIVE MODE (6) → TASK-COMPLETE (7) → ADD-ROADMAP-ITEM (8). Sort all remaining entries by this order.

### 5. Dispatch (with §2d checks)

- Before running a pipeline for an entry:
  - If the entry has non-empty `source_file`, verify the file exists in the vault (e.g. `obsidian_read_note` or list notes). If the file is missing, skip this entry; append to Watcher-Result: `requestId: <id> | status: failure | message: "source_file not found: <path>" | trace: "" | completed: <ISO8601>`. Continue to the next entry.
  - If the mode (after normalization) is not in the known list (INGEST MODE, ORGANIZE MODE, DISTILL MODE, EXPRESS MODE, ARCHIVE MODE, FORCE-WRAPPER, TASK-ROADMAP, TASK-COMPLETE, ADD-ROADMAP-ITEM, SEEDED-ENHANCE, BATCH-DISTILL, BATCH-EXPRESS, ASYNC-LOOP, NAME-REVIEW, SCOPING MODE, SCOPING), skip this entry; append to Watcher-Result: `requestId: <id> | status: failure | message: "unknown or invalid mode: <mode>" | trace: "" | completed: <ISO8601>`. Continue to the next entry.
- **Match mode to pipeline**:
  - `INGEST MODE` → full-autonomous-ingest (always-ingest-bootstrap + para-zettel-autopilot). For entries whose `source_file` is an `Ingest/*.md` note (and no `hard_target_path` yet), this runs **Phase 1 (propose-only + Decision Wrapper, no moves/renames)**. For entries whose `source_file` is a Decision Wrapper under `Ingest/Decisions/` and/or where `feedback-incorporate` emits a `hard_target_path`, the ingest run is treated as **Phase 2 apply-mode** and may execute `obsidian_move_note` / `obsidian_rename_note` after snapshots and confidence checks.
  - `ORGANIZE MODE` → autonomous-organize (auto-organize).
  - `DISTILL MODE` → autonomous-distill (auto-distill).
  - `EXPRESS MODE` → autonomous-express (auto-express).
  - **`SCOPING MODE`** / **`SCOPING`** → queue alias: run **DISTILL MODE** then **EXPRESS MODE** on the **same note** (resolve `source_file` as PMG path); research-scope runs inside express. Optional: SCOPING MODE \<path-to-pmg\> in prompt or source_file. Append one Watcher-Result line per queue entry after both steps complete.
  - `ARCHIVE MODE` → autonomous-archive (auto-archive).
  - (Future) `TASK-ROADMAP`, `TASK-COMPLETE`, `ADD-ROADMAP-ITEM` → dispatch when those pipelines exist.

### 6. Run

- **Guidance-aware runs:** When about to run a pipeline for an entry with non-empty **`prompt`** or when the note at **`source_file`** has **`user_guidance`** or tag **`#guidance-aware`**, treat the run as **guidance-aware** (see guidance-aware rule): run **feedback-incorporate** to load guidance (from note `user_guidance`, from entry `prompt`, or from an associated Decision Wrapper under `Ingest/Decisions/`) and pass the resulting `guidance_text` (and any `hard_target_path` / `guidance_conf_boost` hints) into the pipeline context so that when the agent runs classify_para, subfolder-organize, name-enhance, distill_note, split_atomic, it has the guidance in context.
- **Decision Wrappers → apply-mode ingest:** For Decision Wrapper entries specifically, `feedback-incorporate` resolves `approved_option` / `approved_path` into a `hard_target_path` for the original Ingest note and emits guidance from the wrapper’s Thoughts block. The subsequent `INGEST MODE` run for that note is treated as **Phase 2 apply-mode**: Phase 1 rules (para-zettel-autopilot, always-ingest-bootstrap, ingest-processing) have already run; this run may now perform `obsidian_move_note` (dry_run then commit) and `obsidian_rename_note` when confidence and snapshot gates are satisfied. All backup/snapshot/dry_run safety from the ingest pipeline remains unchanged.
- Execute the corresponding pipeline for each entry. Backup, snapshot, and confidence rules from the pipeline reference and MCP rule apply unchanged. Process one entry fully (including logging) before starting the next.

### 7. Log

- Append one line per processed request to `3-Resources/Watcher-Result.md`:
  `requestId: <id> | status: success|failure | message: "..." | trace: "..." | completed: <ISO8601>`.

### 8. Clear passed entries only (§2e)

- Track which requestIds were logged with `status: success` vs `status: failure` (or skipped without running a pipeline).
- Rewrite `.technical/prompt-queue.jsonl` so that **only entries that failed or were skipped** remain. Remove every entry that completed with **status: success**.
- For each entry that is kept (failed/skipped), set **`queue_failed: true`** on the object before writing the line back. Thus the next EAT-QUEUE run will skip them (no automatic retry). They remain in the file until the user runs "Clear queue" in Obsidian or manually edits.
- If **approved_wrappers_remaining** (set in step 0) is true, **append one `CHECK_WRAPPERS` entry** to the rewritten queue file, e.g. `{"mode":"INGEST MODE","prompt":"CHECK_WRAPPERS","source_file":"Ingest/Decisions/","id":"check-wrappers-<timestamp>"}`, so the next run has it for visibility; step 0 will again process any remaining approved wrappers.
- If all entries passed and approved_wrappers_remaining is false, the queue file becomes empty.

## Watcher-Result contract

- When a run was triggered by EAT-QUEUE (queue or pasted EAT-CACHE), append the one-line format per processed `requestId` as above. See `[.cursor/rules/always/watcher-result-append.mdc](.cursor/rules/always/watcher-result-append.mdc)`.

## Safety

- **Step 0 always runs first**: The always-check wrappers step runs before reading the queue, so approved wrappers are processed even when the queue is empty or the `CHECK_WRAPPERS` entry was omitted.
- Do not run destructive pipelines on a note whose path is under `Ingest/` until batch INGEST has been processed in this run (ordering enforces this).
- Missing queue file or zero valid entries (after step 2) → exit without further dispatch; step 0 has already run. Missing `source_file` or unknown mode → skip entry, log failure, continue. Tagged (`queue_failed`) entries are never processed; they are only written back when they fail again.
