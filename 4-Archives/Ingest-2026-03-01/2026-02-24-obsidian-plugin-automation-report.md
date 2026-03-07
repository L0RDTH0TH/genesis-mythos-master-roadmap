---
title: Obsidian Plugin Automation Report — Autonomous Second Brain
created: 2026-02-24
tags: [pkm, obsidian, plugins, automation, para-zettelkasten, mcp]
para-type: resource
status: active
links: ["[[Resources Hub]]"]
confidence: 70%
---
# Obsidian Plugin Automation Report

**Goal:** Post-capture autonomy — manual capture only; pipelines handle Organize, Distill, and Express (e.g. full-autonomous-ingest: backup → classify → split → distill → frontmatter/tags → hub append → move → log).

**Scope:** Config files under `.obsidian/plugins/[plugin-id]/data.json` (and related). Focus: auto-triggers, MCP integration, reduced tag reliance (frontmatter/Dataview/tasks/callouts), Highlightr for distill, periodic/conditional automation.

**Sources:** Vault plugin configs, `3-Resources/Cursor-Project-Rules-Summary.md`, `Templates/AI Prompts.md`, `Untitled.md` (pipeline table), `3-Resources/2026-02-24-cursor-ingest-pipeline-trigger-prompt.md`, MCP para-zettel-autopilot tools.

---

## 1. Templater

**Config path:** `.obsidian/plugins/templater-obsidian/data.json`

### Current config summary

- **Trigger on file creation:** `trigger_on_file_creation: true` ✅
- **Folder templates:** Ingest → `Templates/Ingest-Selector.md`; Ingest/Mobile-Questions → `Templates/Mobile-AI-Question.md`; 1-Projects, 2-Areas, 3-Resources → respective templates
- **Startup templates:** `[]` (none)
- **Folder templates enabled:** `true`
- **File templates:** disabled; regex `.*` with empty template
- **User scripts folder:** empty
- **System commands:** disabled

### Automation alignment gaps

- No **startup template** to trigger a “vault ready / sweep” check or to preload MCP-related state.
- No **auto-run on note load** (Templater does not support “on open” natively; would need QuickAdd + Templater chain).
- Ingest folder correctly triggers **Ingest-Selector** (template picker), but there is no automatic “run full ingest pipeline” from inside Obsidian — that is triggered by Cursor/MCP via launch phrases (“INGEST MODE”, “Process Ingest/ with autopilot”).
- **User scripts folder** empty — no Templater scripts yet for periodic sweeps (e.g. archive, distill batch).

### Recommended changes

1. **Add a startup template** (optional) for daily/session prep (e.g. ensure Ingest-Log.md exists, append session header). Only if you want in-app automation on Obsidian open.

   ```json
   "startup_templates": ["Templates/Daily-Session-Header.md"]
   ```

   Create `Templates/Daily-Session-Header.md` with minimal content (e.g. `## Session YYYY-MM-DD` appended to a designated log).

2. **Keep `trigger_on_file_creation` and folder templates as-is** — they already support “new note in Ingest/ → template selector” and PARA folder templates.

3. **Introduce a user scripts folder** for future sweep/archive scripts (Templater + Dataview JS):

   ```json
   "user_scripts_folder": "Templates/Scripts"
   ```

   Then add scripts (e.g. `archive-sweep.js`, `distill-batch.js`) that list notes by frontmatter/para-type and output proposed moves or log lines for MCP/Cursor to execute.

### Potential risks

- Startup template runs on every Obsidian launch; keep it lightweight to avoid slowing startup.
- User scripts that modify files should follow same safety as MCP (backup first, propose then execute); prefer “output list for Cursor” over direct move/delete in Templater.

---

## 2. QuickAdd

**Config path:** `.obsidian/plugins/quickadd/data.json`

### Current config summary

- **Choices:** `[]` — no macros/captures/templates configured.
- **Template folder path:** empty (Templater uses `Templates` from app settings).
- **Ribbon icon:** disabled.
- **Capture notification:** enabled.
- **Date aliases:** t, tm, yd, nw, nm, ny, lw, lm, ly.
- **AI:** providers (OpenAI, Gemini) present; no API keys in snippet (use secret storage).
- **Dev mode:** off.

### Automation alignment gaps

- No **QuickAdd choices** to run “Process Ingest”, “Archive sweep”, or “Distill batch” — so no one-click in-Obsidian trigger for pipelines that are currently Cursor/MCP-driven.
- No **macro** that chains: list Ingest → (optional) call Local REST API or paste a standard prompt for Cursor.
- No **capture** templates for consistent Ingest frontmatter (Templater handles creation; QuickAdd could add “Capture to Ingest with type” for mobile/shortcuts).

### Recommended changes

1. **Add a “Process Ingest” macro** that (a) opens or focuses a note with the canonical INGEST MODE prompt, or (b) appends a timestamped “Run ingest” line to Ingest-Log.md so you can trigger Cursor from that. No JSON change alone — create a QuickAdd Macro choice that runs a Templater template or inserts text.

2. **Optional: Template folder for QuickAdd** if you want QuickAdd-specific templates separate from Templater:
   ```json
   "templateFolderPath": "Templates/QuickAdd"
   ```

3. **Optional: “Capture to Ingest” capture** with fixed frontmatter (para-type: Ingest, status: ingest, tags: [ingest, raw-capture]) and folder `Ingest/` — complements Templater’s Ingest-Selector for quick capture without picking a subtype.

### Potential risks

- QuickAdd macros that run shell or API calls: ensure they don’t bypass backup-first; prefer “prepare for MCP” over direct vault moves.
- AI features: keep API keys in Obsidian secret storage, not in `data.json`.

---

## 3. Dataview

**Config path:** `.obsidian/plugins/dataview/data.json`

### Current config summary

- **Refresh:** enabled, interval 2500 ms.
- **Default date format:** `yyyy-MM-dd` (aligns with frontmatter).
- **Task completion:** not used for completion tracking (`taskCompletionTracking: false`).
- **Inline queries:** enabled (`inlineQueryPrefix: "="`, `enableInlineDataview: true`).
- **DataviewJS:** disabled (`enableDataviewJs: false`, `enableInlineDataviewJs: false`).
- **Warn on empty result:** true.
- **Pretty render inline fields:** true (live preview and reading).

### Automation alignment gaps

- **Hubs/MOCs:** Rules say “insert Dataview blocks (e.g. TABLE from para-type)” in hubs; no plugin config can “auto-insert” — that’s done by MCP/templates when creating or updating hub notes. Dataview’s role is to *evaluate* those blocks.
- **Tag reliance reduction:** Dataview can query by `para-type`, `status`, `created`, `file.folder` — no config change needed; hub templates and MCP should prefer frontmatter-based queries over tag-only.
- **Dynamic hubs:** Already supported by current settings; ensure hub notes use `TABLE ... FROM ... WHERE para-type = "Resource"` (etc.) and optional `WHERE contains(tags, "needs-distill")` for distill queue.
- **Tasks:** Task extraction (next-action-extract) is MCP/LLM; Obsidian Tasks plugin surfaces tasks in UI; Dataview can list tasks with `task` or `tasks` (if enabled). No need to enable Dataview task completion for your pipeline.

### Recommended changes

1. **Optional: Enable DataviewJS** if you want more complex hub logic (e.g. “notes with no `links`” or “stale resurface-date” for BASB):
   ```json
   "enableDataviewJs": true,
   "enableInlineDataviewJs": true
   ```
   Use sparingly; prefer simple DQL for maintainability.

2. **Keep refresh interval** at 2500 ms for responsive hubs; increase only if performance is an issue.

3. **Standardize hub snippets** (in templates or MCP append_to_hub logic), e.g.:
   - Resources Hub: `TABLE file.link AS "Note", para-type, status, created FROM "3-Resources" WHERE para-type = "Resource"`.
   - Projects: filter by `para-type = "Project"` and optional `deadline`.
   - Reduce tag-only queries in favor of `para-type`, `status`, `created`, `resurface-date`.

### Potential risks

- DataviewJS in many large notes can slow rendering; enable only where needed.
- Queries over whole vault without folder filter can be slow; scope by folder when possible.

---

## 4. Obsidian Tasks

**Config path:** `.obsidian/plugins/obsidian-tasks-plugin/data.json`

### Current config summary

- **Task format:** `dataview` (compatible with Dataview task queries).
- **Set done date:** true; **set cancelled date:** true; **set created date:** false.
- **Global filter:** empty; **remove global filter:** false.
- **Statuses:** Todo, Done, In Progress, Cancelled (core + custom).
- **Auto-suggest:** enabled (min match 0, max 20).
- **Filename as scheduled date:** off.

### Automation alignment gaps

- **Next-action extraction:** Pipeline doc mentions “next-action-extract” (task-like phrases → checklist). Tasks plugin doesn’t auto-create tasks from text; MCP/LLM does that and can write `- [ ]` or use `manage_frontmatter` for `next-actions`. Tasks plugin then surfaces them.
- **Archive sweep:** “No open tasks” as inactivity signal — Tasks plugin is the source of truth for task queries; no config change required for that logic.
- **Reducing tag reliance:** Prefer frontmatter (e.g. `priority`, `deadline`) and Tasks status; config already supports standard statuses.

### Recommended changes

1. **Optional: Set created date** for new tasks so “inactivity” and “created” are consistent:
   ```json
   "setCreatedDate": true
   ```

2. **Keep global filter empty** unless you need to restrict tasks to a specific tag (you’re reducing tag reliance, so leave empty).

3. **Use in hubs:** In Resources/Projects Hub, you can add a Dataview block that uses Tasks (e.g. `tasks` from a folder) so that “action extraction” from distill shows up in a single view.

### Potential risks

- Enabling `setCreatedDate` can change behavior for existing tasks (only for new ones if plugin respects it).

---

## 5. Local REST API

**Config path:** `.obsidian/plugins/obsidian-local-rest-api/data.json`

### Current config summary

- **Secure server:** enabled (HTTPS).
- **Insecure server:** enabled; **insecure port:** 27122; **port:** 27124 (secure).
- **API key:** set (long hex string — store in env for MCP; do not commit).
- **Crypto:** cert and keys present for HTTPS.

### Automation alignment gaps

- **MCP integration:** Cursor uses the **Obsidian MCP server** (para-zettel-autopilot) which talks to the vault via its own integration (file system / Obsidian API), not necessarily HTTP. Local REST API is an *alternative* way for external tools (e.g. cron, another server) to append/create notes, search, or update — e.g. `PUT /vault/` (create/overwrite), `PATCH` (append), or similar endpoints.
- **obsidian_append_to_hub / obsidian_update_note:** If MCP uses file I/O, Local REST API is redundant for Cursor. If you want **non-Cursor** automation (e.g. iOS Shortcuts, Zapier, or a small script), Local REST API is the right integration point; then “MCP” in that case means “external process calling REST API” with the same backup-first discipline (script must create backup before destructive calls).
- **API key security:** Config contains API key and certs; recommend moving key to env (e.g. `OBSIDIAN_API_KEY`) and referencing in scripts; avoid committing `data.json` with key.

### Recommended changes

1. **Keep both servers enabled** if you use external automation (e.g. mobile, cron). For Cursor-only pipelines, MCP para-zettel-autopilot may not need REST; document when to use which (Cursor → MCP; Shortcuts/cron → Local REST API).

2. **Document base URL and key for scripts:** e.g. `https://localhost:27124` (or insecure `http://localhost:27122`) and header `Authorization: Bearer <apiKey>`. Use env var for key in any script.

3. **Endpoints to align with MCP-style operations:** Typically:
   - Create/overwrite note ≈ `PUT /vault/<path>` (or equivalent in the plugin’s API).
   - Append to note ≈ PATCH or dedicated append endpoint.
   - Search / list — use plugin’s search or list endpoints.
   Reference the [official API docs](https://coddingtonbear.github.io/obsidian-local-rest-api/) for exact paths and body format.

### Potential risks

- **Exposing API key:** Do not paste `data.json` with key into shared docs; use “apiKey is set” and “load from env”.
- **HTTPS on localhost:** Browsers/scripts may need to allow self-signed cert; insecure port is easier for local scripts but avoid on untrusted networks.

---

## 6. Highlightr

**Config path:** `.obsidian/plugins/highlightr-plugin/data.json`

### Current config summary

- **Style:** `realistic`; **method:** `inline-styles`.
- **Colors:** Pink, Red, Orange, Yellow, Green, Cyan, Blue, Purple, Grey (hex with alpha, e.g. `#FFB8EBA6`).
- **Order:** Pink, Red, Orange, Yellow, Green, Cyan, Blue, Purple, Grey.

### Automation alignment gaps

- **Distill-highlight-color skill:** Pipeline says “apply color-coded highlights (e.g. red = key concepts, blue = quotes, green = actions)”. Highlightr stores colors in config; the **application** is done by MCP/LLM (e.g. `obsidian_search_replace` or `obsidian_update_note`) inserting Highlightr’s Markdown (e.g. `==highlight==` or the plugin’s chosen syntax). Plugin does not “auto-apply on save” by default — no such option in config.
- **Auto-apply in distill pipelines:** “Auto-apply” here means “MCP pipeline step after distill_note”: read note, decide spans to highlight and color key (e.g. key terms → red, quotes → blue), then write back with Highlightr-compatible markup. No plugin config change for that; ensure MCP/LLM uses the same syntax Highlightr expects (inline-styles → likely `<mark>` or `==text==`; check plugin docs).

### Recommended changes

1. **Document color semantics for MCP** in a small vault note (e.g. `3-Resources/Highlightr-Color-Key.md`): e.g. Red = key concepts, Blue = quotes/sources, Green = actions/dates. Then distill-highlight-color skill can reference that.

2. **No mandatory config change.** Optional: add a “Distill” preset order (e.g. Red, Blue, Green first) in `highlighterOrder` if you want consistent palette order in menus:
   ```json
   "highlighterOrder": ["Red", "Blue", "Green", "Orange", "Yellow", "Cyan", "Pink", "Purple", "Grey"]
   ```

3. **Verify syntax:** Confirm with Highlightr docs whether it uses `==text==`, `<mark class="...">`, or other; then ensure MCP `obsidian_update_note` / `obsidian_search_replace` output that format.

### Potential risks

- Inline styles can differ between Reading/Live Preview; test in both. Large in-place replacements need backup-first (already in pipeline).

---

## 7. Advanced Exclude

**Config path:** `.obsidian/plugins/advanced-exclude/data.json`

### Current config summary

- **Exclude mode:** Full.
- **Obsidian ignore content:** `"\n"` (effectively empty or newline).
- **Should ignore excluded files:** false.
- **Include .gitignore patterns:** true.

### Automation alignment gaps

- **Search and graph:** Excluded files won’t appear in Obsidian search/graph; MCP that uses vault search or list may still see them depending on implementation. For autonomy, you may want to exclude backup folders, `Archives/Eaten`, or temp folders from global search so that “list Ingest” and “list 3-Resources” aren’t cluttered — align exclude patterns with PARA and backup paths.
- **No auto-trigger** — this is a filter only.

### Recommended changes

1. **Optional: Add patterns** so that MCP list/search don’t return noisy paths (e.g. `*.backup`, `Archives/Eaten` if you want them hidden from some flows). Configure via Obsidian UI (Advanced Exclude) and the content will be stored in `obsidianIgnoreContent` or similar; document the patterns in a vault note.

2. **Consider `shouldIgnoreExcludedFiles: true`** if you want search and backlinks to fully skip excluded files; false means they’re only excluded from graph/some views.

### Potential risks

- Excluding too much can hide notes that should be in “archive sweep” or “distill batch”; keep Ingest, 1–4 folders, and key Resources in scope.

---

## 8. BRAT

**Config path:** `.obsidian/plugins/obsidian42-brat/data.json`

### Current config summary

- **Plugin list:** `["mnaoumov/obsidian-advanced-exclude"]`.
- **Update at startup:** true; **enable after install:** true.
- **Logging:** disabled; **notifications:** enabled.
- **No global token**; **allow incompatible plugins:** false.

### Automation alignment gaps

- BRAT is for installing plugins from GitHub (e.g. beta); no role in ingest/distill/archive pipelines. No config changes needed for autonomy.

### Recommended changes

- None for automation report. Keep as-is for plugin updates.

### Potential risks

- None for pipeline automation.

---

## 9. Overall recommendations

### Cross-plugin integrations

1. **QuickAdd → Templater → Dataview**
   - **QuickAdd macro “Process Ingest”:** Runs a Templater template that (a) inserts the canonical INGEST MODE prompt into the active note or (b) appends “Trigger: Process Ingest – YYYY-MM-DD HH:mm” to Ingest-Log.md. You then run Cursor with “Process Ingest/ with autopilot” or use the log as a trigger.
   - **Templater:** Keeps handling new file creation (Ingest → Ingest-Selector; PARA folders → templates). Add optional `Templates/Scripts` for sweep scripts that output lists for Cursor/MCP.
   - **Dataview:** Hubs/MOCs use DQL TABLE/LIST by `para-type`, `status`, `file.folder`; Dataview evaluates when you open the hub. MCP append_to_hub should insert these blocks when creating/updating hubs.

2. **Full-autonomous-ingest (Cursor/MCP)**
   - Trigger: “INGEST MODE – safe batch autopilot” or “Process Ingest/ with autopilot.”
   - No Obsidian plugin “auto-runs” this; Templater only ensures new files in Ingest get a template. The pipeline runs in Cursor with para-zettel-autopilot MCP (create_backup → classify → split → distill → frontmatter/tags → append_to_hub → move → log).

3. **Autonomous-distill**
   - **Highlightr:** MCP step “distill-highlight-color” after distill_note: apply highlights per color key (documented in vault). No plugin auto-trigger.
   - **Periodic:** Use a QuickAdd macro or Templater startup script that writes “Distill batch: YYYY-MM-DD” to Ingest-Log.md; then run Cursor with “distill notes with status needs-distill” or similar.

4. **Autonomous-archive**
   - **Periodic sweep:** Templater script or QuickAdd macro that (e.g. weekly) creates a note `Archive-Sweep-YYYY-MM-DD.md` with a Dataview list of candidates (e.g. `para-type = "Project" AND status = "complete"` or “no tasks in last 30d”); you run Cursor to execute moves with backup-first.

5. **Autonomous-express**
   - Read-only first (read_note, generate ideas); append only at ≥85%. Local REST API or MCP can append to Express-Hub; no plugin config change.

### Reduce tag reliance

- **Prefer in frontmatter:** `para-type`, `status`, `created`, `resurface-date`, `priority`, `deadline`.
- **Dataview:** Query by `para-type`, `status`, `file.folder`; use tags only when necessary (e.g. `#review-needed`).
- **Tasks:** Use Tasks plugin status and optional frontmatter `next-actions`; Dataview can list tasks from folders.
- **Callouts/canvases:** Use in templates and distill output; no plugin config change.

---

## 10. Test plan

1. **Full-autonomous-ingest**
   - **Setup:** Ensure Ingest/ exists; Obsidian closed or idle (no conflict on file writes).
   - **Step 1:** Create a test note in Ingest/ (e.g. `Ingest/Test-Autonomous-Ingest.md`) with minimal content and frontmatter `para-type: Ingest`, `status: ingest`.
   - **Step 2:** In Cursor, run: “INGEST MODE – safe batch autopilot” or “Process Ingest/ with autopilot.”
   - **Verify:** (a) create_backup runs first; (b) classify_para → distill → frontmatter → append_to_hub → move_note (if ≥85%) and log_action; (c) Ingest-Log.md has one line per note with Backup path, Confidence, Proposed MV or final path; (d) note moved to 1–4 or 3-Resources and linked from relevant hub.

2. **Templater on create**
   - **Setup:** Templater folder template for Ingest → Ingest-Selector.md.
   - **Step:** Create new note in Ingest/ from Obsidian (e.g. right-click Ingest → New note).
   - **Verify:** Templater runs; Ingest-Selector template (or picker) appears; new note has expected frontmatter/structure.

3. **Dataview hubs**
   - **Setup:** Open Resources Hub (or a MOC) that contains a TABLE query by `para-type` or `file.folder`.
   - **Verify:** Dataview shows correct rows; after ingest, newly moved note appears in the right hub/MOC.

4. **Highlightr + distill**
   - **Setup:** Run ingest on a note that includes a quote and a key concept.
   - **Verify:** After distill_note, a follow-up step (or same run) applies Highlightr-style highlights (e.g. red for concept, blue for quote); note content uses the same syntax as Highlightr (e.g. `==...==` or plugin’s format).

5. **Local REST API (optional)**
   - **Setup:** From another terminal/script, call `GET` on base URL with API key to list or search.
   - **Verify:** Response matches expected format; then try append/create with backup taken first (e.g. via Cursor or manual copy).

6. **Archive sweep (manual trigger)**
   - **Setup:** Create a note in 2-Areas or 1-Projects with `status: complete` or no open tasks.
   - **Step:** In Cursor, “Run archive sweep” or “Propose archive for completed notes.”
   - **Verify:** Proposals in Ingest-Log.md; no move without confirmation (or auto at ≥85% if you enable that in rules).

---

## 11. If configs are missing

- **Templater:** If `data.json` were missing, Obsidian would recreate defaults; re-add `templates_folder`, `trigger_on_file_creation`, `folder_templates` and `enable_folder_templates` as in current config.
- **QuickAdd:** Default is empty choices; add macros/captures via UI then copy resulting `data.json` for backup.
- **Dataview:** Defaults are fine; set `defaultDateFormat` to `yyyy-MM-dd` and enable refresh.
- **Tasks:** Default statuses are sufficient; set `taskFormat` to `dataview` for compatibility.
- **Local REST API:** If missing, re-enable plugin and set port; regenerate API key and store in env.
- **Highlightr:** Default colors are sufficient; document color key in vault for MCP.

---

*Report generated for autonomous Second Brain (PARA-Zettelkasten + MCP). Apply JSON changes with Obsidian closed or backup `.obsidian/plugins` first.*

## Why resource?
Assigned based on content/frontmatter (confidence ~70%).

## Review Needed
Proposed para-type: resource. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.