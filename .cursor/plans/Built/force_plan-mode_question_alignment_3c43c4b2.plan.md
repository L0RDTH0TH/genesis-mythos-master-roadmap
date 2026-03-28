---
name: Force Plan-mode question alignment
overview: Inline the canonical Plan-mode question and option text from User-Questions-and-Options-Reference §1 into the plan-mode-prompt-crafter rule so the planning agent always has the exact wording in context, eliminating reliance on reading a separate file.
todos: []
isProject: false
---

# Force alignment with specific questions (Plan-mode)

## Problem

The planning agent is told to use "exact" question text from [User-Questions-and-Options-Reference](3-Resources/Second-Brain/User-Questions-and-Options-Reference.md) §1, but that content lives only in a separate file. The rule does not inline it. In Plan mode the agent often does not read that file (or cannot), so it invents wording from param names and alignment fails.

## Approach: Inline canonical wording in the rule

Put the exact strings the user must see into the rule itself so they are always in the same context as the behavior steps. No dependency on the agent reading another file. The reference doc remains the human-facing source of truth; the rule gets a **canonical wording** block that must be kept in sync when §1 is updated.

## Changes

### 1. Add a "Canonical wording (Plan-mode §1)" block to the rule

**File:** [.cursor/rules/context/plan-mode-prompt-crafter.mdc](.cursor/rules/context/plan-mode-prompt-crafter.mdc)

Insert a new section after the **Invariants** block (or before **Behavior**), containing the exact text from [User-Questions-and-Options-Reference](3-Resources/Second-Brain/User-Questions-and-Options-Reference.md) §1:

- **Q0 (kickoff):**  
Question: "Which kind?"  
Options: **A.** CODE (pipelines: ingest, organize, distill, express, archive, task modes) | **B.** ROADMAP (setup or resume roadmap)
- **Mode-narrowing (CODE):**  
"Which pipeline or task mode?" with options from Queue-Alias-Table (INGEST MODE, ORGANIZE MODE, DISTILL MODE, EXPRESS MODE, ARCHIVE MODE, or task modes).
- **Mode-narrowing (ROADMAP):**  
"ROADMAP MODE vs RESUME-ROADMAP". If RESUME-ROADMAP: "Which action?" (deepen, recal, revert-phase, sync-outputs, handoff-audit, resume-from-last-safe, expand, advance-phase, compact-depth, etc.).
- **Per-param options (standard):**  
**A.** yes / include (or first concrete option) | **B.** no / exclude (or second option) | **C.** let AI decide.  
Each question: one per message, with "It does …" for the param; format as explicit **A. … B. … C. …** on separate lines.
- **Manual text phase:**  
For each included param with `accepts_manual_text: true`: "What is the [param name]?" (replace [param name] with the param, e.g. source_file, user_guidance, sectionOrTaskLocator).
- **Final:**  
"Append to queue?" Options: **Y** | **n**

Param **order** stays from [Prompt-Crafter-Param-Table](3-Resources/Second-Brain/Prompt-Crafter-Param-Table.md) (question_order); the rule already instructs to read that. No need to duplicate the full param list in the rule.

### 2. Point behavior steps at the canonical block

In the same file, update steps 3–5 and 7–8 so they explicitly reference the in-rule block:

- **Step 3:** Change "Read [User-Questions-and-Options-Reference] §1" to: "Use **only** the question and option text from the **Canonical wording (Plan-mode §1)** block in this rule. Do not invent wording from param names."
- **Steps 4, 5, 7, 8:** Replace "per User-Questions-and-Options-Reference §1" / "from the reference §1" with "from the **Canonical wording** block in this rule" (or equivalent). Keep the link to the reference doc in the header for maintainability.

This makes it unambiguous that the agent must use the text that is now in-context (the block) rather than a separate file.

### 3. Add a sync note in the rule

In the rule, add one line near the canonical block or in the reference bullet: "When [User-Questions-and-Options-Reference](3-Resources/Second-Brain/User-Questions-and-Options-Reference.md) §1 is updated, update this canonical block to match."

### 4. Backbone sync (per [backbone-docs-sync](.cursor/rules/always/backbone-docs-sync.mdc))

- **Sync folder:** Update [.cursor/sync/rules/context/plan-mode-prompt-crafter.md](.cursor/sync/rules/context/plan-mode-prompt-crafter.md) with the same content as the edited .mdc (copy or convert).
- **Changelog:** Append an entry to [.cursor/sync/changelog.md](.cursor/sync/changelog.md): rule name `plan-mode-prompt-crafter`, date, one-line summary: "Inline canonical Plan-mode §1 question/option text into rule to force alignment; planning agent no longer depends on reading User-Questions-and-Options-Reference."
- **Docs:** No change to Rules.md table required unless you want to add a short note that Plan-mode wording is now in-rule; optional.

## Optional: Explicit "read if available" fallback

If you want the agent to still try to read the reference when possible (e.g. in non–Plan-mode chat), keep step 3 as: "Use the **Canonical wording** block in this rule. If you have read [User-Questions-and-Options-Reference] §1, prefer that section for any wording not covered in the block." That preserves a single source of truth in the reference while guaranteeing the rule is self-sufficient.

## Outcome

- The planning agent always has the exact Q0, mode-narrowing, per-param format, manual-text template, and final question in the same context as the steps.
- No reliance on Plan mode reading a separate file; alignment is forced by in-context text.
- User-Questions-and-Options-Reference.md remains the human and doc source of truth; the rule’s block is the agent-facing copy and must be kept in sync when §1 changes.

