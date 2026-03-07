---
title: 
created: "2026-02-23 21:29"
tags: 
para-type: resource
status: ingest
links: [[2026-02-24-ingest-prompt-improvement-recommendations]]
---
# Raw Capture — 2026-02-23 21:29

## What am I thinking?

*Paste/type your core idea, observation, question, or spark here. Keep it focused — aim for one main thought if possible (Zettelkasten atomicity).*

## What does this seem to mean?

*Quick reflection: Why does this matter? What connections/insights does it trigger? Implications? Future use?*

## TL;DR (add later or during review)

*Optional quick 1–2 sentence summary — fill this in when distilling/processing.*

## Images / Visuals

*Paste images directly here (drag-drop or Cmd/Ctrl+V), or add links. Include alt text or short caption for each to make them searchable/linked.*

- ![description](image-link-or-pasted) — caption or why it's relevant
- (or just paste images one after another)

## Related Links / Sources

- [[Existing note or hub]] — quick reason
- External source: [URL or description]

## AI/Chat Appendices

### Canonical INGEST MODE prompt (use this to launch every ingest workflow)

**INGEST MODE – safe batch autopilot for entire Ingest/ (or current note)**

Follow updated PARA-Zettel-Autopilot + rules: backup-first, auto-execute at ≥85%, log everything.

1. **List & filter**
   - **Batch:** Call **obsidian_list_notes** with `directory: "Ingest"`. Process all `.md` files (or only those with `#raw-ingest` or `status: raw` in frontmatter—state which you use). Skip non-markdown.
   - **Single note:** Process the currently open/focused note in Ingest/ (or the note I just created/pasted into).

2. **Per note pipeline (strict order)**
   - Read relevant `resources/` first (e.g. forte-para-core.md, ahrens-zettel-principles.md); follow para-zettel-autopilot multi-shot examples.
   - **obsidian_create_backup** (first, per note).
   - **obsidian_classify_para** (CoT + confidence %).
   - If multi-idea → **obsidian_split_atomic**.
   - **obsidian_distill_note**.
   - **obsidian_manage_frontmatter** / **obsidian_manage_tags**.
   - **obsidian_append_to_hub**.
   - If **≥85%:** **obsidian_move_note** to PARA path (1-Projects/, 2-Areas/, 3-Resources/, 4-Archives/).
   - **obsidian_log_action** (always): include `backup_path` from create_backup.
   - **Log line format:** `YYYY-MM-DD HH:MM | Excerpt: [snippet] | PARA: [type] | Changes: [list] | Confidence: X% | Proposed MV: [path or 'stay'] | Backup: [backup_path] | Flag: [none or #review-needed + reason]`

3. **Confidence**
   - **≥85%:** Auto-execute all actions (frontmatter, tags, hub, move, rename, log). No confirmation.
   - **<85%:** Propose only; flag #review-needed; no moves or in-place edits; note stays in Ingest/.

4. **Batch behavior**
   - Process notes sequentially. Per-note isolation: if one note fails (e.g. backup fails), skip only that note, log failure, continue.

5. **Output**
   - Grouped results: auto-executed vs flagged (and failed if any).
   - **Batch summary:** Processed N | High-confidence (≥85%) auto-executed: X | Flagged (#review-needed): Z | Skipped/Failed: W.

**Launch phrase:** “INGEST MODE – safe batch autopilot” or “Process Ingest/ with autopilot” → run this pipeline.



- [YYYY-MM-DD HH:MM] — Grok response on [topic]:

[pasted output]


- [YYYY-MM-DD HH:MM] — Cursor agent log:

[pasted output]

---
*No auto-filtering — manual review / Cursor Agent processing required. Keep in Ingest/ until confirmed move. Run Templater after creation if needed, then save & sync.*

## Why resource?
Assigned based on content/frontmatter (confidence ~85%).

## Review Needed
Proposed para-type: resource. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.