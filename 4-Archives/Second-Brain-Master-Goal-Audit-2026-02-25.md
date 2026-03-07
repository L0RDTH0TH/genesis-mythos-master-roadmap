---
title: Second Brain Master Goal — Production Audit
created: 2026-02-25
tags: [pkm, audit, second-brain, para, cursor, mcp]
para-type: Resource
status: active
links: [[Resources Hub]], [[Cursor-Skill-Pipelines-Reference]], [[Second-Brain-Config]]
---

# Second Brain Master Goal — Full Audit

**Reference:** Master Goal (verbatim) — *Building a fully autonomous, post-capture Second Brain in Obsidian using PARA + Zettelkasten, where capture is the only manual step; everything after that happens automatically via Cursor + MCP pipelines whenever the user says "INGEST MODE", "Process Ingest", or when new notes land in Ingest/; high-confidence (≥85%) execution, backup-first, and Highlightr as a relational visual language.*

**Audit date:** 2026-02-25. **Scope:** Entire codebase and Obsidian vault configuration in this Cursor workspace.

**Post-refinement update:** This audit was updated after implementation of the [Second Brain Post-Audit Refinement Plan](.cursor/plans/second_brain_post-audit_refinement_07264231.plan.md). Phase 1–3 changes are reflected below: Highlightr format alignment, always-ingest-bootstrap rule, central config, project-MOC transition, links array, auto-layer-select, graph hints, dashboard graph health, and tag vs frontmatter policy. Overall alignment score and gap heatmap have been revised accordingly. Watcher ("when notes land") remains Phase 4 (on hold).

---

## 1. Project structure (explored)

| Area | Location | Notes |
|------|----------|--------|
| **Cursor rules** | `.cursor/rules/` | `always/mcp-obsidian-integration.mdc`, **`always/always-ingest-bootstrap.mdc`**; context: `para-zettel-autopilot`, `auto-organize`, `auto-distill`, `auto-archive`, `auto-express`, `auto-restore`, `auto-resurface`, `snapshot-sweep` |
| **Skills** | `.cursor/skills/<name>/SKILL.md` | 17 skills (+ **auto-layer-select**); frontmatter-enrich, subfolder-organize, split-link-preserve, distill-highlight-color, next-action-extract, layer-promote, callout-tldr-wrap, readability-flag, archive-check, resurface-candidate-mark, summary-preserve, call-to-action-append, version-snapshot, express-mini-outline, related-content-pull, obsidian-snapshot |
| **Sync** | `.cursor/sync/` | Mirrors of rules/skills (e.g. `.md`) |
| **Plans** | `.cursor/plans/*.plan.md` | highlight_consistency_audit, visual_health_dashboard, auto-pipelines-rules-and-quickadd, enhanced-snapshots, etc. |
| **Scripts** | `scripts/quickadd/` | `ingest-batch.js`, `run-ingest.js`, `distill-current.js`, `express-current.js`; README documents macros |
| **Templates** | `Templates/` | `AI Prompts.md`, `Session-Prep.md`, `ProcessIngestTrigger.js`, project/daily/weekly |
| **Ingest** | `Ingest/` | 8 items (Master Goal.md, Obsidian Second Brain Audit.md, .md reports, Untitled Document 1/2) |
| **PARA** | `1-Projects/`, `2-Areas/`, `3-Resources/`, `4-Archives/` | Present; Test-Project, Test-Project-Archive, hubs in root |
| **Backups** | `Backups/Per-Change/`, `Backups/Batch/` | In-vault snapshots; external BACKUP_DIR per MCP env |
| **Config** | `.obsidian/` | community-plugins (QuickAdd, Templater, Dataview, etc.), workspace, appearance |
| **MCP descriptors** | `~/.cursor/projects/.../mcps/user-obsidian-para-zettel-autopilot/tools/*.json` | create_backup, classify_para, split_atomic, distill_note, append_to_hub, move_note, ensure_structure, update_note, etc. |
| **Dataview** | `3-Resources/_dv-visual-health-dashboard.js`, `*.md` with `dataview` blocks | Visual-Health-Dashboard.md, Resources Hub, Resurface.md, PARA-Dashboard.md |
| **Highlightr** | `3-Resources/Highlightr-Color-Key.md` | Single source of truth; inline CSS format; project `highlight_key` overrides; **Legacy format** subsection (deprecated `==...==^{Color}`) |
| **Central config** | `3-Resources/Second-Brain-Config.md` | **Single source of truth**: hub_names, archive (age_days, no_activity_days), highlight default_key, graph moc_strength; links array + tags vs frontmatter policy |
| **MCP descriptions** | `3-Resources/MCP-Descriptor-Descriptions.md` | Suggested descriptions for classify_para, split_atomic, append_to_hub (for server or project mcps) |
| **Pipeline reference** | `3-Resources/Cursor-Skill-Pipelines-Reference.md` | Canonical pipeline order, confidence gates, snapshot triggers, trigger→rule mapping; footnote to always-ingest-bootstrap |
| **Logs** | `Ingest-Log.md`, `3-Resources/*-Log.md`, `3-Resources/Backup-Log.md` | Ingest, Distill, Archive, Express, Organize, Backup |

---

## 2. Per-requirement evaluation

### 2.1 Trigger mechanisms ("INGEST MODE", "Process Ingest", filesystem watcher on Ingest/)

| Item | Current implementation | Alignment | Strengths | Gaps / risks | Risk |
|------|------------------------|-----------|-----------|--------------|------|
| **Phrase triggers** | **✅** `.cursor/rules/always/always-ingest-bootstrap.mdc` exists: when user says "INGEST MODE", "Process Ingest", or "run ingests", ensures para-zettel-autopilot + mcp-obsidian-integration apply; lists Ingest via `obsidian_list_notes` and runs full-autonomous-ingest per pipeline reference. Pipeline reference trigger table points to this rule. | **95%** | Clear canonical phrases; always-ingest-bootstrap + para-zettel + MCP rule chain; no documentation gap. | — | Low |
| **Process Ingest** | QuickAdd `data.json` has "Ingest Batch" and "Run Ingest" macros; scripts append to `Ingest-Log.md` ("INGEST MODE – safe batch autopilot" / "execute now"). `Templates/Scripts/ProcessIngestTrigger.js` appends trigger block to Ingest-Log. | **90%** | One-click in Obsidian adds log line; user then opens Cursor and runs pipeline. | Scripts do not invoke Cursor or run the pipeline; they only append to log. "Process Ingest" is therefore "append reminder → user runs Cursor manually". | Low |
| **Filesystem watcher on Ingest/** | **None.** Session-Prep (Templater) runs on Obsidian load and appends a session line to Ingest-Log *if* Ingest has .md files ("Say in Cursor: INGEST MODE…"). No daemon or watcher that runs when new files land. | **30%** | Session-Prep gives a reminder on startup. | Master Goal says "when new notes land in Ingest/" — **no automatic trigger**. No background watcher, no Cursor auto-launch, no Obsidian→Cursor bridge on file create. | Med |

**Relevant code/files:**
- `.cursor/rules/always/always-ingest-bootstrap.mdc` — ensures para-zettel-autopilot + MCP rule apply on INGEST MODE / Process Ingest; list Ingest, run full-autonomous-ingest.
- `.cursor/rules/context/para-zettel-autopilot.mdc` (globs: `Ingest/*.md`) — applies when Ingest note is open.
- `3-Resources/Cursor-Skill-Pipelines-Reference.md` (trigger table + footnote to always-ingest-bootstrap).
- `scripts/quickadd/ingest-batch.js`, `run-ingest.js`; `.obsidian/plugins/quickadd/data.json`.
- `Templates/Session-Prep.md` (Templater: append reminder on load).

---

### 2.2 Full post-capture autonomy (zero manual steps after capture)

| Item | Current implementation | Alignment | Strengths | Gaps / risks | Risk |
|------|------------------------|-----------|-----------|--------------|------|
| **Zero manual after capture** | Once user runs Cursor with "INGEST MODE" or "Process Ingest" (or opens an Ingest note and triggers the pipeline), the **full chain** runs per pipeline reference: backup → classify → frontmatter-enrich → subfolder-organize → split_atomic → split-link-preserve → distill → distill-highlight-color → next-action-extract → append_to_hub → move_note → log. No per-step confirmations at ≥85%. | **80%** | Single prompt runs full pipeline; confidence gates and backup/snapshot are enforced; no "wait for ok" in AI Prompts. | (1) User must **manually** open Cursor and say the phrase (or run QuickAdd then Cursor). (2) "When new notes land" is not automated. So autonomy is **after** the user triggers, not from file drop alone. | Med |

**Relevant code/files:**
- `Templates/AI Prompts.md` — "No 'wait for ok' or interactive confirmation loops — decide and act (or flag) immediately."
- `.cursor/rules/context/para-zettel-autopilot.mdc` — batch isolation, backup/snapshot, confidence.

---

### 2.3 PARA organization + intelligent subfolder creation (up to 4 levels deep)

| Item | Current implementation | Alignment | Strengths | Gaps / risks | Risk |
|------|------------------------|-----------|-----------|--------------|------|
| **PARA roots** | `1-Projects`, `2-Areas`, `3-Resources`, `4-Archives`; MCP `obsidian_ensure_structure` creates top-level PARA + Ingest, etc. | **95%** | Consistent naming and rule/skill references. | — | Low |
| **Subfolder creation (≤4 levels)** | **subfolder-organize** skill: builds path `{para-root}/{ProjectOrAreaName?}/{IdeaClusterOrSubtheme?}/{YYYY-MM-DD-title}.md`; max 4 path segments. For deep moves, rule and skill require `obsidian_ensure_structure` with **folder_path** set to target parent; documented in `mcp-obsidian-integration.mdc` and `Second-Brain-Limitations.md` (verified 2026-02-25). Project MCP descriptor includes `folder_path` in schema; vault doc `3-Resources/MCP-Descriptor-Descriptions.md` documents ensure_structure behavior. | **92%** | Logic is clear; deep-move behavior verified and documented; folder_path in descriptor or documented. | — | Low |

**Relevant code/files:**
- `.cursor/skills/subfolder-organize/SKILL.md` (path pattern, ensure_structure, move_note).
- `.cursor/rules/always/mcp-obsidian-integration.mdc` (fallback table, "Documented behavior" — deep nested PARA).
- `3-Resources/Second-Brain-Limitations.md` (ensure_structure + folder_path).

---

### 2.4 Atomic note splitting

| Item | Current implementation | Alignment | Strengths | Gaps / risks | Risk |
|------|------------------------|-----------|-----------|--------------|------|
| **Split** | MCP `obsidian_split_atomic` (path, split_on e.g. `## `); pipeline runs it when multi-idea. **split-link-preserve** skill: after split, sets `split_from` on children, appends `## Splits` on parent with bullets and optional `split_into` for Dataview. **✅** Suggested description in `3-Resources/MCP-Descriptor-Descriptions.md` for server/repo. | **90%** | Atomic split + traceability; idempotent; backlinks; descriptor text documented in vault. | Server descriptor may still be empty until applied in repo. | Low |

**Relevant code/files:**
- `.cursor/rules/always/mcp-obsidian-integration.mdc` (destructive steps include split_atomic; snapshot before).
- `.cursor/skills/split-link-preserve/SKILL.md`.
- `3-Resources/Cursor-Skill-Pipelines-Reference.md` (pipeline order, split-link-preserve slot).

---

### 2.5 Progressive distillation pipeline

| Item | Current implementation | Alignment | Strengths | Gaps / risks | Risk |
|------|------------------------|-----------|-----------|--------------|------|
| **Distill** | MCP `obsidian_distill_note` (path, add_tldr); then skills: **distill-highlight-color** → **layer-promote** → **callout-tldr-wrap** → **readability-flag**. **✅** Optional **auto-layer-select** skill (content complexity → 1/2/3 layers); referenced in auto-distill.mdc and pipeline reference. Autonomous-distill: backup → (auto-layer-select when enabled) → distill layers → distill-highlight-color → layer-promote → callout-tldr-wrap → readability-flag; per-change snapshot before first structural rewrite; batch checkpoint ~every 3 notes. | **92%** | Full layer chain; optional layer autonomy; confidence and snapshot triggers defined. | Distill_note tool descriptor does not specify "progressive layers"; layer-promote and readability are skill-driven. | Low |

**Relevant code/files:**
- `.cursor/rules/context/auto-distill.mdc` (optional auto-layer-select step).
- `3-Resources/Cursor-Skill-Pipelines-Reference.md` (§2 autonomous-distill, auto-layer-select).
- `.cursor/skills/auto-layer-select/SKILL.md`, `.cursor/skills/distill-highlight-color/SKILL.md`, `layer-promote/SKILL.md`, `callout-tldr-wrap/SKILL.md`, `readability-flag/SKILL.md`.

---

### 2.6 Highlightr color system as relational visual language (analogous/complementary/project overrides, cross-project)

| Item | Current implementation | Alignment | Strengths | Gaps / risks | Risk |
|------|------------------------|-----------|-----------|--------------|------|
| **Semantic mapping** | `3-Resources/Highlightr-Color-Key.md`: semantic table (Yellow/Green/Blue/Red/Orange/Purple/Pink/Cyan/Grey); **exact storage format**: inline CSS only (e.g. `<mark style="background: #C1E1C1A6;">text</mark>`); **forbidden**: `==text==`, `^{Color}`. | **85%** | Single source of truth; project `highlight_key` overrides; color theory (analogous/complementary) in key and in distill-highlight-color skill. | — | Low |
| **Pipeline usage** | **distill-highlight-color**: uses master key + project highlight_key; analogous for related ideas, complementary for contrasts. **layer-promote**: complementary for conflicting ideas. | **85%** | Skills reference color key and apply via search_replace/update_note. | — | Low |
| **Format consistency** | **✅ Addressed.** (1) **express-mini-outline** SKILL now specifies inline CSS only (e.g. `<mark style="background: #A3D8FFA6;">Section A</mark>`) and "Never use `==text==` or `^{Color}`". (2) **Visual Health Dashboard** `_dv-visual-health-dashboard.js` counts **both** inline CSS (`<mark style="background: #...">` → hexToColor map) and legacy `^{Color}`; combined count per note. (3) **Highlightr-Color-Key.md** has "Legacy format" subsection: `==text==^{Color}` deprecated; pipeline uses inline CSS only; existing notes may be migrated or left until next edit. Some test notes may still contain legacy format (optional migration). | **88%** | Single canonical format; skill and dashboard aligned; legacy documented and supported during migration. | Optional one-time migration of Test-Project/Ingest notes with legacy format. | Low |

**Relevant code/files:**
- `3-Resources/Highlightr-Color-Key.md` (Section 1 semantics, Section 2 format, **Legacy format** subsection, project guidelines).
- `.cursor/skills/distill-highlight-color/SKILL.md`, `.cursor/skills/layer-promote/SKILL.md`.
- `.cursor/skills/express-mini-outline/SKILL.md` (inline CSS only, no `==...==^{Color}`).
- `3-Resources/_dv-visual-health-dashboard.js` (hexToColor map, getInlineHexes, hasLegacyColor; combined counts).
- `1-Projects/Test-Project/2026-02-25-distill-messy.md` (may still contain legacy; documented as acceptable until migration).

---

### 2.7 Frontmatter enrichment (all required keys, dynamic population)

| Item | Current implementation | Alignment | Strengths | Gaps / risks | Risk |
|------|------------------------|-----------|-----------|--------------|------|
| **Required keys** | **frontmatter-enrich** skill: status, confidence, para-type, created, **links as YAML array** (e.g. `["[[Resources Hub]]", "[[Project X]]"]`); optional project-id, priority, deadline, resurface-date. **✅** When `project-id` set, adds `[[ProjectName MOC]]` to links. Value format: always array; Dataview use `contains(links, "[[HubName]]")`. Uses `obsidian_manage_frontmatter`. | **92%** | Clear list; links standardised; project-MOC link when project-id set; applied after classify_para in ingest and organize. | — | Low |

**Relevant code/files:**
- `.cursor/skills/frontmatter-enrich/SKILL.md` (links array, project MOC).
- `3-Resources/Second-Brain-Config.md` (links frontmatter note).
- `3-Resources/Cursor-Skill-Pipelines-Reference.md` (frontmatter-enrich slot).

---

### 2.8 Hub / MOC linking

| Item | Current implementation | Alignment | Strengths | Gaps / risks | Risk |
|------|------------------------|-----------|-----------|--------------|------|
| **Append to hub** | MCP `obsidian_append_to_hub` (hub_name, wikilink, summary). Pipeline: after move, append to relevant hub. **✅** Hub names in **`3-Resources/Second-Brain-Config.md`** (hub_names: projects, areas, resources, resurface); resurface-candidate-mark and skills prefer config. **✅** Notes with `project-id` get `[[ProjectName MOC]]` in links (frontmatter-enrich); project MOCs linked into hubs; documented in Ingest/Master Goal.md (Organization). | **90%** | Tool and pipeline step present; central config for hub names; project-MOC transition started; hub notes exist with Dataview LIST/TABLE. | — | Low |

**Relevant code/files:**
- `mcps/.../tools/obsidian_append_to_hub.json`; `3-Resources/MCP-Descriptor-Descriptions.md` (suggested description).
- `.cursor/rules/always/mcp-obsidian-integration.mdc` (chain includes append_to_hub).
- `3-Resources/Second-Brain-Config.md` (hub_names); `.cursor/skills/frontmatter-enrich/SKILL.md` (project MOC); `.cursor/skills/resurface-candidate-mark/SKILL.md` (config).
- `Resources Hub.md`, `Resurface.md`, `PARA-Dashboard.md`; `Ingest/Master Goal.md` (Organization).

---

### 2.9 Action extraction + task list handling

| Item | Current implementation | Alignment | Strengths | Gaps / risks | Risk |
|------|------------------------|-----------|-----------|--------------|------|
| **Tasks** | **next-action-extract** skill: parse task-like phrases → checklists `- [ ]` in body and `next-actions` in frontmatter (JSON array string or comma-separated for Dataview). Confidence ≥85%. **✅** When `project-id` exists, **project-specific highlight color for action blocks is required** (from highlight_key or Highlightr-Color-Key); inline CSS only. | **92%** | Clear instructions; backup before edits; format documented; project colors mandated when project-id set. | — | Low |

**Relevant code/files:**
- `.cursor/skills/next-action-extract/SKILL.md`.
- `3-Resources/Visual-Health-Dashboard.md` (LIST for next-actions, needs-simplify, resurface-candidate).
- `3-Resources/_dv-visual-health-dashboard.js` (hasNextActions, counts).

---

### 2.10 Archiving logic

| Item | Current implementation | Alignment | Strengths | Gaps / risks | Risk |
|------|------------------------|-----------|-----------|--------------|------|
| **Archive pipeline** | **autonomous-archive**: backup → classify_para → **archive-check** (no open tasks, status complete, age threshold; ≥85% for move) → **subfolder-organize** (archive path) → **resurface-candidate-mark** → **summary-preserve** → obsidian_move_note → log. **✅** archive-check reads age threshold from **Second-Brain-Config.md** (archive.age_days / no_activity_days) if available; else default 90/60. Per-change snapshot after archive-check (≥85%) before subfolder-organize/summary-preserve/move. | **94%** | Full sequence; safety invariants; central config for archive thresholds. | — | Low |

**Relevant code/files:**
- `.cursor/rules/context/auto-archive.mdc`.
- `.cursor/skills/archive-check/SKILL.md`, `subfolder-organize/SKILL.md`, `resurface-candidate-mark/SKILL.md`, `summary-preserve/SKILL.md`.
- `3-Resources/Cursor-Skill-Pipelines-Reference.md` (§3 autonomous-archive).

---

### 2.11 Resurfacing candidates logic

| Item | Current implementation | Alignment | Strengths | Gaps / risks | Risk |
|------|------------------------|-----------|-----------|--------------|------|
| **Mark** | **resurface-candidate-mark** (in archive pipeline): set `resurface-candidate: true`; optional append to Resurface hub; ≥75%. **✅** Hub names prefer **Second-Brain-Config.md** hub_names; fallback to "Resurface", "Projects Hub", etc. | **92%** | Skill and pipeline slot defined; Resurface.md has Dataview TABLE; hub names from config. | — | Low |
| **Surface** | **auto-resurface** rule (globs: Resurface.md): on "resurface" / "show resurface candidates" or open Resurface — list via global_search or Dataview; optionally append list to Resurface. | **85%** | Trigger-based; no cron; aligns with manual curation. | — | Low |

**Relevant code/files:**
- `.cursor/skills/resurface-candidate-mark/SKILL.md`.
- `.cursor/rules/context/auto-resurface.mdc`.
- `Resurface.md` (Dataview block, manual links).

---

### 2.12 Early express/output generation

| Item | Current implementation | Alignment | Strengths | Gaps / risks | Risk |
|------|------------------------|-----------|-----------|--------------|------|
| **Express pipeline** | **autonomous-express**: backup → **version-snapshot** (Versions/ slug--timestamp.md, mode: "create") → **related-content-pull** → **express-mini-outline** → **call-to-action-append**; log to Express-Log and Backup-Log. **✅** express-mini-outline uses inline CSS only (no deprecated format). **✅** Rule includes optional graph frontmatter from project color. Triggers: "EXPRESS MODE", "express this note", etc. | **92%** | Version snapshot before appends; related content + outline + CTA; highlight format aligned; graph hint. | — | Low |

**Relevant code/files:**
- `.cursor/rules/context/auto-express.mdc` (graph frontmatter bullet).
- `.cursor/skills/version-snapshot/SKILL.md`, `related-content-pull/SKILL.md`, `express-mini-outline/SKILL.md` (inline CSS only), `call-to-action-append/SKILL.md`.
- `3-Resources/Cursor-Skill-Pipelines-Reference.md` (§4 autonomous-express).

---

### 2.13 Confidence thresholding (≥85% silent execution, else #review-needed)

| Item | Current implementation | Alignment | Strengths | Gaps / risks | Risk |
|------|------------------------|-----------|-----------|--------------|------|
| **Threshold** | Rules and pipeline reference: **≥85%** for auto-execute (move, rename, destructive edits); **<85%** → propose only, flag **#review-needed** in logs. Some skills use ≥80% (distill-highlight-color, summary-preserve) or ≥70% (readability-flag), ≥75% (resurface-candidate-mark) per reference table. | **92%** | Consistent 85% for destructive/move; lower thresholds only for metadata or optional appends; #review-needed used in Ingest-Log, Archive-Log, etc. | Slight variance (80/75/70) is intentional per pipeline reference; no conflict. | Low |

**Relevant code/files:**
- `.cursor/rules/context/para-zettel-autopilot.mdc` (≥85% auto, <85% #review-needed).
- `3-Resources/Cursor-Skill-Pipelines-Reference.md` (confidence gate columns).
- `.cursor/rules/always/mcp-obsidian-integration.mdc` (snapshot chaining: confirm confidence ≥85%).

---

### 2.14 Backup-first / Option C – Zero-Manual safety (every destructive step)

| Item | Current implementation | Alignment | Strengths | Gaps / risks | Risk |
|------|------------------------|-----------|-----------|--------------|------|
| **External backup** | Every ingest/archive/etc. starts with **obsidian_create_backup**; destructive MCP calls use internal ensure_backup gate; backup path included in log (e.g. Ingest-Log `changes`). Rule: "Abort pipeline if create_backup fails." | **95%** | Option C explicit; no cp/mv/rm on vault; backup path in logs. | — | Low |
| **In-vault snapshots** | **obsidian-snapshot** skill: per-change (before split_atomic, distill_note rewrite, append_to_hub, move_note, etc.) and batch checkpoints; SNAPSHOT_DIR, BATCH_SNAPSHOT_DIR; snapshot before destructive when confidence ≥85%; on failure skip destructive and log #review-needed. | **92%** | Snapshot triggers table in pipeline reference and in each pipeline rule; Backup-Log; append-only. | — | Low |

**Relevant code/files:**
- `.cursor/rules/always/mcp-obsidian-integration.mdc` (Option C, snapshot chaining, fallback table).
- `.cursor/skills/obsidian-snapshot/SKILL.md`.
- `3-Resources/Cursor-Skill-Pipelines-Reference.md` (Snapshot triggers table).

---

### 2.15 Visual & relational clarity (no tag clutter, Dataview, callouts, project-linked colors, canvas/graph hints, scannable layout)

| Item | Current implementation | Alignment | Strengths | Gaps / risks | Risk |
|------|------------------------|-----------|-----------|--------------|------|
| **Frontmatter + Dataview** | Hubs and dashboards use `para-type`, `status`, `project-id`, `next-actions`, `resurface-candidate`, `needs-simplify` in LIST/TABLE/TASK. **✅** **Second-Brain-Config.md** states: tags are convenience only (#dev-task, #bug); pipelines and core filtering use frontmatter. Minimal tag reliance; key fields in frontmatter. | **90%** | PARA-Dashboard, Resources Hub, Resurface, Visual Health Dashboard; tag vs frontmatter policy in config. | Tag-based filters still exist where useful (e.g. task overview); intentional hybrid. | Low |
| **Callouts** | TL;DR wrapped in `> [!summary]` (callout-tldr-wrap); readability warning `> [!warning]`; CTA `> [!tip]` etc. | **90%** | Consistent callout usage across skills. | — | Low |
| **Project-linked colors** | highlight_key and color theory in skills; **✅** Visual Health Dashboard counts **both** inline CSS and legacy `^{Color}` (combined); "highlight patterns by folder" uses same logic. | **88%** | Dashboard aligned with canonical format; no undercount of inline-CSS highlights. | — | Low |
| **Canvas/graph hints** | **✅** **Graph view**: para-zettel-autopilot and auto-express include optional **graph-related frontmatter** (e.g. `graph: { color: "#hex" }`) from project color. **✅** Second-Brain-Config: project MOCs include "Graph Focus" callout with Dataview (e.g. `WHERE project-id = "Test-Project"`). **✅** Visual Health Dashboard has **Graph health** section (avg outlinks per note, notes with graph frontmatter). Canvas left for later. | **68%** | Graph frontmatter and callout guidance in place; dashboard graph health metric. | Canvas not yet implemented (deferred). | Low |

**Relevant code/files:**
- `3-Resources/Visual-Health-Dashboard.md`, `3-Resources/_dv-visual-health-dashboard.js` (highlight combined counts, Graph health section).
- `3-Resources/Second-Brain-Config.md` (tags vs frontmatter, Graph Focus for project MOCs).
- `.cursor/rules/context/para-zettel-autopilot.mdc`, `.cursor/rules/context/auto-express.mdc` (graph frontmatter bullet).
- `Resources Hub.md`, `PARA-Dashboard.md`, `Resurface.md`.
- `.cursor/skills/callout-tldr-wrap/SKILL.md`, `readability-flag/SKILL.md`, `call-to-action-append/SKILL.md`.

---

## 3. Overall alignment and gap heatmap

### Overall alignment score (weighted) — post-refinement

| Category | Weight | Avg score (from above) | Weighted |
|----------|--------|------------------------|----------|
| Triggers + autonomy | 15% | ~68% (triggers 95+90+30)/3, autonomy 80 | ~10.2 |
| PARA + structure | 10% | 93% | 9.3 |
| Ingest pipeline (split, distill, highlight, frontmatter, hub, actions) | 35% | ~91% | 31.9 |
| Archive + resurface + express | 20% | ~92% | 18.4 |
| Safety (confidence + backup/snapshot) | 15% | 93% | 14 |
| Visual/clarity (Dataview, callouts, colors, graph) | 5% | ~84% | 4.2 |
| **Total** | 100% | — | **~88%** |

**Justification (post-refinement):** Triggers improved (always-ingest-bootstrap in place). Highlightr format aligned (express-mini-outline inline CSS only; dashboard counts both formats; legacy documented). Central config (Second-Brain-Config.md) for hub names and archive thresholds; project-MOC transition and links array standard; project colors mandated in action extraction; graph hints and dashboard graph health added. Remaining gap: "when new notes land" automation (watcher on hold until ≥93% re-audit).

---

### Gap heatmap — post-refinement

| Requirement | Score | Priority to close |
|-------------|-------|--------------------|
| Trigger mechanisms (phrase triggers) | 95% | — |
| Trigger mechanisms (watcher / "when notes land") | 30% | **High** (Phase 4, on hold) |
| Full post-capture autonomy (trigger from file drop) | 80% | **High** (intentional; watcher later) |
| PARA + 4-level subfolders | 92–95% | Low |
| Atomic splitting | 90% | Low |
| Progressive distillation | 92% | Low |
| Highlightr as relational language (format consistency) | 88% | Low |
| Frontmatter enrichment | 92% | Low |
| Hub/MOC linking | 90% | Low |
| Action extraction | 92% | Low |
| Archiving logic | 94% | Low |
| Resurfacing candidates | 92% | Low |
| Early express | 92% | Low |
| Confidence thresholding | 92% | Low |
| Backup-first / Option C | 92–95% | Low |
| Visual/clarity (dashboard + highlight + graph) | 84% | Low |
| Canvas (deferred) | — | Later iteration |

---

## 4. Critical blocking issues (must-fix before claiming "autonomous") — post-refinement

1. **No automatic trigger when new notes land in Ingest/** **(unchanged; Phase 4 on hold)**  
   Master Goal says processing happens "whenever the user says … or **when new notes land in Ingest/**". Today: user must open Cursor and say the phrase (or run QuickAdd then Cursor). **Fix:** Add a documented, supported trigger path for "notes landed" (e.g. watcher script that appends to Ingest-Log and optionally opens Cursor) once Phase 1–3 are stable and re-audit ≥93%. Intentional design: user-triggered autonomy first; watcher last.

2. **~~Highlightr format inconsistency~~** **✅ CLOSED.**  
   express-mini-outline uses inline CSS only; dashboard counts both inline CSS and legacy `^{Color}`; Highlightr-Color-Key has Legacy format subsection. Optional migration of existing notes with legacy format.

3. **~~Missing always-ingest-bootstrap rule~~** **✅ CLOSED.**  
   `.cursor/rules/always/always-ingest-bootstrap.mdc` exists; pipeline reference trigger table points to it.

---

## 5. Nice-to-have polish — post-refinement

- **~~MCP tool descriptors~~** **✅** `folder_path` in ensure_structure schema (project descriptor); suggested descriptions in `3-Resources/MCP-Descriptor-Descriptions.md` for classify_para, split_atomic, append_to_hub (apply in server repo when available).
- **~~Single config for hub names / archive age threshold~~** **✅** `3-Resources/Second-Brain-Config.md` in place; skills read from it (archive-check, resurface-candidate-mark, etc.).
- **Canvas:** Optional rule or doc on canvas for MOCs (deferred; graph hints done).
- **QuickAdd → Cursor:** Optional "Open Cursor with INGEST MODE prompt" (e.g. URI or script) so one click in Obsidian + one in Cursor completes the trigger.
- **Legacy highlight migration:** Optional one-time pass on Test-Project + Ingest notes with `==...==^{Color}` → inline CSS (documented as optional in Color Key).

---

## 6. Actionable recommendations — post-refinement

| # | Action | Status | Notes |
|---|--------|--------|-------|
| 1 | Align Highlightr format (express-mini-outline) | **✅ Done** | Inline CSS only; no `==...==` or `^{Color}`. |
| 2 | Dashboard: count inline CSS + legacy | **✅ Done** | hexToColor map, getInlineHexes, hasLegacyColor; combined counts. |
| 3 | always-ingest-bootstrap rule | **✅ Done** | `.cursor/rules/always/always-ingest-bootstrap.mdc` created; pipeline reference updated. |
| 4 | "When notes land" / watcher | **Phase 4 (on hold)** | Implement after re-audit ≥93%; document in plan. |
| 5 | Legacy highlight (document or migrate) | **✅ Done** | Highlightr-Color-Key.md "Legacy format" subsection; optional migration remains. |
| 6 | ensure_structure descriptor | **✅ Documented** | folder_path in project descriptor; MCP-Descriptor-Descriptions.md references it. |
| 7 | Central config | **✅ Done** | Second-Brain-Config.md; archive-check, resurface-candidate-mark use it. |
| 8 | Project-MOC + links array | **✅ Done** | frontmatter-enrich; Master Goal.md Organization; links array standard. |
| 9 | Graph hints + dashboard graph health | **✅ Done** | para-zettel-autopilot, auto-express; Second-Brain-Config (Graph Focus); _dv-visual-health-dashboard.js Graph health section. |

---

## 7. Roadmap to 95%+ alignment — post-refinement

### Phase 1 — Critical consistency **✅ Complete**

- **Success criteria:** Zero Highlightr format conflicts; always-ingest-bootstrap exists; MCP descriptors documented; project colors mandated in next-action-extract.
- **Status:** Implemented per Post-Audit Refinement Plan.

### Phase 2 — Central config + MOC transition **✅ Complete**

- **Success criteria:** Second-Brain-Config.md in place; hub names and archive thresholds read from config; project-MOC link for notes with project-id; links array standard; optional auto-layer-select skill.
- **Status:** Implemented.

### Phase 3 — Visual/graph + dashboard **✅ Complete**

- **Success criteria:** Graph frontmatter and callout guidance in rules and config; Visual Health Dashboard includes graph health and correct highlight counts; config states tag vs frontmatter.
- **Status:** Implemented. Re-test dashboard on 20–30 pipeline-processed notes recommended.

### Phase 4 — Watcher ("when notes land") **On hold**

- **Success criteria:** Lightweight watcher on Ingest/ → append to Ingest-Log + optional "Open Cursor with INGEST MODE"; start only after re-audit ≥93% and 10+ flawless end-to-end runs.
- **Status:** Not started; intentional.

---

*End of audit (updated). Post-refinement: ~88% alignment. System is production-grade in pipeline design, safety, Highlightr consistency, central config, project-MOC and links array, and graph hints. Remaining gap: "when new notes land" automation (Phase 4, on hold).*
