---
description: High-level entry funnels that distinguish Prompt-Crafter flows from manual/advanced mode triggers and route them to context rules.
globs: "*"
alwaysApply: true
---

# System Funnels (Prompt-Crafter vs Manual/Advanced)

This rule defines how **instructions and prompts enter the system**, and how they are routed to context rules. It distinguishes:

- **Primary entry**: Question-led **Prompt-Crafter** flows (preferred, safest).
- **Secondary entry**: Direct mode phrases (manual/advanced triggers).

It does **not** define pipeline internals; it only routes to context rules under `.cursor/rules/context/**`.

## Primary entry: Prompt-Crafter (preferred door)

When the user says **“We are making a prompt”**, **“We are making a CODE prompt”**, **“We are making a ROADMAP prompt”**, or equivalent question-led crafting intent:

- The **Prompt-Crafter rule** (`.cursor/rules/context/plan-mode-prompt-crafter.mdc`) runs a strict Q&A flow:
  - All questions and options come from `3-Resources/Second-Brain/User-Questions-and-Options-Reference.md` §1.
  - Exactly one question per message; options A/B/C on separate lines; no skipping questions for the chosen branch.
  - Only after all questions, optionals, and manual text are collected does it assemble a payload.
- The **payload** is a JSON object:
  - `mode: string` — the target mode (e.g. `"INGEST_MODE"`, `"DISTILL_MODE"`, `"RESUME_ROADMAP"`, `"TASK_ROADMAP"`, etc.).
  - `params: object` (optional) — structured parameters for that mode.
  - `param_meta: object` (optional) — advisory-only descriptions; never required for correctness.
- The Prompt-Crafter then:
  - Validates the payload against `Queue-Sources.md`,
  - Appends a single JSONL line to `.technical/prompt-queue.jsonl` **only after user confirms** (“Append to queue? Y/n”).

**Invariants for Prompt-Crafter flows**:

- Prompt-Crafter is the **canonical, high-safety door** for:
- Running INGEST_MODE, DISTILL_MODE, EXPRESS_MODE, ARCHIVE_MODE,
- Roadmap flows (ROADMAP_MODE, RESUME_ROADMAP, RECAL-ROAD, etc.),
  - Task/roadmap queues (TASK-ROADMAP, TASK-COMPLETE, ADD-ROADMAP-ITEM, EXPAND-ROAD, etc.).
- Pipelines invoked via Prompt-Crafter:
  - Always receive fully-specified, validated `mode` + `params` objects.
  - May apply `crafted_params_conf_boost` per `Parameters.md`.
  - Are considered **standard / normal** automation flows.

## Secondary entry: Manual / advanced mode triggers

In addition to Prompt-Crafter, the system supports **direct phrases** that map to pipelines. These are treated as **manual/advanced operations**:

- Intended for laptop use (power users, Commander macros).
- Bypass Prompt-Crafter Q&A, but **must still obey** `always/core-guardrails.mdc` (backups, snapshots, confidence bands, exclusions).
- May assume more context (e.g. current file, selection, folder scope), and may rely on defaults more heavily.

- **PromptCraft recovery (machine-routed, not question-led crafter):** **REPAIR CRAFT**, **PROMPT CRAFT RECOVERY** — Layer 0 calls **`Task(prompt_craft)`** per [dispatcher.mdc](.cursor/rules/always/dispatcher.mdc); optional Layer 1 automation when **Second-Brain-Config** `recovery_auto_craft_enabled` is true ([[.cursor/rules/agents/queue.mdc|queue.mdc]] **A.5d**). Coexists with plan-mode Prompt Crafter; does not replace User-Questions §1.

### Manual mode phrases and routing (declarative)

Pipeline triggers: **EAT-QUEUE** — **Layer 0 must launch the Queue/Dispatcher subagent (Layer 1) via the `Task` tool**; Layer 0 must not run queue orchestration inline. The **Queue subagent** then dispatches pipeline modes **only** by **calling the `Task` tool** with the hand-off block as **prompt** and the matching **subagent_type** (roadmap | ingest | distill | express | archive | organize | research | **validator**). For **ROADMAP_HANDOFF_VALIDATE**, the queue passes **model** from Second-Brain-Config § validator.roadmap_handoff.model. For other pipeline Task calls, **omit** `model` to inherit the parent model, or pass **`"fast"`** only when intended; **never** pass `model: "inherit"` (invalid Task API). The subagent runs in a separate context. There is no same-run fallback; if the Task tool is unavailable or a call fails, the entry is treated as failed (Watcher-Result, Errors.md). **Direct triggers** (user said "Resume roadmap", "INGEST MODE", etc. without EAT-QUEUE): route through the `Task` tool with hand-off + subagent_type; do not execute pipeline steps inline.

The following phrases (case-insensitive, partial match) are recognized as manual/advanced triggers and routed accordingly:

- **INGEST MODE – safe batch autopilot**, **INGEST MODE**, **Process Ingest**, **run ingests**
  - Delegate to [.cursor/agents/ingest.md](.cursor/agents/ingest.md) or run from [legacy-agents/ingest.mdc](.cursor/rules/legacy-agents/ingest.mdc) — non-MD handling, Phase 1 propose + Decision Wrapper, Phase 2 apply-mode when queue Step 0 invokes.

- **DISTILL MODE – safe batch autopilot**, **distill this note**, **refine this note**, **DISTILL LENS: [angle]**, **HIGHLIGHT PERSPECTIVE: [lens]**
  - Delegate to [.cursor/agents/distill.md](.cursor/agents/distill.md) or run from [legacy-agents/distill.mdc](.cursor/rules/legacy-agents/distill.mdc) — autonomous-distill; Step 0 distill-apply-from-wrapper re-runs this pipeline.

- **EXPRESS MODE – safe batch autopilot**, **express this note**, **generate outline**, **create publishable summary**, **EXPRESS VIEW: [angle]**
  - Delegate to [.cursor/agents/express.md](.cursor/agents/express.md) or run from [legacy-agents/express.mdc](.cursor/rules/legacy-agents/express.mdc) — autonomous-express; Step 0 express-apply-from-wrapper re-runs this pipeline.

- **ARCHIVE MODE – safe batch autopilot**, **archive this note**, **send to Archives**, **move completed to 4-Archives**
  - Delegate to [.cursor/agents/archive.md](.cursor/agents/archive.md) or run from [legacy-agents/archive.mdc](.cursor/rules/legacy-agents/archive.mdc) — autonomous-archive; ghost-folder sweep after moves.

- **ORGANIZE MODE – safe batch autopilot**, **re-organize this note**, **Re-organize Projects and Resources**, **classify and move**, **put this note in the right folder**
  - Delegate to [.cursor/agents/organize.md](.cursor/agents/organize.md) or run from [legacy-agents/organize.mdc](.cursor/rules/legacy-agents/organize.mdc) — autonomous-organize; name-enhance in organize context.

- **EAT-QUEUE**, **EAT-QUEUE BREAK-SPIN**, **Process queue**, **EAT-CACHE**, **eat cache**
  - Routed to:
    - **Queue/Dispatcher subagent** `agents/queue.mdc` (via [always/dispatcher.mdc](.cursor/rules/always/dispatcher.mdc)) — prompt queue processor for `.technical/prompt-queue.jsonl` or EAT-CACHE payloads. **BREAK-SPIN:** optional **`## operator_break_spin`** YAML in the Layer 0 hand-off; alternate deepen before recal fallback; Layer 0 loud voice only after **`Task(queue)`** when Config **`queue.layer0_escalation_enabled`** ([[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]] § EAT-QUEUE BREAK-SPIN).

- **PROCESS TASK QUEUE**
  - Routed to:
    - **Queue/Dispatcher subagent** `agents/queue.mdc` (via [always/dispatcher.mdc](.cursor/rules/always/dispatcher.mdc)) — task/roadmap queue processor for `3-Resources/Task-Queue.md`.

- **RESEARCH_AGENT** (queue mode only; e.g. EAT-QUEUE with mode RESEARCH_AGENT or RESEARCH-GAPS alias)
  - Delegate to [.cursor/agents/research.md](.cursor/agents/research.md) or run from [legacy-agents/research.mdc](.cursor/rules/legacy-agents/research.mdc) — resolve project_id + linked_phase, research-agent-run, queue INGEST/DISTILL, Errors backstop, Watcher-Result. Pre-deepen research remains with Roadmap subagent (calls research-agent-run directly).

- **GARDEN REVIEW**, **run garden review**, **orphans and distill candidates**, **garden health**, **vault orphans**, **distill candidates sweep**
  - Routed to:
    - `context/auto-garden-review.mdc` (garden review flow).

- **CURATE CLUSTER**, **cluster curate**, **theme gaps**, **merge suggestions**
  - Routed to:
    - `context/auto-curate-cluster.mdc` (curate cluster flow).

### Roadmap-related manual/queue modes

Roadmap flows are unified through `RESUME_ROADMAP` with `params.action` set appropriately. **Execution**: delegate to [.cursor/agents/roadmap.md](.cursor/agents/roadmap.md) or run from [legacy-agents/roadmap.mdc](.cursor/rules/legacy-agents/roadmap.mdc). The Queue processor (main agent) performs normalization, bootstrap, and Step 0 (roadmap-next-step wrapper) then delegates to the Roadmap subagent (real or legacy).

- **ROADMAP MODE – generate from outline**, **ROADMAP MODE**
  - Delegate to `.cursor/agents/roadmap.md` or run from `legacy-agents/roadmap.mdc` in **setup** path (Phase 0, roadmap-state, workflow_state, initial roadmap tree). Queue processor dispatches ROADMAP_MODE entries to the Roadmap subagent.

- **RESUME_ROADMAP**, **Resume roadmap**
  - Delegate to `.cursor/agents/roadmap.md` or run from `legacy-agents/roadmap.mdc` in **continue** path (single action per run, default `action: deepen`). Queue processor dispatches RESUME_ROADMAP entries to the Roadmap subagent.

- **Chain commands (Phase 3):** When the user says **Resume roadmap with research** or **RESUME_ROADMAP-RESEARCH**, the queue processor accepts chain mode `RESUME_ROADMAP-RESEARCH` (run RESEARCH_AGENT then RESUME_ROADMAP with results). **Resume roadmap with research and ingest** / **RESUME_ROADMAP-RESEARCH-INGEST** runs RESEARCH_AGENT → INGEST_MODE → RESUME_ROADMAP. See Queue-Sources § Chain modes and Queue-Alias-Table § Chain command aliases.

- Aliases normalized (in **Queue** flow `agents/queue.mdc` before dispatch):
  - **RECAL-ROAD** → `mode: "RESUME_ROADMAP"`, `params.action: "recal"`.
  - **RESUME-FROM-LAST-SAFE** → `mode: "RESUME_ROADMAP"`, `params.action: "resume-from-last-safe"`.
  - **REVERT-PHASE** → `mode: "RESUME_ROADMAP"`, `params.action: "revert-phase"`, `params.phase: …`.
  - **SYNC-PHASE-OUTPUTS** → `mode: "RESUME_ROADMAP"`, `params.action: "sync-outputs"`.
  - **HANDOFF-AUDIT** → `mode: "RESUME_ROADMAP"`, `params.action: "handoff-audit"`.
  - **EXPAND-ROAD** → `mode: "RESUME_ROADMAP"`, `params.action: "expand"`, with section/task locator + user text.

- **ROADMAP_HANDOFF_VALIDATE** (queue mode): Queue dispatches to **Validator subagent** ([agents/validator.mdc](.cursor/rules/agents/validator.mdc)); final validation pass on roadmap → one handoff-readiness report. Params: project_id (required), optional roadmap_dir, phase_range. Queue passes **model** from Second-Brain-Config § validator.roadmap_handoff.model.

These modes may be enqueued by Prompt-Crafter **or** manually. All roadmap execution and state mutations flow through the **Roadmap subagent** (real `.cursor/agents/roadmap.md` or legacy `legacy-agents/roadmap.mdc`); queue processor keeps normalization, bootstrap, and Step 0. Must respect `always/core-guardrails.mdc`.

## Guidance-Aware Runs

Some runs are **guidance-aware**, meaning they load user refinement instructions from:

- Note frontmatter `user_guidance` (often with `approved: true`), or
- Queue entry `prompt` when `source_file` points at a note, or
- Tag `#guidance-aware`.

The full behavior is defined in `always/guidance-aware.mdc`. This funnel only states:

- Guidance is a **soft hint** only:
  - It may influence classification, path, split, distill depth, etc.
  - It must **never** override safety gates (backups, snapshots, confidence bands, exclusions).
- Guidance-aware behavior is applied **after** routing:
  - First, system-funnels decide which pipeline/context rule runs.
  - Then, if the run qualifies as guidance-aware, `guidance-aware` applies its contract to that run.

## Watcher Bridge (Watcher-Result)

The Obsidian Watcher plugin relies on a stable line format in `3-Resources/Watcher-Result.md`:

```text
requestId: <id> | status: success|failure | message: "..." | trace: "..." | completed: <ISO8601>
```

- The **canonical behavior** is defined in `always/watcher-result-append.mdc`:
  - Queue-based runs (EAT-QUEUE, PROCESS TASK QUEUE) append one line per processed queue entry.
  - Direct Watcher-triggered runs append one line per requestId from `Watcher-Signal.md`.
- Pipelines and context rules **must not** invent new formats for Watcher-Result:
  - Additional detail goes into `message` and `trace` strings.
  - `requestId`, `status`, and `completed` remain stable and parseable.

System-funnels only declare **when** to treat a run as Watcher-triggered:

- When a mode phrase is invoked from the Watcher plugin or from a queue entry with an `id` used as `requestId`.
- When processing Decision Wrappers or task/roadmap queue entries that originated from Watcher or Commander flows.

