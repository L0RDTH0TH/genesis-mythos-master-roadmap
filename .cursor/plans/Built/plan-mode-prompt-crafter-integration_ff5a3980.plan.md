---
name: plan-mode-prompt-crafter-integration
overview: Integrate the prompt-crafter into Cursor Plan mode with two kickoffs (CODE and ROADMAP), funnel optionals with A/B/C (C = let AI decide), and fully migrate mobile to manual observation and filling Ingest folder, requiring deep wiring rework.
todos:
  - id: two-kickoff-protocol
    content: Define CODE and ROADMAP as the only Plan-mode crafting entrypoints; document funnel from kickoff to pipeline/action and optionals.
    status: completed
  - id: abc-option-loop
    content: Specify Q&A pattern with A/B/C and "It does …" per optional; param grouping and when to offer C.
    status: completed
  - id: param-table
    content: Build param table (param, parentage, used_by, question_order, accepts_manual_text); standardize question order per mode.
    status: completed
  - id: manual-text-phase
    content: "Document manual text phase: after all optionals, reprompt \"What is the [param]?\" for each text-accepting param until confirmed."
    status: completed
  - id: code-funnel-design
    content: Design CODE funnel (INGEST, ORGANIZE, DISTILL, EXPRESS, ARCHIVE, task modes) and their optionals with defaults load.
    status: completed
  - id: roadmap-funnel-design
    content: Design ROADMAP funnel (ROADMAP MODE setup vs RESUME-ROADMAP continue) and optionals; tie to existing two-command funnel.
    status: completed
  - id: mobile-migration-spec
    content: Specify full mobile migration to manual observation + filling Ingest; list all wiring to rework (Watcher, Commander, queue, Mobile-Pending-Actions).
    status: completed
  - id: wiring-rework-plan
    content: Produce deep rework plan for rules, Queue-Sources, Watcher/Commander docs so queue/prompt flow is laptop-only; mobile = Ingest fill only.
    status: completed
  - id: examples-and-validation
    content: Add Plan-mode examples (CODE and ROADMAP), C-option behavior, and fixture/validation for crafted payloads.
    status: completed
  - id: guardrails-and-crafted-params
    content: Reinforce non-destructive invariant and crafted_params_conf_boost for Plan-mode output; optional rule/skill sketch.
    status: completed
  - id: clarify-doc-entrypoints
    content: Document Plan-mode prompt crafting entrypoints and scope in Prompt-Crafter-Structure-Detailed and related docs.
    status: completed
  - id: define-plan-mode-protocol
    content: Specify the generic Plan-mode prompt-crafting protocol (defaults loading, param grouping, Q&A loop, validation).
    status: completed
  - id: roadmap-qna-design
    content: Design the RESUME-ROADMAP-specific Q&A script and param mapping, including action selection and research/context options.
    status: completed
  - id: align-commander-macros
    content: Align Commander prompt-crafter macros conceptually with the Plan-mode crafter and document their relationship.
    status: completed
  - id: extend-to-other-modes
    content: Lightly extend Plan-mode crafting support docs to INGEST/ORGANIZE/DISTILL/EXPRESS with minimal Q&A.
    status: completed
  - id: examples-and-tests
    content: Add Plan-mode crafting examples and ensure fixtures/tests match expected assembled params.
    status: completed
  - id: guardrails-and-future
    content: Reinforce non-destructive invariants, tie into crafted_params_conf_boost, and optionally sketch a future rule/skill for automated use.
    status: completed
isProject: false
---

## Plan-Mode Prompt-Crafter Integration (Two-Kickoff + Mobile Migration)

### 1. Two kickoffs: CODE and ROADMAP

- **Single entrypoint**: User starts a Plan-mode crafting session with one of two kickoffs only:
  - **CODE** — leads to pipeline and task modes: INGEST MODE, ORGANIZE MODE, DISTILL MODE, EXPRESS MODE, ARCHIVE MODE, task/queue modes (TASK-ROADMAP, TASK-COMPLETE, ADD-ROADMAP-ITEM, etc.).
  - **ROADMAP** — leads to roadmap flows: ROADMAP MODE (setup only: Phase 0 + workflow_state + roadmap-generate-from-outline) and RESUME-ROADMAP (single continue entry; params.action: deepen, recal, revert-phase, sync-outputs, handoff-audit, etc.).
- **Optional clarification when unclear**: If the user says only "We are making a prompt" (or equivalent) without specifying CODE or ROADMAP, the agent **must ask** before proceeding: e.g. "Which kind? A. CODE (pipelines: ingest, organize, distill, express, archive, task modes) B. ROADMAP (setup or resume roadmap)." Do **not** guess kickoff from context; asking protects against wrong inference when the user is unclear.
- **Funnel**: After kickoff selection (explicit or from clarification), the agent narrows to a concrete mode (e.g. CODE → INGEST MODE, or ROADMAP → RESUME-ROADMAP deepen), then walks through **optionals** until a full prompt/queue entry is crafted.
- **Docs**: In [Prompt-Crafter-Structure-Detailed.md](3-Resources/Second-Brain/Second-Brain-User-Flows/Prompt-Crafter-Structure-Detailed.md) and [Chat-Prompts.md](3-Resources/Second-Brain/Chat-Prompts.md) (or equivalent), replace per-mode entrypoints with "We are making a CODE prompt" / "We are making a ROADMAP prompt" and document that generic "We are making a prompt" triggers the optional "Which kind? CODE or ROADMAP?" question; document the funnel and that crafting is **laptop-only**.

### 2. Optionals and the A/B/C pattern

- **Three choices per optional (or per group)**:
  - **A** — Yes / include (or first concrete option).
  - **B** — No / exclude (or second concrete option).
  - **C** — Let AI decide (agent chooses after all other user selections are made).
- **Present options with explanation**: When asking about a param or group, do **not** ask only "Use this param?" — always add a short "It does …" (or "They do …" for groups) so the user can choose informed. Example: "Include research-related options? **It does:** run external research before deepen and inject results; can fill gaps when util is low. A. yes B. no C. let AI decide."
- **When to offer C**: Offer C for optionals that can be inferred from context (e.g. project_id, phase, depth profile, research on/off) so the user can defer; the agent resolves C only after the rest of the Q&A is complete, using defaults + context (current file, roadmap state, Config).
- **Param grouping**: Retain logical blocks (core required, common optionals, advanced optionals). For each optional or group, present A/B/C where applicable **with a brief "It does …"**; for binary toggles, A = yes, B = no, C = let AI decide.
- **Protocol**: Plan-mode agent (1) resolves kickoff: if user said only "We are making a prompt" (or similar) without CODE/ROADMAP, ask "Which kind? A. CODE B. ROADMAP" and do not guess; (2) loads base schema and defaults from [Queue-Sources.md](3-Resources/Second-Brain/Queue-Sources.md), [Parameters.md](3-Resources/Second-Brain/Parameters.md), and [Second-Brain-Config.md](3-Resources/Second-Brain/Second-Brain-Config.md); (3) shows current param block; (4) asks optionals in order (per **param table** question order); (5) collects C choices and resolves them in a final pass; (6) **manual text phase** (see below); (7) presents summary for confirmation; (8) emits prompt/queue payload (readonly: no direct vault writes).
- **Manual text input for params**: Some params accept free-text input to shape the run (e.g. `user_guidance`, `prompt`, `research_queries`, `userText`, `sectionOrTaskLocator`). When such a param is selected as true (included) during the A/B/C loop, **do not** ask for the text yet — user clicks continue (default Cursor behavior) and the agent moves to the next question. **After all param optionals are finished**, the agent reprompts: for each param that (a) was set to true and (b) accepts manual text, ask e.g. "What is the [param name]?" with a text input field (or clear placeholder for user to type). Iterate back and forth until the agent has **manual confirmation** for every such param. Only then present the final summary and emit the payload. This keeps the A/B/C flow unbroken and batches all text gathering in one predictable phase.

### 2b. Param table (question order and ownership)

- **Deliverable**: Build and maintain a **param table** that the Plan-mode crafter (and any rule/skill) uses so questions are always in a **predictable order** and ownership is clear. Columns (minimal):
  - **param** — name (e.g. `enable_research`, `user_guidance`, `research_queries`).
  - **parentage / owner** — which kickoff and sub-mode owns it (e.g. ROADMAP → RESUME-ROADMAP, CODE → INGEST MODE).
  - **used_by** — which pipeline, skill, or queue processor consumes it (e.g. auto-roadmap, research-agent-run, full-autonomous-ingest).
  - **question_order** — position in the question list for that kickoff/sub-mode (integer or group + order) so the agent always asks in the same sequence.
  - **accepts_manual_text** — true if the param takes free-text input; when true and param is included, the agent asks for it in the manual text phase after all optionals.
- **Location**: Add the table (or link to it) in [Prompt-Crafter-Structure-Detailed.md](3-Resources/Second-Brain/Second-Brain-User-Flows/Prompt-Crafter-Structure-Detailed.md) and/or a dedicated `3-Resources/Second-Brain/Prompt-Crafter-Param-Table.md`; keep it in sync with [Queue-Sources](3-Resources/Second-Brain/Queue-Sources.md) and [Parameters](3-Resources/Second-Brain/Parameters.md) so new params get a row and a question_order.
- **Effect**: Standardizes the question list per mode — no ad-hoc ordering. Agent (and future rule/skill) reads the table to determine (1) which params to ask for, (2) in what order, (3) which need a follow-up "What is the [param]?" in the manual text phase.

### 3. CODE funnel design

- **After "CODE"**: Ask which pipeline or task mode (INGEST, ORGANIZE, DISTILL, EXPRESS, ARCHIVE, or task modes from [Queue-Alias-Table](3-Resources/Second-Brain/Queue-Alias-Table.md)).
- **Per-mode optionals** (truncated; only key toggles in Q&A):
  - INGEST / ORGANIZE: e.g. context_mode, max_candidates, profile (default / project-priority); C for project_id/source_file when obvious from context.
  - DISTILL / EXPRESS: e.g. distill_lens, express_view, depth; C for lens/view when inferable.
  - ARCHIVE: minimal optionals; C for target path when clear.
  - Task modes: task_id, sectionOrTaskLocator, userText as needed; C where inferable.
- **Defaults load**: For the selected CODE sub-mode, load from `prompt_defaults` (ingest, organize) and MCP defaults; validate against [MCP-Tools.md](3-Resources/Second-Brain/MCP-Tools.md). Output: one JSONL line for `prompt-queue.jsonl` or Task-Queue.md plus optional ready-to-paste chat prompt.

### 4. ROADMAP funnel design

- **After "ROADMAP"**: Ask branch: ROADMAP MODE (setup only) vs RESUME-ROADMAP (continue).
- **ROADMAP MODE**: Few optionals (project_id, seed note path); C for project when unambiguous.
- **RESUME-ROADMAP**: Action selection first (deepen, recal, revert-phase, sync-outputs, handoff-audit, resume-from-last-safe, expand, advance-phase, compact-depth); then optionals in groups:
  - Phase/target: project_id, phase, sectionOrTaskLocator — A/B/C as appropriate.
  - Context/research: enable_context_tracking, enable_research, research_queries, async_research; C for research when util/depth suggest it.
  - Depth/branching: max_depth, branch_factor, profile (e.g. deepen-aggressive); A/B/C for profile.
- **Defaults**: Load from `prompt_defaults.roadmap` and [auto-roadmap](.cursor/rules/context/auto-roadmap.mdc); effective context-tracking remains default-on unless user picks B for that toggle. Output: JSONL for prompt-queue and/or paste-ready prompt; consistent with EAT-CACHE flow.

### 5. Mobile migration: manual observation and Ingest only

- **Target state**: Mobile is **no longer** a prompt-crafting or queue-appending channel. Mobile usage becomes:
  - **Manual observation** — user reads/reviews notes, MOCs, roadmap state.
  - **Filling Ingest folder** — user creates or moves content into `Ingest/` (e.g. quick captures, drafts, links to process later). No Watcher/Commander queue appends from mobile; no Mobile-Pending-Actions for crafting or async approval flows that assume queue-driven runs.
- **Processing**: All queue consumption (EAT-QUEUE, PROCESS TASK QUEUE) and Plan-mode crafting happen on the **laptop**. When the user returns to the laptop, they run EAT-QUEUE (or paste a crafted payload); anything in Ingest/ is then processed by the existing pipelines (full-autonomous-ingest, etc.) as today.
- **Deprecate/remove on mobile**:
  - Watcher "Prompt Modal" / queue append from mobile (or restrict to observation-only actions if any).
  - Commander macros that append to prompt-queue or Task-Queue from mobile (e.g. "Resume Roadmap", "Craft Deepen Aggressive", "Async Approve" that inject queue entries).
  - Reliance on Mobile-Pending-Actions as the primary way to "queue" work from mobile; optionally keep Mobile-Pending-Actions as a **read-only** checklist of things to do on laptop (e.g. "Process Ingest", "Run RESUME-ROADMAP for project X") without auto-appending to queue files.
- **Documentation**: Update [Commander-Plugin-Usage](4-Archives/Resources/Plugins-Usage/Commander-Plugin-Usage.md), [Queue-Sources](3-Resources/Second-Brain/Queue-Sources.md), [Vault-Layout](3-Resources/Second-Brain/Vault-Layout.md) (toolbar / mobile), [Backbone](3-Resources/Second-Brain/Backbone.md), and any mobile-specific flows to state: mobile = observe + fill Ingest; queue and crafting = laptop only.

### 6. Deep rework of wiring

- **Rules to update**:
  - [watcher-result-append.mdc](.cursor/rules/always/watcher-result-append.mdc): clarify that queue-based and task-queue runs are laptop-originated; mobile does not send queue entries.
  - [auto-eat-queue.mdc](.cursor/rules/context/auto-eat-queue.mdc): no expectation of mobile-originated queue entries; EAT-CACHE / prompt-queue.jsonl are filled by Plan-mode crafting or Commander on laptop.
  - [auto-queue-processor.mdc](.cursor/rules/context/auto-queue-processor.mdc): same for Task-Queue.md.
  - [confidence-loops.mdc](.cursor/rules/always/confidence-loops.mdc): async approval (e.g. approved: true + re-queue) remains valid on laptop; remove or reframe mobile-specific "Async Approve" as "approve on laptop when reviewing Mobile-Pending-Actions".
  - [mobile-seed-detect.mdc](.cursor/rules/context/mobile-seed-detect.mdc): reframe so mobile can add content (e.g. `<mark>`) into notes that live in Ingest or elsewhere, but triggering SEEDED-ENHANCE is a laptop action (user runs EAT-QUEUE with a queue that references that note, or runs Plan-mode CODE → DISTILL/SEEDED-ENHANCE).
- **Queue-Sources and Queue-Alias-Table**: State explicitly that prompt-queue.jsonl and Task-Queue.md are written only from laptop (Plan-mode crafter, Commander macros, or manual edit); mobile does not append. Remove or qualify any "Mobile stub" / "Mobile-Pending-Actions" that implied mobile-originated queue flow.
- **Watcher plugin / Commander**: Document configuration change: on mobile, hide or repurpose commands that append to queue; show only commands that support observation and Ingest (e.g. "New note in Ingest", "Move to Ingest"). If Watcher has a "copy queue to clipboard" for EAT-CACHE, that remains a laptop-side flow (paste into Plan mode).
- **MCP / backup safety**: No change to backup/snapshot rules; ingest processing when user runs EAT-QUEUE on laptop is unchanged.

### 7. Examples, validation, and guardrails

- **Examples**: Add transcript-style examples in Prompt-Crafter-Structure-Detailed or a dedicated examples doc (each optional shown with "It does …"; include manual text phase when a text-accepting param is included):
  - CODE → INGEST MODE with A/B/C (e.g. C for project_id); if user_guidance included, show "What is the user_guidance?" → final JSONL.
  - ROADMAP → RESUME-ROADMAP deepen with research and depth optionals, one C (e.g. let AI decide profile); if research_queries or userText included, show manual text reprompt → final JSONL.
- **Fixtures**: Align [Testing.md](3-Resources/Second-Brain/Testing.md) and `tests/fixtures/prompt-crafter/` so that for given A/B/C answers, the resolved payload matches expected-queue.jsonl shape; document C resolution rules (defaults + context).
- **Guardrails**: Plan-mode crafting remains **readonly** (no direct vault writes); only emits prompt/queue payload. [confidence-loops.mdc](.cursor/rules/always/confidence-loops.mdc) and [Parameters.md](3-Resources/Second-Brain/Parameters.md): "crafted params" includes Plan-mode crafted output; `crafted_params_conf_boost` applies when the run uses a payload produced by the Plan-mode crafter.
- **Future**: Optionally add `.cursor/rules/context/plan-mode-prompt-crafter.mdc` or a prompt-crafter SKILL that encodes the two-kickoff funnel and A/B/C loop for agent use.

