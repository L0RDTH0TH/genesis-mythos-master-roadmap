---
title: Responsibilities Breakdown
created: 2026-03-05
tags: [second-brain, pipelines, skills, rules, responsibilities, reference]
para-type: Resource
status: active
links:
  - "[[3-Resources/Second-Brain/Pipelines]]"
  - "[[3-Resources/Second-Brain/Skills]]"
  - "[[3-Resources/Second-Brain/Rules]]"
  - "[[3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference]]"
---

# Responsibilities Breakdown

This document outlines **what each pipeline, skill, and rule is responsible for**—what it performs and what it enforces. Use it to avoid overlap, assign ownership, and debug “who should do what.”

---

## 1. Pipelines

Pipelines are end-to-end flows triggered by a phrase or queue mode. Each has a primary responsibility and may delegate to skills/rules.

### full-autonomous-ingest

| Responsibility | What it performs / enforces |
|----------------|-----------------------------|
| **Capture** | Ensures every Ingest note is read, classified (PARA), and enriched; no note left in raw form without at least minimal distill before any move. |
| **Classify & propose** | Runs classify_para → frontmatter-enrich → name-enhance (propose only) → subfolder-organize to produce a ranked path proposal; **post-process stabilizer:** re-rank by PARA-Actionability-Rubric v1.0, pad to 7 (mandatory), set heuristic_adjusted/heuristic_reason when order changed; uses confidence bands to decide in-note work (split, distill, hub append, task-reroute) vs. propose-only. |
| **Decision Wrapper** | Creates/refreshes a single Decision Wrapper type (A–G from propose_para_paths; pad to 7 with deterministic fallbacks) under `Ingest/Decisions/Ingest-Decisions/`; never moves/renames in Phase 1. |
| **Apply-mode (Phase 2)** | When a wrapper is approved (EAT-QUEUE Step 0), runs guidance-aware ingest: move/rename original note to user-approved PARA path only; no roadmap tree creation from ingest. |
| **Safety** | Enforces backup before run; per-change snapshots before split, distill, append_to_hub, task-reroute, and (in Phase 2) move/rename; dry_run before move_note; confidence gates (≥85% for destructive in-note, ≥78% for safe cross-note). |

### Queue processor (EAT-QUEUE)

| Responsibility | What it performs / enforces |
|----------------|-----------------------------|
| **Read & validate** | Reads `.technical/prompt-queue.jsonl` (or EAT-CACHE payload); parses and validates entries; filters queue_failed; requires `mode`. |
| **Order** | Pins CHECK_WRAPPERS to front; sorts remaining by canonical pipeline order; **post-process stabilizer:** when originating note conf ≥ 90%, bump TASK-ROADMAP (and EXPAND-ROAD / TASK-TO-PLAN-PROMPT) after ORGANIZE, before DISTILL; log queue_order_adjusted, reason. |
| **Step 0 (always-check wrappers)** | Enumerates `Ingest/Decisions/**`; for approved or re-wrap wrappers not yet processed: runs feedback-incorporate → re-wrap branch (archive + new wrapper) or path-apply (apply-mode ingest move/rename only); for processed wrappers still in Decisions, runs location check → archive or tag #orphan/#true-orphan. |
| **Dispatch** | Maps each entry’s `mode` to the correct pipeline (INGEST MODE → full-autonomous-ingest, DISTILL MODE → autonomous-distill, etc.); runs one entry fully before the next. |
| **Log & clear** | Appends one line per request to Watcher-Result.md; rewrites queue file (remove passed, keep failed/skipped with queue_failed: true); re-inserts CHECK_WRAPPERS entry when approved_wrappers_remaining. |

### Task/roadmap queue (PROCESS TASK QUEUE)

| Responsibility | What it performs / enforces |
|----------------|-----------------------------|
| **Read Task-Queue** | Reads Task-Queue.md (or equivalent); parses entries by mode. |
| **Dispatch task modes** | TASK-ROADMAP, TASK-COMPLETE, ADD-ROADMAP-ITEM, EXPAND-ROAD, etc. → invokes corresponding skills (task-complete-validate, add-roadmap-append, expand-road-assist, etc.). |
| **Result** | Watcher-Result + Mobile-Pending-Actions; optional banner cleanup (success > failure). |

### autonomous-distill

| Responsibility | What it performs / enforces |
|----------------|-----------------------------|
| **Refine structure** | Runs distill layers (bold → highlight → TL;DR), then highlight color, perspective layer, layer-promote, perspective-refine, callout-tldr-wrap, readability-flag. **Post-process stabilizer:** short-note core bias (config), emoji fallback only when mobile context detected; log heuristic in Distill-Log. |
| **Depth control** | Optional auto-layer-select (1/2/3 layers from complexity); distill_lens from frontmatter shapes depth/drift indicators; confidence bands (distill_conf) gate structural edits. |
| **Safety** | Backup before run; per-change snapshot before first structural rewrite; excludes Backups/Logs/Hubs. |

### autonomous-archive

| Responsibility | What it performs / enforces |
|----------------|-----------------------------|
| **Archive readiness** | Runs archive-check (no open tasks, status complete, age threshold; archive_conf); cross-checks project subfolders. **Post-process stabilizer:** when age > no_activity_days and (#stale or #review-later), raise confidence floor +5–8%; never when status active/evergreen. |
| **Path & preserve** | subfolder-organize → archive path (e.g. 4-Archives/Project-X-Archive/); resurface-candidate-mark; summary-preserve (TL;DR/summary callout, project color links). |
| **Move** | ensure_structure(parent of target) → move_note dry_run then commit; only when archive_conf ≥85% (or post_loop_conf after mid-band loop). |
| **Safety** | Backup; per-change snapshot before move; dry_run before commit. |

### autonomous-express

| Responsibility | What it performs / enforces |
|----------------|-----------------------------|
| **Version & relate** | version-snapshot (dated copy in Versions/) before major appends; related-content-pull (semantic + project-id) → Related section. |
| **Scoping (PMG)** | When note is a PMG, **research-scope** runs after related-content-pull: aggregate Resources by project-id/phases; propose-first callout with source citation; commit ## Scoped Resources only on second pass when approved. Scoping the "road to goal" = run DISTILL then EXPRESS on the PMG (or use SCOPING MODE queue alias). |
| **Outline & CTA** | express-mini-outline (summary/outline, project colors); express-view-layer when express_view set; call-to-action-append at end. |
| **Safety** | Backup; version-snapshot before large appends; excludes Archives/Backups/Versions. |

### autonomous-organize

| Responsibility | What it performs / enforces |
|----------------|-----------------------------|
| **Re-classify** | classify_para → frontmatter-enrich → subfolder-organize → name-enhance (organize context; optional rename) for notes already in PARA. |
| **Move within PARA** | ensure_structure(parent of target) → move_note dry_run then commit when confidence ≥85%. |
| **Safety** | Backup; per-change snapshot before rename and move; dry_run before commit. |

### Queue-driven batch / special modes

| Pipeline / mode | Responsibility |
|-----------------|----------------|
| **BATCH-DISTILL / BATCH-EXPRESS** | Same as autonomous-distill / autonomous-express but on multiple notes from queue; batch snapshot when batch size > threshold. |
| **NAME-REVIEW** | name-enhance in batch on scope (folder/paths); apply renames when confidence ≥85% and not protected; log to Name-Review-Log. |
| **SEEDED-ENHANCE** | highlight-seed-enhance on note with user `<mark>`; backup + snapshot before edits. |
| **ASYNC-LOOP** | Re-process after async preview (user approved or feedback); feedback-incorporate → snapshot + commit if post_loop_conf ≥85%. |
| **SCOPING MODE** | Queue alias: run DISTILL MODE then EXPRESS MODE on same note (PMG path from source_file); research-scope runs inside express. |
| **FORCE-WRAPPER** | Create Decision Wrapper instead of destructive step; apply when user approves via Step 0. |

---

## 2. Skills

Skills are discrete units of work invoked within a pipeline or by a queue mode. Each has a clear “slot” (after which step) and confidence/usage conditions.

### Ingest

| Skill | Performs | Enforces / gates |
|-------|----------|------------------|
| **prompt-crafter** | Assemble/validate params from config/templates; inject into queue or pipeline context. | Doc-only / optional skill; slots before classify_para when implemented; config read, template concat, queue append; owns validation but delegates MCP calls. |
| **frontmatter-enrich** | Sets status, confidence, para-type, created, links (hub + related); optional project-id, priority, deadline from classification. | Runs after classify_para; no move. |
| **name-enhance** | Proposes (ingest) or applies (organize/NAME-REVIEW) better filename; protects MOC/hub/index/project from auto-rename. | Ingest: propose only; organize/name-review: apply with snapshot when confidence tier met. |
| **subfolder-organize** | Builds target path (max 4 levels) from para-type + project-id + themes; accepts suggested_filename; path segment per Naming-Conventions. | Used by ingest (path proposal), archive, organize; move via MCP only when pipeline commits. |
| **split-link-preserve** | Writes split_from on each child; split_into or Splits section on parent. | After split_atomic; traceability only. |
| **distill-highlight-color** | Applies Highlightr colors from master key + project highlight_key; 50–70% coverage; perspective/lens. | After distill_note; analogous/complementary; log coverage_adapted. |
| **next-action-extract** | Extracts tasks → checklists + next-actions frontmatter for Dataview. | After distill-highlight-color. |
| **task-reroute** | find_parent; create task note or append_tasks to existing note; snapshot target before append. | When task-like and confidence ≥78%; no append without snapshot. |
| **link-to-pmg-if-applicable** | When note has project-id, find PMG in project folder and append PMG wikilink to note's links array. | After append_to_hub; only append to current note; never edit PMG. |

### Distill

| Skill | Performs | Enforces / gates |
|-------|----------|------------------|
| **auto-layer-select** | Suggests 1/2/3 layers from content complexity. | Optional; manual override remains; ≥85% to auto-apply. |
| **highlight-perspective-layer** | Sets data-drift-level (0–3); store highlight_angles in frontmatter. | After distill-highlight-color; log to Distill-Log. |
| **layer-promote** | Promotes bold → highlight → TL;DR; project color overrides; contrast for conflicting ideas. | After highlight-perspective-layer or distill-highlight-color. |
| **callout-tldr-wrap** | Wraps TL;DR in `> [!summary] TL;DR` callout. | After layer-promote. |
| **distill-perspective-refine** | Adds emojis/gradient in TL;DR for depth/drift; uses distill_lens when set. | After layer-promote; log lens + gradient. |
| **readability-flag** | Sets needs-simplify frontmatter; inserts warning callout when readability low. | At end of distill pipeline. |

### Archive

| Skill | Performs | Enforces / gates |
|-------|----------|------------------|
| **archive-check** | Evaluates no open tasks, status complete, age threshold; cross-checks project subfolders; outputs archive_conf. | After classify_para; primary signal for archive move. |
| **resurface-candidate-mark** | Marks high-potential notes (links/highlights) with resurface-candidate: true; optional Resurface hub append. | Before move. |
| **summary-preserve** | Ensures minimal TL;DR/summary callout; preserves project color links before move. | Before move. |

### Express

| Skill | Performs | Enforces / gates |
|-------|----------|------------------|
| **version-snapshot** | Creates dated snapshot in Versions/ before major append; mode create; preserves original content and colors. | Before related-content-pull and large appends. |
| **related-content-pull** | Pulls similar notes (semantic + project-id); appends Related section; color-theory emphasis. | After version-snapshot. |
| **research-scope** | When note is PMG: search 3-Resources by project-id/phases; propose-first callout with source citation; commit ## Scoped Resources on second pass when approved. | After related-content-pull; ≥85% propose + optional link-back; 68–84% callout only; <68% log only. |
| **express-mini-outline** | Generates outline/summary; project colors for sections; express_view shapes outline. | After related-content-pull. |
| **express-view-layer** | Applies connection strength indicators in Related when express_view set; log to Express-Log. | After related-content-pull or express-mini-outline. |
| **call-to-action-append** | Appends CTA callout at end (e.g. Share/Publish?); optional color by action type or project. | After express-mini-outline. |

### Queue / task / roadmap

| Skill | Performs | Enforces / gates |
|-------|----------|------------------|
| **feedback-incorporate** | Scans queue/Mobile-Pending-Actions for approved or feedback; loads user_guidance; interprets Decision Wrappers (approved_path, re-wrap/option 0); emits hard_target_path, guidance_text, guidance_conf_boost. | No destructive writes; used by ingest/organize/distill when guidance-aware. |
| **roadmap-generate-from-outline** | Creates project folder + Roadmap subtree, master roadmap, per-phase notes, project MOC; moves seed into Roadmap/Source; sets provenance and roadmap_generation_status. | Trigger: ROADMAP MODE – generate from outline or dedicated queue mode; not from ingest. |
| **roadmap-checklist** | Produces hierarchical checklist from roadmap note + [[links]]; optional flatten, status-sync. | Queue or manual. |
| **roadmap-ingest** | Parses roadmap from queue path; standardizes phases/tasks. | Queue. |
| **add-roadmap-append** | Appends one line to primary roadmap under chosen section; optional duplicate check. | Queue (ADD-ROADMAP-ITEM). |
| **expand-road-assist** | Parses user text into sub-phases/tasks; appends under target section; links back to roadmap. | Queue (EXPAND-ROAD). |
| **task-complete-validate** | Locates task; detects subtasks; marks [x] only when all subtasks complete. | Queue (TASK-COMPLETE). |
| **queue-cleanup** | Marks failed entries queue_failed: true; appends summary to Errors.md. | After dedup when auto_cleanup_after_process; no reprocess of failed. |
| **distill-apply-from-wrapper** | Re-runs autonomous-distill with approved_option as distill_lens on wrapper’s original_path. | Step 0 when applying approved refinement wrapper (pipeline: distill). |
| **express-apply-from-wrapper** | Re-runs autonomous-express with approved_option as express_view on wrapper’s original_path. | Step 0 when applying approved refinement wrapper (pipeline: express). |

### Cross-cutting

| Skill | Performs | Enforces / gates |
|-------|----------|------------------|
| **obsidian-snapshot** | Creates per-change or batch snapshot in Backups/ before destructive MCP action; retention guidance. | All pipelines; before split, distill rewrite, append_to_hub, move_note, rename_note. |
| **highlight-seed-enhance** | Treats user `<mark>` as cores; extends with AI highlights (analogous color; optional drift). | SEEDED-ENHANCE queue or trigger only; no auto-run on save. |
| **log-rotate** | Copies pipeline logs to Logs-Archive/; truncates or starts fresh. | Manual or “Rotate logs” command. |
| **move-attachment-to-99** | Fallback move Ingest → 5-Attachments when MCP move_note fails for binaries; updates companion .md. | User-invoked only; backup → ensure_structure → mv; scope Ingest/ → 5-Attachments/[subtype]. |

---

## 3. Rules

Rules define persona, safety, and when which pipeline runs. **Always-applied** rules run on every relevant context; **context** rules run when their trigger or glob matches.

### Always-applied rules

| Rule | Performs | Enforces |
|------|----------|----------|
| **00-always-core** | Sets persona (Thoth-AI); Ingest-first behavior. | All new/unknown files start in Ingest/; frontmatter (created, tags) on every new .md. |
| **mcp-obsidian-integration** | Defines backup/snapshot gates, dry_run before move, Error Handling Protocol, fallback table (ensure_structure, propose_alternative_paths). | No destructive action without backup; dry_run before move_note; errors → Errors.md with trace/summary; ensure_structure before every move. |
| **second-brain-standards** | Defines PARA, atomic notes, attachment syntax, naming. | PARA structure; atomic notes; `![[5-Attachments/...]]`; searchable title and tags. |
| **confidence-loops** | Defines bands (≥85, 68–84, <68); single non-destructive refinement loop in mid-band; loop_* fields in logs. | One loop per note per run; post_loop_conf > pre_loop_conf to proceed; decay rule. |
| **guidance-aware** | Loads user_guidance or queue prompt; passes to classify_para, subfolder-organize, name-enhance, distill_note, split_atomic; length cap 500 words; optional guidance_conf_boost. | Guidance is soft hint only; never overrides safety or confidence gates; log guidance_used, guidance_truncated, guidance_ignored. |
| **always-ingest-bootstrap** | On INGEST MODE / Process Ingest: lists Ingest notes, runs full-autonomous-ingest. | Ensures ingest pipeline runs when user asks for it. |
| **watcher-result-append** | Appends one line per request to Watcher-Result.md (requestId, status, message, trace, completed). | On run finish (Watcher or EAT-QUEUE); enables lag estimation. |
| **backbone-docs-sync** | Maps rule/skill changes to Second-Brain docs (Rules, Skills, Pipelines, Logs, etc.); syncs to .cursor/sync/. | When rules/skills change, update docs and sync folder; refresh diagrams. |

### Context rules (triggered)

| Rule | Trigger / glob | Performs | Enforces |
|------|----------------|----------|----------|
| **para-zettel-autopilot** | `Ingest/*.md` | Runs full-autonomous-ingest: backup → classify → enrich → … → Decision Wrapper (A–G from propose_para_paths); Phase 2 apply-mode only via approved wrapper. | No move/rename in Phase 1; single wrapper type (Ingest-Decisions only); confidence gates for in-note vs. propose-only. |
| **auto-eat-queue** | EAT-QUEUE, Process queue, eat cache / EAT-CACHE | Reads queue; validates; dedups/sorts; Step 0 always-check wrappers (re-wrap or apply-mode ingest); dispatches by mode; Watcher-Result; clear passed only. | CHECK_WRAPPERS first; path-apply = apply-mode ingest only (no roadmap tree from ingest). |
| **auto-queue-processor** | PROCESS TASK QUEUE | Reads Task-Queue.md; dispatches TASK-ROADMAP, TASK-COMPLETE, ADD-ROADMAP-ITEM, etc.; Watcher-Result + Mobile-Pending-Actions. | Task/roadmap modes only. |
| **auto-distill** | DISTILL MODE, distill note/vault | Runs autonomous-distill: backup → (auto-layer-select) → distill layers → highlight → layer-promote → callout-tldr-wrap → readability-flag. | Excludes Backups/Logs/Hubs; snapshot before structural edits. |
| **auto-archive** | ARCHIVE MODE, archive, #eaten | Runs autonomous-archive: archive-check → subfolder-organize → resurface-mark → summary-preserve → move (dry_run then commit). | Only when archive_conf ≥85% (or post_loop_conf); dry_run before commit. |
| **auto-express** | EXPRESS MODE, express note | Runs autonomous-express: version-snapshot → related-content-pull → express-mini-outline → call-to-action-append. | Excludes Archives/Backups/Versions. |
| **auto-organize** | ORGANIZE MODE, re-organize | Re-classifies and moves within PARA; frontmatter-enrich → subfolder-organize → name-enhance (optional rename) → move (dry_run then commit). | Confidence ≥85% for move/rename; snapshot before. |
| **ingest-processing** | Non-MD in Ingest; embedded normalization | Normalizes embedded images; creates companion .md for non-.md; runs before full ingest on Ingest/*.md. | Pre-step only; no move of binaries from ingest pipeline. |
| **non-markdown-handling** | Non-.md in Ingest | Creates companion .md; leaves original in Ingest/ with #needs-manual-move. | No move_note on binaries; user or move-attachment skill for binaries. |
| **snapshot-sweep** | Snapshot cleanup / retention | User-triggered retention/cleanup of Backups/Per-Change and Backups/Batch. | User-triggered only. |
| **auto-restore** | Restore from snapshot/backup | User-triggered restore from snapshot or BACKUP_DIR. | User-triggered only. |
| **auto-resurface** | Resurface, show resurface candidates | Surfaces notes marked resurface-candidate; optional Resurface hub. | Read/display only. |
| **auto-highlight-perspective** | HIGHLIGHT PERSPECTIVE: [lens] | Sets highlight_perspective or queue payload; runs distill with perspective so distill-highlight-color uses lens. | Context only. |
| **mobile-seed-detect** | SEEDED-ENHANCE, "Enhance highlights from seeds" | Allows highlight-seed-enhance only when triggered or queued; user <mark> as cores. | No auto-run on save. |
| **auto-distill-perspective** | DISTILL LENS: [angle] | Sets distill_lens frontmatter; runs autonomous-distill with lens for depth/TL;DR indicators. | Context only. |
| **auto-express-view** | EXPRESS VIEW: [angle] | Sets express_view frontmatter; runs autonomous-express; express-view-layer shapes Related. | Context only. |
| **auto-async-cascade** | EAT-QUEUE when queue >3 entries | Proposes batch run to Mobile-Pending-Actions; user confirms BATCH-DISTILL/BATCH-EXPRESS. | Propose only; no auto-batch without user confirm. |

---

## 4. Responsibility boundaries (summary)

| Domain | Owned by | Not owned by |
|--------|----------|--------------|
| **Capture & place (ingest)** | full-autonomous-ingest, para-zettel-autopilot; Decision Wrapper A–G; apply-mode move/rename to approved path only | Roadmap tree creation (that’s ROADMAP MODE / roadmap-generate-from-outline) |
| **Refine (distill)** | autonomous-distill, auto-distill; layers, highlight, TL;DR, readability | Move/rename (ingest/organize/archive) |
| **Archive** | autonomous-archive, archive-check, summary-preserve, resurface-candidate-mark | Ingest, express, roadmap |
| **Express** | autonomous-express; version-snapshot, related-content, outline, CTA | Move/rename; distill structural rewrite |
| **Re-place (organize)** | autonomous-organize; re-classify, move within PARA | Ingest (first-time place); archive |
| **Queue & dispatch** | auto-eat-queue; Step 0 wrappers, ordering, dispatch, Watcher-Result | Pipeline internals (each pipeline owns its steps) |
| **Safety (backup, snapshot, dry_run)** | mcp-obsidian-integration; obsidian-snapshot skill; each pipeline’s backup/snapshot steps | No rule “does” backup alone—pipelines and MCP gate call it |
| **Decision Wrappers** | para-zettel-autopilot (create); auto-eat-queue Step 0 (apply/re-wrap/archive); feedback-incorporate (resolve path) | Watcher only syncs checkbox → frontmatter when approved: true already set; never sets approved or re-wrap |

For pipeline order, skill slots, and confidence gates in detail, see [[3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference]].

