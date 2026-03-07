---
name: feedback-incorporate
description: Scans queue or Mobile-Pending-Actions for user edits (approved true, text feedback); adapts params (e.g. liberalness, lens) and loads user_guidance for guidance-aware runs. Lightweight; no destructive writes. Use at start of queue processor or when re-running after async preview.
---

# feedback-incorporate

## When to use

- At **start of queue processor** (optional) or when re-processing a note after an async preview (user set `approved: true` or added feedback in Mobile-Pending-Actions).
- **Always-applied** or invoked when EAT-QUEUE runs and queue/Mobile-Pending-Actions contain recent user edits.
- When the run is **guidance-aware** (see [guidance-aware](.cursor/rules/always/guidance-aware.mdc)): also read `user_guidance` and emit guidance output for the pipeline.

## Instructions

1. **Scan**: Read [Mobile-Pending-Actions](3-Resources/Mobile-Pending-Actions.md) and, if applicable, the last N queue entries or the current entry's context. Look for **`approved: true`** in note frontmatter (for the note being re-processed) or **text feedback** (e.g. user-added comments, revised lens/view strings).

2. **Load guidance (guidance-aware runs):** If the note (from queue `source_file` or current context) has frontmatter **`user_guidance`**, set `guidance_text` to that value; else if the current queue entry has non-empty **`prompt`**, set `guidance_text` to `prompt`. If length >500 words, truncate to first 500 words and set `guidance_truncated: true`. Set `guidance_used` and `guidance_length` accordingly. Emit **guidance** object: `{ guidance_text: string | null, guidance_used: boolean, guidance_length: number, guidance_truncated?: boolean }` so the pipeline can include `guidance_text` in context when invoking classify_para, subfolder-organize, name-enhance, distill_note, split_atomic.

3. **Adapt params**: From feedback or approved flag, adapt parameters for the upcoming run without writing back to the note yet. Examples: increase/decrease highlight liberalness, set `distill_lens` or `express_view` from user text, adjust depth (layers) if user requested "simpler" or "deeper".

4. **No destructive writes**: This skill only **reads** and **outputs** adapted params and guidance (or updates in-memory/context for the pipeline). Do not call `obsidian_update_note` or `obsidian_search_replace` for feedback-incorporate itself; the pipeline uses the adapted params and guidance in subsequent steps.

5. **Observability**: Optionally log that feedback was incorporated (e.g. "approved: true; lens set to beginner") and when guidance was passed ("guidance_used: true; length: N") in [Feedback-Log.md](3-Resources/Feedback-Log.md) or the pipeline log for MOC/analytics.

### Wrapper support (Decision Wrappers under Ingest/Decisions/)

- When a queue entry's `source_file` points to a **Decision Wrapper** under `Ingest/Decisions/` (see `para-zettel-autopilot.mdc`) and the wrapper has either `approved: true` or an explicit `approved_option` / `approved_path` set in frontmatter:
  - **Resolve target_path (letters A–G)**:
    - **Prefer `approved_path`:** If `approved_path` is present in frontmatter, use it as the **hard target path** (highest-priority). No need to map from letter.
    - **Fallback parse body:** If `approved_path` is missing but `approved_option` is one of `A`–`G`, resolve the path by: (1) using frontmatter candidate keys if present (e.g. `candidate_a_path`), or (2) parsing the wrapper body for the line that matches that letter (e.g. `**F.** path — N%`) and extracting the path from that line. Use that as `hard_target_path`.
    - **Re-wrap / no path:** If `re-wrap: true` or `approved_option` is `0` (reject all), emit **no** `hard_target_path` — the pipeline runs the re-wrap branch (archive wrapper to Re-Wrap, create new wrapper with Thoughts as seed).
  - **Extract guidance**:
    - Read the "Thoughts / corrections / why this location?" block in the wrapper body and treat it as `user_guidance` text for the original note.
    - Emit this text via the existing `guidance` object so `guidance-aware.mdc` can pass it into classify_para / subfolder-organize on the re-run.
  - **Emit ingest hints (hard path + boosted guidance)**:
    - Include a recommended `guidance_conf_boost` (e.g. 18) and the resolved `target_path` / `hard_target_path` in the skill's output so the ingest pipeline can treat this as a **hard path + boosted guidance** on the next run.
    - When emitting guidance for classify_para / subfolder-organize, include a short, explicit note in the prompt context such as:  
      `"User explicitly chose: {{approved_option}} → {{hard_target_path}}. User reasoning: {{user_guidance}}. Treat selected path as very high confidence."`
- This skill remains **read-only**: it does **not** mark wrappers `approved: true` or move notes itself; the queue processor + ingest pipeline perform writes and moves using the emitted `hard_target_path` and `guidance_text`.

## MCP tools

- `obsidian_read_note` — read Mobile-Pending-Actions, optional note frontmatter for approved/feedback and `user_guidance`

## Confidence gate

Not applicable (read-only, no destructive action). Run when queue processor or re-run context indicates user feedback is present, or when run is guidance-aware.

## Reference

- [confidence-loops](.cursor/rules/always/confidence-loops.mdc) — async mid-band, approved: true
- [guidance-aware](.cursor/rules/always/guidance-aware.mdc) — Guidance-Aware Run Contract; when to load and pass user_guidance
- [Queue-Sources](3-Resources/Second-Brain/Queue-Sources.md) — ASYNC-LOOP mode, queue entry prompt
- [Feedback-Log](3-Resources/Feedback-Log.md) — aggregate user refinements, loop outcomes
