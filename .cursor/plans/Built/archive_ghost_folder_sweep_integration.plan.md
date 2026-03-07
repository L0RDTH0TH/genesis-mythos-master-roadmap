---
name: ""
overview: ""
todos: []
isProject: false
---

# Archive ghost-folder sweep — integration plan

## Context

The MCP server already implements `**obsidian_remove_empty_folder**` and the **archive-ghost-folder-sweep** skill exists (on the MCP side or in the skill folder). This plan covers **vault-side integration only**: wiring the tool and skill into rules, pipeline reference, MCP docs, queue/Commander, logging, confidence bands, and testing. **All vault mutations for empty folders use the MCP tool only** — no rmdir/shell exception (per mcp-obsidian-integration § MCP usage and safety).

**Pre-existing (no build):**

- **MCP tool**: `obsidian_remove_empty_folder` — params: `folder_path` (required), `dry_run` (default `"true"`), `recursive`, `force`, `blacklist` (optional), `root_path`, `retry_count`. Server uses `archive_folder_blacklist` from `~/.cursor/mcp.json` or `ARCHIVE_FOLDER_BLACKLIST` env. Protects PARA roots, Templates, `.technical`, Backups, and config blacklist. **Extensibility**: Callable from other skills (e.g. post-organize cleanup in autonomous-organize).
- **Skill**: `archive-ghost-folder-sweep` — see §1 for full algorithm (backup gate, candidates, loop tool calls, confidence bands, logging).

---

## 1. Skill: algorithm and behavior (SKILL.md)

**File**: `[.cursor/skills/archive-ghost-folder-sweep/SKILL.md](.cursor/skills/archive-ghost-folder-sweep/SKILL.md)`. Ensure it exists; add from Grok/MCP output if missing, then align to the following.

**Key change — no rmdir**: Replace any “rmdir” or shell-removal wording with a **loop over candidates** using only the MCP tool:

- For each candidate folder: call `**obsidian_remove_empty_folder`**(folder_path: candidate, dry_run: true) → review effects → if OK, call again with dry_run: false to commit.
- No shell exception; preserves “all vault mutations via MCP” invariant and makes the sweep auditable/extensible (e.g. future recursive mode).

**Backup/snapshot gate** (per [Skills-Structure-Detailed](3-Resources/Second-Brain/Second-Brain-User-Flows/Skills-Structure-Detailed.md) backup gate):

- **Before** the candidate loop: call **obsidian_ensure_backup**(max_age_minutes: 1440 from [Second-Brain-Config](3-Resources/Second-Brain-Config.md)) or fallback to **obsidian_create_backup**. Archive already backs up notes; this gate covers folder ops.
- If candidate count **> batch_size_for_snapshot** (e.g. 5 from [Parameters](3-Resources/Second-Brain/Parameters.md)), call **obsidian-snapshot** (batch mode) and log batch snapshot path to [Backup-Log](3-Resources/Backup-Log.md).

**Confidence bands & loop** (per [confidence-loops](.cursor/rules/always/confidence-loops.mdc) always-applied):

- **High ≥85%**: Commit removes after snapshot (and backup gate above).
- **Mid 68–84%**: Preview candidate list in Archive-Log with `#review-needed`; run **one refinement loop** (re-verify empty via obsidian_list_notes); then commit only if post_loop_conf ≥85%. Log loop_* fields (loop_attempted, loop_band, pre_loop_conf, post_loop_conf, loop_outcome, loop_type, loop_reason).
- **Low <68%**: Propose only; no removals. Log proposal.
- If **>10 candidates**, call **calibrate_confidence** before committing.
- **Extensibility**: Mid-band can emit preview to [Mobile-Pending-Actions](3-Resources/Mobile-Pending-Actions.md) per [User-Flow-Diagram-Detailed](3-Resources/Second-Brain/Second-Brain-User-Flows/User-Flow-Diagram-Detailed.md) for async approval.

**Candidate computation** (in SKILL.md):

- From `moved_notes_list`: for each path, extract all parent folders up to (but not including) PARA root. **Deduplicate** (set unique). **Sort deepest-first** (reverse by path segment count).
- **Skip** any candidate that appears in **folder_blacklist** (read from [Second-Brain-Config](3-Resources/Second-Brain-Config.md) or [Parameters](3-Resources/Second-Brain/Parameters.md); default e.g. `["/Templates/", "/.technical/"]`).
- **Verify empty** for each candidate via **obsidian_list_notes**(directory: candidate); treat as empty only if no notes (recursive: false for this check unless tool supports it). Skip removal if not empty.
- **Extensibility**: Optional input param **scope: "full-para"** for broader sweeps, gated behind a config toggle (e.g. in Second-Brain-Config).

**Logging** (per [Logs](3-Resources/Second-Brain/Logs.md)):

- **Archive-Log.md** and **Backup-Log.md**: Append lines with (timestamp, pipeline: archive, actions: "removed X folders" or "no empty folders", confidence, snapshot_path, flag: #ghost-sweep). Include loop_* when a loop ran.
- **Failures**: Append to [Errors](3-Resources/Errors.md) with severity and full trace per **Error Handling Protocol** in mcp-obsidian-integration. Tag #review-needed when appropriate.
- **Observability**: Entries are aggregateable in [Vault-Change-Monitor](4-Archives/Resources/Vault-Change-Monitor.md) MOC via Dataview (e.g. “Ghost sweeps this week”).
- **Extensibility**: Merge with **user_guidance** via [guidance-aware](.cursor/rules/always/guidance-aware.mdc) (e.g. “skip these folders”) when guidance is present.

---

## 2. Auto-archive rule: trigger sweep after moves

**File**: `[.cursor/rules/context/auto-archive.mdc](.cursor/rules/context/auto-archive.mdc)`

- In the **pipeline overview** (numbered list), add **Step 8** after Step 7 (Logging):
  - **8. Ghost-folder sweep**: After all `obsidian_move_note` and `obsidian_log_action` steps for the run, if **at least one note was moved**, invoke **archive-ghost-folder-sweep** with `moved_notes_list` = list of **source paths** (original paths before move) of notes successfully moved. Agent accumulates this list during the run. Sweep uses only `obsidian_remove_empty_folder` (dry_run then commit); no shell rmdir. Log result in Archive-Log with flag `#ghost-sweep`.
- Add **“Ghost folders”** subsection (e.g. after “Batch and isolation” or “Logging requirements”):
  - Sweep runs only for folders that had files moved in **this** archive run (scope: archive-run-only).
  - Only verified-empty folders are removed; MCP tool enforces empty-check and blacklist. No global empty-folder cleanup.
  - **All** empty-folder removal is via `**obsidian_remove_empty_folder`** — no rmdir or other shell file ops (preserves mcp-obsidian-integration invariant).

---

## 3. MCP rule: document tool; no rmdir exception

**File**: `[.cursor/rules/always/mcp-obsidian-integration.mdc](.cursor/rules/always/mcp-obsidian-integration.mdc)`

- **Do not add** any “rmdir exception” or shell-removal exception for archive (or elsewhere). Shell ops are explicitly discouraged per § MCP usage and safety; all vault mutations use MCP (e.g. move_note’s dry_run pattern). The new tool is the single way to remove empty folders.
- **Add** a short reference to `**obsidian_remove_empty_folder`** in the “Prompt → action” or “Path before every move” area: use for post-archive (and optionally post-organize) empty-folder removal; dry_run then commit; server enforces empty-check and blacklist. Config: `archive_folder_blacklist` / `ARCHIVE_FOLDER_BLACKLIST` (see MCP-Tools.md).

---

## 4. MCP-Tools.md: Folder ops group and descriptor

**File**: [3-Resources/Second-Brain/MCP-Tools.md](3-Resources/Second-Brain/MCP-Tools.md)

- Add a **“Folder ops”** group (alongside Move/structure) with:
  - **obsidian_ensure_structure** (existing)
  - **obsidian_remove_empty_folder** (new)
- **Descriptor** for `obsidian_remove_empty_folder`:
  - **folder_path** (required): vault-relative path to the folder to remove.
  - **dry_run** (default true): if true, report effects only; no filesystem change. Always dry_run first, then commit (dry_run: false) if OK.
  - **recursive**: false (default); future use for recursive empty removal.
  - **force**: false (default); server may use for override in edge cases.
  - **blacklist**: optional JSON override; otherwise server uses `archive_folder_blacklist` from mcp.json or `ARCHIVE_FOLDER_BLACKLIST` env.
- Note: Used by archive-ghost-folder-sweep; **extensible** to other skills (e.g. post-organize cleanup). Update the tool-groups table and, if present, the Mermaid diagram.

---

## 5. Pipeline reference and Skill locations

**File**: [3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference.md](3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference.md)

- **autonomous-archive** table (§3): Add row **archive-ghost-folder-sweep** | after all moves and log_action (once per sweep) | Remove empty source folders left after archive moves; only folders that had files moved in this run; loop over candidates with obsidian_remove_empty_folder (dry_run then commit). | Run only when moved_notes_list non-empty.
- **Pipeline order**: … → move_note (dry_run first, then commit) → log_action → **archive-ghost-folder-sweep** (if any moves in this run).
- **Skill locations**: Add archive-ghost-folder-sweep | .cursor/skills/archive-ghost-folder-sweep/SKILL.md

---

## 6. Queue and Commander integration (required)

- **Queue-Sources.md** ([3-Resources/Second-Brain/Queue-Sources.md](3-Resources/Second-Brain/Queue-Sources.md)): Add mode **ARCHIVE-GHOST-SWEEP** to prompt-queue.jsonl supported modes. Payload: optional `moved_notes_list`; if absent, agent scans recent Archive-Log for moved paths.
- **auto-eat-queue.mdc** ([.cursor/rules/context/auto-eat-queue.mdc](.cursor/rules/context/auto-eat-queue.mdc)): Add dispatch branch: when `mode == "ARCHIVE-GHOST-SWEEP"`, read payload.moved_notes_list (fallback: recent Archive-Log scan) and run archive-ghost-folder-sweep.
- **Queue-Alias-Table.md** ([3-Resources/Second-Brain/Queue-Alias-Table.md](3-Resources/Second-Brain/Queue-Alias-Table.md)): Add alias **"SWEEP GHOSTS"** → ARCHIVE-GHOST-SWEEP (and optionally “CLEAN GHOST FOLDERS”).
- **Commander-Plugin-Usage.md** ([4-Archives/Resources/Plugins-Usage/Commander-Plugin-Usage.md](4-Archives/Resources/Plugins-Usage/Commander-Plugin-Usage.md)): Add macro **“Sweep Ghost Folders”** that enqueues ARCHIVE-GHOST-SWEEP; prompt user for dry_run (true/false). **Extensibility**: Mobile trigger (queue on phone, EAT-QUEUE on laptop).

---

## 7. Backbone docs and config

- **Configs** ([3-Resources/Second-Brain/Configs.md](3-Resources/Second-Brain/Configs.md) or Second-Brain-Config): Document **archive_folder_blacklist** (mcp.json) and **ARCHIVE_FOLDER_BLACKLIST** (env, JSON array). Document **folder_blacklist** (or equivalent) for skill candidate filtering if stored in config (default e.g. ["/Templates/", "/.technical/"]).
- **Skills.md** ([3-Resources/Second-Brain/Skills.md](3-Resources/Second-Brain/Skills.md)): Add table row:
  - | archive-ghost-folder-sweep | .cursor/skills/archive-ghost-folder-sweep/SKILL.md | autonomous-archive | post-moves | Remove empty ancestors via MCP tool | Collect/sort candidates, loop tool calls, log.
- **Rules.md** ([3-Resources/Second-Brain/Rules.md](3-Resources/Second-Brain/Rules.md)): In auto-archive summary, add **“Ghost folders”** subsection: Invoke archive-ghost-folder-sweep after moves when moved_notes_list non-empty; MCP tool only, no shell.
- **README.md** ([3-Resources/Second-Brain/README.md](3-Resources/Second-Brain/README.md)) **Changelog**: Add line: “Added ghost sweep skill + MCP tool integration for archive pipeline.”

---

## 8. Testing (per Testing.md)

**File**: [3-Resources/Second-Brain/Testing.md](3-Resources/Second-Brain/Testing.md) — reference and extend as needed.

- **Unit**: In **tests/unit/** (or equivalent under [3-Resources/Second-Brain/tests](3-Resources/Second-Brain/tests)): Add fixture that mocks `moved_notes_list` → compute sorted candidate list (dedup, deepest-first); assert empty-check behavior (obsidian_list_notes stub). Optional: fixture for **blacklisted** folders (candidates in folder_blacklist are skipped).
- **Integration**: Run archive + sweep on a **tests/integration/** (or tests/fixtures) subdir: create structure (e.g. 1-Projects/Test-Ghost/Sub/), move the only note to 4-Archives/, run sweep; assert no ghost folders remain and Archive-Log (and Backup-Log) entries match expected format.
- **Regression**: Include ghost-sweep in [Regression-Stability-Log](3-Resources/Second-Brain/Regression-Stability-Log.md); track **ghost flip-rate** (e.g. folders left empty vs removed) with target **<10%** regression.

---

## 9. Sync folder and changelog

- **.cursor/sync**: Add or update `.cursor/sync/skills/archive-ghost-folder-sweep.md` to match SKILL.md; update `.cursor/sync/rules/context/auto-archive.md` with Step 8 and Ghost folders subsection. **No other sync folder changes** required if already set up.
- **changelog**: Append to `.cursor/sync/changelog.md`: e.g. “archive-ghost-folder-sweep: integrate with auto-archive (Step 8); MCP tool only (no rmdir); Folder ops in MCP-Tools; queue ARCHIVE-GHOST-SWEEP + Commander macro; confidence bands, backup gate, logging per Logs.md; tests and Regression-Stability-Log.”

---

## Summary checklist


| Task                             | Action                                                                                                                                                                                                                       |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SKILL.md                         | Ensure exists; algorithm: backup gate → candidates (dedup, blacklist, deepest-first) → verify empty → **loop obsidian_remove_empty_folder** (dry_run then commit). Confidence bands + loop_*; logging per Logs.md. No rmdir. |
| auto-archive.mdc                 | Step 8 (sweep when moves > 0); Ghost folders subsection; MCP tool only.                                                                                                                                                      |
| mcp-obsidian-integration         | Document tool reference; **remove** any rmdir exception.                                                                                                                                                                     |
| MCP-Tools.md                     | Folder ops group; descriptor (folder_path, dry_run default true, recursive: false, force: false).                                                                                                                            |
| Cursor-Skill-Pipelines-Reference | archive-ghost-folder-sweep in table + pipeline order + Skill locations.                                                                                                                                                      |
| Queue + Commander                | ARCHIVE-GHOST-SWEEP mode; auto-eat-queue dispatch; alias “SWEEP GHOSTS”; Commander macro “Sweep Ghost Folders” (prompt dry_run).                                                                                             |
| Backbone docs                    | Configs (blacklist); Skills.md row; Rules.md Ghost folders; README Changelog.                                                                                                                                                |
| Testing                          | Unit (candidates + empty verify); integration (archive + sweep, assert no ghosts + logs); Regression-Stability-Log (ghost flip-rate <10%).                                                                                   |
| .cursor/sync                     | Sync skill + auto-archive; changelog entry.                                                                                                                                                                                  |


No new MCP server work required; this plan is integration-only. All empty-folder removal is auditable and extensible via the MCP tool.