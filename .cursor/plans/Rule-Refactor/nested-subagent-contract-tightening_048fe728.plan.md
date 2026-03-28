---
name: nested-subagent-contract-tightening
overview: Define a documentation-only plan to support experimental nested subagent calls while preserving existing primary coordination logic.
todos:
  - id: define-orchestration-hierarchy
    content: Document single-orchestrator hierarchy (main → queue/dispatcher → pipeline subagent → optional nested subagent) and add a small mermaid diagram.
    status: completed
  - id: write-nested-policy
    content: Add a central nested-subagent policy (max depth, fan-out guidance, prohibited behaviors, pure-function semantics).
    status: completed
  - id: whitelist-nested-pairs
    content: Enumerate and document allowed nested subagent pairs with their input/output contracts.
    status: completed
  - id: update-agent-specs
    content: Update each pipeline subagent spec with a "Subagent nesting" subsection and tighten prompts/specs to forbid orchestration behaviors.
    status: completed
  - id: clarify-error-ownership
    content: Clarify that only top-level runs write Errors.md and Decision Wrappers; nested subagents return structured errors only.
    status: completed
  - id: document-fallbacks
    content: Document experimental status of nested subagents and the non-nested fallback behavior in core architecture docs.
    status: completed
isProject: false
---

# Nested Subagent Call Support Contract Tightening

## Goals

- **Clarify contracts** for when and how subagents may call other subagents (nesting) without changing existing coordination code.
- **Preserve the current single-orchestrator model**: queue/dispatcher and top-level agent remain the only sources of orchestration, queue writes, and watcher logging.
- **Make nested subagent use explicitly optional and reversible**, since the feature is experimental.

## Plan

### 1. Document orchestration boundaries

- **Describe the orchestration hierarchy** in the backbone docs (e.g. `3-Resources/Second-Brain/Second-Brain-Config.md` or `Backbone.md` plus `Cursor-Skill-Pipelines-Reference.md`):
  - Top-level agent + Queue/Dispatcher are the **only orchestrators** allowed to:
    - Read/write `.technical/prompt-queue.jsonl` and `3-Resources/Task-Queue.md`.
    - Dispatch modes to pipeline subagents.
    - Append to `3-Resources/Watcher-Result.md` and pipeline logs (`Ingest-Log`, `Archive-Log`, etc.).
  - Pipeline subagents (ingest, organize, archive, distill, express, roadmap, research, validator) are **executors** that implement one mode per run.
  - Nested subagents (called from inside a pipeline subagent) must **not** perform orchestration responsibilities.
- **Add a small mermaid diagram** in the backbone docs to visualize the call tree: `MainAgent -> QueueDispatcher -> PipelineSubagent -> OptionalNestedSubagent`.

### 2. Define a global nested subagent policy

- In a central rule or docs section (e.g. `Cursor-Skill-Pipelines-Reference.md` or a new "Subagent-Nesting" subsection), define:
  - **Max depth**: recommended maximum nesting depth (e.g. 3): main → pipeline subagent → specialized nested subagent.
  - **Fan-out guidance**: parents may use multiple nested subagent calls in parallel for *local* subtasks only (e.g. several research lookups), not for global re-orchestration.
  - **Prohibited behaviors for nested subagents**:
    - No direct reads/writes to `.technical/prompt-queue.jsonl` or `Task-Queue.md`.
    - No calls to EAT-QUEUE, PROCESS TASK QUEUE, or other orchestration modes.
    - No writes to `Watcher-Result.md` or creation of Decision Wrappers.
    - No global roadmap state updates (e.g. `roadmap-state.md`) unless explicitly delegated from the parent pipeline and documented as such.
- Emphasize that nested subagents behave as **pure functions** from the parent’s perspective: well-specified inputs; constrained outputs; no external side effects beyond what their parent is allowed to perform.

### 3. Create/extend a whitelist of allowed nested calls

- For each pipeline subagent type, document **which nested subagent calls are allowed** and for what purpose:
  - **Roadmap**: may call `research` subagent for pre-deepen research, or `validator` subagent for handoff validation.
  - **Ingest/Organize/Archive/Distill/Express**: may call `docs-researcher` or other lightweight analyzers, but not ingest/organize/archive/roadmap again.
  - **Research**: treated as a leaf or near-leaf; it should not call other orchestrating agents.
- For each allowed pairing, specify:
  - **Input contract**: which fields/paths the nested agent may see (e.g. project_id, source note path, distilled outline).
  - **Output contract**: what data structure comes back (e.g. `research_summaries`, `validation_report`) and how the parent is expected to consume it.
- Note explicitly that any other nested pairing is **disallowed unless later added to this whitelist**.

### 4. Tighten individual agent specs and prompts

- For each major subagent (`ingest`, `organize`, `archive`, `distill`, `express`, `roadmap`, `research`, `validator`, `docs-researcher`):
  - Add a short **"Subagent nesting"** subsection to its documentation/spec describing:
    - Whether it is allowed to call nested subagents.
    - If yes, which specific nested subagent types and for which narrow tasks.
    - An explicit reminder: "This subagent must not manipulate the prompt queue, task queue, or Watcher-Result; those are owned by the top-level Queue/Dispatcher and main agent."
  - Update any high-level prompt or operational description for that agent to:
    - Treat nested agents as **helpers**, not orchestrators.
    - Instruct the agent to return summarized results and **not** to delegate control decisions back out through further queue writes.

### 5. Clarify error-handling responsibilities

- In the backbone error-handling documentation (`3-Resources/Errors.md` spec and related rules):
  - State that **only the top-level run** should:
    - Write structured entries to `3-Resources/Errors.md`.
    - Create Decision Wrappers under `Ingest/Decisions/`**.
  - Nested subagents, on failure, should:
    - Return a **structured error result** to their caller (e.g. `status: "failed"`, `error_type`, `message`).
    - Avoid writing logs or wrappers themselves.
- In pipeline docs, add a note that when a nested subagent fails, the parent subagent either:
  - Degrades gracefully (skip optional validation/research step), or
  - Surfaces the problem in its own output to the top-level agent, which then logs it using the existing error protocol.

### 6. Make experimental nature and fallback behavior explicit

- In a central config/architecture doc, add a short section:
  - Acknowledge that **nested subagent support is experimental and may disappear**.
  - Define a **fallback rule**: if nested subagents are unavailable or error consistently, pipelines must:
    - Skip their nested calls for that run; or
    - Fall back to simpler, inline reasoning within the parent subagent.
  - Reiterate that no critical safety mechanisms (backups, snapshots, PARA moves, queue writes) rely solely on nested agents; they remain implemented in the parent/top-level flows.

### 7. Sync and cross-reference docs

- After updating the above conceptual docs:
  - Ensure any rule/skill documentation mirrors the same constraints (e.g. in `.cursor/sync/`** if you use a sync mirror for rules/skills, and in `3-Resources/Second-Brain/Docs/`** for user-facing descriptions).
  - Add short cross-links between:
    - The orchestration overview (Queue/Dispatcher / pipelines docs),
    - The nested subagent policy section,
    - Each individual subagent’s "Subagent nesting" subsection.

## Todos

- **define-orchestration-hierarchy**: Document the single-orchestrator model and add a mermaid diagram for main → queue → pipeline → nested.
- **write-nested-policy**: Add a central nested-subagent policy section (depth, fan-out, prohibitions, pure-function behavior).
- **whitelist-nested-pairs**: Enumerate and document allowed caller↔nested-subagent pairs with input/output contracts.
- **update-agent-specs**: For each pipeline subagent, add a "Subagent nesting" subsection and adjust prompts/specs to forbid orchestration behavior.
- **clarify-error-ownership**: Update error-handling docs so only top-level runs write Errors.md / Decision Wrappers, nested agents only return structured failures.
- **document-fallbacks**: Document experimental status and fallback behavior when nested calls are unavailable, and ensure this is referenced from pipeline docs.

