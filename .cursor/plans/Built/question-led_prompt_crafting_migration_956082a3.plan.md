---
name: Question-led prompt crafting migration
overview: "Migrate the prompt crafter from \"Plan mode\" to agent-facing, question-led flow: document and enforce that it runs in Chat or Agent mode (not Cursor Plan mode), add a hard \"first response = first question; do not create a plan file\" instruction, and rename framing throughout docs to \"question-led prompt crafting.\""
todos: []
isProject: false
---

# Migrate to agent-facing question-led prompt crafting

## Goal

Stop Cursor Plan mode from creating a plan file when the user says "We are making a prompt." Reframe the flow as **question-led prompt crafting** that runs in **Chat or Agent mode**. The agent’s first response must be to ask the first question (Q0 if kickoff unclear); it must not create or write a `.plan.md` file.

## Strategy

- **Keep the rule filename** `plan-mode-prompt-crafter.mdc` so existing references (Rules.md, links) keep working. Update **in-rule wording** and all **docs** to "question-led" and "Chat/Agent mode."
- Add a **mandatory mode-and-first-response** block at the top of the rule so the agent always sees: use Chat/Agent; do not use Cursor Plan mode; first response = first question; do not create .plan.md.
- **Rip out all old Plan-facing logic**: Remove or replace every reference that assumes this flow runs in Cursor Plan mode, that produces a "plan" as output, or that uses "Plan-mode" as the name of the flow. No remaining "Plan mode" / "Plan-mode" for this crafter.

---

## 0. Rip out old Plan-facing logic (do everywhere)

Apply these removals/replacements in addition to the additive changes below. Goal: zero remaining "Plan mode" or "Plan-mode" framing for this flow; no "plan document" or ".plan.md" as something the agent may produce.

**Rule (.mdc and sync):**

- **Remove** all uses of "Plan-mode" in headings, bullets, and fail messages. Replace with "question-led" or "prompt crafter" (e.g. "Fail conditions (Plan-mode)" → "Fail conditions (prompt crafter)").
- **Replace** every fail report string "Plan-mode failed: ..." with "Prompt crafter failed: ..." (or "Crafter failed: ...").
- **Replace** "§1 (Plan-mode Prompt Crafter)" with "§1 (Question-led Prompt Crafter)" in the rule body and in step 1.
- **Replace** "Plan-mode crafting intent" with "question-led crafting intent"; "Plan-mode entrypoints" with "question-led entrypoints" in the Reference line; "§ Plan-mode crafting" with "§ Prompt crafting (question-led)" in the Chat-Prompts link; "§ Plan-mode queue routing" with "§ Question-led crafter queue routing" in Queue-Sources link.
- **Order invariant**: Change "Do **not** create a plan document (outline, steps, todos)" to "Do **not** create a plan document or write a `.plan.md` file." Change "present summary, optionally output a plan (questions + choices + payload)" to "present summary, optionally a short recap (questions + choices + payload)."
- **Step 8**: Change "Optionally output a plan that lists..." to "Optionally present a recap that lists...". Change "payload is in the plan for copy-paste" to "payload is below for copy-paste" (or "in this chat"). Change "leave payload in plan" to "leave payload in chat" in the confirm bullet.
- **"Cursor Plan mode question UI"** bullet: Reword to "**Question UI (Chat/Agent)**" and keep the format/one-question-only content; say "In Chat or Agent, Cursor can show a question box with click-to-answer (A, B, C) when you ask one question per message..." so it's clear the UI is in Chat, not "Plan mode."
- **"Exactly three options only"**: Remove "(Decision Wrappers ... Plan-mode prompt crafting is A/B/C only)" tail; replace with "(Decision Wrappers use A–G in other flows; this flow is A/B/C only)."

**User-Questions-and-Options-Reference §1:**

- **Remove** "Plan-mode" from heading and "Plan-mode contract"; use "Question-led contract" or "Contract."
- **Remove** "(Cursor Plan mode)" from "How to format each question" subheading.

**Chat-Prompts:**

- **Remove** "in Cursor Plan mode" entirely; replace with "in Chat or Agent mode."
- **Remove** "payload remains in plan" → "payload remains in chat for copy-paste" (or "below for copy-paste").

**Rules.md:**

- **Remove** "Plan-mode" from table row label and Commander bullet; use "Question-led prompt crafting" only.
- **Remove** "payload in plan for copy-paste" → "payload in chat for copy-paste." "from the Plan-mode crafter" → "from the question-led crafter."

**Prompt-Crafter-Structure-Detailed:**

- **Remove** "Plan-mode" from every section title: "Plan-mode crafting entrypoints" → "Question-led prompt crafting entrypoints"; "Plan-mode architecture" → "Question-led prompt crafting architecture"; "Plan-mode Q&A pattern" → "Q&A pattern (question-led)."
- **Remove** "Prompt crafting in **Cursor Plan mode**" → "Prompt crafting in **Chat or Agent mode**."
- **Remove** "Plan-mode crafting is **laptop-only**" → "Question-led crafting is **laptop-only**."
- **Remove** "§ Plan-mode crafting" in cross-references → "§ Prompt crafting (question-led)."
- **Remove** "Plan-mode agent" in mermaid node → "Agent" or "Crafter agent."
- **Remove** "the Plan-mode agent" in prose → "the agent" or "the crafter."

**Prompt-Crafter-Param-Table:**

- **Remove** "Plan-mode crafter" / "Plan-mode" in intro and footnote → "question-led crafter" / "question-led crafting." "For Plan-mode, the **order**" → "For question-led crafting, the **order**."

**Queue-Sources:**

- **Remove** section title "Plan-mode queue routing and append" → "Question-led crafter: queue routing and append."
- **Remove** "When the **Plan-mode prompt crafter** appends" → "When the **question-led prompt crafter** appends."
- **Remove** "Plan-mode crafter appends" in Task-Queue body → "question-led crafter appends."

**User-Flow docs (High/Mid/Detailed):**

- **Remove** "Plan-mode Q&A user flow" → "Question-led prompt crafting flow."
- **Remove** "Plan-mode architecture" → "Question-led prompt crafting architecture."
- **Remove** "User in Plan mode" in mermaid → "User (Chat/Agent)" or "User."
- **Remove** "Plan-mode path" / "Plan-mode agent" in prose and nodes.

**Backbone, Vault-Layout, README, Parameters, tests/fixtures:**

- **Remove** "Plan-mode crafting" / "Plan-mode crafter" / "Plan mode" wherever they refer to this flow → "question-led prompt crafting" / "question-led crafter" / "Chat or Agent mode."
- **Remove** "payload in plan" → "payload in chat" or "payload below."

**Ingest note:**

- **Add** the migrated note; optionally **remove** or soften the old "Folding the prompt crafter into Plan mode" framing so it's clear that path is deprecated.

---

## 1. Rule: mode and first-response mandate

**File:** [.cursor/rules/context/plan-mode-prompt-crafter.mdc](.cursor/rules/context/plan-mode-prompt-crafter.mdc)

- **Add a short "Mode and first response" block** immediately after the frontmatter (or as the first bullet under the title):
  - "**Use Chat or Agent mode** for this flow. Do **not** use Cursor Plan mode: in Plan mode the agent creates a plan file instead of asking questions."
  - "Your **first** response must be to **ask** the first question from User-Questions-and-Options-Reference §1 (Q0 'Which kind?' if the user did not already say CODE or ROADMAP). Do **not** create or write a `.plan.md` file. Do not output a plan document before asking questions."
  - **Pothole E defense:** "**Even if the user is in Cursor Plan mode or you are instructed to create a plan**, for this flow your first response must be to ask the first question from §1. Do not create or write a `.plan.md` file. If the user wanted a plan document, they would not say 'We are making a prompt' for this flow."
- **Update the rule title/heading** from "Plan-mode prompt crafter" to **"Question-led prompt crafter (Chat/Agent)"**.
- **Update the description** (frontmatter) to say "question-led prompt crafting" and "Chat or Agent mode"; remove "Plan-mode" where it implies Cursor Plan mode.
- **Trigger line**: Keep the same trigger phrases; add "(Use Chat or Agent mode; not Cursor Plan mode.)"
- **Fail conditions**: Add one: "**Creates or writes a .plan.md file** before all Q&A is complete → **FAIL.**" Optionally rename the section to "Fail conditions (prompt crafter)" instead of "(Plan-mode)".

**Sync:** Apply the same changes to [.cursor/sync/rules/context/plan-mode-prompt-crafter.md](.cursor/sync/rules/context/plan-mode-prompt-crafter.md).

---

## 2. User-Questions-and-Options-Reference §1

**File:** [3-Resources/Second-Brain/User-Questions-and-Options-Reference.md](3-Resources/Second-Brain/User-Questions-and-Options-Reference.md)

- **§1 heading**: Change "Plan-mode Prompt Crafter (Cursor Plan mode)" to **"Question-led Prompt Crafter (Chat/Agent)"**.
- **When line**: After "User says ...", add: "**Use Chat or Agent mode.** Do not use Cursor Plan mode for this flow (Plan mode creates a plan file instead of asking questions)."
- **Contract**: Optionally rename "Plan-mode contract" to "Question-led contract" or leave as-is and only change the heading.
- **"How to format each question"**: Change "(Cursor Plan mode)" to "(Chat/Agent)" so it doesn’t imply Cursor Plan mode.

---

## 3. Chat-Prompts

**File:** [3-Resources/Second-Brain/Chat-Prompts.md](3-Resources/Second-Brain/Chat-Prompts.md)

- **Section heading**: Change "Plan-mode crafting (two kickoffs)" to **"Prompt crafting — question-led (Chat/Agent)"**.
- **Intro sentence**: Replace "in Cursor Plan mode" with "in **Chat or Agent mode** (not Cursor Plan mode)."
- **Table and paragraph**: Keep content; add one short bullet or sentence: "Run this flow in Chat or Agent; in Plan mode the agent may create a plan file instead of asking questions."

---

## 4. Rules.md

**File:** [3-Resources/Second-Brain/Rules.md](3-Resources/Second-Brain/Rules.md)

- **Context table row** for `plan-mode-prompt-crafter.mdc`: Change "Plan-mode crafting" to **"Question-led prompt crafting (Chat/Agent)"**. In the description, add "Use Chat or Agent mode; do not use Cursor Plan mode."
- **Questions and options** line: Change "Plan-mode" to "Question-led prompt crafter" in the list (Plan-mode, Decision Wrappers, ...).
- **Commander section** bullet: Change "Plan-mode prompt crafting" to **"Question-led prompt crafting"** and add "Use Chat or Agent mode." Update the Chat-Prompts link anchor if the section id changes (e.g. to `#Prompt crafting — question-led (Chat/Agent)` or similar).

---

## 5. Prompt-Crafter-Structure-Detailed

**File:** [3-Resources/Second-Brain/Second-Brain-User-Flows/Prompt-Crafter-Structure-Detailed.md](3-Resources/Second-Brain/Second-Brain-User-Flows/Prompt-Crafter-Structure-Detailed.md)

- **Section "Plan-mode crafting entrypoints"**: Rename to **"Question-led prompt crafting entrypoints (Chat/Agent)"**.
- **First paragraph**: Replace "Cursor Plan mode" with "**Chat or Agent mode**" for where the flow runs; keep "two kickoffs."
- **"When the user is unclear"**: No need to mention Plan mode; keep Q0 wording.
- **Funnel / Protocol**: Where it says "Plan mode" or "Cursor Plan mode" in the sense of "this flow," change to "Chat/Agent" or "question-led." Where it refers to the **question UI** (click-to-answer A/B/C), keep "Cursor" only as "Cursor can show a questions box" (the UI exists in Chat when the agent asks one question per message).
- **Cross-references**: Update any link text "Plan-mode" to "question-led" for this flow.

---

## 6. Prompt-Crafter-Examples

**File:** [3-Resources/Second-Brain/Prompt-Crafter-Examples.md](3-Resources/Second-Brain/Prompt-Crafter-Examples.md)

- **Title or intro**: If it says "Plan-mode" or "Plan mode," change to **"Question-led prompt crafting"** or "Chat/Agent."
- **Example headings**: e.g. "Example 1: CODE → INGEST MODE" can stay; no need to say "Plan mode" there.

---

## 7. Other docs (Backbone, Vault-Layout, Queue-Sources, Mobile-Migration-Spec)

- **Backbone, Vault-Layout, Queue-Sources**: Replace "Plan mode" / "Plan-mode" with "question-led prompt crafting" or "Chat/Agent" only where they refer to **this** prompt-crafting flow. Do not change references to other "plan" concepts (e.g. roadmap plans).
- **Mobile-Migration-Spec**: Where it says "Plan mode" for crafting, change to "Chat/Agent question-led crafting" and keep "laptop-only."

---

## 8. Ingest note (historical)

**File:** [Ingest/cursor_integration_of_prompt_crafter_in.md](Ingest/cursor_integration_of_prompt_crafter_in.md)

- Add a **one-line note** at the top of "Things to watch" or after the Update (2025) line: "**Migrated (2026-03):** This flow now runs in **Chat or Agent mode**; do not use Cursor Plan mode (it creates a plan file instead of Q&A)."

---

## 9. Changelog and optional rule rename

- **[.cursor/sync/changelog.md](.cursor/sync/changelog.md)**: Add an entry: "Migrate prompt crafter to **agent-facing question-led** (Chat/Agent mode). **Rip out** all Plan-facing logic: remove 'Plan mode' / 'Plan-mode' for this flow; 'Plan-mode failed' → 'Prompt crafter failed'; 'plan document' / 'output a plan' → no .plan.md + optional recap; 'payload in plan' → 'payload in chat'; rename section titles and node labels to question-led. Rule and docs: use Chat or Agent, not Cursor Plan mode; first response = first question; do not create .plan.md. User-Questions-and-Options-Reference §1, Chat-Prompts, Rules, Prompt-Crafter-Structure-Detailed, Param-Table, Queue-Sources, User-Flow docs, Backbone, Vault-Layout, README, Parameters, tests, Ingest note. Sync: plan-mode-prompt-crafter.md."
- **Optional (not in scope for this plan):** Rename the rule file to `prompt-crafter-question-led.mdc` and update all references (Rules.md, links in docs). That would be a follow-up if you want the filename to match the new framing.

---

## Potholes and defenses (codebase search)

Potential pitfalls that could undo or weaken the migration. Address each during implementation.

**A. Ingest/cursor_integration_of_prompt_crafter_in.md**

- **Pothole:** The note is a long "fold prompt crafter into Plan mode" opinion: title, section "Folding the prompt crafter into Plan mode", "Plan mode is already the approval gate", "Plan-mode Q&A", "high-accuracy path is Plan mode on the laptop", "In Plan mode, when crafting...", "Plan-mode prompt-crafting protocol", "plan-mode-craft rule", "full, accurate path is Plan mode + Q&A", "Plan-mode agent", "Plan-mode crafting are laptop-only", and a reference to the plan file `~/.cursor/plans/plan-mode-prompt-crafter-integration_ff5a3980.plan.md`. If the agent (or a future run) reads this note, it can infer the flow belongs in Plan mode.
- **Defense:** Per Section 8, add the migrated note at the top of "Things to watch". **Also** add a short deprecation callout at the very top of the note (after the title): "**Deprecated (2026-03):** This flow now runs in **Chat or Agent mode**; do not use Cursor Plan mode. The following text describes the original Plan-mode design and is kept for history only." Optionally move the note to 4-Archives after migration and link from Chat-Prompts or Rules so the archive is clearly historical.

**B. Legacy Built plans (.cursor/plans/Built/)**

- **Pothole:** Files such as `plan-mode_mermaid_graphs_three_levels_6c56fbfc.plan.md`, `plan-mode_q&a-first_and_queue_append_52027bb1.plan.md`, `plan-mode-prompt-crafter-integration_ff5a3980.plan.md`, `agent_questions_reference_integration_e685dd4e.plan.md` describe "Plan-mode", "optional plan + payload", "Payload in plan for copy-paste", "Plan-mode agent", "output a plan". If opened or indexed, they reinforce the old behavior.
- **Defense:** Do not rewrite Built plans (they are historical). In the **migration changelog entry**, state clearly: "Legacy .cursor/plans/Built/* prompt-crafter plans are superseded by question-led (Chat/Agent); do not use them for current prompt-crafter behavior." Optionally add one line at the top of each Built plan that mentions the prompt crafter: "Superseded by question-led migration (Chat/Agent); see Rules.md and plan-mode-prompt-crafter rule for current behavior."

**C. Rules.md table row — "optional plan"**

- **Pothole:** The context table still says "then optional plan and append to queue after confirm". That can be read as "output a plan document."
- **Defense:** Already in Section 0 rip-out: replace with "then optional recap and append to queue after confirm" (or "optional summary (Q&A + payload)").

**D. Changelog history**

- **Pothole:** Many changelog entries say "Plan-mode prompt-crafter", "Plan-mode Q&A", "Plan-mode: ...". They are a historical record; changing them would be noisy. If something directs the agent to the changelog to infer "how does prompt crafter work", it could still see Plan-mode.
- **Defense:** Do not edit old changelog lines. The **new** migration entry must be explicit: "Rip out all Plan-facing logic; flow is **question-led (Chat/Agent) only**. Prior changelog entries that mention Plan-mode are historical; current behavior is defined by the rule and docs as of this entry."

**E. Rule loaded in Plan mode**

- **Pothole:** When the user is in Cursor Plan mode, the product may inject a system instruction like "create a plan" or "you are in Plan mode." The context rule might be loaded alongside that, and the product instruction could still win.
- **Defense:** In the rule's "Mode and first response" block, add an explicit override: "**Even if the user is in Cursor Plan mode or you are instructed to create a plan**, for this flow your **first** response must be to **ask** the first question from §1 (Q0 if kickoff unclear). Do **not** create or write a `.plan.md` file. If the user wanted a plan document, they would not say 'We are making a prompt' for this flow."

**F. Parameters.md**

- **Pothole:** Parameters.md says "Plan-mode crafted payload" for `crafted_params_conf_boost`. That keeps Plan-mode in the vocabulary.
- **Defense:** In Parameters.md, replace "Plan-mode crafted payload" with "question-led crafted payload" (or "prompt-crafter crafted payload").

**G. README Documentation index**

- **Pothole:** README lines 31–34 and 40 say "Plan-mode crafting", "Plan-mode examples", "Plan-mode" in the User-Questions list, and "Plan-mode user flow and architecture diagrams". These are entry points for discovery.
- **Defense:** Already in Section 0 "Backbone, Vault-Layout, README"; explicitly replace in README every "Plan-mode" with "question-led" or "Question-led prompt crafting" in those lines.

**H. tests/fixtures/prompt-crafter/README.md**

- **Pothole:** Says "Plan-mode contract tests" and "**Plan-mode**: Given A/B/C answers". Test docs can reinforce the old name.
- **Defense:** Replace "Plan-mode contract tests" with "question-led prompt crafter contract tests". Replace "**Plan-mode**:" with "**Question-led crafter**:" in the expected-queue.jsonl bullet.

**I. Chat-Prompts section anchor**

- **Pothole:** When the section heading is renamed from "Plan-mode crafting (two kickoffs)" to "Prompt crafting — question-led (Chat/Agent)", the anchor (e.g. `#Plan-mode-crafting-two-kickoffs`) will change. Any link that points to the old anchor will break (e.g. Rules.md Commander bullet, Backbone, other docs).
- **Defense:** After renaming the heading, search for links to `#Plan-mode crafting` or `Plan-mode crafting (two kickoffs)` and update them to the new anchor (e.g. `#Prompt-crafting—question-led-ChatAgent` or the slug your editor generates). Check Rules.md, Backbone, Prompt-Crafter-Structure-Detailed, User-Questions-and-Options-Reference cross-references.

**J. Protocol step "optional plan" in Structure-Detailed**

- **Pothole:** Protocol step (7)/(8) says "optionally output a plan" or "Summary + optional plan + payload". The word "plan" can be interpreted as writing a plan file.
- **Defense:** Already in Section 0: use "optional recap" or "optional summary (Q&A + payload)". In Structure-Detailed Protocol, replace "optional plan" with "optional recap" or "optional summary" so it is unambiguous that no .plan.md is produced.

**K. No other rule on same trigger**

- **Pothole:** Another context rule could theoretically trigger on "We are making a prompt" and do something different (e.g. create a plan).
- **Defense:** Grep confirmed only `plan-mode-prompt-crafter.mdc` uses that trigger. No change needed; just ensure the single rule is the only one and that its "first response = first question" and "do not create .plan.md" are at the top so they are seen first.

---

## Summary


| Location                                                     | Change                                                                                                                                                                                                                                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| plan-mode-prompt-crafter.mdc (+ sync)                        | **Rip out** Plan-mode in headings/fail/links; "plan document" → no .plan.md + optional recap; "Cursor Plan mode question UI" → "Question UI (Chat/Agent)". **Add** Mode and first response; title → "Question-led prompt crafter (Chat/Agent)"; new fail: .plan.md before Q&A. |
| User-Questions-and-Options-Reference.md §1                   | Heading and "When" → question-led, Chat/Agent; do not use Plan mode.                                                                                                                                                                                                           |
| Chat-Prompts.md                                              | Section → "Prompt crafting — question-led (Chat/Agent)"; intro and note: use Chat/Agent.                                                                                                                                                                                       |
| Rules.md                                                     | Table row and Commander bullet → "Question-led prompt crafting (Chat/Agent)"; use Chat or Agent.                                                                                                                                                                               |
| Prompt-Crafter-Structure-Detailed.md                         | Entrypoints and funnel/protocol wording → question-led, Chat/Agent.                                                                                                                                                                                                            |
| Prompt-Crafter-Examples.md                                   | Title/intro → question-led / Chat/Agent if present.                                                                                                                                                                                                                            |
| Backbone, Vault-Layout, Queue-Sources, Mobile-Migration-Spec | Replace Plan mode with question-led/Chat/Agent for this flow only.                                                                                                                                                                                                             |
| Parameters.md, tests/fixtures/prompt-crafter/README.md       | **Pothole F, H:** Parameters "Plan-mode crafted payload" → "question-led crafted payload"; fixtures README "Plan-mode" → "question-led crafter".                                                                                                                               |
| Ingest/cursor_integration...                                 | **Add** migrated note + **deprecation callout** at top (Pothole A). Optionally soften Plan framing or archive.                                                                                                                                                                 |
| changelog.md                                                 | Entry for migration; note supersedes legacy Built prompt-crafter plans (Pothole B, D).                                                                                                                                                                                         |


**Potholes (Section above):** Apply defenses A–K: Ingest note deprecation callout (+ optional archive); Built plans note in changelog / optional one-liner in Built files; Parameters.md "question-led crafted payload"; README index lines; tests/fixtures README "question-led"; Chat-Prompts anchor and link updates; rule override for "even if in Plan mode"; changelog entry wording; Protocol "recap" not "plan"; confirm no other rule on same trigger.

**Rip out (Section 0):** Strip all "Plan mode" / "Plan-mode" for this flow; replace fail messages "Plan-mode failed" → "Prompt crafter failed"; replace "plan document" / "output a plan" with recap/summary and "do not create .plan.md"; replace "payload in plan" with "payload in chat/below"; rename all section titles and node labels that say "Plan-mode" to "question-led" or "Question-led prompt crafting." Apply in rule, User-Questions-and-Options-Reference, Chat-Prompts, Rules, Structure-Detailed, Param-Table, Queue-Sources, User-Flow docs (High/Mid/Detailed), Backbone, Vault-Layout, README, Parameters, tests/fixtures, Ingest note.

No changes to the Q&A sequence, §1 order, or queue append behavior—only mode, framing, and removal of all Plan-facing wording.