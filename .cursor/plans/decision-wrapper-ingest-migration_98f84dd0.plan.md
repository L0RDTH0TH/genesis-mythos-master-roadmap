---
name: decision-wrapper-ingest-migration
overview: Migrate ingest and queue behavior so all low-confidence ingest cases route through Decision Wrapper notes and approved wrappers are automatically consumed on later ingest runs while preserving them for training data.
todos:
  - id: audit-ingest-rule
    content: Verify and, if needed, adjust `para-zettel-autopilot.mdc` so any low/mid-confidence or review_required ingest outcome always creates/updates a Decision Wrapper and stops ingest for that note, and add an \"always-wrap-on-ambiguity\" trigger for multiple strong candidates even when ingest_conf is high (configurable).
    status: completed
  - id: align-confidence-docs
    content: Align `confidence-loops.mdc`, `Cursor-Skill-Pipelines-Reference.md`, and `Pipelines.md` so low-confidence and decay rule behavior are defined as routing into user decision loops (Decision Wrappers for ingest, async preview for others), not bare manual review.
    status: completed
  - id: document-wrapper-consumption
    content: Clarify in `auto-eat-queue.mdc` and `feedback-incorporate` SKILL docs how wrappers with approved_option/approved_path are consumed during EAT-QUEUE, including conflict resolution rules between approved_path, approved_option, user_guidance, and original-note frontmatter.
    status: completed
  - id: training-data-policy
    content: Document in Second-Brain Rules/Pipelines that Decision Wrappers under `Ingest/Decisions/` are retained as training data (not auto-deleted), and define a processed/used_at convention and Dataview history queries for wrappers that have already driven a successful ingest rerun.
    status: completed
  - id: batch-helper-wiring
    content: Implement a minimal batch helper (Commander macro or queue-injection rule) that enqueues ingest runs for all approved, unprocessed wrappers, instead of leaving the batch helper as documentation-only.
    status: pending
  - id: stale-wrapper-policy
    content: Define and document stale-wrapper handling (age thresholds, requeue behavior, and optional re-wrap against the updated vault state) so wrappers do not linger silently forever without being reconsidered.
    status: pending
isProject: false
---

# Decision Wrapper–Centric Ingest Migration

### Goals

- **Unify low/mid-confidence ingest behavior** so every such case creates a Decision Wrapper and never falls back to bare `#review-needed` in Ingest.
- **Make wrapper approvals first-class inputs** to ingest: when rerunning ingest/EAT-QUEUE, automatically consume wrappers with `approved_option`/`approved_path` and drive a guidance-aware ingest run on the original note.
- **Preserve wrappers as training data**, never auto-deleting them, but optionally marking them as processed for analytics.

### Key files to touch

- Rules:
  - `.cursor/rules/context/para-zettel-autopilot.mdc` (low/mid-confidence ingest branch; Decision Wrapper creation semantics)
  - `.cursor/rules/always/confidence-loops.mdc` and `.cursor/sync/rules/always/confidence-loops.md` (global low-band + decay rule → user-decision behavior)
  - `.cursor/rules/context/auto-eat-queue.mdc` (how EAT-QUEUE dispatches ingest and guidance-aware reruns)
- Skills:
  - `.cursor/skills/feedback-incorporate/SKILL.md` and `.cursor/sync/skills/feedback-incorporate.md` (wrapper parsing → hard_target_path + guidance_conf_boost)
- Docs:
  - `3-Resources/Second-Brain/Rules.md` (context rule map)
  - `3-Resources/Second-Brain/Pipelines.md` (confidence bands summary)
  - `3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference.md` (canonical ingest flow + confidence bands)

### Planned changes

- **1. Make Decision Wrapper the only low/mid ingest outcome (and default for ambiguity)**
  - Ensure `para-zettel-autopilot.mdc` explicitly states:
    - Trigger: `ingest_conf < 85` OR mid-band loop decay OR `review_required=true` OR multiple strong candidates.
    - Ambiguity trigger: even when `ingest_conf ≥ 85`, if `classify_para` returns **multiple strong candidates** (e.g. ≥2 paths within a small confidence window such as 5–10 points), **default to wrapping** instead of auto-moving, controlled by a config flag (e.g. `ingest_always_wrap_on_ambiguity: true` in `Second-Brain-Config.md`) so advanced users can opt out later.
    - Steps: create/update wrapper under `Ingest/Decisions/…` using `Templates/Decision-Wrapper.md`, set `decision_candidate` + `proposal_path` + `decision_priority` on original note, log `#decision-wrapper-created`, and **stop ingest** for that note.
  - In `Cursor-Skill-Pipelines-Reference.md` and `Pipelines.md`, align ingest low/mid bands so that any “manual review” case is defined as **Decision Wrapper creation**, not `#review-needed` alone, and call out the “always wrap on ambiguity” behavior explicitly (especially important for fresh vaults with many 70–85% candidates).
- **2. Tighten global confidence semantics toward user-decision loops**
  - In `confidence-loops.mdc` and its sync copy:
    - Keep low-band description as “no destructive actions; hand off to user decision flows (Decision Wrappers / async preview + approved: true) rather than auto-applying.”
    - Clarify the **decay rule** so `post_loop_conf <= pre_loop_conf` always means:
      - No destructive actions this run.
      - Log best-guess path + `#review-needed`.
      - For ingest, **route into Decision Wrapper**, not leave the note in Ingest unwrapped.
  - Confirm all references to “manual review behavior” in docs are either removed or explicitly defined as “user decision loop (Decision Wrapper / async approve)”.
- **3. Define how wrappers are consumed on rerun**
  - In `auto-eat-queue.mdc`:
    - Document that ingest reruns for decisions happen via queue entries whose `source_file` points to a wrapper in `Ingest/Decisions/`.
    - For `INGEST MODE` or `ASYNC-LOOP` entries that target wrappers:
      - Call `feedback-incorporate` first to:
        - Resolve `approved_option` A–G / `approved_path` → `hard_target_path`.
        - Extract `user_guidance` from the thoughts block.
        - Emit `guidance_conf_boost` and a short explicit context string.
      - Then run full-autonomous-ingest on the **original Ingest note**, passing `hard_target_path` + guidance into classify/subfolder-organize.
      - Define a clear **conflict resolution policy** when signals disagree:
        - Path precedence: `approved_path` (literal override) > `approved_option` candidate path > original-note frontmatter path.
        - If user_guidance text explicitly contradicts the chosen path (e.g. guidance says “keep as Resource” but path is a Project), treat this as a **decision conflict**: do not move automatically, log to Feedback-Log (and optionally create a small “conflict wrapper” note linking wrapper + original) and mark `#review-needed` so the user can resolve it.
      - Keep all backup/snapshot/dry_run gates unchanged.
- **4. Clarify wrapper lifecycle and training-data preservation**
  - In docs (Rules/Pipelines/README):
    - State that wrappers **are never auto-deleted**; they remain in `Ingest/Decisions/` as historical training examples.
    - Explain that setting `approved: true` hides them from the “pending decisions” Dataview but does not remove the note.
  - Optionally define a **frontmatter convention** like `processed: true` or `used_at: <timestamp>` that ingest can set after a successful rerun, while still leaving the wrapper in place.
  - Update the Decision-Wrapper template to include both:
    - A **pending decisions** Dataview (current behavior): `decision_candidate = true AND approved = false`.
    - A **history view** Dataview for recently decided wrappers (e.g. `approved = true`, sorted by `file.ctime` or `used_at`) so users can see “recently decided” wrappers easily.
- **5. Batch helper to process approved wrappers**
  - Implement a simple batch mode, not just design:
    - List all wrappers under `Ingest/Decisions/` with `approved: true` and not `processed: true`.
    - For each, enqueue an `INGEST MODE` or `ASYNC-LOOP` entry pointing to that wrapper (e.g. via a small helper rule or Commander macro).
    - Run EAT-QUEUE to apply decisions and mark wrappers `processed: true` on success.
  - Optionally surface this as a **toolbar / Commander action** (e.g. “Apply approved decisions”) that injects the queue entries; keep the content of wrappers unchanged so they remain usable for training.
- **6. Stale-wrapper handling**
  - Define a **staleness policy** in docs and, if desired, a helper rule:
    - Detect wrappers with `approved: false` and `created` (or file ctime) older than a configurable threshold (e.g. 30 days).
    - For each stale wrapper, re-queue it for reconsideration:
      - Re-run classify/pathing against the current vault state.
      - If confidence is now high and always-wrap-on-ambiguity is enabled, either:
        - Re-render the wrapper with updated A–G options, or
        - (Configurable) propose a direct move but still prefer wrapping by default.
    - Optionally reduce any guidance_conf_boost for very old wrappers so they don’t override newer signals too aggressively.
  - Make clear that stale wrappers are **never auto-deleted**; they are simply re-evaluated and, if still ambiguous, may be re-wrapped or left pending based on config.

### Todos

- **audit-ingest-rule**: Reconfirm `para-zettel-autopilot.mdc` low/mid-confidence section matches the Decision Wrapper–only behavior and adds an always-wrap-on-ambiguity trigger for multiple strong candidates even at high confidence (configurable).
- **align-confidence-docs**: Update `Cursor-Skill-Pipelines-Reference.md` and `Pipelines.md` so all ingest low/mid references point to Decision Wrappers / user-decision loops instead of generic manual review.
- **document-wrapper-consumption**: Expand `auto-eat-queue.mdc` and `feedback-incorporate` docs to clearly describe how approved wrappers drive guidance-aware ingest reruns, including conflict resolution semantics.
- **training-data-policy**: Add a short section to `Rules.md` or `Pipelines.md` documenting that `Ingest/Decisions/*.md` are retained as long-term decision/training data, plus a history Dataview and processed/used_at convention.
- **batch-helper-wiring**: Add a minimal batch helper (rule + Commander/toolbar macro) that queues ingest runs for all approved, unprocessed wrappers.
- **stale-wrapper-policy**: Define and document a staleness policy and helper for re-queuing old, unapproved wrappers for re-evaluation against the updated vault state.

