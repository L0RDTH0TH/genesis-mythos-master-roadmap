---
title: Ingest Prompt Improvement Recommendations
created: 2026-02-24
tags: [pkm, ingest, prompts, para-zettel-autopilot]
para-type: Resource
status: active
links: [[2026-02-24-cursor-ingest-prompt-reference]]
---
# Ingest Prompt Improvement Recommendations

Recommendations to align the **INGEST MODE** launch prompt with the updated PARA-Zettel-Autopilot pipeline (backup-first, auto-execute ≥85%, log everything) and to use it as the single entry point for every ingest workflow.

---

## 1. Remove “wait for ok” — state auto-execute explicitly

**Issue:** The current prompts in the resource say “Propose only — wait for my explicit ok” and “Wait for my batch ok,” which **conflicts** with para-zettel-autopilot and always-ingest-bootstrap (≥85% → auto-execute, no confirmation).

**Recommendation:** The launch prompt must state clearly:
- **≥85% confidence:** Auto-execute all actions after `obsidian_create_backup` (frontmatter, tags, hub append, move, rename, log). No user confirmation.
- **<85% confidence:** Propose only; flag with #review-needed; no moves or in-place edits; note stays in Ingest/.

---

## 2. Fix filter wording and criteria

**Issue:** “Filter #place filters her or skip” is unclear (likely typo for “tag/frontmatter filters here or skip”).

**Recommendation:** Be explicit:
- Call **obsidian_list_notes** with `directory: "Ingest"` (MCP tool uses `directory`, not `dirPath`).
- **Filter:** Process notes that have `#raw-ingest` or `status: raw` in frontmatter, or **all .md** in Ingest/ if you want no filter. Skip non-markdown. State in the prompt which you use (e.g. “all .md in Ingest/” for batch, or “only notes with #raw-ingest or status: raw”).

---

## 3. Name the exact MCP tool sequence

**Issue:** “Per note: backup → classify/distill/etc.” is vague; the agent may omit or reorder steps.

**Recommendation:** In the prompt, list the **exact chain** as in para-zettel-autopilot:
1. **obsidian_create_backup** (first, per note)
2. **obsidian_classify_para** (CoT + confidence %)
3. **obsidian_split_atomic** (if multi-idea)
4. **obsidian_distill_note**
5. **obsidian_manage_frontmatter** / **obsidian_manage_tags**
6. **obsidian_append_to_hub**
7. **obsidian_move_note** (only if ≥85%)
8. **obsidian_log_action** (always; include `backup_path` from create_backup)

---

## 4. Include the exact log line format

**Issue:** If the format isn’t in the launch prompt, the agent may omit Backup or use a different format.

**Recommendation:** Put the canonical line in the prompt:
```
YYYY-MM-DD HH:MM | Excerpt: [snippet] | PARA: [type] | Changes: [list] | Confidence: X% | Proposed MV: [path or 'stay'] | Backup: [backup_path from create_backup] | Flag: [none or #review-needed + reason]
```
- For ≥85%: execute **obsidian_log_action** with this format (including backup_path).
- For <85%: propose log entry only; do not call log_action (or call with flag only, per rule).

---

## 5. Define the batch summary format

**Issue:** “Output grouped results + batch summary” is underspecified.

**Recommendation:** Require a **batch summary** at the end, e.g.:
- **Processed:** N notes.
- **High-confidence (≥85%):** X auto-executed (create_backup → classify → distill → frontmatter/tags → append_to_hub → move_note → log_action).
- **Flagged (#review-needed):** Z (list paths or excerpt).
- **Skipped/Failed:** W (e.g. backup failed, list path).

Optionally **group results** by outcome: “Auto-executed” vs “Flagged” (and “Failed” if any).

---

## 6. One canonical launch prompt for all ingest workflows

**Issue:** Two separate prompts (single-note vs batch) with different wording can drift and one still said “propose only.”

**Recommendation:** Use **one canonical prompt** that works for both:
- **Batch:** “Run INGEST MODE for entire Ingest/” → list_notes("Ingest") → process each note as below.
- **Single:** “Run INGEST MODE for this note” or “process current note” → same pipeline for one note.

Same rules in both cases: backup first, ≥85% auto-execute, <85% propose + #review-needed, log format with Backup.

---

## 7. Trinity integration in the launch prompt

**Issue:** Rules say to read `resources/` and use `prompts/` templates; the launch prompt doesn’t mention this.

**Recommendation:** Add one line to the launch prompt: “Before classifying/distilling, read relevant `resources/` (e.g. forte-para-core.md, ahrens-zettel-principles.md) and follow para-zettel-autopilot multi-shot examples.” So every ingest run triggers trinity behavior.

---

## 8. Per-note isolation and failure handling

**Issue:** Not explicit in the current prompt text.

**Recommendation:** State: “Process notes sequentially. Per-note isolation: if one note fails (e.g. create_backup fails), skip only that note, log the failure, and continue with the rest.”

---

## 9. Where to maintain the prompt

**Recommendation:** Keep the **single canonical INGEST MODE prompt** in `3-Resources/2026-02-24-cursor-ingest-prompt-reference.md` (or a dedicated `prompts/ingest-launch.md` if you add a prompts folder). Rules in `.cursor/rules/` (always-ingest-bootstrap, para-zettel-autopilot, auto-ingest-processing) stay the source of truth for behavior; the launch prompt is the **user-facing entry** that invokes that behavior and should be kept in sync with the rules.

---

## 10. Optional: “Launch phrase” for consistency

**Recommendation:** Standardize the phrase that triggers the full pipeline, e.g. **“INGEST MODE – safe batch autopilot”** or **“Process Ingest/ with autopilot.”** Document it in the resource so you (and the agent) always use the same wording for “run the full ingest pipeline with auto-execute at ≥85%.”

---

## Summary checklist

- [ ] Remove “propose only / wait for ok”; state ≥85% auto-execute, <85% propose + #review-needed.
- [ ] Clarify filter: list_notes("Ingest"), then filter by #raw-ingest/status: raw or all .md; use `directory` param.
- [ ] List exact MCP tool order: create_backup → classify_para → split_atomic (if needed) → distill_note → manage_frontmatter/tags → append_to_hub → move_note → log_action.
- [ ] Include full log line format including Backup.
- [ ] Require batch summary: Processed N; high-confidence X auto-executed; flagged Z; failed W.
- [ ] One canonical prompt for both single-note and batch.
- [ ] Mention trinity (resources/ + para-zettel-autopilot examples).
- [ ] State per-note isolation and continue-on-failure.
- [ ] Keep prompt in one place and in sync with .cursor/rules.

## Review Needed
Proposed para-type: resource. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.