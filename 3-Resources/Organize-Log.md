---
title: Organize-Log
created: 2026-02-25
tags: [logs, cursor, autonomous-organize]
para-type: Resource
status: active
---

# Organize-Log

Canonical log for the **autonomous-organize** pipeline.

Each run should append lines in this format (mirroring the global pipelines reference):

`YYYY-MM-DD HH:MM | Pipeline: autonomous-organize | Note: [path] | Confidence: X% | Changes: [list; include Backup: [path], Snapshot: [path(s)], Move: [new path or 'stay'], Rename: [new name or '—']] | Flag: [none or #review-needed + reason]`

## Example entries (template — replace with real runs)

```
2026-02-25 14:00 | Pipeline: autonomous-organize | Note: 1-Projects/Test-Project/some-note.md | Confidence: 88% | Changes: backup, per-change snapshot, classify_para, frontmatter-enrich, subfolder-organize, move; Backup: [path]; Snapshot: Backups/Per-Change/...; Move: 1-Projects/Test-Project/Subtheme/2026-02-25-some-note.md | Flag: none
2026-02-25 14:05 | Pipeline: autonomous-organize | Note: 3-Resources/old-title.md | Confidence: 86% | Changes: backup, per-change snapshot, frontmatter-enrich, rename; Backup: [path]; Snapshot: Backups/Per-Change/...; Rename: 2026-02-25-old-title.md; Move: stay | Flag: none
2026-02-25 14:10 | Pipeline: autonomous-organize | Note: 1-Projects/Test-Project/uncertain.md | Confidence: 72% | Changes: backup, classify_para; proposed path only (below 85%); Move: stay | Flag: #review-needed confidence below threshold
```

Batch checkpoint example:

```
2026-02-25 14:15 | Batch: Backups/Batch/2026-02-25T141500Z-batch-organize-001.md | notes: 3 | pipeline: autonomous-organize | flag: none
```

## QuickAdd (optional)

To trigger the pipeline from Obsidian: add a QuickAdd **Macro** choice (e.g. **Organize sweep**) that appends a line to this log, e.g. `ORGANIZE MODE – safe batch autopilot on [folder]` + timestamp (or open Cursor with that prompt). Mirror the pattern used for Distill/Express in `scripts/quickadd/README.md` (UserScript appends to `3-Resources/Organize-Log.md`).
2026-03-02 06:04:26Z | 01-Genesis-KJV | Archive | Classify 70%; subfolder proposed 4-Archives; no move (scope 3-Resources). Backup 20260302-060412. | 70% | 4-Archives/01-Genesis-KJV.md (proposed; do not use 10 Zettelkasten) | #review-needed
2026-03-02 06:04:28Z | atomic-notes-zettelkasten-principle | Resource | Classify 70%; path unchanged. Backup 20260302-060412. | 70% | 3-Resources/ (stay) | #review-needed
2026-03-02 06:04:28Z | obsidian-append-to-hub | Resource | Classify 70%; path unchanged. Backup 20260302-060412. | 70% | 3-Resources/ (stay) | #review-needed
2026-03-02 06:04:29Z | ai-on-mobile-idea | Resource | Classify 70%; path unchanged. Backup 20260302-060412. | 70% | 3-Resources/ (stay) | #review-needed
2026-03-02 06:04:30Z | building-a-second-brain-code-para-summary | Resource | Classify 70%; path unchanged. Backup 20260302-060412. | 70% | 3-Resources/ (stay) | #review-needed
2026-03-02 06:04:42Z | connection-ingest-plugin-spec | Resource | Classify 70%; no move. Backup 20260302-060412. | 70% |  | #review-needed
2026-03-02 06:04:42Z | cursor-ingest-pipeline-trigger-prompt | Resource | Classify 70%; no move. Backup 20260302-060412. | 70% |  | #review-needed
2026-03-02 06:04:42Z | cursor-ingest-prompt-reference | Resource | Classify 70%; no move. Backup 20260302-060412. | 70% |  | #review-needed
2026-03-02 06:04:42Z | ingest-prompt-improvement-recommendations | Resource | Classify 70%; no move. Backup 20260302-060412. | 70% |  | #review-needed

---

## ORGANIZE MODE run 2026-03-02 — 3-Resources

- **Scope**: All `3-Resources/**/*.md` (excluded: *Log*.md, * Hub.md, Watcher-Result.md, Watcher-Signal.md).
- **Processed**: 25 notes in 2 batches. Backup: 20260302-060412 (10), 20260302-060448/060449 (15).
- **Outcome**: All classified at 70% (1 Archive, 1 Project, 23 Resource); **no moves** (confidence &lt;85%).
- **Remaining**: ~77 notes in 3-Resources (including Second-Brain/ and subfolders). Re-run **Organize 3-Resources** or **continue organizing 3-Resources** to process next batch.
2026-03-02 06:05:11Z | Batch 2: networkchuck-mcp, obsidian-mcp-integration, templater-ingest-chooser, ai-outputs-markdown, config-reference, enhanced-snapshots, highlighter-pipeline, test-prep-* (5), 2026-03-01_Screenshot, 2026-03-01_later-Summary, Archive-Prep-Checklist | Resource | Classify 70% (14 Resource, 1 Project); no moves. Backup 20260302-060448/060449. | 70% |  | #review-needed
