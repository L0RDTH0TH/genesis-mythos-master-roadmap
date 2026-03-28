---
title: archive-ghost-folder-sweep
created: 2026-03-07
tags: [pkm, second-brain, skills, archive, cleanup]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/README]]"]
---

# archive-ghost-folder-sweep

**Purpose**  
Remove empty ancestor folders of moved notes post-archive. Uses **obsidian_remove_empty_folder** (MCP tool only; no shell rmdir). Preserves invariants; extensible to other pipelines (e.g. autonomous-organize cleanup).

**Inputs** (from pipeline/queue)  
- **moved_notes_list**: array of original moved paths (required) — no log parsing; agent passes list from run context.  
- **dry_run**: boolean (default true).

**Algorithm**  
1. **obsidian_ensure_backup** (max_age_minutes: 1440 from Second-Brain-Config).  
2. Compute candidates: for each path in moved_notes_list, extract parent folders up to PARA root; **unique set**; **sort deepest-first** (/ count reverse).  
3. **Pull folder_blacklist** from [Second-Brain-Config](3-Resources/Second-Brain-Config.md): `archive.folder_blacklist` (default: `["/Templates/", "/.technical/", "/Backups/"]` plus PARA roots `1-Projects`, `2-Areas`, `3-Resources`, `4-Archives`). **Skip** any candidate that matches blacklist (pre-call). Extensibility: per-run overrides via queue payload or [user_guidance](.cursor/rules/always/guidance-aware.mdc) merge.  
4. If **len(candidates) > 5** → **obsidian-snapshot** (batch), log path to Backup-Log.md (per confidence-loops / batch gate).  
5. **Loop over candidates** (deepest-first): for each candidate, call **obsidian_remove_empty_folder**(folder_path: candidate, dry_run: true) → review effects → if OK, call again with dry_run: false to commit. No rmdir or other shell ops.  
6. If dry_run looked good for a candidate → commit that candidate (dry_run: false).  
7. Log to Archive-Log.md; on failure append to Errors.md (Error Handling Protocol).

**Confidence bands** (per [confidence-loops](.cursor/rules/always/confidence-loops.mdc))  
- **High ≥85%**: Commit after ensure_backup/snapshot.  
- **Mid 68–84%**: Preview candidate list in Archive-Log.md + #review-needed + one refinement loop (re-verify empty); then commit only if post_loop_conf ≥85%. Ties into async preview ([Mobile-Pending-Actions](3-Resources/Mobile-Pending-Actions.md) per User-Flow-Diagram-Detailed when applicable).  
- **Low <68%**: Propose only; no removals.

**Logging** (per [Logs](3-Resources/Second-Brain/Logs.md))  
`timestamp | pipeline: archive | actions: "removed X folders" | confidence | snapshot_path | flag: #ghost-sweep`
