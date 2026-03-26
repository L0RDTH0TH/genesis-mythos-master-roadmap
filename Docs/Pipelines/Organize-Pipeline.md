# Organize Pipeline

**Version: 2026-03 – post-subagent migration**

Documents the autonomous-organize pipeline: re-classify, re-path, frontmatter-enrich, name-enhance, move in 1/2/3 when confidence ≥85%.

---

## Purpose

Single reference for organize steps, confidence bands, and return format. Implementation in `.cursor/agents/organize.md` and legacy-agents/organize.mdc. Re-org target stays under PARA, not 4-Archives. FORCE-WRAPPER with source under 1/2/3 invokes organize with force_wrapper: true.

---

## Pipeline steps

1. **Backup** — obsidian_create_backup for the note.
2. **Classify PARA** — obsidian_classify_para (para-type, status, themes).
3. **frontmatter-enrich** — status, confidence, para-type, created, links; optional project-id, priority, deadline (≥85% auto-apply).
4. **subfolder-organize** — target path under 1/2/3 (max 4 levels). Mid-band: optionally propose_para_paths (context_mode organize), calibrate, dry_run then commit.
5. **Mid-band (68–84)** — Single organize-path loop; if post_loop_conf ≥85 snapshot and move; else Decision Wrapper under Ingest/Decisions/Refinements/ (pipeline organize).
6. **Low (<68)** — Decision Wrapper under Ingest/Decisions/Low-Confidence/.
7. **name-enhance** (context organize) — opportunistic rename when suggested_name and conf ≥85% for Regular note; snapshot then obsidian_rename_note. MOC/hub/index/project root require explicit request.
8. **Per-change snapshot** — before rename (if name-enhance); before move when path_conf ≥85%.
9. **Move** — if path differs: obsidian_ensure_structure(parent) → obsidian_move_note dry_run then commit. Post-move: set para-type, project-id (when under 1-Projects/) from new path.
10. **Logging** — obsidian_log_action; Organize-Log.md, Backup-Log.md.

**Loop logging:** loop_type "organize-path". **Batch:** snapshot type "batch" ~every 3 notes. **Exclusions:** 4-Archives/, Backups/, Templates/, Log*.md, * Hub.md, watcher-protected.

**Return:** One-paragraph summary; any wrapper; Success / #review-needed / failure. Watcher-Result when requestId provided.
