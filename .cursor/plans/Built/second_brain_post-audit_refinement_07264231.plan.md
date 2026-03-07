---
name: Second Brain Post-Audit Refinement
overview: "Close audit gaps to reach ≥93% alignment: eliminate Highlightr format drift, add always-ingest-bootstrap, centralize config, mandate project colors in action extraction, standardize links as array, start hub→project-MOC transition, add graph hints and dashboard fixes. Watcher remains Phase 4 (on hold)."
todos: []
isProject: false
---

# Second Brain Post-Audit Refinement Plan

**Reference:** [3-Resources/Second-Brain-Master-Goal-Audit-2026-02-25.md](3-Resources/Second-Brain-Master-Goal-Audit-2026-02-25.md) (85.5% alignment), [Untitled 1.md](Untitled 1.md) (direction notes).

**Guiding principles (from your notes):** Watcher is last; user-triggered autonomy is intentional; Highlightr consistency is highest-risk; project-MOC transition and central config are required; links = array; graph now, canvas later; MCP/skill clean-ups in Phase 1.

---

## Phase 1 – Critical consistency and blocking (target 90%+, by 2026-02-28)

### 1.1 Highlightr format – zero drift

**1.1.1 express-mini-outline**  

- **File:** [.cursor/skills/express-mini-outline/SKILL.md](.cursor/skills/express-mini-outline/SKILL.md)  
- **Change:** In "Format" (step 3), remove the deprecated example `==Section A==^{Blue}`. Replace with: use **inline CSS only** per [3-Resources/Highlightr-Color-Key.md](3-Resources/Highlightr-Color-Key.md) Section 2 (e.g. `<mark style="background: #A3D8FFA6;">Section A</mark>` for Blue). Add one sentence: "Never use `==text==` or `^{Color}` in outline output."

**1.1.2 Visual Health Dashboard – count both formats**  

- **File:** [3-Resources/_dv-visual-health-dashboard.js](3-Resources/_dv-visual-health-dashboard.js)  
- **Current:** Sections 2 and 4 count only legacy `^{Color}` via regex `\^\{${c.trim()}\}`.  
- **Change:**  
  - Define a mapping from color name to hex (e.g. Red → `#FFAAAAA6`, from [Highlightr-Color-Key.md](3-Resources/Highlightr-Color-Key.md)).  
  - For each note content, count **inline CSS**: match `<mark style="background: #XXXXXX">` and map hex back to color name where possible; aggregate by color.  
  - Keep legacy `^{Color}` counting for migration period; **combined** count = note uses that color if either format present.  
  - Update the "Notes using each color" and "Highlight patterns by folder" sections to use combined counts and optionally show "inline" vs "legacy" in the table or a footnote.

**1.1.3 Legacy notes – migrate or document**  

- **Option A (migration):** One-time script or manual pass on notes under `1-Projects/Test-Project/` and `Ingest/*.md` that contain `==...==^{Color}`: replace with equivalent `<mark style="background: #...">...</mark>` using the Color Key hex table.  
- **Option B (document only):** In [3-Resources/Highlightr-Color-Key.md](3-Resources/Highlightr-Color-Key.md), add a short "Legacy format" subsection: "`==text==^{Color}` is deprecated; pipeline outputs inline CSS only. Existing notes with legacy format may be migrated or left until next edit."  
- **Recommendation:** Do Option B in Phase 1; run Option A as a separate task if you want Test-Project and Ingest fully canonical.

### 1.2 always-ingest-bootstrap rule

- **Create:** [.cursor/rules/always/always-ingest-bootstrap.mdc](.cursor/rules/always/always-ingest-bootstrap.mdc)  
- **Content (8–10 lines):** When the user says "INGEST MODE", "Process Ingest", or "run ingests", ensure para-zettel-autopilot and mcp-obsidian-integration apply. List Ingest notes via `obsidian_list_notes`("Ingest") and run the full-autonomous-ingest pipeline per [Cursor-Skill-Pipelines-Reference](3-Resources/Cursor-Skill-Pipelines-Reference.md). No new tool sequence—defer to MCP rule and para-zettel-autopilot for exact steps.  
- **Update:** [3-Resources/Cursor-Skill-Pipelines-Reference.md](3-Resources/Cursor-Skill-Pipelines-Reference.md) trigger table (L24–26): keep row "Ingest", "process Ingest", "run ingests" | **always-ingest-bootstrap**, para-zettel-autopilot | full-autonomous-ingest. Add a footnote or sentence under the table: "always-ingest-bootstrap ensures ingest triggers apply the ingest pipeline; see `.cursor/rules/always/always-ingest-bootstrap.mdc`."

### 1.3 MCP descriptor clean-ups

- **Location:** MCP tool descriptors are under the Cursor project MCP cache: `~/.cursor/projects/home-darth-Documents-Second-Brain/mcps/user-obsidian-para-zettel-autopilot/tools/`.  
- **obsidian_ensure_structure:** Already includes `folder_path` in the schema; no change.  
- **obsidian_classify_para, obsidian_split_atomic, obsidian_append_to_hub:** Each has `"description": ""`.  
  - **If these JSON files are editable** (not overwritten by the server): add short descriptions, e.g.  
    - classify_para: "Classify note into PARA type (Project/Area/Resource/Archive) with confidence; uses path and optional para_type hint."  
    - split_atomic: "Split a multi-idea note into atomic child notes; split_on (default '## ') defines section boundary; returns child paths."  
    - append_to_hub: "Append a wikilink and summary to a hub/MOC note (hub_name, e.g. 'Resources Hub' or 'Resurface')."
  - **If the server regenerates descriptors:** add the same text to a vault doc (e.g. `3-Resources/MCP-Descriptor-Descriptions.md`) and apply in the MCP server repo when you have access.

### 1.4 next-action-extract – mandate project color overrides

- **File:** [.cursor/skills/next-action-extract/SKILL.md](.cursor/skills/next-action-extract/SKILL.md)  
- **Change:** In the bullet that currently says "Optional: Color-code action blocks by project", replace with: **When `project-id` (or project frontmatter) exists, use project-specific highlight color for action blocks** (from note's `highlight_key` or [Highlightr-Color-Key.md](3-Resources/Highlightr-Color-Key.md) project guidelines). Use inline CSS only. Make this a required step when project-id is set, not optional.  
- **Sync:** Update [.cursor/sync/skills/next-action-extract.md](.cursor/sync/skills/next-action-extract.md) to match if that file is maintained.

---

## Phase 2 – Config centralization and polish (target 92–93%, by 2026-03-05)

### 2.1 Single source of truth config

- **Create:** [3-Resources/Second-Brain-Config.md](3-Resources/Second-Brain-Config.md)  
- **Content:** Frontmatter + readable body. Include the YAML you specified, e.g.:

```yaml
---
title: Second Brain Config
para-type: Resource
status: active
---

# Second Brain Config

Single source of truth for pipeline and skill configuration. Skills/rules that need hub names or thresholds should read this note (e.g. via context or Templater/Dataview).

## hub_names
- projects: "Projects Hub"
- areas: "Areas Hub"
- resources: "Resources Hub"
- resurface: "Resurface"

## archive
- age_days: 90
- no_activity_days: 60

## highlight
- default_key: "3-Resources/Highlightr-Color-Key.md"

## graph
- moc_strength: 3
```

- **Usage:** In [archive-check/SKILL.md](.cursor/skills/archive-check/SKILL.md), add: "Age threshold: read from Second-Brain-Config.md (archive.age_days / no_activity_days) if available; else default 90 / 60." In [resurface-candidate-mark/SKILL.md](.cursor/skills/resurface-candidate-mark/SKILL.md) and any skill that calls `append_to_hub`, add: "Hub names: prefer Second-Brain-Config.md hub_names; fallback to 'Resurface', 'Projects Hub', etc." Document in the config note that pipelines pass it as context or read it when resolving hub names and archive thresholds.

### 2.2 Hub → project-MOC transition (start)

- **Keep:** Current hubs (Projects Hub, Areas Hub, Resources Hub, Resurface).  
- **Rule/skill change:** In the ingest pipeline, after **frontmatter-enrich** (or in **append_to_hub** flow): for any note with `project-id` set, ensure the note's `links` (or a dedicated field) includes a link to that project's MOC. Convention: MOC note title = project name or "ProjectName MOC" (e.g. `[[Test-Project MOC]]`). If the project MOC note does not exist, the pipeline can create a minimal note (e.g. under `1-Projects/Test-Project/Test-Project MOC.md`) with title and a Dataview block for notes where `project-id = "Test-Project"`, or document "create MOC manually once per project."  
- **Best place to implement:** Either (a) extend [.cursor/skills/frontmatter-enrich/SKILL.md](.cursor/skills/frontmatter-enrich/SKILL.md) to add `[[ProjectName MOC]]` (or `[[project-id MOC]]`) into `links` when `project-id` exists, or (b) add a short bullet in [.cursor/rules/context/para-zettel-autopilot.mdc](.cursor/rules/context/para-zettel-autopilot.mdc) and in the pipeline reference: "After append_to_hub, ensure notes with project-id link to that project's MOC; create MOC note if missing (or document creation in config)."  
- **Document:** In [Ingest/Master Goal.md](Ingest/Master Goal.md) (or a short "Organization" subsection), add one paragraph: notes are linked to PARA hubs and to **project MOCs** (one MOC per project, linked when `project-id` is set); project MOCs are linked into the main hubs for discovery.

### 2.3 Links format – array standard

- **Decision (from your plan):** `links` = array in frontmatter: `links: ["[[Resources Hub]]", "[[Related]]"]`.  
- **frontmatter-enrich:** [.cursor/skills/frontmatter-enrich/SKILL.md](.cursor/skills/frontmatter-enrich/SKILL.md) — Change "Required" and "Value format" to: output `links` as a **YAML array** (e.g. `["[[Resources Hub]]", "[[Project X]]"]`). If the MCP only accepts string, use JSON array string and document that Dataview parses it; otherwise prefer native array. Update the skill to say "always output array format; never comma-separated only."  
- **Dataview:** No current queries in the vault filter on `links`. Add a short note in [3-Resources/Second-Brain-Config.md](3-Resources/Second-Brain-Config.md) or [Cursor-Skill-Pipelines-Reference.md](3-Resources/Cursor-Skill-Pipelines-Reference.md): "For queries, use `contains(links, "[[HubName]]")` or array membership; `links` is always an array."

### 2.4 Distillation autonomy – optional auto-layer-select (Phase 2)

- **Add optional skill:** Create [.cursor/skills/auto-layer-select/SKILL.md](.cursor/skills/auto-layer-select/SKILL.md) (or document in pipeline reference only): uses content complexity (sentence length, heading density, jargon) to suggest 1 / 2 / 3 distillation layers; LLM confidence gates whether to auto-apply or propose. Manual override remains: "distill this note with 2 layers."  
- **Integration:** Reference in [auto-distill.mdc](.cursor/rules/context/auto-distill.mdc) and [Cursor-Skill-Pipelines-Reference.md](3-Resources/Cursor-Skill-Pipelines-Reference.md) as optional step before "distill layers" (when enabled). This can be a small addition so autonomy is configurable without changing the default pipeline.

---

## Phase 3 – Visual and graph clarity (target 93%+, by 2026-03-12)

### 3.1 Graph-view changes (now)

- **para-zettel-autopilot and auto-express:** In [.cursor/rules/context/para-zettel-autopilot.mdc](.cursor/rules/context/para-zettel-autopilot.mdc) and [.cursor/rules/context/auto-express.mdc](.cursor/rules/context/auto-express.mdc), add a short bullet: when enriching frontmatter or after express, **optionally set graph-related frontmatter** (e.g. `graph: { color: "#hex" }` or a vault-convention key) from project color so graph view can use it. Prefer reading project color from Highlightr-Color-Key or Second-Brain-Config.  
- **Project MOCs:** Add guidance: in each project MOC note, include a "Graph Focus" callout with a Dataview query that lists notes in that project (e.g. `WHERE project-id = "Test-Project"`) for quick graph context. Document in [Second-Brain-Config.md](3-Resources/Second-Brain-Config.md) or pipeline reference.

### 3.2 Visual Health Dashboard – graph health and alignment

- **File:** [3-Resources/_dv-visual-health-dashboard.js](3-Resources/_dv-visual-health-dashboard.js)  
- **After Phase 1:** Dashboard already counts both inline-CSS and legacy highlights. Add a **"Graph health score"** section: e.g. link density (outgoing links per note), share of notes with graph-related frontmatter (if you add it). Keep it simple (one paragraph or one metric).  
- **Re-test:** Run pipeline on 20+ notes (or use existing Test-Project + Resources notes), then confirm TL;DR %, highlight counts, and actionable summary match expectations and no false undercounts.

### 3.3 Tag + frontmatter hybrid

- **Config note:** In [3-Resources/Second-Brain-Config.md](3-Resources/Second-Brain-Config.md), add: "Tags are convenience only (e.g. #dev-task, #bug for QuickAdd and task filters); pipelines and core filtering use frontmatter. Do not rely on tags for ingest/distill/archive logic."  
- **No change** to PARA-Dashboard or existing Dataview that uses `contains(file.tags, "dev-task")`; keep those as-is.

---

## Phase 4 – "When notes land" watcher (on hold until ≥93% re-audit, target 2026-03-20)

- **Scope:** Lightweight watcher (Node script via QuickAdd or Obsidian plugin): on Ingest/ file create or modify, append a trigger line to Ingest-Log.md and optionally open Cursor with "INGEST MODE" URI or prompt.  
- **Start only after:** Phase 1–3 complete, re-audit ≥93%, and 10+ flawless end-to-end runs. No implementation details in this plan; treat as placeholder.

---

## Implementation order and success criteria


| Phase   | Complete by | Success criteria                                                                                                                                                                                                                 |
| ------- | ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Phase 1 | 2026-02-28  | Zero Highlightr format conflicts; always-ingest-bootstrap.mdc exists and is referenced; MCP descriptors filled (or documented); next-action-extract mandates project colors when project-id set.                                 |
| Phase 2 | 2026-03-05  | Second-Brain-Config.md in place; hub names and archive thresholds read from config; project-MOC link added for notes with project-id; links standardized as array; optional auto-layer-select documented/skill added.            |
| Phase 3 | 2026-03-12  | Graph frontmatter/callout guidance in rules and project MOCs; Visual Health Dashboard includes graph health and correct highlight counts; config states tag vs frontmatter; 30-note pipeline run with 0 spurious #review-needed. |
| Phase 4 | 2026-03-20+ | Watcher implemented only after re-audit ≥93%.                                                                                                                                                                                    |


---

## Immediate next actions (today)

1. Execute Phase 1.1 (Highlightr): edit express-mini-outline SKILL, then _dv-visual-health-dashboard.js (inline CSS + legacy), then Highlightr-Color-Key legacy subsection.
2. Create always-ingest-bootstrap.mdc and update Cursor-Skill-Pipelines-Reference trigger table.
3. Create 3-Resources/Second-Brain-Config.md with hub_names, archive, highlight, graph.
4. Update next-action-extract to mandate project color overrides; update frontmatter-enrich for links array.
5. MCP descriptors: add descriptions for classify_para, split_atomic, append_to_hub (in project mcps if writable, else in 3-Resources/MCP-Descriptor-Descriptions.md).

---

## File summary

**Create:** `.cursor/rules/always/always-ingest-bootstrap.mdc`, `3-Resources/Second-Brain-Config.md`; optionally `.cursor/skills/auto-layer-select/SKILL.md`, `3-Resources/MCP-Descriptor-Descriptions.md`.

**Edit:** `.cursor/skills/express-mini-outline/SKILL.md`, `3-Resources/_dv-visual-health-dashboard.js`, `3-Resources/Highlightr-Color-Key.md`, `3-Resources/Cursor-Skill-Pipelines-Reference.md`, `.cursor/skills/next-action-extract/SKILL.md`, `.cursor/skills/frontmatter-enrich/SKILL.md`, `.cursor/skills/archive-check/SKILL.md`, `.cursor/skills/resurface-candidate-mark/SKILL.md`, `.cursor/rules/context/para-zettel-autopilot.mdc`, `.cursor/rules/context/auto-express.mdc`, `Ingest/Master Goal.md`; MCP tool JSONs if editable.

**Sync:** `.cursor/sync/skills/next-action-extract.md`, `.cursor/sync/skills/frontmatter-enrich.md` if kept in sync with skills.