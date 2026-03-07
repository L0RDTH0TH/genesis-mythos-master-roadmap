---
title: Backup and Snapshot Log
created: 2026-02-25
para-type: Resource
status: active
tags: [backups, snapshots, safety, cursor, obsidian]
---

# Backup and Snapshot Log

Central log for **backups**, **snapshots**, and **restores** across all pipelines (ingest, distill, archive, express).

- External backups live in `BACKUP_DIR` (managed by `obsidian_create_backup`).
- In-vault snapshots live under `Backups/Per-Change/`, `Backups/Batch/`, and optionally `Backups/Archives/`.
- This note summarizes events and points to the underlying snapshot files, which carry rich frontmatter for Dataview queries.

## How entries are written

- Snapshot and restore skills/rules should append concise lines such as:

```text
2026-02-25 01:23 | type: per-change | note: 1-Projects/Project-X/note.md | snapshot: Backups/Per-Change/note--ab12cd34--20260225-012300.md.bak | pipeline: ingest | confidence: 92% | flag: none
2026-02-25 01:25 | type: batch | batch: Backups/Batch/2026-02-25T012500Z-batch-0003.md | notes: 5 | pipeline: ingest | flag: none
2026-02-25 01:30 | type: restore | note: 1-Projects/Project-X/note.md | from: Backups/Per-Change/note--ab12cd34--20260225-012300.md.bak | result: success | flag: none
```

- Failures and anomalies should include `flag: #review-needed + reason`.

## Recent failures (Dataview suggestion)

Use Dataview (or similar) against snapshot files’ frontmatter for precise filtering; this section is a lightweight text index. Suggested pattern:

- When a failure occurs (snapshot write fails, hash mismatch on restore, retention sweep issues), include:
  - `flag: #review-needed`
  - A short reason (e.g. `SNAPSHOT_DIR unreachable`, `snapshot_hash mismatch`).

You can then surface these in `Restore Hub.md` via a Dataview block that scans snapshot files and/or this log for `#review-needed`.

## How to restore

Short version:

1. Identify a candidate snapshot:
   - From this log, or
   - Via `Restore Hub.md` Dataview listings of recent snapshots for a note.
2. Use a RESTORE MODE prompt in Cursor, e.g.:
   - `RESTORE MODE – rollback last change to [[Note Title]]`
3. Follow the auto-restore rule:
   - It will present recent snapshots, verify the `snapshot_hash`, and only then overwrite the original note.

See `Restore Hub.md` and `.cursor/rules/context/auto-restore.mdc` for the detailed flow.



2026-03-03 06:27 | type: per-change | note: Ingest/DM Free Camera.md | snapshot: Backups/Per-Change/DM-Free-Camera--f479a5f7--20260303-062754.md.bak | pipeline: ingest | confidence: 90% | flag: none

2026-02-25 11:57 | type: backup | note: 1-Projects/Test-Project/2026-02-25-express-narrative.md | backup: /home/darth/Documents/Second-Brain-oops-Backups/20260225-115752-2026-02-25-express-narrative.md | pipeline: autonomous-express | version-snapshot skipped (destination path new; backup requires existing file) | flag: none

2026-02-25 20:40 | type: backup | note: 1-Projects/Test-Project/2026-02-25-express-narrative.md | backup: /home/darth/Documents/Second-Brain-oops-Backups/20260225-204004-2026-02-25-express-narrative.md | pipeline: autonomous-express | flag: none
2026-02-25 20:41 | type: per-change | note: 1-Projects/Test-Project/2026-02-25-express-narrative.md | snapshot: Backups/Per-Change/2026-02-25-express-narrative--376aa0cd--20260225-204100.md.bak | pipeline: express | confidence: 85% | flag: none

2026-02-25 20:49 | type: per-change | note: 1-Projects/Test-Project/2026-02-25-distill-messy.md | snapshot: Backups/Per-Change/2026-02-25-distill-messy--0da3acfa--20260225-204930.md.bak | pipeline: autonomous-distill | confidence: 88% | flag: none

2026-02-25 21:22 | type: backup | note: 1-Projects/Test-Project/2026-02-25-distill-messy.md, 2026-02-25-distill-short.md | backup: 20260225-212242 (batch) | pipeline: autonomous-distill | flag: none
2026-02-25 21:22 | type: per-change | note: 1-Projects/Test-Project/2026-02-25-distill-messy.md | snapshot: Backups/Per-Change/2026-02-25-distill-messy--0da3acfa--20260225-212245.md.bak | pipeline: autonomous-distill | confidence: 88% | flag: none
2026-02-25 21:22 | type: per-change | note: 1-Projects/Test-Project/2026-02-25-distill-short.md | snapshot: Backups/Per-Change/2026-02-25-distill-short--334b0054--20260225-212246.md.bak | pipeline: autonomous-distill | confidence: 90% | flag: none
2026-02-25 21:22 | type: batch | batch: Backups/Batch/2026-02-25T212250Z-batch-distill-002.md | notes: 2 | pipeline: autonomous-distill | flag: none

2026-02-25 21:28 | type: backup | note: 1-Projects/Test-Project/2026-02-25-archive-candidate.md, 2026-02-25-archive-candidate-2.md | backup: /home/darth/Documents/Second-Brain-oops-Backups/20260225-212851-* | pipeline: autonomous-archive | flag: none
2026-02-25 21:29 | type: per-change | note: 1-Projects/Test-Project/2026-02-25-archive-candidate.md | snapshot: Backups/Per-Change/2026-02-25-archive-candidate--cf88fb0b--20260225-212918.md.bak | pipeline: autonomous-archive | confidence: 88% | flag: none
2026-02-25 21:29 | type: per-change | note: 1-Projects/Test-Project/2026-02-25-archive-candidate-2.md | snapshot: Backups/Per-Change/2026-02-25-archive-candidate-2--d6826c4a--20260225-212935.md.bak | pipeline: autonomous-archive | confidence: 87% | flag: none
2026-02-25 21:30 | type: batch | batch: Backups/Batch/2026-02-25T213000Z-batch-archive-001.md | notes: 2 | pipeline: autonomous-archive | flag: none

2026-02-26 00:39 | type: backup | note: Ingest/01 - Genesis - KJV.md | backup: /home/darth/Documents/Second-Brain-oops-Backups/20260226-003942-01 - Genesis - KJV.md | pipeline: heuristic-audit-ingest | flag: none
2026-02-26 00:43 | type: backup | note: 3-Resources/01-Genesis-KJV.md | backup: /home/darth/Documents/Second-Brain-oops-Backups/20260226-004317-01-Genesis-KJV.md | pipeline: autonomous-distill (distill-highlight-color) | flag: none

2026-03-01 23:29 | type: backup | note: 3-Resources/Second-Brain/Deprecated-Vestigial-Audit.md | backup: /home/darth/Documents/Second-Brain-oops-Backups/20260301-232854-Deprecated-Vestigial-Audit.md | pipeline: organize (move out of backbone) | flag: none
2026-03-01 23:29 | type: per-change | note: 3-Resources/Second-Brain/Deprecated-Vestigial-Audit.md | snapshot: Backups/Per-Change/Deprecated-Vestigial-Audit--3da6bcc3--20260301-232910.md.bak | pipeline: organize | confidence: 95% | move to 3-Resources/Deprecated-Vestigial-Audit.md | flag: none

2026-03-02 05:19 | type: backup | note: Ingest/Genesis Roadmap.md, Ingest/Master goal for Genesis.md | backup: 20260302-051937 | pipeline: ingest (70% min confidence this run) | flag: none
2026-03-02 05:19 | type: per-change | note: Ingest/Genesis Roadmap.md | snapshot: Backups/Per-Change/genesis-roadmap--45c0880b--20260302-051937.md.bak | pipeline: ingest | confidence: 70% | moved to 1-Projects/Genesis/genesis-roadmap-2026-03-02-0520.md | flag: none
2026-03-02 05:19 | type: per-change | note: Ingest/Master goal for Genesis.md | snapshot: Backups/Per-Change/master-goal-for-genesis--095f4f39--20260302-051937.md.bak | pipeline: ingest | confidence: 70% | moved to 1-Projects/Genesis/master-goal-for-genesis-2026-03-02-0520.md | flag: none

2026-03-02 05:56 | type: backup | notes: Ingest/genesis-ingest-classification-context, Genesis task, Genesis week One | backup: 20260302-054536 | pipeline: ingest (re-run with Genesis context) | flag: none
2026-03-02 05:56 | type: per-change | note: Ingest/Genesis week One.md | snapshot: Backups/Per-Change/genesis-week-one--a1b2c3d4--20260302-0556.md.bak | pipeline: ingest | confidence: 88% | moved to 1-Projects/Genesis/Genesis week One.md | flag: none
2026-03-02 05:56 | type: per-change | note: Ingest/why-genesis-roadmap-should-be-project-2026-03-02-0522.md | snapshot: Backups/Per-Change/why-genesis-roadmap--e5f6g7h8--20260302-0556.md.bak | pipeline: ingest | confidence: 88% | moved to 1-Projects/Genesis/why-genesis-roadmap-should-be-project-2026-03-02-0522.md | flag: none

2026-03-02 06:02 | type: per-change | note: Ingest/Genesis task.md | snapshot: Backups/Per-Change/genesis-task--c8d9e0f1--20260302-0602.md.bak | pipeline: ingest | confidence: 100% (explicit: name = Genesis project) | moved to 1-Projects/Genesis/Genesis task.md | flag: none

2026-03-02 06:04 | type: backup | notes: 3-Resources (batch 1: 10 notes, batch 2: 15 notes) | backup: 20260302-060412, 20260302-060448/060449 | pipeline: autonomous-organize (3-Resources) | flag: none

2026-03-02 07:03 | type: backup | notes: Genesis project (5 notes: roadmap, master-goal, week one, task, why-genesis-roadmap) | backup: 20260302-070310, 20260302-070311 | pipeline: genesis-fix (distill+enrich, move meta, rename) | flag: none
2026-03-02 07:03 | type: move | note: why-genesis-roadmap-should-be-project-2026-03-02-0522.md | from: 1-Projects/Genesis/ | to: 3-Resources/ | pipeline: genesis-fix | flag: none
2026-03-02 07:03 | type: rename | note: Genesis task.md → genesis-task-2026-03-02-0715.md, Genesis week One.md → genesis-week-one-2026-03-02-0715.md | path: 1-Projects/Genesis/ | pipeline: genesis-fix | flag: none

2026-03-03 22:12 | type: per-change | note: Ingest/dnd basic rules.md | snapshot: Backups/Per-Change/dnd-basic-rules--2111e760--20260303-221154.md.bak | pipeline: ingest | confidence: 92% | move to 3-Resources/TTRPGs/Rulebooks/dnd basic rules.md | flag: none

2026-03-03 23:06 | type: per-change | note: Ingest/Cascade Branches.md | snapshot: Backups/Per-Change/Cascade-Branches--7f5b3aab--20260303-230612.md.bak | pipeline: ingest | confidence: 70% | move to 4-Archives/Genesis/Cascade Branches.md | flag: none
2026-03-03 23:06 | type: per-change | note: Ingest/Decisions/cascade-branches-2026-03-03-2305.md | snapshot: Backups/Per-Change/cascade-branches-2026-03-03-2305--faff0a50--20260303-230618.md.bak | pipeline: ingest | confidence: 100% | move to 4-Archives/Ingest-Decisions/cascade-branches-2026-03-03-2305.md | flag: none

2026-03-07 00:23 | type: backup | note: 144 candidates (1-Projects, 2-Areas, 3-Resources) | backup: /home/darth/Documents/Second-Brain-oops-Backups/20260307-002246 through 20260307-002308 | pipeline: autonomous-archive (#full-sweep) | flag: none
2026-03-07 00:23 | type: batch | batch: Backups/Batch/2026-03-07T002310Z-batch-archive-full-sweep.md | notes: 144 | pipeline: autonomous-archive (#full-sweep) | flag: none
2026-03-07 00:24–00:30 | type: per-change | notes: Example-Project, Example-Area, Test-Project (5) | snapshot: Backups/Per-Change/*--20260307-*.md.bak | pipeline: autonomous-archive | confidence: 90% | flag: none

2026-03-07 00:35 | type: batch | batch: Backups/Batch/2026-03-07T003500Z-batch-archive-full-sweep-continue.md | notes: 137 | pipeline: autonomous-archive (#full-sweep continue) | flag: none
2026-03-07 00:40–00:42 | type: per-change | notes: Example (2), Genesis-Mythos (10), OG-minecraft (1), Pong-Game (7), Retro Snake Game (2), Resources (10) | snapshot: Backups/Per-Change/*--20260307-004*.md.bak | pipeline: autonomous-archive | confidence: 90% | flag: none

2026-03-07 00:45 | type: batch | batch: Backups/Batch/2026-03-07T004500Z-batch-archive-full-sweep-continue2.md | notes: 105 | pipeline: autonomous-archive (#full-sweep continue 2) | flag: none
2026-03-07 00:46–00:48 | type: per-change | notes: Retro Snake Game (6), Resources batch2 (20), Resources batch3 (25 stubs) | snapshot: Backups/Per-Change/phase-*-rs*.md.bak, Res-batch2-*.md.bak, Res-batch3-*.md.bak | pipeline: autonomous-archive | confidence: 90% | flag: none

2026-03-07 00:55 | type: batch | batch: Backups/Batch/2026-03-07T005500Z-batch-archive-full-sweep-continue3.md | notes: 43 | pipeline: autonomous-archive (#full-sweep continue 3) | flag: none
2026-03-07 00:56 | type: per-change | notes: 43 Resources (MCP-*, OG-minecraft, Plugins-Usage, Testing, Watcher, Zettelkasten-PKM, etc.) | snapshot: Backups/Per-Change/Res-cont3-*-20260307-005600.md.bak | pipeline: autonomous-archive | confidence: 90% | flag: none

2026-03-07 03:32 | type: batch | batch: Backups/Batch/2026-03-07T033200Z-batch-archive-full-sweep.md | notes: 0 (full sweep re-run; all candidates protected or folders empty) | pipeline: autonomous-archive (#full-sweep) | flag: none