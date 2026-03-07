---
title: Ingest failure – files not removed
created: 2026-03-02
tags: [ingest, meta, failure, pipeline]
para-type: resource
status: ingest
project-id: genesis-mythos
highlight_key: Genesis-Mythos-Key
highlight_perspective: geosynchronous-view
---
# Ingest failure – files not removed

## What happened

On **2026-03-02** the EAT-QUEUE ingest run processed two notes in `Ingest/`:

- **Genesis Roadmap.md** — classified as Resource (70%)
- **Master goal for Genesis.md** — classified as Project (70%)

Backup was created and classification ran, but **neither note was moved** out of Ingest. The pipeline stopped before the move step because confidence was below the 85% threshold (`review_required: true — do not move`).

## Failure

**Ingested files were left in Ingest.** Per pipeline design, successful ingest should end with notes moved to their target PARA location (e.g. `1-Projects/Genesis/`, `3-Resources/...`). That did not occur.

## Cause

Classification returned 70% for both notes; destructive actions (including `obsidian_move_note`) are only allowed at ≥85%. The run correctly refused to move but did not subsequently remove or relocate the files, so Ingest still contains the original captures.

## What to do

- Re-run classification with project context (e.g. Genesis) to raise confidence and then run move, or
- Manually move **Genesis Roadmap.md** and **Master goal for Genesis.md** to the appropriate project/resource paths after review.

## TL;DR

EAT-QUEUE ingest 2026-03-02: two notes classified at 70%; no move (threshold 85%). Files remain in Ingest. Documented so the failure is visible in the Ingest dir.

## Why resource?
Assigned based on content/frontmatter (confidence ~85%).