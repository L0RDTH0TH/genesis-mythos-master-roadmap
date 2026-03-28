# Express Pipeline

**Version: 2026-03 – post-subagent migration**

Documents the autonomous-express pipeline: related content, outline, CTA, version snapshots; express-apply-from-wrapper when an approved wrapper applies.

---

## Purpose

Single reference for express steps, confidence bands, and return format. Implementation in `.cursor/agents/express.md` and legacy-agents/express.mdc.

---

## Pipeline steps

1. **Backup** — obsidian_create_backup for the note.
2. **version-snapshot** — under Versions/<slug>--<timestamp>.md before major append; obsidian_ensure_structure(Versions/); create with mode create when target does not exist.
3. **related-content-pull** — similar notes via semantic + project-id; append Related section (≥85%). express-view-layer when express_view set.
4. **research-scope** — when note is PMG (is_master_goal / Master*Goal*): aggregate Resources; propose-first; commit Scoped Resources on second pass when approved.
5. **express-mini-outline** — mini-outline/summary, project colors (≥85%).
6. **Optional** — obsidian_append_to_moc / obsidian_generate_moc for hub-like notes.
7. **call-to-action-append** — CTA callout at end.
8. **Logging** — obsidian_log_action; Express-Log.md, Backup-Log.md.

---

## Confidence

- **High (≥85):** Version + per-change snapshots, full outline + CTA.
- **Mid (68–84):** Preview outline; if post_loop_conf ≥90 commit full; else Decision Wrapper under Ingest/Decisions/Refinements/ (pipeline express).
- **Low (<68):** Decision Wrapper under Ingest/Decisions/Low-Confidence/.
- **Loop logging:** loop_type "express-soft".

**Exclusions:** 4-Archives/, Backups/, Templates/, **/Log*.md, **/* Hub.md, **/Versions/.

**Return:** One-paragraph summary; any wrapper; Success / #review-needed / failure. Watcher-Result when requestId provided.
