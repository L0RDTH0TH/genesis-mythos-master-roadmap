---
title: Highlight Consistency Audit — Genesis KJV (Targeted Test)
created: 2026-02-26
tags: [pkm, second-brain, distill, highlightr, audit, genesis]
para-type: Resource
status: active
---

# Highlight Consistency Audit — Genesis KJV (Targeted Test)

**Date:** 2026-02-26  
**Pipeline:** Full post-capture (classify → move → autonomous-distill + distill-highlight-color).  
**Scope:** Single file `Ingest/01 - Genesis - KJV.md` → moved to 3-Resources; highlights applied to representative section (Genesis Ch 1–3) using **only** Highlightr-Color-Key.md Section 2 format (`<mark style="background: #HEX...">`).

---

## 1. Final PARA location of processed note(s)

| Original path | Final path | PARA type (classified) |
|---------------|------------|-------------------------|
| Ingest/01 - Genesis - KJV.md | 3-Resources/01-Genesis-KJV.md | Resource (classifier suggested archive ~70%; placed in Resources for heuristic test) |

---

## 2. List of all applied highlights

Per-highlight: color, short excerpt, semantic verdict (Yes/Partial/No + reason vs Option B key), format verdict (correct Highlightr storage? Yes/No + raw source snippet).

| # | Color | Excerpt (10–20 words) | Semantic verdict | Format verdict | Raw source snippet |
|---|-------|------------------------|------------------|----------------|--------------------|
| 1 | Yellow | In the beginning God created the heaven and the earth. | Yes — key fact, main point (Option B). | Yes | `<mark style="background: #FFF3A3A6;">In the beginning God created the heaven and the earth.</mark>` |
| 2 | Blue | Let there be light: and there was light. | Yes — divine fiat / actionable statement. | Yes | `<mark style="background: #A3D8FFA6;">Let there be light: and there was light.</mark>` |
| 3 | Yellow | it was good | Yes — supporting evidence, refrain. | Yes | `<mark style="background: #FFF3A3A6;">it was good</mark>` |
| 4 | Cyan | the evening and the morning were the first day. | Yes — secondary/temporal framing. | Yes | `<mark style="background: #A3FFFFA6;">the evening and the morning were the first day.</mark>` |
| 5 | Blue | Be fruitful, and multiply, and fill the waters in the seas... | Yes — actionable instruction (blessing). | Yes | `<mark style="background: #A3D8FFA6;">Be fruitful, and multiply, and fill the waters in the seas, and let fowl multiply in the earth.</mark>` |
| 6 | Purple | Let us make man in our image, after our likeness | Yes — key insight / divine quote. | Yes | `<mark style="background: #E6CCFFA6;">Let us make man in our image, after our likeness</mark>` |
| 7 | Green | man became a living soul. | Yes — definition / core concept (anthropology). | Yes | `<mark style="background: #C1E1C1A6;">man became a living soul.</mark>` |
| 8 | Green | the tree of knowledge of good and evil. | Yes — core concept / named element. | Yes | `<mark style="background: #C1E1C1A6;">the tree of knowledge of good and evil.</mark>` |
| 9 | Red | thou shalt not eat of it: for in the day that thou eatest thereof thou shalt surely die. | Yes — warning / high-priority command. | Yes | `<mark style="background: #FFAAAAA6;">thou shalt not eat of it: for in the day that thou eatest thereof thou shalt surely die.</mark>` |
| 10 | Purple | This is now bone of my bones, and flesh of my flesh... | Yes — direct quote / key insight. | Yes | `<mark style="background: #E6CCFFA6;">This is now bone of my bones, and flesh of my flesh: she shall be called Woman, because she was taken out of Man.</mark>` |
| 11 | Red | Ye shall not surely die: | Yes — serpent's critique / disagreement with God. | Yes | `<mark style="background: #FFAAAAA6;">Ye shall not surely die:</mark>` |
| 12 | Pink | Where art thou? | Yes — open question. | Yes | `<mark style="background: #FFC1CCA6;">Where art thou?</mark>` |

---

## 3. Overall match rates

- **Semantic match (vs Option B key):** 12 / 12 → **100%**
- **Technical / format correctness (Highlightr `<mark>` storage):** 12 / 12 → **100%**

No `==text==` or `^{Color}` used; all highlights use inline CSS from Highlightr-Color-Key.md Section 2.

---

## 4. Color usage summary table (count per color)

| Color | Count | Option B role |
|-------|-------|----------------|
| Yellow | 2 | Key facts, supporting evidence |
| Green | 2 | Definitions, core concepts |
| Blue | 2 | Actionable items, instructions |
| Red | 2 | Warnings, critiques, disagreement |
| Purple | 2 | Quotes, key insights |
| Pink | 1 | Open questions |
| Cyan | 1 | Secondary/temporal details |
| Orange | 0 | — |
| Grey | 0 | — |

---

## 5. Top mismatch patterns (semantic or format)

- **None.** All 12 highlights matched Option B semantically and used the correct `<mark style="background: #...">` format. No legacy `==...==` or `^{Color}` present in the applied section.

---

## 6. Specific, actionable tuning recommendations

- **Key and skill are aligned:** The pipeline referenced Highlightr-Color-Key.md (Section 1 semantics + Section 2 exact storage format) and applied only inline CSS. No change required for this run.
- **For future runs:** Keep the gating rule explicit in the key and skill: "Never use `==text==` or `^{Color}` for semantic highlights; always use the exact format from Section 2."
- **Optional:** Add one line to the key under Green: "Prefer Green for definitions and named concepts (e.g. 'X is …', 'the tree of …'); Red for warnings and character disagreement; Purple for direct speech or key insights" to reinforce biblical/narrative handling.

---

## 7. Observations on how well biblical text fits Option B semantics

- **Narrative and speech:** KJV Genesis maps cleanly to Option B: creation statements → Yellow (facts); divine commands and blessings → Blue (actionable); definitions (e.g. "living soul", "tree of knowledge of good and evil") → Green; warnings and prohibition → Red; serpent’s contradiction → Red; direct speech (e.g. Adam’s "bone of my bones") → Purple; divine question "Where art thou?" → Pink.
- **Refrains and repetition:** "It was good" as Yellow (supporting evidence) and "the evening and the morning were the Nth day" as Cyan (secondary/temporal) fit well and keep the key consistent.
- **No stretch:** No need to force Orange (examples) or Grey (deprecated) in Ch 1–3; the chosen palette covered the representative content without over-tagging.

---

## 8. Backups and snapshots

- **Pre-move backup:** `Second-Brain-oops-Backups/20260226-011438-01 - Genesis - KJV.md`
- **Pre–search_replace backups:** Confirmed by MCP for each highlight edit (e.g. `20260226-004317-01-Genesis-KJV.md`).
- Per-change snapshot: Backups confirmed by MCP; Backup-Log and pipeline logs can be updated separately.

---

**Conclusion:** Genesis KJV targeted test (Ch 1–3) produced **100% semantic match** and **100% format correctness**. Option B semantics and the Highlightr storage format from Highlightr-Color-Key.md are validated for this biblical narrative sample.
