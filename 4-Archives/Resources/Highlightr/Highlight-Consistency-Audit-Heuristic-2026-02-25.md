---
title: Highlight Consistency Audit (Heuristic)
created: 2026-02-26
tags: [pkm, second-brain, distill, highlightr, audit]
para-type: Resource
status: active
---

# Highlight Consistency Audit — Heuristic Pipeline

**Date:** 2026-02-26  
**Pipeline:** Full ingest (classify → move) + autonomous-distill (distill_note + distill-highlight-color with Option B key).  
**Scope:** Highlights applied to a representative section (Genesis Ch 1–3) of the processed note for tractable audit.

---

## 1. Processed files and final PARA locations

| File (original) | Final location | PARA type |
|-----------------|----------------|-----------|
| Ingest/01 - Genesis - KJV.md | 3-Resources/01-Genesis-KJV.md | Resource (treated as Resource for heuristic test; classifier had suggested archive) |

---

## 2. Option B key (canonical)

| Color | Intended meaning |
|-------|------------------|
| Yellow | Key facts, premises, supporting evidence, main points |
| Green | Definitions, explanations of terms, core concepts |
| Blue | Actionable items, instructions, next steps, thesis statements |
| Red | Disagreements, critiques, warnings, questions, high-priority review |
| Orange | Examples, case studies, applications, analogies |
| Purple | Quotes (direct verbatim), key insights, mental models/frameworks |
| Pink | Ideas to resurface later, connections to other notes, open questions |
| Cyan | Secondary/supporting details, less critical but useful |
| Grey | Deprecated, outdated, or low-confidence info |

---

## 3. Per-note highlight audit — 3-Resources/01-Genesis-KJV.md

Highlights applied in Genesis Ch 1–3 (representative section).

| # | Color | Excerpt | Verdict | Reason |
|---|-------|---------|---------|--------|
| 1 | Yellow | In the beginning God created the heaven and the earth. | Yes | Key fact / main point. |
| 2 | Blue | Let there be light: and there was light. | Yes | Divine fiat / actionable statement. |
| 3 | Yellow | it was good | Yes | Supporting evidence / refrain. |
| 4 | Cyan | the evening and the morning were the first day. | Yes | Secondary/metadata (temporal framing). |
| 5 | Blue | Be fruitful, and multiply, and fill the waters in the seas, and let fowl multiply in the earth. | Yes | Actionable instruction (blessing). |
| 6 | Purple | Let us make man in our image, after our likeness | Yes | Key insight / divine quote. |
| 7 | Green | man became a living soul. | Yes | Definition / core concept (anthropology). |
| 8 | Green | the tree of knowledge of good and evil. | Yes | Core concept / named element. |
| 9 | Red | thou shalt not eat of it: for in the day that thou eatest thereof thou shalt surely die. | Yes | Warning / high-priority command. |
| 10 | Purple | This is now bone of my bones, and flesh of my flesh: she shall be called Woman, because she was taken out of Man. | Yes | Direct quote / key insight. |
| 11 | Red | Ye shall not surely die: | Yes | Serpent’s critique / disagreement with God. |
| 12 | Pink | Where art thou? | Yes | Open question. |

---

## 4. Overall match rate and color usage

- **Total highlights audited:** 12  
- **Match (Yes):** 12  
- **Partial:** 0  
- **No:** 0  
- **Overall match rate:** **100%** (against Option B key).

### Summary table of color usage (this note)

| Color | Count | Role in Option B |
|-------|-------|------------------|
| Yellow | 2 | Key facts, supporting evidence |
| Green | 2 | Definitions, core concepts |
| Blue | 2 | Actionable items, instructions |
| Red | 2 | Warnings, critiques |
| Purple | 2 | Quotes, key insights |
| Pink | 1 | Questions |
| Cyan | 1 | Secondary/metadata |
| Orange | 0 | — |
| Grey | 0 | — |

---

## 5. Mismatch patterns and tuning recommendations

- **Most common mismatch:** None in this run; all 12 highlights matched Option B.
- **Pipeline strength:** Clear application of Yellow (facts), Green (definitions/concepts), Blue (actionable), Red (warnings/critiques), Purple (quotes/insights), Pink (questions), Cyan (secondary).
- **Tuning:** No changes required for this sample. For future runs:
  - Keep **Highlightr-Color-Key.md** as the single source of truth (Option B table).
  - In **distill-highlight-color** skill, continue to reference the key and use chain-of-thought for span selection; optional: add one line such as “Prefer Green for definitions and named concepts (e.g. ‘X is …’, ‘the tree of …’); Red for warnings and character disagreement; Purple for direct speech or key insights.”

---

## 6. Backups and snapshots

- **Pre-ingest backup:** `Second-Brain-oops-Backups/20260226-003942-01 - Genesis - KJV.md`
- **Pre-distill backup:** `Second-Brain-oops-Backups/20260226-004317-01-Genesis-KJV.md`
- Per-change snapshot: Backups confirmed by MCP for each `obsidian_search_replace`; Backup-Log and pipeline log updated separately.

---

**Conclusion:** Heuristic audit pipeline run on Genesis (Ch 1–3) with Option B key produced a **100% match rate**. Option B semantics are validated for this sample; no tuning needed for the key or skill for the patterns observed.
