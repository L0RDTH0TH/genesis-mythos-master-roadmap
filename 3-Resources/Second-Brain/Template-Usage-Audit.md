---
title: Template Usage Audit
created: 2026-03-14
tags: [second-brain, templates, audit, vestigial]
para-type: Resource
status: active
links: ["[[3-Resources/Second-Brain/Templates]]", "[[3-Resources/Second-Brain/README]]"]
---

# Template Usage Audit

Audit of **Templates/** in the vault: which templates are actually used by rules, skills, plugins, or docs, and which are vestigial (unused or superseded). Scope: repo root `Templates/`; excludes `Second-Brain-Starter-Kit/Templates/` (reference kit) and `.git-clones/`.

## Folder structure (organized)

- **Templates/Decisions/** — Decision wrappers (ingest, phase-direction).
- **Templates/Roadmap/** — Master-Goal, Hand-Off-Roadmap, Planning-Prompt-Task, Roadmap-*-Template.
- **Templates/Ingest/** — Ingest-Selector (.md + .tpl), Ingest-Template, By-Type/ (Stray-Thoughts, AI-Output, Link-Note).
- **Templates/Prompt-Components/** — Base-Prompt, Param-Defaults, Param-Overrides, Guidance-Default, Error-Handling-Template, Skill-Chain.
- **Templates/Notes/** — Session-Prep, Daily-Note-Template, Weekly-Note-Template, Mobile-AI-Question.
- **Templates/Chat/** — AI Prompts (copy-paste pipeline prompts).
- **Templates/Scripts/** — ProcessIngestTrigger.js (user script).

---

## Actually used (code, rules, or plugins)

| Template | Used by | Notes |
|----------|---------|--------|
| **Templates/Decisions/Decision-Wrapper.md** | Ingest pipeline (agents/ingest, legacy-agents/ingest), Pipelines.md, Cursor-Skill-Pipelines-Reference, Decision-Wrapper-Flow, auto-eat-queue (re-wrap), Templates.md | Filled by pipelines for mid/low/error wrappers; 7 options A–G. |
| **Templates/Decisions/Decision-Wrapper-Phase-Direction.md** | auto-queue-processor (EXPAND-ROAD post-step), Cursor-Skill-Pipelines-Reference | Phase-direction wrappers under Ingest/Decisions/Roadmap-Decisions/. |
| **Templates/Roadmap/Master-Goal.md** | roadmap-generate-from-outline (normalize seed), normalize-master-goal skill, Cursor-Skill-Pipelines-Reference, Roadmap-Skills-Overview, Templates.md | PMG structure (One-line, Vision, Phases, Technical Integration, TL;DR, Related). |
| **Templates/Roadmap/Hand-Off-Roadmap.md** | roadmap-resume skill (step 5: load hand-off template), Templates.md | Resumption prompt skeleton: previous_outputs, current_directive, open_tbd. |
| **Templates/Roadmap/Planning-Prompt-Task.md** | workspace, changelog (TASK-TO-PLAN-PROMPT, phase-direction comment injection), Templates.md | Placeholders: project_name, session_memory_hint, task_text, git_diff_hint. |
| **Templates/Prompt-Components/** (folder) | Backbone, Templates.md, Prompt-Crafter flows (Structure-Detailed, Commander-Plugin-Usage), changelog | Assembly: Base-Prompt → Param-Defaults/Param-Overrides → Guidance-Default → Error-Handling-Template → optional Skill-Chain. **Laptop prompt-crafter only**; not read by current question-led crafter (which uses User-Questions-and-Options-Reference). |
| **Templates/Ingest/By-Type/Stray-Thoughts.md** | Ingest-Selector (Templater), Vault-Layout, Templates.md | Ingest-Selector suggester includes this when user picks "Stray Thoughts". |
| **Templates/Ingest/By-Type/AI-Output.md** | Ingest-Selector (Templater), Vault-Layout, Templates.md | Ingest-Selector suggester includes this when user picks "AI Output". |
| **Templates/Ingest/By-Type/Link-Note.md** | Ingest-Selector (Templater), Vault-Layout, Templates.md | Ingest-Selector suggester includes this when user picks "Link Note". |
| **Templates/Ingest/Ingest-Selector.md** | Templater `data.json` (folder template for `Ingest`), Ingest-Selector content (links to By-Type) | Creating a note in Ingest triggers Templater to run this; user picks type → content from By-Type. |
| **Templates/Ingest/Ingest-Selector.tpl** | Templater plugin | **Required for Templater:** this file is what lets the Templater plugin work for the Ingest folder template. **Do not remove** — removing it will break Templater. |
| **Templates/Notes/Session-Prep.md** | Templater `data.json` (`startup_templates`) | Runs on Obsidian startup. |
| **Templates/Notes/Mobile-AI-Question.md** | Templater `data.json` (folder template for `Ingest/Mobile-Questions`), Templates.md | New note in that folder uses this template. |
| **Templates/Scripts/ProcessIngestTrigger.js** | Templater `user_scripts_folder: "Templates/Scripts"`; QuickAdd/macro docs in archives | User script; appends "Say in Cursor: INGEST MODE…" to Ingest-Log. Not auto-invoked by Templater; only if a macro calls it. |

---

## Documented / referenced but not code-driven

| Template | Referenced in | Notes |
|----------|----------------|--------|
| **Templates/Roadmap/Roadmap-Master-Template.md** | normalize-roadmap-mocs-and-templates plan, extend-roadmap-hierarchy plan | Created as “canonical source for future roadmap note creation”. **Skills do not read these files** — roadmap-generate-from-outline and roadmap-deepen build structure inline. Use: human copy-paste or future tooling. |
| **Templates/Roadmap/Roadmap-Primary-Template.md** | (same plan) | Same as above. |
| **Templates/Roadmap/Roadmap-Secondary-Template.md** | (same plan) | Same as above. |
| **Templates/Roadmap/Roadmap-Tertiary-Template.md** | (same plan), extend-roadmap-hierarchy plan | Same as above. |
| **Templates/Ingest-Template.md** | Vault-Layout, Templates.md (e.g. “Ingest-template”), Templates-Archive README | Generic ingest note template. No rule or skill **reads** it; listed as “for new notes”. Possibly redundant with By-Type + Ingest-Selector. |
| **Templates/Chat/AI Prompts.md** | Archives, automation recommendations, plugin reports | Copy-paste pipeline prompts (e.g. INGEST MODE block). **Canonical phrases** now live in `3-Resources/Second-Brain/Chat-Prompts.md`; this file is legacy / optional duplicate. |

---

## Vestigial or optional to remove

| Template | Reason |
|----------|--------|
| **Templates/Daily-Note-Template.md** | Mentioned in Templates.md diagram and Starter-Kit; **no** reference in rules, skills, or Templater config. Optional daily-note workflow. |
| **Templates/Weekly-Note-Template.md** | Same as Daily — docs/Starter-Kit only; not in Templater or pipeline rules. |
| **Templates/Chat-Prompts/** (folder) | Docs (Templates.md, Chat-Prompts.md, User-Flow) say optional location for copy-paste chat prompts. **Folder does not exist** in repo; only `3-Resources/Second-Brain/Chat-Prompts.md` exists as canonical. |

---

## Summary

- **Actively used by pipelines/plugins:** Decisions/*, Roadmap/Master-Goal, Hand-Off-Roadmap, Planning-Prompt-Task, Prompt-Components/*, Ingest/By-Type/*, Ingest/Ingest-Selector.md, **Ingest/Ingest-Selector.tpl** (required for Templater — do not remove), Notes/Session-Prep.md, Notes/Mobile-AI-Question.md; Scripts/ProcessIngestTrigger.js if invoked by a macro.
- **Documented, not code-read:** Roadmap/*-Template (reference only), Ingest/Ingest-Template.md; Chat/AI Prompts.md (legacy copy-paste, superseded by Chat-Prompts.md).
- **Vestigial / safe to archive:** Notes/Daily-Note-Template, Notes/Weekly-Note-Template unless you use them manually; Chat-Prompts/ is optional and currently missing.

---

## Recommendations

1. **Keep:** All “Actually used” templates and Prompt-Components; Roadmap/* if you want human copy-paste for new roadmap notes.
2. **Do not remove:** `Templates/Ingest/Ingest-Selector.tpl` — required for the Templater plugin; removing it will break Templater.
3. **Clarify:** Ingest-Template.md — either document as “generic ingest when not using selector” or merge into one of the By-Type templates and update docs.
4. **AI Prompts.md:** Either point to Chat-Prompts.md as canonical and mark AI Prompts “legacy”, or consolidate content and remove duplicate.
5. **Chat-Prompts folder:** Create `Templates/Chat-Prompts/` only if you want file-based copy-paste prompts in addition to `3-Resources/Second-Brain/Chat-Prompts.md`; otherwise treat the doc as single source of truth.
