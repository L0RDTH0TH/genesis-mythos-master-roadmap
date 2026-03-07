---
name: Highlight consistency audit
overview: "Heuristic highlight consistency test: one Cursor prompt runs full ingest + classify + move + autonomous-distill (with Option B key) on test files in Ingest/, then self-audits highlights and writes a single audit report note. Only two manual steps: update the key, drop files in Ingest/, paste the prompt."
todos: []
isProject: false
---

# Highlight Consistency Audit — Plan (Heuristic Pipeline)

The audit uses the **existing ingest + distill pipelines** with **one Cursor prompt**. The LLM ingests files from `Ingest/`, classifies and moves them, runs full `autonomous-distill` (including `distill-highlight-color` with the updated Option B key), then **self-audits** the resulting highlights and writes a clean audit report. No manual per-highlight scan.

**Manual steps:** (1) Update Highlightr-Color-Key to Option B and save. (2) Drop test .md file(s) into `Ingest/`. (3) Paste the single prompt in Cursor.

---

## 1. Update Highlightr-Color-Key.md to Option B (single source of truth)

Open [3-Resources/Highlightr-Color-Key.md](3-Resources/Highlightr-Color-Key.md) and **replace** the entire “Semantic use” / “When to apply” table with:

```markdown
| Color  | Intended meaning (Option B baseline)                                      |
|--------|---------------------------------------------------------------------------|
| Yellow | Key facts, premises, supporting evidence, main points                     |
| Green  | Definitions, explanations of terms, core concepts                         |
| Blue   | Actionable items, instructions, next steps, thesis statements             |
| Red    | Disagreements, critiques, warnings, questions, high-priority review       |
| Orange | Examples, case studies, applications, analogies                           |
| Purple | Quotes (direct verbatim), key insights, mental models/frameworks          |
| Pink   | Ideas to resurface later, connections to other notes, open questions      |
| Cyan   | Secondary/supporting details, less critical but useful                    |
| Grey   | Deprecated, outdated, or low-confidence info                              |
```

Then:

- Update the **Vault default** section to match (e.g. Yellow = key facts, Green = definitions, Blue = actionable).
- (Optional) Add a short “Example snippet” column or one-line examples per color so the skill sees them clearly.
- Keep existing “For MCP / pipelines”, `highlight_key`, and “Project-Specific Guidelines” sections.
- Save the file.

This is the single source of truth for the entire pipeline.

---

## 2. Drop test content into Ingest/

- Convert your book (or selected chapters/excerpts) to one or more clean `.md` files, or use existing test markdown.
- Place them in **`Ingest/`**.
  - **Recommended** for 1 Project + 1 Area + 1 Resource coverage:
    - `test-project-book-chapter.md`
    - `test-area-maintenance.md`
    - `test-resource-literature-summary.md`
  - Or a single file (e.g. `book-test.md`) — the classifier will assign PARA and move accordingly.
- Use content with mixed facts, definitions, actions, critiques, quotes, etc. for a strong heuristic test.

---

## 3. Launch Cursor (vault open) and paste the one prompt

Paste the following **entire block** into Cursor (chat or Composer) and submit:

```markdown
**HEURISTIC HIGHLIGHT CONSISTENCY AUDIT – FULL INGEST PIPELINE**

I have placed test markdown file(s) (the book / sample content for Project/Area/Resource) into the `Ingest/` folder.

Run the complete post-capture autonomous pipeline on **every** file currently in `Ingest/`:

1. Classify each file's PARA type and target folder.
2. Ensure folder structure (`obsidian_ensure_structure`).
3. Move note (`obsidian_move_note`), handling any conflicts.
4. Run full `autonomous-distill` on the moved note:
   - Generate TL;DR
   - Apply atomic splitting + split-from/into linking if appropriate
   - Apply highlights **strictly** using the `distill-highlight-color` skill and the **updated Option B semantics** from `3-Resources/Highlightr-Color-Key.md` (table above is now canonical)
   - All other distill steps (backlinks, related frontmatter, etc.)
5. Create per-change snapshot + batch snapshot.

6. Immediately after processing all files, create a new note at:
   `3-Resources/Highlight-Consistency-Audit-Heuristic-2026-02-25.md`

   In that note, produce:
   - List of processed files and their final PARA locations
   - Per-note highlight audit: every applied highlight (color + short excerpt), match verdict (Yes / Partial / No), reason
   - Overall match rate % against Option B key
   - Summary table of color usage
   - Top 1–2 mismatch patterns (if any)
   - Specific tuning recommendations for `distill-highlight-color` skill or Highlightr-Color-Key.md

Use every relevant context rule and skill (`auto-distill.mdc`, `distill-highlight-color`, etc.). Prioritize perfect adherence to the new color key. Be explicit and transparent in the audit note.

When complete, reply only with: "✅ Heuristic audit pipeline finished – review 3-Resources/Highlight-Consistency-Audit-Heuristic-2026-02-25.md"
```

---

## 4. What happens next

- Cursor runs: **ingest** (classify → ensure_structure → move) → **autonomous-distill** (including distill-highlight-color with Option B) → **self-audit** → **write** [3-Resources/Highlight-Consistency-Audit-Heuristic-2026-02-25.md](3-Resources/Highlight-Consistency-Audit-Heuristic-2026-02-25.md).
- You review the audit note: per-note highlights, match rate, mismatch patterns, tuning suggestions.

---

## 5. Evaluate and tune

- **If match rate ≥ 85–90%:** Treat as validated. Say **“Mark audit as done”** to get the final checklist and updated status (99–100%).
- **If lower:** Use the audit note’s suggested 1–2 lines for the skill prompt or key. Apply those edits, then re-run:
  - Same prompt again (with same or fresh files in Ingest/), or
  - A shortened “re-distill only” prompt on the same moved notes.
- Re-test in under a few minutes. Once results are acceptable, say **“Mark audit as done”** for the final checklist.

---

## 6. Optional later: dashboard alerts for “inconsistent” patterns

[3-Resources/_dv-visual-health-dashboard.js](3-Resources/_dv-visual-health-dashboard.js) Section 4 can be extended with alerts based on Option B semantics (e.g. “>40% Yellow but low Green → possible definition bleed”) after the audit is done and semantics are stable.

---

## Summary

| Step | Action |
|------|--------|
| 1 | Update [Highlightr-Color-Key](3-Resources/Highlightr-Color-Key.md) to Option B table; adjust Vault default; optionally add example snippets. Save. |
| 2 | Drop test .md file(s) into `Ingest/` (one or three files; mixed content recommended). |
| 3 | In Cursor, paste the **Heuristic Highlight Consistency Audit** prompt (full block above). Submit. |
| 4 | Review `3-Resources/Highlight-Consistency-Audit-Heuristic-2026-02-25.md` (match rate, mismatches, tuning suggestions). |
| 5 | If match &lt;85%: apply suggested tuning to key/skill → re-run prompt or re-distill → re-check. If ≥85%: say **“Mark audit as done”** for final checklist. |
| 6 | (Optional) Add inconsistency alerts to the dashboard script once semantics are stable. |
