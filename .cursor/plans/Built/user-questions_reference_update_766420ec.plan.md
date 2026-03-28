---
name: User-Questions Reference Update
overview: "Update User-Questions-and-Options-Reference.md §1 and plan-mode-prompt-crafter with new A/B/C semantics, Quick mapping table, Messages 1–9 block, C choice behavior (reasoning → payload.user_guidance or equivalent), and compensations. Optional polish after first ship. Safety net before save: grep B/no/false, dry-run flows."
todos: []
isProject: false
---

# Update User-Questions-and-Options-Reference for explanatory prompt-crafter flow

## Goal

Adopt the new, more explanatory Cursor chat prompt-crafter flow while keeping:

- The same logical order and question IDs so macros, templates, queue parsing, and downstream rules stay compatible
- One question per agent message (clickable A/B/C boxes)
- Deterministic mapping from choices to queue payload keys

Each question will: explain **what** the parameter does, state the **default** when omitted, give **recommended ranges** where sensible, and use: **A** = explicit value, **B** = default (omit key), **C** = AI reasoning (omit key + append reasoning to payload).

---

## 1. Minimal diff order (build sequence)

### 1.1 User-Questions-and-Options-Reference.md

1. **Replace old §1 bullets** with new semantics + **Quick mapping table** (A = explicit key = chosen value; B = omit key; C = omit key + append short reasoning to payload).
2. **Add “Boolean params” clarification paragraph**: A = add param with chosen value; B and C = omit key — do not set explicit false on B or C; downstream treats absent = default (usually enabled).
3. **Replace old “Question sequence — explicit wording”** with the **full Messages 1–9 block** (Welcome/mode → Pipeline → context_mode → max_candidates → rationale_style → distill_lens optional → source_file → user_guidance → Final A/B/C: yes append | no cancel | AI double-check).
4. **Add “C choice behavior” subsection**: (a) When user picks C, limit reasoning to **1–3 sentences max**; (b) reasoning **appended to payload.user_guidance or equivalent** (e.g. queue entry `prompt` or `params.user_guidance`) so pipelines receive it.
5. **Add note**: “Param order by branch for CODE→INGEST now matches this message sequence (pipeline first, then context_mode, …, user_guidance last). distill_lens added as optional conditional question.”
6. **If Final is now A/B/C**: Add **bold callout**: “**Final confirmation question updated 2026-03-12 — see Message 9.**”

### 1.2 plan-mode-prompt-crafter.mdc (and sync copy)

1. **Add constraint**: “When user chooses C, limit your reasoning to **3–5 sentences max**. Append that exact text to the queue entry’s **user_guidance** field (or **prompt** if no separate field).”
2. **Replace old A/B/C mapping** with: **A** = include explicit key = chosen value; **B** = omit key (Config/MCP default); **C** = omit key + append short reasoning (1–3 sentences) to user_guidance.
3. **For booleans**: “Do not set explicit false on B or C — omit the key instead. Downstream treats absent = default (usually enabled).”
4. **Step 8 (payload assembly)**: Ensure **user_guidance merge happens after all C choices** before writing the queue line.
5. **Sync**: Update `.cursor/sync/rules/context/plan-mode-prompt-crafter.md` to match.

---

## 2. Compensations (quick search & replace)


| File                                 | Change                                                                                                                                   |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Prompt-Crafter-Structure-Detailed.md | Replace “user picks B for that toggle” → “unless payload explicitly sets enable_context_tracking: false”                                 |
| Prompt-Crafter-Examples.md           | Update old “A yes B no C let AI decide” examples to new style                                                                            |
| Parameters.md, Queue-Sources.md      | Add one line near defaults: “Crafted payloads may omit keys (B or C choice); consumers treat absent as default per Second-Brain-Config.” |
| auto-eat-queue.mdc                   | In validation step: “Validate **merged** params (entry + Config + defaults), not only raw entry keys.”                                   |
| Chat-Prompts.md, Rules.md            | Search “Y/n” or “Append to queue?” → replace with pointer to §1 Message 9                                                                |


---

## 3. Optional polish (do after first ship if time tight)

- Add “Recommended ranges” column or inline to Param descriptors in §1.
- Update Prompt-Crafter-Param-Table.md CODE→INGEST question_order to match new sequence.
- Add short **ROADMAP mirror** note in §1: “ROADMAP side uses identical A/B/C semantics and explanatory style; ask params in existing param order with wording patterned on CODE flow.”

---

## 4. Safety net before save (pre-commit checklist)

1. **Grep** vault for “B” near “no” or “false” in prompt-crafter / examples / rules → ensure nothing assumes **B = explicit false**. Fix or document.
2. **Dry-run CODE→INGEST (C on context_mode)**: User picks C → agent appends reasoning → queue entry has no context_mode key but has user_guidance → EAT-QUEUE merges default + guidance → pipeline sees strict-para + reasoning. Should work.
3. **Dry-run boolean (C on enable_research)**: Omit key + append reasoning → downstream sees default + reasoning. No explicit false; correct.

---

## 5. Reference doc §1 (expanded detail — §1 minimal diff is source of truth)

### 5.1 Option semantics and payload mapping

- **Replace** the current "Per-param question" and "Payload mapping (A/B/C → params)" bullets (lines 63–69) with the new contract:
  - **A** = explicit key = chosen value (user picks concrete option)
  - **B** = key omitted → Config / MCP default
  - **C** = key omitted + append short reasoning to `user_guidance` (1–3 sentences max)
- **Add** the **Quick mapping table** (as provided):

  | User choice | Queue payload effect               | user_guidance append? |
  | ----------- | ---------------------------------- | --------------------- |
  | **A**       | explicit key = chosen value        | no                    |
  | **B**       | key omitted → Config / MCP default | no                    |
  | **C**       | key omitted → default              | yes (short reasoning) |

- **Clarify** for boolean params (e.g. `enable_research`): **A** = add to `params` with the chosen value (e.g. `true`); **B** and **C** = omit key (downstream uses default); **C** additionally appends reasoning to `user_guidance`. This preserves queue/processor behavior while matching the new semantics.

### 5.2 Question format and explanatory style

- In **"How to format each question"** and the **Question output template** (invariants):
  - Require that each question: explains **what** the parameter does, states the **default** when omitted, and gives **recommended ranges / values** where sensible (per Param descriptors).
  - Keep: one question per message; real newlines; A/B/C on separate lines; no code block wrapping.
- Extend the **Question output template** so the optional second line can include default and recommended range (e.g. "Default (when omitted) = strict-para." / "Recommended safe range: 3–10.").

### 5.3 Revised question sequence — explicit wording (CODE side)

- **Replace** the current "Question sequence — explicit wording (CODE → INGEST, RESUME-ROADMAP)" subsection (lines 139–156) with the new **Revised Question Sequence – Explicit Wording** as the drop-in replacement for the CODE side:
  - **Message 1 – Welcome / mode choice**: Welcome text + "Which side would you like to configure first?" with **A.** CODE side, **B.** ROADMAP side, **C.** AI reasoning (agent gives 1–2 sentence reasoning, picks A or B, then continues). Use exact wording from the user’s Message 1.
  - **Message 2 – Pipeline**: "Which pipeline do you want to run?" **A.** INGEST MODE (description), **B.** default (usually INGEST if just captured), **C.** AI reasoning (suggest best pipeline + why).
  - **Message 3 – context_mode**: Explain strict vs loose; default = strict-para. **A.** strict-para, **B.** default, **C.** AI reasoning.
  - **Message 4 – max_candidates**: Explain; recommended 3–10; default = 7. **A.** 7 (balanced), **B.** default (7), **C.** AI reasoning.
  - **Message 5 – rationale_style**: Options and default = concise. **A.** concise, **B.** default, **C.** AI reasoning.
  - **Message 6 – distill_lens / highlight_perspective** (optional/conditional): **A.** yes — ask for lens, **B.** no / default, **C.** AI reasoning. If A, next message asks for the actual lens string.
  - **Message 7 – source_file / batch**: **A.** yes — paths/folder/glob, **B.** default (Ingest/ or recently captured), **C.** AI reasoning.
  - **Message 8 – user_guidance**: **A.** yes — user pastes, **B.** no / skip, **C.** AI reasoning (propose starter guidance).
  - **Message 9 – Final confirmation**: Summary of payload then **A.** yes — append to queue, **B.** no — cancel / edit, **C.** AI reasoning — double-check if anything looks off. On **A**: craft queue line, append to `prompt-queue.jsonl`, reply "Queued. Run EAT-QUEUE when ready."
- **Preserve** the existing **Param order by branch** (and question IDs) so queue and rule logic still match. Add a short note that the "explicit wording" sequence above is the recommended message order and text for CODE → INGEST; param order in "Param order by branch" remains canonical for payload assembly. If the new message order differs from the current CODE→INGEST param list (e.g. pipeline first, then context_mode, max_candidates, rationale_style, optional distill_lens, source_file, user_guidance), either:
  - **Option A**: Update "Param order by branch" for CODE → INGEST to match the new sequence (and add optional distill_lens), and keep **profile** in the list with an explanatory question in §1 and in Param descriptors; or
  - **Option B**: Keep current param order in "Param order by branch" and document that the explicit wording is one recommended flow; agents ask in §1 order (Param order by branch) but use the new wording and A/B/C semantics for each param.
- **Recommendation**: Option A — align Param order by branch with the new sequence and add optional **distill_lens**; add **profile** to the explicit sequence with one line of explanatory wording so it is not dropped.

### 5.4 Final question (Append to queue?)

- Either keep **"Append to queue? Y · n"** as the canonical Final question (simplest for existing rules) or switch to the new **A/B/C** Final (A = append, B = cancel, C = AI double-check). If switching to A/B/C, document: on **A** → append; on **B** → no write; on **C** → agent performs 1–3 sentence sanity check, then either suggests edits (no append) or confirms and appends. Rule and other docs that reference "Append to queue? Y/n" would then reference the new Final wording from §1.

### 5.5 C choice behavior and implementation notes

- **Add** an "Implementation notes" or "C choice behavior" subsection under §1:
  - When the user picks **C**, the agent must limit reasoning to **1–3 sentences max** and append that to `user_guidance` (or to the payload’s guidance field used by the pipeline).
  - Keep the same question IDs / order numbers internally for reference in macros and rules.
- **Param descriptors**: Ensure "Param descriptors (for agents and param_meta overlay)" tables already include "It does" and "Default when C / omitted"; add **Recommended ranges** column or sentence where sensible (e.g. max_candidates: "3–10; above 10 often wastes time").

---

## 2. ROADMAP side mirror

- **Document** in §1 that for the **ROADMAP side** the structure is mirrored: same A/B/C semantics, same explanatory style (what it does, default, recommended ranges), same one-question-per-message and Final confirmation pattern.
- **Keep** the existing "Param order by branch" for ROADMAP MODE (setup) and RESUME-ROADMAP unchanged for compatibility; add a short "ROADMAP – explicit wording" note or subsection that points to the same message pattern (welcome if needed, then mode/action, then each param in order with the new wording and A/B/C). Full drop-in wording for every ROADMAP param can be a follow-up; the plan only requires documenting the mirror and keeping param order.

---

## 3. Prompt-crafter rule update

- In [.cursor/rules/context/plan-mode-prompt-crafter.mdc](.cursor/rules/context/plan-mode-prompt-crafter.mdc):
  - **Add** an explicit constraint: when the user chooses **C** (AI reasoning), the agent must limit the reasoning to **1–3 sentences** and, when applicable, append that reasoning to `user_guidance` (or the payload field used for guidance).
  - **Update** the "Payload mapping" description in **Step 8** (and any inline A/B/C description) to match the new semantics: **A** = explicit key = value, **B** = omit key (default), **C** = omit key + append short reasoning to user_guidance. Adjust boolean handling so **B** and **C** both omit the key (no longer "B → false" for include params); downstream continues to use Config/MCP default when key is absent.
  - **Optionally** reference the new "Quick mapping table" in User-Questions-and-Options-Reference §1 for the authoritative mapping.

---

## 4. Sync and docs

- **Sync**: Update [.cursor/sync/rules/context/plan-mode-prompt-crafter.md](.cursor/sync/rules/context/plan-mode-prompt-crafter.md) to match the prompt-crafter rule changes (per backbone-docs-sync).
- **Backbone**: In [Rules.md](3-Resources/Second-Brain/Rules.md) (and [Prompt-Crafter-Structure-Detailed](3-Resources/Second-Brain/Second-Brain-User-Flows/Prompt-Crafter-Structure-Detailed.md) if it describes A/B/C), update the brief description of Plan-mode prompt crafting to state the new option semantics (A = explicit, B = default, C = AI reasoning + user_guidance) and the 1–3 sentence cap for C. No need to rewrite full flows; a short pointer to User-Questions-and-Options-Reference §1 is enough.

---

## 5. Optional: Prompt-Crafter-Param-Table and param order

- If **Param order by branch** for CODE → INGEST is changed to match the new message sequence (Message 2–8), update [Prompt-Crafter-Param-Table.md](3-Resources/Second-Brain/Prompt-Crafter-Param-Table.md) CODE → INGEST table so **question_order** matches (pipeline/mode, then context_mode, max_candidates, rationale_style, optional distill_lens, source_file, user_guidance; and profile if kept). If **profile** remains in the list, assign it an order and ensure one explanatory question exists in §1.

---

## Summary of files to touch


| File                                                                                                                          | Action                                                                                                                                                                                           |
| ----------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [User-Questions-and-Options-Reference.md](3-Resources/Second-Brain/User-Questions-and-Options-Reference.md)                   | Revise §1: new A/B/C semantics, quick mapping table, explanatory style, Revised Question Sequence (Messages 1–9), C reasoning cap, implementation notes; optional Param order and ROADMAP mirror |
| [plan-mode-prompt-crafter.mdc](.cursor/rules/context/plan-mode-prompt-crafter.mdc)                                            | Add 1–3 sentence cap for C; update payload mapping to new A/B/C semantics; require C reasoning in payload (e.g. prompt)                                                                          |
| .cursor/sync/rules/context/plan-mode-prompt-crafter.md                                                                        | Sync with rule changes                                                                                                                                                                           |
| [Rules.md](3-Resources/Second-Brain/Rules.md)                                                                                 | Short update to Plan-mode crafting: new semantics + C cap; if Final becomes A/B/C, reference §1                                                                                                  |
| [Prompt-Crafter-Param-Table.md](3-Resources/Second-Brain/Prompt-Crafter-Param-Table.md)                                       | Optional: align CODE→INGEST question_order with new sequence                                                                                                                                     |
| [Parameters.md](3-Resources/Second-Brain/Parameters.md), [Queue-Sources.md](3-Resources/Second-Brain/Queue-Sources.md)        | One sentence: absent = default; crafted payloads may omit keys                                                                                                                                   |
| [Prompt-Crafter-Structure-Detailed.md](3-Resources/Second-Brain/Second-Brain-User-Flows/Prompt-Crafter-Structure-Detailed.md) | Update enable_research example; “user picks B” → “payload explicitly sets enable_context_tracking: false”                                                                                        |
| [Prompt-Crafter-Examples.md](3-Resources/Second-Brain/Prompt-Crafter-Examples.md)                                             | Align examples with new A/B/C semantics and explanatory style                                                                                                                                    |
| [auto-eat-queue.mdc](.cursor/rules/context/auto-eat-queue.mdc)                                                                | Clarify that validation applies to merged params (entry + Config + defaults)                                                                                                                     |
| [Chat-Prompts.md](3-Resources/Second-Brain/Chat-Prompts.md)                                                                   | If Final becomes A/B/C, reference §1 for Final question wording                                                                                                                                  |


---

## 6. Codebase check: compensations and failure shields

Areas that must compensate for the new A/B/C semantics and where to add shields so the change does not cause silent failures or broken behavior.

### 6.1 Downstream param consumption (omit = default)

- **Current**: Rule and Queue-Sources say for booleans A → true, B → false, C → omit. **New**: A → explicit value, B → omit, C → omit + user_guidance.
- **Impact**: Consumers already treat **absent** as “use default” (Parameters.md, Queue-Sources.md, auto-roadmap.mdc). So B and C both yielding **omit** is compatible.
- **Shield**: In [Parameters.md](3-Resources/Second-Brain/Parameters.md) and [Queue-Sources.md](3-Resources/Second-Brain/Queue-Sources.md), add one sentence: “Crafted payloads may omit optional params (B or C); consumers must treat absent keys as default per Param descriptors. Only explicit values in the payload override Config/MCP defaults.”
- **Boolean “explicit false”**: For `enable_context_tracking`, `enable_research`, `queue_next`, downstream uses “only explicit false disables” / “absent = default”. With the new flow, **B** and **C** no longer emit `false`; they omit. So users who previously chose “B. no” for e.g. research get **default** (auto-detect) instead of **off**. Document this in §1: for booleans where “explicit off” matters, either (a) add a separate “Turn off for this run? A. yes B. no” for that param, or (b) state that “explicit false” is only via manual queue edit or a future override. [Prompt-Crafter-Structure-Detailed.md](3-Resources/Second-Brain/Second-Brain-User-Flows/Prompt-Crafter-Structure-Detailed.md) line 160 says “effective context-tracking remains default-on unless user picks B” — **update** to: “unless the payload explicitly sets `enable_context_tracking: false`” (no longer “user picks B”), since B now means omit/default.

### 6.2 C reasoning: where it must land (payload, not only chat)

- **Risk**: If C reasoning is only said in chat and not written into the queue entry, pipelines never see it.
- **Shield**: In User-Questions-and-Options-Reference §1 and plan-mode-prompt-crafter rule, **require** that when the user picks **C**, the agent appends the 1–3 sentence reasoning to the **queue payload**: e.g. merge into the entry’s `prompt` field (or a dedicated `params.user_guidance` / `params.reasoning` if added). Document in [Queue-Sources.md](3-Resources/Second-Brain/Queue-Sources.md) that queue entries may carry a `prompt` (or merged guidance) that includes crafter-generated reasoning when C was chosen, and that EAT-QUEUE / guidance-aware merge this into pipeline context.

### 6.3 Validation and merge (auto-eat-queue, dispatch)

- **Current**: auto-eat-queue Step 5 merges params (entry + Config + defaults) and validates “merged params against MCP-Tools.md contracts”.
- **Shield**: Ensure **merged** params (after applying defaults for omitted keys) are validated, not only the raw entry. Document in [.cursor/rules/context/auto-eat-queue.mdc](.cursor/rules/context/auto-eat-queue.mdc) that when a key is absent (B or C), validation uses the result of the merge chain; ensure [Second-Brain-Config](3-Resources/Second-Brain/Second-Brain-Config.md) / prompt_defaults never set invalid values (e.g. rationale_style, context_mode, max_candidates in allowed ranges).

### 6.4 Explicit wording and “exact match” rule

- **Current**: plan-mode-prompt-crafter requires “exact question text and options from §1”. New §1 will have longer explanatory text.
- **Shield**: Keep the rule’s requirement that questions come from §1; no change. After §1 is updated, the “exact wording” is the new text. If the rule is ever interpreted as “character-for-character”, add a short note: “Exact = use the question and option text from §1; minor formatting (e.g. bold, line breaks) may follow the Question output template.”

### 6.5 Examples and flow docs (outdated A/B/C)

- **Files**: [Prompt-Crafter-Examples.md](3-Resources/Second-Brain/Prompt-Crafter-Examples.md) uses “Include X? A. yes B. no C. let AI decide” and “B. use default / infer”. [Prompt-Crafter-Structure-Detailed.md](3-Resources/Second-Brain/Second-Brain-User-Flows/Prompt-Crafter-Structure-Detailed.md) has “Include enable_research? … A. yes B. no C. let AI decide” and “user picks B for that toggle” for context-tracking.
- **Shield**: Update Prompt-Crafter-Examples.md to use the new semantics (A = explicit value, B = default/omit, C = AI reasoning + user_guidance) and, where applicable, the new explanatory question style. Update Prompt-Crafter-Structure-Detailed.md: replace the “Include enable_research?” example with a §1-aligned example; change “unless user picks B for that toggle” to “unless the payload explicitly sets enable_context_tracking: false”.

### 6.6 Commander / macros and Queue-Alias-Table

- **Risk**: Commander “Craft Prompt” or other macros might assume old “B = no” or “include/no” semantics.
- **Shield**: Grep for Commander/macro docs and [Queue-Alias-Table.md](3-Resources/Second-Brain/Queue-Alias-Table.md); if they reference “B = false” or “include/no”, add a note that the question-led flow now uses A = explicit, B = default (omit), C = AI reasoning per User-Questions-and-Options-Reference §1. No code change if macros only append validated payloads from the crafter.

### 6.7 Chat-Prompts and Rules references to “Y/n”

- **Files**: [Chat-Prompts.md](3-Resources/Second-Brain/Chat-Prompts.md), [Rules.md](3-Resources/Second-Brain/Rules.md) reference “Append to queue? (Y/n)”.
- **Shield**: If the Final question stays **Y/n**, leave as-is. If §1 switches to **A/B/C** Final (A = append, B = cancel, C = double-check), update these docs to reference the Final question from §1 (e.g. “Append to queue? A. yes — append … B. no — cancel … C. AI reasoning — double-check”) and ensure the rule’s Step 8 and fail conditions refer to “Final question from §1” rather than hardcoding “Y/n”.

### 6.8 Param descriptors and param_meta

- **Current**: Param descriptors have “Default when C / omitted”. With new semantics, B and C both omit; C adds reasoning.
- **Shield**: In User-Questions-and-Options-Reference §1 Param descriptors, optionally add a line: “When B or C, key is omitted; when C, append short reasoning to prompt/user_guidance.” param_meta remains advisory; no consumer change.

### 6.9 Summary: extra files for compensation/shields


| File                                 | Action                                                                                                        |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------- |
| Parameters.md, Queue-Sources.md      | One sentence: absent = default; crafted payloads may omit keys.                                               |
| Prompt-Crafter-Structure-Detailed.md | Update enable_research example and “user picks B” → “payload explicitly sets enable_context_tracking: false”. |
| Prompt-Crafter-Examples.md           | Align examples with new A/B/C semantics and explanatory style.                                                |
| auto-eat-queue.mdc                   | Clarify that validation applies to merged params (entry + Config + defaults).                                 |
| Chat-Prompts.md, Rules.md            | If Final becomes A/B/C, reference §1 for Final question wording.                                              |


---

## Order of operations

1. **User-Questions-and-Options-Reference.md** per §1 minimal diff (replace §1 bullets + Quick mapping table; Boolean params para; Messages 1–9 block; C choice behavior; param order note; Final callout if A/B/C).
2. **plan-mode-prompt-crafter.mdc** (constraint 3–5 sentences + append to user_guidance/prompt; replace A/B/C mapping; booleans omit not false; Step 8 user_guidance merge after C choices); then **sync** `.cursor/sync/rules/context/plan-mode-prompt-crafter.md`.
3. **Compensations**: Prompt-Crafter-Structure-Detailed (B→payload explicitly sets false); Prompt-Crafter-Examples (new A/B/C style); Parameters + Queue-Sources (one line re omit keys); auto-eat-queue (validate merged params); Chat-Prompts + Rules (pointer to §1 Message 9 if Final A/B/C).
4. **Safety net before save**: Grep for B/no/false; dry-run C on context_mode; dry-run C on enable_research.
5. *Optional after first ship*: Recommended ranges in Param descriptors; Prompt-Crafter-Param-Table question_order; ROADMAP mirror note.

