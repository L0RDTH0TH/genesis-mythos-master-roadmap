---
title: Test prep — autonomous-distill
created: 2026-02-25
para-type: Resource
status: active
tags: [test-prep, pipelines, autonomous-distill]
---
# Test prep — autonomous-distill

Summary of preparations for **Goal 1: Run distill batch** (5–10 notes, preferably from Ingest/ or Resources).

## Fixes implemented

- **3-Resources/Distill-Log.md**: Added an "Example entries (template)" section with two sample log lines so the log has a clear format reference before the first real run. Pipeline can append below these.

## Test data prepared

- **1-Projects/Test-Project/2026-02-25-distill-messy.md** — Long, multi-paragraph note with several ideas; suitable for testing distill-highlight-color, layer-promote, callout-tldr-wrap, and readability-flag.
- **1-Projects/Test-Project/2026-02-25-distill-short.md** — Short note with existing TL;DR; tests callout wrap and minimal pipeline path.

Additional test notes can be added under `1-Projects/Test-Project/` (e.g. 3–5 more) to reach 5–10 for a full micro-batch.

## Readiness

**Mostly ready.** Distill-Log has example format; Test-Project has at least two notes. No pipeline has been run yet; first run will confirm snapshot and backup paths.

## User next steps

1. **Run a micro-batch (2–5 notes):** In Cursor, say: **"DISTILL MODE – safe batch autopilot on 1-Projects/Test-Project/"** or **"Distill the notes in Test-Project"**. Scope the agent to only the test folder.
2. **Verify:** Check that `3-Resources/Distill-Log.md` and `3-Resources/Backup-Log.md` have new entries with backup and snapshot paths; confirm `Backups/Per-Change/` and `Backups/Batch/` get new files.
3. **Optional:** Add more dummy notes under Test-Project and run again to validate batch checkpoint every 3 notes.

## Review Needed
Proposed para-type: resource. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.