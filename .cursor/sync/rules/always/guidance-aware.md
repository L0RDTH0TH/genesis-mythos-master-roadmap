---
description: Guidance-Aware Run Contract — user_guidance and queue prompt as soft hints for classify, path, split, distill
alwaysApply: true
---

# Guidance-Aware Run Contract

When a run is **guidance-aware**, user refinement instructions (from the note's `user_guidance` or the queue entry's `prompt`) are loaded and passed as a **soft hint** to classify_para, subfolder-organize, name-enhance, distill_note, and split_atomic. Guidance never overrides safety (snapshot, dry_run, confidence bands).

## Trigger (any of)

- Note has frontmatter **`approved: true`** and **`user_guidance`** is present, OR
- Current queue entry has non-empty **`prompt`** and **`source_file`** points to a note (use note's `user_guidance` if present, else use `prompt` as guidance), OR
- Note has tag **`#guidance-aware`**.

## Behavior

1. **Load guidance:** From note `user_guidance` first; if missing and queue entry has `prompt`, use `prompt` as guidance for this run.
2. **Guidance is never mandatory.** Guidance is a soft hint only. If following it would drop confidence below 68% or violate any safety gate (backup missing, dry_run fail, exclusion match), ignore it and log `guidance_ignored: safety`. The agent listens to guidance but does not override safety.
3. **Length cap:** Truncate guidance to first 500 words if length >500; log `guidance_truncated: true`. Prevents context-window bloat for classify_para / distill_note.
4. **Pass as context:** Include the (possibly truncated) guidance text in context when calling classify_para, subfolder-organize, name-enhance, distill_note, split_atomic. No new MCP parameters—the agent includes the guidance in its own context when invoking these steps.
5. **guidance_conf_boost (optional):** If note has frontmatter `guidance_conf_boost: N` (e.g. 15, range 0–20) and guidance is followed, add N to the final confidence score for this run (capped at 95%). Helps push marginal notes over the 85% move threshold without faking safety.
6. **Logging:** In pipeline log (Ingest-Log, Organize-Log, Distill-Log): `guidance_used: true | guidance_length: N`; when truncated add `guidance_truncated: true`; when ignored for safety add `guidance_ignored: safety`. Optional: first 80 chars of guidance for traceability.
7. **Safety:** Never let guidance override high-confidence (≥85%) destructive actions or safety gates (snapshot, dry_run, confidence bands). Guidance can inform classification/path/split so confidence moves into mid/high band; it does not bypass snapshot or dry_run.
8. **After run (optional, configurable):** Clearing or archiving `user_guidance` after a successful run is configurable (e.g. Second-Brain-Config: `clear_guidance_after_run: true`). Implementation of the clear step is a follow-up; this rule documents the contract.

## Cross-references

- confidence-loops — approved: true, async re-run
- auto-eat-queue — queue entry prompt, pre-dispatch
- Cursor-Skill-Pipelines-Reference — where guidance is passed in pipelines
- Parameters — user_guidance, guidance_conf_boost
