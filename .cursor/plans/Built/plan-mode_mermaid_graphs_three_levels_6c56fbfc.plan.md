---
name: Plan-mode Mermaid graphs three levels
overview: Add three levels (High, Mid, Detailed) of Mermaid diagrams for (1) user flow through Plan-mode prompt-crafter questions and (2) Plan-mode/prompt-crafter architecture, in the existing Second-Brain-User-Flows and Prompt-Crafter-Structure docs.
todos:
  - id: user-flow-high
    content: Add Plan-mode Q&A user flow Mermaid to User-Flow-Prompt-Crafter-High-Level.md
    status: completed
  - id: user-flow-mid
    content: Add Plan-mode Q&A user flow (mid-level) Mermaid to User-Flow-Prompt-Crafter-Mid-Level.md
    status: completed
  - id: user-flow-detailed
    content: Add Plan-mode Q&A user flow (detailed) Mermaid to User-Flow-Prompt-Crafter-Detailed.md
    status: completed
  - id: arch-high
    content: Add Plan-mode architecture (high-level) Mermaid to Prompt-Crafter-Structure-High-Level.md
    status: completed
  - id: arch-mid
    content: Add Plan-mode architecture (mid-level) Mermaid to Prompt-Crafter-Structure-Mid-Level.md
    status: completed
  - id: arch-detailed
    content: Add Plan-mode architecture (detailed) Mermaid to Prompt-Crafter-Structure-Detailed.md
    status: completed
  - id: verify-docs
    content: Verify Rules, Chat-Prompts, Queue-Sources, Param-Table, Backbone, README, rule, Vault-Layout, Logs for stale entries and gaps; fix and optionally add verification note
    status: completed
isProject: false
---

# Plan-mode Mermaid graphs (three levels: user flows + architecture)

## Scope

- **User flows**: The path the user takes through Plan-mode Q&A (kickoff → mode → optionals in order → manual text → summary → append?). Three Mermaid flowcharts at High, Mid, and Detailed level.
- **Architectures**: The system components and data flow for Plan-mode prompt crafting (rule, param table, Config, Queue-Sources, validation, routing, queue append). Three Mermaid flowcharts at High, Mid, and Detailed level.
- **Location**: Reuse existing three-level doc structure in [3-Resources/Second-Brain/Second-Brain-User-Flows](3-Resources/Second-Brain/Second-Brain-User-Flows) and [Prompt-Crafter-Structure-*](3-Resources/Second-Brain/Second-Brain-User-Flows/Prompt-Crafter-Structure-High-Level.md). No new files; add new sections + diagrams to the six existing files.

**Source of truth for question order**: [Prompt-Crafter-Param-Table.md](3-Resources/Second-Brain/Prompt-Crafter-Param-Table.md) (ROADMAP MODE 2 params; RESUME-ROADMAP 18; CODE→INGEST 6; ORGANIZE 5; DISTILL 3; EXPRESS 2; ARCHIVE 1; Task modes 5).

---

## Part 1: User flow diagrams (three levels)

Add a new section **"Plan-mode Q&A user flow"** (or **"Plan-mode crafting: user path through questions"**) to each of the three User-Flow-Prompt-Crafter docs. Each section contains one Mermaid flowchart; the level of granularity increases from High to Detailed.

### 1.1 High-Level — [User-Flow-Prompt-Crafter-High-Level.md](3-Resources/Second-Brain/Second-Brain-User-Flows/User-Flow-Prompt-Crafter-High-Level.md)

**Content**: One linear flowchart. No branching by kickoff or mode; a single path.

- **Nodes**: Start (e.g. "User says We are making a prompt") → Kickoff (Which kind? CODE / ROADMAP) → ModeChoice (e.g. "Choose mode or pipeline") → Optionals (single box: "Optionals in param table order, one question per message, A/B/C") → ManualText ("Manual text phase for params that accept text") → Summary ("Summary + optional plan + payload") → AppendConfirm ("Append to queue? Y/n") → branch: Confirm → ValidateRouteAppend → Done; Decline → NoWrite ("Payload in plan for copy-paste").
- **Mermaid**: Use `flowchart TD`; node IDs without spaces (e.g. `Kickoff`, `ModeChoice`, `Optionals`, `ManualText`, `Summary`, `AppendConfirm`, `Confirm`, `Decline`, `ValidateRouteAppend`, `Done`, `NoWrite`). Edge labels like `|Y|` and `|n|` for the AppendConfirm branch.
- **Placement**: After the existing "Safety invariants" section; add a short intro sentence that this is the Plan-mode Q&A path (distinct from Commander macro path already described).

### 1.2 Mid-Level — [User-Flow-Prompt-Crafter-Mid-Level.md](3-Resources/Second-Brain/Second-Brain-User-Flows/User-Flow-Prompt-Crafter-Mid-Level.md)

**Content**: One flowchart with branching by kickoff and by mode. Still no per-question nodes.

- **Nodes**: Start → Kickoff → decision: CODE vs ROADMAP.
  - **CODE branch**: ModeChoice ("Which pipeline? INGEST / ORGANIZE / DISTILL / EXPRESS / ARCHIVE / Task modes") → OptionalsCODE (single box: "Optionals per param table for chosen pipeline, e.g. 1–6 for INGEST") → ManualText → Summary → AppendConfirm → Confirm/Decline → same as High.
  - **ROADMAP branch**: ModeChoiceRoadmap ("ROADMAP MODE vs RESUME-ROADMAP") → OptionalsRoadmap (two boxes or one: "ROADMAP MODE: 2 optionals; RESUME-ROADMAP: 18 optionals") → ManualText → Summary → AppendConfirm → same.
- **Mermaid**: `flowchart TD` with `Kickoff --> CodeBranch` and `Kickoff --> RoadmapBranch`; subgraphs optional for clarity (e.g. `subgraph code [CODE path]`, `subgraph road [ROADMAP path]`). Merge back before ManualText so the rest of the flow is shared.
- **Placement**: New section "Plan-mode Q&A user flow (mid-level)" after the existing "Sub-macros and batch" section. One short paragraph: Plan-mode path is one-question-per-message; optionals count varies by mode (see Param-Table).

### 1.3 Detailed — [User-Flow-Prompt-Crafter-Detailed.md](3-Resources/Second-Brain/Second-Brain-User-Flows/User-Flow-Prompt-Crafter-Detailed.md)

**Content**: Flowcharts that reflect the actual question order from the param table. Two options (choose one to keep the diagram maintainable):

- **Option A (recommended)**: One main flowchart with **subgraphs per mode** (e.g. "CODE → INGEST MODE", "CODE → ORGANIZE MODE", "ROADMAP → RESUME-ROADMAP"). Inside each subgraph, **nodes for each question_order step** — but for RESUME-ROADMAP (18 steps), group into 3–4 logical blocks (e.g. "Q1–4: action, project_id, phase, sectionOrTaskLocator" → "Q5–11: context_tracking, research, handoff" → "Q12–16: inject, token_cap, depth, branch_factor, profile" → "Q17–18: userText, queue_next") to avoid 18 tiny nodes. For INGEST (6), all 6 can be individual nodes (Q1_source_file through Q6_rationale_style). Label nodes with param name so the diagram doubles as a visual index into [Prompt-Crafter-Param-Table](3-Resources/Second-Brain/Prompt-Crafter-Param-Table.md).
- **Option B**: Separate small flowcharts per mode (e.g. one for "RESUME-ROADMAP optionals 1–18", one for "INGEST optionals 1–6") and a top-level flowchart that switches by kickoff/mode to "see diagram RESUME-ROADMAP" / "see diagram INGEST". More diagrams, clearer per-mode view.

Recommend **Option A** in the plan: one diagram with subgraphs; inside RESUME-ROADMAP subgraph use 4 grouped nodes (Q1_4, Q5_11, Q12_16, Q17_18) with labels that list param names; inside CODE→INGEST use 6 nodes Q1..Q6. Add a note below the diagram: "Full question_order and param names: see [[Prompt-Crafter-Param-Table]]."

**Placement**: New section "Plan-mode Q&A user flow (detailed)" at the end of User-Flow-Prompt-Crafter-Detailed.md. Optional: add a second, smaller flowchart for "Manual text phase and append" (which params have accepts_manual_text true, then Summary → Append? → Validate → Route → Read-append-write).

---

## Part 2: Architecture diagrams (three levels)

Add a new section **"Plan-mode architecture"** to each of the three Prompt-Crafter-Structure docs. Each section contains one Mermaid diagram showing components and data flow.

### 2.1 High-Level — [Prompt-Crafter-Structure-High-Level.md](3-Resources/Second-Brain/Second-Brain-User-Flows/Prompt-Crafter-Structure-High-Level.md)

**Content**: Minimal component view.

- **Nodes**: User → CursorPlanMode ["Cursor Plan mode"] → Rule ["plan-mode-prompt-crafter rule"] → ParamTable ["Param table + Config + Queue-Sources"] → Questions ["One question per message, A/B/C"] → Summary → Validate → Route ["Route by mode: prompt-queue vs Task-Queue"] → Append ["Read-append-write to queue file"] → Done.
- **Mermaid**: `flowchart LR` or `flowchart TD`; simple left-to-right or top-to-down. No file paths yet; labels like "Param table", "Validate", "Route".
- **Placement**: New section after "End-to-end flow (high-level)" (which already has the Commander flow). Title: "Plan-mode architecture (high-level)".

### 2.2 Mid-Level — [Prompt-Crafter-Structure-Mid-Level.md](3-Resources/Second-Brain/Second-Brain-User-Flows/Prompt-Crafter-Structure-Mid-Level.md)

**Content**: Name the main artifacts and show data flow.

- **Nodes**: Trigger ["We are making a prompt / CODE / ROADMAP"] → RuleMdc [".cursor/rules/context/plan-mode-prompt-crafter.mdc"] → ParamTableDoc ["Prompt-Crafter-Param-Table.md"] + Config ["Second-Brain-Config, Parameters"] + QueueSources ["Queue-Sources.md"] → LoadSchema ["Load schema and question_order"] → AskOptionals ["Ask one per message, A/B/C"] → ResolveC → ManualTextPhase → Summary → Validate ["mode + params object + JSON"] → Route ["Routing table: Task-Queue.md for 9 task modes, else prompt-queue.jsonl"] → ReadAppendWrite ["Read file, append one line, write back"] → promptQueue [".technical/prompt-queue.jsonl"] or taskQueue ["3-Resources/Task-Queue.md"].
- **Mermaid**: `flowchart TD`; subgraph for "Sources" (ParamTableDoc, Config, QueueSources) feeding LoadSchema. Show Validate and Route as distinct steps; branch after Route to the two queue files. Use node IDs without spaces; labels may include "Queue-Sources" (use quotes if needed: `QueueSources["Queue-Sources"]`).
- **Placement**: New section "Plan-mode architecture (mid-level)" after "EAT-QUEUE and guidance-aware merge". Brief prose: Rule reads param table and Config; after Q&A, payload is validated and routed per Queue-Sources.

### 2.3 Detailed — [Prompt-Crafter-Structure-Detailed.md](3-Resources/Second-Brain/Second-Brain-User-Flows/Prompt-Crafter-Structure-Detailed.md)

**Content**: All artifacts and Defenses (validation, routing, decline, read-then-append).

- **Nodes**: Include: trigger phrase; .cursor/rules/context/plan-mode-prompt-crafter.mdc; .cursor/sync/rules/context/plan-mode-prompt-crafter.md; Prompt-Crafter-Param-Table.md (with note: question_order per mode); Queue-Sources.md (Plan-mode queue routing, Task-Queue structure); Parameters.md; Second-Brain-Config.md; validation step (mode present, known mode, params object, valid JSON); routing decision (9 task modes → Task-Queue.md, else prompt-queue.jsonl); decline path (no write); read-then-append (read full file → append one newline + one JSONL line → write back); Cursor question UI (one question per message, A./B./C. format). Optionally: Defenses cross-ref (Task-Queue body structure, minimal file creation).
- **Mermaid**: `flowchart TD` with subgraphs, e.g. "Rules", "Docs (param table, Queue-Sources, Config)", "Flow (validate → route → read-append-write)", "Output (prompt-queue.jsonl | Task-Queue.md)". Include a decision node "User confirms append?" with No → NoWrite, Yes → Validate.
- **Placement**: New section "Plan-mode architecture (detailed)" near the end of Prompt-Crafter-Structure-Detailed.md (e.g. after "CODE funnel design" and "ROADMAP funnel design", before or after "Config: prompt_defaults"). One short paragraph referencing Defenses in the plan and Queue-Sources § Plan-mode queue routing.

---

## Part 3: Verify other docs (no stale entries, no gaps)

After adding the six Mermaid sections, **audit** the following docs so they stay consistent with Plan-mode behavior and the new diagrams. Fix any stale wording, add missing cross-links, and close gaps.

### 3.1 Docs to check and what to verify


| Doc                                                                                                                           | Checks                                                                                                                                                                                                                                                         |
| ----------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Rules.md](3-Resources/Second-Brain/Rules.md)                                                                                 | Context table row for `plan-mode-prompt-crafter.mdc`: mentions one-question-per-message and question box; no "readonly" or "emit only"; references queue append after confirm. No stale pipeline list.                                                         |
| [Chat-Prompts.md](3-Resources/Second-Brain/Chat-Prompts.md)                                                                   | Plan-mode crafting table and paragraph: Q&A first, one question per message, "Append? (Y/n)", confirm/decline, validate/route/read-append-write. No "no direct vault writes" without "except queue append after confirm".                                      |
| [Queue-Sources.md](3-Resources/Second-Brain/Queue-Sources.md)                                                                 | Plan-mode queue routing table matches rule (9 task modes → Task-Queue.md; else prompt-queue.jsonl). Task-Queue.md structure and append location, validation, decline, read-then-append all present. Mode list vs Param-Table and Queue-Alias-Table consistent. |
| [Prompt-Crafter-Param-Table.md](3-Resources/Second-Brain/Prompt-Crafter-Param-Table.md)                                       | All modes in Queue-Sources / rule that use Plan-mode have a table section; question_order has no gaps or duplicates per owner. Column definitions still match rule (param, parentage, used_by, question_order, accepts_manual_text).                           |
| [Backbone.md](3-Resources/Second-Brain/Backbone.md)                                                                           | Prompt-Crafter bullet: Plan-mode appends to queue after confirm; optional one-line pointer to "Plan-mode user flow and architecture: see User-Flow-Prompt-Crafter-* and Prompt-Crafter-Structure-*" if not already there.                                      |
| [README](3-Resources/Second-Brain/README.md)                                                                                  | Documentation index or links: User-Flow-Prompt-Crafter-* and Prompt-Crafter-Structure-* (and/or Plan-mode diagrams) listed if they are the canonical flow/structure docs. No broken or outdated links.                                                         |
| [.cursor/rules/context/plan-mode-prompt-crafter.mdc](.cursor/rules/context/plan-mode-prompt-crafter.mdc)                      | Description and step 7 match Queue-Sources routing table and Defenses. No leftover "readonly" or "emit only". Reference to Prompt-Crafter-Param-Table and Queue-Sources present.                                                                               |
| [Prompt-Crafter-Structure-Detailed.md](3-Resources/Second-Brain/Second-Brain-User-Flows/Prompt-Crafter-Structure-Detailed.md) | After adding architecture diagram: cross-links to Param-Table, Queue-Sources, plan rule, and (optional) to User-Flow-Prompt-Crafter-* for "user path" are correct. Protocol (8) and Funnel still say Q&A first and append after confirm.                       |
| [Vault-Layout.md](3-Resources/Second-Brain/Vault-Layout.md)                                                                   | .technical row still points to Queue-Sources for Task-Queue body and Plan-mode append. No stale path or format.                                                                                                                                                |
| [Logs.md](3-Resources/Second-Brain/Logs.md)                                                                                   | If prompt-crafter or Plan-mode logging is documented, it matches current behavior (e.g. no "readonly" logging only; append outcome if applicable).                                                                                                             |


### 3.2 Gap and consistency checks

- **Mode list**: The set of modes that route to Task-Queue.md (TASK-ROADMAP, TASK-COMPLETE, ADD-ROADMAP-ITEM, EXPAND-ROAD, REORDER-ROADMAP, DUPLICATE-ROADMAP, MERGE-ROADMAPS, EXPORT-ROADMAP, PROGRESS-REPORT) is identical in the rule, Queue-Sources, and any routing table in the new architecture diagrams.
- **Stale phrases**: Search for "readonly", "no direct vault writes", "emit payload only" in prompt-crafter and Plan-mode context; remove or qualify so "append to queue after confirm" is the single allowed write.
- **Cross-links**: From User-Flow-Prompt-Crafter-* and Prompt-Crafter-Structure-*, links to Param-Table, Queue-Sources, Chat-Prompts, Rules, and the plan-mode rule resolve and are still relevant. Add "See also" to the new diagram sections pointing to the other level (e.g. High links to Mid and Detailed).
- **Sync**: If any of the above docs reference .cursor/sync/rules/context/plan-mode-prompt-crafter.md or changelog, ensure they are not outdated relative to the .mdc rule.

### 3.3 Deliverable

- A short **audit pass**: For each doc in the table, confirm the checks and fix any issues found.
- Optional: Append a one-line **verification note** to the plan or to [Second-Brain-User-Flows](3-Resources/Second-Brain/Second-Brain-User-Flows) README / index (if one exists) that "Plan-mode user flow and architecture diagrams (High/Mid/Detailed) and related docs were verified for consistency on [date]."

---

## Mermaid syntax (reminder)

- Node IDs: camelCase or underscores; no spaces (e.g. `AppendConfirm`, `ManualText`, `ParamTableDoc`).
- Labels with special characters in quotes: `Route["Route: Task-Queue vs prompt-queue"]`, `NoWrite["Payload in plan for copy-paste"]`.
- Avoid reserved words as IDs: use `ConfirmAppend`, `DeclineAppend` instead of `end`.
- Subgraphs: `subgraph id [Label]` with explicit id (e.g. `subgraph codePath [CODE path]`).
- No styling (no `fill:#`, `classDef`); theme handles colors.

---

## Summary of file changes


| File                                                                                                                              | Change                                                                                                                                                                                                                                                                                  |
| --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [User-Flow-Prompt-Crafter-High-Level.md](3-Resources/Second-Brain/Second-Brain-User-Flows/User-Flow-Prompt-Crafter-High-Level.md) | Add section "Plan-mode Q&A user flow" with one High-level Mermaid (linear path: Start → Kickoff → Mode → Optionals → ManualText → Summary → Append? → Confirm/Decline → Done/NoWrite).                                                                                                  |
| [User-Flow-Prompt-Crafter-Mid-Level.md](3-Resources/Second-Brain/Second-Brain-User-Flows/User-Flow-Prompt-Crafter-Mid-Level.md)   | Add section "Plan-mode Q&A user flow (mid-level)" with one Mermaid (branch by CODE vs ROADMAP; then by mode; optionals as one box per branch; merge at ManualText; same end flow).                                                                                                      |
| [User-Flow-Prompt-Crafter-Detailed.md](3-Resources/Second-Brain/Second-Brain-User-Flows/User-Flow-Prompt-Crafter-Detailed.md)     | Add section "Plan-mode Q&A user flow (detailed)" with one Mermaid (subgraphs per mode; RESUME-ROADMAP optionals as 4 grouped blocks; CODE→INGEST as 6 nodes; note linking to Param-Table). Optionally second small diagram for manual-text + append flow.                               |
| [Prompt-Crafter-Structure-High-Level.md](3-Resources/Second-Brain/Second-Brain-User-Flows/Prompt-Crafter-Structure-High-Level.md) | Add section "Plan-mode architecture (high-level)" with one Mermaid (User → Rule → Param table + Config → Questions → Summary → Validate → Route → Append → Done).                                                                                                                       |
| [Prompt-Crafter-Structure-Mid-Level.md](3-Resources/Second-Brain/Second-Brain-User-Flows/Prompt-Crafter-Structure-Mid-Level.md)   | Add section "Plan-mode architecture (mid-level)" with one Mermaid (trigger, rule path, Param-Table + Config + Queue-Sources, load schema, ask optionals, validate, route, read-append-write, two queue files).                                                                          |
| [Prompt-Crafter-Structure-Detailed.md](3-Resources/Second-Brain/Second-Brain-User-Flows/Prompt-Crafter-Structure-Detailed.md)     | Add section "Plan-mode architecture (detailed)" with one Mermaid (all artifacts: rule, sync, Param-Table, Queue-Sources, Config, Parameters; Defenses: validate, route, decline, read-then-append; Cursor question UI).                                                                 |
| **Part 3: Verification**                                                                                                          | Audit Rules.md, Chat-Prompts.md, Queue-Sources.md, Prompt-Crafter-Param-Table.md, Backbone.md, README, plan-mode-prompt-crafter.mdc, Prompt-Crafter-Structure-Detailed.md, Vault-Layout.md, Logs.md for stale entries, gaps, and consistency; fix and optionally add verification note. |


---

## Optional follow-ups (out of scope for this plan)

- Backbone.md or README: add one-line links to "Plan-mode user flow diagrams" and "Plan-mode architecture diagrams" in the User-Flow and Structure docs.
- Regenerate or add a single "index" Mermaid in a doc that links the six diagrams (e.g. "High / Mid / Detailed: User flow in User-Flow-Prompt-Crafter-*; Architecture in Prompt-Crafter-Structure-*"). Not required for the minimal deliverable.

