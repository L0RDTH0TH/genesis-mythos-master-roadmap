---
title: Test prep — post-split linking (split-link-preserve)
created: 2026-02-25
para-type: Resource
status: active
tags: [test-prep, pipelines, ingest, split_atomic]
---
# Test prep — post-split linking (split-link-preserve)

Summary of preparations for **Goal 5: Post-split linking / traceability** after `obsidian_split_atomic`.

- [x] **Create minimal "split from / split into" linking after obsidian_split_atomic** (2026-02-25): Children get `split_from: "[[Original Note Title]]"` in YAML + optional `related[]` append; original note gets ## Splits bullet list with one-line reason per child; idempotent; doc in Second-Brain-Limitations.md.

## Fixes implemented

- **.cursor/skills/split-link-preserve/SKILL.md**: Skill runs immediately after `obsidian_split_atomic` in full-autonomous-ingest. It:
  - Sets `split_from: "[[Original Note Title]]"` on each child; appends to `related[]` if present (no overwrite).
  - Appends (or updates) **## Splits** on parent with "Splits / Extracted" and bullets `- [[Child Title]] — brief one-line reason`.
  - Idempotent (no duplicate bullets/related); uses Obsidian backlinks for reverse nav.
  - Confidence gate ≥85%; uses read_note, manage_frontmatter, update_note/search_replace.
- **3-Resources/Cursor-Skill-Pipelines-Reference.md**:
  - Ingest table: added **split-link-preserve** row (slot: after split_atomic).
  - Pipeline order: inserted **split-link-preserve** between split_atomic and distill_note.
  - Skill locations table: added split-link-preserve path.
  - Flowchart: added E2[split_link_preserve] and chain E → E2 → F.
- **.cursor/rules/context/para-zettel-autopilot.mdc**: Skills line updated to include "after split_atomic → split-link-preserve".

## Test data prepared

- **1-Projects/Test-Project/2026-02-25-split-test-multi-idea.md**: Multi-idea note with three clear sections (progressive summarization, archive heuristics, express pipeline). **Copy this note to Ingest/** (e.g. `Ingest/2026-02-25-split-test-multi-idea.md`) then run the ingest pipeline; expect `obsidian_split_atomic` to produce 3 child notes and **split-link-preserve** to add `split_from` on each child and `split_into` (or "Split into" section) on the parent if it still exists.

## Readiness

**Mostly ready.** Skill is implemented and wired into the pipeline reference and ingest rule. One multi-idea test note is in Ingest/. Run the ingest pipeline once to validate that split_atomic runs and split-link-preserve runs after it and writes traceability metadata.

## User next steps

1. **Copy the test note to Ingest, then run ingest:** Copy `1-Projects/Test-Project/2026-02-25-split-test-multi-idea.md` to `Ingest/2026-02-25-split-test-multi-idea.md`. Then in Cursor, run the full ingest pipeline on it (e.g. **"Process Ingest: run full ingest on Ingest/2026-02-25-split-test-multi-idea.md"** or **"INGEST MODE – safe batch autopilot on Ingest/2026-02-25-split-test-multi-idea.md"**). Ensure backup and per-change snapshot run before split_atomic.
2. **Verify traceability:** After the run, open the new atomic child notes and the parent (if it still exists). Confirm frontmatter has `split_from` on children and `split_into` on parent (or a "Split into" section with wikilinks). Check Ingest-Log.md for an entry mentioning split-link-preserve.
3. **Optional:** Add a Dataview query in a test note or Resources to list "notes where split_from = ..." or "notes that have split_into" to confirm the metadata is queryable.

## Review Needed
Proposed para-type: resource. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.