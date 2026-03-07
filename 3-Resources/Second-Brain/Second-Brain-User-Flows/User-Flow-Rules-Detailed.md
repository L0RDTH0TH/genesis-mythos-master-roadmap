---
title: User Flow — Rules (Detailed)
created: 2026-03-05
tags: [pkm, second-brain, user-flow, rules, level-3]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/README]]", "[[Rules]]", "[[User-Flow-Diagram-Detailed]]"]
---

# User Flow — Rules (Detailed)

This document is the full breakdown of user choices and the **rules** that govern each: Decision Wrapper (A–G, approved_path, user_guidance, approved: true, re-wrap: true / option 0), mid-band refinement (preview → approve or feedback → re-queue), async preview (Mobile-Pending-Actions + Commander “Async Approve”), dry_run review before commit, queue modes and Step 0, Watcher checkbox sync, and guidance-aware re-run. Every documented user decision point is tied to the rule(s) that enforce or describe it.

---

## Decision Wrapper: full option set (rules)

- **Rules:** **para-zettel-autopilot** creates/refreshes the wrapper with A–G (and optionally 0 and R). **Pipelines.md** and template: no default approved_option or approved_path. **auto-eat-queue** Step 0 processes wrappers with approved: true, re-wrap: true, or re-try: true. **feedback-incorporate** (skill) prefers approved_path from frontmatter; fallback parse body for A–G; re-wrap: true or approved_option: 0 → no path (re-wrap branch); re-try: true or approved_option: R → re-try branch (re-queue with guidance; see below).

- **User is presented with:** Options A, B, C, D, E, F, G (each a ranked PARA path; order is stabilizer-adjusted: re-rank by PARA-Actionability-Rubric v1.0 → semantic fit → path depth → alphabetize; exactly 7 options via pad-to-7 when MCP returns fewer). Option 0 (reject all), and **option R** (re-try with guidance — for roadmap/phase-direction wrappers only). When the stabilizer changed the order, wrapper has `heuristic_adjusted: true` and `heuristic_reason` for audit.

- **User choices and rule response:**
  - **Check one of A–G** → User sets **approved: true** in frontmatter manually. **Watcher** (plugin) never sets approved: true; it only syncs checkbox → approved_option and approved_path when approved: true is already set (documented in Pipelines, Cursor-Skill-Pipelines-Reference; Wrapper-Sync-Log.md). User may add **user_guidance** multiline. User runs **EAT-QUEUE** → **auto-eat-queue** Step 0 → **feedback-incorporate** resolves approved_path (frontmatter or parse body) → apply-mode ingest (or phase-direction apply; see § Phase-direction and roadmap wrappers); wrapper moved to 4-Archives/Ingest-Decisions/ (or Roadmap-Decisions/ for phase-direction).
  - **Check 0 or set re-wrap: true** → User runs EAT-QUEUE → Step 0 runs **re-wrap branch** (auto-eat-queue): backup + per-change snapshot of wrapper; ensure_structure(Re-Wrap path); move_note(wrapper, Re-Wrap); create new wrapper under Ingest/Decisions/ with Thoughts as seed, link to archived wrapper; new wrapper has approved: false, no approved_option/approved_path.
  - **Check R or set re-try: true** (roadmap/phase-direction wrappers only) → User runs EAT-QUEUE → Step 0 runs **re-try branch**: cap check (re_try_count vs re_try_max_loops); if over cap, create cap-hit wrapper (A: Force approve, B: Prune branch, 0: Re-wrap full phase) and log #review-needed to Feedback-Log; else resolve guidance from Thoughts/user_guidance, inject session_success_hint and git_diff_hint into params, append one queue entry (EXPAND-ROAD or TASK-TO-PLAN-PROMPT), set processed/used_at, move wrapper to 4-Archives/Ingest-Decisions/Roadmap-Decisions/. Re-queued entry carries previous_decisions and re_try_count for session continuity.
  - **Ignore** → No rule performs a move; wrapper stays pending.

---

## Confidence bands: high / mid / low (rules that enforce)

- **Rules:** **confidence-loops** (always) + each pipeline rule (auto-distill, auto-archive, auto-express, auto-organize, para-zettel-autopilot for ingest).

- **High (≥85%):** No user choice. **mcp-obsidian-integration** and pipeline rule: per-change snapshot then destructive action (move, rename, split, distill rewrite, append). dry_run: true then dry_run: false for every move_note.

- **Mid (68–84%):** One refinement loop only. **confidence-loops**: async preview may be written to Mobile-Pending-Actions; user may set approved: true or add feedback and re-run; commit only if post_loop_conf ≥85% and post_loop_conf &gt; pre_loop_conf. If user ignores, no destructive action; loop_* logged.

- **Low (&lt;68%):** **confidence-loops** and pipeline rule: proposal only; no loop. User is presented with proposal callout and/or Decision Wrapper. To proceed: user adds **approved: true** and optionally **user_guidance**, then runs EAT-QUEUE → **guidance-aware** and **feedback-incorporate** apply; **guidance-aware** passes guidance to classify_para, subfolder-organize, etc.; safety (snapshot, confidence ≥85%) still enforced; guidance never overrides safety.

---

## Mid-band async preview (rules)

- **Rules:** **confidence-loops** (async mid-band option); pipeline rules that implement the loop (auto-distill, auto-archive, etc.). Preview written to Mobile-Pending-Actions; **feedback-incorporate** loads approved/feedback on re-run.

- **User is presented with:** Preview in Mobile-Pending-Actions. Text may say to set approved: true or add feedback and run EAT-QUEUE.

- **User choices:** (A) Set approved: true in note frontmatter and run EAT-QUEUE or re-run. (B) Add feedback text and run EAT-QUEUE. (C) Ignore. For (A) or (B), **feedback-incorporate** runs; if post_loop_conf ≥85%, **mcp-obsidian-integration** and pipeline rule require snapshot then commit. For (C), no commit; rules require logging and no destructive action.

- **Commander “Async Approve”** — Macro may scan Mobile-Pending-Actions, set approved: true, re-queue. Same rules apply on the next EAT-QUEUE run.

---

## Guidance-aware re-run (rules)

- **Rules:** **guidance-aware** (always): trigger when approved: true + user_guidance present, or queue prompt + source_file, or #guidance-aware. Load guidance (cap 500 words); pass as soft hint to classify_para, subfolder-organize, name-enhance, distill_note, split_atomic. Optional guidance_conf_boost 0–20. Never override safety (backup, snapshot, confidence ≥85%). **feedback-incorporate** (skill) loads user_guidance or queue prompt and emits guidance for the pipeline.

- **User is presented with:** Proposal callout or Decision Wrapper suggesting to add user_guidance and approved: true and run EAT-QUEUE.

- **User choice:** Add approved: true and optionally user_guidance (multiline). Run EAT-QUEUE. Next run is guidance-aware; rules ensure guidance is passed but safety gates still apply; if confidence stays &lt;85% or snapshot fails, no destructive action (guidance_ignored: safety may be logged).

---

## Dry_run review before commit (rules)

- **Rules:** **mcp-obsidian-integration** (always): before every move_note at ≥85%, call move_note with **dry_run: true**; review effects (path, new_path, backup status, risks); then call with **dry_run: false** to commit. ensure_structure(folder_path: parent of target) before move. On dry_run failure or high-risk effects: propose_alternative_paths → calibrate_confidence → verify_classification → dry_run again; if still failing, log to Errors.md and do not commit.

- **User is presented with:** dry_run output in the run (path, new_path, backup status, risks e.g. dangling links). The agent reviews; user does not need to act unless they are reading the run log.

- **User choice:** None required; the rule enforces the sequence. If the user were to trigger a move manually, the same rule would apply (backup, ensure_structure, dry_run then commit).

---

## Queue modes and Step 0 (rules)

- **Rule:** **auto-eat-queue**. Step 0 (always first): enumerate Ingest/Decisions/**; for each wrapper with approved: true, re-wrap: true, or re-try: true and not processed → feedback-incorporate → **path-apply** (apply-mode ingest, phase-direction apply, or other wrapper_type), **re-wrap branch**, or **re-try branch** (re-queue EXPAND-ROAD/TASK-TO-PLAN-PROMPT with guidance; cap re_try_max_loops; on cap hit create cap-hit wrapper); set approved_wrappers_remaining. Then read queue; validate; dedup; sort (CHECK_WRAPPERS first); dispatch each entry by mode (INGEST MODE, EXPAND-ROAD, TASK-TO-PLAN-PROMPT, DISTILL MODE, TASK-COMPLETE, ADD-ROADMAP-ITEM, SEEDED-ENHANCE, BATCH-DISTILL, etc.); append Watcher-Result per entry; clear passed only. Step 8: if approved_wrappers_remaining, re-insert one CHECK_WRAPPERS entry for next run.

- **User is presented with:** Watcher-Result.md line(s) per request. For task-queue entries, pipeline/queue rules may perform banner cleanup (success &gt; failure): pending callout removed from note on success.

- **User choices:** Add entries (Watcher, Commander, mobile toolbar, or edit queue file). Run EAT-QUEUE or Process queue (or PROCESS TASK QUEUE for Task-Queue.md). Single valid entry → fast-path (no dedup/sort). No need to add CHECK_WRAPPERS manually; Step 0 always runs and processes approved wrappers; step 8 re-queues CHECK_WRAPPERS when needed for visibility.

---

## Decision Wrapper Watcher sync (rules and safety)

- **Documented in:** **Pipelines.md**, **Cursor-Skill-Pipelines-Reference** (Watcher bridge / Decision Wrapper checkbox sync). Not a Cursor rule; Watcher plugin behavior.

- **User is presented with:** After user checks one option A–G and sets approved: true in frontmatter, Watcher (on modify) may sync the checked letter → approved_option and approved_path in frontmatter. Sync/skip/conflict → Wrapper-Sync-Log.md; conflicts also to Errors.md.

- **Safety (rules/docs):** Watcher **never** sets approved: true or re-wrap: true. User must set approved: true manually (or via Commander). Write-loop protection: Watcher reads frontmatter before write; if already matching, skip. This prevents accidental auto-approval (stated in Pipelines.md, template, para-zettel-autopilot).

---

## Re-wrap branch (rules)

- **Rules:** **auto-eat-queue** Step 0: when feedback-incorporate returns no hard_target_path (re-wrap: true or approved_option: 0), run re-wrap branch. **feedback-incorporate** (skill) treats re-wrap: true and approved_option: 0 as “no path.”

- **User is presented with:** After re-wrap: current wrapper is in 4-Archives/Ingest-Decisions/Re-Wrap/; new wrapper under Ingest/Decisions/ with same original_path, Thoughts as seed, and link to archived wrapper. New wrapper has fresh A–G; approved: false.

- **User choices:** Set re-wrap: true or check option 0; run EAT-QUEUE. No other user action required for the branch to run; Step 0 always runs first and detects re-wrap intent.

---

## Phase-direction and roadmap wrappers (rules)

- **Rules:** **Phase-direction** wrappers are created after **EXPAND-ROAD** or **roadmap-generate-from-outline** when a phase implies direction choices (e.g. "Grid: fixed or dynamic?"). Optional heuristic in **expand-road-assist** (phase_fork_heuristic: strict/off) scans for "or"/"vs"/"options:" and sets phase_forks frontmatter; wrapper is created under **Ingest/Decisions/Roadmap-Decisions/** from Templates/Decision-Wrapper-Phase-Direction.md. **auto-eat-queue** Step 0: when wrapper_type is phase-direction and approved: true, **path-apply** = per-change snapshot of target roadmap/phase note → append provenance callout and inline "Comment guidance" near approved task → set processed/used_at → move wrapper to **4-Archives/Ingest-Decisions/Roadmap-Decisions/**.

- **User is presented with:** Phase-direction wrapper with A–G (conceptual end-state options; technical in frontmatter for provenance) and option R (re-try with guidance). Same safety: Watcher never sets approved: true; user sets approved: true or re-try: true manually.

- **User choices:** Check A–G → apply updates roadmap with chosen direction + provenance + comment guidance; wrapper archived to Roadmap-Decisions. Check R or set re-try: true → re-try branch runs (re-queue EXPAND-ROAD or TASK-TO-PLAN-PROMPT with guidance; cap re_try_max_loops). Plan evolution is visible in Wrapper-MOC and "Plan Evolution" Dataview (4-Archives/Ingest-Decisions/Roadmap-Decisions).

---

## What happens if user ignores proposal (rules)

- **Low confidence:** **para-zettel-autopilot** (ingest) or other pipeline rule has created Decision Wrapper and/or proposal callout. **confidence-loops**: no destructive action in low band. If user ignores (does not add approved: true and run EAT-QUEUE), note stays in Ingest or current location; wrapper remains under Ingest/Decisions/ pending; log may include #review-needed. No rule performs a move.

- **Mid-band preview:** If user ignores preview (does not set approved: true or add feedback and re-run), **confidence-loops** and pipeline rule: no destructive action; proposal/preview remains; loop_* fields logged. No rule commits.

---

## Commander and mobile toolbar (rules)

- **Rules:** Queue entries added by Commander/mobile are consumed by **auto-eat-queue** when the user runs EAT-QUEUE. **watcher-result-append** appends result per request. Commander macros may set commander_source, commander_macro for MOC (documented in Queue-Sources). No separate “Commander rule”; same dispatch and safety rules apply.

- **User is presented with:** Options from the toolbar or Commander (e.g. Queue Highlight: Combat, Process Queue, Async Approve, Task toolbar commands). Running EAT-QUEUE or PROCESS TASK QUEUE triggers the same rules as phrase-based triggers.

- **User choices:** Invoke macro or toolbar; optionally run EAT-QUEUE (or Process queue) if not auto-triggered. Result appears in Watcher-Result and, for task queue, possibly in banner cleanup on the note.
