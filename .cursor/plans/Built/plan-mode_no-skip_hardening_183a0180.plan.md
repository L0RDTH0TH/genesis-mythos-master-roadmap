---
name: Plan-mode no-skip hardening
overview: "Harden the Plan-mode prompt crafter so questions are never skipped: add an explicit no-skip invariant, make the post-mode-narrowing sequence unambiguous (especially RESUME-ROADMAP after \"Which action?\"), and reinforce the contract in the rule, reference doc, and supporting docs."
todos: []
isProject: false
---

# Plan-mode prompt crafter: no-skip hardening pass

## Goal

Ensure the agent **never** skips a question in Plan mode. Every question in [User-Questions-and-Options-Reference.md](3-Resources/Second-Brain/User-Questions-and-Options-Reference.md) §1 for the current branch must be asked, in order. Skipping any question = FAIL.

## Root cause (from prior audit)

The rule already says "Skips a question → FAIL," but the agent still stopped after "Which action?" (deepen) and asked zero param questions. Likely causes: (1) §1 not retained in context so the agent had no explicit "Param order by branch" list; (2) the transition from mode-narrowing to param questions was implicit, so the agent did not treat "then param questions" as mandatory next steps.

## Changes

### 1. Rule: add a top-level "Never skip" invariant and explicit continuation

**File:** [.cursor/rules/context/plan-mode-prompt-crafter.mdc](.cursor/rules/context/plan-mode-prompt-crafter.mdc)

- **After the "Questions source (mandatory)" bullet (around line 11):** Add a dedicated short bullet:
  - **Never skip a question.** For the current branch, you must ask every question §1 specifies (Q0 if needed, mode-narrowing, then every param in "Param order by branch," then manual text for each included text param, then Final). If you skip any of these, the run fails. Do not proceed to summary or queue append until all are asked and answered.
- **In step 4 (Narrow mode):** Add one sentence at the end:
  - Immediately after the last mode-narrowing answer (e.g. after user selects "deepen" for RESUME-ROADMAP), continue with the **next** question in §1: the first param in "Param order by branch" that was not already answered by mode-narrowing (e.g. for RESUME-ROADMAP after "Which action?" that is project_id, then phase, then the rest in §1 order). Do not stop after mode-narrowing.
- **In step 5 (Ask optionals):** Add an explicit reminder:
  - For RESUME-ROADMAP, "Param order by branch" in §1 lists 18 params (1. action … 18. queue_next). Action is already set by "Which action?"; you must still ask for params 2–18 in order (project_id, phase, sectionOrTaskLocator, …). Do not skip any.
- **New invariant** in the Invariants section:
  - **No skips:** You must ask every question in §1 for the current branch, in the order given. Before step 8, mentally verify: kickoff (if needed), mode-narrowing, each param in "Param order by branch" (except any already answered by mode-narrowing), manual text for each included accepts_manual_text param, then Final. If any is missing, FAIL before appending.

No other edits to the rule are required; existing Fail conditions and step 1 (load reference first) stay as-is.

### 2. Reference doc §1: add a contract and explicit RESUME-ROADMAP continuation

**File:** [3-Resources/Second-Brain/User-Questions-and-Options-Reference.md](3-Resources/Second-Brain/User-Questions-and-Options-Reference.md)

- **At the start of §1 (after "When:" and before "Order of questions"):** Add a one-line contract:
  - **Plan-mode contract:** The agent must ask **every** question in this section for the current branch, **in order**. No skips. Skipping any question fails the run.
- **In the ROADMAP bullet (around line 33):** Make the continuation explicit so it cannot be read as "then optionally param questions":
  - Current: "Then param questions in question_order."
  - Replace with: "Then ask **every** param in 'Param order by branch' for RESUME-ROADMAP in order (param 1 = action is already set by 'Which action?'; ask for params 2–18: project_id, phase, sectionOrTaskLocator, …). Do not skip any param question."
- **Optional but recommended:** Add a short "Sequence after mode-narrowing" sub-bullet under "Param order by branch" for RESUME-ROADMAP only: "After 'Which action?', the very next question is project_id (param 2), then phase (3), then the rest in the list order."

### 3. Supporting docs: reinforce §1 as the no-skip source

**File:** [3-Resources/Second-Brain/Second-Brain-User-Flows/Prompt-Crafter-Structure-Detailed.md](3-Resources/Second-Brain/Second-Brain-User-Flows/Prompt-Crafter-Structure-Detailed.md)

- In the **Funnel** paragraph (around line 25): After "then asks optionals in **param table order**", add: "The agent must not skip any question; the authoritative order and list are in User-Questions-and-Options-Reference §1 'Param order by branch'."
- In **Protocol (sequence)** step (4): Add: "Do not skip any optional; follow §1 Param order by branch for the current branch."

**File:** [3-Resources/Second-Brain/Prompt-Crafter-Param-Table.md](3-Resources/Second-Brain/Prompt-Crafter-Param-Table.md)

- In the intro (around line 12): After "Canonical question text and option wording for Plan-mode are in … §1", add: "The agent must ask every param in §1 'Param order by branch' for the chosen branch; no skips."

**File:** [3-Resources/Second-Brain/Chat-Prompts.md](3-Resources/Second-Brain/Chat-Prompts.md)

- For the ROADMAP row: Add that after setup vs resume the agent asks "Which action?" (if RESUME-ROADMAP), then **all** param optionals in §1 order with no skips, then manual text, then "Append to queue?".

### 4. Fix Prompt-Crafter-Examples.md (pothole A)

**File:** [3-Resources/Second-Brain/Prompt-Crafter-Examples.md](3-Resources/Second-Brain/Prompt-Crafter-Examples.md)

- **Example 2, "Which action?" line:** Replace the A–G list with exactly three options per §1: **A.** deepen | **B.** recal | **C.** Other (revert-phase, sync-outputs, handoff-audit, expand, advance-phase, etc. — if C, ask again with A/B/C).
- **Example 2, after "User: A." (deepen):** Insert the missing param questions in §1 order. After "Which action? A." the next line must be the agent asking **project_id** (param 2), then **phase** (param 3); then show at least one or two more (e.g. sectionOrTaskLocator, enable_context_tracking) before enable_research. Add a bracketed note: "[All 18 params for RESUME-ROADMAP are asked in §1 order; no skips.]"

### 5. Rule and reference: potholes B–J (explicit wording)

**Rule** ([plan-mode-prompt-crafter.mdc](.cursor/rules/context/plan-mode-prompt-crafter.mdc)): Add or fold in:

- **B.** One line: every param in §1 must be **asked**; "optional" = param inclusion (A/B/C), not "skip the question".
- **C.** Step 5 or separate bullet: same no-skip for CODE (every param for chosen sub-mode in order); do not skip the C (Other) follow-up for CODE pipeline choice.
- **D.** In Order invariant or Fail: only Q0 may be skipped when kickoff is explicit; all other questions must be asked.
- **F.** Invariant or Fail: always ask the Final question ("Append to queue?"); skipping it = FAIL.
- **G.** Step 7: for every param that (a) was included and (b) accepts_manual_text true, ask "What is the [param name]?" in §1 order; skip = FAIL.
- **H.** For ROADMAP MODE (setup): ask both project_id and source_file in order; do not skip.
- **J.** Step 5/6: ask every param (A/B/C); resolve C only **after** all are asked; do not skip asking and assume C.

**Reference §1** ([User-Questions-and-Options-Reference.md](3-Resources/Second-Brain/User-Questions-and-Options-Reference.md)): Add to contract or nearby:

- **B.** "Optional" refers to whether the user includes the param (A/B/C); every param in "Param order by branch" must still be **asked**.
- **D.** Only Q0 may be omitted when user already said CODE or ROADMAP; all other questions must be asked.
- **H.** ROADMAP MODE (setup): ask both project_id and source_file; "few" does not mean skip.

**Structure-Detailed** ([Prompt-Crafter-Structure-Detailed.md](3-Resources/Second-Brain/Second-Brain-User-Flows/Prompt-Crafter-Structure-Detailed.md)):

- **E.** In Protocol: step (3) "Show current param block" is not a substitute for asking; step (4) must ask every param in §1 order; do not skip any question.

**Param-Table** ([Prompt-Crafter-Param-Table.md](3-Resources/Second-Brain/Prompt-Crafter-Param-Table.md)):

- **I.** Add: question order for Plan-mode is defined **only** in §1 "Param order by branch"; if this table diverges, §1 wins; do not skip any param in that list.

### 6. Sync and changelog

- **File:** [.cursor/sync/rules/context/plan-mode-prompt-crafter.md](.cursor/sync/rules/context/plan-mode-prompt-crafter.md)  
Apply the same wording changes as in the .mdc rule so the sync copy matches.
- **File:** [.cursor/sync/changelog.md](.cursor/sync/changelog.md)  
Add one entry at the top: date 2026-03-10; scope plan-mode-prompt-crafter, User-Questions-and-Options-Reference, Prompt-Crafter-Structure-Detailed, Prompt-Crafter-Param-Table, Prompt-Crafter-Examples, Chat-Prompts, sync; short description: "Plan-mode no-skip hardening: never skip questions; explicit invariant and post-mode-narrowing continuation; Q0-only conditional skip; optional=param not question; CODE parity and C follow-up; Final always asked; manual-text and ROADMAP-setup no-skip; §1 order wins; fix Examples (three options, no modeled skipping); contract and supporting docs updated."

## Verification

- After edits, a run in Plan mode with "We are making a ROADMAP prompt" → RESUME-ROADMAP → deepen must ask the next question (project_id) and then phase, sectionOrTaskLocator, etc., in order, with no skips.
- If the agent skips, the Fail condition and the new invariant require it to report "Plan-mode failed: skipped a required question" and stop (no queue append).
- "Which action?" must always show exactly three options (A. deepen | B. recal | C. Other); never A–G. Prompt-Crafter-Examples Example 2 must match this and must not model skipping params 2–5.

## Potholes and additional protections (from codebase search)

These items were identified as sources of ambiguity or bad examples that could cause the agent to skip questions or use wrong options. Address them in the hardening pass.

### A. Prompt-Crafter-Examples.md — wrong options and modeled skipping

- **Example 2** currently shows "Which action?" with **A–G** (seven options: deepen, recal, revert-phase, D, E, F, G). §1 and the rule require **exactly three options** (A. deepen | B. recal | C. Other). The example contradicts the rule and would train the agent to present D–G.
- **Example 2** also **models skipping**: after "Which action? A." it jumps to "Include enable_research?" and later "Include profile?" and "Include research_queries?", omitting project_id, phase, sectionOrTaskLocator, enable_context_tracking (params 2–5). An agent copying the example would skip those questions.
- **Plan addition:** In [Prompt-Crafter-Examples.md](3-Resources/Second-Brain/Prompt-Crafter-Examples.md), fix Example 2: (1) "Which action?" must show exactly **A.** deepen | **B.** recal | **C.** Other (with "if C, ask again with A/B/C"). (2) After "Which action? A.", show the agent asking **project_id** (param 2), then **phase** (param 3), then at least one or two more in order (e.g. sectionOrTaskLocator, enable_context_tracking) before enable_research; add a bracketed note that all 18 params are asked in §1 order with no skips.

### B. "Optional" / "optionals" ambiguity

- Docs say "ask optionals", "few optionals", "minimal optionals". The word can be read as "optional to ask" (can skip).
- **Clarification:** "Optional" means the *parameter* is optional to include (user answers A/B/C); it does **not** mean the *question* can be skipped. Every param in §1 "Param order by branch" for the current branch must be **asked** (one question per message).
- **Plan addition:** In the rule (and optionally in §1), add one line: "Every param in §1 'Param order by branch' must be **asked**; 'optional' refers to whether the user includes the param (A/B/C), not to skipping the question."

### C. CODE branch parity and C (Other) follow-up

- The plan focuses on RESUME-ROADMAP; CODE branches (INGEST, ORGANIZE, DISTILL, etc.) must have the same no-skip behavior.
- **CODE:** After mode-narrowing (e.g. "INGEST MODE"), ask **every** param in §1 "Param order by branch" for that sub-mode (e.g. INGEST = 6 params in order). Do not skip.
- **CODE → C (Other):** §1 says if user picks C (Other) for pipeline/task mode, "ask a follow-up with exactly A/B/C". The agent must not skip this follow-up or assume a default; ask the follow-up question.
- **Plan addition:** In the rule step 5 (or a separate bullet), state explicitly: "Same no-skip for CODE: after mode-narrowing (e.g. INGEST MODE, or the follow-up if user chose C (Other)), ask every param in §1 for that sub-mode in order (e.g. INGEST = 6 params). Do not skip the C (Other) follow-up."

### D. Q0 = only conditional skip

- The **only** question that may be omitted is **Q0** ("Which kind?") when the user has already said CODE or ROADMAP. All other questions must be asked.
- **Plan addition:** In the rule or §1 contract, state explicitly: "The only question that may be skipped is Q0 when kickoff is already explicit (user said CODE or ROADMAP). All other questions — mode-narrowing, every param in 'Param order by branch', manual text for each included accepts_manual_text param, and the Final 'Append to queue?' — must be asked."

### E. Protocol step (3) "Show current param block"

- [Prompt-Crafter-Structure-Detailed.md](3-Resources/Second-Brain/Second-Brain-User-Flows/Prompt-Crafter-Structure-Detailed.md) Protocol says "(3) Show current param block. (4) Ask optionals…". Step 3 could be read as "display a block and skip asking" or "summarize instead of asking".
- **Plan addition:** In Structure-Detailed Protocol, clarify: "Step (3) is not a substitute for asking. Every param in §1 for the current branch is still asked one per message in step (4); do not skip step (4) or any question."

### F. Final "Append to queue?" always asked

- The Final question must **always** be asked after summary; it is not optional.
- **Plan addition:** In the rule Invariants (or Fail conditions), add: "Always ask the Final question ('Append to queue?' Y | n) after presenting the summary; do not append without asking. Skipping the Final question = FAIL."

### G. Manual text phase — ask for every included text param

- When there are params where (a) user chose to include (A or C resolved to include) and (b) accepts_manual_text is true, the agent must ask "What is the [param name]?" for **each** such param, in §1 order. When zero params qualify, the manual text phase has zero questions (correct).
- **Plan addition:** In the rule step 7 (manual text phase), add: "For every param that (a) was included and (b) has accepts_manual_text true, ask exactly one 'What is the [param name]?' in §1 order. Do not skip any of these; if you skip one, FAIL."

### H. ROADMAP MODE (setup) — both params asked

- ROADMAP MODE (setup) has only 2 params: project_id, source_file. "Few" must not mean "skip"; ask **both** in order.
- **Plan addition:** In the rule or §1, state: "For ROADMAP MODE (setup), ask both params in §1 order: project_id, then source_file (manual text). Do not skip because there are only two."

### I. §1 order wins over Param-Table

- If Param-Table and §1 "Param order by branch" ever diverge, §1 is authoritative for Plan-mode.
- **Plan addition:** In [Prompt-Crafter-Param-Table.md](3-Resources/Second-Brain/Prompt-Crafter-Param-Table.md), add: "For Plan-mode, the **order** in which questions are asked is defined **only** in User-Questions-and-Options-Reference §1 'Param order by branch'. This table matches that order; if it diverges, §1 wins. Do not skip any param in that list."

### J. Resolve C only after asking

- The agent must **ask** every param (with A/B/C options); for any where user chose C, **resolve** after the loop. Do not skip asking and assume C for all.
- **Plan addition:** In the rule step 5 or 6, add: "You must **ask** each param question (with A/B/C); only after all are asked do you resolve C choices. Do not skip asking a param and default it to C."

---

## Summary


| Location                                   | Change                                                                                                                                                                                                                      |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| plan-mode-prompt-crafter.mdc               | "Never skip" bullet; step 4 continuation; step 5 RESUME-ROADMAP + CODE parity + C follow-up; step 6 resolve-C-after-ask; step 7 manual-text no-skip; Final always asked; Q0-only conditional skip; new "No skips" invariant |
| User-Questions-and-Options-Reference.md §1 | Plan-mode contract; "optional" = param not question; Q0 only skip when kickoff explicit; ROADMAP explicit continuation; ROADMAP MODE both params; optional sequence reminder                                                |
| Prompt-Crafter-Structure-Detailed.md       | Funnel + Protocol: §1 authoritative, no skips; step (3) not a substitute for step (4); do not skip any question                                                                                                             |
| Prompt-Crafter-Param-Table.md              | Intro: ask every param §1 order, no skips; §1 order wins if table diverges                                                                                                                                                  |
| Prompt-Crafter-Examples.md                 | Example 2: exactly three options for "Which action?"; show project_id, phase (and note all 18 in order); no modeled skipping                                                                                                |
| Chat-Prompts.md                            | ROADMAP row: Which action? then all optionals §1 order, no skips                                                                                                                                                            |
| .cursor/sync/*                             | Sync rule copy + changelog entry                                                                                                                                                                                            |


