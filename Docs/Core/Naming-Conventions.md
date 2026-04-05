---
title: Naming Conventions
created: 2026-03-01
tags: [pkm, second-brain, naming, conventions]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/README]]"]
---

**TL;DR** — Note format: `kebab-slug-YYYY-MM-DD-HHMM.md` (slug first, date and time at end). Time 24-hour; source priority: created frontmatter → file mtime → ingest/now. Referenced by Parameters, subfolder-organize, name-enhance.

---

# Naming Conventions

Single source of truth for note and file naming in the vault. Referenced by [[Parameters]], [[.cursor/rules/always/second-brain-standards|second-brain-standards]], [[Templates]], [[Vault-Layout]], [[.cursor/skills/subfolder-organize/SKILL|subfolder-organize]], and [[.cursor/skills/name-enhance/SKILL|name-enhance]].

## Regular notes

**Core format**: `kebab-slug-YYYY-MM-DD-HHMM.md` — semantic slug first, **date and time at the end** = human-readable + searchable + sort-by-time. Time is 24-hour (e.g. `1430` for 2:30 PM). When time is unknown, use `0000`.

### Date and time source priority

1. **`created` frontmatter** (if present and reliable; parse date and optional time)
2. **File creation date/time** (fs stat)
3. **Ingest / current date and time** (fallback)

### Slug rules

- **Max ~60–70 chars** — truncate smartly if needed.
- **Lowercase, kebab-case** (hyphens); no special chars except numbers, letters, hyphens.
- **Source priority**: Prefer first real heading > TL;DR sentence > first sentence summary.
- **Stop-words**: Remove at start/end if they make slug worse (a, the, of, using, etc.).
- **Generic slugs**: If slug would be too generic after cleaning (e.g. "note-on-x"), append short disambiguator from content (e.g. "note-on-x-2025-q1-review").

### Daily / same-day notes

If multiple notes created/ingested in the same minute on the same topic → use distinct time (e.g. +1 minute) or append `-2`, `-3` to the slug; or derive from content to avoid numbers when possible.

### Display names

Filename is primarily a **stable identifier + retrieval cue**. Frontmatter `title:` or `aliases:` can hold prettier or longer display names if desired.

### Research notes (Ingest/Agent-Research/)

Notes created by the research-agent use the same core format `kebab-slug-YYYY-MM-DD-HHMM.md`. **Slug source**: derive from `research_query` (e.g. "faction state persistence" → `faction-state-persistence`) or from `linked_phase` (e.g. `Phase-4-1`); optionally combine both, e.g. `faction-state-persistence-Phase-4-1-2026-03-09-1430.md`. Keeps research notes findable by phase and query.

---

## MOCs

`Topic MOC.md` or `ProjectName MOC.md`. Avoid renaming unless explicitly requested (see [[.cursor/skills/name-enhance/SKILL|name-enhance]] skill).

---

## Hubs

`X Hub.md`. Excluded from pipelines; do not rename via automation.

---

## Project Master Goal notes

**Preferred**: `<project-slug>-Master-Goal.md` or `Project-Master-Goal.md` (under `1-Projects/<project-id>/`).

**Allowed variations**: `*Master-Goal*.md`, `*MasterGoal*.md` — used by roadmap-generate-from-outline and link-to-pmg-if-applicable to detect the canonical goal note for a project.

**Discouraged**: `Goal.md`, `Roadmap.md` (too generic; name-enhance should propose a better, detectable name).

---

## Project folder

Folder name = project name. Renaming a project folder is manual/merge-only; the name-enhance skill only renames **notes**, not folders.

---

## Attachments

Preserve or suggest descriptive name on move to `5-Attachments/` (see ingest-processing "Bonus" callout for optional rename suggestion during move).

---

## Vague / untitled

Filenames like Untitled, Note, Document, etc. are candidates for name-enhance during ingest and name re-evaluation (NAME-REVIEW queue or opportunistic organize).
