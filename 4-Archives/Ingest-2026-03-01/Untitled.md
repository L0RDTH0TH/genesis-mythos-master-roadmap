---

---
| Pipeline Name                | Purpose / Autonomy Level                                                           | Maps to CODE Step  | Mandatory First Step     | Core Steps (Sequence)                                                                                                                                 | Confidence Gate    | Destructive? / Safety                 | Typical Triggers                                | Parameters (Examples)                                                               |
| ---------------------------- | ---------------------------------------------------------------------------------- | ------------------ | ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ | ------------------------------------- | ----------------------------------------------- | ----------------------------------------------------------------------------------- |
| **full-autonomous-ingest**   | Post-capture processing: auto-organize, distill, hub-link, move if high-confidence | Organize + Distill | `obsidian_create_backup` | classify_para → split_atomic? → distill_note → manage_frontmatter + manage_tags → append_to_hub → move_note (if ≥85%) → log_action                    | ≥85% for move/auto | Move if high-conf; propose/log if low | Auto on new Ingest/ files; "process ingests"    | {batch: true, target_folder: 'Ingest/', execute_moves: true}                        |
| **autonomous-distill**       | Auto-refine/summarize notes without relocation                                     | Distill            | `obsidian_create_backup` | distill_note (progressive: bold → ==highlight== → TL;DR) → manage_tags? → log_action                                                                  | ≥85% for auto-edit | In-place edits                        | Periodic on Resources/; "distill vault"         | {batch: true, layers: 3, target_tags: ['needs-distill']}                            |
| **autonomous-archive**       | Scan for inactive/complete → auto-move to Archives                                 | Organize           | `obsidian_create_backup` | classify_para → check_inactivity (e.g., no open tasks, status=complete) → move_note (to Archives/) → update_frontmatter (archived: date) → log_action | ≥85% for move      | Auto-move if high                     | Cron-like periodic; "archive sweep"             | {batch: true, inactivity_threshold: '30d'}                                          |
| **autonomous-express**       | Generate output suggestions or drafts from distilled notes                         | Express            | — (read-only first)      | read_note → generate_express_ideas (1–3 outputs: e.g., blog outline, checklist) → append_to_note? (if ≥85%) → log_action                              | ≥85% for append    | Append if high; suggest if low        | "express ideas from note"; post-distill chain   | {output_types: ['blog', 'talk'], target_note: 'Express-Hub.md'}                     |
| **highlightr-apply** (Skill) | Search files, apply color-coded highlights per key                                 | Distill (enhance)  | `obsidian_create_backup` | semantic_search_notes (per color-key) → apply_highlights (Markdown syntax per Highlightr colors) → log_action                                         | ≥85% for apply     | In-place highlights                   | "highlight with key: {json}", manual skill call | {color_key: {"key-terms": "red", "quotes": "blue"}, target_files: 'Resources/*.md'} |






Yes, integrating highlighting (via Highlightr or similar color-coded mechanisms) as part of the **distill phase** is the right call for autonomy and coherence.

To push post-capture autonomy further, here are ~5 potential **skill pipelines** (modular, reusable sub-sequences or "skills") suggested for each main pipeline. These are designed to be:

- Callable as optional/conditional steps within the parent pipeline
- Autonomous (high-confidence auto-apply; low → log/propose/flag #review-needed)
- Safety-first (leverage the parent pipeline's backup + logging)
- Aligned with BASB layers (especially for distill-focused ones)
- Focused on small, high-value enhancements that reduce manual work

I've grouped them per pipeline, with brief rationale + where it would slot in.

### 1. full-autonomous-ingest
(This is the flagship end-to-end flow after capture.)

Potential skill pipelines to embed/enhance autonomy:

1. **semantic-tag-suggest**  
   After classify_para: Use semantic analysis (or keyword + context) to suggest 3–8 tags; auto-apply if ≥85% match to existing vault patterns; else propose in log.  
   *Rationale*: Accelerates Organize step; tags feed future searches/hubs.

2. **atomic-split-refine**  
   After split_atomic: For each child note → quick re-classify + frontmatter inheritance from parent + minimal distill (first bold layer).  
   *Rationale*: Ensures children are immediately usable, not just split.

3. **distill-highlight-color** (the Highlightr integration skill)  
   After distill_note (text layers): Apply color-coded highlights based on note frontmatter `highlight_key`, vault default, or semantic detection (e.g., red = key concepts, blue = quotes/sources, green = actions).  
   *Rationale*: Natural Layer 2 extension; makes progressive summarization visual & scannable.

4. **next-action-extract**  
   After distill: Scan for task-like phrases ("should", "next", TODO, deadlines) → convert to Obsidian tasks/checklist + add to frontmatter `next-actions` array.  
   *Rationale*: Bridges to actionability (PARA Projects/Areas priority).

5. **express-mini-outline**  
   At end (before/after move): Generate 1-paragraph executive summary or bullet outline of key takeaways → append as fenced block "## Express Quick View".  
   *Rationale*: Early Express step; makes note immediately shareable/useful.

### 2. autonomous-distill
(Focused refinement pass, often periodic or targeted.)

Potential skill pipelines:

1. **distill-highlight-color** (same as above)  
   Core Layer 2 skill: Apply color highlights on top of bold layer; use progressive rules (e.g., only highlight inside already-bolded sections).

2. **layer-promote**  
   If note already has Layer 1 (bold), promote select bold → ==highlight== (Layer 2); or highlight → TL;DR bullets (Layer 3).  
   *Rationale*: True progressive summarization automation; iterate over time.

3. **key-term-glossary-link**  
   After highlight: Identify repeated colored terms → auto-create/check [[wiki-style links]] to a central Glossary or Resources note.  
   *Rationale*: Builds Zettelkasten connectivity without manual effort.

4. **contradiction-flag**  
   Scan distilled content for potential conflicts (e.g., "but", "however", date mismatches) → add #potential-contradiction tag + log excerpt.  
   *Rationale*: Quality gate for knowledge integrity.

5. **readability-score-append**  
   Compute simple readability metrics (Flesch-Kincaid via code if available, or heuristic sentence length) → append as metadata or comment.  
   *Rationale*: Helps identify notes needing further distillation.

### 3. autonomous-archive
(Declutter inactive items autonomously.)

Potential skill pipelines:

1. **archive-metadata-clean**  
   Before move: Strip active-only fields (e.g., remove open tasks, priority, deadline); add `archived-from`, `last-active`.  
   *Rationale*: Keeps Archives clean and traceable.

2. **resurface-candidate-mark**  
   Before/after move: If note has high resurfacing potential (e.g., many links, unique tags, recent highlights), add `resurface-candidate: true` or append to Resurface hub.  
   *Rationale*: Implements BASB Principle 7 without manual review.

3. **duplicate-check-before-archive**  
   Quick semantic similarity scan against existing Archives → flag potential duplicates instead of archiving.  
   *Rationale*: Prevents vault bloat.

4. **summary-preserve**  
   If note has no TL;DR yet → force a minimal distill (Layer 3 bullets) before archiving.  
   *Rationale*: Archived notes remain glanceable.

5. **link-forward**  
   Before move: Add redirect-style frontmatter or alias so old links still resolve (e.g., `aliases: [old-path]`).  
   *Rationale*: Maintains graph integrity.

### 4. autonomous-express
(Push notes toward output/creation.)

Potential skill pipelines:

1. **output-format-generate**  
   Based on note type/content: Generate structured output (e.g., blog post markdown template, Twitter thread bullets, slide outline). Append to Express-Hub or new child note.  
   *Rationale*: Core Express automation.

2. **audience-adapt**  
   Rewrite key takeaways at different levels (beginner/intermediate/expert) → append variants.  
   *Rationale*: Increases reusability ("Idea Recycling").

3. **call-to-action-append**  
   Add boilerplate CTA (e.g., "Share this on X?", "Add to newsletter?") with pre-filled prompts.  
   *Rationale*: Reduces friction to actual expression.

4. **related-content-pull**  
   Pull 2–3 semantically similar notes/links → append "Related" section with summaries.  
   *Rationale*: Sparks new connections for expression.

5. **version-snapshot**  
   Before major express append: Create dated snapshot of current distilled version for versioning.  
   *Rationale*: Protects against over-editing.

### 5. highlightr-apply (now distill sub-skill, but standalone-callable)

If you ever want to run it independently (e.g., bulk retroactive highlighting):

Potential skill pipelines to chain after it:

1. **highlight-consolidate**  
   Merge overlapping/adjacent highlights of same color; clean up.

2. **color-to-tag-map**  
   Convert frequent colors to tags (e.g., many red highlights → add #key-concept).

3. **highlight-export**  
   Extract all highlighted passages (per color) → append to dedicated "Highlights Export" note or CSV.

4. **progression-check**  
   Verify Layer 2 highlights are inside Layer 1 bold; flag inconsistencies.

5. **theme-sync**  
   If vault theme changes, re-apply/re-parse Highlightr syntax for compatibility.

These ~25 suggestions give a strong set of building blocks. Start by picking 2–4 per pipeline (especially distill-highlight-color as the priority Highlightr integration), document them in your pipelines-reference note as "optional skills", and define simple invocation rules (e.g., "if note has #enable-X-skill or confidence high").

Which pipeline would you like to flesh out first with detailed sequences for its top 3–4 skills?






To address the tag-heavy nature of your current PARA-Zettelkasten setup (e.g., relying on #review-needed, #raw-ingest, #needs-distill, or #highlight-needed to trigger actions), we can shift toward more structured, visual, and dynamic methods in Obsidian. Tags are great for quick categorization but can clutter notes and lead to inconsistent querying. Instead, leverage Obsidian's built-in features and plugins to convey data more elegantly—making it scannable, interactive, and actionable—while automating improvements via pipelines, scripts, and integrations.

I'll outline key alternative methods below, focusing on how they improve data conveyance (e.g., better readability, relationships, and insights) and how to automate them in your autonomous post-capture workflows (e.g., integrating into full-autonomous-ingest or autonomous-distill pipelines). These build on your MCP tools (like `obsidian_manage_frontmatter` or `obsidian_append_to_note`) and reduce manual tagging by using frontmatter, queries, and programmatic logic.

### 1. **Frontmatter for Structured Metadata (Instead of Tags for Status/Triggers)**
   - **Improvement in Data Conveyance**: Frontmatter (YAML at the top of notes) stores key-value data cleanly, making notes self-describing without inline tags. For example, use keys like `status: raw`, `confidence: 85`, `needs-distill: true`, or `resurface-date: 2026-03-01` to convey state. This allows for collapsible, non-intrusive metadata that's queryable and exportable.
   - **Automation Enhancements**:
     - Integrate into pipelines: In `full-autonomous-ingest` or `autonomous-distill`, use `obsidian_manage_frontmatter` to auto-set/update keys based on analysis (e.g., after classify_para, set `para-type: Project` and `status: active` if ≥85% confidence).
     - Templater Plugin: Auto-apply templates on note creation/ingest with scripts like `<% tp.date.now("YYYY-MM-DD") %>` for `created`, or conditional logic for `needs-distill: <% if (tp.file.content.includes("TODO")) { "true" } else { "false" } %>`.
     - MCP Chaining: Extend `obsidian_log_action` to append frontmatter changes to Ingest-Log.md, creating an audit trail without tags.
     - Quick Script: Use Obsidian's console (via dev tools) or a community plugin like QuickAdd to run JavaScript that scans frontmatter and updates batches (e.g., "if status=raw and age>7d, set needs-distill=true").

### 2. **Dataview Plugin for Dynamic Queries and Views**
   - **Improvement in Data Conveyance**: Instead of tag-based searches, create live, table/list-based views that aggregate and display data across notes. For example, a hub note could show a TABLE of all `para-type: Resource` notes with columns for `title`, `status`, `confidence`, and linked excerpts—making complex data interactive and filterable without cluttering individual notes.
   - **Automation Enhancements**:
     - Pipeline Integration: In `autonomous-distill` or `full-autonomous-ingest`, after `append_to_hub`, auto-insert Dataview blocks via `obsidian_append_to_note` (e.g., `TABLE title, status, confidence FROM "3-Resources" WHERE status = "needs-review" SORT confidence DESC`).
     - Periodic Sweeps: Use Obsidian's "DataviewJS" or pair with Templater to auto-refresh hubs on vault load/reload—e.g., a script that rebuilds a "Review Dashboard" note with queries for low-confidence items.
     - MCP Extension: Chain `obsidian_global_search` with Dataview syntax to generate and insert views programmatically (e.g., query for "notes with confidence <85" and append a sorted list to a log hub).
     - Community Automation: Plugins like "Periodic Notes" or "Calendar" can trigger daily/weekly Dataview updates, auto-flagging resurfacing candidates without manual tags.

### 3. **Callouts and Admonitions for Visual Emphasis**
   - **Improvement in Data Conveyance**: Use Obsidian's built-in callouts (e.g., > [!note] Title \n Content) to box important sections like TL;DR summaries, next actions, or warnings—conveying hierarchy and focus without tags. Customize with colors/icons (via CSS snippets) for at-a-glance meaning (e.g., green for actions, red for reviews).
   - **Automation Enhancements**:
     - Pipeline Embed: In `autonomous-distill`, after generating TL;DR, use `obsidian_append_to_note` to insert callouts like `> [!summary] TL;DR\n- Bullet 1\n- Bullet 2`.
     - Templater Scripts: Auto-generate callouts in templates, e.g., `> [!action] Next Steps\n<% tp.system.prompt("Enter actions") %>` (or AI-populate via Cursor/MCP).
     - Batch Processing: Extend MCP with a custom `obsidian_insert_callout` tool that scans notes for patterns (e.g., "if low confidence, insert > [!warning] Review Needed") during ingest sweeps.
     - Highlightr Synergy: Combine with your distill-highlight-color skill to auto-wrap highlighted text in themed callouts (e.g., red highlights → > [!important] block).

### 4. **Canvas and Graph Views for Relational Mapping**
   - **Improvement in Data Conveyance**: Move beyond linear tags to visual graphs/canvases that show note relationships (e.g., a canvas linking Projects to Resources with arrows for dependencies). This conveys context and flows intuitively, reducing the need for tag-based navigation.
   - **Automation Enhancements**:
     - Pipeline Hook: In `full-autonomous-ingest`, after `append_to_hub`, use `obsidian_create_canvas` or append links to an existing canvas file (e.g., auto-add nodes for new notes via JSON canvas format).
     - Graph Automation: Plugins like "Graph Analysis" or "Excalidraw" can auto-generate sub-graphs; script via MCP to update a "PARA Overview" canvas with new edges based on frontmatter `links`.
     - Resurfacing Integration: In `autonomous-archive`, before archiving, auto-add archived notes to a "History Canvas" for visual timeline conveyance.
     - JS Automation: Use Obsidian's API (via plugins like "Advanced Scripts") to periodically rebuild graphs/canvases from queries, e.g., "connect all notes with para-type: Project to their Areas."

### 5. **Tasks and Checklists for Actionable Data**
   - **Improvement in Data Conveyance**: Convert implied actions (e.g., from tags like #todo) into native Obsidian tasks ([ ] Item), which are queryable and integrable with plugins like Tasks. This makes data more interactive—e.g., a dashboard showing overdue items across notes.
   - **Automation Enhancements**:
     - Skill Integration: Embed your next-action-extract skill in `full-autonomous-ingest` to scan and convert phrases to tasks automatically (e.g., "Next: do X" → - [ ] Do X).
     - Tasks Plugin: Auto-query and embed task lists in hubs (e.g., `Tasks: not done due before today`); use Templater to insert checklists in new notes based on para-type.
     - MCP Chaining: After `distill_note`, use `obsidian_search_replace` to format actions as tasks, then log completions.
     - Periodic Automation: Plugins like "Tasks Calendar" auto-sync tasks to daily notes; script sweeps to escalate unchecked items (e.g., add to frontmatter `priority: high`).

### Implementation Tips for Your Pipelines
- **Reducing Tag Reliance Overall**: In your rules/pipelines, prioritize frontmatter over tags (e.g., query via Dataview `WHERE status = "raw"` instead of #raw-ingest). Start by auditing existing notes with MCP's `obsidian_global_search` to migrate tags to frontmatter.
- **Testing Autonomy**: Prototype in a test vault—e.g., drop raw notes into Ingest/, trigger `full-autonomous-ingest`, and verify automated insertions (callouts, Dataview blocks) without manual steps.
- **Plugin Stack**: Ensure Dataview, Templater, and Tasks are installed; for advanced automation, add "Obsidian Scripts" or "QuickAdd" to run JS/MCP on events like note save.
- **Scalability**: These methods are less brittle than tags for large vaults, as they're structured and queryable. If needed, extend MCP with custom tools for bulk operations.

This approach keeps your Second Brain more visual and automated, aligning with BASB's emphasis on resurfacing and expression without overwhelming tag sprawl. If you share a specific pipeline or note example, I can refine these further!




# Recommended Plugin Changes for Pipeline Alignment

Based on the Obsidian Plugin Automation Report (`Ingest/2026-02-24-obsidian-plugin-automation-report.md`), your current setup is already reasonably aligned with the autonomous pipeline framework (e.g., full-autonomous-ingest, autonomous-distill, autonomous-archive, autonomous-express). The pipelines are primarily driven by Cursor/MCP tools (e.g., `obsidian_create_backup`, `obsidian_classify_para`), with Obsidian plugins providing supporting infrastructure like templates, dynamic queries, and visual enhancements.

The key alignment goals:
- **Post-capture autonomy**: Plugins handle initial structuring (e.g., frontmatter on creation) and visualization (e.g., Dataview hubs), but core pipeline execution remains in Cursor/MCP via triggers like "INGEST MODE".
- **Reduce tag reliance**: Shift to frontmatter (`para-type`, `status`, `confidence`, `resurface-date`), Dataview queries, tasks/checklists, callouts, and canvases.
- **Support distill/highlight**: Enable Highlightr for color-coded layers in autonomous-distill.
- **Periodic/conditional automation**: Use QuickAdd/Templater for in-Obsidian triggers that prepare for MCP sweeps (e.g., log entries for archive/distill batches).
- **Safety**: All changes respect Option C (backup-first via MCP); no direct destructive actions in plugins.

Below, I summarize **required/minimal changes** (must-do for alignment) and **optional enhancements** (nice-to-have for better autonomy). Changes are to `.obsidian/plugins/[plugin-id]/data.json` (edit with Obsidian closed or backup the folder first). For UI-driven plugins (e.g., QuickAdd macros), use the plugin settings to configure, then verify the JSON updates.

## Per-Plugin Changes

### 1. Templater
   - **Current Alignment**: Good for new-note creation in Ingest/ and PARA folders (triggers templates with frontmatter). Supports reducing tags by auto-setting `para-type`, `status: raw`.
   - **Required Changes**:
     - None critical—`trigger_on_file_creation: true` and folder templates are already set.
   - **Optional Enhancements**:
     - Add a user scripts folder for periodic sweeps (e.g., a script to list notes for autonomous-archive).
       - Edit `data.json`: Add `"user_scripts_folder": "Templates/Scripts"`.
       - Create `Templates/Scripts/archive-sweep.js`: Use Obsidian API to query notes (e.g., by frontmatter `status: complete`), output a list to `Archive-Sweep-YYYY-MM-DD.md` for Cursor/MCP to process.
     - Add a startup template for session prep (e.g., check Ingest/ and append to log if new files exist, prompting MCP trigger).
       - Edit `data.json`: `"startup_templates": ["Templates/Session-Prep.md"]`.
       - Create `Templates/Session-Prep.md`: `## Session Start: <% tp.date.now("YYYY-MM-DD HH:mm") %>\nCheck Ingest/ for new files. If any, run INGEST MODE in Cursor.`
     - **Pipeline Impact**: Enhances full-autonomous-ingest (auto-frontmatter on create) and autonomous-archive (scripted candidate lists).

### 2. QuickAdd
   - **Current Alignment**: Empty—no macros yet, but can chain with Templater for triggers.
   - **Required Changes**:
     - Add a "Process Ingest" macro to bridge Obsidian to Cursor/MCP (e.g., insert INGEST MODE prompt or log entry).
       - In QuickAdd settings: Create a Macro choice named "Process Ingest".
         - Step 1: Open or create `Ingest-Log.md`.
         - Step 2: Run Templater template to append `Trigger: INGEST MODE – safe batch autopilot | Date: <% tp.date.now("YYYY-MM-DD HH:mm") %>`.
       - Verify `data.json` updates with the new choice (e.g., `"choices": [{"type": "Macro", "name": "Process Ingest", ...}]`).
   - **Optional Enhancements**:
     - Add "Capture to Ingest" capture: Sets frontmatter (`para-type: Ingest`, `status: raw`, no tags) and saves to `Ingest/`.
       - In settings: Create Capture choice with template and folder.
     - Add "Distill Batch" macro: Uses Dataview to list notes with frontmatter `needs-distill: true`, appends to log for Cursor.
     - **Pipeline Impact**: Triggers full-autonomous-ingest or autonomous-distill from Obsidian UI/shortcuts, reducing manual Cursor prompts.

### 3. Dataview
   - **Current Alignment**: Solid for dynamic hubs (queries by frontmatter like `para-type`, `status`). Reduces tags via structured queries.
   - **Required Changes**:
     - Enable DataviewJS for advanced automation in hubs (e.g., resurfacing candidates based on `resurface-date`).
       - Edit `data.json`: `"enableDataviewJs": true, "enableInlineDataviewJs": true`.
   - **Optional Enhancements**:
     - Update hub templates (via Templater/MCP) to use frontmatter queries, e.g., `TABLE title, status, confidence FROM "1-Projects" WHERE status = "active" AND confidence >= 85 SORT resurface-date ASC`.
     - **Pipeline Impact**: In autonomous-distill or full-autonomous-ingest, MCP's `append_to_hub` can insert these blocks; Dataview evaluates them live for better data conveyance.

### 4. Tasks
   - **Current Alignment**: Good for actionable data (tasks from next-action-extract skill); compatible with Dataview.
   - **Required Changes**:
     - Enable created date tracking to align with frontmatter `created`.
       - Edit `data.json`: `"setCreatedDate": true`.
   - **Optional Enhancements**:
     - Set task format to Dataview for query integration: `"taskFormat": "dataview"`.
     - In hubs, add Tasks queries (e.g., `TASKS FROM "1-Projects" WHERE !completed AND due < date(today)`).
     - **Pipeline Impact**: Supports autonomous-archive (check for "no open tasks") and full-autonomous-ingest (convert phrases to tasks via MCP).

### 5. Local REST API
   - **Current Alignment**: Enables external calls (e.g., for non-Cursor automation like cron sweeps), but pipelines use MCP primarily.
   - **Required Changes**:
     - None—ports and API key are set. Ensure API key is in environment variables (not committed to `data.json`).
   - **Optional Enhancements**:
     - Use for external triggers (e.g., a cron script calls API to append "Run archive sweep" to log, then trigger Cursor).
     - **Pipeline Impact**: Backup for autonomous-archive sweeps if Cursor isn't running; e.g., API call to list notes by frontmatter, then process in MCP.

### 6. Highlightr
   - **Current Alignment**: No config needed; supports color-coded distill.
   - **Required Changes**:
     - None—plugin is enabled.
   - **Optional Enhancements**:
     - Document a vault-wide color key in `3-Resources/Highlightr-Color-Key.md` (e.g., red: key concepts, blue: quotes, green: actions).
     - In autonomous-distill, MCP applies via `apply_highlights` (using Markdown `==text==^{color}` if Highlightr syntax matches).
     - **Pipeline Impact**: Integrates into distill-highlight-color skill for visual emphasis without tags.

### 7. Advanced Exclude
   - **Current Alignment**: Filters noise from searches/graphs.
   - **Required Changes**:
     - None.
   - **Optional Enhancements**:
     - Add exclusions for backups/logs (e.g., `*.backup.md`, `Ingest-Log.md` if not needed in graphs).
       - Configure in UI; updates `data.json` with patterns.
     - **Pipeline Impact**: Ensures MCP searches (e.g., in autonomous-archive) ignore irrelevant files.

### 8. BRAT
   - **Current Alignment**: For plugin installs/updates; no direct pipeline role.
   - **Required Changes**:
     - None.
   - **Optional Enhancements**:
     - None needed.
     - **Pipeline Impact**: Indirect—keeps plugins up-to-date for stability.

## Implementation Steps
1. **Backup Vault**: Run `obsidian_create_backup` on `.obsidian/` before edits.
2. **Apply Changes**: Edit `data.json` files manually (JSON format) or via plugin UI.
3. **Test per Report's Plan**: Use the 6-step test plan in the report (e.g., create Ingest note → trigger macro → verify pipeline run).
4. **Monitor**: After changes, check for startup slowdowns or conflicts; log issues in Ingest-Log.md.
5. **Next Priority**: Start with QuickAdd (for triggers) and DataviewJS (for advanced queries), as they directly enhance autonomy.

These changes will make your plugins more supportive of the pipelines without overcomplicating the setup. If you need exact JSON snippets for a specific plugin or help with script/template creation, provide more details!





Yes, integrating highlighting (via Highlightr or similar color-coded mechanisms) as part of the **distill phase** is the right call for autonomy and coherence.

To push post-capture autonomy further, here are ~5 potential **skill pipelines** (modular, reusable sub-sequences or "skills") suggested for each main pipeline. These are designed to be:

- Callable as optional/conditional steps within the parent pipeline
- Autonomous (high-confidence auto-apply; low → log/propose/flag #review-needed)
- Safety-first (leverage the parent pipeline's backup + logging)
- Aligned with BASB layers (especially for distill-focused ones)
- Focused on small, high-value enhancements that reduce manual work

I've grouped them per pipeline, with brief rationale + where it would slot in.

### 1. full-autonomous-ingest
(This is the flagship end-to-end flow after capture.)

Potential skill pipelines to embed/enhance autonomy:

1. **semantic-tag-suggest**  
   After classify_para: Use semantic analysis (or keyword + context) to suggest 3–8 tags; auto-apply if ≥85% match to existing vault patterns; else propose in log.  
   *Rationale*: Accelerates Organize step; tags feed future searches/hubs.

2. **atomic-split-refine**  
   After split_atomic: For each child note → quick re-classify + frontmatter inheritance from parent + minimal distill (first bold layer).  
   *Rationale*: Ensures children are immediately usable, not just split.

3. **distill-highlight-color** (the Highlightr integration skill)  
   After distill_note (text layers): Apply color-coded highlights based on note frontmatter `highlight_key`, vault default, or semantic detection (e.g., red = key concepts, blue = quotes/sources, green = actions).  
   *Rationale*: Natural Layer 2 extension; makes progressive summarization visual & scannable.

4. **next-action-extract**  
   After distill: Scan for task-like phrases ("should", "next", TODO, deadlines) → convert to Obsidian tasks/checklist + add to frontmatter `next-actions` array.  
   *Rationale*: Bridges to actionability (PARA Projects/Areas priority).

5. **express-mini-outline**  
   At end (before/after move): Generate 1-paragraph executive summary or bullet outline of key takeaways → append as fenced block "## Express Quick View".  
   *Rationale*: Early Express step; makes note immediately shareable/useful.

### 2. autonomous-distill
(Focused refinement pass, often periodic or targeted.)

Potential skill pipelines:

1. **distill-highlight-color** (same as above)  
   Core Layer 2 skill: Apply color highlights on top of bold layer; use progressive rules (e.g., only highlight inside already-bolded sections).

2. **layer-promote**  
   If note already has Layer 1 (bold), promote select bold → ==highlight== (Layer 2); or highlight → TL;DR bullets (Layer 3).  
   *Rationale*: True progressive summarization automation; iterate over time.

3. **key-term-glossary-link**  
   After highlight: Identify repeated colored terms → auto-create/check [[wiki-style links]] to a central Glossary or Resources note.  
   *Rationale*: Builds Zettelkasten connectivity without manual effort.

4. **contradiction-flag**  
   Scan distilled content for potential conflicts (e.g., "but", "however", date mismatches) → add #potential-contradiction tag + log excerpt.  
   *Rationale*: Quality gate for knowledge integrity.

5. **readability-score-append**  
   Compute simple readability metrics (Flesch-Kincaid via code if available, or heuristic sentence length) → append as metadata or comment.  
   *Rationale*: Helps identify notes needing further distillation.

### 3. autonomous-archive
(Declutter inactive items autonomously.)

Potential skill pipelines:

1. **archive-metadata-clean**  
   Before move: Strip active-only fields (e.g., remove open tasks, priority, deadline); add `archived-from`, `last-active`.  
   *Rationale*: Keeps Archives clean and traceable.

2. **resurface-candidate-mark**  
   Before/after move: If note has high resurfacing potential (e.g., many links, unique tags, recent highlights), add `resurface-candidate: true` or append to Resurface hub.  
   *Rationale*: Implements BASB Principle 7 without manual review.

3. **duplicate-check-before-archive**  
   Quick semantic similarity scan against existing Archives → flag potential duplicates instead of archiving.  
   *Rationale*: Prevents vault bloat.

4. **summary-preserve**  
   If note has no TL;DR yet → force a minimal distill (Layer 3 bullets) before archiving.  
   *Rationale*: Archived notes remain glanceable.

5. **link-forward**  
   Before move: Add redirect-style frontmatter or alias so old links still resolve (e.g., `aliases: [old-path]`).  
   *Rationale*: Maintains graph integrity.

### 4. autonomous-express
(Push notes toward output/creation.)

Potential skill pipelines:

1. **output-format-generate**  
   Based on note type/content: Generate structured output (e.g., blog post markdown template, Twitter thread bullets, slide outline). Append to Express-Hub or new child note.  
   *Rationale*: Core Express automation.

2. **audience-adapt**  
   Rewrite key takeaways at different levels (beginner/intermediate/expert) → append variants.  
   *Rationale*: Increases reusability ("Idea Recycling").

3. **call-to-action-append**  
   Add boilerplate CTA (e.g., "Share this on X?", "Add to newsletter?") with pre-filled prompts.  
   *Rationale*: Reduces friction to actual expression.

4. **related-content-pull**  
   Pull 2–3 semantically similar notes/links → append "Related" section with summaries.  
   *Rationale*: Sparks new connections for expression.

5. **version-snapshot**  
   Before major express append: Create dated snapshot of current distilled version for versioning.  
   *Rationale*: Protects against over-editing.

### 5. highlightr-apply (now distill sub-skill, but standalone-callable)

If you ever want to run it independently (e.g., bulk retroactive highlighting):

Potential skill pipelines to chain after it:

1. **highlight-consolidate**  
   Merge overlapping/adjacent highlights of same color; clean up.

2. **color-to-tag-map**  
   Convert frequent colors to tags (e.g., many red highlights → add #key-concept).

3. **highlight-export**  
   Extract all highlighted passages (per color) → append to dedicated "Highlights Export" note or CSV.

4. **progression-check**  
   Verify Layer 2 highlights are inside Layer 1 bold; flag inconsistencies.

5. **theme-sync**  
   If vault theme changes, re-apply/re-parse Highlightr syntax for compatibility.

These ~25 suggestions give a strong set of building blocks. Start by picking 2–4 per pipeline (especially distill-highlight-color as the priority Highlightr integration), document them in your pipelines-reference note as "optional skills", and define simple invocation rules (e.g., "if note has #enable-X-skill or confidence high").

Which pipeline would you like to flesh out first with detailed sequences for its top 3–4 skills?




To address the tag-heavy nature of your current PARA-Zettelkasten setup (e.g., relying on #review-needed, #raw-ingest, #needs-distill, or #highlight-needed to trigger actions), we can shift toward more structured, visual, and dynamic methods in Obsidian. Tags are great for quick categorization but can clutter notes and lead to inconsistent querying. Instead, leverage Obsidian's built-in features and plugins to convey data more elegantly—making it scannable, interactive, and actionable—while automating improvements via pipelines, scripts, and integrations.

I'll outline key alternative methods below, focusing on how they improve data conveyance (e.g., better readability, relationships, and insights) and how to automate them in your autonomous post-capture workflows (e.g., integrating into full-autonomous-ingest or autonomous-distill pipelines). These build on your MCP tools (like `obsidian_manage_frontmatter` or `obsidian_append_to_note`) and reduce manual tagging by using frontmatter, queries, and programmatic logic.

### 1. **Frontmatter for Structured Metadata (Instead of Tags for Status/Triggers)**
   - **Improvement in Data Conveyance**: Frontmatter (YAML at the top of notes) stores key-value data cleanly, making notes self-describing without inline tags. For example, use keys like `status: raw`, `confidence: 85`, `needs-distill: true`, or `resurface-date: 2026-03-01` to convey state. This allows for collapsible, non-intrusive metadata that's queryable and exportable.
   - **Automation Enhancements**:
     - Integrate into pipelines: In `full-autonomous-ingest` or `autonomous-distill`, use `obsidian_manage_frontmatter` to auto-set/update keys based on analysis (e.g., after classify_para, set `para-type: Project` and `status: active` if ≥85% confidence).
     - Templater Plugin: Auto-apply templates on note creation/ingest with scripts like `<% tp.date.now("YYYY-MM-DD") %>` for `created`, or conditional logic for `needs-distill: <% if (tp.file.content.includes("TODO")) { "true" } else { "false" } %>`.
     - MCP Chaining: Extend `obsidian_log_action` to append frontmatter changes to Ingest-Log.md, creating an audit trail without tags.
     - Quick Script: Use Obsidian's console (via dev tools) or a community plugin like QuickAdd to run JavaScript that scans frontmatter and updates batches (e.g., "if status=raw and age>7d, set needs-distill=true").

### 2. **Dataview Plugin for Dynamic Queries and Views**
   - **Improvement in Data Conveyance**: Instead of tag-based searches, create live, table/list-based views that aggregate and display data across notes. For example, a hub note could show a TABLE of all `para-type: Resource` notes with columns for `title`, `status`, `confidence`, and linked excerpts—making complex data interactive and filterable without cluttering individual notes.
   - **Automation Enhancements**:
     - Pipeline Integration: In `autonomous-distill` or `full-autonomous-ingest`, after `append_to_hub`, auto-insert Dataview blocks via `obsidian_append_to_note` (e.g., `TABLE title, status, confidence FROM "3-Resources" WHERE status = "needs-review" SORT confidence DESC`).
     - Periodic Sweeps: Use Obsidian's "DataviewJS" or pair with Templater to auto-refresh hubs on vault load/reload—e.g., a script that rebuilds a "Review Dashboard" note with queries for low-confidence items.
     - MCP Extension: Chain `obsidian_global_search` with Dataview syntax to generate and insert views programmatically (e.g., query for "notes with confidence <85" and append a sorted list to a log hub).
     - Community Automation: Plugins like "Periodic Notes" or "Calendar" can trigger daily/weekly Dataview updates, auto-flagging resurfacing candidates without manual tags.

### 3. **Callouts and Admonitions for Visual Emphasis**
   - **Improvement in Data Conveyance**: Use Obsidian's built-in callouts (e.g., > [!note] Title \n Content) to box important sections like TL;DR summaries, next actions, or warnings—conveying hierarchy and focus without tags. Customize with colors/icons (via CSS snippets) for at-a-glance meaning (e.g., green for actions, red for reviews).
   - **Automation Enhancements**:
     - Pipeline Embed: In `autonomous-distill`, after generating TL;DR, use `obsidian_append_to_note` to insert callouts like `> [!summary] TL;DR\n- Bullet 1\n- Bullet 2`.
     - Templater Scripts: Auto-generate callouts in templates, e.g., `> [!action] Next Steps\n<% tp.system.prompt("Enter actions") %>` (or AI-populate via Cursor/MCP).
     - Batch Processing: Extend MCP with a custom `obsidian_insert_callout` tool that scans notes for patterns (e.g., "if low confidence, insert > [!warning] Review Needed") during ingest sweeps.
     - Highlightr Synergy: Combine with your distill-highlight-color skill to auto-wrap highlighted text in themed callouts (e.g., red highlights → > [!important] block).

### 4. **Canvas and Graph Views for Relational Mapping**
   - **Improvement in Data Conveyance**: Move beyond linear tags to visual graphs/canvases that show note relationships (e.g., a canvas linking Projects to Resources with arrows for dependencies). This conveys context and flows intuitively, reducing the need for tag-based navigation.
   - **Automation Enhancements**:
     - Pipeline Hook: In `full-autonomous-ingest`, after `append_to_hub`, use `obsidian_create_canvas` or append links to an existing canvas file (e.g., auto-add nodes for new notes via JSON canvas format).
     - Graph Automation: Plugins like "Graph Analysis" or "Excalidraw" can auto-generate sub-graphs; script via MCP to update a "PARA Overview" canvas with new edges based on frontmatter `links`.
     - Resurfacing Integration: In `autonomous-archive`, before archiving, auto-add archived notes to a "History Canvas" for visual timeline conveyance.
     - JS Automation: Use Obsidian's API (via plugins like "Advanced Scripts") to periodically rebuild graphs/canvases from queries, e.g., "connect all notes with para-type: Project to their Areas."

### 5. **Tasks and Checklists for Actionable Data**
   - **Improvement in Data Conveyance**: Convert implied actions (e.g., from tags like #todo) into native Obsidian tasks ([ ] Item), which are queryable and integrable with plugins like Tasks. This makes data more interactive—e.g., a dashboard showing overdue items across notes.
   - **Automation Enhancements**:
     - Skill Integration: Embed your next-action-extract skill in `full-autonomous-ingest` to scan and convert phrases to tasks automatically (e.g., "Next: do X" → - [ ] Do X).
     - Tasks Plugin: Auto-query and embed task lists in hubs (e.g., `Tasks: not done due before today`); use Templater to insert checklists in new notes based on para-type.
     - MCP Chaining: After `distill_note`, use `obsidian_search_replace` to format actions as tasks, then log completions.
     - Periodic Automation: Plugins like "Tasks Calendar" auto-sync tasks to daily notes; script sweeps to escalate unchecked items (e.g., add to frontmatter `priority: high`).

### Implementation Tips for Your Pipelines
- **Reducing Tag Reliance Overall**: In your rules/pipelines, prioritize frontmatter over tags (e.g., query via Dataview `WHERE status = "raw"` instead of #raw-ingest). Start by auditing existing notes with MCP's `obsidian_global_search` to migrate tags to frontmatter.
- **Testing Autonomy**: Prototype in a test vault—e.g., drop raw notes into Ingest/, trigger `full-autonomous-ingest`, and verify automated insertions (callouts, Dataview blocks) without manual steps.
- **Plugin Stack**: Ensure Dataview, Templater, and Tasks are installed; for advanced automation, add "Obsidian Scripts" or "QuickAdd" to run JS/MCP on events like note save.
- **Scalability**: These methods are less brittle than tags for large vaults, as they're structured and queryable. If needed, extend MCP with custom tools for bulk operations.

This approach keeps your Second Brain more visual and automated, aligning with BASB's emphasis on resurfacing and expression without overwhelming tag sprawl. If you share a specific pipeline or note example, I can refine these further!












## Overall Progress Assessment

**High-level view**

Your system is **roughly 70% aligned** with the Master Goal at the design/configuration level, and **~55–60% in terms of fully wired, routinely exercised automation**. Conceptually it’s very strong: PARA, Zettelkasten, Highlightr color grammar, MCP tools, and Cursor skills/rules are all thoughtfully designed and mostly implemented. The main gaps are **missing context rules that bind pipelines to natural-language triggers**, **QuickAdd wiring**, and **lack of empirical validation + logging for edge cases and fallbacks**.

**Estimated completion by major components**

| Component                    | Est. Completion | Rationale (short)                                                                 |
|-----------------------------|----------------|-----------------------------------------------------------------------------------|
| **Overall automation**      | **75%**        | Pipelines + skills + MCP tools exist; some triggers/rules not yet fully wired.   |
| **Trustworthiness/safety**  | **70%**        | Backup-first, thresholds, logging designed; some behavior not yet battle-tested. |
| **Visual/relational clarity** | **65%**      | Highlightr grammar, Dataview dashboards, hubs defined; needs more automation use.|
| **PARA/Zettelkasten alignment** | **80%**    | Folder structure, templates, MCP tools and skills align well with BASB principles.|
| **End-to-end autonomy (post-capture)** | **60%** | Ingest autopilot implemented; distill/archiving/express pipelines lack context rules & macros. |

**Key strengths**

- **Strong conceptual and structural foundation**: PARA folders, `PARA-Dashboard`, project/area/resource hubs, `Resurface` hub, ingest templates, and Zettelkasten principles are all clearly articulated and consistently applied in templates and docs (`README`, `Second Brain Summary`, atomic notes resource).
- **Well-specified MCP + skill pipelines**: The four pipelines (full-autonomous-ingest, autonomous-distill, autonomous-archive, autonomous-express) and 14 skills are described in detail in `Cursor-Skill-Pipelines-Reference.md` and individual `SKILL.md` files.
- **Safety and trust mechanisms are clearly designed**: Option C backup-first (`mcp-obsidian-integration.mdc`), clear confidence thresholds, and `obsidian_log_action` patterns are all present and reasonably consistent.
- **Visual grammar is unusually well thought-out**: `Highlightr-Color-Key.md` and distill-related skills encode a visual language (analogous/complementary colors, project `highlight_key` overrides) aligned with your Master Goal.

**High-level weaknesses / roadblocks**

- **Missing or incomplete context rules for several pipelines**: Only `mcp-obsidian-integration.mdc`, `para-zettel-autopilot.mdc`, and `auto-resurface.mdc` are present; others described in `Cursor-Project-Rules-Summary.md` are not yet recreated as `.cursor/rules/*.mdc`.
- **QuickAdd automation not actually wired yet**: `quickadd/data.json` has no choices; the “Process Ingest” script exists, but buttons/commands in Obsidian are not configured.
- **Some capabilities are still “on paper”**: The Connection Ingest plugin spec, archive and express pipelines, and some fallback behaviors are documented but not present as working code or logs.
- **Limited real-world logs**: `Ingest-Log.md` shows a single autopilot batch; fallback behavior and threshold edge cases are not yet well exercised.

---

## Component-by-Component Breakdown

### 1. Capture Manual-Only

**Status: Partially Implemented (design solid; some UX wiring missing)**

- **Evidence**
  - Ingest templates (`Templates/Ingest-Template.md`, `Templates/Ingest-template/*.md`) and folder templates wired via Templater (`.obsidian/plugins/templater-obsidian/data.json`) mean **new files in `Ingest/` are automatically structured** with appropriate frontmatter (`status: ingest`, `para-type: Ingest`, etc.).
  - `Templates/Ingest-Selector.tpl` and `Ingest-Selector.md` implement a chooser so the user can pick ingest subtype; capture feels guided but still **invoked by the user creating a note or using Templater**.
  - `Templates/Scripts/ProcessIngestTrigger.js` + `2026-02-24-plugin-modification-report.md` define a QuickAdd script for appending standardized ingest triggers to `Ingest-Log.md`.
  - `Templates/AI Prompts.md` and `2026-02-24-cursor-ingest-prompt-reference.md` define canonical prompts like “INGEST MODE – safe batch autopilot”.

**Gaps / Missing elements**

- **QuickAdd choices are not configured** in `quickadd/data.json` (no `choices` array), so:
  - There is **no single-click capture/trigger** for “Process Ingest” yet; the user must run the script manually (e.g., from devtools or by custom command) or type prompts directly in Cursor.
- Capture on mobile and highlights:
  - The **Connection Ingest plugin spec** exists (`2026-02-24-connection-ingest-plugin-spec.md`) but there is **no corresponding plugin folder** under `.obsidian/plugins/` in this workspace snapshot.
- The Master Goal wants **capture to be the only manual step**; currently:
  - Users must manually trigger batch processing (e.g., by saying “INGEST MODE” in Cursor, or running QuickAdd once wired).
  - Low-confidence items intentionally require manual review (`#review-needed`), which is acceptable but still an extra manual lane.

**Improvements Needed**

- **Wire QuickAdd**:
  - Create QuickAdd choices that:
    - **Append ingest triggers** using `ProcessIngestTrigger.js`.
    - Optionally **open Cursor** with a pre-filled “INGEST MODE” prompt.
  - This will make capture + trigger a single frictionless gesture.
- **Implement and install the Connection Ingest plugin**:
  - Turn the spec into a real plugin directory in `.obsidian/plugins/connection-ingest/`.
  - Test with highlighted text → ingest note workflow.
- Long-term: consider a **background watcher** (e.g., small script that, when Obsidian is open and `Ingest/` changes, suggests or auto-launches “INGEST MODE” in Cursor via a hotkey).

**Risks / Edge Cases**

- Without QuickAdd choices, users might **inconsistently trigger ingest**, leading to a backlog in `Ingest/`.
- Mobile workflows may remain partially manual until the Connection Ingest plugin is installed.

---

### 2. Automation Pipeline Triggers

**Status: Partially Implemented**

- **Evidence**
  - **Ingest**:
    - Rule: `.cursor/rules/context/para-zettel-autopilot.mdc` matches `Ingest/*.md` and describes the ingest pipeline and confidence thresholds.
    - `2026-02-24-cursor-ingest-prompt-reference.md` defines “INGEST MODE – safe batch autopilot” as the prompt pattern.
    - `Ingest-Log.md` documents actually running a batch on 2026-02-25.
  - **Resurface**:
    - Context rule: `.cursor/rules/context/auto-resurface.mdc` binds resurfacing behavior to `Resurface.md` and specific phrases.
  - Pipelines:
    - `Cursor-Skill-Pipelines-Reference.md` and `.cursor/plans/skill_pipelines_implementation_4a85cdd2.plan.md` define **four pipelines** and their trigger phrases conceptually.

**Gaps / Missing elements**

- **No dedicated context rules yet for**:
  - Autonomous-distill (e.g., “DISTILL MODE”, “Refine this note”).
  - Autonomous-archive (archive sweeps).
  - Autonomous-express (“Express this note”).
- **QuickAdd → Cursor launch integration** isn’t wired:
  - The design says “use QuickAdd to append triggers and then say X in Cursor”, but there is no direct call chain.
- No explicit tests for **bulk imports**:
  - `para-zettel-autopilot` rule design states per-note processing with sequential backups, but you have only one real ingest batch log (`Ingest-Log.md`), not a stress test.

**Improvements Needed**

- **Create `.cursor/rules/context/*.mdc` for each pipeline**:
  - E.g. `auto-distill.mdc`, `auto-archive.mdc`, `auto-express.mdc` with:
    - Glob patterns (e.g. `1-Projects/*.md`, `2-Areas/**/*.md`).
    - Trigger phrases (“DISTILL MODE”, “Archive sweep”, “Express this note”).
- **Add QuickAdd macros** that:
  - Insert appropriate **trigger callouts** into logs or notes.
  - Optionally call `cursor-ide` or open Cursor with specific prompt snippets (manually for now).
- **Design and test bulk-ingest behavior**:
  - Use Ingest with 10–20 notes and verify:
    - Per-note backup creation.
    - Performance (no timeouts).
    - Logging for successes and `#review-needed`.

**Risks / Edge Cases**

- Without these context rules, **distill/archiving/express pipelines are discoverable only via documentation**, not actual automation.
- Bulk ingest may stress the MCP server without clear progress feedback if logging isn’t robust.

---

### 3. PARA Organization

**Status: Largely Implemented (with minor empirical gaps)**

- **Evidence**
  - PARA root structure: `1-Projects/`, `2-Areas/`, `3-Resources/`, `4-Archives/` and `PARA-Dashboard.md`.
  - Hubs: `Projects Hub.md`, `Areas Hub.md`, `Resources Hub.md`.
  - MCP tool: `obsidian_classify_para` + resource note describing classification logic.
  - Skill: `frontmatter-enrich` sets `para-type` and `project-id`.
  - Skill: `subfolder-organize` builds up to 4-level deep paths based on `para-type`, `project-id`, and semantic themes, then uses `obsidian_move_note` (and `obsidian_ensure_structure`) to **automatically create nested subfolders**.
  - Ingest rule: `para-zettel-autopilot.mdc` includes “move from Ingest to correct PARA location” steps.

**Gaps / Missing elements**

- Behavior of `obsidian_move_note` and `obsidian_ensure_structure` is **partially assumed**:
  - `mcp-obsidian-integration.mdc` and `skill` docs promise that if the parent directory doesn’t exist, `obsidian_ensure_structure` will handle it, but they note that **actual behavior still needs verifying and documenting**.
- No explicit tests for **deep subfolder hierarchies** (3–4 levels) or conflicting path decisions.

**Improvements Needed**

- **Empirically confirm**:
  - Whether `obsidian_move_note` plus `obsidian_ensure_structure` reliably creates nested directories.
  - How conflicts are handled (e.g., existing file at target path).
- Once tested, **add a short note** (e.g., `3-Resources/2026-XX-XX-mcp-move-note-behavior.md`) and update `mcp-obsidian-integration.mdc` with confirmed behavior.

**Risks / Edge Cases**

- Mis-handled path creation could lead to:
  - Notes stranded in `Ingest/`.
  - Ambiguous folder names.
  - Risk of overwriting if `update_note` is misused on non-existent paths.

---

### 4. Atomic Note Splitting

**Status: Implemented at MCP + rule level; not heavily exercised**

- **Evidence**
  - Resource: `2026-02-23-atomic-notes-zettelkasten-principle.md` clearly defines atomicity.
  - MCP tool: `obsidian_split_atomic` with dedicated resource note describing prompts/behavior.
  - Rule: `para-zettel-autopilot.mdc` includes “split into atomic notes if multi-idea” step after classification.
  - `Cursor-Project-Rules-Summary.md` includes an “auto-zettelkasten-atomicity” section.

**Gaps / Missing elements**

- No **logged examples in `Ingest-Log.md`** of split operations, or what resulting note names look like.
- No explicit tests for:
  - Overlapping themes between resulting notes.
  - Idempotency (running split twice shouldn’t keep splitting forever).
  - Maintaining links between original and splits (e.g. via `related` field or backlinks).

**Improvements Needed**

- Run **controlled experiments**:
  - Create synthetic multi-idea ingest notes.
  - Trigger ingest and record:
    - Number and naming of new notes.
    - How links/frontmatter are propagated.
- Consider adding a **post-split skill or rule**:
  - E.g., “split-link-preserve” that:
    - Writes a “Split from” / “Split into” section for manual navigation and Dataview.

**Risks / Edge Cases**

- Over-aggressive splitting could fragment context and overwhelm the PARA structure.
- Under-splitting could defeat Zettelkasten goals and degrade distillation.

---

### 5. Progressive Distillation

**Status: Conceptually and technically implemented; triggers/rules incomplete**

- **Evidence**
  - MCP tool: `obsidian_distill_note` and resource note.
  - Rule: `para-zettel-autopilot.mdc` includes distill step as part of ingest.
  - Skills:
    - `distill-highlight-color` — applies color grammar after distill.
    - `layer-promote` — implements progressive summarization layers.
    - `callout-tldr-wrap` — callout emphasis.
    - `summary-preserve` — pre-archive preservation.
    - `readability-flag` — readability assessment.
  - `Cursor-Skill-Pipelines-Reference.md` defines an “autonomous-distill pipeline” that chains these skills.

**Gaps / Missing elements**

- No **context rule** yet that triggers “autonomous-distill” for arbitrary notes.
- Distill pipeline is mostly described as part of ingest and distill pipelines; not yet a **standalone mode**.
- Lack of **real-world logs**:
  - There are no logs showing `readability-flag` or `layer-promote` outcomes in typical notes.

**Improvements Needed**

- Add `.cursor/rules/context/auto-distill.mdc`:
  - Triggers on phrases like “Distill this note” and globs for key folders.
- Run **batch distill** on a small set of existing notes and inspect results:
  - Confirm TL;DR placement, highlight layering, readability warnings.

**Risks / Edge Cases**

- Over-distillation might oversimplify nuanced notes.
- Misinterpreted readability thresholds might flood notes with warning callouts.

---

### 6. Color-Coded Highlighting (Highlightr)

**Status: Strong design and partial automation; needs wider usage**

- **Evidence**
  - Plugin config: `.obsidian/plugins/highlightr-plugin/data.json` defines palette and ordering.
  - Master key: `3-Resources/Highlightr-Color-Key.md` outlines semantics, analogies, complementary colors, and `highlight_key` project overrides.
  - Skills: `distill-highlight-color` and `layer-promote` explicitly read the master key and use complementary/analogous colors to express relationships.
  - `2026-02-25-highlighter-second-brain-pipeline.md` describes how Highlightr integrates into distill pipelines.

**Gaps / Missing elements**

- No **Dataview-based checks** to ensure highlight usage is consistent across notes/projects.
- Limited evidence of **actual highlight patterns** already applied to many notes; it appears still early-stage (design-heavy, usage-light).

**Improvements Needed**

- Run “autonomous-distill” (once the context rule exists) on a sample of:
  - One project note.
  - One area note.
  - One resource note.
- Then create a **“Highlight Audit”** Dataview or daynote:
  - Sampling `==...==^{Color}` patterns to verify consistent semantics and catch anomalies.

**Risks / Edge Cases**

- Misalignment between user-intended meaning and automated color assignment could reduce trust in the visual language.
- Overuse of colors could cause visual clutter without meaning.

---

### 7. Frontmatter Enrichment

**Status: Implemented with strong design**

- **Evidence**
  - Skill: `frontmatter-enrich/SKILL.md` clearly specifies:
    - `status`, `confidence`, `para-type`, `created`, `links`, optional `project-id`, `priority`, `deadline`.
  - MCP tool: `obsidian_manage_frontmatter` and resource note.
  - `Cursor-Project-Rules-Summary.md` “always-frontmatter-naming” section defines conventions.
  - Additional frontmatter from skills:
    - `readability-flag` (`needs-simplify`).
    - `resurface-candidate-mark` (`resurface-candidate`).
    - `next-action-extract` (frontmatter `next-actions`).
    - Archive-related fields (`status: complete`).

**Gaps / Missing elements**

- Not yet clear **how uniformly** frontmatter is applied across legacy notes.
- Some dashboards rely on `para-type` and `status`; older notes might not yet conform.

**Improvements Needed**

- Consider an **audit pipeline**:
  - Use `obsidian_global_search` + Dataview to find notes missing required frontmatter fields.
  - Run a one-time “frontmatter normalization” operation with conservative thresholds.

**Risks / Edge Cases**

- Inconsistent frontmatter could break Dataview queries or misclassify notes in dashboards.

---

### 8. Hub Linking and Relationships

**Status: Implemented for core PARA hubs; dynamic expression partially planned**

- **Evidence**
  - Hubs: `Projects Hub.md`, `Areas Hub.md`, `Resources Hub.md`, `Resurface.md`.
  - MCP: `obsidian_append_to_hub` + resource note.
  - `Cursor-Skill-Pipelines-Reference.md`:
    - Ingest pipeline includes hub appends for new notes.
    - Resurface pipeline uses hubs + `resurface-candidate-mark`.
- Also, the express pipeline’s `related-content-pull` skill adds **“Related” sections**, acting as relational overlays.

**Gaps / Missing elements**

- No explicit **graph/canvas integration** (e.g., auto-building Canvas boards) beyond text + Dataview.
- It’s not clear if **every** new note from ingest gets hub entries; logging suggests more design than practice so far.

**Improvements Needed**

- Verify via Dataview:
  - That new notes **do appear** in hubs as expected.
- Consider designing a **canvas/graph generator**:
  - E.g., a script/skill that creates or updates `.canvas` files for each project/area.

**Risks / Edge Cases**

- Under-linking might make the network feel sparser than the actual knowledge base.
- Over-linking could clutter hubs and reduce scanability.

---

### 9. Action Extraction

**Status: Implemented and conceptually sound**

- **Evidence**
  - Skill: `next-action-extract` extracts tasks into:
    - Markdown checkboxes (`- [ ]`) in note body.
    - `next-actions` frontmatter.
  - Tasks plugin config (`obsidian-tasks-plugin/data.json`) and plugin modification report show:
    - Created dates are captured; plugin is configured to work with Dataview.
  - `PARA-Dashboard.md` and `Projects Hub.md` include **task-oriented Dataview queries** (e.g., incomplete tasks per project).

**Gaps / Missing elements**

- No metrics/logging of:
  - How many notes have `next-actions` frontmatter.
  - How accurate auto-extracted tasks are.
- No dedicated context rule for “extract actions now” outside ingest/express pipelines.

**Improvements Needed**

- Add “Action extraction audit”:
  - A Dataview table listing all notes with/without `next-actions` and tasks.
- Optionally, create an `auto-actions` context rule for triggered extraction.

**Risks / Edge Cases**

- Misinterpreted narrative text as actions could clutter task lists.
- Task duplication between narrative and frontmatter list.

---

### 10. Archiving and Resurfacing

**Status: Archive pipeline designed; partially wired. Resurfacing is on-demand and implemented.**

- **Evidence**
  - Skills:
    - `archive-check` — identifies archive candidates by status, age, and open-tasks check.
    - `subfolder-organize` — handles moves into `4-Archives/`.
    - `summary-preserve` — enforces TL;DR before archive.
    - `resurface-candidate-mark` — marks potential resurfacing items.
  - Rule: `.cursor/rules/context/auto-resurface.mdc` + `Resurface.md` hub with Dataview for `resurface-candidate: true`.
  - `Cursor-Skill-Pipelines-Reference.md` defines the “autonomous-archive” pipeline.

**Gaps / Missing elements**

- No dedicated `auto-archive.mdc` context rule so far.
- No existing logs that show a full **archive batch run**:
  - `Ingest-Log.md` is the only log with autopilot behavior, focused on ingest.
- Resurfacing remains **user-triggered only** by design:
  - No scheduled/resident process.

**Improvements Needed**

- Implement `.cursor/rules/context/auto-archive.mdc`:
  - Trigger phrases like “Archive sweep” and appropriate globs.
- Run a small **pilot archive sweep** on old notes:
  - Confirm `archive-check` + `subfolder-organize` behavior.
  - Verify logs include backup paths and archive destinations.

**Risks / Edge Cases**

- Over-aggressive archival without enough `summary-preserve` might make archived notes hard to re-use.
- Resurfacing may under-surface useful notes if `resurface-candidate-mark` is rarely triggered.

---

### 11. Early Express/Output Generation

**Status: Designed and partially implemented at skill level; not yet wired via rules**

- **Evidence**
  - Express pipeline in `Cursor-Skill-Pipelines-Reference.md`.
  - Skills:
    - `version-snapshot` — snapshots original notes to `Versions/` subfolder before major appends.
    - `related-content-pull` — builds a related section.
    - `express-mini-outline` — adds an outline/summary block.
    - `call-to-action-append` — appends a CTA callout.

**Gaps / Missing elements**

- No `auto-express.mdc` context rule or similar to bind it to triggers.
- No logged examples of an express pipeline run.

**Improvements Needed**

- Create `auto-express` context rule and test on:
  - A project note with multiple highlights and tasks.
- Optionally, add a **Dataview view** for notes that have `Versions/` snapshots and CTA callouts to track express-ready material.

**Risks / Edge Cases**

- Express pipeline might **override user’s narrative style** if applied too aggressively.
- Version snapshot frequency must be managed to avoid clutter.

---

### 12. Trustworthiness Features (Confidence, Backup, Logging)

**Status: Strong on paper and largely in rules/skills; needs more empirical runs**

- **Evidence**
  - Confidence thresholds:
    - Centralized in `Cursor-Skill-Pipelines-Reference.md` and each `SKILL.md`.
    - Most capabilities use **≥85%** for auto-execution, with some lower thresholds (e.g., readability at 70%, resurface candidate at 75%, distill-highlight at 80%).
    - `para-zettel-autopilot.mdc` enforces 85% for destructive actions and requires `#review-needed` tagging otherwise.
  - Backup-first:
    - `mcp-obsidian-integration.mdc` and `Cursor-Project-Rules-Summary.md` describe:
      - Always call `obsidian_create_backup` before destructive operations.
      - Never use shell `cp/mv/rm` — only MCP.
      - Document backup paths in logs and “changes” strings.
    - `~/.cursor/mcp.json` config ensures `BACKUP_DIR` and autoApproval for `obsidian_create_backup` and related tools.
  - Logging:
    - `obsidian_log_action` MCP tool.
    - `Cursor-Project-Rules-Summary.md` “auto-logging” section describes canonical log line.
    - `Ingest-Log.md` shows an example autopilot batch summary with confidence and backup path.

**Gaps / Missing elements**

- **Inconsistent documentation vs. reality**:
  - `rule_recreation_evaluation_d0f44390.plan.md` mentions **older 90% thresholds** and calls for unification; current files mostly use 85%, but a quick grep could still find inconsistencies.
- **No dedicated MCP behavior note** confirming fallbacks:
  - `mcp-obsidian-integration.mdc` outlines desired fallback logic but acknowledges real behavior must be verified.
- Limited **failure-mode logs**:
  - Very few examples of backup failures or move failures logged with `#review-needed`.

**Improvements Needed**

- Perform a **“safety audit run”** with intentionally malformed operations:
  - Force `obsidian_create_backup` to fail (e.g., misconfigured `BACKUP_DIR` temporarily in a test env).
  - Attempt moves to invalid paths.
  - Verify fallback behavior and logs, then capture results in a dedicated resource note and update rules accordingly.
- Run a **global grep** for “90%” and unify all thresholds at 85% where appropriate.

**Risks / Edge Cases**

- If thresholds or fallbacks are implemented inconsistently across skills, users may see **surprising auto-edits** or unexpected `#review-needed` behavior.
- Misconfigured backup paths could result in false sense of safety.

---

### 13. Visual and Relational Clarity

**Status: Strong design; moderate actual deployment**

- **Evidence**
  - Visual clarity elements:
    - Highlightr color semantics (`Highlightr-Color-Key.md`).
    - Distill/tldr callouts (`callout-tldr-wrap`, `summary-preserve`).
    - Dataview dashboards (`PARA-Dashboard.md`, hubs).
    - Resurface hub (`Resurface.md`) with Dataview queries.
    - Tasks dashboards in dashboards and hubs.
  - No heavy use of tag clutter; most semantics are in **frontmatter** and structural organization.

**Gaps / Missing elements**

- No **single “visual audit” report**:
  - Nothing synthesizing how many notes are highlight-rich, how many have TL;DRs, etc.
- Canvas/graph integration is not yet automated, as noted above.

**Improvements Needed**

- Add a **“Visual Health Dashboard”** note:
  - Dataview tables:
    - Notes with TL;DR vs without.
    - Notes with Highlightr usage.
    - Notes with `needs-simplify`.
    - Notes with `resurface-candidate`.
- Consider incremental **canvas automation** for high-value projects.

**Risks / Edge Cases**

- If the visual layers remain under-used, the system might feel like a standard text-first vault despite strong underlying design.

---

## Cross-Cutting Analysis

### Integration and Flow

- **Design-wise, integration is excellent**:
  - Ingest pipeline: Ingest templates → Templater → MCP classify PARA → split atomic → distill → frontmatter-enrich → subfolder-organize → append-to-hub → distill-highlight-color → layer-promote → next-action-extract → log-action.
  - Archive pipeline: archive-check → summary-preserve → subfolder-organize → resurface-candidate-mark.
  - Express pipeline: version-snapshot → related-content-pull → express-mini-outline → call-to-action-append.
- **Actual runtime integration** is best for **ingest**; other pipelines are still design-stage until you add rules/macros.

### Performance and Efficiency

- No explicit performance issues detected:
  - Tools are designed to operate one-note-at-a-time, with per-note backups.
  - However, there are no benchmarks or notes about **large collections** (hundreds or thousands of notes) being processed in one go.

### User Experience (“Hands-off yet trustworthy”)

- The system **leans heavily toward trust** via:
  - Confidence thresholds.
  - Backup-first policies.
  - Clear `#review-needed` path to `3-Resources/Ingest-Review.md`.
- It is **not yet fully hands-off** because:
  - Triggering pipelines still requires manual prompts or not-yet-configured QuickAdd macros.
  - Some rules have not been created, so the assistant relies on you typing long prompts or using resources as references.

### Extensibility

- **Extensibility is strong**:
  - Skills-based design makes it easy to add new capabilities.
  - MCP tool descriptors and resource notes clearly document behavior.
  - PARA and Zettelkasten patterns are generic and reusable across projects.

### Compliance with PARA, Zettelkasten, BASB

- Good compliance:
  - PARA folder structure and templates are correct.
  - Atomic notes principle is explicit and linked to splitting logic.
  - Emphasis on “Action & Expression” through express pipeline and tasks extraction aligns well with BASB.
- Minimal tag clutter; frontmatter + paths + Highlightr handle most semantics.

---

## Recommendations and Roadmap

### High priority (impactful and foundational)

1. **Implement missing context rules for distill, archive, and express pipelines**  
   - **Effort**: Medium  
   - **Actions**:
     - Add `.cursor/rules/context/auto-distill.mdc`, `auto-archive.mdc`, `auto-express.mdc` that:
       - Bind natural language triggers (“DISTILL MODE”, “Archive sweep”, “Express this note”) and note patterns.
       - Invoke the appropriate skill sequences as defined in `Cursor-Skill-Pipelines-Reference.md`.

2. **Wire QuickAdd choices for ingest and processing triggers**  
   - **Effort**: Medium  
   - **Actions**:
     - Configure QuickAdd choices that:
       - Call `ProcessIngestTrigger.js` to append standardized ingest triggers to `Ingest-Log.md`.
       - Optionally open Cursor (manually) with the canonical “INGEST MODE – safe batch autopilot” prompt.
     - Add docs/screenshots to `Plugin Automation Report` or a small new resource.

3. **Turn the Connection Ingest plugin from spec into a live plugin**  
   - **Effort**: Medium–High  
   - **Actions**:
     - Move the code from `2026-02-24-connection-ingest-plugin-spec.md` into a real plugin folder (`.obsidian/plugins/connection-ingest/`).
     - Run `npm install` + build, enable in Obsidian.
     - Test highlight → ingest note workflows and log outcomes.

4. **Empirically validate MCP fallbacks and document behavior**  
   - **Effort**: Medium  
   - **Actions**:
     - In a safe test environment, intentionally cause:
       - `move_note` to fail (invalid parents).
       - `update_note` to a new path with missing parent.
       - `create_backup` failures via temporary misconfig.
     - Confirm actual behavior and update:
       - `mcp-obsidian-integration.mdc`.
       - Add a `2026-XX-XX-mcp-behavior-validation.md` resource.

5. **Unify and confirm confidence thresholds across rules and skills**  
   - **Effort**: Low–Medium  
   - **Actions**:
     - Grep for “90%” or inconsistent threshold values.
     - Align all to your **standard 85%** (with exceptions explicitly justified).
     - Update `Cursor-Skill-Pipelines-Reference.md` and skills accordingly.

### Medium priority

6. **Fill out `Rules-Recreation-Gap-Table.md` and `Rules-Recreation-Log.md`**  
   - **Effort**: Medium  
   - **Actions**:
     - For each rule family in `Cursor-Project-Rules-Summary.md`, record:
       - Which `.cursor/rules/*.mdc` files now exist.
       - Which skills cover their behavior.
       - Remaining gaps and planned fixes.

7. **Run real pilot batches for archive and express pipelines and log them**  
   - **Effort**: Medium  
   - **Actions**:
     - Choose a small set of older notes.
     - Run “Archive sweep” and “Express this note” once rules exist.
     - Record before/after snapshots, backup paths, and notes in logs.

### Lower priority / long-term

8. **Visual Health Dashboard**  
   - **Effort**: Low–Medium  
   - **Actions**:
     - Create a `Visual Health.md` note with Dataview queries for:
       - TL;DR presence.
       - Highlightr usage.
       - `needs-simplify`, `resurface-candidate`, `next-actions`.
     - Use this dashboard to drive periodic cleanup.

9. **Canvas/graph hints automation**  
   - **Effort**: Medium–High  
   - **Actions**:
     - Explore a small script/skill that:
       - Generates `.canvas` files for each project or area using hubs + relationships.
     - Start with 1–2 pilot projects.

10. **Bulk ingest performance tests**  
    - **Effort**: Medium  
    - **Actions**:
      - Simulate ingest for 20+ notes and observe:
        - MCP timeouts.
        - Log readability.
        - Memory/performance impacts.

---

## Final Summary

Your Second Brain is **conceptually robust and structurally well-built**, with PARA, Zettelkasten, and Highlightr color grammar all thoughtfully integrated and backed by MCP tools, skills, and rules. The core ingest pipeline is operational and safety-focused, but **distill, archive, and express pipelines remain mostly at the design and configuration stage until additional context rules and QuickAdd wiring are added**. Trust and safety mechanisms (backup-first, confidence thresholds, `#review-needed`, structured logs) are strong on paper but still need more real-world runs and failure-mode validation. Closing these wiring and validation gaps will move you from a highly promising, partially-autonomous system to the fully hands-off, post-capture external brain you’re targeting.





## Summary of changes

- **Snapshot skill & MCP env**: Added a new `obsidian-snapshot` skill with flattened naming, integrity hashes, retention guidance, and anomaly handling; updated `~/.cursor/mcp.json` to introduce `SNAPSHOT_DIR` and `BATCH_SNAPSHOT_DIR` for in-vault snapshots and batch checkpoints.
- **Rules & pipelines**: Extended the always-applied MCP rule and ingest rule to require per-change snapshots before destructive actions, added explicit batch checkpoint behavior, created trigger-based `auto-restore` and `snapshot-sweep` context rules, and documented snapshot triggers across all four pipelines.
- **Docs & hubs**: Created `obsidian_snapshot_TOOL` spec, a central `Backup-Log`, a `Restore Hub` with storage health and failure surfacing, and an `enhanced-snapshots` reference; updated `version-snapshot`, `archive-check`, and the pipelines reference to align with the new architecture and testing expectations.
- **Security & trust**: Documented encryption recommendations for external backups, ensured snapshots are treated as immutable atomic states with hash verification on restore, and kept all restore and retention behavior explicitly user-triggered (no silent auto-rollback or deletion).

---

## Key code / config updates

### 1. New skill: `obsidian-snapshot`

**File added**: `.cursor/skills/obsidian-snapshot/SKILL.md`

- Defines flattened snapshot naming under `SNAPSHOT_DIR`:

```markdown
`SNAPSHOT_DIR/<slug>--<short-path-hash>--<timestamp>.md.bak`
```

- Requires rich frontmatter in each snapshot (per-change):

```markdown
original_path
original_title
pipeline
snapshot_type: per-change
snapshot_created
snapshot_hash
confidence
flag
immutable: true
para-type: Archive
status: frozen
```

- Per-change flow (high level):
  - `obsidian_read_note` → build flattened `snapshot_path` → compute `snapshot_hash` → `obsidian_update_note` to `snapshot_path` → append entry to `3-Resources/Backup-Log.md`.
  - On anomaly (bad paths, misconfigured dirs, write failure):
    - Log `#review-needed` in `Backup-Log.md`, **skip** the destructive action, continue batch.
- Batch flow:
  - Accepts `{note_path, snapshot_path}` list from caller.
  - Writes summary markdown into `BATCH_SNAPSHOT_DIR` with a small table of notes/snapshots/confidences.
  - Logs to `Backup-Log.md`.

It also documents retention knobs (`SNAPSHOT_MAX_DAYS`, `SNAPSHOT_MAX_PER_NOTE`) and defers actual cleanup to the `snapshot-sweep` rule.

---

### 2. MCP server config: snapshot directories

**File updated**: `~/.cursor/mcp.json`

```json
"obsidian-para-zettel-autopilot": {
  "command": "docker",
  "args": [
    "run",
    "-i",
    "--rm",
    "--network",
    "host",
    "-v",
    "/home/darth/Documents/Second-Brain:/home/darth/Documents/Second-Brain",
    "-v",
    "/home/darth/Documents/Second-Brain-oops-Backups:/home/darth/Documents/Second-Brain-oops-Backups",
    "-e",
    "OBSIDIAN_API_KEY",
    "-e",
    "OBSIDIAN_REST_URL",
    "-e",
    "OBSIDIAN_VAULT_PATH",
    "-e",
    "BACKUP_DIR",
    "-e",
    "SNAPSHOT_DIR",
    "-e",
    "BATCH_SNAPSHOT_DIR",
    "obsidian-para-zettel-autopilot-mcp:latest"
  ],
  "env": {
    "OBSIDIAN_API_KEY": "...",
    "OBSIDIAN_REST_URL": "http://127.0.0.1:27122",
    "OBSIDIAN_VAULT_PATH": "/home/darth/Documents/Second-Brain",
    "BACKUP_DIR": "/home/darth/Documents/Second-Brain-oops-Backups",
    "SNAPSHOT_DIR": "/home/darth/Documents/Second-Brain/Backups/Per-Change",
    "BATCH_SNAPSHOT_DIR": "/home/darth/Documents/Second-Brain/Backups/Batch"
  },
  ...
}
```

This keeps external backups (`BACKUP_DIR`) separate from in-vault snapshots (`Backups/`), which you can encrypt or handle via sync separately.

---

### 3. Always-applied MCP rule: snapshot configuration & chaining

**File updated**: `.cursor/rules/always/mcp-obsidian-integration.mdc`

Key additions:

- Ingest processing now explicitly mentions the snapshot skill:

```12:14:/home/darth/Documents/Second-Brain/.cursor/rules/always/mcp-obsidian-integration.mdc
- **Ingest processing**: Follow para-zettel-autopilot; chain MCP tools: **obsidian_create_backup** (first), then `obsidian_classify_para`, `obsidian_split_atomic`, `obsidian_distill_note`, `obsidian_append_to_hub`, `obsidian_move_note`, `obsidian_log_action`; verify after each step. For destructive steps, also call the **obsidian-snapshot** skill (see `.cursor/skills/obsidian-snapshot/SKILL.md`) to create a per-change snapshot before proceeding.
```

- New **Snapshot configuration** section documenting `BACKUP_DIR`, `SNAPSHOT_DIR`, `BATCH_SNAPSHOT_DIR`, and advising that `Backups/` should be on encrypted/protected storage if synced.
- **Snapshot chaining guidelines**:
  - Before any destructive MCP call (`split_atomic`, `distill_note` rewrites, `append_to_hub`, `move_note`, `rename_note`, `delete_note`):
    - Check confidence ≥85%.
    - Call `obsidian-snapshot` (per-change).
    - On failure → skip destructive action, log `#review-needed` in `Backup-Log.md`, continue with next note.
- **Security considerations**: Clarifies that snapshots are safety/history, not access control, and suggests excluding/encrypting backup dirs if the vault is public or synced widely.

---

### 4. Ingest rule: per-change snapshots & batch checkpoints

**File updated**: `.cursor/rules/context/para-zettel-autopilot.mdc`

New **Snapshots and checkpoints** section:

```18:36:/home/darth/Documents/Second-Brain/.cursor/rules/context/para-zettel-autopilot.mdc
- **External backup**: Every ingest run MUST start with `obsidian_create_backup` for each note, writing into `BACKUP_DIR` (see `mcp-obsidian-integration.mdc`).
- **Per-change snapshots (in-vault)**:
  - Before any destructive or structural step for a given note, call the `obsidian-snapshot` skill with `type: "per-change"`:
    - Before `obsidian_split_atomic` ...
    - Before `obsidian_distill_note` when it will rewrite ...
    - Before `obsidian_append_to_hub` ...
    - Before `obsidian_move_note` or `obsidian_rename_note`.
  - Only take per-change snapshots when confidence ... **≥85%**. If confidence is lower:
    - Do not snapshot.
    - Do not perform the destructive action; instead flag with `#review-needed` in Ingest-Log.md.
...
- **Batch checkpoints**:
  - Maintain a simple counter ...
  - After every **5 notes**, call `obsidian-snapshot` with `type: "batch"` ...
  - Log the batch checkpoint path into both `Ingest-Log.md` and `3-Resources/Backup-Log.md`.
- **Exclusions**:
  - Do not process or ingest notes under `Backups/` automatically ...
```

This keeps your existing batch semantics (one note at a time, up to 5 notes per run, continue-on-failure) and layers snapshots on top.

---

### 5. New context rules: restore & retention

**Restore rule**: `.cursor/rules/context/auto-restore.mdc`

- Trigger phrases: **RESTORE MODE**, “rollback last change”, “restore from snapshot”.
- Flow:
  - Identify target note (link/current).
  - Read `Restore Hub.md` + `Backup-Log.md`, choose recent per-change snapshots whose `original_path` matches.
  - Present last N candidates to you for selection.
  - For chosen snapshot:
    - Read snapshot, recompute hash, compare to `snapshot_hash`.
    - On mismatch → no restore; log `#review-needed` and recommend using external backup.
    - On match → overwrite original note with snapshot via `obsidian_update_note`, set `restored_from_snapshot` + `restored_at` in frontmatter, log restore in `Backup-Log.md`.
- Safety:
  - Never deletes snapshot files.
  - Never runs without explicit user trigger.
  - Only writes to non-`Backups/` paths.

**Snapshot sweep rule**: `.cursor/rules/context/snapshot-sweep.mdc`

- Globs: `Backups/Per-Change/*.md.bak` (for context).
- Trigger phrases: **SNAPSHOT SWEEP**, “Clean old snapshots”, “Apply snapshot retention”.
- Behavior:
  - Uses conceptual `SNAPSHOT_MAX_DAYS` and `SNAPSHOT_MAX_PER_NOTE` to find aged/excess snapshots.
  - Default action: **move**, not delete, into `Backups/Archives/` (ensuring the directory exists).
  - Logs each sweep into `Backup-Log.md` with summary (scanned/moved counts, criteria, and any `#review-needed` recommendations).
  - Deletion is only considered when explicitly requested and logged, and still recommends checking `BACKUP_DIR` first.

---

### 6. New resources: tool spec, log, hub, and summary

**Tool spec**: `3-Resources/obsidian_snapshot_TOOL.md`

- Defines a future `obsidian_snapshot` MCP tool schema:
  - Params: `note_path`, `type` (`per-change`|`batch`), `description`, `batch_details`, `profile`, `project_override`.
  - Pseudocode for:
    - Creating flattened per-change snapshots with hashes and frontmatter.
    - Creating batch snapshot markdown (with table of notes).
- Clarifies that until the tool exists, the `.cursor/skills/obsidian-snapshot` skill plus existing MCP tools implement the behavior.

**Log**: `3-Resources/Backup-Log.md`

- Central index for backup/snapshot/restore events, e.g.:

```markdown
2026-02-25 01:23 | type: per-change | note: 1-Projects/Project-X/note.md | snapshot: Backups/Per-Change/... | pipeline: ingest | confidence: 92% | flag: none
2026-02-25 01:30 | type: restore | note: ... | from: ... | result: success | flag: none
```

- Encourages using `flag: #review-needed` + reason for anomalies.
- Includes “How to restore” summary pointing to `Restore Hub.md` and `auto-restore.mdc`.

**Hub**: `3-Resources/Restore Hub.md`

- Explains:
  - Layered safety (external backups, per-change snapshots, batch checkpoints).
  - Storage health heuristics (Backups counts, suggested thresholds, when to run snapshot sweep).
  - How to surface **recent failures** by scanning `Backup-Log.md` / snapshot frontmatter for `#review-needed`.
  - Step-by-step restore checklist tied to RESTORE MODE prompts.
  - Positions snapshots as PARA **Resources** and atomic state units aligned with Zettelkasten.

**Summary doc**: `3-Resources/2026-02-25-enhanced-snapshots.md`

- Summarizes:
  - External backups vs in-vault snapshots vs batch checkpoints vs hubs/logs.
  - High-level per-change snapshot pseudocode.
  - Where and how rules integrate snapshots (`mcp-obsidian-integration.mdc`, `para-zettel-autopilot.mdc`, `auto-restore.mdc`, `snapshot-sweep.mdc`).
  - Performance notes and a table you can fill in when benchmarking.

---

### 7. Existing skills and pipelines reference updates

**`version-snapshot` skill**: `.cursor/skills/version-snapshot/SKILL.md`

- Clarified as **express-only narrative snapshotting**:

```8:12:/home/darth/Documents/Second-Brain/.cursor/skills/version-snapshot/SKILL.md
> **Note**: `version-snapshot` is focused on **narrative versions** ... It complements, but does not replace, the system-level `obsidian-snapshot` safety net ...
```

- Confidence note: still always runs in express, while destructive system actions must respect ≥85% and use `obsidian-snapshot`.

**`archive-check` skill**: `.cursor/skills/archive-check/SKILL.md`

- Added guidance for anomalies:

```13:22:/home/darth/Documents/Second-Brain/.cursor/skills/archive-check/SKILL.md
4. **If anomalies are detected** ... recommend **not archiving** automatically and suggest reviewing recent snapshots instead; include a short note to consult `Restore Hub.md`.
```

**Pipelines reference**: `3-Resources/Cursor-Skill-Pipelines-Reference.md`

- Added **Snapshot triggers (all pipelines)** table:

```139:149:/home/darth/Documents/Second-Brain/3-Resources/Cursor-Skill-Pipelines-Reference.md
## Snapshot triggers (all pipelines)

| Pipeline            | Per-change triggers                                                                                      | Batch frequency      |
|---------------------|----------------------------------------------------------------------------------------------------------|----------------------|
| full-autonomous-ingest | Before `split_atomic`, `distill_note` (when rewriting), `append_to_hub` ..., `move_note`, `rename_note` | Every 5 notes        |
| autonomous-distill  | Before first structural rewrite ...                                                                      | ~Every 3 notes       |
| autonomous-archive  | After `archive-check` recommends archive ... before `subfolder-organize` / `summary_preserve` / move    | Once per archive sweep |
| autonomous-express  | Before large appends ... alongside `version-snapshot`                                                    | Optional per batch   |
```

- Re-emphasizes that snapshots never become pipeline inputs and that <85% confidence leads to no snapshot + no destructive action + `#review-needed`.

---

## Updated files list

- **New**:
  - `.cursor/skills/obsidian-snapshot/SKILL.md`
  - `.cursor/rules/context/auto-restore.mdc`
  - `.cursor/rules/context/snapshot-sweep.mdc`
  - `3-Resources/obsidian_snapshot_TOOL.md`
  - `3-Resources/Backup-Log.md`
  - `3-Resources/Restore Hub.md`
  - `3-Resources/2026-02-25-enhanced-snapshots.md`
- **Updated**:
  - `~/.cursor/mcp.json` (env + args for snapshot dirs)
  - `.cursor/rules/always/mcp-obsidian-integration.mdc`
  - `.cursor/rules/context/para-zettel-autopilot.mdc`
  - `.cursor/skills/version-snapshot/SKILL.md`
  - `.cursor/skills/archive-check/SKILL.md`
  - `3-Resources/Cursor-Skill-Pipelines-Reference.md`

---

## Test report / how to validate

Since I can’t execute the MCP server from here, the following tests are designed for you to run in your environment:

### 1. Configuration sanity check

- Confirm that:
  - `Backups/Per-Change/` and `Backups/Batch/` directories exist (or will be auto-created by the MCP server on write).
  - `~/.cursor/mcp.json` validates as JSON and Cursor still launches the `obsidian-para-zettel-autopilot` server correctly.
- Open `mcp-obsidian-integration.mdc` and `para-zettel-autopilot.mdc` in Cursor to ensure no rule parsing errors.

### 2. Ingest pipeline snapshot behavior

- Create a few test notes under `Ingest/` (including normal, low-confidence, and malformed ones).
- Run your ingest trigger (e.g. **INGEST MODE – safe batch autopilot**):
  - For notes where destructive steps occur with ≥85% confidence, verify:
    - New files appear under `Backups/Per-Change/` with flattened names and proper frontmatter (including `original_path` and `snapshot_hash`).
    - `3-Resources/Backup-Log.md` has new `type: per-change` and `type: batch` lines.
  - For low-confidence or anomalous notes:
    - No destructive actions occur.
    - `Ingest-Log.md` and `Backup-Log.md` contain `#review-needed` entries.

### 3. Restore flow

- Pick a test note that has at least one snapshot.
- Manually edit the note to something obviously wrong.
- In Cursor, run a RESTORE MODE prompt, e.g.:
  - `RESTORE MODE – rollback last change to [[Your Test Note]]`
- Verify:
  - You are offered recent snapshots to choose from.
  - The selected snapshot’s content replaces the note.
  - The note’s frontmatter now has `restored_from_snapshot` and `restored_at`.
  - `Backup-Log.md` has a `type: restore` line.

### 4. Snapshot sweep (retention)

- Generate several snapshots so that `Backups/Per-Change/` has enough files.
- Run a snapshot sweep prompt, e.g.:
  - `SNAPSHOT SWEEP – apply retention`
- Confirm:
  - Older/excess snapshots are **moved** into `Backups/Archives/` (if your server implements that behavior).
  - `Backup-Log.md` records a sweep summary with counts and any `#review-needed` recommendations.
  - No snapshots are deleted unless you explicitly ask for that in a prompt and implement such behavior in the MCP layer.

### 5. Performance spot-check

- Run a small ingest batch (e.g., 5–10 notes) both:
  - With snapshots enabled (current setup), and
  - Temporarily skipping `obsidian-snapshot` calls (by manually not triggering pipelines or by testing in a copy where you comment those references).
- Roughly time each run and fill in the performance table in `2026-02-25-enhanced-snapshots.md` to see overhead and decide if you want to tune batch frequencies.

If you’d like, next we can add more concrete Dataview examples for `Restore Hub.md` and a small example note in `Backups/Per-Change/` to serve as a reference snapshot template.

## Review Needed
Proposed para-type: project. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.