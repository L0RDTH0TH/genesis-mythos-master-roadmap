---
title: Rules Structure — Detailed
created: 2026-03-05
tags: [pkm, second-brain, rules, structure, level-3]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/README]]", "[[Rules]]"]
---

# Rules Structure — Detailed

This document lists every rule file, its trigger/glob, pipeline or flow, main responsibilities, and cross-references. Use it to see exactly which rule applies for a given phrase, queue mode, or file path, and how Step 0 (apply, re-wrap, re-try, phase-direction), Watcher sync, and safety invariants are spelled out in rules.

---

## Always-applied rules (full)

| File | Purpose | Responsibilities |
|------|---------|------------------|
| **00-always-core.mdc** | Persona and Ingest-first | Thoth-AI persona; all new/unknown files in Ingest/; frontmatter (created, tags) on every new .md; never assume files already processed. |
| **mcp-obsidian-integration.mdc** | MCP safety and fallbacks | Backup/snapshot gates (ensure_backup vs create_backup); dry_run before every move_note; ensure_structure(folder_path) before move; Error Handling Protocol (trace, summary, Errors.md, pipeline log ref); fallback table (ensure_structure → retry move; propose_alternative_paths → calibrate → verify → dry_run again). Snapshot triggers table; Restore-queue mode; no shell cp/mv/rm except move-attachment skill. |
| **second-brain-standards.mdc** | PARA and note standards | PARA only (1–4, Ingest, Templates, 5-Attachments); no 00 Inbox, 10 Zettelkasten, 99 Attachments, 99 Templates; atomic notes; frontmatter and tags; attachment syntax ![[5-Attachments/...]]; naming kebab-slug-YYYY-MM-DD-HHMM. |
| **confidence-loops.mdc** | Confidence bands and loop | High ≥85%: destructive only after snapshot. Mid 68–84%: single non-destructive refinement loop; post_loop_conf &gt; pre_loop_conf to commit. Low &lt;68%: proposal only; user adds approved and/or user_guidance. loop_* fields in logs; tunable bands from Config; loop-skip flag. |
| **guidance-aware.mdc** | Guidance-Aware Run Contract | Trigger: approved: true + user_guidance, or queue prompt + source_file, or #guidance-aware. Load guidance; pass to classify_para, subfolder-organize, name-enhance, distill_note, split_atomic; cap 500 words; guidance_conf_boost 0–20; never override safety; log guidance_used, guidance_truncated, guidance_ignored. |
| **always-ingest-bootstrap.mdc** | INGEST MODE entry point | On INGEST MODE / Process Ingest / run ingests: list Ingest notes (obsidian_list_notes), run full-autonomous-ingest per ingest-processing then Phase 1 (propose + Decision Wrapper); move/rename in Phase 2 apply-mode via EAT-QUEUE. |
| **watcher-result-append.mdc** | Watcher-Result contract | On run finish (Watcher request or EAT-QUEUE): append one line per request to 3-Resources/Watcher-Result.md: requestId, status, message, trace, completed (ISO8601). One line per processed queue entry when run is queue-based. |
| **backbone-docs-sync.mdc** | Docs and sync currency | When rules/skills/pipelines/config change: update 3-Resources/Second-Brain/ (Rules, Skills, Pipelines, Logs, etc.) and .cursor/sync/; refresh Mermaid where used; append changelog. |

---

## Context rules (full table)

| Rule file | Trigger / glob | Pipeline or flow | Responsibilities |
|-----------|----------------|------------------|------------------|
| **para-zettel-autopilot.mdc** | Ingest/*.md open or batch; INGEST MODE (with bootstrap) | full-autonomous-ingest | Backup → classify_para → frontmatter-enrich → name-enhance (propose) → subfolder-organize → split_atomic → split-link-preserve → distill_note → distill-highlight-color → next-action-extract → task-reroute → append_to_hub → create/refresh Decision Wrapper. Mid/low or ambiguous → Decision Wrapper under Ingest/Decisions/ with A–G (propose_para_paths wrapper mode; **post-process stabilizer:** re-rank by PARA-Actionability-Rubric v1.0, pad to 7, set heuristic_adjusted/heuristic_reason when order changed); no move in Phase 1. User picks approved_option (A–G or 0) or approved_path; apply in Step 0 on EAT-QUEUE. Exclude Ingest/Decisions/** from primary input. |
| **auto-eat-queue.mdc** | EAT-QUEUE, Process queue, eat cache, EAT-CACHE (or pasted payload) | Queue processor | Step 0 (always first): enumerate Ingest/Decisions/**; for approved: true, re-wrap: true, or re-try: true and not processed → feedback-incorporate → path-apply (apply-mode ingest, phase-direction apply), re-wrap branch, or re-try branch (re-queue EXPAND-ROAD/TASK-TO-PLAN-PROMPT with guidance; cap re_try_max_loops; on cap hit create cap-hit wrapper); move processed wrapper to 4-Archives/Ingest-Decisions/ or 4-Archives/Ingest-Decisions/Roadmap-Decisions/. Then read queue; validate; dedup; sort (CHECK_WRAPPERS first); **post-process stabilizer:** when originating note conf ≥ 90%, bump TASK-ROADMAP (and EXPAND-ROAD / TASK-TO-PLAN-PROMPT) after ORGANIZE, before DISTILL; log queue_order_adjusted, reason. Dispatch by mode; append Watcher-Result per entry; clear passed only; optional queue-cleanup. approved_wrappers_remaining → re-insert CHECK_WRAPPERS at step 8. |
| **auto-queue-processor.mdc** | PROCESS TASK QUEUE | Task/roadmap queue | Read Task-Queue.md; dispatch TASK-ROADMAP, TASK-COMPLETE, ADD-ROADMAP-ITEM, EXPAND-ROAD, etc.; Watcher-Result + Mobile-Pending-Actions; banner cleanup (success &gt; failure). |
| **auto-distill.mdc** | DISTILL MODE, distill note/vault | autonomous-distill | Backup; optional auto-layer-select; distill layers → distill-highlight-color → highlight-perspective-layer (optional) → layer-promote → distill-perspective-refine → callout-tldr-wrap → readability-flag. Per-change snapshot before first structural rewrite at ≥85%. Exclude 4-Archives, Backups, Logs, * Hub. |
| **auto-archive.mdc** | ARCHIVE MODE, archive, #eaten | autonomous-archive | Backup; classify_para; archive-check → subfolder-organize → resurface-candidate-mark → summary-preserve → ensure_structure → move_note dry_run then commit. Per-change snapshot before move when archive_conf ≥85%. Exclude 4-Archives, Backups, Logs, * Hub, watcher-protected. |
| **auto-express.mdc** | EXPRESS MODE, express note | autonomous-express | Backup; version-snapshot; related-content-pull → express-mini-outline → express-view-layer (when express_view) → call-to-action-append. Per-change snapshot before large appends when ≥85%. Exclude 4-Archives, Backups, Versions, Logs, * Hub. |
| **auto-organize.mdc** | ORGANIZE MODE, re-organize | autonomous-organize | Backup; classify_para; frontmatter-enrich → subfolder-organize → name-enhance (optional) → ensure_structure → move_note dry_run then commit; snapshot before rename and before move when ≥85%. Exclude 4-Archives, Backups, Logs, * Hub, watcher-protected. |
| **ingest-processing.mdc** | Non-MD in Ingest; embedded normalization | Pre-step before ingest | Normalize embedded images (rewrite to 5-Attachments/Images/); create companion .md for non-.md; attempt move of original to 5-Attachments/[subtype]; then run full ingest on Ingest/*.md. |
| **non-markdown-handling.mdc** | Non-.md in Ingest | Companion .md | Create companion .md; leave original in Ingest/ with #needs-manual-move; no move_note on binaries. |
| **snapshot-sweep.mdc** | Snapshot cleanup / retention | Per-change and batch retention | User-triggered retention/cleanup of Backups/Per-Change and Backups/Batch. |
| **auto-restore.mdc** | Restore from snapshot/backup | User-triggered restore | Restore from snapshot or BACKUP_DIR; user-triggered only; no auto-restore. |
| **auto-resurface.mdc** | Resurface, show resurface candidates | Resurface flow | Surface notes marked resurface-candidate; optional Resurface hub. |
| **auto-highlight-perspective.mdc** | HIGHLIGHT PERSPECTIVE: [lens] | Highlight pass | Set highlight_perspective or queue payload; run distill (or highlight step) with perspective for distill-highlight-color. |
| **mobile-seed-detect.mdc** | SEEDED-ENHANCE, "Enhance highlights from seeds" | highlight-seed-enhance | Run highlight-seed-enhance only when triggered or queued; user &lt;mark&gt; as cores; no auto-run on save. |
| **auto-distill-perspective.mdc** | DISTILL LENS: [angle] | autonomous-distill with lens | Set distill_lens frontmatter; run autonomous-distill; distill-perspective-refine and auto-layer-select use lens. |
| **auto-express-view.mdc** | EXPRESS VIEW: [angle] | autonomous-express with view | Set express_view frontmatter; run autonomous-express; express-view-layer shapes Related. |
| **auto-async-cascade.mdc** | EAT-QUEUE when queue &gt;3 entries | Propose batch | Propose batch to Mobile-Pending-Actions; user confirms BATCH-DISTILL/BATCH-EXPRESS. |

---

## Step 0 and re-wrap / re-try / phase-direction (rule detail)

- **Step 0 (auto-eat-queue)**  
  Runs before reading the queue. Enumerate Ingest/Decisions/** recursively. For each wrapper: skip if approved: false and re-wrap is not true and re-try is not true. For (approved: true or re-wrap: true or re-try: true) and not processed: run feedback-incorporate → hard_target_path, re-wrap intent, or re-try intent.  
  - **Re-wrap branch** (re-wrap: true or approved_option: 0 or no hard_target_path): backup + per-change snapshot of wrapper; ensure_structure(4-Archives/Ingest-Decisions/Re-Wrap/Ingest-Decisions); move_note(wrapper, Re-Wrap path) dry_run then commit; create new wrapper under Ingest/Decisions/ with same original_path, Thoughts as seed, link to archived wrapper; approved: false, no approved_option/approved_path on new wrapper; log CHECK_WRAPPERS re-wrap line.  
  - **Re-try branch** (re-try: true or approved_option: R; roadmap/phase-direction wrappers): cap check (re_try_count vs re_try_max_loops); if over cap, create cap-hit wrapper (A: Force approve, B: Prune branch, 0: Re-wrap full phase) and log #review-needed; else resolve guidance, inject session_success_hint and git_diff_hint, append queue entry (EXPAND-ROAD or TASK-TO-PLAN-PROMPT), set processed/used_at, move wrapper to 4-Archives/Ingest-Decisions/Roadmap-Decisions/.  
  - **Path-apply**: apply-mode ingest (move/rename original to approved_path only) or **phase-direction apply** (per-change snapshot of target roadmap note → append provenance callout and inline "Comment guidance" near approved task → set processed/used_at → move wrapper to 4-Archives/Ingest-Decisions/Roadmap-Decisions/). Then update wrapper, move wrapper to 4-Archives/Ingest-Decisions/ (or Roadmap-Decisions/ for phase-direction). Roadmap tree creation is triggered by ROADMAP MODE – generate from outline (or dedicated queue mode), not from ingest.  
  Branch B: approved and processed but still under Ingest/Decisions/ → location check (companion search) → archive or tag #orphan/#true-orphan.

- **Watcher (not a Cursor rule)**  
  Documented in Pipelines.md and Cursor-Skill-Pipelines-Reference: Watcher only syncs checked A–G → approved_option and approved_path when approved: true is already set by user; Watcher never sets approved: true or re-wrap: true. Write-loop protection; Wrapper-Sync-Log.md; conflicts to Errors.md.

---

## Cross-references

- Rule map and usage examples: [[Rules]]
- Pipeline order and snapshot triggers: [[Cursor-Skill-Pipelines-Reference]]
- Trigger summary and Decision Wrapper safety: [[Pipelines]]
- Queue and Step 0: [[Queue-Sources]]
- Log destinations: [[Logs]]
- Vault layout and Re-Wrap: [[Vault-Layout]]
