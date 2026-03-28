# Decision Wrapper Flow

**Version: 2026-03 – post-subagent migration**

Describes how Decision Wrappers are created, approved, and applied: Step 0 (always-check wrappers), path-apply, and archive.

---

## Purpose

Single reference for the lifecycle of a Decision Wrapper so pipeline authors and users know when wrappers are created, where they live, and how EAT-QUEUE applies them.

---

## Flow overview

1. **Creation:** A pipeline (e.g. Ingest, Organize, Archive, Distill, Express) hits a **mid-band** or **low-confidence** case and creates a **Decision Wrapper** under `Ingest/Decisions/` (e.g. Ingest-Decisions/, Refinements/, Low-Confidence/, Errors/, Roadmap-Decisions/). The wrapper uses `Templates/Decisions/Decision-Wrapper.md`; frontmatter includes `wrapper_type`, `pipeline`, `original_path`, `approved_option` (empty until user chooses), `approved: false`, options A–G (or 0, R, re-wrap) per User-Questions-and-Options-Reference §2.
2. **Logging:** The pipeline appends one line to `3-Resources/Watcher-Result.md`: message "created wrapper → Decisions/<subfolder>/<basename>". Ensures CHECK_WRAPPERS is in the queue when needed.
3. **User approval:** User opens the wrapper note, chooses an option (A–G or 0, R, re-wrap), sets **`approved: true`** (and optionally fills `approved_option` / `approved_path`). For ingest path-apply, the chosen option maps to a target path (e.g. A = first candidate path).
4. **EAT-QUEUE Step 0:** On the next **EAT-QUEUE** run, the Queue rule runs **Step 0 (always-check wrappers)** before reading the queue. It enumerates all markdown under `Ingest/Decisions/`. For each wrapper with `approved: true` (or re-wrap/re-try) and not yet processed:
   - **feedback-incorporate** resolves `approved_option` / `approved_path` into **hard_target_path** and **guidance_text**.
   - **Path-apply** by wrapper_type and pipeline: e.g. **ingest apply-mode** (dispatch INGEST MODE to subagent with hard_target_path so it runs Phase 2 apply-mode); **distill-apply-from-wrapper** (dispatch DISTILL MODE with approved_option as distill_lens); **express-apply-from-wrapper** (dispatch EXPRESS MODE with approved_option as express_view); **organize**, **archive**, **low-confidence**, **error** (per auto-eat-queue § Always-check wrappers).
   - After successful apply: update wrapper (used_at, processed: true); **move wrapper to archive** (Ingest/Decisions/ → 4-Archives/Ingest-Decisions/; ensure_structure, per-change snapshot, obsidian_move_note dry_run then commit).
5. **Re-wrap / re-try:** If user sets **re-wrap: true** or **re-try: true**, Step 0 handles those branches.
   - **Re-wrap branch:** When a wrapper has **re-wrap: true** or **approved_option: 0** (reject all), Step 0 runs: backup + per-change snapshot of the wrapper, **move wrapper to** `4-Archives/Ingest-Decisions/Re-Wrap/<subfolder>/`, then **create a new wrapper** under `Ingest/Decisions/` with Thoughts as seed and a link to the archived wrapper. No path apply; feedback-incorporate treats re-wrap/option 0 as no path. See Vault-Layout § 4-Archives/Ingest-Decisions/Re-Wrap.
   - **Re-try:** Cap check and requeue semantics (session_success_hint, git_diff_hint, re_try_count, append to prompt-queue, move wrapper to archive) per auto-eat-queue.mdc.
   <!-- Gap filled from old Cursor-Skill-Pipelines-Reference.md -->

---

## Key points

- **Step 0 runs first** on every EAT-QUEUE run; it does not require a queue entry. CHECK_WRAPPERS meta-entries in the queue are no-ops (already run in Step 0).
- **approved_wrappers_remaining:** If any wrapper has decision_candidate: true, approved: true, and is not marked processed, the Queue may append one CHECK_WRAPPERS entry when writing the queue back at A.8 so the next run again runs Step 0.
- **Roadmap wrappers:** Approved roadmap-next-step wrappers in Ingest/Decisions/Roadmap-Decisions/ are scanned when dispatching RESUME-ROADMAP; approved_option is mapped to params.action per User-Questions-and-Options-Reference §4; wrapper is marked processed and moved to 4-Archives/Ingest-Decisions/Roadmap-Decisions/.

---

## References

- `.cursor/rules/agents/queue.mdc` (A.0 Always-check wrappers)
- `.cursor/rules/context/auto-eat-queue.mdc` (§ Always-check wrappers, path-apply)
- User-Questions-and-Options-Reference §2 (Decision Wrappers: A–G, 0, R, re-wrap)
- [Pipelines/Ingest-Pipeline](../Pipelines/Ingest-Pipeline.md) (Phase 2 apply-mode)
