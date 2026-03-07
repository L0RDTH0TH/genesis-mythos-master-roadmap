---
title: Archive-Log
created: 2026-02-25
tags: [logs, cursor, autonomous-archive]
para-type: Resource
status: active
---

# Archive-Log

Canonical log for the **autonomous-archive** pipeline.

Each run should append lines in this format (mirroring the global pipelines reference):

`YYYY-MM-DD HH:MM | Pipeline: autonomous-archive | Note: [path] | Confidence: X% | Changes: [list; include Backup: [path], Snapshot: [path(s)], Move: [new path]] | Flag: [none or #review-needed + reason]`

## Example entries (template — replace with real runs)

```
2026-02-25 12:10 | Pipeline: autonomous-archive | Note: 1-Projects/Test-Project/2026-02-25-archive-candidate.md | Confidence: 88% | Changes: backup, per-change snapshot, archive-check, subfolder-organize, summary-preserve, move; Backup: [path]; Snapshot: Backups/Per-Change/...; Move: 4-Archives/Test-Project-Archive/... | Flag: none
```

## 2026-02-25 sweep (1-Projects/Test-Project/; test candidates only)

2026-02-25 21:29 | Pipeline: autonomous-archive | Note: 1-Projects/Test-Project/2026-02-25-archive-candidate.md | Confidence: 88% | Changes: backup, per-change snapshot, archive-check, subfolder-organize, resurface-candidate-mark, summary-preserve, move; Backup: /home/darth/Documents/Second-Brain-oops-Backups/20260225-212851-2026-02-25-archive-candidate.md; Snapshot: Backups/Per-Change/2026-02-25-archive-candidate--cf88fb0b--20260225-212918.md.bak; Move: 4-Archives/Test-Project-Archive/2026-02-25-archive-candidate.md | Flag: none

2026-02-25 21:30 | Pipeline: autonomous-archive | Note: 1-Projects/Test-Project/2026-02-25-archive-candidate-2.md | Confidence: 87% | Changes: backup, per-change snapshot, archive-check, subfolder-organize, resurface-candidate-mark, summary-preserve, move; Backup: /home/darth/Documents/Second-Brain-oops-Backups/20260225-212851-2026-02-25-archive-candidate-2.md; Snapshot: Backups/Per-Change/2026-02-25-archive-candidate-2--d6826c4a--20260225-212935.md.bak; Move: 4-Archives/Test-Project-Archive/2026-02-25-archive-candidate-2.md | Flag: none

Batch checkpoint: Backups/Batch/2026-02-25T213000Z-batch-archive-001.md | notes: 2 | Flag: none

---

## 2026-03-01 — Archive Ingest notes (bulk)

**Pipeline:** User request "Archive the ingest notes" — bulk move from Ingest/ to 4-Archives/Ingest-2026-03-01/. **Excluded:** watched-file.md (watcher-protected). **Non-.md** (Screenshot jpg, later.txt, Untitled, Untitled Document 1, Untitled Document 2) remain in Ingest; move manually to 5-Attachments/ if desired.

**Backup:** Existing backup confirmed (20260301-212029 / 20260301-212031 under `/home/darth/Documents/Second-Brain-oops-Backups/`). Dry-run then commit for each note.

**Moved (29 notes):** 2026-02-24-obsidian-plugin-automation-report, 2026-02-24-plugin-modification-report, 2026-02-26-Automation-Flows-MCP-Improvements, 2026-02-26-Second-Brain-Automations-Setup-Report, 2026-02-26-Untitled-Companion, 2026-02-26-Untitled-Document-1-Companion, 2026-02-26-Untitled-Document-2-Companion, CONFIG-REFERENCE, Canvas Highlighter and Scripts, Master Goal, Multiple Choice Popup, Obsidian Second Brain Audit, Pipeline Potentials, Second Brain Project, Test of attachment, Untitled 1–6, Untitled, Untitled.sync-conflict-…, V4 Draft Thoughts, V4 Draft, Vault Name, Vault as Example, Virginal testing, We are running a test, structure — all to `4-Archives/Ingest-2026-03-01/`.

---

## 2026-03-02 — Archive sweep (no candidates)

**Pipeline:** User request "Ingest and Archive". Autonomous-archive sweep over 1-Projects, 2-Areas, 3-Resources.

**Result:** No archive candidates found. No notes in active PARA folders have `status: complete` or equivalent; only notes already in 4-Archives/ have that frontmatter. No moves. Flag: none.

---

## 2026-03-02 — Archive Ingest (after sync-conflict removal)

**Pipeline:** User request "Remove sync conflicts from Ingest, then Archive the Ingest folder". Sync-conflict files removed (backup then delete); remaining Ingest .md notes moved to 4-Archives/Ingest-2026-03-01/. **Excluded:** watched-file.md (watcher-protected).

**Backup:** 20260302-043726 under `/home/darth/Documents/Second-Brain-oops-Backups/`. Dry-run then commit for each note.

**Moved (4 notes):** obsidian-screenshot-2026-02-25-2026-03-01-0205, user-interaction-logging-watcher-2026-03-01-0205, obsidian-second-brain-auditor-2026-03-01-0205, expert-consultant-second-brain-kms-2026-03-01-0205 → `4-Archives/Ingest-2026-03-01/`. Flag: none.

---

## 2026-03-07 — ARCHIVE MODE full sweep #full-sweep

**Pipeline:** autonomous-archive. **Trigger:** ARCHIVE MODE – full sweep of 1-Projects, 2-Areas, 3-Resources; move non-protected notes to 4-Archives; age_days/no_activity_days ignored.

**Backup:** All 144 candidates backed up to `/home/darth/Documents/Second-Brain-oops-Backups/` (20260307-002246 through 20260307-002308). **Batch snapshot:** Backups/Batch/2026-03-07T002310Z-batch-archive-full-sweep.md.

**Excluded (per Vault-Layout):** Backups/, *Log*.md, * Hub.md, Watcher-Signal.md, Watcher-Result.md, 3-Resources/Second-Brain/**, Second-Brain-Config.md, Errors.md.

**Archive path convention:** 1-Projects/{project}/… → 4-Archives/Projects/{project}-Archive/…; 2-Areas/… → 4-Archives/Areas/…; 3-Resources/… → 4-Archives/Resources/….

**Moved in this run (7):** Example-Project.md → 4-Archives/Projects/Example-Project-Archive/; Example-Area.md → 4-Archives/Areas/; Test-Project (5 notes) → 4-Archives/Projects/Test-Project-Archive/. Each with per-change snapshot, dry_run, then commit.

**Pending (137):** Backup exists for all. To apply: for each note run ensure_structure(target_parent), per-change snapshot, dry_run, then move commit. Proposed paths below.

| Original path | Proposed archive path | Status |
|--------------|------------------------|--------|
| 1-Projects/Example-Project.md | 4-Archives/Projects/Example-Project-Archive/Example-Project.md | moved |
| 1-Projects/Example/Roadmap/Example-Phase-1-Sub-Roadmap.md | 4-Archives/Projects/Example-Archive/Roadmap/Example-Phase-1-Sub-Roadmap.md | pending |
| 1-Projects/Example/Roadmap/Example-Roadmap.md | 4-Archives/Projects/Example-Archive/Roadmap/Example-Roadmap.md | pending |
| 1-Projects/Genesis-Mythos/Genesis-Mythos Master Goal.md | 4-Archives/Projects/Genesis-Mythos-Archive/Genesis-Mythos Master Goal.md | pending |
| 1-Projects/Genesis-Mythos/Genesis-Mythos-Roadmap-MOC.md | 4-Archives/Projects/Genesis-Mythos-Archive/Genesis-Mythos-Roadmap-MOC.md | pending |
| 1-Projects/Genesis-Mythos/Roadmap/Genesis-Mythos-Roadmap-2026-03-02-1200.md | 4-Archives/Projects/Genesis-Mythos-Archive/Roadmap/Genesis-Mythos-Roadmap-2026-03-02-1200.md | pending |
| 1-Projects/Genesis-Mythos/Roadmap/Phase-1-Maps/Phase-1-Maps-Roadmap-2026-03-02-1200.md | 4-Archives/Projects/Genesis-Mythos-Archive/Roadmap/Phase-1-Maps/Phase-1-Maps-Roadmap-2026-03-02-1200.md | pending |
| 1-Projects/Genesis-Mythos/Roadmap/Phase-2-Terrain3D/Phase-2-Terrain3D-Roadmap-2026-03-02-1200.md | 4-Archives/Projects/Genesis-Mythos-Archive/Roadmap/Phase-2-Terrain3D/Phase-2-Terrain3D-Roadmap-2026-03-02-1200.md | pending |
| 1-Projects/Genesis-Mythos/Roadmap/Phase-3-Lore/Phase-3-Lore-Roadmap-2026-03-02-1200.md | 4-Archives/Projects/Genesis-Mythos-Archive/Roadmap/Phase-3-Lore/Phase-3-Lore-Roadmap-2026-03-02-1200.md | pending |
| 1-Projects/Genesis-Mythos/Roadmap/Phase-4-Combat/Phase-4-Combat-Roadmap-2026-03-02-1200.md | 4-Archives/Projects/Genesis-Mythos-Archive/Roadmap/Phase-4-Combat/Phase-4-Combat-Roadmap-2026-03-02-1200.md | pending |
| 1-Projects/Genesis-Mythos/Roadmap/Phase-5-Politics/Phase-5-Politics-Roadmap-2026-03-02-1200.md | 4-Archives/Projects/Genesis-Mythos-Archive/Roadmap/Phase-5-Politics/Phase-5-Politics-Roadmap-2026-03-02-1200.md | pending |
| 1-Projects/Genesis-Mythos/Roadmap/Phase-6-Wizard/Phase-6-Wizard-Roadmap-2026-03-02-1200.md | 4-Archives/Projects/Genesis-Mythos-Archive/Roadmap/Phase-6-Wizard/Phase-6-Wizard-Roadmap-2026-03-02-1200.md | pending |
| 1-Projects/OG-minecraft/minecraft-beta-clone-master-goal-2026-03-06-0640.md | 4-Archives/Projects/OG-minecraft-Archive/minecraft-beta-clone-master-goal-2026-03-06-0640.md | pending |
| 1-Projects/Pong-Game/Pong-Game-Roadmap-MOC.md | 4-Archives/Projects/Pong-Game-Archive/Pong-Game-Roadmap-MOC.md | pending |
| 1-Projects/Pong-Game/Roadmap/Phase-1-Paddle-Controls/Phase-1-Paddle-Controls-Roadmap-2026-03-05-0614.md | 4-Archives/Projects/Pong-Game-Archive/Roadmap/Phase-1-Paddle-Controls/Phase-1-Paddle-Controls-Roadmap-2026-03-05-0614.md | pending |
| 1-Projects/Pong-Game/Roadmap/Phase-2-Ball-Physics/Phase-2-Ball-Physics-Roadmap-2026-03-05-0614.md | 4-Archives/Projects/Pong-Game-Archive/Roadmap/Phase-2-Ball-Physics/Phase-2-Ball-Physics-Roadmap-2026-03-05-0614.md | pending |
| 1-Projects/Pong-Game/Roadmap/Phase-3-Collision-Scoring/Phase-3-Collision-Scoring-Roadmap-2026-03-05-0614.md | 4-Archives/Projects/Pong-Game-Archive/Roadmap/Phase-3-Collision-Scoring/Phase-3-Collision-Scoring-Roadmap-2026-03-05-0614.md | pending |
| 1-Projects/Pong-Game/Roadmap/Phase-4-UI-Game-Loop/Phase-4-UI-Game-Loop-Roadmap-2026-03-05-0614.md | 4-Archives/Projects/Pong-Game-Archive/Roadmap/Phase-4-UI-Game-Loop/Phase-4-UI-Game-Loop-Roadmap-2026-03-05-0614.md | pending |
| 1-Projects/Pong-Game/Roadmap/Pong-Game-Roadmap-2026-03-05-0614.md | 4-Archives/Projects/Pong-Game-Archive/Roadmap/Pong-Game-Roadmap-2026-03-05-0614.md | pending |
| 1-Projects/Pong-Game/Roadmap/Source-Pong-Game-Roadmap-Outline--2026-03-05-0614.md | 4-Archives/Projects/Pong-Game-Archive/Roadmap/Source-Pong-Game-Roadmap-Outline--2026-03-05-0614.md | pending |
| 1-Projects/Retro Snake Game/retro-snake-game-roadmap-moc.md | 4-Archives/Projects/Retro Snake Game-Archive/retro-snake-game-roadmap-moc.md | pending |
| 1-Projects/Retro Snake Game/Roadmap/Phase-1-Game-Grid/phase-1-game-grid-roadmap-2026-03-05-0202.md | 4-Archives/Projects/Retro Snake Game-Archive/Roadmap/Phase-1-Game-Grid/phase-1-game-grid-roadmap-2026-03-05-0202.md | pending |
| 1-Projects/Retro Snake Game/Roadmap/Phase-2-Snake/phase-2-snake-roadmap-2026-03-05-0202.md | 4-Archives/Projects/Retro Snake Game-Archive/Roadmap/Phase-2-Snake/phase-2-snake-roadmap-2026-03-05-0202.md | pending |
| 1-Projects/Retro Snake Game/Roadmap/Phase-3-Food-Apple/phase-3-food-apple-roadmap-2026-03-05-0202.md | 4-Archives/Projects/Retro Snake Game-Archive/Roadmap/Phase-3-Food-Apple/phase-3-food-apple-roadmap-2026-03-05-0202.md | pending |
| 1-Projects/Retro Snake Game/Roadmap/Phase-4-Collision-Detection/phase-4-collision-detection-roadmap-2026-03-05-0202.md | 4-Archives/Projects/Retro Snake Game-Archive/Roadmap/Phase-4-Collision-Detection/phase-4-collision-detection-roadmap-2026-03-05-0202.md | pending |
| 1-Projects/Retro Snake Game/Roadmap/Phase-5-Scoring-UI/phase-5-scoring-ui-roadmap-2026-03-05-0202.md | 4-Archives/Projects/Retro Snake Game-Archive/Roadmap/Phase-5-Scoring-UI/phase-5-scoring-ui-roadmap-2026-03-05-0202.md | pending |
| 1-Projects/Retro Snake Game/Roadmap/Phase-6-Controls-Game-Loop/phase-6-controls-game-loop-roadmap-2026-03-05-0202.md | 4-Archives/Projects/Retro Snake Game-Archive/Roadmap/Phase-6-Controls-Game-Loop/phase-6-controls-game-loop-roadmap-2026-03-05-0202.md | pending |
| 1-Projects/Retro Snake Game/Roadmap/retro-snake-game-roadmap-2026-03-05-0202.md | 4-Archives/Projects/Retro Snake Game-Archive/Roadmap/retro-snake-game-roadmap-2026-03-05-0202.md | pending |
| 1-Projects/Retro Snake Game/Roadmap/Source-snake-roadmap-2026-03-05-0202.md | 4-Archives/Projects/Retro Snake Game-Archive/Roadmap/Source-snake-roadmap-2026-03-05-0202.md | pending |
| 1-Projects/Test-Project/2026-02-25-distill-messy.md | 4-Archives/Projects/Test-Project-Archive/2026-02-25-distill-messy.md | moved |
| 1-Projects/Test-Project/2026-02-25-distill-short.md | 4-Archives/Projects/Test-Project-Archive/2026-02-25-distill-short.md | moved |
| 1-Projects/Test-Project/2026-02-25-express-narrative.md | 4-Archives/Projects/Test-Project-Archive/2026-02-25-express-narrative.md | moved |
| 1-Projects/Test-Project/2026-02-25-split-test-multi-idea.md | 4-Archives/Projects/Test-Project-Archive/2026-02-25-split-test-multi-idea.md | moved |
| 1-Projects/Test-Project/Versions/2026-02-25-express-narrative--20260225-204100.md | 4-Archives/Projects/Test-Project-Archive/Versions/2026-02-25-express-narrative--20260225-204100.md | moved |
| 2-Areas/Example-Area.md | 4-Archives/Areas/Example-Area.md | moved |
| 3-Resources/01-Genesis-KJV.md | 4-Archives/Resources/01-Genesis-KJV.md | pending |
| … (104 more 3-Resources entries; see Backups/Batch/2026-03-07T002310Z-batch-archive-full-sweep.md or re-run script) | | |

Flag: none. **Next step:** Re-run ARCHIVE MODE full sweep (or apply remaining moves per table) with ensure_structure → per-change snapshot → dry_run → commit for each pending note.
2026-03-07 00:25:15Z | ARCHIVE MODE full sweep | Archive | Backup 144 notes; batch snapshot Backups/Batch/2026-03-07T002310Z-batch-archive-full-sweep.md; 7 moved (Example-Project, Example-Area, Test-Project x5); 137 pending with proposed paths | 90% | 4-Archives/Projects|Areas|Resources/* | #full-sweep

---

## 2026-03-07 — ARCHIVE MODE full sweep (continue) #full-sweep

**Pipeline:** autonomous-archive. **Trigger:** Same full-sweep; continue moving remaining 137 notes.

**Batch snapshot:** Backups/Batch/2026-03-07T003500Z-batch-archive-full-sweep-continue.md. **Backup:** Existing from initial sweep (20260307-002246–002308).

**Moved this run (32):** Example/Roadmap (2), Genesis-Mythos (10), OG-minecraft (1), Pong-Game (7), Retro Snake Game (2), 3-Resources (10: 01-Genesis-KJV, 2026-02-25-*, 2026-03-01_*, 2d-map-maker-*, Archive-Prep-Checklist, Attachment-Subtype-Mapping). Each with per-change snapshot, dry_run, then commit.

**Remaining (105):** 6 × Retro Snake Game roadmap notes; 99 × 3-Resources. Re-run ARCHIVE MODE full sweep to apply (ensure_structure → per-change snapshot → dry_run → commit). Proposed paths: 1-Projects → 4-Archives/Projects/{project}-Archive/…; 3-Resources → 4-Archives/Resources/….

Flag: none.
2026-03-07 00:36:48Z | ARCHIVE full sweep continue | Archive | Batch snapshot 2026-03-07T003500Z; 32 moved (Example, Genesis-Mythos, OG-minecraft, Pong-Game, Retro Snake Game partial, 10 Resources); 105 pending | 90% | 4-Archives/Resources/* (99), Retro Snake Game (6) | #full-sweep

---

## 2026-03-07 — ARCHIVE MODE full sweep (continue 2) #full-sweep

**Pipeline:** autonomous-archive. **Trigger:** Same full-sweep; continue moving remaining 105 notes.

**Batch snapshot:** Backups/Batch/2026-03-07T004500Z-batch-archive-full-sweep-continue2.md. **Backup:** Existing from initial sweep.

**Moved this run (49):** 6 × Retro Snake Game roadmap (Phase-3–6, retro-snake-game-roadmap, Source-snake-roadmap); 20 × 3-Resources (Autonomous-Runs-Options-Reference, Beta-Launch-Audit-Report, cascade-image-attachment, Clean-technical-folder*, Cursor-Ingest/*, Cursor-Skill-Pipelines-Reference, Deprecated-Vestigial-Audit, EAT-CACHE-Testing*, enhanced-snapshots, fantasy-archetypes-*, Genesis-Docs-Timeline); 23 × 3-Resources (Genesis-Mythos/*, Genesis-Mythos-System-Roadmap, Highlightr/*, Ingest-*). Each with per-change snapshot, dry_run, then commit. **Not found (2):** genesis-docs-timeline-companion-2026-03-02-0200.md, Genesis-Mythos/docs--azgaar_integration_report_2025-12-30.md (may already be archived or path mismatch).

**Remaining (54):** All in 3-Resources. Re-run ARCHIVE MODE full sweep to apply (ensure_structure → per-change snapshot → dry_run → commit). Proposed paths: 3-Resources/… → 4-Archives/Resources/….

Flag: none.
2026-03-07 00:50:00Z | ARCHIVE full sweep continue 2 | Archive | Batch snapshot 2026-03-07T004500Z; 49 moved (6 Retro Snake, 43 Resources); 2 not found; 54 pending | 90% | 4-Archives/Resources/* | #full-sweep

---

## 2026-03-07 — ARCHIVE MODE full sweep (continue 3) #full-sweep — COMPLETE

**Pipeline:** autonomous-archive. **Trigger:** Same full-sweep; final batch of 43 notes in 3-Resources.

**Backup:** `obsidian_ensure_backup` confirmed (max_age 1440 min). **Batch snapshot:** Backups/Batch/2026-03-07T005500Z-batch-archive-full-sweep-continue3.md.

**Moved this run (43):** MCP-Descriptor-Descriptions, MCP-Obsidian/* (15), obsidian_snapshot_TOOL, OG-minecraft/* (6), player-basic-rules-pdf-attachment, Plugins-Usage/* (4), Restore-Queue, Resurface, Roadmap-Standard-Format, Rules-Recreation-*, Task-Queue, Testing/* (5), TTRPGs/Rulebooks/dnd basic rules, Vault-Change-Monitor, Visual-Health-Dashboard, Watcher-Request.sync-conflict, Watcher/* (4), why-genesis-roadmap-should-be-project, Workflows-Pipelines-Skills-Report, Zettelkasten-PKM/* (2). Each with per-change snapshot (Res-cont3-*), dry_run, then commit.

**Remaining: 0.** Full sweep of 1-Projects, 2-Areas, 3-Resources complete. All non-protected notes are now under 4-Archives (Projects/{project}-Archive/…, Areas/…, Resources/…).

Flag: none.
2026-03-07 00:58:00Z | ARCHIVE full sweep continue 3 | Archive | Batch snapshot 2026-03-07T005500Z; 43 moved; 0 pending; full sweep COMPLETE | 90% | 4-Archives/Resources/* | #full-sweep

---

## 2026-03-07 — ARCHIVE MODE full sweep #full-sweep (re-run)

**Pipeline:** autonomous-archive. **Trigger:** Full sweep of 1-Projects, 2-Areas, 3-Resources; move non-protected notes to 4-Archives; age_days/no_activity_days ignored; backup and per-batch snapshot first; dry_run before commit; exclude protected paths per Vault-Layout.

**Backup:** No backup required (0 candidates). **Batch snapshot:** Backups/Batch/2026-03-07T033200Z-batch-archive-full-sweep.md.

**Excluded (per Vault-Layout):** Backups/, *Log*.md, * Hub.md, Watcher-Signal.md, Watcher-Result.md, 3-Resources/Second-Brain/**, Second-Brain-Config.md, Errors.md, .technical/, Templates/, watcher-protected: true.

**Archive path convention (for reference):** 1-Projects/{project}/… → 4-Archives/Projects/{project}-Archive/…; 2-Areas/… → 4-Archives/Areas/…; 3-Resources/… → 4-Archives/Resources/{project-id or General}/….

**Candidates:** 0. 1-Projects and 2-Areas contain no .md files (already archived in prior sweep). All 3-Resources notes are protected (Logs, Hubs, Second-Brain backbone, Config, Errors, Watcher paths). **Moved:** 0.

Flag: none. #full-sweep
2026-03-07 03:32:00Z | ARCHIVE MODE full sweep | Archive | Batch snapshot 2026-03-07T033200Z; 0 candidates (all protected or folders empty); 0 moved | — | — | #full-sweep
2026-03-07 03:32:19Z | ARCHIVE MODE full sweep re-run | Archive | Batch snapshot Backups/Batch/2026-03-07T033200Z-batch-archive-full-sweep.md; 0 candidates (all protected or 1-P/2-A empty); 0 moved | — |  | #full-sweep

---

## ARCHIVE-GHOST-SWEEP (report-only) #ghost-sweep

**Pipeline:** archive-ghost-folder-sweep. **Trigger:** ARCHIVE-GHOST-SWEEP (manual).

**Result:** Identified **25 empty folders** under 1-Projects and 3-Resources (left behind after full-sweep archive moves). **No folders removed:** MCP tool `obsidian_remove_empty_folder` is not available on the Obsidian MCP server; vault rules require folder removal via MCP only (no shell rmdir). To complete removal, add `obsidian_remove_empty_folder` to the server and re-run ARCHIVE-GHOST-SWEEP.

**Empty folders (deepest first):**
| Folder |
|--------|
| 1-Projects/Retro Snake Game/Roadmap/Phase-6-Controls-Game-Loop |
| 1-Projects/Retro Snake Game/Roadmap/Phase-5-Scoring-UI |
| 1-Projects/Retro Snake Game/Roadmap/Phase-4-Collision-Detection |
| 1-Projects/Retro Snake Game/Roadmap/Phase-3-Food-Apple |
| 1-Projects/Retro Snake Game/Roadmap/Phase-2-Snake |
| 1-Projects/Retro Snake Game/Roadmap/Phase-1-Game-Grid |
| 1-Projects/Pong-Game/Roadmap/Phase-4-UI-Game-Loop |
| 1-Projects/Pong-Game/Roadmap/Phase-3-Collision-Scoring |
| 1-Projects/Pong-Game/Roadmap/Phase-2-Ball-Physics |
| 1-Projects/Pong-Game/Roadmap/Phase-1-Paddle-Controls |
| 1-Projects/Genesis-Mythos/Roadmap/Phase-6-Wizard |
| 1-Projects/Genesis-Mythos/Roadmap/Phase-5-Politics |
| 1-Projects/Genesis-Mythos/Roadmap/Phase-4-Combat |
| 1-Projects/Genesis-Mythos/Roadmap/Phase-3-Lore |
| 1-Projects/Genesis-Mythos/Roadmap/Phase-2-Terrain3D |
| 1-Projects/Genesis-Mythos/Roadmap/Phase-1-Maps |
| 3-Resources/TTRPGs/Rulebooks |
| 1-Projects/Example/Roadmap |
| 3-Resources/Zettelkasten-PKM |
| 3-Resources/Watcher |
| 3-Resources/Testing |
| 3-Resources/Reference |
| 3-Resources/Plugins-Usage |
| 3-Resources/OG-minecraft |
| 3-Resources/MCP-Obsidian |
| 3-Resources/Highlightr |
| 3-Resources/Genesis-Mythos |
| 3-Resources/Cursor-Ingest |
| 1-Projects/OG-minecraft |

**Blacklist applied:** PARA roots (1-Projects, 2-Areas, 3-Resources as top-level only), /Templates/, /.technical/, /Backups/ — none of the above match.

Flag: #ghost-sweep (report-only; MCP tool not available).

---

## ARCHIVE-GHOST-SWEEP (re-run) #ghost-sweep

**Pipeline:** archive-ghost-folder-sweep. **Trigger:** ARCHIVE-GHOST-SWEEP (manual).

**Result:** Same **25 empty folders** still present under 1-Projects and 3-Resources. **obsidian_remove_empty_folder** is now available on the MCP server; calls with `dry_run: true` returned **empty_check_failed — "Directory not found"** for tested paths (e.g. `1-Projects/Retro Snake Game/Roadmap/Phase-6-Controls-Game-Loop`, `3-Resources/MCP-Obsidian`). Likely cause: vault root or path resolution mismatch on the server (e.g. `root_path` or `OBSIDIAN_VAULT_PATH`). **No folders removed.** Fix MCP server vault path / root_path so folder_path resolves, then re-run ARCHIVE-GHOST-SWEEP.

Flag: #ghost-sweep (report-only; tool path resolution failed).

---

## ARCHIVE-GHOST-SWEEP (completed) #ghost-sweep

**Pipeline:** archive-ghost-folder-sweep. **Trigger:** ARCHIVE-GHOST-SWEEP (manual).

**Result:** **33 empty folders removed** via `obsidian_remove_empty_folder` (vault-relative paths; dry_run then commit). Pass 1: 25 leaf folders (Phase-* roadmaps, Cursor-Ingest, Genesis-Mythos, Highlightr, MCP-Obsidian, OG-minecraft, Plugins-Usage, Reference, Testing, Watcher, Zettelkasten-PKM, TTRPGs/Rulebooks, Example/Roadmap, 1-Projects/OG-minecraft). Pass 2: 5 parents (Retro Snake Game/Roadmap, Pong-Game/Roadmap, Genesis-Mythos/Roadmap, TTRPGs, Example). Pass 3: 3 project roots (Pong-Game, Retro Snake Game, Genesis-Mythos). No blacklisted paths removed. **0 empty folders** remain under 1-Projects, 2-Areas, 3-Resources.

Flag: #ghost-sweep
