---
title: Genesis ingest classification context (prep step + sub-roadmap)
created: "2026-03-02 05:55"
tags: [ingest, raw-capture, stray-thought, meta, classification]
para-type: resource
status: ingest
ingest-type: stray-thought
project-id: genesis-mythos
highlight_key: Genesis-Mythos-Key
highlight_perspective: geosynchronous-view
---
# Stray Thought

## What am I thinking?

Prior EAT-QUEUE ingest classified two notes incorrectly. **Genesis task.md** was classified as Archive (70%) — wrong: it is a **roadmap item / prep step** to be added before any other Genesis items are built (e.g. "add a section to account for Cursor dev"; rules, skills, sub-agents, Cursor plugins, MCP servers). **Genesis week One.md** was classified as Project (70%) — misleading: it is not a new project but a **sub-roadmap** belonging to the pre-existing **Genesis** project (Master goal for Genesis). Use this context when re-running ingest: Genesis task = prep-step roadmap item; Genesis week One = sub-roadmap under 1-Projects/Genesis (or linked to the existing Genesis project).

## What does this seem to mean?

Re-run ingest with project-id / project_name set to **Genesis** for both notes. Treat Genesis task as a roadmap/prep item (e.g. ADD-ROADMAP-ITEM or phase 0) and Genesis week One as project content under Genesis, not a standalone project.

## TL;DR

Genesis task = prep-step roadmap item (add before other items). Genesis week One = sub-roadmap to pre-existing Genesis project. Re-classify with Genesis context; do not treat as Archive or as new Project.

---

## Re-run outcome (2026-03-02)

- **Genesis week One.md** → re-classified Project 88% (project-id Genesis); **moved** to `1-Projects/Genesis/Genesis week One.md`.
- **why-genesis-roadmap-should-be-project-2026-03-02-0522.md** → re-classified Project 88%; **moved** to `1-Projects/Genesis/why-genesis-roadmap-should-be-project-2026-03-02-0522.md`.
- **Genesis task.md** → moved to `1-Projects/Genesis/Genesis task.md` on explicit user clarification (name = Genesis project); prep-step roadmap item.
- This note (context) → 70%; left in Ingest for reference.

## Review Needed
Proposed para-type: project. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.

## Why resource?
Assigned based on content/frontmatter (confidence ~85%).