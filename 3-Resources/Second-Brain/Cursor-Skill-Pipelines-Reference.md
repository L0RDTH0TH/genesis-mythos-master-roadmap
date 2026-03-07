---
title: Cursor Skill Pipelines Reference
created: 2026-02-25
tags: [pkm, cursor, second-brain, pipelines, skills]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[Second-Brain-Automation-Recommendations]]"]
---

# Cursor Skill Pipelines Reference

**Single Pipelines-and-Rules-Reference** for the autonomous skill pipelines (full-autonomous-ingest, autonomous-distill, autonomous-archive, autonomous-express, autonomous-organize), trigger → rule mapping, and skills. Skills live in **`.cursor/skills/<skill-name>/`**; Phase 2 always-applied rules and Phase 3 context-specific rules define triggers and safety (backup-first, no shell vault ops).

**Documentation map**: Summary tables and cheat sheets live in the Second-Brain folder — [[3-Resources/Second-Brain/README|README]] (trigger cheat sheet, troubleshooting, mental model), [[3-Resources/Second-Brain/Pipelines|Pipelines]] (trigger → pipeline, snapshot triggers summary, usage examples), [[3-Resources/Second-Brain/Logs|Logs]] (log destinations, example log line, log → MOC flow). This file is the **canonical** source for pipeline order, skill slots, confidence gates, and the full snapshot triggers table.

**Conventions**:
- Skills use frontmatter **`highlight_key`** for project overrides; fallback to master key in [Highlightr-Color-Key.md](Highlightr-Color-Key.md). See that note for **Project-Specific Guidelines** (when added) and color semantics.
- Subfolder depth **≤4** levels; paths derived from **`project-id`** + semantic themes.
- **Path before every move**: Before any **`obsidian_move_note`**, call **`obsidian_ensure_structure`**(folder_path: *parent of new_path*) so the target path exists (create if missing). Then **Move and dry_run**: for any **`obsidian_move_note`** at ≥85% confidence, move is always **"`dry_run` first, then commit"** — call with `dry_run: true`, review effects (path, new_path, backup status, risks), then call with `dry_run: false` to commit. After every successful move (dry_run: false), set **para-type** on the note at the new path from the first path segment (1-Projects→Project, 2-Areas→Area, 3-Resources→Resource, 4-Archives→Archive); when under 1-Projects/ set **project-id** from the second segment; when under 4-Archives/ set **status: archived**. Use obsidian_manage_frontmatter; see mcp-obsidian-integration. See MCP fallback table in mcp-obsidian-integration.mdc for dry_run/move-failure fallback.
- Confidence **bands** and snapshots:
  - **High-confidence (proceed)**: \(\ge 85\%\) — destructive actions (move, rename, split, structural distill, large appends) are allowed **only** in this band and only after a successful per-change snapshot (see `obsidian-snapshot` skill).
  - **Mid-band (loop)**: \(68\% \le conf \le 84\%\) — triggers a single, non-destructive refinement loop (self-critique) per note per pipeline run.
  - **Low-confidence**: \(<68\%\) — no loop; propose-only behavior that flows into **user decision loops** (Decision Wrappers for ingest, async preview + approval for other pipelines) instead of auto-applying changes.

---

## Trigger → rule mapping

| Trigger / phrase | Rule(s) | Pipeline |
|------------------|---------|----------|
| **EAT-QUEUE**, "Process queue", **eat cache** / **EAT-CACHE**, or pasted EAT-CACHE payload | auto-eat-queue | **Queue processor**: read `.technical/prompt-queue.jsonl` → validate → fast-path if single entry → dedup → sort → dispatch by mode → Watcher-Result → clear passed only; optional queue-cleanup (auto_cleanup_after_process); tag failed with `queue_failed: true` |
| **EAT-QUEUE**, **PROCESS TASK QUEUE** (task/roadmap queue) | auto-queue-processor | Read Task-Queue.md → fast-path if single entry → dispatch by mode (TASK-ROADMAP, TASK-COMPLETE, …) → Watcher-Result + Mobile-Pending-Actions → banner cleanup (success > failure) |
| "Ingest", "process Ingest", "run ingests" | always-ingest-bootstrap, para-zettel-autopilot | full-autonomous-ingest |
| Ingest/*.md (open or batch) | para-zettel-autopilot | full-autonomous-ingest |
| #raw-ingest, status: raw | ingest-processing (pre-step; propose only) | — |
| "Distill", "distill note/vault" | auto-distill | autonomous-distill |
| "Archive", #eaten, complete | auto-archive | autonomous-archive |
| "Organize", "re-organize", "ORGANIZE MODE" | auto-organize | autonomous-organize |
| "Resurface", "show resurface candidates" | auto-resurface | — |
| "GARDEN REVIEW", "run garden review", "orphans and distill candidates", "garden health", "vault orphans", "distill candidates sweep" | auto-garden-review | Garden review flow: `obsidian_garden_review` → feed to distill/organize batches; queue mode **GARDEN-REVIEW** |
| "CURATE CLUSTER #tag", "suggest gaps and merges", "cluster curate #tag", "theme gaps #tag", "merge suggestions 3-Resources/…" | auto-curate-cluster | Curate cluster flow: `obsidian_curate_cluster` → gaps/merges/synthesis → optional split/MOC/merge; queue mode **CURATE-CLUSTER** |
| "ROADMAP MODE – generate checklist", "Generate hierarchical checklist", "roadmap checklist for this note" | (interpret by agent) | Run **roadmap-checklist** skill on current or specified note: recursive link traversal → hierarchical checklist; see `.cursor/skills/roadmap-checklist/SKILL.md` |
| MCP vault operations | mcp-obsidian-integration (always) | — |

always-ingest-bootstrap ensures ingest triggers apply the ingest pipeline; see `.cursor/rules/always/always-ingest-bootstrap.mdc`.

Rules live in `.cursor/rules/always/` (always-applied) and `.cursor/rules/context/` (globs/triggers).

### Watcher bridge (Obsidian plugin)

- **Exclusions (Watcher)**: Pipelines must **not** move or delete notes that (a) have frontmatter **`watcher-protected: true`**, or (b) are one of the fixed Watcher paths: `Ingest/watched-file.md`, `3-Resources/Watcher-Signal.md`, `3-Resources/Watcher-Result.md`. Context rules (ingest, organize, archive) list these in their Excludes sections.
- **Exclusions (Decision Wrappers)**: Pipelines must **not** treat Decision Wrapper notes under `Ingest/Decisions/*.md` as primary inputs for ingest/distill/organize/express/archive. These notes coordinate user-approved moves only; the pipelines operate on the original `Ingest/*.md` notes, using wrapper decisions via EAT-QUEUE + guidance-aware runs.
- **Watcher-Result contract**: When a run was triggered by a Watcher request (e.g. INGEST MODE, DISTILL MODE, EXPRESS MODE, ARCHIVE MODE from the Obsidian Watcher plugin) or by **EAT-QUEUE** (queue-based run), the agent must **on run finish** append one line per request to `3-Resources/Watcher-Result.md`: `requestId: <id> | status: success|failure | message: "..." | trace: "..." | completed: <ISO8601>`. See `.cursor/rules/always/watcher-result-append.mdc` for the full contract and format.
- **Decision Wrapper — Watcher checkbox sync**: For notes under `Ingest/Decisions/**`, the Watcher plugin (on modify) syncs the **checked** A–G option into frontmatter `approved_option` and `approved_path` **only when** the user has **already** set `approved: true` (manual only). Watcher never sets `approved: true` or `re-wrap: true`. Write-loop protection: read frontmatter before write; skip if already matching. All sync/skip/conflict decisions → `3-Resources/Wrapper-Sync-Log.md`; conflicts also to Errors.md. See Pipelines.md (Decision Wrapper), Logs.md.
- **Decision Wrapper — re-wrap (EAT-QUEUE Step 0)**: When a wrapper has `re-wrap: true` or `approved_option: 0` (reject all), Step 0 runs the **re-wrap branch**: backup + per-change snapshot of the wrapper, move it to `4-Archives/Ingest-Decisions/Re-Wrap/<subfolder>/`, then create a **new** wrapper under `Ingest/Decisions/` with Thoughts as seed and a link to the archived wrapper. `feedback-incorporate` prefers `approved_path` from frontmatter; fallback parse body for letter; treats re-wrap/option 0 as no path. No default `approved_option`/`approved_path` in the template. See auto-eat-queue.mdc, feedback-incorporate SKILL, Vault-Layout.md (Re-Wrap).
- **Decision Wrapper — apply-mode (Step 0 path-apply)**: For approved wrappers with `hard_target_path`, Step 0 runs apply-mode ingest only (move/rename original note to approved path). After move: set para-type (and when under 1-Projects/ project-id) from new path per mcp-obsidian-integration. Roadmap tree creation is **not** triggered from ingest; use **ROADMAP MODE – generate from outline** (or a dedicated queue mode) and the `roadmap-generate-from-outline` skill for that.

### New flows: Garden review and Curate cluster

- **Garden review**: Trigger phrases include "GARDEN REVIEW", "run garden review", "orphans and distill candidates", "garden health", "vault orphans", "distill candidates sweep". Flow: call **`obsidian_garden_review`**(scope, focus: orphans | distill_candidates | weak_links | all, output_path optional, auto_apply). Suggest **`auto_apply: false`** by default during initial adoption. Downstream: use the report to feed autonomous-distill and autonomous-organize batches.
- **Curate cluster**: Trigger phrases include "CURATE CLUSTER #tag", "suggest gaps and merges for 3-Resources", "cluster curate #tag", "theme gaps #tag", "merge suggestions 3-Resources/…". Flow: call **`obsidian_curate_cluster`**(query: tag or folder, note_list optional, actions: suggest_gaps, suggest_merges, generate_synthesis). Suggest **`auto_apply: false`** by default during initial adoption. Client LLM analyzes the report and can call obsidian_split_atomic, obsidian_generate_moc, or merge proposals. Document in report §2 and §8.

---

## Log format, backup path, and loops

Every pipeline that performs move/overwrite/delete must log with **backup path included**. The MCP tool `obsidian_log_action` has no dedicated `backup_path` parameter; include the backup path in the **`changes`** string (e.g. `"TL;DR, bolded; Backup: /path/to/backup/note.md"`) or in the log line format below.

**Log line format** (align with auto-logging rule):

`YYYY-MM-DD HH:MM | Excerpt: [snippet] | PARA: [type] | Changes: [list; include Backup: [path] when processing] | Confidence: X% | Proposed MV: [path or 'stay'] | Flag: [none or #review-needed + reason] | Loop: [attempted: true/false, type: <loop_type>, pre: X%, post: Y%, outcome: increased|flat|decreased, reason: <short>]`

Pipelines that implement loops should also expose structured fields (for Dataview and analysis):

- `loop_attempted: true|false`
- `loop_band: "68-84" | "none"`
- `pre_loop_conf: int`
- `post_loop_conf: int`
- `loop_outcome: increased | flat | decreased`
- `loop_type: ingest-refine | organize-path | archive-refine | express-soft | distill-depth`
- `loop_reason: string`

Always call `obsidian_log_action` after processing a note; never skip logging.

---

## Pipeline flowcharts

**full-autonomous-ingest** (two-phase, Decision Wrapper–gated). Phase 1 never moves; Phase 2 runs when EAT-QUEUE Step 0 (always-check wrappers) finds a wrapper with `approved: true`.

```mermaid
flowchart LR
  ingestInit[IngestInitialRun] --> classify[classify_para + frontmatter_enrich]
  classify --> distill[split/distill/next-actions/hub (no move)]
  distill --> wrapper[Create/refresh Decision Wrapper A–G]
  wrapper --> userEdit[User checks option, sets approved: true]
  userEdit --> eatStep0[EAT-QUEUE Step 0 finds approved wrapper]
  eatStep0 --> applyRun[Apply-mode: move/rename to approved_path]
  applyRun --> moveSnap[Snapshot + dry_run then commit; archive wrapper to 4-Archives/Ingest-Decisions/]
  moveSnap --> done[Note in PARA; wrapper archived]
```

**autonomous-distill**: backup → distill layers → distill-highlight-color → highlight-perspective-layer (optional) → layer-promote → callout-tldr-wrap → readability-flag.

**autonomous-archive**: backup → classify_para → archive-check → subfolder-organize → resurface-candidate-mark → summary-preserve → move_note → (after move: set para-type from new path, **status: archived** when under 4-Archives/) → log_action.

**autonomous-express**: backup → version-snapshot → related-content-pull → express-mini-outline → call-to-action-append.

**autonomous-organize**: backup → classify_para → frontmatter-enrich → subfolder-organize → **name-enhance** (context organize; opportunistic rename when vague or confidence ≥85%) → move_note → (after move: set para-type and when under 1-Projects/ project-id from new path) → log_action.

### Ingest confidence loop (state diagram)

```mermaid
flowchart LR
  eval[Evaluate ingest_conf] --> high[High (>=85)]
  eval --> mid[Mid (68-84)]
  eval --> low[Low (<68)]

  high --> snap_ingest[Per-change snapshot]
  snap_ingest --> ingest_actions[Split / distill / hub / move]

  mid --> loop_ingest[Non-destructive self-critique loop]
  loop_ingest --> post_high[post_loop_conf >= 85]
  loop_ingest --> post_low[post_loop_conf < 85 or <= pre_loop_conf]

  post_high --> snap_ingest
  post_low --> manual_ingest[Manual review (no destructive actions)]

  low --> manual_ingest
```

---

## 1. full-autonomous-ingest

Ingest → organize + initial distill + hub, with **relocation deferred to user-approved Decision Wrappers** (Phase 2).

### Bootstrap at start (before classify_para)

After **`obsidian_list_notes("Ingest")`**, call **`obsidian_list_projects`** and **`bootstrap_project_batch`**(paths, existing_projects_json). If a project seed is detected (≥85%), either auto-apply project creation or set requires_confirmation and ask user, then **`confirm_bootstrap`** to apply in one step. **Defensive**: If **`bootstrap_project_batch`** returns multiple possible projects or low-confidence matches (<85%), default to requires_confirmation = true and prompt user rather than auto-applying. Insert this **before** classify_para in the pipeline order.

### Pre-step (when Ingest contains non-.md)

List non-.md files in Ingest (e.g. workspace glob/list; MCP may return only .md). For each non-.md file: create companion .md per non-markdown-handling rule (`.cursor/rules/context/non-markdown-handling.mdc`). Attempt move of original to 5-Attachments/[subtype]/ (ensure_structure, create_backup, move_note; backup required first); on success companion links to final path and no #needs-manual-move; on failure leave in Ingest/ with #needs-manual-move and log. Subtype from [Attachment-Subtype-Mapping](3-Resources/Attachment-Subtype-Mapping.md) or rule table. Then run the pipeline below on all Ingest/*.md (including newly created companions).

#### Additional step: Embedded image normalization

Any .md in Ingest/ is scanned for image embeds pointing to root/Ingest/. Links are rewritten to `5-Attachments/Images/`. Manual-move callout + `#needs-attachment-relocation` tag added. Image files remain in place until user drags them (MCP-safe).

| Skill | Slot (after) | What it does | Confidence gate |
|-------|----------------|--------------|------------------|
| **frontmatter-enrich** | classify_para | Set status, confidence, para-type, created, links (hub + related); optional project-id, priority, deadline; at ≥75% with project_name still set project-id + MOC and lift confidence to ≥82% | ≥85% full; ≥75% project fallback |
| **name-enhance** | frontmatter-enrich | When filename is vague/untitled: **propose only** (never rename in ingest). Returns suggested_name; subfolder-organize uses it in path when confidence ≥85% and not protected. In ingest, name-enhance proposes; subfolder-organize commits the name via move. | ≥85% to use suggested_name in path |
| **subfolder-organize** | name-enhance (or frontmatter-enrich) | Auto-create/move to subfolder (max 4 levels) from para-type + themes/project-id; use **suggested_filename** from name-enhance when provided and confidence ≥85%; path segment format kebab-slug-YYYY-MM-DD-HHMM per Naming-Conventions (date and time at end); move into **existing** folder allowed at ≥78% | ≥85% new structure; ≥78% into existing |
| **split-link-preserve** | split_atomic | Minimal split linking: split_from (wikilink) + related[] append on each child; ## Splits bullet list with one-line reason on parent; idempotent, backlinks for reverse nav | ≥85% |
| **distill-highlight-color** | distill_note | Apply colors from master key + project highlight_key; color theory (analogous/complementary) | ≥80% |
| **next-action-extract** | distill-highlight-color | Extract tasks → checklists + next-actions frontmatter array (string format); color-code by project if desired | ≥85% |
| **task-reroute** | next-action-extract | When next-action-extract confidence ≥78% and task-like (weighted score ≥70): **find_parent** or project path → **obsidian_create_task_note** or **append_tasks**; snapshot target before append. See `.cursor/skills/task-reroute/SKILL.md`. | ≥78% + task-like |
| **`obsidian_refactor_to_zettel`** (optional) | alternative to split_atomic for literature/fleeting | For literature/fleeting notes where atomic split is desired: only when input note length > ~800 words or multiple clear `##` headings; otherwise prefer **obsidian_split_atomic**. Server splits on `##` and creates permanent zettel with frontmatter. | optional branch |

**Pipeline order (Phase 1 — propose + wrapper)**: (optional **bootstrap_project_batch** after list_notes + list_projects, before classify) → create_backup → classify_para → **frontmatter-enrich** → **name-enhance** (when vague/untitled; propose only; returns suggested_name) → **subfolder-organize** (use suggested_name in path when ≥85% and not protected) → (optional mid-band self-critique loop: use **`propose_para_paths`** in `"midband"` context to obtain 2–3 ranked PARA path candidates, then **calibrate_confidence** / **verify_classification** on the best candidate) → split_atomic (when confidence allows) → **split-link-preserve** → distill_note → **distill-highlight-color** → **next-action-extract** → **task-reroute** (when task-like, ≥78%) → manage_frontmatter / manage_tags → append_to_hub → log_action → **create/refresh Decision Wrapper** for relocation (see `para-zettel-autopilot.mdc`). Moves/renames occur only in **Phase 2 apply-mode ingest**, triggered by approved Decision Wrappers via EAT-QUEUE; see below.

**Ingest confidence bands & gates (Decision Wrapper-aware, Phase 1 focus):**

- Let `ingest_conf` be the primary signal after frontmatter + path proposal.
- **High (ingest_conf ≥85)**:
  - Execute in-note structural steps (split, distill, hub append, task-reroute) after required per-change snapshots; still **do not move/rename** in Phase 1. High confidence primarily raises `decision_priority` and ranks candidates in the Decision Wrapper.
- **Mid (68 ≤ ingest_conf ≤ 84, inclusive)**:
  - Run a **single, non-destructive self-critique loop** on classification/path:
    - Use the shared self-critique template (see `.cursor/rules/always/confidence-loops.mdc`).
    - Call **`obsidian_propose_para_paths`** with `context_mode: "midband"` (and appropriate `max_candidates`) to obtain 2–3 ranked PARA path candidates `{path, score, reason_short, rationale, confidence_breakdown}`.
    - Feed the top candidate (or top 2, when helpful) into **`calibrate_confidence`**(prior_output: classification + path proposal) then **`verify_classification`**(note_path, calibrated_output).
    - Re-score to `post_loop_conf` and adjust `decision_priority` and wrapper ordering accordingly.
  - Structural steps may be limited or skipped when confidence remains mid-band, but the outcome is still a Decision Wrapper rather than an immediate move.
- **Low (ingest_conf <68)**:
  - No loop; apply only safe frontmatter and links where appropriate.
  - Still create/update a Decision Wrapper under `Ingest/Decisions/` and treat the note as a **user decision candidate**. Low confidence lowers or raises `decision_priority` depending on age/importance, but **never triggers a move** without explicit user approval.

---

## 2. autonomous-distill

Periodic or targeted refinement pass.

**Optional pre-step (strongly recommended for batch mode, >5 notes)**: Use **`obsidian_garden_review`**(scope/folder, focus: **distill_candidates**, output_path, auto_apply) to pre-select notes that need distill; then run autonomous-distill on that set. Optional for single-note triggers. Document as "strongly recommended batch init when >5 notes."

| Skill | Slot | What it does | Confidence gate |
|-------|------|--------------|------------------|
| **auto-layer-select** (optional) | before distill layers | Suggest 1/2/3 layers from content complexity; manual override e.g. "distill with 2 layers" | ≥85% to apply |
| **distill-highlight-color** | after standard distill layers | Same as above; project-linked colors, semantic cross-file check; coverage 50–70%, perspective | ≥80% |
| **highlight-perspective-layer** | after distill-highlight-color | data-drift-level (0–3), highlight_angles; log drift/angles to Distill-Log; snapshot before structural edits | ≥85% |
| **layer-promote** | after highlight-perspective-layer or distill-highlight-color | Promote bold → highlight → TL;DR; project color overrides; contrast for conflicting ideas | ≥85% |
| **distill-perspective-refine** | after layer-promote | Emojis/gradient indicators in TL;DR for depth/drift; log lens + gradient stats to Distill-Log; snapshot before rewrite | ≥85% |
| **callout-tldr-wrap** | after layer-promote | Wrap TL;DR in `> [!summary] TL;DR` callout; optional color-callout border via CSS | always |
| **readability-flag** | at end | If low readability: needs-simplify: true + warning callout; flag related project ideas | ≥70% |

**Pipeline order**: (backup) → **(auto-layer-select** when enabled, read **distill_lens** from frontmatter) → (optional mid-band depth self-critique loop) → distill layers → **distill-highlight-color** → **highlight-perspective-layer** (optional) → **layer-promote** → **distill-perspective-refine** → **callout-tldr-wrap** → **readability-flag**.

**Distill confidence bands & depth control:**

- Let `distill_conf` be the depth signal from `auto-layer-select` / depth evaluation.
- **High (distill_conf ≥85)**:
  - Run full planned distill depth (all structural steps) after snapshot.
- **Mid (68 ≤ distill_conf ≤ 84)**:
  - Run a **single depth self-critique loop**:
    - Evaluate risk of nuance loss; consider a shallower plan (e.g. fewer layers).
    - Compute `post_loop_conf` for the shallower plan.
  - If `post_loop_conf ≥ 85`: snapshot → run the **shallower** structural distill plan.
  - Else or if `post_loop_conf ≤ pre_loop_conf`: skip structural distill; run only `readability-flag` (and safe metadata tweaks) and log.
- **Low (distill_conf <68)**:
  - No structural distill; only `readability-flag` and frontmatter flags.

---

## 3. autonomous-archive

Declutter inactive/complete items.

| Skill | Slot | What it does | Confidence gate |
|-------|------|--------------|------------------|
| **archive-check** | after classify_para | Heuristic: no open tasks, status complete, age > threshold; cross-check project subfolders | ≥85% for move (primary signal: archive_conf) |
| **subfolder-organize** | before move | Archive path with subfolders (e.g. 4-Archives/Project-X-Archive/Subtheme/) from project-id | ≥85% |
| **resurface-candidate-mark** | before move | If high potential (links/highlights): resurface-candidate: true; optional Resurface hub append | ≥75% |
| **summary-preserve** | before move | If no TL;DR: light distill + callout; preserve project color links | ≥80% |
| **archive-ghost-folder-sweep** | after log_action | Remove empty moved-note ancestors via MCP tool (obsidian_remove_empty_folder); run only when moved_notes_list non-empty | once per sweep |

**Pipeline order**: (backup) → classify_para → **archive-check** → (optional mid-band archive-refine loop: **calibrate_confidence** → **verify_classification** → **obsidian_move_note**(..., `dry_run: true`) → then commit after snapshot) → **subfolder-organize** → **resurface-candidate-mark** → **summary-preserve** → **move_note (dry_run first, then commit)** → (after move: set para-type from new path, **status: archived** when under 4-Archives/) → **log_action** → **archive-ghost-folder-sweep** (if any moves in this run). On move failure or dry_run risks, reuse the same fallback chain in mcp-obsidian-integration.mdc; do not duplicate fallback logic per pipeline.

**Archive confidence bands & gates:**

- Let `archive_conf` be the signal from `archive-check`. **Mid-band = 68–84% inclusive.**
- **High (archive_conf ≥85)**:
  - After snapshot, run archive pathing, resurface marking, summary preservation, and move as usual (**dry_run first, then commit**).
- **Mid (68 ≤ archive_conf ≤ 84)**:
  - Run a **single archive-refine loop**:
    - Re-check for open tasks and recent edits.
    - Optionally generate a TL;DR **preview** (non-destructive) to evaluate “closedness”.
    - Apply the shared self-critique template with emphasis on readiness and neighbor notes.
  - If `post_loop_conf ≥ 85`: snapshot → proceed with archive move.
  - Else or if `post_loop_conf ≤ pre_loop_conf`: do not archive; keep note active, log proposed archive path + reason, and mark as candidate (`#review-needed`).
- **Low (archive_conf <68)**:
  - No loop; mark as **archive candidate** only (e.g. frontmatter flag), keep in active PARA, and log.

---

## 4. autonomous-express

Generate output from distilled notes.

| Skill | Slot | What it does | Confidence gate |
|-------|------|--------------|------------------|
| **version-snapshot** | before any major append | Dated snapshot in `Versions/` with path `Versions/<original_slug>--<YYYYMMDD-HHMMSS>.md`; use `obsidian_update_note(..., mode: "create")` so the server skips destination backup for new files. Preserve original content and colors. Confidence ≥85% for version write. | ≥85% for write |
| **related-content-pull** / **`obsidian_suggest_connections`** | before outline | Pull similar notes (semantic + project-id) or use MCP **`obsidian_suggest_connections`**(note_path, num_suggestions, auto_insert, suggested_links); if `auto_insert: true`, wrap inserted Related section in a collapsible callout `[!related]` to keep notes visually clean. Color theory for relations. | ≥80% |
| **express-mini-outline** | after read_note | Outline/summary → append as fenced block; project colors; **express_view** shapes outline | ≥85% for append (primary signal: express_conf) |
| **express-view-layer** | after related-content-pull or express-mini-outline | Connection strength indicators in Related when **express_view** set; log view + relation stats to Express-Log | ≥85% |
| **`obsidian_append_to_moc`** / **`obsidian_generate_moc`** (optional) | after outline | For hub-like notes: append to MOC or generate MOC (topic, moc_path, tag/folder, content). | optional |
| **call-to-action-append** | at end | Append CTA callout (e.g. `> [!tip] Share/Publish?`); color by action type/project key | always |

**Pipeline order**: (backup) → **version-snapshot** (before major append) → **related-content-pull** (or **`obsidian_suggest_connections`**; read **express_view** from frontmatter) → (optional mid-band soft express loop) → **express-mini-outline** → **express-view-layer** (when express_view set) → (optional **obsidian_append_to_moc** / **obsidian_generate_moc** for hub-like notes) → **call-to-action-append**.

**Express confidence bands & soft loop:**

- Let `express_conf` be the expressive readiness signal (outline + CTA).
- **High (express_conf ≥85)**:
  - After version + per-change snapshots, run related-content, full outline, and CTA.
- **Mid (68 ≤ express_conf ≤ 84)**:
  - Run a **soft express loop**:
    - Generate a short **preview outline** and self-critique coherence/fidelity **without writing** to the note.
    - Compute `post_loop_conf`.
  - If `post_loop_conf ≥ 90`: commit full outline + CTA.
  - If `85 ≤ post_loop_conf ≤ 89`: commit a **shorter outline** + CTA.
  - Else or if `post_loop_conf ≤ pre_loop_conf`: skip outline/related blocks; optionally add a small CTA (“needs further distill before publish”) and log.
- **Low (express_conf <68)**:
  - No express beyond optional minimal CTA; rely on future distill/organize runs.

**Note (version-snapshot)**: version-snapshot now supports **reliable new-file creation** without the destination backup gate (server update 2026-02-25). Use `mode: "create"` in `obsidian_update_note` for the version path; the server skips dest backup and fails if the path already exists, so timestamped filenames `<original_slug>--<YYYYMMDD-HHMMSS>.md` guarantee a new path each run. Ensure `Versions/` exists (create once per project/area; optional `.gitkeep`). Source note is always backed up at pipeline start and per-change snapshots apply before appends.

---

## 5. autonomous-organize

Re-organize existing notes in active PARA folders (1-Projects, 2-Areas, 3-Resources): re-evaluate classification, enrich frontmatter, suggest/create subfolders (max 4 levels), rename for atomicity, move when confidence ≥85%. Separate from ingest (new captures) and archive (completed → 4-Archives/).

| Skill / step | Slot | What it does | Confidence gate |
|--------------|------|--------------|------------------|
| **classify_para** (MCP) | after backup | Re-evaluate para-type, status, themes | — |
| **frontmatter-enrich** | after classify_para | Set/update status, confidence, para-type, created, links; optional project-id, priority, deadline | ≥85% auto |
| **subfolder-organize** | after frontmatter-enrich | Build target path under active PARA roots (1/2/3; re-org mode, not 4-Archives); max 4 levels from para-type + project-id + themes | ≥85% for move (primary signal: path_conf) |
| **name-enhance** (optional) | after subfolder-organize | Opportunistic filename improvement; context `organize`; apply when vague or confidence ≥85% (per skill confidence tiers); snapshot before obsidian_rename_note; after rename sync frontmatter `title` from new slug via manage_frontmatter | ≥85% for apply |
| **obsidian_rename_note** (optional) | after name-enhance when it applies | Rename in place to suggested_name (kebab-slug-YYYY-MM-DD-HHMM per Naming-Conventions; date and time at end); only when name-enhance returns apply | ≥85% |
| **obsidian_move_note** | after path computed | **obsidian_ensure_structure**(folder_path: parent of target) first so path exists; then **dry_run first, then commit** | ≥85% |

**Pipeline order**: (backup) → classify_para → **frontmatter-enrich** → **subfolder-organize** (or MCP **`obsidian_subfolder_organize`** for 2–3 path candidates in mid-band) → (optional mid-band organize-path loop: **calibrate_confidence** → **verify_classification** → **obsidian_move_note**(..., `dry_run: true`) → then commit) → **name-enhance** (context organize; opportunistic rename when vague or confidence ≥85%) → (obsidian_rename_note when name-enhance applied) → **obsidian_move_note (dry_run first, then commit)** (if path changed) → (after move: set para-type and when under 1-Projects/ project-id from new path) → log_action. On move failure or dry_run risks, reuse the same fallback chain defined in mcp-obsidian-integration.mdc (§1.2); do not duplicate fallback logic per pipeline.

**Organize confidence bands & path loop:**

- Let `path_conf` be the path fit signal from `subfolder-organize` in re-org mode. **Mid-band = 68–84% inclusive.**
- **High (path_conf ≥85)**:
  - After snapshot, apply rename (if warranted) and move to the new path (**dry_run first, then commit**).
- **Mid (68 ≤ path_conf ≤ 84)**:
  - Run a **single neighbor/context loop**:
    - Use **MCP** **`propose_para_paths`** (context_mode `"organize"`) for 2–3 ranked path candidates (replacing or complementing the skill-based single path) and their reasons/breakdowns.
    - Compare the note to siblings in candidate folders (headings, tags, backlinks/hubs).
    - Apply the shared self-critique template focused on path fit.
    - **calibrate_confidence**(prior_output: path_conf, para_type, selected_path) → **verify_classification** → **obsidian_move_note**(..., `dry_run: true`) → then commit.
    - Optionally propose 2–3 alternative paths with scores and compute `post_loop_conf`.
  - If `post_loop_conf ≥ 85`: snapshot → apply rename (if any) and move (**dry_run first, then commit**).
  - Else or if `post_loop_conf ≤ pre_loop_conf`: skip rename/move; log alternative paths + reasons and mark `#review-needed`.
- **Low (path_conf <68)**:
  - No loop; proposals remain propose-only and no rename/move is executed. Log as such.


---

## Skill locations

| Skill | Path |
|-------|------|
| auto-layer-select | .cursor/skills/auto-layer-select/SKILL.md |
| distill-highlight-color | .cursor/skills/distill-highlight-color/SKILL.md |
| highlight-perspective-layer | .cursor/skills/highlight-perspective-layer/SKILL.md |
| distill-perspective-refine | .cursor/skills/distill-perspective-refine/SKILL.md |
| express-view-layer | .cursor/skills/express-view-layer/SKILL.md |
| subfolder-organize | .cursor/skills/subfolder-organize/SKILL.md |
| frontmatter-enrich | .cursor/skills/frontmatter-enrich/SKILL.md |
| next-action-extract | .cursor/skills/next-action-extract/SKILL.md |
| task-reroute | .cursor/skills/task-reroute/SKILL.md |
| roadmap-ingest | .cursor/skills/roadmap-ingest/SKILL.md |
| roadmap-generate-from-outline | .cursor/skills/roadmap-generate-from-outline/SKILL.md |
| add-roadmap-append | .cursor/skills/add-roadmap-append/SKILL.md |
| expand-road-assist | .cursor/skills/expand-road-assist/SKILL.md |
| task-complete-validate | .cursor/skills/task-complete-validate/SKILL.md |
| roadmap-checklist | .cursor/skills/roadmap-checklist/SKILL.md |
| related-content-pull | .cursor/skills/related-content-pull/SKILL.md |
| express-mini-outline | .cursor/skills/express-mini-outline/SKILL.md |
| callout-tldr-wrap | .cursor/skills/callout-tldr-wrap/SKILL.md |
| layer-promote | .cursor/skills/layer-promote/SKILL.md |
| readability-flag | .cursor/skills/readability-flag/SKILL.md |
| archive-check | .cursor/skills/archive-check/SKILL.md |
| resurface-candidate-mark | .cursor/skills/resurface-candidate-mark/SKILL.md |
| summary-preserve | .cursor/skills/summary-preserve/SKILL.md |
| call-to-action-append | .cursor/skills/call-to-action-append/SKILL.md |
| version-snapshot | .cursor/skills/version-snapshot/SKILL.md |
| highlight-seed-enhance | .cursor/skills/highlight-seed-enhance/SKILL.md |
| feedback-incorporate | .cursor/skills/feedback-incorporate/SKILL.md |
| split-link-preserve | .cursor/skills/split-link-preserve/SKILL.md |
| name-enhance | .cursor/skills/name-enhance/SKILL.md |
| archive-ghost-folder-sweep | .cursor/skills/archive-ghost-folder-sweep/SKILL.md |
| obsidian-snapshot | .cursor/skills/obsidian-snapshot/SKILL.md |
| log-rotate | .cursor/skills/log-rotate/SKILL.md |
| move-attachment-to-99 | .cursor/skills/move-attachment-to-99/SKILL.md |
| research-scope | .cursor/skills/research-scope/SKILL.md |
| distill-apply-from-wrapper | .cursor/skills/distill-apply-from-wrapper/SKILL.md |
| express-apply-from-wrapper | .cursor/skills/express-apply-from-wrapper/SKILL.md |
| link-to-pmg-if-applicable | .cursor/skills/link-to-pmg-if-applicable/SKILL.md |

Triggers and globs for when to run each pipeline are defined in Phase 2/3 rules (e.g. always-applied ingest bootstrap, context-specific para-zettel-autopilot and distill/archive/express/organize rules).

---

## Snapshot triggers (all pipelines)

Summary of when to create **per-change snapshots** and **batch checkpoints** using the `obsidian-snapshot` skill.

| Pipeline            | Per-change triggers                                                                                      | Batch frequency      |
|---------------------|----------------------------------------------------------------------------------------------------------|----------------------|
| full-autonomous-ingest | Before `split_atomic`, `distill_note` (when rewriting), `append_to_hub` (cross-note writes), **task-reroute** (per-change snapshot of **target** note before append_tasks), `move_note`, `rename_note`; name-enhance in ingest **proposes only** (subfolder-organize commits name via move) | Every 5 notes        |
| autonomous-distill  | Before first structural rewrite (distill layers / `highlight-perspective-layer` / `layer-promote` / `distill-perspective-refine` / heavy `obsidian_update_note`)       | ~Every 3 notes       |
| autonomous-archive  | After `archive-check` recommends archive (≥85% confidence) but before `subfolder-organize` / `summary-preserve` / move | Once per archive sweep |
| autonomous-express  | Before large appends (`related-content-pull`, `express-mini-outline`, `express-view-layer`, `call-to-action-append`), alongside `version-snapshot` | Optional per batch   |
| autonomous-organize | Before `obsidian_rename_note` (when name-enhance applies) and before `obsidian_move_note` (when confidence ≥85% for each)                             | ~Every 3 notes       |

- All destructive actions should also:
  - Respect the **≥85%** confidence rule for auto-execution.
  - Skip both snapshot and destructive step when confidence is below threshold, logging `#review-needed` instead.
- Snapshot files live under `Backups/Per-Change/` and `Backups/Batch/` and are never processed as pipeline inputs.

---

## Phase-direction wrapper creation

When creating a Phase Direction Wrapper (after EXPAND-ROAD or roadmap-generate-from-outline when a phase has direction choices):

- **Options A–G (body)**: Fill each option with a **conceptual end-state** description only — one plain-language sentence stating *what the situation is* after that choice. No technical terms (no "CSS Grid," "breakpoints," "design tokens"). Example (phase fork = "How do we handle the grid?"): **A.** One shared grid everywhere — same behavior on every device and screen. **B.** Each surface tuned to itself — mobile, desktop, and large displays each get a layout that fits. **C.** Shared core, local tweaks — one grid system with small per-context overrides so it stays consistent but adapts. Pad to 7 options (A–G); use "Reserved" or "—" if fewer than 7 meaningful options.
- **Technical resolution**: Store in wrapper **frontmatter** only (e.g. `technical_by_option: { "A": "single token set", "B": "per-context tokens", ... }` or per-option fields) for provenance and Step 0 apply. Do not put technical text in the main option list the user sees.
- **Template**: [Templates/Decision-Wrapper-Phase-Direction.md](Templates/Decision-Wrapper-Phase-Direction.md). Optional: populate the collapsible "Technical resolution (for reference)" block from frontmatter for power users.

---

## Apply-from-wrapper (Step 0)

When EAT-QUEUE Step 0 finds a wrapper under `Ingest/Decisions/**` with `approved: true`, behavior depends on **wrapper_type** and **pipeline**:

| wrapper_type | pipeline | Step 0 behavior |
|--------------|----------|------------------|
| ingest-decision, roadmap-decision | ingest | feedback-incorporate → resolve `approved_path` → apply-mode ingest (move/rename original note to approved path only); then move wrapper to `4-Archives/Ingest-Decisions/` (mirror subfolder). |
| **phase-direction** | — | **Apply**: Per-change snapshot of target roadmap/phase note → append provenance callout (`> [!provenance] Evolved from [[Master-Goal]] via [[Wrapper-1]] (re-try on <date>) → [[Wrapper-2]] (approved).`) and, near the approved task bullet, inline callout with "Comment guidance: …" (see §6.2 Comment and provenance injection) → set `processed: true`, `used_at` on wrapper → move wrapper to `4-Archives/Ingest-Decisions/Roadmap-Decisions/`. Options A–G are conceptual end-state descriptions; technical resolution stored in frontmatter (e.g. `technical_by_option`) for provenance. |
| mid-band-refinement, force-wrapper | distill | **distill-apply-from-wrapper**: read wrapper `original_path`, `approved_option`; run autonomous-distill on original with `approved_option` as distill_lens; update/move wrapper. |
| mid-band-refinement, force-wrapper | express | **express-apply-from-wrapper**: read wrapper `original_path`, `approved_option`; run autonomous-express on original with `approved_option` as express_view; update/move wrapper. |
| mid-band-refinement, force-wrapper | organize, archive | Resolve `approved_path`; run path-apply (move to approved path) for that pipeline; snapshot + dry_run then commit; move wrapper to archive. |
| low-confidence | (any) | Same as mid-band-refinement by pipeline: apply approved path or lens/view; move wrapper to archive. |
| error | — | Link to Errors.md entry; no destructive apply; move wrapper to archive after user review. |
| **task-decision** | — | **Apply**: Per Rules.md § Task-Decision wrappers: per-change snapshot of `target_note` → append provenance block to `target_note` (Resolved via [[wrapper]], Choice, Guidance applied) → set `processed: true`, `used_at` on wrapper → move wrapper to `4-Archives/Ingest-Decisions/Task-Decisions/`. *Implementation: queue Step 0 or dedicated helper; document as supported when Task-Decision flow is enabled.* |

---

## Error handling (all pipelines)

On any pipeline or workflow error, the agent follows the **Error Handling Protocol** in `.cursor/rules/always/mcp-obsidian-integration.mdc`. Trace and summary are appended to **`3-Resources/Errors.md`** (create the note if missing). Each entry uses: heading `### YYYY-MM-DD HH:MM — Short Title`; metadata table (`pipeline`, `severity`, `approval`, `timestamp`, `error_type`); **#### Trace** (sanitized); **#### Summary** (Root cause, Impact, Suggested fixes, Recovery). Pipeline-specific logs get a one-line reference to the error. High severity or critical errors are tagged `#review-needed` and the current note is paused (no destructive steps); batch continues with the next note unless it is a global failure (e.g. backup at run start). Rollback remains user-triggered (RESTORE MODE); error entries document snapshot path when available for recovery.

---

## Dataview & dashboards (logs + loops)

- All pipeline logs (`Ingest-Log`, `Organize-Log`, `Archive-Log`, `Distill-Log`, `Express-Log`) are expected to expose, at minimum:
  - `timestamp`, `pipeline`, `note path`, `confidence`, `actions taken / skipped`, `backup path`, `snapshot path(s)`, `flag`.
- For notes that went through a loop, also expose:
  - `loop_attempted`, `loop_band`, `pre_loop_conf`, `post_loop_conf`, `loop_outcome`, `loop_type`, `loop_reason`.
- Example Dataview query ideas (pseudo-code):
  - “Where did loops increase confidence?” → `WHERE loop_attempted AND loop_outcome = "increased"`.
  - “Which pipelines most often fall back to user decision flows?” → group by `pipeline`, count where `loop_attempted AND post_loop_conf < 85`.
  - “Mid-band hot spots” → `WHERE loop_band = "68-84" AND loop_outcome = "decreased"`.

These assumptions keep dashboards consistent as confidence loops evolve.

## Autonomous-Organize Readiness

| Component                 | Status       | Notes                                                                 |
|---------------------------|--------------|-----------------------------------------------------------------------|
| Context rule              | Ready        | `.cursor/rules/context/auto-organize.mdc` — triggers, globs, excludes, snapshot triggers, MCP safety. |
| Pipeline reference        | Ready        | §5 above + trigger row + snapshot row in table.                      |
| Skills chaining           | Ready        | frontmatter-enrich, subfolder-organize (re-org mode), obsidian-snapshot updated. |
| Logging setup             | Ready        | `3-Resources/Organize-Log.md` + cross-post to Backup-Log.md per rule. |
| Test-ready prompt example | Ready        | e.g. "ORGANIZE MODE – safe batch autopilot on 1-Projects/Test-Project" or "Re-organize Projects and Resources" with 1–3 notes in Test-Project. |
