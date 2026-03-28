---
name: agent-subagents-refactor
overview: Refactor the existing monolithic Second-Brain Cursor agent into a modular RoadmapSubagent, wired through a minimal dispatcher, without breaking current workflows.
todos:
  - id: survey-roadmap-rules
    content: Survey existing roadmap-related rules and skills, and list their current triggers, inputs, and outputs.
    status: pending
  - id: define-roadmap-subagent-contract
    content: Define the RoadmapSubagent contract, including actions, state ownership, and invariants, and sketch its internal action dispatcher.
    status: pending
  - id: design-dispatcher-routing
    content: Design how the top-level dispatcher and auto-eat-queue will route roadmap modes into the RoadmapSubagent, reusing shared guardrails.
    status: pending
  - id: plan-extraction-of-roadmap-logic
    content: Plan how to factor roadmap logic out of monolithic rules (auto-eat-queue, auto-roadmap) into the RoadmapSubagent without behavior regressions.
    status: pending
  - id: update-backbone-docs-and-queue-sources
    content: Plan the necessary documentation and sync updates (Backbone, Pipelines, Queue-Sources, .cursor/sync) to reflect the new RoadmapSubagent.
    status: pending
  - id: prepare-rollout-and-test-checklist
    content: Outline an incremental rollout strategy and a regression test checklist for all roadmap modes and actions.
    status: pending
isProject: false
---

## RoadmapSubagent Refactor Plan

### 1. Clarify scope and current behavior

- **Goal**: Capture exactly what the current roadmap-related rules/skills do so we don’t regress behavior.
- **Identify rules**: Review roadmap-related context rules under `.cursor/rules/context/` such as `auto-roadmap.mdc`, `auto-eat-queue.mdc` (roadmap portions), and any roadmap-specific context rules (resume, deepen, audit, revert, hand-off, phase-output-sync).
- **Identify skills**: Review roadmap-related skills in `.cursor/skills/` including `roadmap-generate-from-outline`, `roadmap-resume`, `roadmap-deepen`, `roadmap-advance-phase`, `roadmap-audit`, `roadmap-revert`, `roadmap-phase-output-sync`, `hand-off-audit`, and any roadmap-ingest helpers.
- **Trace triggers**: From `[3-Resources/Second-Brain/Queue-Sources.md](3-Resources/Second-Brain/Queue-Sources.md)` and `[.cursor/rules/always/system-funnels.mdc](.cursor/rules/always/system-funnels.mdc)`, list the modes and phrases that currently route into roadmap behavior (e.g. `ROADMAP MODE`, `RESUME-ROADMAP`, `RECAL-ROAD`, `REVERT-PHASE`, `SYNC-PHASE-OUTPUTS`, `HANDOFF-AUDIT`, `EXPAND-ROAD`, etc.).

### 2. Design the RoadmapSubagent surface and responsibilities

- **Define subagent contract**: Draft a short contract in a new context rule (conceptually `agents/roadmap.mdc`) describing inputs (queue `mode`, `params`, `source_file`, roadmap state notes), outputs (updated notes, new roadmap notes, queue entries), and invariants (state integrity, snapshots, confidence bands).
- **Map actions to skills**: For each roadmap action (`deepen`, `advance-phase`, `recal`, `revert-phase`, `sync-outputs`, `handoff-audit`, `expand`), assign one primary skill as the executor, using existing skills where possible.
- **State ownership**: Explicitly declare that RoadmapSubagent is the only component allowed to mutate `roadmap-state.md`, `workflow_state.md`, and phase roadmap notes, while still honoring global guardrails from `core-guardrails.mdc` and `mcp-obsidian-integration.mdc`.

### 3. Introduce a minimal dispatcher entry for roadmap modes

- **Dispatcher responsibilities**: Conceptually extend the dispatcher (from `system-funnels.mdc` / `auto-eat-queue.mdc`) so that when it sees a roadmap-related `mode` (`ROADMAP MODE`, `RESUME-ROADMAP`, `RECAL-ROAD`, `REVERT-PHASE`, `SYNC-PHASE-OUTPUTS`, `HANDOFF-AUDIT`, `EXPAND-ROAD`), it routes into the RoadmapSubagent instead of inlining roadmap logic.
- **Shared core layer**: Ensure the dispatcher and RoadmapSubagent both rely on the existing always rules (`core-guardrails.mdc`, `confidence-loops.mdc`, `guidance-aware.mdc`, `mcp-obsidian-integration.mdc`, `watcher-result-append.mdc`, `backbone-docs-sync.mdc`) rather than duplicating safety logic.
- **Routing sketch**: Document the routing table in `Queue-Sources.md` (or an adjacent design note) so each roadmap `mode` and `params.action` maps clearly to a RoadmapSubagent action.

### 4. Factor roadmap logic out of existing monolithic rules

- **Extract from auto-eat-queue**: In the design, isolate the roadmap-specific branches from `auto-eat-queue.mdc` (e.g. `RESUME-ROADMAP` handling, stale-removal rules, roadmap-related wrapper handling) into conceptual handlers that will move into the RoadmapSubagent.
- **Extract from auto-roadmap**: Separate initial roadmap setup (`ROADMAP MODE`) from resume/deepen behavior into explicit actions that belong to the new subagent.
- **Centralize state checks**: Consolidate scattered roadmap state checks into a single place in the RoadmapSubagent (e.g. validating `roadmap-state.md`, enforcing phase ordering, snapshot-before-update) so they’re not duplicated across multiple rules.

### 5. Define the RoadmapSubagent internal flow

- **Action dispatcher**: Within the RoadmapSubagent design, define a small internal dispatcher that takes normalized `{ mode, params }` and calls the appropriate skill (`roadmap-generate-from-outline`, `roadmap-deepen`, `roadmap-advance-phase`, etc.).
- **Error and safety handling**: Specify that, for all roadmap actions, the subagent must:
  - Validate roadmap state and config before mutating.
  - Create per-change snapshots for any destructive updates (using the `obsidian-snapshot` skill).
  - Respect confidence bands and only advance phases or rewrite notes when in the high band, falling back to Decision Wrappers when confidence is low or mid.
  - Log errors to `3-Resources/Errors.md` and append Watcher-Result lines per existing protocol.

### 6. Update documentation and sync layer

- **Backbone docs**: Update or extend `[3-Resources/Second-Brain/Backbone.md](3-Resources/Second-Brain/Backbone.md)` and `[3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference.md](3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference.md)` to describe the new RoadmapSubagent, its responsibilities, and how it interacts with the dispatcher and queue processor.
- **Queue-Sources**: Adjust `[3-Resources/Second-Brain/Queue-Sources.md](3-Resources/Second-Brain/Queue-Sources.md)` to reflect that roadmap modes are handled by the RoadmapSubagent rather than monolithic rules, including any updated mode → action mapping.
- **Sync copies**: Plan corresponding updates for `.cursor/sync/rules/context/`* and `.cursor/sync/skills/`* once the new subagent and refactored rules are implemented, keeping the sync folder aligned with `.cursor/rules/` and `.cursor/skills/`.

### 7. Plan incremental rollout and validation

- **Phase 1 (design-only)**: Keep existing behavior in place while designing the RoadmapSubagent and dispatcher changes on paper (and in design notes), ensuring all modes and edge cases are accounted for.
- **Phase 2 (shadow routing in future work)**: When you’re ready to implement, introduce the new RoadmapSubagent alongside the existing logic, initially guarded by a feature flag or limited scope (e.g. a specific project or mode) to validate behavior safely.
- **Regression checklist**: Prepare a concise test checklist for roadmap flows (initial ROADMAP MODE setup, single RESUME-ROADMAP deepen step, RECAL-ROAD audit, REVERT-PHASE, handoff-audit, phase-output-sync), so that once implementation happens you can verify the refactor didn’t break critical workflows.

