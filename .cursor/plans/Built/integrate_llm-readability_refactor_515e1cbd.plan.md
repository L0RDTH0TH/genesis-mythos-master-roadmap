---
name: Integrate LLM-Readability Refactor
overview: Add a dedicated refactor step to the prompt-crafter-chat-trigger plan and define the User-Questions-and-Options-Reference refactor so the reference file is easier for the LLM to parse and follow when implementing the question-led flow.
todos: []
isProject: false
---

# Integrate LLM-Readability Refactor into Prompt-Crafter Plan

## Objective

Integrate a **refactor step** into the existing plan at [prompt-crafter-chat-trigger_e8c642e6.plan.md](/home/darth/.cursor/plans/prompt-crafter-chat-trigger_e8c642e6.plan.md) so that [User-Questions-and-Options-Reference.md](3-Resources/Second-Brain/User-Questions-and-Options-Reference.md) is restructured for better LLM legibility before or in parallel with the Q&A state machine and trigger implementation.

---

## 1. Changes to the existing plan file

Edit [prompt-crafter-chat-trigger_e8c642e6.plan.md](/home/darth/.cursor/plans/prompt-crafter-chat-trigger_e8c642e6.plan.md) as follows.

### 1.1 Add a new todo

Insert a new todo (recommended after `analyze-docs`, before `design-state-machine`):

- **id:** `refactor-user-questions-reference`
- **content:** Refactor User-Questions-and-Options-Reference §1 for LLM readability: per-branch question sequences (one item per line), option lists instead of pipes in table cells, and optional quick-sequence block; preserve §2–§5 and cross-references.

### 1.2 Add a new section

Insert a new section **"Refactor: User-Questions-and-Options-Reference for LLM readability"** (e.g. after "Safety & invariants", before "Potholes and guards"). Content of the section is the refactor spec below.

---

## 2. Refactor spec (content for the new plan section)

Target file: [3-Resources/Second-Brain/User-Questions-and-Options-Reference.md](3-Resources/Second-Brain/User-Questions-and-Options-Reference.md). Scope: **§1 only** (Question-led Prompt Crafter). Leave §2–§5 and frontmatter/cross-references unchanged.

### 2.1 Per-branch question sequence (one item per line)

Replace the dense single-line "Param order by branch" bullets (lines 67–75) with **one param per line** and an explicit index so the agent can tick off steps.

**Example format for RESUME-ROADMAP:**

```markdown
- **RESUME-ROADMAP** (after "Which action?", ask in this order):
  1. action *(already set by "Which action?" — do not ask again)*
  2. project_id
  3. phase
  4. sectionOrTaskLocator (manual)
  5. enable_context_tracking
  ...
  18. queue_next
```

Apply the same pattern for ROADMAP MODE (setup), CODE → INGEST, CODE → ORGANIZE, CODE → DISTILL, CODE → EXPRESS, CODE → ARCHIVE, CODE → Task modes. Keep `(manual)` or `(manual text)` on the same line as the param name.

### 2.2 Option lists instead of pipes in table cells

In §1, avoid using `|` inside table cells (it clashes with markdown table column separators). For Q0, per-param options, and Final:

- Either list options as **bullets** under the question (e.g. "- **A.** CODE …", "- **B.** ROADMAP …"), or
- Keep a table but put each option on a **separate line within the cell** (line break in the cell), or
- Use a two-column table where the second column is "A / B / C" and a third column or a following list gives the meaning.

Ensure the **exact** option text the agent must output (e.g. "**A.** CODE (pipelines: ingest, organize, …)") appears in a way that is easy to copy or parse, with no ambiguous pipe characters.

### 2.3 Explicit question text for each step (optional but recommended)

For at least one branch (e.g. CODE → INGEST MODE), add a **numbered list of exact questions** so the agent has a single checklist. Example:

```markdown
**CODE → INGEST MODE — question sequence:**
1. **Which pipeline?** *(if not already chosen)* A. INGEST MODE | B. ORGANIZE MODE | C. Other…
2. **What is the source_file?** (manual)
3. **Include context_mode?** A. yes / B. no / C. let AI decide
...
6. **Append to queue?** Y | n
```

If not every branch gets this, at least add it for INGEST and RESUME-ROADMAP (the longest flows). Other branches can keep the one-per-line param list plus the generic "Per-param question" and "Manual text phase" rules.

### 2.4 Optional: Quick-sequence block at top of §1

After "Order of questions", add a short **Quick sequence** block that lists only param names in order per branch (no options), so the agent can verify "ask in this order" at a glance. Example:

```markdown
**Quick sequence (param names only):**
- CODE → INGEST: source_file (manual), context_mode, max_candidates, profile, user_guidance (manual), rationale_style.
- RESUME-ROADMAP: action *(set by Which action?)*, project_id, phase, sectionOrTaskLocator (manual), … queue_next.
```

This is optional; include only if the rest of §1 stays consistent with it.

### 2.5 Preserve contract and formatting rules

Do **not** change:

- The "Question-led contract" (ask every question in order, no skips, Q0 omit only when CODE/ROADMAP said).
- "How to format each question (Chat/Agent)" and the one-question-per-message, real line breaks, A/B/C on separate lines.
- The example (Q0) with options on their own lines.
- Branch logic (CODE vs ROADMAP; ROADMAP MODE vs RESUME-ROADMAP; "Which action?" with deepen/recal/Other).
- §2–§5 and Cross-references.

### 2.6 Sync and docs

After refactoring the reference file:

- Update [.cursor/sync/](.cursor/sync/) if this file is synced there (e.g. no separate sync copy for this doc; confirm in backbone-docs-sync).
- Ensure [Prompt-Crafter-Param-Table](3-Resources/Second-Brain/Prompt-Crafter-Param-Table.md) and [User-Flow-Prompt-Crafter-Detailed](3-Resources/Second-Brain/Second-Brain-User-Flows/User-Flow-Prompt-Crafter-Detailed.md) still align with the refactored order and wording; add a one-line note in the reference if Param Table remains the source for `question_order` and `accepts_manual_text`.

---

## 3. Dependency and order

- **Refactor** can run **before** or **in parallel with** `design-state-machine` and `implement-trigger-and-qna`, since the state machine and rules will read the reference file.
- **analyze-docs** should still run (it covers Param-Table and User-Flow-Prompt-Crafter-Detailed); the refactor step makes the reference file the primary LLM-facing checklist for §1 question order and wording.

---

## 4. Summary


| Action                                                                                   | Location                                                                                                    |
| ---------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Add todo `refactor-user-questions-reference`                                             | Plan frontmatter `todos:`                                                                                   |
| Add section "Refactor: User-Questions-and-Options-Reference for LLM readability"         | Plan body (after Safety & invariants)                                                                       |
| Refactor §1: one param per line, option lists, optional question list and quick-sequence | [User-Questions-and-Options-Reference.md](3-Resources/Second-Brain/User-Questions-and-Options-Reference.md) |
| Leave §2–§5, contract, and formatting rules unchanged                                    | Same file                                                                                                   |


