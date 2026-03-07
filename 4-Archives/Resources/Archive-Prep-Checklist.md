---
title: Archive Prep Checklist
created: 2026-03-01
tags: [pkm, second-brain, archive, testing, prep]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/README]]", "[[3-Resources/Cursor-Skill-Pipelines-Reference]]"]
---
# Archive Prep Checklist — Manual Pipeline Testing

Prep the vault so you can run **ARCHIVE MODE** (and other pipelines) manually with a clean slate: only **permanent** system/content stays in active PARA; everything else is either already archived or clearly marked as archive candidates.

## 1. What is permanent (do not archive)

These locations and patterns must **never** be moved to 4-Archives by the archive pipeline (and are excluded in auto-archive):

| Category | Paths / pattern |
|----------|------------------|
| **Backbone** | `3-Resources/Second-Brain/**` (README, Backbone, Pipelines, Logs, Rules, Skills, Configs, Parameters, Templates, Queue-Sources, MCP-Tools, Vault-Layout, Testing, tests/) |
| **Config & hubs** | `3-Resources/Second-Brain-Config.md`, `**/* Hub.md` (Resources Hub, Projects Hub, Areas Hub, Resurface) |
| **Logs** | `**/Log*.md` (Ingest-Log, Distill-Log, Archive-Log, Express-Log, Organize-Log, Backup-Log, Feedback-Log), `3-Resources/Errors.md` |
| **Watcher** | `Ingest/watched-file.md`, `3-Resources/Watcher-Signal.md`, `3-Resources/Watcher-Result.md`, any note with `watcher-protected: true` |
| **System** | `Backups/**`, `Templates/**`, `3-Resources/Second-Brain/tests/**`, `.cursor/**`, `.obsidian/**` |
| **Structure** | `5-Attachments/**` (folder structure); Ingest/ as folder (contents are processed, not the folder) |

**Archive pipeline** already excludes the above; this list is for your reference when deciding what to keep in place before a test run.

---

## 2. Archive candidates (prep for ARCHIVE MODE)

Content under **1-Projects**, **2-Areas**, and **3-Resources** that is *not* in the permanent list above is eligible for archiving when it meets archive-check (status complete, no open tasks, age threshold). Below is a snapshot for prep; run archive-check per note when you execute ARCHIVE MODE.

### 2.1 — 1-Projects

| Path | Notes |
|------|--------|
| `1-Projects/Example/Roadmap/Example-Roadmap.md` | Example project content |
| `1-Projects/Test-Project/*.md` | Test notes (split, distill, express) |
| `1-Projects/Test-Project/Versions/*.md` | Version snapshots — optional to archive with project or leave under Backups |
| `1-Projects/Example-Project.md` | Single-note project |

### 2.2 — 2-Areas

| Path | Notes |
|------|--------|
| `2-Areas/Example-Area.md` | Example area |

### 2.3 — 3-Resources (non-backbone)

These are in 3-Resources but are **not** backbone/config/logs/hubs; they are archive candidates if complete/inactive:

- `3-Resources/Commander-Plugin-Usage.md` — reference; keep if actively used
- `3-Resources/Vault-Change-Monitor.md` — dashboard; keep
- `3-Resources/Highlightr-Color-Key.md` — config reference; keep
- `3-Resources/Mobile-Toolbar-Task-Commands.md`, `3-Resources/Roadmap-Standard-Format.md`, `3-Resources/Task-Queue.md` — keep if in use
- Dated/report notes (e.g. `2026-02-23-*`, `2026-02-24-*`, `2026-02-25-*`, audits, MCP tool docs, test-prep notes) — **good candidates** to archive for testing
- `3-Resources/Restore Hub.md` — keep for restore workflow
- `3-Resources/Mobile-Pending-Actions.md` — keep; queue/async
- Watcher / EAT / workflow notes — keep if part of active setup

When prepping for testing, consider archiving the **dated reference and test-prep notes** in 3-Resources so the vault is lean; keep hubs, config, logs, and Second-Brain/ intact.

### 2.4 — Already in 4-Archives

- `4-Archives/Test-Project-Archive/2026-02-25-archive-candidate.md`
- `4-Archives/Test-Project-Archive/2026-02-25-archive-candidate-2.md`
- `4-Archives/Example-Archive.md`

No action; pipeline does not re-process 4-Archives.

---

## 3. Root-level and Ingest cleanup (before testing)

### 3.1 — Root-level files (move or archive)

These are **outside** PARA and should be cleaned so the vault root is minimal for testing:

| File at vault root | Suggested action |
|---------------------|------------------|
| `Ingest-Log.md` | Move to `3-Resources/Ingest-Log.md` if not already there; delete duplicate at root |
| `Ingest-Log.sync-conflict-20260301-040823-4EESXVM.md` | Resolve conflict; keep one Ingest-Log in 3-Resources; archive or delete conflict copy |
| `Untitled.md`, `Untitled 1.md` … `Untitled 6.md` | Move to Ingest for processing, or to `4-Archives/Pre-Archive-Root-Cleanup/` |
| `Untitled.sync-conflict-20260224-212757-6BSAQAK.md` | Archive or delete after resolving |
| `structure.md`, `V4 Draft.md`, `V4 Draft Thoughts.md` | Move to Ingest then process, or archive to 4-Archives/Pre-Archive-Root-Cleanup/ |
| `Periodic-Notes-Setup.md`, `PARA-Dashboard.md`, `Ingest-Review.md`, `Master goal task migration.md`, `Virginal testing.md`, `Capture-Guide.md` | Move to Ingest and run INGEST MODE, or archive if intentionally inactive |
| `README.md` | Keep at root (vault readme) |
| `Areas Hub.md`, `Resources Hub.md`, `Projects Hub.md`, `Resurface.md` | Move into `3-Resources/` if your layout keeps hubs there; pipeline excludes `* Hub.md` |

**Recommendation**: Move root-level content into **Ingest/** (then run INGEST MODE) or into **4-Archives/Pre-Archive-Root-Cleanup/** so that the archive pipeline only sees notes under 1-Projects, 2-Areas, 3-Resources.

### 3.2 — Ingest/

- **Process first**: Run **INGEST MODE** (or Process Ingest) so that Ingest/*.md are classified and moved to PARA; then run ARCHIVE MODE on the resulting locations.
- **Or** leave in Ingest and exclude from archive (archive pipeline processes 1–3, not Ingest).
- **Watcher**: Do not move `Ingest/watched-file.md` (excluded).
- **Non-.md**: `later.txt` and any binaries — handle per ingest-processing / non-markdown rules; add `#needs-manual-move` if leaving in Ingest.

---

## 4. Order of operations (manual test)

1. **Backup**  
   Run `obsidian_create_backup` (or ensure recent backup via Watcher/MCP) before any destructive steps.

2. **Root cleanup**  
   Move root-level orphans into Ingest or 4-Archives/Pre-Archive-Root-Cleanup; resolve sync conflicts; ensure only one Ingest-Log in 3-Resources.

3. **Optional — process Ingest**  
   Run **INGEST MODE** so all Ingest/*.md are in PARA; then you have a clear set of project/area/resource notes to archive.

4. **Run ARCHIVE MODE**  
   Trigger **ARCHIVE MODE – safe batch autopilot** on a **small scope** first (e.g. `1-Projects/Test-Project` or a single folder). Confirm:
   - Per-change snapshots under Backups/Per-Change
   - Moves to 4-Archives/… with expected paths
   - Entries in Archive-Log.md and Backup-Log.md

5. **Verify**  
   Check Archive-Log.md, Backup-Log.md, and 4-Archives for expected moves; fix any #review-needed.

---

## 5. Scope for first archive test

- **Recommended**: Run ARCHIVE MODE on **1-Projects/Test-Project** (and optionally 1-Projects/Example) so only test/example project notes are archived.
- **Then**: Expand to 2-Areas (e.g. Example-Area) and to 3-Resources dated/test-prep notes if desired.

This keeps the first manual run small and reversible.

---

## 6. Quick reference — permanent vs archiveable

- **Permanent**: Second-Brain/, Config, * Hub.md, **/Log*.md, Errors.md, Watcher paths, Backups/, Templates/, tests/, .cursor, .obsidian.
- **Archiveable**: Completed/inactive notes in 1-Projects, 2-Areas, and 3-Resources that are not in the permanent list and pass archive-check (no open tasks, status complete, age).

After prep, the vault is ready for manual pipeline testing with a clear boundary between permanent system content and archive candidates.

## Review Needed
Proposed para-type: resource. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.