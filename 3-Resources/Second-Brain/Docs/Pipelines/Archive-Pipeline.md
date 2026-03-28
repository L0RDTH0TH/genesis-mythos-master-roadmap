# Archive Pipeline

**Version: 2026-03 – post-subagent migration**

Documents the autonomous-archive pipeline: move completed/inactive notes to 4-Archives/ with summary preservation, resurface markers, and ghost-folder sweep.

---

## Purpose

Single reference for archive steps, confidence bands, and return format. Implementation in `.cursor/agents/archive.md` and legacy-agents/archive.mdc. No archive-apply-from-wrapper; re-queue ARCHIVE MODE after wrapper approval to re-run.

---

## Pipeline steps

1. **Backup** — obsidian_create_backup for the note.
2. **Classify PARA** — confirm para-type and status.
3. **archive-check** — archive readiness (no open tasks, status complete, age threshold). Primary signal: archive_conf (≥85% for move).
4. **Mid-band (68–84)** — Single archive-refine loop; if post_loop_conf ≥85 snapshot and proceed; else Decision Wrapper under Ingest/Decisions/Refinements/ (mid-band-refinement, pipeline archive).
5. **Low (<68)** — Decision Wrapper under Ingest/Decisions/Low-Confidence/.
6. **Per-change snapshot** — after archive-check ≥85%, before move. Fail → do not move; log #review-needed.
7. **subfolder-organize** — target path under 4-Archives/ (≥85%).
8. **resurface-candidate-mark** — mark high-potential notes.
9. **summary-preserve** — minimal TL;DR/summary callout, project color links (≥85%).
10. **Move** — obsidian_ensure_structure(parent of target) → obsidian_move_note dry_run then commit. Post-move: para-type Archive, **status: archived** per mcp-obsidian-integration.
11. **Logging** — obsidian_log_action; Archive-Log.md, Backup-Log.md.
12. **Ghost-folder sweep** — after moves, archive-ghost-folder-sweep (obsidian_remove_empty_folder); log #ghost-sweep.

**Loop logging:** loop_type "archive-refine". **Exclusions:** 4-Archives/, Backups/, Templates/, Log*.md, * Hub.md, watcher-protected.

**Return:** One-paragraph summary; any wrapper; Success / #review-needed / failure. Watcher-Result when requestId provided.
