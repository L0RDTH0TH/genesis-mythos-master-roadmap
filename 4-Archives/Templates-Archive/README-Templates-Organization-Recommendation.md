---
title: Templates folder — organization recommendation (applied 2026-03-06)
created: 2026-03-06
archived_from: Templates/README-Templates-Organization-Recommendation.md
archived_date: 2026-03-06
tags: [templates, organization, recommendation]
status: archived
---

# Templates folder — organization recommendation

**Scope:** Vault root `Templates/` only (excludes `Second-Brain-Starter-Kit/Templates/`).  
**Applied 2026-03-06:** Ingest by-type consolidated to `Templates/Ingest/By-Type/`; root duplicates and `Ingest-Template/` subfolder archived to `4-Archives/Templates-Archive/`; PARA templates (Area, Resource, Project) archived; Templater folder_templates for 1-Projects, 2-Areas, 3-Resources removed.

---

## 1. Confirmed in use (you)

| Template | Purpose |
|----------|---------|
| **AI-Output.md** | Ingest-type template for AI output captures; docs and pipelines reference it. |
| **Decision-Wrapper.md** | Canonical A–G wrapper for ingest/organize/archive/distill/express/error pipelines; created under `Ingest/Decisions/**`. Heavy refs in para-zettel-autopilot, Pipelines, MCP-Tools, confidence-loops. |
| **Link-Note.md** | Ingest-type template for link/source notes. |
| **Stray-Thoughts.md** | Ingest-type template for quick captures. |

---

## 2. Trace of other templates (what they're for)

| File / folder | Where referenced | Purpose |
|---------------|------------------|---------|
| **Prompt-Components/** | `3-Resources/Second-Brain/Templates.md`, Prompt-Crafter flows, Commander-Plugin-Usage, Backbone, prompt-crafter plan, changelog | **Prompt-crafter (laptop):** Assembly for queue/crafter: Base-Prompt → Param-Defaults/Param-Overrides → Guidance-Default → Error-Handling-Template → optional Skill-Chain. Used to build MCP params from Second-Brain-Config. |
| **Decision-Wrapper.md** | *(see above)* | Pipeline-critical; single source of truth for A–G wrappers. |
| **Scripts/ProcessIngestTrigger.js** | Audit notes, plugin reports, Templater `data.json` (`user_scripts_folder: "Templates/Scripts"`) | Obsidian-side script: appends "Say in Cursor: INGEST MODE…" (or similar) to Ingest-Log when Ingest has notes. QuickAdd/Templater user script. |
| **Session-Prep.md** | Audit, Starter-Kit, Templater `data.json` (`startup_templates: ["Templates/Session-Prep.md"]`) | Templater **startup template**: on vault load, if Ingest has .md files, appends reminder to run INGEST MODE to Ingest-Log. |
| **Ingest-Template.md** | workspace.json, audit | Generic **raw-capture** ingest template (Templater placeholders). |
| **Ingest-Selector.md** | Templater `data.json` (folder template for `Ingest`), Ingest-Selector.tpl | **Templater script**: suggester that offers "Stray Thoughts" / "AI Output" / "Link Note" and includes content from `Ingest-Template/*`. |
| **Ingest-Selector.tpl** | Only in archived audits (Ingest-2026-03-01, Pre-Archive-Root-Cleanup) | Legacy/alternate form of selector; current config uses `Ingest-Selector.md`. |
| **Ingest-Template/** (subfolder) | **Only** `Ingest-Selector.md` (and .tpl) | Contains **selector targets**: AI-Output, Stray-Thoughts, Link-Note. Duplicates of root `AI-Output.md`, `Stray-Thoughts.md`, `Link-Note.md`; selector points here. |
| **AI-Output.md**, **Stray-Thoughts.md**, **Link-Note.md** (root) | Templates.md, you | Canonical ingest-type templates; used when creating notes directly. |
| **Mobile-AI-Question.md** | Templates.md, Templater `data.json` (folder template for `Ingest/Mobile-Questions`) | Template for mobile AI query captures. |
| **Daily-Note-Template.md**, **Weekly-Note-Template.md** | Second-Brain-Starter-Kit README only | PARA/daily-weekly structure; not referenced by rules or pipelines. |
| **Area-Template.md**, **Resource-Template.md**, **Project-Template.md** | Example-Area, Example-Project, Starter-Kit README, **Templater** `data.json` (folder templates for 2-Areas, 3-Resources, 1-Projects) | PARA structure templates when creating new Area/Resource/Project. |
| **AI Prompts.md** | Automation recommendations, audit | **Copy-paste** pipeline prompts (e.g. INGEST MODE block) for Cursor chat. |
| **AI Prompts.md** (content) | — | Contains "INGEST MODE – safe batch autopilot" and similar blocks. |

---

## 3. Recommended organization (subdirs by use)

Proposed layout so that **usage** is clear and **Templater/scripts** keep working. If you adopt this, you must update **Templater** `data.json` (and any Obsidian plugin paths) to the new paths.

### Option A — By usage (recommended)

```
Templates/
├── README-Templates-Organization-Recommendation.md   # this note (or move to 3-Resources)
├── Decision-Wrapper.md                               # pipelines (keep at root or under Pipelines/)
├── Prompt-Components/                                # unchanged; prompt-crafter
│   ├── Base-Prompt.md
│   ├── Param-Defaults.md
│   ├── Param-Overrides.md
│   ├── Guidance-Default.md
│   ├── Error-Handling-Template.md
│   └── Skill-Chain.md
├── Ingest/                                           # all ingest-related
│   ├── Ingest-Template.md                             # raw capture
│   ├── Ingest-Selector.md                             # Templater suggester (update links to Ingest/By-Type/ below)
│   ├── Ingest-Selector.tpl                            # optional; archive if unused
│   ├── Mobile-AI-Question.md
│   └── By-Type/                                      # selector targets (currently Ingest-Template/)
│       ├── AI-Output.md
│       ├── Stray-Thoughts.md
│       └── Link-Note.md
├── Pipelines/                                        # pipeline-critical + copy-paste
│   └── Decision-Wrapper.md                           # if you prefer it under Pipelines/
├── Chat-Prompts/                                     # optional; copy-paste for Cursor
│   └── AI-Prompts.md                                 # rename from "AI Prompts.md" for consistency
├── PARA/                                             # structure templates
│   ├── Project-Template.md
│   ├── Area-Template.md
│   ├── Resource-Template.md
│   ├── Daily-Note-Template.md
│   └── Weekly-Note-Template.md
├── Scripts/                                          # unchanged
│   └── ProcessIngestTrigger.js
└── Session-Prep.md                                   # startup; keep at root so path stays simple
```

- **Root** `AI-Output.md`, `Stray-Thoughts.md`, `Link-Note.md`: either **remove** (and point direct usage to `Ingest/By-Type/`) or **keep as shortcuts** that duplicate or link to `Ingest/By-Type/` so "create from template" still works without changing Obsidian template picker.
- **Ingest-Selector**: today it points to `Templates/Ingest-Template/…`. If you move to `Ingest/By-Type/`, update the three `[[Templates/Ingest-Template/…]]` links in `Ingest-Selector.md` to `[[Templates/Ingest/By-Type/…]]`.

### Option B — Minimal change (only group + archive)

- Add **Templates/PARA/** and move **Project-Template**, **Area-Template**, **Resource-Template**, **Daily-Note-Template**, **Weekly-Note-Template** there. Update Templater folder templates to `Templates/PARA/Project-Template.md` etc.
- Add **Templates/Archive/** and move **Ingest-Selector.tpl** there (only archived audits reference it; active config uses `.md`).
- Leave everything else in place (no consolidation of Ingest-Template/ with root).

---

## 4. Archive candidates (not used by rules/pipelines)

| Item | Recommendation |
|------|----------------|
| **Ingest-Selector.tpl** | **Archive** under `Templates/Archive/` or `4-Archives/Templates-Archive/`. Only mentioned in old audits; live setup uses `Ingest-Selector.md`. |
| **Daily-Note-Template.md**, **Weekly-Note-Template.md** | **Optional archive** if you don't use daily/weekly notes; otherwise keep (e.g. under `Templates/PARA/`). |
| **Duplicate content** | **Ingest-Template/AI-Output.md**, **Stray-Thoughts.md**, **Link-Note.md** duplicate root. Either: (1) remove root copies and point all refs to `Ingest-Template/` (or `Ingest/By-Type/`), or (2) remove Ingest-Template/ and change Ingest-Selector to use root `Templates/AI-Output.md` etc., so one set of files. |

Existing **4-Archives/Templates-Archive/** already holds e.g. `Decision-Wrapper-legacy-5-option.md`; use the same location for archived templates.

---

## 5. Paths to update if you move files

- **Templater** (`.obsidian/plugins/templater-obsidian/data.json`):
  - `templates_folder`: currently `"Templates"` (unchanged if you keep templates under `Templates/`).
  - `user_scripts_folder`: `"Templates/Scripts"` (unchanged if Scripts stays).
  - `folder_templates`: update any path that points to a moved file, e.g.  
    `Ingest` → `Templates/Ingest/Ingest-Selector.md`,  
    `1-Projects` → `Templates/PARA/Project-Template.md`,  
    `2-Areas` → `Templates/PARA/Area-Template.md`,  
    `3-Resources` → `Templates/PARA/Resource-Template.md`,  
    `Ingest/Mobile-Questions` → `Templates/Ingest/Mobile-AI-Question.md`.
  - `startup_templates`: `Templates/Session-Prep.md` (unchanged if Session-Prep stays at root).
- **Ingest-Selector.md**: if you rename `Ingest-Template/` to `Ingest/By-Type/`, replace:
  - `[[Templates/Ingest-Template/Stray-Thoughts]]` → `[[Templates/Ingest/By-Type/Stray-Thoughts]]`
  - `[[Templates/Ingest-Template/AI-Output]]` → `[[Templates/Ingest/By-Type/AI-Output]]`
  - `[[Templates/Ingest-Template/Link-Note]]` → `[[Templates/Ingest/By-Type/Link-Note]]`
- **Rules/docs**: no hardcoded paths to PARA or Chat-Prompts templates in pipeline rules; only `Templates/Decision-Wrapper.md` is fixed. Update that only if you move Decision-Wrapper (e.g. to `Templates/Pipelines/Decision-Wrapper.md`).

---

## 6. One-line summary

- **Keep as-is (critical):** Decision-Wrapper.md, Prompt-Components/, Scripts/, Session-Prep.md, AI-Output, Stray-Thoughts, Link-Note (either root or Ingest/By-Type/), Ingest-Selector.md, Ingest-Template.md, Mobile-AI-Question.md, Area/Resource/Project templates (or under PARA/).
- **Organize by use:** Ingest/*, PARA/*, optional Chat-Prompts/, optional Pipelines/.
- **Archive:** Ingest-Selector.tpl; optionally Daily/Weekly if unused; optionally one of the duplicate sets (root vs Ingest-Template/) after consolidating links and Templater.

No moves were performed; apply the structure you prefer and then update Templater and Ingest-Selector links as above.
