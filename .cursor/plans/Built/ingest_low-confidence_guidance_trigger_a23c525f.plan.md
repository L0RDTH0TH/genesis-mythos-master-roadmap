---
name: Ingest low-confidence guidance trigger
overview: Automatically trigger the guidance-aware decision confidence boosting system when the ingest pipeline produces low-confidence classifications, by marking notes as decision candidates, wiring them into the queue, and re-running them in guidance-aware mode once the user has provided instructions.
todos: []
isProject: false
---

# Ingest Low-Confidence Guidance Trigger — Plan

## 1. Goal and scope

- **Goal:** When the ingest pipeline (`full-autonomous-ingest`) produces **low-confidence** classification/path results, automatically route those notes into a **decision + guidance-aware** path so that:
  - The note is clearly marked as needing user guidance (decision candidate).
  - The user can provide `user_guidance` once, then `approved: true`.
  - The **next EAT-QUEUE** run re-processes the note in **guidance-aware** mode (using the existing Guidance-Aware Run Contract and `guidance_conf_boost`).
- **Scope:** Only affects ingest (`para-zettel-autopilot.mdc`, ingest section in [Cursor-Skill-Pipelines-Reference.md](3-Resources/Cursor-Skill-Pipelines-Reference.md)), queue processor ([auto-eat-queue.mdc](.cursor/rules/context/auto-eat-queue.mdc)), and Second-Brain docs (Parameters, Queue-Sources, Templates). No new MCP APIs.

---

## 2. Define when to trigger (low-confidence ingest)

Use the existing ingest confidence bands from:

- [para-zettel-autopilot.mdc](.cursor/rules/context/para-zettel-autopilot.mdc)
- [Cursor-Skill-Pipelines-Reference.md](3-Resources/Cursor-Skill-Pipelines-Reference.md)
- [Parameters.md](3-Resources/Second-Brain/Parameters.md)

**Trigger conditions:**

- **Primary:** `ingest_conf < 72` (low band), or the ingest loop ends in low band after mid-band refinement (i.e. `post_loop_conf < 72` or `post_loop_conf ≤ pre_loop_conf` and pipeline chooses “manual review”).
- **Optional extension:** For mid-band cases where the loop fails to raise confidence (`post_loop_conf ≤ pre_loop_conf`) even if still ≥72, you MAY also mark as decision candidate. Make this **configurable** via Second-Brain-Config: e.g. `low_conf_decision_threshold_mid: true | false`. **Default false** to avoid over-triggering on marginal notes.

**Plan change:**

- In the ingest section of [Cursor-Skill-Pipelines-Reference.md](3-Resources/Cursor-Skill-Pipelines-Reference.md) and [para-zettel-autopilot.mdc](.cursor/rules/context/para-zettel-autopilot.mdc), explicitly state that **low-band ingest outcomes** (and optionally mid-band failures when config is true) create **decision candidates** and hook into guidance-aware runs.

---

## 3. Mark decision candidates in the note

When ingest determines a note is low-confidence and will not perform destructive actions:

- **Frontmatter additions on the original note:**
  - `decision_candidate: true`
  - `guidance_conf_boost: 15` (or a default from config), if not already present.
  - Optionally `guidance_stage: ingest-low-conf` for future filtering.
  - **Optional:** `decision_priority: high | medium | low` — auto-set to **high** when triggered from low band (<72), **medium** when triggered from mid-band failure (`post_loop_conf ≤ pre_loop_conf`). Enables Dataview-sorting of pending decisions later.
- **Tag:** Add `#guidance-aware` to the note so the always rule ([guidance-aware.mdc](.cursor/rules/always/guidance-aware.mdc)) treats it as eligible for guidance-aware runs.
- **Callout (proposal + guidance hint):** Insert a standard callout at the top (after frontmatter) so mobile users spot them instantly:
  - `> [!warning] Decision needed (low confidence)` — this note needs guidance. Add `user_guidance: | ...` and `approved: true` to frontmatter, then run EAT-QUEUE.
  - **Default user_guidance template:** When creating the callout, also add a **suggested copy-paste** block in a separate tip callout, e.g. in [para-zettel-autopilot.mdc](.cursor/rules/context/para-zettel-autopilot.mdc):
    - `> [!tip] Suggested user_guidance (copy-paste into frontmatter)` followed by a starter YAML block the user can copy, e.g. `user_guidance: |` with placeholder lines: "Classify as [Resource/Area/Project]. Prefer path: 3-Resources/Genesis-Mythos/Phase-X-... Split if >500 words or multiple topics." Makes the first edit frictionless.
- **Logging:** When marking a note `decision_candidate: true`, log `**low_conf_trigger: low-band | mid-band-failure`** in Ingest-Log so the log tells you *why* it went to decisions.

**Optional Decision folder integration:**

- If you want a separate **decision wrapper note** (e.g. `Ingest/Decisions/<slug>--YYYY-MM-DD-HHMM.md`):
  - Create a simple decision note that:
    - Links to the original note `[[path/to/original]]`.
    - Has its own frontmatter (`approved: false`, `decision_selected`, `user_guidance` placeholder, `#guidance-aware`).
  - Either treat **original note** as the guidance target (where `user_guidance` lives) or let the **decision note** hold `user_guidance` and make the guidance-aware rule read from the decision note and apply to the original path. The simpler first implementation is: **keep `user_guidance` on the original note**; Decision folder is purely organizational.

Document this behavior in:

- [para-zettel-autopilot.mdc](.cursor/rules/context/para-zettel-autopilot.mdc): “Low-band ingest_conf (<72) → mark decision_candidate, tag #guidance-aware, add proposal callout, optional decision note in Ingest/Decisions/.”
- [Templates.md](3-Resources/Second-Brain/Templates.md): add an example decision proposal callout.

---

## 4. Queue integration: auto-creating work for EAT-QUEUE

Leverage and extend [auto-eat-queue.mdc](.cursor/rules/context/auto-eat-queue.mdc) and [Queue-Sources.md](3-Resources/Second-Brain/Queue-Sources.md):

1. **Pre-dispatch scan (already exists, extend):**
  - Today, auto-eat-queue optionally scans for notes with `approved: true` and injects queue entries.
  - Extend this so that it **also looks for notes with**:
    - `decision_candidate: true`
    - `approved: true`
    - `user_guidance` present (or tag `#guidance-aware`)
  - For each such note, inject a queue entry into the in-memory queue (do not write back to prompt-queue.jsonl), e.g.:
    - `{ "mode": "INGEST MODE", "source_file": "path/to/note.md", "prompt": <user_guidance text>, "id": "auto-decision-..." }`
  - This ensures the next **EAT-QUEUE** run will process the note through **full-autonomous-ingest** in **guidance-aware** mode without manual queue editing.
2. **Guidance-aware dispatch (already sketched in previous plan):**
  - When dispatching an entry whose `source_file` is tagged `#guidance-aware` or has `user_guidance`, treat it as **guidance-aware** and run **feedback-incorporate** to load `guidance_text` and pass it into the pipeline context.
  - The existing guidance-aware rule and feedback-incorporate extension already define how `user_guidance` and `prompt` become `guidance_text`.
3. **Queue-Sources.md updates:**
  - Clarify that for decision/ingest confidence-boost runs, the injected entries may use `mode: "INGEST MODE"` with `prompt` populated from `user_guidance`, and that users do **not** need to hand-edit prompt-queue.jsonl.

---

## 5. Applying guidance_conf_boost safely

Tie `guidance_conf_boost` into ingest confidence without breaking invariants:

- **Where:** In the ingest confidence evaluation step (described in [Cursor-Skill-Pipelines-Reference.md](3-Resources/Cursor-Skill-Pipelines-Reference.md) and [para-zettel-autopilot.mdc](.cursor/rules/context/para-zettel-autopilot.mdc)), after the pipeline has re-run the note with guidance-aware context and computed a new `ingest_conf` (or `post_loop_conf`).
- **Behavior:**
  - If `guidance_used: true` and the note has `guidance_conf_boost: N` (0–20), then set:
    - `effective_ingest_conf = min(ingest_conf + N, 95)`.
  - Use `effective_ingest_conf` to decide whether the note crosses the ≥85% threshold for destructive actions (split, distill, move). Log both raw and boosted confidence in Ingest-Log.
- **Safety:**
  - All existing gates still apply: per-change snapshot, dry_run move, exclusions, etc.
  - If guidance would push actions that still conflict with safety (e.g. missing backup, dry_run risks), follow the guidance-aware rule and **log `guidance_ignored: safety`** — do not perform destructive actions.

Document this behavior under the ingest confidence band section in [Cursor-Skill-Pipelines-Reference.md](3-Resources/Cursor-Skill-Pipelines-Reference.md) and reference `guidance_conf_boost` from [Parameters.md](3-Resources/Second-Brain/Parameters.md).

---

## 6. User workflow summary

Putting it together from the user’s perspective:

1. **Ingest runs** on Ingest/*.md. For some notes, `ingest_conf < 72`, so ingest:
  - Marks them `decision_candidate: true`, `#guidance-aware`, sets default `guidance_conf_boost`, and inserts a proposal callout (and optionally creates a decision note under Ingest/Decisions/).
2. **User reviews decision candidates** (e.g. via a view or MOC) and for each:
  - Adds a multi-line `user_guidance` block in frontmatter (instructions: atomize, path preference, etc.).
  - Sets `approved: true` when ready.
3. **User runs EAT-QUEUE.**
  - auto-eat-queue’s pre-dispatch finds notes with `decision_candidate: true`, `approved: true`, `user_guidance` present.
  - It injects queue entries (e.g. mode INGEST MODE, prompt = user_guidance).
4. For each such entry, **guidance-aware ingest** runs:
  - feedback-incorporate loads `user_guidance` (and/or prompt) as `guidance_text`.
  - classify_para, subfolder-organize, name-enhance, distill_note, split_atomic run with guidance in context.
  - `guidance_conf_boost` raises effective confidence (capped at 95) if guidance is used and safe.
  - If thresholds and safety checks pass, ingest completes the split/distill/move; otherwise it logs `guidance_ignored: safety` and leaves the note as a (still) decision candidate.

This satisfies “decision confidence boosting system triggered automatically by the ingest pipeline low confidence scores” while keeping all existing safety gates intact.

---

## 7. Files to touch

- Rules / Pipelines:
  - `.cursor/rules/context/para-zettel-autopilot.mdc` — low band → decision_candidate + #guidance-aware + callout (and optional decision note behavior reference).
  - `3-Resources/Cursor-Skill-Pipelines-Reference.md` — ingest section: low band → decision candidate; guidance-aware run + guidance_conf_boost.
  - `.cursor/rules/context/auto-eat-queue.mdc` — pre-dispatch scan extended to decision_candidate+approved+user_guidance; guidance-aware dispatch.
- Docs:
  - `3-Resources/Second-Brain/Parameters.md` — already contains user_guidance/guidance_conf_boost; add a brief line that ingest low band can auto-set `decision_candidate: true`, optional `decision_priority`, and default `guidance_conf_boost`. Document `low_conf_decision_threshold_mid` (default false) when present in Second-Brain-Config.
  - `3-Resources/Second-Brain/Queue-Sources.md` — document that decision candidates with approved+user_guidance auto-inject into the queue; no manual prompt editing needed. Note inject-only-if-file-exists and not excluded.
  - `3-Resources/Second-Brain/Templates.md` — add a standard ingest decision proposal callout pattern (warning + suggested user_guidance tip).
  - `3-Resources/Second-Brain/Rules.md` — optional one-line summary tying decision_candidate → guidance-aware ingest.
  - `3-Resources/Second-Brain/Pipelines.md` — Under "full-autonomous-ingest" (or the ingest row in the trigger table), add a cross-reference: "See low-confidence handling in para-zettel-autopilot.mdc and Guidance-Aware Run Contract (guidance-aware.mdc)."

No implementation is performed in Plan mode; this is the concrete blueprint for wiring low-confidence ingest outcomes into the guidance-aware decision confidence boosting system.