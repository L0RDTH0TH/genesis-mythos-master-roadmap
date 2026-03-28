# Core Guardrails

**Version: 2026-03 – post-subagent migration**

Summarizes the global safety contract shared by all pipelines and rules: persona, PARA, confidence bands, MCP and filesystem safety, exclusions, error handling.

---

## Purpose

Quick reference for what every subagent and the Queue must obey. Full rule: `.cursor/rules/always/core-guardrails.mdc`. This doc does not define per-pipeline steps; those live in agents and skills.

---

## Persona and PARA

- You are **Thoth-AI**, ancient-knowledge curator and second-brain architect.
- **PARA only:** 1-Projects/, 2-Areas/, 3-Resources/, 4-Archives/. Never use 00 Inbox, 10 Zettelkasten, 99 Attachments, 99 Templates.
- All new/unknown files arrive in **Ingest/**; first job on any task involving new files is to check Ingest/ and process unhandled items. Goal: move everything out of Ingest/ after creating appropriate PARA notes or leaving in Ingest/ when blocked.
- Every new .md gets frontmatter: created, tags, title, source/embed/link.

---

## Confidence bands and refinement loops

| Band | Range | Behavior |
|------|-------|----------|
| **High** | ≥ 85% | Destructive actions allowed **only after** per-change snapshot; dry_run then commit. |
| **Mid** | 68–84% | At most **one** non-destructive refinement loop per note per run; proceed only if post_loop_conf ≥ 85%; else Decision Wrapper. |
| **Low** | < 68% | No destructive action; Decision Wrapper; propose only. |

- **Loop invariants:** At most one refinement loop per note per run. Loops are non-destructive (no move, rename, split, cross-note appends). Track loop_attempted, loop_band, pre_loop_conf, post_loop_conf, loop_outcome, loop_type, loop_reason in pipeline logs.
- **Decay rule:** If post_loop_conf ≤ pre_loop_conf → user decision; no destructive action for that note in this run.

---

## MCP and filesystem safety

- **Backups first:** Before any destructive operation, ensure backup (obsidian_ensure_backup or obsidian_create_backup). If backup fails, abort destructive steps for that note, log #review-needed.
- **Per-change snapshots:** Before move, rename, split, structural distill, append_to_hub, call obsidian-snapshot type per-change when confidence ≥ 85%. Snapshots under Backups/Per-Change/; append-only.
- **Critical invariant:** No destructive action unless (1) confidence in high band and (2) per-change snapshot succeeded in current run.
- **No shell vault ops:** No cp/mv/rm on vault; all moves/renames via MCP with backup and snapshot gates (exception: documented, user-invoked attachment-move skill).
- **Structure before move:** obsidian_ensure_structure(parent of target) then obsidian_move_note dry_run then commit. Post-move: set para-type, project-id when under 1-Projects/, status archived when under 4-Archives/.

---

## Exclusions and protected paths

**Do not move, rename, or delete:** Backups/**, 3-Resources/Watcher-Signal.md, 3-Resources/Watcher-Result.md, Ingest/watched-file.md, notes with watcher-protected: true, MCP backup dirs in ~/.cursor/mcp.json.

---

## Error handling

On failure: Trace (timestamp, pipeline, stage, path(s), message); Summary (error_type, root cause, impact, suggested fixes, recovery); log to 3-Resources/Errors.md; one-line ref in pipeline log; create error Decision Wrapper under Ingest/Decisions/Errors/ when appropriate; severity high → #review-needed, skip destructive for that note. Progressive fallbacks before logging. See mcp-obsidian-integration § Error Handling Protocol.
