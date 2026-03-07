---
title: Highlight Consistency Audit — Expanded Plan (v2)
created: 2026-02-25
tags: [pkm, second-brain, distill, highlightr, audit]
para-type: Resource
status: active
---

# Highlight Consistency Audit — Expanded Plan (v2)

**Goal**  
Run a clean heuristic test via ingest → distill pipeline and verify **both**:
- Semantic correctness (Option B key)
- Technical correctness (Highlightr plugin storage format)

**Chosen approach**  
Adopt **Option B semantics** as the single source of truth **and** embed the full Highlightr plugin usage & storage rules directly inside [Highlightr-Color-Key.md](Highlightr-Color-Key.md).  
This eliminates any chance of the LLM guessing syntax (no more `==text==^{Yellow}` failures).

---

## 1. Update Highlightr-Color-Key.md — now the SINGLE source of truth

(Do this **before** any test run.)

The key has been updated to include:
- **Section 1 — Semantic Mapping (Option B – Canonical):** Table of Color | Intended meaning.
- **Section 2 — Highlightr Plugin Usage & Storage Format (Technical Rules – MANDATORY):** Storage mode (Inline CSS preferred), exact `<mark style="background: #...">` per color, gating rules (no `==text==`, no `^{Color}`), vault default mapping, optional example snippets.

Confirm hex codes match your Highlightr plugin: highlight once in Obsidian, copy from source. The key is the **only** place the pipeline looks for color meaning and exact output format.

---

## 2. Choosing the three notes

- **Project:** e.g. `1-Projects/Test-Project/2026-02-25-distill-messy.md` (or your book chapter)
- **Area:** Create or use one short Area note → run distill
- **Resource:** Same for one Resource note

Place the chosen files in **Ingest/** before running the prompt.

---

## 3. Where to log the audit

Create or update: **3-Resources/Highlight-Consistency-Audit-Heuristic-2026-02-25.md**

The pipeline will write the audit results there (processed files, per-highlight audit with semantic + format match, overall %, summary table, mismatches + tuning suggestions).

---

## 4. The ONE Cursor prompt (updated for new key)

Paste the following into Cursor (chat or Composer) and submit:

```markdown
**HEURISTIC HIGHLIGHT CONSISTENCY AUDIT – FULL INGEST + DISTILL**

Files are in Ingest/. Run the complete ingest → classify → move → distill pipeline.

When applying highlights, use **only** the rules in 3-Resources/Highlightr-Color-Key.md (both the semantic table **and** the exact Highlightr storage format section).

Create the audit note at 3-Resources/Highlight-Consistency-Audit-Heuristic-2026-02-25.md containing:
- Processed files & final locations
- Per-highlight audit (color, excerpt, semantic match, format match, verdict)
- Overall semantic match % and format correctness %
- Summary table of color usage
- Top mismatches + exact tuning suggestions

Reply only: "✅ Heuristic audit finished – review the audit note"
```

---

## 5. Manual / self-audit process

- Open each resulting note in **Source mode** → confirm `<mark style=...>` (or class) format.
- In **Reading mode** → verify colors appear correctly.
- Audit note will already contain the match rates.

---

## 6. Evaluate and tune (semantics + format)

- **≥90% on both** semantic and format → validated.
- If format fails: the audit note will point to the exact line to strengthen in the key.
- Re-run the same prompt after any tweak (usually 1–2 minutes).
- When both rates are ≥90%, say **“Mark audit as done”** for the final checklist (99–100%).

---

## 7. Optional later improvements

- Add Dataview queries in the Visual Health Dashboard to flag any legacy `==text==` highlights.
- One-time batch re-color script for old notes (once stable).

---

## Summary table

| Step | Action |
|------|--------|
| 1 | Expand [Highlightr-Color-Key.md](Highlightr-Color-Key.md) with Option B semantics **+** full Highlightr storage format & gating rules |
| 2 | Drop test file(s) into `Ingest/` |
| 3 | Paste the one Cursor prompt above |
| 4 | Review generated audit note (semantics + format) |
| 5 | Tune key if needed → re-run prompt |
| 6 | Mark audit complete once ≥90% on both |

---

## Next action

1. Confirm hex codes in [Highlightr-Color-Key.md](Highlightr-Color-Key.md) match your Highlightr plugin (highlight once, copy from source).
2. Drop your test book/chapter or Project/Area/Resource notes into **Ingest/**.
3. Paste the new one prompt (Section 4) into Cursor.

When highlights come out clean (both semantically and technically), say **“Mark audit as done”** for the final checklist at 99–100%.
