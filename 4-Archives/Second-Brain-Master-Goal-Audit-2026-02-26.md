---
title: Second Brain Master Goal — Production Audit (2026-02-26)
created: 2026-02-26
tags: [pkm, audit, second-brain, para, cursor, mcp]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[Cursor-Skill-Pipelines-Reference]]", "[[Second-Brain-Config]]", "[[Second-Brain-Master-Goal-Audit-2026-02-25]]"]
---

# Second Brain Master Goal — Full Production Audit

**Reference (verbatim):** *Building a fully autonomous, post-capture Second Brain in Obsidian using the PARA + Zettelkasten principles (inspired by Tiago Forte's Building a Second Brain methodology), where capture is the only manual step the user ever has to perform. Everything after that — organizing into PARA folders (including intelligent subfolder creation up to 4 levels deep), atomic note splitting, progressive distillation, color-coded highlighting that visually links and relates ideas across project files, frontmatter enrichment, hub linking, action extraction, archiving, resurfacing candidates, and even early express/output generation — happens automatically via Cursor + MCP pipelines whenever the user says something like "INGEST MODE", "Process Ingest", or when new notes land in Ingest/. The system should feel hands-off yet trustworthy: high-confidence (≥85%) actions execute silently; lower-confidence items are proposed/logged/flagged (#review-needed); every potentially destructive step is protected by backup-first (Option C – Zero-Manual); and the user gets maximum visual and relational clarity at a glance without tag clutter (frontmatter + Dataview + callouts + project-linked Highlightr colors informed by color theory + task lists + canvas/graph hints). Highlightr colors are a visual language for idea relationships (analogous/complementary/project-specific). In short: Turn Obsidian into an external brain that ingests raw material, organizes/distills/expresses it autonomously, and presents knowledge in the most scannable, relationally clear, and action-oriented way.*

**Audit date:** 2026-02-26. **Scope:** Entire codebase and Obsidian vault in this Cursor workspace. **Method:** Exploration of `.cursor/`, rules, skills, MCP descriptors, pipeline reference, config, templates, scripts, PARA/Ingest/Backups, Dataview, Highlightr key.

---

## 1. Project structure (explored)

| Area | Location | Notes |
|------|----------|--------|
| **Cursor rules (always)** | `.cursor/rules/always/` | `00-always-core.mdc`, `always-ingest-bootstrap.mdc`, `mcp-obsidian-integration.mdc`, `second-brain-standards.mdc` |
| **Cursor rules (context)** | `.cursor/rules/context/` | `para-zettel-autopilot.mdc`, `ingest-processing.mdc`, `non-markdown-handling.mdc`, `auto-distill.mdc`, `auto-archive.mdc`, `auto-express.mdc`, `auto-organize.mdc`, `auto-restore.mdc`, `auto-resurface.mdc`, `snapshot-sweep.mdc` |
| **Skills** | `.cursor/skills/<name>/SKILL.md` | frontmatter-enrich, subfolder-organize, split-link-preserve, distill-highlight-color, next-action-extract, layer-promote, callout-tldr-wrap, readability-flag, archive-check, resurface-candidate-mark, summary-preserve, call-to-action-append, version-snapshot, express-mini-outline, related-content-pull, obsidian-snapshot, auto-layer-select |
| **Sync** | `.cursor/sync/` | Mirrors of rules/skills (`.md`) |
| **Plans** | `.cursor/plans/*.plan.md` | ingest_rules_and_non-md_handling, visual_health_dashboard, skill_pipelines_implementation, enhanced-snapshots-rollback, etc. |
| **Scripts** | `scripts/quickadd/` | ingest-batch.js, run-ingest.js, distill-current.js, express-current.js (append to logs / trigger text; do not invoke Cursor) |
| **Templates** | `Templates/` | Ingest-Template, Ingest-Selector, AI-Output, Stray-Thoughts, Session-Prep, ProcessIngestTrigger, etc. |
| **Ingest** | `Ingest/` | 9 items (Master Goal.md, Obsidian Second Brain Audit.md, reports, Vault Name.md, Test of attachment.md, Untitled Document 1/2, etc.) — **unprocessed** |
| **PARA** | `1-Projects/`, `2-Areas/`, `3-Resources/`, `4-Archives/` | Present; Test-Project, Test-Project-Archive; hubs in root |
| **Backups** | `Backups/Per-Change/`, `Backups/Batch/` | In-vault snapshots; external BACKUP_DIR per MCP env |
| **Config** | `.obsidian/` | community-plugins (QuickAdd, Templater, Dataview, etc.), workspace, appearance |
| **MCP descriptors** | `~/.cursor/projects/.../mcps/user-obsidian-para-zettel-autopilot/tools/*.json` | create_backup, classify_para, split_atomic, distill_note, append_to_hub, move_note, ensure_structure (with `folder_path`), update_note, read_note, log_action, etc. |
| **Dataview** | `3-Resources/_dv-visual-health-dashboard.js`, dashboards | Visual-Health-Dashboard.md, PARA-Dashboard.md, Resurface.md, Resources Hub |
| **Highlightr** | `3-Resources/Highlightr-Color-Key.md` | Single source of truth; inline CSS; project `highlight_key`; legacy subsection |
| **Central config** | `3-Resources/Second-Brain-Config.md` | hub_names, archive (age_days, no_activity_days), highlight default_key, graph moc_strength, links array, tag vs frontmatter |
| **Pipeline reference** | `3-Resources/Cursor-Skill-Pipelines-Reference.md` | Canonical pipeline order, confidence gates, snapshot triggers, trigger→rule mapping |
| **Logs** | Root + `3-Resources/` | Ingest-Log.md, Distill-Log.md, Archive-Log.md, Express-Log.md, Organize-Log.md, Backup-Log.md |

---

## 2. Per-requirement evaluation

### 2.1 Trigger mechanisms ("INGEST MODE", "Process Ingest", filesystem watcher on Ingest/)

| Item | Current implementation | Alignment | Strengths | Gaps / deviations | Risk |
|------|------------------------|-----------|-----------|-------------------|------|
| **Phrase triggers** | **always-ingest-bootstrap.mdc** (always-applied): when user says "INGEST MODE", "Process Ingest", or "run ingests", ensures ingest-processing (non-MD + embedded normalization) then full-autonomous-ingest on Ingest/*.md per pipeline reference; lists Ingest via `obsidian_list_notes("Ingest")`. Pipeline reference trigger table points to this rule. | **95%** | Canonical phrases; bootstrap + para-zettel + MCP rule chain; no doc gap. | None. | Low |
| **Process Ingest (Obsidian-side)** | QuickAdd macros ("Ingest Batch", "Run Ingest") and scripts append to Ingest-Log or trigger text; `Templates/Scripts/ProcessIngestTrigger.js` appends reminder. Session-Prep (Templater) on load can append "Say in Cursor: INGEST MODE…" if Ingest has .md. | **85%** | One-click in Obsidian adds log/reminder. | Scripts do **not** invoke Cursor or run the pipeline; user must open Cursor and say the phrase. | Low |
| **Filesystem watcher on Ingest/** | **None.** No daemon, no background watcher, no Obsidian→Cursor bridge on file create. Master Goal says processing happens "**when new notes land in Ingest/**". | **25%** | Session-Prep can remind on startup. | **Critical gap:** "When new notes land" is **not** automated. User must open Cursor and say "INGEST MODE" or "Process Ingest". | **Med** |

**Relevant code/files:**
- `.cursor/rules/always/always-ingest-bootstrap.mdc` (lines 9–10): trigger phrases and pipeline reference.
- `.cursor/rules/context/para-zettel-autopilot.mdc` (globs: `Ingest/*.md`): applies when Ingest note is open.
- `3-Resources/Cursor-Skill-Pipelines-Reference.md` (trigger table): "Ingest", "process Ingest", "run ingests" → full-autonomous-ingest.
- No watcher script or Cursor URI in repo.

---

### 2.2 Full post-capture autonomy (zero manual steps after capture)

| Item | Current implementation | Alignment | Strengths | Gaps / deviations | Risk |
|------|------------------------|-----------|-----------|-------------------|------|
| **Zero manual after capture** | Once user runs Cursor with "INGEST MODE" or "Process Ingest" (or opens an Ingest note and pipeline runs), the **full chain** runs per reference: backup → classify → frontmatter-enrich → subfolder-organize → split_atomic → split-link-preserve → distill → distill-highlight-color → next-action-extract → append_to_hub → move_note → log. No per-step confirmations at ≥85%. | **78%** | Single prompt runs full pipeline; confidence gates and backup/snapshot enforced; no "wait for ok" in AI Prompts. | (1) User must **manually** open Cursor and say the phrase (or run QuickAdd then Cursor). (2) "When new notes land" is not automated. Autonomy is **after** user trigger, not from file drop alone. | **Med** |

**Relevant code/files:**
- `Templates/AI Prompts.md` (if present): no interactive confirmation loops.
- `.cursor/rules/context/para-zettel-autopilot.mdc`: batch isolation, backup/snapshot, ≥85% auto.

---

### 2.3 PARA organization + intelligent subfolder creation (up to 4 levels deep)

| Item | Current implementation | Alignment | Strengths | Gaps / deviations | Risk |
|------|------------------------|-----------|-----------|-------------------|------|
| **PARA roots** | `1-Projects`, `2-Areas`, `3-Resources`, `4-Archives`; MCP `obsidian_ensure_structure` creates top-level PARA + Ingest. | **98%** | Consistent naming; rules/skills reference same roots. | — | Low |
| **Subfolder creation (≤4 levels)** | **subfolder-organize** skill: path `{para-root}/{ProjectOrAreaName?}/{IdeaClusterOrSubtheme?}/{YYYY-MM-DD-title}.md`; max 4 path segments. For deep moves, **obsidian_ensure_structure** with **folder_path** (target parent) is required; documented in `mcp-obsidian-integration.mdc` and verified 2026-02-25. MCP descriptor `obsidian_ensure_structure.json` includes `folder_path`. | **92%** | Logic clear; deep-move behavior verified; folder_path in descriptor. | — | Low |

**Relevant code/files:**
- `.cursor/skills/subfolder-organize/SKILL.md`: path pattern, ensure_structure, move_note.
- `.cursor/rules/always/mcp-obsidian-integration.mdc`: "Documented behavior" table (obsidian_move_note does not create parents; ensure_structure with folder_path does).
- `~/.../mcps/.../tools/obsidian_ensure_structure.json`: `folder_path` in schema.

---

### 2.4 Atomic note splitting

| Item | Current implementation | Alignment | Strengths | Gaps / deviations | Risk |
|------|------------------------|-----------|-----------|-------------------|------|
| **Split** | MCP `obsidian_split_atomic` (path, split_on e.g. `## `). Pipeline runs it when multi-idea. **split-link-preserve** skill: after split, sets `split_from` on children, appends `## Splits` on parent; idempotent; backlinks. | **90%** | Atomic split + traceability; skill and pipeline order defined. | MCP descriptor `obsidian_classify_para.json` has **empty description** in repo; vault has suggested text in `3-Resources/MCP-Descriptor-Descriptions.md` but server may not have it. | Low |

**Relevant code/files:**
- `.cursor/skills/split-link-preserve/SKILL.md`.
- `.cursor/rules/always/mcp-obsidian-integration.mdc`: destructive steps include split_atomic; snapshot before.
- `3-Resources/MCP-Descriptor-Descriptions.md`: suggested descriptions for server/repo.

---

### 2.5 Progressive distillation pipeline

| Item | Current implementation | Alignment | Strengths | Gaps / deviations | Risk |
|------|------------------------|-----------|-----------|-------------------|------|
| **Distill** | MCP `obsidian_distill_note` (path, add_tldr); then skills: **distill-highlight-color** → **layer-promote** → **callout-tldr-wrap** → **readability-flag**. Optional **auto-layer-select** (content complexity → 1/2/3 layers). Autonomous-distill: backup → (auto-layer-select) → distill layers → distill-highlight-color → layer-promote → callout-tldr-wrap → readability-flag; per-change snapshot before first structural rewrite; batch checkpoint ~every 3 notes. | **92%** | Full layer chain; optional layer autonomy; snapshot triggers in pipeline reference. | Distill_note tool descriptor does not specify "progressive layers"; layer-promote/readability are skill-driven. | Low |

**Relevant code/files:**
- `.cursor/rules/context/auto-distill.mdc`: optional auto-layer-select.
- `3-Resources/Cursor-Skill-Pipelines-Reference.md` (§2 autonomous-distill).
- `.cursor/skills/auto-layer-select/SKILL.md`, `distill-highlight-color/SKILL.md`, `layer-promote/SKILL.md`, `callout-tldr-wrap/SKILL.md`, `readability-flag/SKILL.md`.

---

### 2.6 Highlightr color system as relational visual language (analogous/complementary/project overrides, cross-project)

| Item | Current implementation | Alignment | Strengths | Gaps / deviations | Risk |
|------|------------------------|-----------|-----------|-------------------|------|
| **Semantic mapping** | `3-Resources/Highlightr-Color-Key.md`: semantic table (Yellow/Green/Blue/Red/Orange/Purple/Pink/Cyan/Grey); **exact storage format** inline CSS only; **forbidden**: `==text==`, `^{Color}`. | **90%** | Single source of truth; project `highlight_key` overrides; color theory in key. | — | Low |
| **Pipeline usage** | **distill-highlight-color**: master key + project highlight_key; analogous for related ideas, complementary for contrasts. **layer-promote**: complementary for conflicting ideas. | **85%** | Skills reference color key; apply via search_replace/update_note. | — | Low |
| **Format consistency** | express-mini-outline SKILL specifies inline CSS only; Visual Health Dashboard `_dv-visual-health-dashboard.js` counts **both** inline CSS and legacy `^{Color}`; Highlightr-Color-Key has "Legacy format" subsection. | **88%** | Single canonical format; dashboard aligned; legacy documented. | Optional migration of existing notes with legacy format. | Low |

**Relevant code/files:**
- `3-Resources/Highlightr-Color-Key.md`: Section 1 semantics, Section 2 format, Legacy subsection, project guidelines.
- `.cursor/skills/distill-highlight-color/SKILL.md`, `.cursor/skills/layer-promote/SKILL.md`.
- `3-Resources/_dv-visual-health-dashboard.js`: hexToColor, getInlineHexes, hasLegacyColor; combined counts.

---

### 2.7 Frontmatter enrichment (all required keys, dynamic population)

| Item | Current implementation | Alignment | Strengths | Gaps / deviations | Risk |
|------|------------------------|-----------|-----------|-------------------|------|
| **Required keys** | **frontmatter-enrich** skill: status, confidence, para-type, created, **links** as YAML array; optional project-id, priority, deadline, resurface-date. When project-id set, adds `[[ProjectName MOC]]` to links. Uses `obsidian_manage_frontmatter`. | **92%** | Clear list; links array; project-MOC link; applied after classify_para in ingest and organize. | — | Low |

**Relevant code/files:**
- `.cursor/skills/frontmatter-enrich/SKILL.md`: links array, project MOC.
- `3-Resources/Second-Brain-Config.md`: links frontmatter note.
- `3-Resources/Cursor-Skill-Pipelines-Reference.md`: frontmatter-enrich slot.

---

### 2.8 Hub / MOC linking

| Item | Current implementation | Alignment | Strengths | Gaps / deviations | Risk |
|------|------------------------|-----------|-----------|-------------------|------|
| **Append to hub** | MCP `obsidian_append_to_hub` (hub_name, wikilink, summary). Pipeline: after move, append to relevant hub. Hub names in **Second-Brain-Config.md** (hub_names: projects, areas, resources, resurface). Notes with project-id get `[[ProjectName MOC]]` in links (frontmatter-enrich). | **88%** | Tool and pipeline step present; central config; project-MOC transition. | MCP descriptor `obsidian_append_to_hub.json` has **empty description** in project descriptor; hub behavior relies on rule/skill docs. | Low |

**Relevant code/files:**
- `~/.../mcps/.../tools/obsidian_append_to_hub.json`: description `""`.
- `3-Resources/Second-Brain-Config.md`: hub_names.
- `.cursor/skills/frontmatter-enrich/SKILL.md`: project MOC in links.
- `3-Resources/MCP-Descriptor-Descriptions.md`: suggested description for append_to_hub.

---

### 2.9 Action extraction + task list handling

| Item | Current implementation | Alignment | Strengths | Gaps / deviations | Risk |
|------|------------------------|-----------|-----------|-------------------|------|
| **Tasks** | **next-action-extract** skill: parse task-like phrases → checklists `- [ ]` in body and `next-actions` in frontmatter (array/string for Dataview). Confidence ≥85%. When project-id exists, project-specific highlight color for action blocks (inline CSS only). | **92%** | Clear instructions; backup before edits; project colors when project-id set. | — | Low |

**Relevant code/files:**
- `.cursor/skills/next-action-extract/SKILL.md`.
- `3-Resources/Visual-Health-Dashboard.md`: LIST for next-actions, needs-simplify, resurface-candidate.
- `3-Resources/_dv-visual-health-dashboard.js`: hasNextActions, counts.

---

### 2.10 Archiving logic

| Item | Current implementation | Alignment | Strengths | Gaps / deviations | Risk |
|------|------------------------|-----------|-----------|-------------------|------|
| **Archive pipeline** | **autonomous-archive**: backup → classify_para → **archive-check** (no open tasks, status complete, age threshold; ≥85% for move) → **subfolder-organize** (archive path) → **resurface-candidate-mark** → **summary-preserve** → obsidian_move_note → log. archive-check reads age from **Second-Brain-Config.md** (archive.age_days / no_activity_days); default 90/60. Per-change snapshot after archive-check (≥85%) before subfolder-organize/summary-preserve/move. | **94%** | Full sequence; safety invariants; central config for thresholds. | — | Low |

**Relevant code/files:**
- `.cursor/rules/context/auto-archive.mdc`.
- `.cursor/skills/archive-check/SKILL.md`, subfolder-organize, resurface-candidate-mark, summary-preserve.
- `3-Resources/Cursor-Skill-Pipelines-Reference.md` (§3).

---

### 2.11 Resurfacing candidates logic

| Item | Current implementation | Alignment | Strengths | Gaps / deviations | Risk |
|------|------------------------|-----------|-----------|-------------------|------|
| **Mark** | **resurface-candidate-mark** (in archive pipeline): set `resurface-candidate: true`; optional append to Resurface hub; ≥75%. Hub names from **Second-Brain-Config.md**. | **92%** | Skill and pipeline slot defined; Resurface.md has Dataview TABLE; config. | — | Low |
| **Surface** | **auto-resurface** rule (globs: Resurface.md): on "resurface" / "show resurface candidates" or open Resurface — list via global_search or Dataview; optionally append list. | **85%** | Trigger-based; no cron; aligns with manual curation. | — | Low |

**Relevant code/files:**
- `.cursor/skills/resurface-candidate-mark/SKILL.md`.
- `.cursor/rules/context/auto-resurface.mdc`.
- `Resurface.md`.

---

### 2.12 Early express/output generation

| Item | Current implementation | Alignment | Strengths | Gaps / deviations | Risk |
|------|------------------------|-----------|-----------|-------------------|------|
| **Express pipeline** | **autonomous-express**: backup → **version-snapshot** (Versions/ slug--timestamp.md, `mode: "create"`) → **related-content-pull** → **express-mini-outline** → **call-to-action-append**; log to Express-Log and Backup-Log. express-mini-outline uses inline CSS only. Rule includes optional graph frontmatter from project color. Triggers: "EXPRESS MODE", "express this note", etc. | **92%** | Version snapshot before appends; related + outline + CTA; highlight format aligned; graph hint. | — | Low |

**Relevant code/files:**
- `.cursor/rules/context/auto-express.mdc`.
- `.cursor/skills/version-snapshot/SKILL.md` (mode: "create"), related-content-pull, express-mini-outline, call-to-action-append.
- `3-Resources/Cursor-Skill-Pipelines-Reference.md` (§4).

---

### 2.13 Confidence thresholding (≥85% silent execution, else #review-needed)

| Item | Current implementation | Alignment | Strengths | Gaps / deviations | Risk |
|------|------------------------|-----------|-----------|-------------------|------|
| **Threshold** | Rules and pipeline reference: **≥85%** for auto-execute (move, rename, destructive edits); **<85%** → propose only, flag **#review-needed** in logs. Some skills use ≥80% (distill-highlight-color, summary-preserve) or ≥70% (readability-flag), ≥75% (resurface-candidate-mark) per reference table. | **92%** | Consistent 85% for destructive/move; lower only for metadata/optional appends; #review-needed in Ingest-Log, Archive-Log, etc. | Intentional variance; no conflict. | Low |

**Relevant code/files:**
- `.cursor/rules/context/para-zettel-autopilot.mdc`: ≥85% auto, <85% #review-needed.
- `3-Resources/Cursor-Skill-Pipelines-Reference.md`: confidence gate columns.
- `.cursor/rules/always/mcp-obsidian-integration.mdc`: snapshot chaining requires confidence ≥85%.

---

### 2.14 Backup-first / Option C – Zero-Manual safety (every destructive step)

| Item | Current implementation | Alignment | Strengths | Gaps / deviations | Risk |
|------|------------------------|-----------|-----------|-------------------|------|
| **External backup** | Every ingest/archive/etc. starts with **obsidian_create_backup**; destructive MCP calls use internal ensure_backup gate; backup path included in log (e.g. Ingest-Log `changes`). Rule: "Abort pipeline if create_backup fails." MCP descriptor has full description. | **95%** | Option C explicit; no cp/mv/rm on vault; backup path in logs. | — | Low |
| **In-vault snapshots** | **obsidian-snapshot** skill: per-change (before split_atomic, distill_note rewrite, append_to_hub, move_note, etc.) and batch checkpoints; SNAPSHOT_DIR, BATCH_SNAPSHOT_DIR; snapshot before destructive when confidence ≥85%; on failure skip destructive and log #review-needed. | **92%** | Snapshot triggers table in pipeline reference and each pipeline rule; Backup-Log; append-only. | — | Low |

**Relevant code/files:**
- `.cursor/rules/always/mcp-obsidian-integration.mdc`: Option C, snapshot chaining, fallback table.
- `.cursor/skills/obsidian-snapshot/SKILL.md`.
- `3-Resources/Cursor-Skill-Pipelines-Reference.md`: Snapshot triggers table.
- `~/.../mcps/.../tools/obsidian_create_backup.json`: description present.

---

### 2.15 Visual & relational clarity (no tag clutter, Dataview, callouts, project-linked colors, canvas/graph hints, scannable layout)

| Item | Current implementation | Alignment | Strengths | Gaps / deviations | Risk |
|------|------------------------|-----------|-----------|-------------------|------|
| **Frontmatter + Dataview** | Hubs and dashboards use para-type, status, project-id, next-actions, resurface-candidate, needs-simplify in LIST/TABLE/TASK. **Second-Brain-Config.md**: tags convenience only; pipelines use frontmatter. | **90%** | PARA-Dashboard, Resources Hub, Resurface, Visual Health Dashboard; tag vs frontmatter policy. | Tag-based filters still used where useful (e.g. task overview); intentional hybrid. | Low |
| **Callouts** | TL;DR in `> [!summary]` (callout-tldr-wrap); readability `> [!warning]`; CTA `> [!tip]`. | **90%** | Consistent callout usage across skills. | — | Low |
| **Project-linked colors** | highlight_key and color theory in skills; Visual Health Dashboard counts inline CSS + legacy (combined); "highlight patterns by folder" uses same logic. | **88%** | Dashboard aligned; no undercount of inline-CSS highlights. | — | Low |
| **Canvas/graph hints** | para-zettel-autopilot and auto-express include optional **graph-related frontmatter** (e.g. `graph: { color: "#hex" }`) from project color. Second-Brain-Config: project MOCs include "Graph Focus" callout with Dataview. Visual Health Dashboard has **Graph health** section (avg outlinks, notes with graph frontmatter). | **70%** | Graph frontmatter and callout guidance; dashboard graph health metric. | **Canvas not implemented** (deferred). | Low |

**Relevant code/files:**
- `3-Resources/Visual-Health-Dashboard.md`, `3-Resources/_dv-visual-health-dashboard.js`: Graph health (lines 150–160), highlight combined counts.
- `3-Resources/Second-Brain-Config.md`: tags vs frontmatter, Graph Focus for project MOCs.
- `.cursor/rules/context/para-zettel-autopilot.mdc`, auto-express.mdc: graph frontmatter bullet.
- `Resources Hub.md`, `PARA-Dashboard.md`, `Resurface.md`.

---

### 2.16 Ingest pipeline — Decision Wrapper fix (2026-03-04)

**Post-audit update:** Decision Wrapper creation in Phase 1 ingest was updated so wrappers always get **multiple choice options (A–G)** and follow the canonical template. **Change:** Use **`obsidian_propose_para_paths`**(path, para_type, max_candidates: "7", context_mode: "wrapper") to obtain up to 7 ranked path candidates regardless of confidence; read **Templates/Decision-Wrapper.md** (A–G version, single source of truth); fill placeholders and write to `Ingest/Decisions/Decision-for-{{slug}}--{{date}}.md`. Ensures every wrapper has seven proper lettered options and full template structure for CHECK_WRAPPERS and mobile-friendly review. See para-zettel-autopilot.mdc, Cursor-Skill-Pipelines-Reference.md §1, and Pipelines.md.

---

## 3. Overall alignment and gap heatmap

### Overall alignment score (weighted)

| Category | Weight | Avg score (from §2) | Weighted |
|----------|--------|---------------------|----------|
| Triggers + autonomy | 15% | ~68% (triggers 95+85+25)/3, autonomy 78 | ~10.2 |
| PARA + structure | 10% | 95% | 9.5 |
| Ingest pipeline (split, distill, highlight, frontmatter, hub, actions) | 35% | ~90% | 31.5 |
| Archive + resurface + express | 20% | ~91% | 18.2 |
| Safety (confidence + backup/snapshot) | 15% | 93% | 14.0 |
| Visual/clarity (Dataview, callouts, colors, graph) | 5% | ~85% | 4.2 |
| **Total** | 100% | — | **~87.6%** |

**Justification:** Strong pipeline design, safety, Highlightr consistency, central config, project-MOC, links array, and graph hints. The main drag is **trigger autonomy**: phrase triggers work well (95%), but "when new notes land" has no automation (25%), and full post-capture autonomy is 78% because the user must open Cursor and say the phrase.

---

### Gap heatmap

| Requirement | Score | Priority to close |
|-------------|-------|--------------------|
| Trigger mechanisms (phrase triggers) | 95% | — |
| Trigger mechanisms (watcher / "when notes land") | 25% | **High** |
| Full post-capture autonomy (trigger from file drop) | 78% | **High** |
| PARA + 4-level subfolders | 92–98% | Low |
| Atomic splitting | 90% | Low |
| Progressive distillation | 92% | Low |
| Highlightr as relational language | 85–88% | Low |
| Frontmatter enrichment | 92% | Low |
| Hub/MOC linking | 88% | Low (MCP descriptor empty) |
| Action extraction | 92% | Low |
| Archiving logic | 94% | Low |
| Resurfacing candidates | 92% | Low |
| Early express | 92% | Low |
| Confidence thresholding | 92% | Low |
| Backup-first / Option C | 92–95% | Low |
| Visual/clarity (dashboard + highlight + graph) | 85% | Low |
| Canvas | 70% (deferred) | Later |

---

## 4. Critical blocking issues (must-fix before claiming "autonomous")

1. **No automatic trigger when new notes land in Ingest/**  
   Master Goal: processing happens "whenever the user says … **or when new notes land in Ingest/**". Today: user must open Cursor and say the phrase (or run QuickAdd then Cursor). There is no watcher, no Cursor URI, no background process. **Fix:** Add a documented trigger path for "notes landed" (e.g. watcher script that appends to Ingest-Log and optionally opens Cursor with INGEST MODE prompt) after pipeline stability and re-audit ≥93%. Intentional: user-triggered autonomy first; watcher last.

2. **MCP tool descriptors with empty description**  
   In project MCP descriptors: `obsidian_classify_para.json` and `obsidian_append_to_hub.json` have `"description": ""`. The vault has suggested text in `3-Resources/MCP-Descriptor-Descriptions.md`, but the LLM may not get guidance from the tool schema. **Fix:** Populate descriptions in the MCP server (or project descriptors if used at runtime) from MCP-Descriptor-Descriptions.md so classify_para and append_to_hub behavior is explicit in tool schema.

3. **Ingest folder has 9 unprocessed notes**  
   Ingest/ currently contains Master Goal.md, Obsidian Second Brain Audit.md, and others. Either they are test fixtures or the pipeline has not been run. For a production claim, ensure "Process Ingest" runs to completion and Ingest/ is empty (or only #needs-manual-move items). **Fix:** Run INGEST MODE on current Ingest/*.md and verify end-to-end; document any notes intentionally left in Ingest.

---

## 5. Nice-to-have polish

- **QuickAdd → Cursor:** Optional "Open Cursor with INGEST MODE prompt" (e.g. custom URI or script) so one click in Obsidian + one in Cursor completes the trigger.
- **Legacy highlight migration:** Optional one-time pass on notes with `==...==^{Color}` → inline CSS (documented as optional in Color Key).
- **Canvas:** Optional rule or doc on canvas for MOCs (deferred; graph hints done).
- **Session-Prep:** Ensure Templater/Session-Prep reliably appends "Say in Cursor: INGEST MODE…" when Ingest has .md so the reminder is consistent.

---

## 6. Actionable recommendations

| # | Action | File(s) to create/edit | Code / rule change | Effort |
|---|--------|------------------------|---------------------|--------|
| 1 | Implement "when notes land" trigger (watcher or bridge) | New script or Obsidian plugin; optional Cursor URI; docs in pipeline reference | Watcher on Ingest/ → append to Ingest-Log + optional "Open Cursor with INGEST MODE"; document in plan. | **High** |
| 2 | Populate MCP descriptions for classify_para and append_to_hub | MCP server repo or project `mcps/.../tools/*.json` | Copy/sync from `3-Resources/MCP-Descriptor-Descriptions.md` into tool descriptors so description is non-empty. | **Low** |
| 3 | Run full ingest and clear Ingest/ | — | User: "INGEST MODE" in Cursor; verify all Ingest/*.md processed; document any intentional exceptions. | **Low** |
| 4 | Optional: QuickAdd macro to open Cursor with INGEST MODE | `scripts/quickadd/` or Templater | Script that writes trigger phrase to clipboard or opens Cursor with pre-filled prompt if supported. | **Med** |
| 5 | Optional: Legacy highlight migration | One-off script or manual batch | Replace `==...==^{Color}` with inline CSS in Test-Project/Ingest notes; optional. | **Low** |

---

## 7. Three-phase roadmap to 95%+ alignment

### Phase 1 — Descriptor and ingest hygiene (target: 90% weighted)

- **Actions:** Populate MCP descriptions for `obsidian_classify_para` and `obsidian_append_to_hub` from MCP-Descriptor-Descriptions.md. Run INGEST MODE on current Ingest/*.md; verify pipeline end-to-end; empty Ingest/ (or document exceptions).
- **Success criteria:** No empty tool descriptions for classify_para and append_to_hub; Ingest/ processed and empty (or explicitly documented); no new #review-needed spikes in logs.
- **Effort:** Low.

### Phase 2 — Trigger and autonomy (target: 93% weighted)

- **Actions:** Document and implement a supported trigger path for "notes landed" (e.g. lightweight watcher that appends to Ingest-Log and optionally opens Cursor with INGEST MODE prompt). Optionally add QuickAdd → Cursor one-click flow. Update pipeline reference and always-ingest-bootstrap with "when notes land" behavior.
- **Success criteria:** When new .md files land in Ingest/, either (a) a watcher appends a log line and optionally opens Cursor with INGEST MODE, or (b) a documented manual one-click flow (QuickAdd + Cursor) is the standard. Re-audit weighted alignment ≥93%.
- **Effort:** High (watcher) or Med (QuickAdd only).

### Phase 3 — Polish and visual completeness (target: 95%+ weighted)

- **Actions:** Optional legacy highlight migration; optional canvas guidance for MOCs; ensure Session-Prep and dashboard graph health are stable on 20–30 pipeline-processed notes. Finalize tag vs frontmatter policy in docs.
- **Success criteria:** Weighted alignment ≥95%; no critical gaps in the heatmap; canvas deferred but documented; Visual Health Dashboard and graph health validated.
- **Effort:** Low–Med.

---

*End of audit. Brutally honest summary: Pipeline design, safety (backup-first, snapshots, confidence gates), PARA structure, distillation, Highlightr format, frontmatter, hub/MOC, archive, resurface, and express are production-grade and well-documented. The only critical gap is **automatic trigger when new notes land in Ingest/**; everything else is either strong or minor polish. MCP descriptor gaps and a single run of INGEST MODE to clear Ingest/ are quick wins. Overall weighted alignment ~88%; Phase 1 gets to ~90%, Phase 2 to ~93%, Phase 3 to 95%+.*
