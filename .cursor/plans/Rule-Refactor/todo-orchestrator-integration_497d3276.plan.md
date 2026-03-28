---
name: todo-orchestrator-integration
overview: Introduce a shared todo-orchestrator skill and integrate it into key agents so multi-step runs track progress explicitly and avoid premature returns.
todos:
  - id: design-skill-api
    content: Define the todo-orchestrator skill API, invariants, and mapping onto Cursor TodoWrite.
    status: completed
  - id: implement-skill
    content: Implement the todo-orchestrator SKILL.md and internal logic.
    status: completed
  - id: integrate-queue-agent
    content: Pilot integration of the todo-orchestrator into the queue/dispatcher agent with concrete phases and guards.
    status: completed
  - id: integrate-roadmap-ingest
    content: Integrate the todo-orchestrator into roadmap and ingest agents using agent-specific phase lists.
    status: completed
  - id: integrate-archive-express-distill
    content: Extend todo-orchestrator usage to archive/organize and distill/express agents.
    status: completed
  - id: test-and-doc
    content: Add tests/scenarios and documentation for todo-orchestrator usage across agents.
    status: completed
isProject: false
---

# Todo-Orchestrator Skill & Agent Integration

### Goals

- **Create a shared todo-orchestrator skill** that encapsulates dynamic todo creation, status updates, and completion checks.
- **Integrate the skill into key agents** (queue/dispatcher, roadmap, ingest, archive/organize, distill/express) so they use todos as an explicit completion contract.

### 1. Analyze current behavior and touchpoints

- **Review existing todo usage** (if any) and how the Cursor `TodoWrite` mechanism is currently (or not yet) used.
- **Identify target agents** that commonly return early or have multi-step flows: queue/dispatcher, roadmap, ingest, archive/organize, distill, express.
- **Sketch phase boundaries** for each agent (e.g. for queue: parse queue → dispatch entries → write Watcher-Result → cleanup).

### 2. Design the shared todo-orchestrator skill

- **Choose skill location** (e.g. `.cursor/skills/todo-orchestrator/SKILL.md`) and define its purpose and guarantees.
- **Design a minimal API** around Cursor todos, for example:
  - `init_todos(task_name, phases[]) -> { todo_ids }`
  - `set_todo_status(id, status)` where status ∈ {pending, in_progress, completed, cancelled}
  - `get_open_todos() -> []` and `all_resolved() -> bool`.
- **Define invariants and policies**:
  - Only one todo in `in_progress` at a time.
  - For any non-trivial run, at least one todo set must exist.
  - Before an agent finishes, either all todos are `completed` or explicitly `cancelled` with a short reason.
- **Specify mapping to `TodoWrite`**: how the skill will actually call `TodoWrite` under the hood, including id conventions and merge behavior.

### 3. Implement the todo-orchestrator skill

- **Write the SKILL.md** describing:
  - Intent, API, and example usage per agent.
  - How it enforces early-return guardrails using `all_resolved()`.
- **Implement the internal logic** so that:
  - Todo IDs are stable and human-readable (e.g. `queue-parse`, `queue-dispatch`).
  - The skill can be called multiple times in a run without duplicating todos.
  - Status transitions are validated (e.g. can’t go from completed back to in_progress).

### 4. Integrate into queue/dispatcher agent as pilot

- **Locate the queue/dispatcher agent definition** (e.g. an agent rule under `.cursor/rules/agents/queue.mdc`).
- **Add a call to the todo-orchestrator at run start**, creating a small, ordered todo set like:
  - `parse-queue`
  - `dispatch-entries`
  - `write-watcher-result`
  - `rewrite-queue/cleanup`.
- **Instrument key phases** to update todo state:
  - Mark `parse-queue` as `completed` only after parse/validation succeeds.
  - Mark `dispatch-entries` as `completed` only after all entries have been handed off to subagents.
  - Mark `write-watcher-result` as `completed` only after lines are written or errors logged.
- **Add a final guardrail call** to `all_resolved()` (or equivalent) before the agent returns; if not resolved, either perform remaining work or mark remaining todos `cancelled` with a clear reason.

### 5. Extend integration to roadmap and ingest agents

- **Roadmap agent**:
  - Define roadmap-specific phases (e.g. `load-state`, `determine-action`, `apply-action`, `snapshot-and-update-state`, `queue-followup-if-needed`).
  - Wire those phases through the todo-orchestrator in the same pattern as the queue agent.
- **Ingest agent**:
  - Define ingest phases (e.g. `ensure-backup`, `classify-para`, `frontmatter-enrich`, `organize/move`, `distill/highlight`, `log-actions`).
  - Integrate todo creation and status updates so ingest runs don’t stop mid-pipeline without reflecting it in todos.

### 6. Integrate into archive/organize and distill/express agents

- **Archive/organize**:
  - Identify core phases (e.g. `select-candidates`, `archive-check`, `snapshot`, `move-notes`, `ghost-folder-sweep`, `log-actions`).
  - Use the orchestrator so a run that only partially moves notes still reflects unresolved work instead of silently returning.
- **Distill/express**:
  - Define phases around `read-note`, `analyze/auto-layer-select`, `apply-distill/express`, `decorate/highlight`, `write-back`, `log-actions`.
  - Ensure todos are used to guard against returns after analysis but before write-back or logging.

### 7. Testing, validation, and tuning

- **Create a small set of test scenarios** for each agent:
  - Happy-path multi-step runs where all phases are expected to complete.
  - Early-failure paths where a phase fails and remaining todos should be `cancelled` with reasons.
- **Verify that**:
  - Todos are created only for non-trivial runs and stay small/legible.
  - Agents do not return with unresolved todos unless they are explicitly marked `cancelled`.
  - Error and logging behavior remains compatible with existing `Watcher-Result` and `Errors` conventions.
- **Iterate on phase definitions** per agent if todos feel too coarse or too granular in practice.

### 8. Documentation and future evolution

- **Document the todo-orchestrator skill** in your internal docs (e.g. how to call it from new agents/rules).
- **Add short examples** to at least one agent rule file showing idiomatic usage.
- **Note future extensions**, such as linking todos to specific queue entries or notes, or surfacing them in a dedicated status view.

