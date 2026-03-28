---
name: Plan-mode question UI hardening v2
overview: "Second hardening pass for Plan-mode prompt crafter: align with Cursor's actual Plan mode clarifying-questions behavior (from docs and forum), fix output format so the question UI triggers reliably, and address the known newline-formatting bug. No-skip invariants from the first pass are kept."
todos: []
isProject: false
---

# Plan-mode prompt crafter: second hardening pass (question UI + format)

## Goal

Make the first-pass no-skip hardening work in practice by (1) aligning rule and docs with how Cursor's Plan mode clarifying-questions UI actually works, and (2) specifying an output format that triggers the question box and avoids the known Cursor formatting bug. The previous changes "failed" — likely due to wrong or ambiguous question UI format, or newline/rendering issues.

## Research summary (Cursor + forum)

- **Context7:** The Context7 MCP (plugin-context7-plugin-context7) provides `resolve-library-id` and `query-docs` for **programming libraries** (e.g. Next.js, MongoDB). Cursor IDE is not a library in Context7, so Cursor Plan mode behavior was researched via web and forum instead.
- **Cursor docs** ([cursor.com/docs/agent/plan-mode](https://cursor.com/docs/agent/plan-mode)): Plan mode "asks clarifying questions" and "researches your codebase" before generating a plan. No documented format for triggering the question UI.
- **Cursor 2.1 changelog / blog:** Clarifying questions are shown in an **interactive UI** with "3–5 targeted questions," **multiple-choice selectors**, and optional **text input**. The **model's output** drives whether Cursor shows "regular (a/b/c)" single-choice vs multi-choice; users can type custom answers if needed.
- **Forum (Feb 2026):** [Formatting of question in Plan Mode](https://forum.cursor.com/t/formatting-of-question-in-plan-mode/152418) — **Bug:** "The question is displayed with '\n' characters instead of newlines." Cursor team has a PR open. So agent output that results in literal `\n` (e.g. escaped newlines or certain markdown) breaks display and may prevent the question box from parsing correctly.
- **Forum (multi-select):** When the model presents a question "as a regular (a/b/c) one," Cursor shows single-choice; multi-select appears only when the model "detects the question as multi-choice." So **A. / B. / C.** format is what we want for our single-choice flow.

**Implications:** (1) Use **real newlines** in the agent's reply so the UI does not show literal `\n`. (2) One question per message, with a clear **(a/b/c)** pattern so Cursor shows the click-to-answer UI. (3) Do not wrap the question in a code block or other context that could escape newlines. (4) Keep exactly three options (A, B, C) per question.

## Root causes of "changes failed" (hypotheses)

1. **Formatting bug:** Output is rendered with literal `\n` (e.g. model or markdown escaping), so the question doesn't show as multiple lines and the UI may not parse A/B/C.
2. **Ambiguous format:** Rule says "on separate lines" but the doc example uses one line ("A. yes B. no C. let AI decide"); the agent may output one line and Cursor may not show the question box.
3. **Batching:** Agent might still output more than one question per message, so only the first gets the UI or the UI is confused.
4. **No explicit "only one question" rule:** We say "one question per message" but don't say "Do not include the next question or any other question in this message; wait for the user to answer."

## Changes (second hardening pass)

### 1. Rule: canonical question output format and UI constraints

**File:** [.cursor/rules/context/plan-mode-prompt-crafter.mdc](.cursor/rules/context/plan-mode-prompt-crafter.mdc)

- **Replace or expand the "Cursor Plan mode question UI" bullet** so it is explicit and bug-aware:
  - Cursor Plan mode can show a **question box with click-to-answer (A, B, C)** when you ask **exactly one question per message** and use a format Cursor can parse. To trigger this UI and avoid display bugs: (1) **One question only** — in each message, output only one question and its options; do not include the next question or any other question; wait for the user to answer before sending the next message. (2) **Format:** Put the question text (and any "It does …" line) first, then put each option on **its own line** with a real line break: line 1 = "A. …", line 2 = "B. …", line 3 = "C. …". (3) **Use real newlines** — use actual line breaks in your reply, not the literal characters backslash-n. Do not wrap the question in a code block or other formatting that could cause newlines to render as literal `\n` (Cursor has a known bug that shows `\n` instead of newlines; using plain markdown with real line breaks reduces the risk). (4) Exactly three options (A., B., C.) per question; never D–G.
- **Add a "Question output template" invariant or short block** (either in the rule or in User-Questions-and-Options-Reference §1) so the agent has a single pattern to follow. Example pattern:
  - First line: question text (e.g. "Which kind?" or "Include project_id?").
  - Optional second line: "**It does:** …" when the param needs explanation.
  - Then a blank line (real newline).
  - Then: "**A.** …" on one line, "**B.** …" on the next, "**C.** …" on the next.
  - Nothing else in the message: no second question, no "Next I'll ask…", and no bracketed or preamble commentary (e.g. "[Param 2 of 18.]" or "Next: project_id") in the same message — only the one question and its A/B/C options (plus optional "It does …" line).

### 2. User-Questions-and-Options-Reference §1: output format and template

**File:** [3-Resources/Second-Brain/User-Questions-and-Options-Reference.md](3-Resources/Second-Brain/User-Questions-and-Options-Reference.md)

- **Add a short "How to format each question (Cursor Plan mode)" subsection** in §1 (after the contract, before "Order of questions"):
  - One question per message. Use **real line breaks** (not literal `\n`). Do not wrap in a code block. Put each option on its own line: first line = question (and optional "It does …"); then a blank line; then "**A.** …", "**B.** …", "**C.** …" on separate lines. This format helps Cursor show the question box with click-to-answer; Cursor has a known bug where `\n` can render literally, so avoid escaping newlines.
- **Optional:** Add a minimal example in §1 showing the exact line-by-line layout for one question (e.g. Q0 or one param question).

### 3. Prompt-Crafter-Structure-Detailed: one question, real newlines, no code block

**File:** [3-Resources/Second-Brain/Second-Brain-User-Flows/Prompt-Crafter-Structure-Detailed.md](3-Resources/Second-Brain/Second-Brain-User-Flows/Prompt-Crafter-Structure-Detailed.md)

- **In "Cursor Plan mode question UI" and the Example:** Change the example so options are on **separate lines** (not "A. yes B. no C. let AI decide" on one line). State explicitly: use **real newlines** between options; do not wrap the question in a code block; one question per message so Cursor shows the question box. Add one sentence: "Cursor has a known bug (literal `\n` instead of newlines); use plain markdown with real line breaks."
- **In Protocol step (4):** Add: "Output exactly one question per message; do not include the next question in the same message; wait for the user to answer before sending the next."

### 4. Ingress note / reference (if present)

**File:** [Ingest/cursor_integration_of_prompt_crafter_in.md](Ingest/cursor_integration_of_prompt_crafter_in.md) (if this file still exists and is referenced)

- Update the "questions box" sentence to: use one question per message, options on separate lines with real newlines, no code block; note the Cursor `\n` bug so the agent avoids escaping newlines.

### 5. Rule: explicit "only one question in this message"

**File:** [.cursor/rules/context/plan-mode-prompt-crafter.mdc](.cursor/rules/context/plan-mode-prompt-crafter.mdc)

- In **step 5 (Ask optionals)** and anywhere we say "one question per message," add an explicit constraint: "In each reply that asks a question, include **only** that one question and its A/B/C options. Do not add the next question, a list of upcoming questions, or any other question in the same message. Wait for the user to answer, then send the next question in a new message."

### 6. Sync and changelog

- **.cursor/sync/rules/context/plan-mode-prompt-crafter.md:** Apply the same wording as in the .mdc rule (question UI bullet and one-question-only constraint).
- **.cursor/sync/changelog.md:** Add an entry: Plan-mode second hardening — question UI format (one question per message; options on separate lines; real newlines; no code block; Cursor `\n` bug workaround); explicit "do not include next question" constraint; User-Questions-and-Options-Reference §1 format subsection; Structure-Detailed example and protocol update.

## What stays from the first pass

- All no-skip invariants, Fail conditions, and step-by-step behavior (load §1 first, Q0-only skip, param order by branch, RESUME-ROADMAP params 2–18, CODE parity, Final always asked, manual text no-skip, etc.) remain in place. This pass **adds** format and UI clarity; it does not remove or relax the no-skip rules.

## Verification

- After edits, a run in Plan mode that asks e.g. "Which kind?" should output that question with A. and B. on **separate lines** with real newlines, and no second question in the same message.
- If the Cursor UI still shows literal `\n`, the cause is likely client-side (Cursor bug); the rule and docs will have instructed the agent to use real newlines and avoid code blocks so that when the bug is fixed, behavior is correct.

## Potholes and additional protections (from codebase search)

These contradict or weaken the second-pass format (options on separate lines, one question only, real newlines, no extra commentary). Address them so the agent has a single, consistent format.

### A. Prompt-Crafter-Examples.md — one-line options and bracketed commentary

- **Every Agent question** in Example 1 and Example 2 shows A, B, C on the **same line** (e.g. "A. I'll specify B. use default / infer C. let AI decide", "Which kind? A. CODE ... B. ROADMAP"). The examples **model the wrong format**; the agent will copy one-line options.
- **Example 2** also has: "**Agent:** [All 18 params for RESUME-ROADMAP are asked in §1 order; no skips.] Next: project_id (param 2). Include project_id? ..." So one message contains **bracketed commentary** plus "Next: ..." plus the question. The second pass forbids "next question" and "Next I'll ask…" — this models exactly that. Same pattern can train the agent to add preamble in every question message.
- **Plan addition:** In [Prompt-Crafter-Examples.md](3-Resources/Second-Brain/Prompt-Crafter-Examples.md), rewrite every Agent question so that (1) options A, B, C appear on **separate lines** (e.g. "**A.** I'll specify" then newline "**B.** use default / infer" then newline "**C.** let AI decide"). (2) Remove or shorten the "[All 18 params...] Next: project_id" style preamble; at most one short bracketed note (e.g. "[Param 2 of 18.]") or no bracket, then only the question and options. Add a one-line note above Example 1 or in the doc intro: "Each question is shown with options on separate lines and no second question or 'Next I'll ask' in the same message; this format helps Cursor show the question box."

### B. Prompt-Crafter-Structure-Detailed — example and protocol show one-line format

- **Example** (line ~80): *"Include research-related options? **It does:** ... A. yes B. no C. let AI decide."* — all on one line in italics. So the doc the rule points to for "format" **contradicts** "on separate lines."
- **Protocol (1)** says: ask "Which kind? A. CODE B. ROADMAP" — one line. So the protocol itself models one-line for Q0.
- **Plan addition:** Already in the plan: change the example to separate lines. Also update the Protocol (1) wording to show that Q0 can be formatted with A and B on separate lines (e.g. "Which kind?" then newline "**A.** CODE ..." then "**B.** ROADMAP") or add a note that "in the UI, put each option on its own line."

### C. User-Questions-and-Options-Reference.md — tables and prose don't specify layout

- The **tables** use pipe format "**A.** CODE ... | **B.** ROADMAP" (markdown table syntax). That's for reference, not the display format. The prose says "one per message" but never says "each option on its own line" or "real newlines."
- **Plan addition:** Already in the plan: add "How to format each question" with separate lines and real newlines. Add one **minimal rendered example** in §1 (e.g. for Q0) showing the exact line-by-line layout so the agent has a copy-paste pattern.

### D. Chat-Prompts.md — inline summary format

- Table cells show "Which kind? A. CODE B. ROADMAP" and "Which action? (A. deepen | B. recal | C. Other)" as inline summary. If the agent uses only Chat-Prompts for format, it might output inline.
- **Plan addition:** In the Plan-mode crafting paragraph or table footnote, add: "Format each question with each option on its own line (real newlines); see User-Questions-and-Options-Reference §1 for the exact layout."

### E. Ingest/cursor_integration_of_prompt_crafter_in.md — one-line and "optional" grouping

- The note says "Ask **one question per message** with explicit 'A. … B. … C. …'" but does **not** say "on separate lines" or "real newlines." So it doesn't reinforce the second pass.
- It also suggests **grouping** ("Research-related options: ... — include any? A. yes (then sub-questions) B. no") which could encourage multi-part or batched questions.
- **Plan addition:** Update the "questions box" sentence to: one question per message, **options on separate lines with real newlines**, no code block; note the Cursor `\n` bug. Add one line: "Do not group multiple params into one question; ask one param per message per §1 order."

### F. Rules.md — no format detail

- Rules.md says "one question per message with A./B./C." but doesn't say "options on separate lines" or "real newlines." So the high-level Rules table doesn't reinforce the format.
- **Plan addition:** In the plan-mode row or the Plan-mode prompt crafting bullet, add: "Format: one question per message, each option on its own line (real newlines); see User-Questions-and-Options-Reference §1."

### G. User-Flow diagrams (Mid-Level, High-Level, Detailed)

- Mermaid node labels use "Which kind? A. CODE B. ROADMAP" as a single string (diagram shorthand). They don't need to show line breaks, but if the agent ever consults only the diagram, it might infer one-line. Low risk; optional note in Structure-Detailed that "diagram labels are abbreviated; actual output uses separate lines per §1."

### H. No "no commentary" rule

- The rule doesn't yet say "do not add bracketed commentary or 'Next I'll ask X' in the same message as the question." So the agent might add "[Param 2 of 18.]" or "Next: project_id" which (a) lengthens the message and (b) could confuse the UI parser.
- **Plan addition:** In the rule "Question output template" or the one-question-only constraint, add: "Do not add commentary such as 'Next I'll ask…' or '[Param 2 of 18]' in the same message; the message must contain only the one question and its A/B/C options (and optional brief 'It does …' line)."

### I. Changelog and legacy plans

- Changelog says "explicit A./B./C. format" and "one question per turn" but not "on separate lines" or "real newlines." Legacy plans (e.g. force_plan-mode_question_alignment) say "on separate lines" but aren't the active rule. No change required for old changelog entries; the **new** changelog entry for the second pass should mention "options on separate lines" and "real newlines."

---

## Summary


| Location                                          | Change                                                                                                                                                                                                  |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| plan-mode-prompt-crafter.mdc                      | Question UI bullet: one question only, options on separate lines, real newlines not `\n`, no code block; no "next question" or commentary in same message; explicit constraint in step 5 and invariant  |
| User-Questions-and-Options-Reference.md §1        | "How to format each question" subsection: real line breaks, no code block, A/B/C on separate lines; **minimal line-by-line example** (e.g. Q0)                                                          |
| Prompt-Crafter-Structure-Detailed.md              | Example with options on **separate lines**; real newlines, no code block; Cursor `\n` bug note; Protocol (1) and (4): one question per message, options on separate lines, wait for answer              |
| Prompt-Crafter-Examples.md                        | **Pothole A:** Rewrite all Agent questions with A/B/C on **separate lines**; remove or shorten "[All 18 params...] Next: ..." preamble; add note that format uses separate lines and no second question |
| Chat-Prompts.md                                   | **Pothole D:** Footnote or sentence: format each question with options on separate lines (real newlines); see §1.                                                                                       |
| Ingest/cursor_integration_of_prompt_crafter_in.md | **Pothole E:** "questions box" sentence: options on separate lines, real newlines, no code block, Cursor bug; do not group multiple params into one question                                            |
| Rules.md                                          | **Pothole F:** Plan-mode row or bullet: add "each option on its own line (real newlines); see User-Questions-and-Options-Reference §1"                                                                  |
| .cursor/sync/*                                    | Sync rule copy + changelog entry (mention "options on separate lines", "real newlines", "no commentary in same message")                                                                                |


