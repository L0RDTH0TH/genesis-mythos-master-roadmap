# Ingest and Organize Skills Overview

**Version: 2026-03 – post-subagent migration**

Overview of skills used by the Ingest and Organize subagents: classify, frontmatter-enrich, name-enhance, subfolder-organize, archive-check, and related.

---

## Purpose

Single reference for which skills the Ingest and Organize pipelines call and when. Skill definitions live in `.cursor/skills/<skill-name>/SKILL.md`.

---

## Ingest (Phase 1 and apply-mode)

| Skill | When used |
|-------|-----------|
| **frontmatter-enrich** | After classify_para: set status, confidence, para-type, created, links; optional project-id, priority, deadline. |
| **name-enhance** | In ingest: **propose only** (never rename). Returns suggested_name; subfolder-organize may use it in path when confidence ≥85%. |
| **subfolder-organize** | Build target path from para-type, project-id, semantic themes (max 4 levels); in Phase 1 no move; in Phase 2 apply-mode used with hard_target_path. |
| **split-link-preserve** | After obsidian_split_atomic: write split_from on each child; split_into or Splits section on parent. |
| **distill-highlight-color** | When distill step runs in ingest (high conf). |
| **task-reroute** | When note is task-like and confidence ≥78%: find or derive parent; create task note or append to existing; snapshot target before append. |
| **link-to-pmg-if-applicable** | After append_to_hub: when note has project-id, append link to project's PMG note to note's links array if PMG exists. |
| **next-action-extract** | Extract tasks into checklists and next-actions frontmatter for Dataview. |
| **feedback-incorporate** | Step 0 and apply-mode: resolve approved_option/approved_path into hard_target_path and guidance_text. |

---

## Organize

| Skill | When used |
|-------|-----------|
| **frontmatter-enrich** | After classify_para: status, confidence, para-type, created, links; optional project-id, priority, deadline (≥85% auto-apply). |
| **subfolder-organize** | Build target path under 1/2/3 (max 4 levels). Re-org mode: target stays under PARA. Mid-band: optionally propose_para_paths (context_mode organize), calibrate, dry_run then commit. |
| **name-enhance** | Context organize: opportunistic rename when suggested_name and conf ≥85% for Regular note; snapshot then obsidian_rename_note. MOC/hub/index/project root require explicit request. |

---

## Archive

| Skill | When used |
|-------|-----------|
| **archive-check** | Verify archive readiness (no open tasks, status complete, age threshold, subfolder checks). Primary signal: archive_conf (≥85% for move). |
| **subfolder-organize** | Compute target path under 4-Archives/ (≥85%). |
| **resurface-candidate-mark** | Mark high-potential notes (≥85% for hub append; metadata-only ≥75%). |
| **summary-preserve** | Minimal TL;DR/summary callout, project color links (≥85%). |
| **archive-ghost-folder-sweep** | After moves: obsidian_remove_empty_folder on affected parents; log #ghost-sweep. |
