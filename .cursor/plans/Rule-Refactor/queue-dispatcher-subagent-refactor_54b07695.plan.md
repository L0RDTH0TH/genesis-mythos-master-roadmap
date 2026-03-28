---
name: queue-dispatcher-subagent-refactor
overview: Refactor the current funnel + queue rules into a lightweight always-on dispatcher and a dedicated Queue/Dispatcher subagent, while preserving all existing pipeline behavior and safety contracts.
todos:
  - id: setup-agents-folder
    content: Create `.cursor/rules/agents/` and decide naming for the Queue/Dispatcher subagent rule file (e.g. `queue.mdc`).
    status: pending
  - id: extract-queue-logic
    content: Move the behavior of `auto-eat-queue.mdc` and `auto-queue-processor.mdc` into the new `agents/queue.mdc` context rule without changing semantics.
    status: pending
  - id: wire-dispatcher-triggers
    content: Update routing so that `EAT-QUEUE` and `PROCESS TASK QUEUE` map to the Queue/Dispatcher subagent, while other modes still map to existing pipeline context rules.
    status: pending
  - id: sync-docs-and-rules
    content: Update `Queue-Sources.md` and `Cursor-Skill-Pipelines-Reference.md` to describe the Queue/Dispatcher subagent, and add/update corresponding `.cursor/sync/rules/**` mirror files.
    status: pending
  - id: run-smoke-tests
    content: Manually run EAT-QUEUE and PROCESS TASK QUEUE against sample queues to verify identical behavior, logs, and safety semantics compared to the pre-refactor state.
    status: pending
isProject: false
---

## Queue/Dispatcher Subagent Refactor

### Goals

- **Isolate queue and dispatch logic** into a dedicated Queue/Dispatcher subagent without changing observable behavior.
- **Keep all existing pipelines (ingest, roadmap, distill, express, archive, organize) intact** and still driven by the same trigger phrases and modes.
- **Reduce always-on rule footprint** so only a small dispatcher and the shared core guardrails are loaded every run.

### High-level architecture

- **Dispatcher (always-on)**
  - Lives in a new rule file (e.g. `[.cursor/rules/always/dispatcher.mdc](.cursor/rules/always/dispatcher.mdc)`), conceptually replacing the routing responsibility currently documented in `system-funnels`.
  - Responsibilities:
    - Recognize primary triggers: `INGEST MODE`, `DISTILL MODE`, `EXPRESS MODE`, `ARCHIVE MODE`, `ORGANIZE MODE`, `EAT-QUEUE`, `PROCESS TASK QUEUE`, roadmap modes, etc.
    - Map each trigger to a **subagent context** (for this phase, Queue/Dispatcher vs “direct pipeline rules”).
    - Ensure shared always-on rules stay loaded: `core-guardrails.mdc`, `confidence-loops.mdc`, `guidance-aware.mdc`, `mcp-obsidian-integration.mdc`, `watcher-result-append.mdc`, `backbone-docs-sync.mdc`.
    - Defer all queue reading, ordering, and per-mode dispatch details to the Queue/Dispatcher subagent.
- **Queue/Dispatcher Subagent (context)**
  - New context rule under an agents folder, e.g. `[.cursor/rules/agents/queue.mdc](.cursor/rules/agents/queue.mdc)`.
  - Encapsulates what `auto-eat-queue.mdc` and `auto-queue-processor.mdc` do today:
    - **Prompt queue path**: `.technical/prompt-queue.jsonl` (EAT-QUEUE / EAT-CACHE).
    - **Task/roadmap queue path**: `3-Resources/Task-Queue.md` (PROCESS TASK QUEUE).
    - Step 0 wrapper handling, parsing/validation, dedup, canonical ordering, dispatch by `mode`, Watcher-Result logging, and clearing/marking entries.
  - Exposes a clean internal interface to the rest of the system: given a queue source and a set of entries, it calls the appropriate pipeline rules (`auto-roadmap`, `auto-organize`, `auto-distill`, `auto-express`, `auto-archive`, ingest apply-mode, etc.), but those pipeline rules themselves remain unchanged.

### Concrete refactor steps

- **1. Introduce agents folder and naming**
  - Add a new folder for subagents: `.cursor/rules/agents/`.
  - Decide naming conventions in comments/header:
    - `agents/queue.mdc` → "Queue/Dispatcher Subagent" (handles both prompt queue and task/roadmap queue).
    - Keep `always/system-funnels.mdc` primarily as documentation of trigger phrases and high-level routing; future phases can further slim it down or fold its content into `dispatcher.mdc`.
- **2. Extract Queue/Dispatcher logic into `agents/queue.mdc`**
  - Start from the current behavior in `[.cursor/rules/context/auto-eat-queue.mdc](.cursor/rules/context/auto-eat-queue.mdc)` and `[.cursor/rules/context/auto-queue-processor.mdc](.cursor/rules/context/auto-queue-processor.mdc)`:
    - Preserve:
      - Step 0 "Always-check wrappers" semantics and `CHECK_WRAPPERS` entry handling.
      - Queue reading, parsing/validation, deduplication, canonical ordering (including roadmap mode normalization and RESUME-ROADMAP bootstrap), and guidance-aware merging of `params`.
      - Mode→pipeline mapping table (INGEST MODE, ORGANIZE MODE, DISTILL MODE, EXPRESS MODE, ARCHIVE MODE, FORCE-WRAPPER, ROADMAP MODE, RESUME-ROADMAP, RESEARCH-AGENT, etc.).
      - Watcher-Result and queue rewrite semantics (re-read before write, `queue_failed` tagging).
      - Task-Queue modes (TASK-ROADMAP, TASK-COMPLETE, ADD-ROADMAP-ITEM, EXPAND-ROAD, REORDER-ROADMAP, DUPLICATE-ROADMAP, MERGE-ROADMAPS, EXPORT-ROADMAP, PROGRESS-REPORT) as a second entrypoint on `Task-Queue.md`.
    - Move this logic into a single new context rule file `agents/queue.mdc` that:
      - Has `alwaysApply: false` and `globs: []` (queue-triggered only).
      - Clearly declares in its header that it is the **Queue/Dispatcher Subagent**, responsible for both `.technical/prompt-queue.jsonl` and `3-Resources/Task-Queue.md`.
      - Maintains all existing safety gates (backups, snapshots, confidence bands, exclusions) by depending on the shared always rules.
- **3. Wire dispatcher to Queue/Dispatcher subagent**
  - Update the routing description (and, where needed, any explicit references) so that:
    - `EAT-QUEUE` / `Process queue` / `EAT-CACHE` triggers → Queue/Dispatcher subagent (agents/queue.mdc) using the prompt-queue source.
    - `PROCESS TASK QUEUE` triggers → Queue/Dispatcher subagent with Task-Queue source.
    - Other mode phrases (INGEST MODE, DISTILL MODE, EXPRESS MODE, ARCHIVE MODE, ORGANIZE MODE, roadmap modes, etc.) still map directly to their existing context rules (`auto-distill.mdc`, `auto-express.mdc`, `auto-archive.mdc`, `auto-organize.mdc`, `auto-roadmap.mdc`, ingest rules), unchanged in this phase.
  - Keep `system-funnels.mdc` as the high-level documentation of which triggers map to which context rules, but conceptually treat Queue/Dispatcher as one of those context rules (subagent) instead of having its logic scattered.
- **4. Maintain and document safety contracts**
  - Ensure the Queue/Dispatcher subagent explicitly calls out that it does not change:
    - The **Error Handling Protocol** (`core-guardrails.mdc` + `mcp-obsidian-integration.mdc`).
    - Confidence bands and refinement loops (`confidence-loops.mdc`).
    - Guidance-aware behavior (`guidance-aware.mdc`).
    - Watcher-Result formatting and semantics (`watcher-result-append.mdc`).
  - In `agents/queue.mdc`, add a short "Safety" section that states all destructive operations still occur in the downstream pipelines; this subagent only orchestrates which pipeline runs when.
- **5. Update backbone docs and sync mirror**
  - In `3-Resources/Second-Brain/`:
    - Update `Queue-Sources.md` to mention the Queue/Dispatcher subagent as the single entrypoint for both prompt and task queues, and explicitly note that it calls the existing pipelines unchanged.
    - Update `Cursor-Skill-Pipelines-Reference.md` to:
      - Add a small section under "System-level" or "Queue funnels" describing the Queue/Dispatcher subagent and how it interacts with pipelines.
      - Clarify that system-funnels/dispatcher is now a thin routing layer.
  - Under `.cursor/sync/`:
    - Add or update sync copies for any new/renamed rules (e.g. `rules/agents/queue.md`) to mirror `agents/queue.mdc`, per `backbone-docs-sync.mdc`.
- **6. Validation and rollback strategy**
  - **Unit-style manual tests** (no code changes required, just usage):
    - With a test `.technical/prompt-queue.jsonl` containing a few entries (INGEST MODE, RESUME-ROADMAP, DISTILL MODE), run `EAT-QUEUE` and confirm:
      - Entries are parsed, ordered, and dispatched to the same pipelines as before.
      - `Watcher-Result.md` lines still match the existing format and status semantics.
      - Successful entries are cleared and failed entries are written back with `queue_failed: true`.
    - With a populated `3-Resources/Task-Queue.md`, run `PROCESS TASK QUEUE` and verify each mode (especially TASK-COMPLETE and ADD-ROADMAP-ITEM) behaves identically.
    - Confirm that wrappers are still processed first via the Step 0 semantics, and that `CHECK_WRAPPERS` requeue behavior is unchanged.
  - **Rollback**:
    - Keep the original `auto-eat-queue.mdc` and `auto-queue-processor.mdc` around (or gated behind a feature flag in comments) until the new Queue/Dispatcher subagent has been manually exercised on sample queues.
    - If any issue surfaces, you can temporarily revert routing in `system-funnels.mdc` back to the original context rules while you adjust `agents/queue.mdc`.

