---
title: Autonomous Runs — Options & Config Reference
created: 2026-02-26
tags: [pkm, cursor, pipelines, mcp, skills, config]
para-type: Resource
status: active
links: ["[[Cursor-Skill-Pipelines-Reference]]", "[[Second-Brain-Config]]"]
---

# Autonomous Runs — Every Option, Config & Param

Single reference for **all exploitable options** during autonomous runs: **rules** (always + context), **skills** (paths, when-to-use, tools, config), MCP tool parameters, pipeline-level options, and vault config keys. Use this when tuning pipelines, writing prompts, or debugging runs.

---

## 1. Pipeline-level options

### 1.1 Triggers (launch phrases)

| Pipeline | Canonical trigger | Other triggers |
|----------|-------------------|----------------|
| **full-autonomous-ingest** | INGEST MODE – safe batch autopilot | "Process Ingest", "run ingests", Ingest/*.md (open/batch) |
| **autonomous-distill** | DISTILL MODE – safe batch autopilot | "distill this note", "refine this note", "autonomous distill on folder X" |
| **autonomous-archive** | ARCHIVE MODE – safe batch autopilot | "archive this note", "send to Archives", "move completed to 4-Archives" |
| **autonomous-express** | EXPRESS MODE – safe batch autopilot | "express this note", "generate outline", "create publishable summary" |
| **autonomous-organize** | ORGANIZE MODE – safe batch autopilot on [folder] | "ORGANIZE MODE", "Re-organize Projects and Resources", "classify and move" |

### 1.2 Scope & batch

| Option | Where | Values / notes |
|--------|--------|------------------|
| **Ingest scope** | always-ingest-bootstrap, AI Prompts | `obsidian_list_notes(directory: "Ingest")`; filter: all .md, or `#raw-ingest` / `status: raw` |
| **Distill batch size** | auto-distill | ~5 notes recommended for DISTILL MODE |
| **Archive scope** | auto-archive | 1-Projects, 2-Areas, 3-Resources only; exclusions: 4-Archives, Backups, Templates, *Hub.md, Log*.md |
| **Express batch** | auto-express | Single-note or very small (2–3 notes) |
| **Organize scope** | auto-organize | Optional folder: e.g. "on 1-Projects/Test-Project" or "on 3-Resources" |

### 1.3 Confidence gates (global)

| Threshold | Effect |
|-----------|--------|
| **≥85%** | Auto-execute destructive steps (move, rename, overwrite, split, distill rewrite, hub append). Per-change snapshot then proceed. |
| **<85%** | Propose only; flag `#review-needed`; do not move/overwrite; note stays in place (e.g. Ingest). |
| **No confirmation loops** | Agent decides and acts (or flags); no "wait for ok" mid-run. |

### 1.4 Snapshot frequency (batch checkpoints)

| Pipeline | Per-change snapshot triggers | Batch checkpoint |
|----------|-----------------------------|------------------|
| full-autonomous-ingest | Before split_atomic, distill_note (rewrite), append_to_hub, move_note, rename_note | Every 5 notes |
| autonomous-distill | Before first structural rewrite (distill layers / layer-promote / heavy update_note) | ~Every 3 notes |
| autonomous-archive | After archive-check ≥85%, before subfolder-organize / summary-preserve / move | Once per sweep |
| autonomous-express | Before related-content-pull, express-mini-outline, call-to-action-append | Optional |
| autonomous-organize | Before rename_note and before move_note (when ≥85%) | ~Every 3 notes |

---

## 2. Vault config (Second-Brain-Config.md)

Read from `3-Resources/Second-Brain-Config.md` when skills need hub names or thresholds.

| Key | Purpose | Example / default |
|-----|---------|-------------------|
| **hub_names.projects** | Projects hub note name | "Projects Hub" |
| **hub_names.areas** | Areas hub note name | "Areas Hub" |
| **hub_names.resources** | Resources hub note name | "Resources Hub" |
| **hub_names.resurface** | Resurface hub note name | "Resurface" |
| **archive.age_days** | Min age (days) for archive candidate | 90 |
| **archive.no_activity_days** | No-activity (last-modified) threshold | 60 |
| **highlight.default_key** | Master color key path | "3-Resources/Highlightr-Color-Key.md" |
| **graph.moc_strength** | MOC graph strength | 3 |

**Note:** `archive-check` uses `age_days` / `no_activity_days`; default 90/60 if config missing. `resurface-candidate-mark` and `append_to_hub` use hub_names. `distill-highlight-color` uses highlight.default_key and note-level `highlight_key`.

---

## 3. MCP tools — parameters

Server: **obsidian-para-zettel-autopilot** (global `~/.cursor/mcp.json`). All paths are vault-relative unless stated.

### 3.1 Backup & safety

| Tool | Params | Defaults | Notes |
|------|--------|----------|--------|
| **obsidian_create_backup** | `paths` (string: JSON array of paths), `backup_dir_override` | paths: `[]`, backup_dir_override: `""` | Required first before any destructive op. Aborts workflow on failure. |
| **obsidian_ensure_backup** | `path`, `max_age_minutes` | path: `""`, max_age_minutes: `"15"` | Verify recent backup exists; used internally by destructive tools. |

### 3.2 Read & list

| Tool | Params | Defaults | Notes |
|------|--------|----------|--------|
| **obsidian_read_note** | `path` | path: `""` | Read note content + frontmatter. |
| **obsidian_list_notes** | `directory` | directory: `""` | List notes/folders at root or under directory (e.g. `"Ingest"`, `"3-Resources"`). |
| **obsidian_global_search** | `query`, `context_length` | query: `""`, context_length: `"100"` | Text search; context_length chars per hit. |

### 3.3 Write & edit

| Tool | Params | Defaults | Notes |
|------|--------|----------|--------|
| **obsidian_update_note** | `path`, `content`, `mode` | path: `""`, content: `""`, mode: `"overwrite"` | mode: `overwrite` | `create` (new file only; skips dest backup). Append: use read + concat + overwrite, or mode `append` if server supports. |
| **obsidian_search_replace** | `path`, `old_text`, `new_text` | — | First occurrence only. Backup required. |
| **obsidian_manage_frontmatter** | `path`, `key`, `value`, `action` | path: `""`, key: `""`, value: `""`, action: `"set"` | action: `set` or `delete`. |
| **obsidian_manage_tags** | `path`, `add_tags`, `remove_tags` | path: `""`, add_tags: `""`, remove_tags: `""` | Comma-separated, without #. |

### 3.4 Structure & move

| Tool | Params | Defaults | Notes |
|------|--------|----------|--------|
| **obsidian_ensure_structure** | `vault_root`, `dry_run`, `folder_path` | vault_root: `""`, dry_run: `"false"`, folder_path: `""` | With `folder_path`: create that path recursively (e.g. `4-Archives/Project-Archive/Subtheme`). Idempotent. dry_run: report only. |
| **obsidian_move_note** | `path`, `new_path` | path: `""`, new_path: `""` | Does not create parent dirs; use ensure_structure first for deep paths. |
| **obsidian_rename_note** | `path`, `new_name` | path: `""`, new_name: `""` | In-place rename (filename only). |
| **obsidian_delete_note** | `path` | path: `""` | Prefer move to 4-Archives over delete. |

### 3.5 Pipeline-specific

| Tool | Params | Defaults | Notes |
|------|--------|----------|--------|
| **obsidian_classify_para** | `path`, `para_type` | path: `""`, para_type: `""` | CoT + confidence; para_type can be hint. |
| **obsidian_split_atomic** | `path`, `split_on` | path: `""`, split_on: `"## "` | Split on heading; returns child paths. |
| **obsidian_distill_note** | `path`, `add_tldr` | path: `""`, add_tldr: `"true"` | Progressive summarization; add_tldr boolean string. |
| **obsidian_append_to_hub** | `hub_name`, `wikilink`, `summary` | hub_name: `""`, wikilink: `""`, summary: `""` | Append link + summary to hub note. |
| **obsidian_log_action** | `log_path`, `excerpt`, `para`, `changes`, `confidence`, `proposed_mv`, `flag` | log_path: `"Ingest-Log.md"`, others: `""` | Append log line. Put backup path in `changes`. |

### 3.6 Log paths (per pipeline)

| Pipeline | Primary log | Also |
|----------|-------------|------|
| Ingest | Ingest-Log.md (default for log_action) | Backup-Log.md (snapshots) |
| Distill | 3-Resources/Distill-Log.md | Backup-Log.md |
| Archive | 3-Resources/Archive-Log.md | Backup-Log.md |
| Express | 3-Resources/Express-Log.md | Backup-Log.md |
| Organize | 3-Resources/Organize-Log.md | Backup-Log.md |

**Log line format:** `YYYY-MM-DD HH:MM | Excerpt: [snippet] | PARA: [type] | Changes: [list; include Backup: [path]] | Confidence: X% | Proposed MV: [path or 'stay'] | Flag: [none or #review-needed + reason]`

---

## 4. Skills — configs & confidence gates

### 4.1 full-autonomous-ingest

| Skill | Slot | Confidence | Config / params |
|-------|-----|------------|------------------|
| **frontmatter-enrich** | after classify_para | ≥85% auto | Set: status, confidence, para-type, created, links (YAML array); optional: project-id, priority, deadline, resurface-date. links: `["[[Hub]]", "[[Project MOC]]"]`. |
| **subfolder-organize** | after frontmatter-enrich | ≥85% move | Max 4 levels. Path: `{para-root}/{Project?}/{Subtheme?}/{YYYY-MM-DD-title}.md`. Call ensure_structure(folder_path: parent) before move. Use `obsidian_propose_para_paths` (e.g. context_mode `"wrapper"` / `"midband"`) when ranked candidates + reasons are needed for Decision Wrappers or mid-band refinement. |
| **split-link-preserve** | after split_atomic | ≥85% | Child: split_from, related (append). Parent: ## Splits with `- [[Child]] — reason`; optional split_into (array). ~60 chars reason. |
| **distill-highlight-color** | after distill_note | ≥80% | Master key: Highlightr-Color-Key.md; note highlight_key for project. Inline CSS or key’s class format only. |
| **next-action-extract** | after distill-highlight-color | ≥85% | Checklists in body; frontmatter next-actions: JSON array string or comma-separated. Project color for action blocks when project-id set. |

### 4.2 autonomous-distill

| Skill | Slot | Confidence | Config / params |
|-------|-----|------------|------------------|
| **auto-layer-select** (optional) | before distill layers | ≥85% to apply | Suggest 1/2/3 layers from complexity. Override: "distill with 2 layers". |
| **distill-highlight-color** | after distill layers | ≥80% | Same as ingest. |
| **layer-promote** | after highlight | ≥85% | Bold → highlight → TL;DR; complementary for conflicting ideas. |
| **callout-tldr-wrap** | after layer-promote | always | Wrap `## TL;DR` in `> [!summary] TL;DR`. |
| **readability-flag** | at end | ≥70% | Set needs-simplify: true + warning callout if low readability. |

### 4.3 autonomous-archive

| Skill | Slot | Confidence | Config / params |
|-------|-----|------------|------------------|
| **archive-check** | after classify_para | ≥85% for move | Heuristic: no open tasks, status complete, age ≥ age_days / no_activity_days (Second-Brain-Config; else 90/60). Cross-check project subfolder. |
| **subfolder-organize** | before move | ≥85% | Archive path: 4-Archives/{Project-Archive?}/{Subtheme?}/. Same max 4 levels. May be complemented by `obsidian_propose_para_paths` (organize/archive context) for advisory ranked archive suggestions. |
| **resurface-candidate-mark** | before move | ≥75% | resurface-candidate: true; optional append to Resurface hub (hub_names.resurface). |
| **summary-preserve** | before move | ≥80% | Ensure TL;DR or summary callout; light distill if missing; preserve highlights. |

### 4.4 autonomous-express

| Skill | Slot | Confidence | Config / params |
|-------|-----|------------|------------------|
| **version-snapshot** | before major append | ≥85% for write | Path: `Versions/<slug>--<YYYYMMDD-HHMMSS>.md`. obsidian_update_note(..., mode: "create"). Skip if <85%. |
| **related-content-pull** | before outline | ≥80% | global_search by themes/project-id; append ## Related. |
| **express-mini-outline** | after read (optional after related) | ≥85% append | Outline as fenced block; project colors from highlight_key; inline CSS only. |
| **call-to-action-append** | at end | always | Append CTA callout (e.g. `> [!tip] Share/Publish?`). |

### 4.5 autonomous-organize

| Skill / step | Slot | Confidence | Config / params |
|-------------|-----|------------|------------------|
| **classify_para** (MCP) | after backup | — | Re-evaluate para-type, status, themes. |
| **frontmatter-enrich** | after classify_para | ≥85% auto | Same fields as ingest. |
| **subfolder-organize** | after frontmatter-enrich | ≥85% move | Re-org mode: target under 1/2/3 only, not 4-Archives. May be complemented by `obsidian_propose_para_paths` (context_mode `"organize"`) for advisory ranked re-org suggestions without bypassing confidence gates. |
| **obsidian_rename_note** (optional) | after path | ≥85% | Atomic title e.g. YYYY-MM-DD-kebab-slug. Per-change snapshot before. |
| **obsidian_move_note** | after path | ≥85% | ensure_structure(parent) if needed. Per-change snapshot before. |

---

## 5. obsidian-snapshot skill (in-vault snapshots)

Not an MCP tool; skill logic using read_note, update_note, ensure_structure.

| Option | Where | Values / notes |
|--------|--------|------------------|
| **type** | Skill invocation | `per-change` \| `batch` |
| **per-change path** | Skill logic | `SNAPSHOT_DIR/<slug>--<hash>--<YYYYMMDD-HHMMSS>.md.bak` (flattened). |
| **Batch path** | Skill logic | `BATCH_SNAPSHOT_DIR/YYYY-MM-DDTHHMMSSZ-batch-NNNN.md`. |
| **Frontmatter (snapshot)** | Required in snapshot file | original_path, original_title, pipeline, snapshot_type, snapshot_created, snapshot_hash, confidence, flag, immutable: true, para-type: Archive, status: frozen. |
| **Retention (documented)** | snapshot-sweep rule | SNAPSHOT_MAX_DAYS (e.g. 30), SNAPSHOT_MAX_PER_NOTE (e.g. 100). Enforcement in separate sweep; this skill only creates. |
| **Confidence gate** | Skill | Per-change only when destructive action is ≥85%. |

**Env (MCP server):** `SNAPSHOT_DIR`, `BATCH_SNAPSHOT_DIR`, `BACKUP_DIR` — see `~/.cursor/mcp.json` and mcp-obsidian-integration rule.

---

## 6. Subfolder & path conventions

| Convention | Value |
|------------|--------|
| **Max depth** | 4 levels (including filename). |
| **Para roots** | 1-Projects, 2-Areas, 3-Resources, 4-Archives. |
| **Ingest/archive path pattern** | `{root}/{ProjectOrArea?}/{Subtheme?}/{YYYY-MM-DD-title}.md`. |
| **Version file pattern** | `Versions/<original_slug>--<YYYYMMDD-HHMMSS>.md`. |
| **Deep move** | Call obsidian_ensure_structure(folder_path: parent_of_new_path) then obsidian_move_note. |

---

## 7. Quick reference — what to set for a given run

- **Batch size:** Ingest = all Ingest/*.md or filter; Distill ≈ 5; Archive = scoped set; Express = 1–3; Organize = folder or ~5.
- **Backup:** Always create_backup first; include backup path in log_action `changes` and in log file.
- **Confidence:** ≥85% → auto-execute + per-change snapshot; <85% → propose + #review-needed.
- **Logs:** Append to pipeline log (Ingest-Log, Distill-Log, etc.) and to Backup-Log.md when snapshots/backups used.
- **Scope:** Explicit folder for Organize; directory "Ingest" for list_notes in Ingest; exclusions (Backups, Logs, Hubs) per pipeline rule.

For exact tool sequences and rule locations, see [Cursor-Skill-Pipelines-Reference](Cursor-Skill-Pipelines-Reference.md). For hub names and archive thresholds, see [Second-Brain-Config](Second-Brain-Config.md).

---

## 8. Rules — reference

Rules live in `.cursor/rules/always/` (always-applied) and `.cursor/rules/context/` (globs/triggers). They define triggers, scope, safety, and which pipeline or behavior runs.

### 8.1 Always-applied rules

| Rule | Path | Description | Key behavior |
|------|------|--------------|--------------|
| **mcp-obsidian-integration** | `.cursor/rules/always/mcp-obsidian-integration.mdc` | MCP Obsidian integration — tool chaining, logging, safety, fallbacks | Use obsidian-mcp from global config only. Ingest: backup first, then classify → split → distill → append_to_hub → move → log; per-destructive-step snapshot. Prompt→action map (read_note, list_notes, global_search, update_note, manage_frontmatter, etc.). Snapshot chaining (≥85% → snapshot then destructive). Fallback table for move_note / ensure_structure / create_backup. Log to Ingest-Log, Backup-Log. |
| **always-ingest-bootstrap** | `.cursor/rules/always/always-ingest-bootstrap.mdc` | Ensures ingest triggers apply full-autonomous-ingest | When user says "INGEST MODE", "Process Ingest", or "run ingests": run ingest-processing first (non-MD + embedded normalization), then full-autonomous-ingest on Ingest/*.md per pipeline reference. List via obsidian_list_notes("Ingest"). |
| **00-always-core** | `.cursor/rules/always/00-always-core.mdc` | Core persona and always-on Ingest awareness | Thoth-AI persona. All new/unknown files arrive in Ingest/; check Ingest/ first; move out after companion .md in PARA. Frontmatter on every new .md. |
| **second-brain-standards** | `.cursor/rules/always/second-brain-standards.mdc` | PARA, linking, frontmatter, atomicity | PARA strictly (1–4); searchable title, frontmatter, tags; atomic notes; attachment syntax; daily date in filename when created today. |

### 8.2 Context rules (triggers & globs)

| Rule | Path | Globs | Description | Triggers / when |
|------|------|-------|-------------|-----------------|
| **para-zettel-autopilot** | `.cursor/rules/context/para-zettel-autopilot.mdc` | `Ingest/*.md` | Master ingest rule — PARA + Zettel pipeline for Ingest/*.md; overrides conflicting rules | Ingest pipeline: backup → classify → frontmatter-enrich → subfolder-organize → split_atomic → split-link-preserve → distill → distill-highlight-color → next-action-extract → append_to_hub → move → log. ≥85% auto; <85% #review-needed. Batch limit ~5; per-note isolation. |
| **ingest-processing** | `.cursor/rules/context/ingest-processing.mdc` | `Ingest/**` | Ingest folder processing and non-MD handling | List Ingest; non-.md → companion .md per non-markdown-handling; embedded image normalization (rewrite to 5-Attachments/Images/, callout + tags #needs-attachment-relocation, #attachment-relocation-pending). No move_note on binaries. |
| **non-markdown-handling** | `.cursor/rules/context/non-markdown-handling.mdc` | `Ingest/**` | Non-MD file-type handling and companion note creation | Create companion .md for non-.md in Ingest; place in PARA; do not move binary; add embeds; user moves file manually. |
| **auto-distill** | `.cursor/rules/context/auto-distill.mdc` | 1-Projects/**/*.md, 2-Areas/**/*.md, 3-Resources/**/*.md; !4-Archives, !Backups, !Templates, !**/Log*.md, !**/* Hub.md | Binds triggers to autonomous-distill pipeline | "DISTILL MODE – safe batch autopilot", "distill this note", "refine this note". Backup → (auto-layer-select) → distill layers → distill-highlight-color → layer-promote → callout-tldr-wrap → readability-flag → log. |
| **auto-archive** | `.cursor/rules/context/auto-archive.mdc` | Same as auto-distill | Binds triggers to autonomous-archive pipeline | "ARCHIVE MODE – safe batch autopilot", "archive this note", "send to Archives". backup → classify_para → archive-check → subfolder-organize → resurface-candidate-mark → summary-preserve → move_note → log. |
| **auto-express** | `.cursor/rules/context/auto-express.mdc` | Same + !**/Versions/** | Binds triggers to autonomous-express pipeline | "EXPRESS MODE – safe batch autopilot", "express this note", "generate outline". backup → version-snapshot → related-content-pull → express-mini-outline → call-to-action-append → log. |
| **auto-organize** | `.cursor/rules/context/auto-organize.mdc` | Same as auto-distill (no Versions exclude) | Binds triggers to autonomous-organize pipeline | "ORGANIZE MODE – safe batch autopilot on [folder]", "re-organize", "classify and move". backup → classify_para → frontmatter-enrich → subfolder-organize → (rename_note) → move_note → log. |
| **auto-restore** | `.cursor/rules/context/auto-restore.mdc` | `*` | Trigger-based restore from in-vault snapshots | "RESTORE MODE – rollback last change", "restore from snapshot". Scope note → read Restore Hub + Backup-Log → list candidate snapshots → user picks → integrity check (snapshot_hash) → overwrite original → log. No auto-restore without user request. |
| **snapshot-sweep** | `.cursor/rules/context/snapshot-sweep.mdc` | `Backups/Per-Change/*.md.bak` | Trigger-based snapshot retention / cleanup | "SNAPSHOT SWEEP", "Clean old snapshots". Use SNAPSHOT_MAX_DAYS, SNAPSHOT_MAX_PER_NOTE; move aged/excess to Backups/Archives/; log to Backup-Log. Deletion only when user explicitly requests. |
| **auto-resurface** | `.cursor/rules/context/auto-resurface.mdc` | `Resurface.md` | Resurface candidates — listing and hub append | "Resurface", "show resurface candidates". global_search for resurface-candidate: true; present list; optionally append to Resurface hub. Trigger-based only. |

### 8.3 Rule → pipeline mapping

| Trigger / phrase | Rule(s) | Pipeline |
|------------------|---------|----------|
| "INGEST MODE", "Process Ingest", "run ingests" | always-ingest-bootstrap, para-zettel-autopilot, mcp-obsidian-integration | full-autonomous-ingest |
| Ingest/*.md (open or batch) | para-zettel-autopilot | full-autonomous-ingest |
| "DISTILL MODE", "distill this note", "refine" | auto-distill | autonomous-distill |
| "ARCHIVE MODE", "archive this note", "send to Archives" | auto-archive | autonomous-archive |
| "EXPRESS MODE", "express this note", "generate outline" | auto-express | autonomous-express |
| "ORGANIZE MODE", "re-organize", "classify and move" | auto-organize | autonomous-organize |
| "RESTORE MODE", "restore from snapshot" | auto-restore | — (restore flow) |
| "SNAPSHOT SWEEP", "Clean old snapshots" | snapshot-sweep | — (sweep flow) |
| "Resurface", "show resurface candidates" | auto-resurface | — |

---

## 9. Skills — full index

Each skill is a `.cursor/skills/<name>/SKILL.md` file. They are invoked during pipelines (no separate MCP tool). Below: path, pipeline(s), when to use, MCP tools used, and main config/params.

| Skill | Path | Pipeline(s) | When to use | MCP tools used | Confidence | Main config / params |
|-------|------|-------------|-------------|----------------|------------|----------------------|
| **frontmatter-enrich** | `.cursor/skills/frontmatter-enrich/SKILL.md` | ingest, organize | After classify_para | read_note, manage_frontmatter | ≥85% auto | status, confidence, para-type, created, links (YAML array); optional project-id, priority, deadline. links = array; project MOC in links when project-id set. |
| **subfolder-organize** | `.cursor/skills/subfolder-organize/SKILL.md` | ingest, archive, organize | After frontmatter-enrich (ingest/organize) or before move (archive) | read_note, ensure_structure, move_note | ≥85% move | Max 4 levels. Ingest/org: {para-root}/{Project?}/{Subtheme?}/{date-title}.md. Archive: 4-Archives/…. Re-org: target under 1/2/3 only. |
| **split-link-preserve** | `.cursor/skills/split-link-preserve/SKILL.md` | ingest | After split_atomic | read_note, manage_frontmatter, update_note, search_replace, list_notes | ≥85% | Child: split_from, related (append). Parent: ## Splits with `- [[Child]] — reason` (~60 chars); optional split_into. Idempotent. |
| **distill-highlight-color** | `.cursor/skills/distill-highlight-color/SKILL.md` | ingest, distill | After distill_note (ingest) or distill layers (distill) | read_note, search_replace, update_note | ≥80% | Highlightr-Color-Key.md + note highlight_key. Inline CSS or key class format only. Analogous/complementary color theory. |
| **next-action-extract** | `.cursor/skills/next-action-extract/SKILL.md` | ingest | After distill-highlight-color | read_note, search_replace, manage_frontmatter | ≥85% | Checklists in body; next-actions frontmatter (JSON array string or comma-sep). Project color for action blocks when project-id set. |
| **auto-layer-select** | `.cursor/skills/auto-layer-select/SKILL.md` | distill | Optional, before distill layers | read_note | ≥85% to apply | Suggest 1/2/3 layers from complexity. Manual override: "distill with 2 layers". |
| **layer-promote** | `.cursor/skills/layer-promote/SKILL.md` | distill | After distill-highlight-color | read_note, search_replace | ≥85% | Bold → highlight → TL;DR; complementary for conflicting ideas; project color overrides. |
| **callout-tldr-wrap** | `.cursor/skills/callout-tldr-wrap/SKILL.md` | distill | After layer-promote | read_note, search_replace | always | Wrap ## TL;DR in `> [!summary] TL;DR`. |
| **readability-flag** | `.cursor/skills/readability-flag/SKILL.md` | distill | End of distill pipeline | read_note, manage_frontmatter, search_replace | ≥70% | needs-simplify: true + warning callout if low readability. |
| **archive-check** | `.cursor/skills/archive-check/SKILL.md` | archive | After classify_para | read_note, list_notes, global_search | ≥85% for move | Heuristic: no open tasks, status complete, age ≥ age_days/no_activity_days (Second-Brain-Config; else 90/60). Cross-check project subfolder. |
| **resurface-candidate-mark** | `.cursor/skills/resurface-candidate-mark/SKILL.md` | archive | Before move (after subfolder-organize) | read_note, manage_frontmatter, append_to_hub | ≥75% | resurface-candidate: true; optional append to Resurface hub (hub_names.resurface). |
| **summary-preserve** | `.cursor/skills/summary-preserve/SKILL.md` | archive | Before move | read_note, distill_note, search_replace | ≥80% | Ensure TL;DR or summary callout; light distill if missing; preserve highlights. |
| **version-snapshot** | `.cursor/skills/version-snapshot/SKILL.md` | express | Before any major append | read_note, update_note(mode: create), ensure_structure | ≥85% for write | Versions/<slug>--<YYYYMMDD-HHMMSS>.md. Skip if <85%. |
| **related-content-pull** | `.cursor/skills/related-content-pull/SKILL.md` | express | Before express-mini-outline | read_note, global_search, update_note(append) | ≥80% | ## Related from themes/project-id search. |
| **express-mini-outline** | `.cursor/skills/express-mini-outline/SKILL.md` | express | After read (optional after related) | read_note, update_note(append) | ≥85% append | Outline as fenced block; project colors; inline CSS only. |
| **call-to-action-append** | `.cursor/skills/call-to-action-append/SKILL.md` | express | End of express pipeline | update_note(append) | always | CTA callout e.g. `> [!tip] Share/Publish?`. |
| **obsidian-snapshot** | `.cursor/skills/obsidian-snapshot/SKILL.md` | all pipelines | Before destructive steps (see §5) | read_note, update_note, ensure_structure | when action ≥85% | type: per-change | batch. Flattened paths; snapshot_hash; log Backup-Log. Retention: SNAPSHOT_MAX_DAYS, SNAPSHOT_MAX_PER_NOTE (sweep rule). |

### 9.1 Skill → pipeline summary

- **Ingest:** frontmatter-enrich, subfolder-organize, split-link-preserve, distill-highlight-color, next-action-extract.
- **Distill:** auto-layer-select (optional), distill-highlight-color, layer-promote, callout-tldr-wrap, readability-flag.
- **Archive:** archive-check, subfolder-organize, resurface-candidate-mark, summary-preserve.
- **Express:** version-snapshot, related-content-pull, express-mini-outline, call-to-action-append.
- **Organize:** frontmatter-enrich, subfolder-organize (+ optional rename_note, move_note).
- **Cross-pipeline:** obsidian-snapshot (per-change and batch before destructive steps).
