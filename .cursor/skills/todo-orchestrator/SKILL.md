---
name: todo-orchestrator
description: Shared helper for dynamic, per-run todos across subagents. Provides a consistent way to declare phases, update statuses, and assert that no work-in-progress todos remain before returning.
---

# todo-orchestrator

## When to use

- Use this skill in **any multi-step subagent** (queue, roadmap, ingest, archive, organize, distill, express, research, validator) where:
  - The pipeline has **3 or more distinct phases**, and
  - Returning early while some phases are silently skipped would be harmful.
- **Do not** use it for:
  - Truly trivial, single-step runs (e.g. one read-only validation, a single log update).
  - Flows where the subagent is already fully atomic and cannot legally exit mid-way.

The goal is to make “what this run intends to do” explicit as a **small todo set**, and to require that the subagent either:

- completes all todos successfully, **or**
- explicitly cancels remaining todos with a short reason before returning.

## Conceptual model

- A **todo set** represents **one run of one subagent** (e.g. “this EAT-QUEUE pass”, “this RESUME_ROADMAP action”, “this INGEST batch on Ingest/”).
- Each todo in the set corresponds to a **pipeline phase**, not micro-steps.
- The orchestrator is **stateless across runs**; it only cares about:
  - The current run’s todo IDs, labels, and statuses.
  - The invariant that at most **one todo** is `in_progress` at a time.

Under the hood, the actual storage and updates are implemented via Cursor’s `TodoWrite` tool; this skill defines a **convention and contract** so all subagents behave consistently.

### Helper contracts vs todos

- Todos cover **run-level phases** (parse, dispatch, apply-action, nested-helpers, logging, rewrite), **not** individual nested helper calls.
- Enforcement that a helper **must be called** (e.g. roadmap’s nested `Task(validator)` / `Task(internal-repair-agent)` / `Task(research)`, or Layer 1’s Task dispatch to pipelines) lives in:
  - [[3-Resources/Second-Brain/Subagent-Safety-Contract|Subagent-Safety-Contract]] § Task-`attempt-before-skip` and nested helper rules,
  - [[3-Resources/Second-Brain/Docs/Nested-Subagent-Ledger-Spec|Nested-Subagent-Ledger-Spec]] (attestation invariants for `nested_subagent_ledger`),
  - [[3-Resources/Second-Brain/Docs/Task-Handoff-Comms-Spec|Task-Handoff-Comms-Spec]] (Task launch and return logging).
- This skill’s job is to make sure **phases** are either completed or explicitly cancelled; helper-level guarantees come from those other contracts. In some pipelines, a dedicated `nested-helpers` phase is used to connect the two layers.

## API surface (conventions for agents)

Subagents do not call a separate MCP tool for this skill; instead they **follow this contract** and use the `TodoWrite` tool accordingly.

### 1. Initialize todos for a run

**Function shape (conceptual):**

- `init_todos(run_id, phase_ids_with_labels[])`

**Behavior:**

1. Choose a **run_id** that is:
   - Human-readable, such as `"queue-eat-queue"`, `"roadmap-resume"`, `"ingest-phase-1"`, or
   - Derived from telemetry, such as `"queue-" + queue_entry_id` when appropriate.
2. Define a **small ordered list** of phases for this run:
   - Example (Queue prompt-queue flow): `["parse-queue", "dispatch-entries", "write-watcher-result", "rewrite-queue"]`.
   - Example (Roadmap RESUME): `["load-state", "determine-action", "apply-action", "snapshot-and-log", "queue-followup-if-needed"]`.
3. For each phase, synthesize a **todo id**:
   - Convention: `"<run_id>:<phase_id>"` (e.g. `"queue-eat-queue:parse-queue"`).
   - Label: short, imperative description (e.g. `"Parse and validate prompt queue"`).
4. Use `TodoWrite` with `merge: true` to create or refresh these todos for the current run:
   - New todos start as `pending`.
   - If a todo with the same id already exists from a previous partial run, you MAY:
     - keep its status when resuming, or
     - reset it to `pending` if you are re-running the entire run from scratch.

**Invariants:**

- A run should have **3–7 todos** at most; if you need more, you probably need a second run or a different abstraction.
- IDs must be **stable within a run** so the agent can update them deterministically.

### 2. Mark progress within a run

**Function shape (conceptual):**

- `set_todo_status(todo_id, status)`

Where `status ∈ { "pending", "in_progress", "completed", "cancelled" }`.

**Behavior:**

1. Before starting work on a phase:
   - Set that phase’s todo to `in_progress` via `TodoWrite`.
   - Ensure **all other todos for this run are not `in_progress`** (at most one `in_progress` todo at a time).
2. After a phase completes successfully:
   - Set its todo to `completed`.
3. When a phase is being **skipped**, blocked, or aborted:
   - Set its todo to `cancelled`, and record the reason in the human-facing summary/logs for the run (e.g. Watcher-Result message, Errors.md entry, or subagent return payload).

The subagent should perform todo updates **around the existing pipeline steps**, not instead of them:

- Example (Queue prompt-queue flow):
  - Before A.1 Read queue: `parse-queue` → `in_progress`.
  - After A.2 Parse/validate succeeds or exits cleanly: `parse-queue` → `completed`.
  - Before A.5 Dispatch loop: `dispatch-entries` → `in_progress`.
  - After all entries have been dispatched (including failures): `dispatch-entries` → `completed`.
  - Similarly for `write-watcher-result` and `rewrite-queue`.

### 3. Check for unresolved todos before returning

**Function shape (conceptual):**

- `all_resolved(run_id) -> boolean`

**Behavior:**

Before the subagent returns success or failure for a run, it **must**:

1. Inspect all todos belonging to this `run_id` (by id prefix convention).
2. Determine whether every todo is either:
   - `completed`, or
   - `cancelled`.
3. If **any** todo is still `pending` or `in_progress`:
   - Either do the work necessary to complete it, **or**
   - Explicitly mark it `cancelled` with a short reason (and surface that reason in the run’s log / return payload).

The subagent **must not** silently return while there are still implicit, unaddressed todos; this is the key guardrail against premature returns.

## Mapping to Cursor TodoWrite

Subagents should apply the above using the built-in `TodoWrite` tool:

- **Create / update todos**
  - `merge: true`
  - `todos: [{ id, content, status }, …]`
- **ID convention**
  - Always include the run_id prefix to group todos logically:
    - `queue-eat-queue:parse-queue`
    - `roadmap-resume:apply-action`
    - `ingest-phase-1:distill-and-hub`
- **Content conventions**
  - Short, human-readable label, e.g. `"Dispatch prompt-queue entries via Task subagents"`.

You do **not** need a separate dedicated MCP tool; the orchestrator is a **pattern + naming convention** built on top of `TodoWrite`.

## Recommended phase sets per subagent

These are canonical starting points; subagents may refine them but should stay small and phase-oriented.

### Queue/Dispatcher (prompt-queue flow)

- `parse-queue` — read, parse, validate, dedup, and order queue entries.
- `dispatch-entries` — build hand-offs and call Task subagents (including chains); collect results **only when mandated nested-helper and validator contracts are satisfied or recorded as `task_error`** per [[.cursor/rules/agents/queue.mdc|queue.mdc]] A.5 and [[3-Resources/Second-Brain/Subagent-Safety-Contract|Subagent-Safety-Contract]] / [[3-Resources/Second-Brain/Docs/Nested-Subagent-Ledger-Spec|Nested-Subagent-Ledger-Spec]].
- `log-watcher-result` — append one Watcher-Result line per processed entry (including chain segments).
- `rewrite-queue` — clear passed entries only; write updated `.technical/prompt-queue.jsonl`.

### Queue/Dispatcher (task-queue flow)

- `read-task-queue` — read and parse `3-Resources/Task-Queue.md`.
- `dispatch-task-entries` — run the appropriate skills/modes for each entry.
- `log-and-banners` — Watcher-Result + Mobile-Pending-Actions + banner cleanup.
- `update-task-queue` — clear or mark processed entries as configured.

### RoadmapSubagent

Normative detail and invariants for roadmap todos also live in [[.cursor/rules/agents/roadmap.mdc|roadmap.mdc]] § **Todo orchestration (todo-orchestrator)**.

#### ROADMAP_MODE (setup only)

Use run_id such as `roadmap-setup`.

- `resolve-project` — resolve project_id and roadmap directory, enforce Projects-only invariants.
- `bootstrap-state` — ensure roadmap-state.md, decisions-log.md, distilled-core.md, workflow_state.md exist and are initialized correctly for Phase 0.
- `generate-from-outline` — invoke `roadmap-generate-from-outline` when appropriate and verify artifacts.

#### RESUME_ROADMAP (single continue action)

Use run_id such as `roadmap-resume`.

- `load-state` — read roadmap-state.md / workflow_state.md and derive current target/phase.
- `determine-action` — merge params with Config/profile and resolve a concrete action (including smart-dispatch when `action: "auto"`).
- `apply-action` — call the corresponding skill(s) (deepen, advance-phase, recal, revert-phase, sync-outputs, handoff-audit, resume-from-last-safe, expand, compact-depth, unfreeze_conceptual, bootstrap-execution-track).
- `nested-helpers` — run required nested helpers (pre-deepen Research, nested Validator, IRA) and ensure Task calls, Task-Handoff-Comms rows, and `nested_subagent_ledger` steps are present or recorded as `task_error` per the roadmap nested-helper contracts.
- `snapshot-and-log` — ensure state snapshots, workflow_state/roadmap-state updates, and any associated logging are complete.
- `queue-followup-if-needed` — **request** the next queue action via `queue_followups` in the return to the Queue/Dispatcher when `params.queue_next !== false` (RoadmapSubagent does not write the queue file); or explicitly no follow-up when `queue_next === false`.

### IngestSubagent

- `scan-ingest` — list Ingest contents and non-MD files.
- `handle-non-md` — run companion .md + attachment handling for non-markdown.
- `normalize-embeds` — normalize embedded images for .md in Ingest.
- `ingest-phase-1` — classify_para, frontmatter-enrich, name-enhance (propose), subfolder-organize, distill/highlight, hubs/tasks.
- `wrapper-or-direct-move` — create Decision Wrapper or perform Cursor-agent direct move when conditions allow.

### ArchiveSubagent

- `archive-check-phase` — classify PARA, run archive-check, evaluate confidence and loops.
- `snapshot-and-move` — snapshot, subfolder-organize, summary-preserve, move, resurface mark.
- `ghost-folder-sweep` — archive-ghost-folder-sweep after moves.
- `log-and-telemetry` — Archive-Log, Backup-Log, Run-Telemetry.

### OrganizeSubagent

- `classify-and-enrich` — classify_para and frontmatter-enrich.
- `path-proposal` — subfolder-organize and any mid-/low-band loops or wrappers.
- `rename-and-move` — name-enhance (when applicable), snapshot, move.
- `log-and-telemetry` — Organize-Log, Backup-Log, Run-Telemetry.

### DistillSubagent

- `prepare-and-backup` — backup, optional garden-review, and auto-layer-select.
- `distill-core` — layers, highlight color, layer-promote, perspective refine.
- `readability-and-flags` — callout-tldr-wrap, readability-flag, research_distilled flag.
- `validator-and-telemetry` — run little val + distill_readability validator, log, Run-Telemetry.

### ExpressSubagent

- `backup-and-version` — backup and version-snapshot.
- `related-and-scope` — related-content-pull / suggest_connections, research-scope when applicable.
- `outline-and-view` — express-mini-outline and express-view-layer.
- `cta-and-log` — call-to-action-append, logs, validator, Run-Telemetry.

Subagents may collapse or split phases if needed, but each todo should still map to a **single responsibility** in the pipeline.

## Guardrails and expectations

- **At most one `in_progress` todo** per run — if you start a new phase, either complete or cancel the previous one.
- **No silent exits** — before returning, always ensure all todos are `completed` or `cancelled`. If you must stop early due to an error, make that explicit in both:
  - the todo statuses (remaining todos → `cancelled`), and
  - the human-facing report (Watcher-Result, Errors.md, or equivalent).
- **Do not over-todo** — avoid creating dozens of ultra-fine-grained todos. If you find yourself needing that, revisit the phase definitions instead.

## Example (queue prompt-queue run)

1. **Initialize**:
   - run_id: `queue-eat-queue`
   - todos:
     - `queue-eat-queue:parse-queue`
     - `queue-eat-queue:dispatch-entries`
     - `queue-eat-queue:log-watcher-result`
     - `queue-eat-queue:rewrite-queue`
2. **A.1–A.2**:
   - Before reading: `parse-queue` → `in_progress`.
   - After validation (or clean early-exit): `parse-queue` → `completed`.
3. **A.5**:
   - Before dispatch loop: `dispatch-entries` → `in_progress`.
   - After all Task calls (success/failure accounted for): `dispatch-entries` → `completed`.
4. **A.6–A.7**:
   - Before Watcher-Result pass: `log-watcher-result` → `in_progress`; after: `completed`.
   - Before rewrite pass: `rewrite-queue` → `in_progress`; after: `completed`.
5. **Before return**:
   - If any todo is not `completed`:
     - Do the remaining phase, **or**
     - Mark todo `cancelled` with a reason and surface that in the run’s summary.

This pattern, applied consistently across subagents, should materially reduce premature returns and make partial runs observable instead of implicit.

