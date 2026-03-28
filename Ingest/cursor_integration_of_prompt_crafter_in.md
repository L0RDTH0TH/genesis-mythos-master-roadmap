# Integration of prompt crafter into plan mode

> **Deprecated (2026-03):** This flow now runs in **Chat or Agent mode**; do not use Cursor Plan mode (it creates a plan file instead of Q&A). The rest of this note describes the original Plan-mode design and is kept for history only.
_Exported on 3/10/2026 at 17:57:51 EDT from Cursor (2.6.18)_

---

**User**

What do you think of folding the prompt crafter into your plan mode? We could setup the workflow to be something like, user starts plan mode with "We are making a ROADMAP-MODE prompt." Then Cursor looks at the rules loads the defaults and uses the question feature to ask questions in a "include this optional?" A. yes B. no, this will practiaclly  depricate mobile prompting support but that is acceptable in exchange for quality and accuracy.

---

**Cursor**


Exploring the prompt crafter and plan-mode setup so we can give an informed opinion.



Checking how ROADMAP-MODE prompts are built and where mobile prompting fits in:



Checking how Commander builds prompts and what "question feature" might refer to:



Here’s a concise take based on your codebase.

---

## Opinion: Folding the prompt crafter into Plan mode

**Verdict: It’s a good direction.** Using Plan mode as the place where “we’re making a ROADMAP-MODE (or RESUME-ROADMAP, etc.) prompt” and having the agent load rules/defaults and then ask “include this optional? A. yes / B. no” fits how your system is already set up and trades mobile prompting for quality in a reasonable way.

### Why it fits

1. **Single source of truth**  
   Plan mode already has access to rules, `Second-Brain-Config.md` (`prompt_defaults`), `Queue-Sources.md`, and `Parameters.md`. The agent can derive the full param set for a mode and ask only for the optionals, so the “schema” stays in the docs/Config instead of in a separate crafter implementation.

2. **Accuracy over guessing**  
   Right now, crafting is either Commander macros (fixed bundles like “Craft Deepen Aggressive”) or EAT-QUEUE merge order (queue → `user_guidance` → Config). An explicit A/B per optional (“Include `enable_research`? A. yes B. no”) makes each choice conscious and avoids wrong or forgotten defaults.

3. **Plan mode is already the “approval gate”**  
   You already use Plan mode for “propose then execute,” EAT-CACHE paste, and approval gates. Using the same mode to “propose a prompt via Q&A, then emit queue entry (or run)” is consistent and keeps one mental model: “structured Cursor session → outcome.”

4. **Crafter stays doc-only, implementation lives in the agent**  
   Prompt-Crafter-Structure-Detailed and Commander describe *what* to assemble; there’s no separate `.cursor/skills/prompt-crafter/SKILL.md`. Plan-mode Q&A doesn’t require a new skill so much as a **protocol**: when the user says “We are making a ROADMAP-MODE prompt” (or RESUME-ROADMAP, INGEST MODE, etc.), the agent:
   - loads that mode’s params from Queue-Sources + Parameters + Config,
   - shows defaults,
   - asks for each optional (or grouped) with “Include X? A. yes B. no,”
   - then emits the queue entry (and optionally runs EAT-QUEUE).

5. **Mobile trade-off is acceptable**  
   Prompt-crafter is already documented as laptop-only; mobile is mainly “simple queue add” (e.g. “Resume roadmap” with defaults) and “approve pending” (e.g. Async Approve, Mobile-Pending-Actions). Deprecating “mobile prompting” here means: the **high-accuracy path** is Plan mode on the laptop with Q&A; mobile doesn’t get the full optional-param flow. That’s consistent with your note that trading mobile prompting for quality/accuracy is acceptable.

### Things to watch

- **No native “question feature”**  
   Cursor doesn’t have a special “ask user A/B” API; the agent would ask in chat and interpret replies (“A” / “B”, “yes” / “no”, “skip”). You’d encode this in a rule or a short skill: “In Plan mode, when crafting a [MODE] prompt, ask one optional at a time (or by group), offer A/B, and map the user’s reply to params.”  
   **Update (2025):** Cursor Plan mode now has a **questions box with click-to-answer (A, B, C)**. **Migrated (2026-03):** Use this question UI pattern in Chat or Agent mode for the question-led prompt crafter; do not run this flow in Plan mode. Ask **one question per message**, options on separate lines with real newlines (not literal backslash-n), no code block; note Cursor known bug where backslash-n can render literally. Do not group multiple params into one question; ask one param per message per User-Questions-and-Options-Reference section 1 order. See plan-mode-prompt-crafter rule and Prompt-Crafter-Structure-Detailed section Plan-mode Q&A pattern.

- **Length of Q&A**  
   RESUME-ROADMAP has many optionals (`enable_research`, `handoff_gate`, `inject_extra_state`, `token_cap`, `branch_factor`, research_*, etc.). Ask **one param per message** in section 1 order; do not group multiple params into a single question.

- **Output**  
   Decide and document whether the agent (1) only appends to `prompt-queue.jsonl`, (2) only outputs a paste-ready EAT-CACHE payload, or (3) both and optionally triggers EAT-QUEUE.

### Summary

Folding the prompt crafter into Plan mode with a “load defaults → ask optionals (A/B) → emit queue entry” flow is a solid way to get better quality and accuracy while keeping one source of truth (rules + Config). Treating mobile as “simple queue + approve” and the laptop Plan-mode Q&A as the high-accuracy path is a reasonable and consistent trade-off. I’d document this as a **Plan-mode prompt-crafting protocol** (e.g. in Prompt-Crafter-Structure-Detailed or a small “plan-mode-craft” rule) and optionally keep Commander macros as one-tap presets that append a fixed entry without Q&A, with the doc stating that the full, accurate path is Plan mode + Q&A.

---

**User**

Build the prompt crafter into plan mode migration plan. 

Mode selection & defaults load: For any supported mode (e.g. RESUME-ROADMAP, INGEST MODE, ORGANIZE MODE, DISTILL MODE, EXPRESS MODE), define a protocol where the Plan-mode agent:


For these I want to truncate them slightly, so we migrate the kickoffs to two; CODE and ROADMAP, then from those funnel the user through optionals until a prompt is crafted. Then completely migrate the mobile to manual observation and filling ingest folder. This will require a deep rework of our wiring to properly funnel. We should also add a C option for let AI decide after other selections are made.

---

**Cursor**


Reading the current plan and updating it for the two-kickoff funnel (CODE / ROADMAP), the "C = let AI decide" option, and the mobile → manual Ingest migration.



Checking how mobile and Watcher/queue wiring are referenced so we can specify the rework:



Updating the plan with the two-kickoff funnel (CODE / ROADMAP), the C option, and the mobile → manual Ingest migration.



Verifying the plan file for completeness and any leftover fragments:



Summary of updates to the plan:

**1. Two kickoffs only (CODE and ROADMAP)**  
- Replaced the many per-mode entrypoints with a single choice: **CODE** or **ROADMAP**.  
- **CODE** → INGEST, ORGANIZE, DISTILL, EXPRESS, ARCHIVE, and task modes.  
- **ROADMAP** → ROADMAP MODE (setup) or RESUME-ROADMAP (continue).  
- Funnel: kickoff → concrete mode → optionals → crafted prompt.

**2. A/B/C pattern**  
- **A** = Yes / first option  
- **B** = No / second option  
- **C** = Let AI decide (resolved after all other choices, using defaults + context).  
- C is offered for optionals that can be inferred (e.g. project_id, phase, profile, research).  
- Protocol: ask optionals in order, collect C’s, resolve C in a final pass, then show summary and emit payload.

**3. Mobile → manual observation + Ingest**  
- Mobile is no longer a prompt-crafting or queue-appending channel.  
- Mobile = **manual observation** (read/review) + **filling Ingest** (create/move content into `Ingest/`).  
- All queue consumption and Plan-mode crafting are **laptop-only**.  
- Deprecate/remove on mobile: Watcher queue append, Commander queue macros, Mobile-Pending-Actions as a queue source; Mobile-Pending-Actions can stay as a read-only “to do on laptop” list.

**4. Deep wiring rework**  
- Section 6 lists concrete changes:  
  - Rules: `watcher-result-append`, `auto-eat-queue`, `auto-queue-processor`, `confidence-loops`, `mobile-seed-detect` updated so queue/prompt flow is laptop-only and mobile is observe + Ingest.  
  - Queue-Sources / Queue-Alias-Table: state that prompt-queue and Task-Queue are written only from laptop.  
  - Watcher/Commander: on mobile, hide or repurpose queue-append commands; keep only observation and Ingest-related commands.

**5. Todos**  
- Todos were replaced with: two-kickoff protocol, A/B/C loop, CODE funnel design, ROADMAP funnel design, mobile migration spec, wiring rework plan, examples and validation, guardrails and crafted_params.

The plan file is at `~/.cursor/plans/plan-mode-prompt-crafter-integration_ff5a3980.plan.md`. If you want, we can adjust any section or add a short “Implementation order” subsection.

---

**User**

It should have an optional we are making a prompt ai ask which kind code or roadmap, this protects against ai guessing when user is unclear.

---

**Cursor**


Adding the clarification step to the protocol so the flow is explicit:



Summary of changes:

**Section 1 (Two kickoffs)**  
- **Optional clarification when unclear**: If the user says only “We are making a prompt” (or similar) and does not say CODE or ROADMAP, the agent **must ask** before continuing, e.g. “Which kind? A. CODE (pipelines: ingest, organize, distill, express, archive, task modes) B. ROADMAP (setup or resume roadmap).” The agent must **not** infer the kickoff from context so it doesn’t guess when the user is unclear.  
- Docs are updated to say that a generic “We are making a prompt” **triggers** this “Which kind? CODE or ROADMAP?” question.

**Section 2 (Protocol)**  
- Protocol step (1) is now: **Resolve kickoff** — if the user only said “We are making a prompt” (or similar) without CODE or ROADMAP, ask “Which kind? A. CODE B. ROADMAP” and do not guess. The rest of the steps are unchanged (load schema, show param block, ask optionals, resolve C, summary, emit payload).

---

**User**

The options  presented to the user should not just be "Use this param?" it should be more "Use this param? It does...".

---

**Cursor**


Adding a reminder in the examples section so transcript-style examples include the "It does..." pattern:



Updating the todo to include the "It does..." requirement:



Summary of updates:

**Section 2 (Optionals and A/B/C)**  
- **Present options with explanation**: The plan now says not to ask only “Use this param?” — each optional (or group) must include a short “It does …” (or “They do …” for groups) so the user can choose with context.  
- Example in the plan: *“Include research-related options? **It does:** run external research before deepen and inject results; can fill gaps when util is low. A. yes B. no C. let AI decide.”*  
- Param grouping bullet updated so each optional or group is presented “**with a brief ‘It does …’**”.

**Section 7 (Examples)**  
- Transcript-style examples are required to show this pattern: “each optional shown with ‘It does …’”.

**Todo**  
- `abc-option-loop` now reads: “Specify Q&A pattern with A/B/C and ‘It does …’ per optional; param grouping and when to offer C.”

---

**User**

Some of our options accept manual text input to help shape the result of the calls/pipelines, when a param like that is selected as true the user will; click continue as that is default Cursor behavior, then moves to next question, when all param options are finished agent should reprompt user with more questions, something like" What is the param text" with a text input field, we iterate back and forth with questions until Cursor has manual confirmation for every available param.

We should probobly build a param table tracking parantage who owns and uses what where in our question list does it get asked etc, this will standardize the questions so they are always in a predictable order for consistency.

---

**Cursor**


Adding the manual text-input phase and the param-table deliverable to the plan.



Adding a todo for the param table and updating the examples to mention the manual-text phase.



Summary of what was added:

**1. Manual text input phase (Section 2)**  
- Params that take free text (e.g. `user_guidance`, `prompt`, `research_queries`, `userText`, `sectionOrTaskLocator`) are only **included or excluded** in the A/B/C loop — no text is requested there.  
- User continues through the A/B/C questions as usual (click continue → next question).  
- **After all param optionals are done**, the agent runs a **manual text phase**: for each included param that accepts text, it asks e.g. “What is the [param name]?” with a text input (or placeholder). It goes back and forth until every such param has **manual confirmation**.  
- Only after that does it show the final summary and emit the payload. So: A/B/C flow first, then one batch of text gathering, then summary/emit.

**2. Param table (new Section 2b)**  
- **Deliverable**: A **param table** used so questions are in a **fixed order** and ownership is clear.  
- **Columns**:  
  - **param** — name  
  - **parentage / owner** — kickoff + sub-mode (e.g. ROADMAP → RESUME-ROADMAP, CODE → INGEST MODE)  
  - **used_by** — pipeline/skill/processor that consumes it  
  - **question_order** — position in the question list for that mode  
  - **accepts_manual_text** — whether to ask “What is the [param]?” in the manual text phase when included  
- **Location**: In or linked from Prompt-Crafter-Structure-Detailed and/or a dedicated `Prompt-Crafter-Param-Table.md`; kept in sync with Queue-Sources and Parameters.  
- **Use**: The agent (and any rule/skill) uses the table to know what to ask, in what order, and which params get a follow-up in the manual text phase.

**3. Protocol and examples**  
- Protocol steps now include: (4) ask optionals **in param-table order**; (6) **manual text phase**; then (7) summary, (8) emit.  
- Examples now mention the manual text phase when a text-accepting param is included (e.g. `user_guidance`, `research_queries`).

**4. New todos**  
- **param-table**: Build the table (param, parentage, used_by, question_order, accepts_manual_text) and standardize question order per mode.  
- **manual-text-phase**: Document the phase: after all optionals, reprompt “What is the [param]?” for each text-accepting param until confirmed.

