---
name: Starter Kit Onboarding Roadmap – First Project Activation
overview: "Pivot onboarding from 'understand Curator' to 'get your first real project living in the system'. Four-phase funnel: Discovery → Minimal Setup → Feed First Project → Make It Yours. No pipeline/code changes—content and framing only."
todos: []
isProject: false
---

# Starter Kit Onboarding Roadmap – Pivot to First Project Activation

## Current state (problems with original approach)

- No dedicated onboarding roadmap that actually gets the user to produce value quickly.
- Welcome-to-Curator.md and Install-and-Setup.md are passive / instructional.
- Testing-Checklist.md is verification-oriented, not value-creation-oriented.
- Users finish setup → feel accomplished → but still don't have momentum on their actual life/work.
- Onboarding feels like "learn the tool" instead of "use the tool to make progress on something that matters to me".

## New goal

Shift onboarding from **"understand Curator"** → **"set up your environment quickly so you can create and activate your first real project inside the system"**.

Core funnel becomes:

1. **Discovery** (why + define your first project)
2. **Fast Setup** (just enough to run ingestion & basic organization)
3. **First Project Creation** (ingest initial material → organize → distill → express something usable)
4. **Activation & Continuation** (project is live, user knows how to keep feeding & using it)

The roadmap should feel like **"I now have a living project in my Second Brain"** rather than "I now understand how Curator works".

---

## Implementation

### 1. Create `0-Onboarding/First-Project-Roadmap.md`

**Location:** `Second-Brain-Starter-Kit/0-Onboarding/First-Project-Roadmap.md`  
(Rename from Onboarding-Roadmap.md – stronger title signal.)

**Frontmatter:**

```yaml
title: First Project Roadmap – Get Your Real Work Into the System
created: 2025-02-28
tags: [onboarding, roadmap, first-project]
roadmap: true
para-type: Resource
status: active
```

**Top callout:**

> This is **not** a tour of the tool.  
> This is the fastest path to get your first real project living and breathing inside Curator.  
> By the end you should have:  
> • A project folder with your initial material  
> • At least one distilled / actionable note  
> • Confidence to keep feeding and using the system  

**Structure (four tight phases):**

#### Phase 1 – Choose & Name Your First Project (~10–20 min)

- Read [[Welcome-to-Curator]] (just the "why this exists" parts – skip heavy theory)
- Decide on **one** small-but-meaningful project / area you want to make progress on in the next 2–6 weeks  
Examples:  
• Write a 10-page personal essay / blog series  
• Research & plan next career move  
• Learn topic X and produce summary notes / cheat sheet  
• Capture & organize family history / genealogy  
• Build reading & literature notes for book Y  
• Plan 2025 fitness / habit overhaul  
- Write the project name and 1–2 sentence goal in a new scratch note (you'll ingest it soon)  
Title suggestion: `2025-03 My First Project – Essay on X` or simply: `Project – [Your Working Title]`

#### Phase 2 – Minimal Setup (just enough to ingest & organize) (~30–60 min)

- Open vault in Obsidian
- Install & enable **only the must-have plugins** first (defer nice-to-haves):
  - Dataview
  - Tasks
  - Templater
  - QuickAdd
  - Watcher
  - Local REST API (for Cursor ↔ Obsidian bridge)
- Open vault folder in Cursor
- Set your API key in Cursor
- Test basic ingestion:
  - Drop your scratch project note into Ingest/
  - Run "Process Ingest" (or equivalent command) in Cursor
  - Confirm it lands somewhere in 1-Projects/ or gets tagged appropriately
- Quick health check: see the moved note, open it, make sure frontmatter & basic links are there

(Mobile and advanced plugins can come later – goal is motion, not perfection.)

#### Phase 3 – Feed Your First Project (~30–90 min)

- Ingest your initial material (aim for 3–10 items to start)
  - Drop PDFs, web clips, voice notes, your own braindumps into Ingest/
  - Run Process Ingest after each batch (or let Watcher do it)
- Tag / name items so they route to your new project
  - Use `#project-your-project-slug` or similar
  - Or put project name in title / YAML
- Run Organize pipeline once everything is ingested
  - Confirm notes are landing in `1-Projects/Your-Project-Name/`
- Run Distill on key notes or on the whole project folder
  - Goal: produce at least one crisp summary / key-insights note
- (Optional but powerful) Run Express to generate:
  - Outline
  - First-draft paragraphs
  - Questions for further research
  - Task list for next steps

#### Phase 4 – Make It Yours & Keep Going (~15–30 min)

- Create or refine the project's "home note" (MOC / dashboard)
  - Link to key ingested notes
  - Add active tasks using Tasks plugin syntax
  - Embed / query recent distill outputs
- Add one new capture (quick thought, article, todo) and ingest it → watch it land correctly
- Say "First project active" (or similar trigger phrase) in Cursor if you have a completion hook
- Decide your next small action (write for 20 min, read one paper, capture 3 more ideas…)
- (Optional) Move or archive 0-Onboarding/ once you feel independent

---

### 2. Surface the new focus in welcome files

**Welcome-to-Curator.md**

- Replace / augment "Next steps" section with:
  > The fastest way to get value: follow [[First-Project-Roadmap]]  
  > Goal: in under 2 hours you have your first real project alive in the vault.

**Install-and-Setup.md**

- Add prominent banner at top:
  > Don't read this file end-to-end yet.  
  > Jump to [[First-Project-Roadmap]] → Phase 2 for the **minimal** setup needed to start your project.  
  > Come back here later for advanced configuration.

**Welcome-to-Second-Brain.md** (if it exists)

- Update to:
  > Start here: [[First-Project-Roadmap]] – get your actual work into the system today.

---

### 3. Deprecate / reposition Testing-Checklist.md

Add banner at top:

> This checklist is for later – once your first project is running and you want to verify / tune every pipeline step.  
> New users: focus on [[First-Project-Roadmap]] first.

---

### 4. Optional but recommended – Roadmap-Format guidance

In **3-Resources/Roadmap-Format.md** (create if it doesn't exist):

- Show [[First-Project-Roadmap]] as living proof that simple nested phases + subtasks are enough for 90% of use cases.
- Encourage users: "Start every new project with a tiny roadmap like this one".

---

## Summary of changes / migration path


| Old focus                 | New focus                              |
| ------------------------- | -------------------------------------- |
| "Understand the system"   | "Get your first project alive"         |
| Learn all plugins upfront | Minimal plugins to ingest & organize   |
| Test pipelines            | Feed real content → see real outputs   |
| Onboarding = completion   | Onboarding = momentum on personal goal |


---

## Deliverables checklist

- Rename / create `0-Onboarding/First-Project-Roadmap.md` with the structure above
- Update Welcome-to-Curator with strong pointer to the new roadmap
- Add minimal-setup callout to Install-and-Setup.md
- Add banner to Testing-Checklist.md repositioning it as "later"
- (Optional) Create or update `3-Resources/Roadmap-Format.md` showing the first-project roadmap as exemplar

**Scope:** No pipeline code changes, no MCP prompt changes, no Cursor rule changes – **pure content & framing pivot**.