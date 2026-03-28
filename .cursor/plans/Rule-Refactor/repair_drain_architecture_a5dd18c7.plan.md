---
name: Repair drain architecture
overview: Single Task(queue); Layer 1 runs forward-then-repair phases with Option 1 + Option 3 combined, hard-block stall skip callouts on queue lines, and internal todo-orchestrator phases (initial + cleanup).
todos:
  - id: pick-routing
    content: "Chosen: Layer 1 forward-then-repair inside single Task(queue); Layer 0 unchanged (one call)."
    status: completed
  - id: resolve-repair-first-tension
    content: "Resolved: Option 1 + Option 3 + stall/skip mods (see plan body)."
    status: completed
  - id: spec-touchpoints
    content: Implement in queue.mdc A.4/A.5 + Todo orchestration, agents/queue.md, Queue-Sources.md, Second-Brain-Config, Parameters; sync .cursor/sync; dispatcher unchanged.
    status: completed
  - id: document-skip-fields
    content: Queue-Sources + MCP-Tools queue JSONL contract for explicit skip-if-stall / queue_agent_may_skip fields and interaction with hard_block + repair loop outcomes.
    status: completed
  - id: observability-spec
    content: Extend plan implementation to Logs.md / Queue-Audit-Log-Spec / Watcher-Result contract for phase tags, skip/stal events, multi-dispatch per eat_queue_run_id.
    status: completed
isProject: false
---

# Repair churn vs true work: routing options

## Decided pivot (operator + contract)

**Fair to pivot away from Layer 0 chaining two `Task(queue)` calls.** Keep [dispatcher.mdc](.cursor/rules/always/dispatcher.mdc) as-is: Layer 0 still invokes **one** `Task(queue)` per EAT-QUEUE.

**Instead, extend the Queue subagent (Layer 1)** so one pass does:

1. **Phase A — true / forward slot:** For each `project_id` (and subject to caps you add in config), dispatch **one** roadmap entry that is **not** classified as repair backlog (no `queue_priority: "repair"`, no `validator_repair_followup: true`, and any other repair flags you standardize). This is the “single true entry” the operator cares about for momentum.
2. **Phase B — leftovers / repair drain:** Then dispatch **repair-class** lines for the same project(s), up to a **separate cap** (`max_repair_dispatches_per_project_per_run` or shared budget), **sequentially**, with **state re-read + resolver refresh + preflight** between roadmap dispatches (same safety as multi-dispatch).

Layer 1 returns to Layer 0 **once** after A.7 rewrite and Watcher-Result for everything it ran in that pass.

**Why this matches your intent:** Repair is not neglected (it runs in the same gesture), but the **orchestration story** is “forward first, then clear the repair tail,” without hiding repair-only intent behind a second user phrase and without dispatcher contract friction.

## Resolved: Option 1 + Option 3 + stall/skip mods (no Option 2)

**Combo policy:**

- **Option 3 (config):** `queue.roadmap_pass_order` with values such as `repair_first` | `forward_first`. Default `**repair_first`** preserves today’s A.4 mental model for existing vaults; your workflow sets `**forward_first`** for forward-then-repair.
- **Option 1 (blocking exception):** When `roadmap_pass_order` is `**forward_first`**, **still** allow a **pre-phase-A** repair dispatch when Layer 1 classifies at least one queued line for that `project_id` as **hard-blocking repair** (narrow definition in spec: e.g. resolver / entry / post–little-val outcome indicates incoherence, state_hygiene_failure, nested_attestation_failure, or other codes you list as **blocking** — not advisory conceptual codes). At most **one** such repair dispatch before the forward slot for that project (unless caps say otherwise), then Phase A, then Phase B.

**Mods — hard blocks, stall, and explicit skip:**

- **Stall behavior:** When a **hard block** persists after one or more repair dispatches in the same pass (or across runs — define whether stall is per-pass only or durable via `queue_failed` / continuation), the queue must not infinite-loop on the same line.
- **Explicit producer callout:** Queue JSONL entries may carry a **machine-readable** flag (exact key TBD in Queue-Sources / MCP-Tools, e.g. `queue_agent_may_skip_if_stall: true` or `skip_policy: hard_block_stall`) meaning: **Layer 1 is allowed to skip dispatching this line** (leave it on disk or mark with a non-terminal skip outcome) when **stall conditions** are met (spec: e.g. hard block still present after configured repair attempts, or validator returns same primary_code twice — tie to existing `queue_next` / A.5c semantics without inventing silent drops).
- **Without** that flag, default remains: do not skip silently; use existing failure / `queue_failed` / Watcher-Result / Errors paths per current rules.

Document in **Queue-Sources** and queue payload contract so producers (Layer 1 append, crafter, Commander) set the flag only when the human accepts “this line may be bypassed if repair cannot clear it.”

## Internal Layer 1 run todos (todo-orchestrator)

Extend Queue subagent orchestration so the **same EAT-QUEUE run** uses **explicit phases** as `TodoWrite` (or equivalent) tasks, not only the existing high-level queue todos:


| Phase id (suggested)  | Role                                                                                                                                                                                     |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `queue-phase-initial` | Step 0 wrappers, read/parse/validate/dedup/order, build dispatchability map, **Phase A forward** dispatches (and optional Option-1 blocking repair before forward when `forward_first`). |
| `queue-phase-cleanup` | **Phase B repair drain**, follow-up append handling, post–little-val / A.5b–A.5c as they apply, A.6 Watcher-Result, A.7 rewrite, audit/continuation hooks.                               |


Rules:

- At most one phase `in_progress` at a time; mark `completed` or `cancelled` with reason before return.
- Subagent **must not** return Success while either phase is `pending` or `in_progress` (align with existing [queue.mdc](.cursor/rules/agents/queue.mdc) todo-orchestration intro; this refines **what** the phases are).

Optional: keep existing coarse todos (`parse-queue`, `dispatch-entries`, …) **or** fold them under `initial` / `cleanup` — spec should pick one tree to avoid duplicate todo noise.

## Logs, telemetry, and tracking (must be specified with behavior)

Previously the plan focused on dispatch ordering; **observability** needs explicit rules so multi-phase / multi-dispatch / skip does not break parsing or hide outcomes.

### Watcher-Result ([watcher-result-append.mdc](.cursor/rules/always/watcher-result-append.mdc))

- **One line per queue entry disposition** remains the baseline (success / failure / skip).
- **Extend** `message` or `trace` with machine-parseable tags where useful, e.g. `queue_pass_phase: initial|cleanup`, `dispatch_ordinal: N`, `roadmap_pass_order: forward_first|repair_first`, so operators and scripts can tell forward vs repair drain without guessing.
- **Stall-skip:** When Layer 1 skips a line under explicit callout + stall rules, emit a line with `status: success` or a dedicated `status: skipped` only if the Watcher contract is extended in spec; **otherwise** use `success` with `message` prefix like `skipped: hard_block_stall` and full rationale in `trace` (avoid breaking the plugin parser — confirm `status` enum before adding a new value).

### Prompt-queue audit ([Queue-Audit-Log-Spec.md](3-Resources/Second-Brain/Docs/Queue-Audit-Log-Spec.md), A.5g)

- Reuse single `**eat_queue_run_id`** for the whole EAT-QUEUE pass (initial + cleanup).
- `**line_removed` / `line_appended`:** Multiple per run is already expected; add optional `**queue_pass_phase`** and `**disposition`**: values such as `skipped_stall_explicit`, `consumed_forward_slot`, `consumed_repair_drain` so audit graphs stay truthful.
- **Skip without dispatch:** If a line is skipped without `Task`, still append audit row (or Feedback-Log) so the line is not “invisible.”

### Queue continuation ([Queue-Continuation-Spec.md](3-Resources/Second-Brain/Docs/Queue-Continuation-Spec.md), A.5e)

- **One continuation row per dispositioned roadmap entry** (unchanged count logic: more dispatches ⇒ more rows when applicable).
- For **stall-skip**, set `**suppress_reason`** / `**rationale_short`** (and `**continuation_eligible`**) per a small enum addition (e.g. `explicit_skip_stall`) — document so empty-queue bootstrap does not mis-fire on skipped lines.

### Task hand-off comms ([Task-Handoff-Comms-Spec](3-Resources/Second-Brain/Docs/Task-Handoff-Comms-Spec.md))

- **One `handoff_out` / `return_in` pair per `Task`** still; Phase A + Phase B mean **more pairs per single Layer 0 trigger** — no contract change, but **volume** increases; ensure `**task_correlation_id`** remains unique per Task.

### Run-Telemetry and dispatch ledger ([Logs.md](3-Resources/Second-Brain/Logs.md), queue.mdc A.5)

- **Pipeline** Run-Telemetry notes: unchanged per `Task(roadmap|…)`; ensure `**queue_entry_id`** and `**parent_run_id`** tie back to the same `**eat_queue_run_id`** in the **Queue** subagent Run-Telemetry note (if present).
- `**dispatch_ledger`:** Append in **global ordinal order** across initial + cleanup (not reset at phase boundary) so a single pass has a linear timeline.

### Errors.md / Feedback-Log

- **Stall-skip** and **blocking-repair exception** paths should log structured entries when policy fires (`error_type` or tag TBD, e.g. `queue_line_skipped_stall`, `queue_blocking_repair_preflight`) — severity usually **low** for explicit skip, **medium** for unexpected stall without skip flag.

### Docs to update in the same implementation pass

- [Logs.md](3-Resources/Second-Brain/Logs.md) — Run-Telemetry / Watcher-Result expectations for multi-phase queue runs.
- [Queue-Audit-Log-Spec.md](3-Resources/Second-Brain/Docs/Queue-Audit-Log-Spec.md) — optional new fields / disposition enum.
- [Queue-Sources.md](3-Resources/Second-Brain/Queue-Sources.md) — cross-link observability behavior next to dispatch rules.

## Previously considered (retained for context)

### Second `Task(queue)` from Layer 0

Avoided: requires dispatcher change and splits orchestration across layers.

### Repair-only second user trigger

Optional later: **EAT-QUEUE REPAIR** still useful for “I only want churn” without running phase A.

### Separate `prompt-queue-repair.jsonl`

Still **out of scope** unless repair volume forces it.

## Implementation touchpoints (when executing)

- [queue.mdc](.cursor/rules/agents/queue.mdc): A.4 dispatchability map, ordering, Option 1 + 3; A.5 two-phase dispatch; stall/skip semantics; **Todo orchestration** section updated with `queue-phase-initial` / `queue-phase-cleanup`.
- [.cursor/agents/queue.md](.cursor/agents/queue.md): Same phase + policy summary for the agent prompt.
- [Queue-Sources.md](3-Resources/Second-Brain/Queue-Sources.md): `roadmap_pass_order`, caps, repair vs forward classification, **skip / stall** JSON fields and when Layer 1 may omit Task for a line.
- [Second-Brain-Config.md](3-Resources/Second-Brain-Config.md): Defaults for `roadmap_pass_order`, repair caps, optional stall thresholds.
- [MCP-Tools.md](3-Resources/Second-Brain/MCP-Tools.md) (or Queue-Sources queue JSONL section): Payload keys for skip callouts.
- [Parameters.md](3-Resources/Second-Brain/Parameters.md): Cross-link if summarized.
- [Logs.md](3-Resources/Second-Brain/Logs.md), [Queue-Audit-Log-Spec.md](3-Resources/Second-Brain/Docs/Queue-Audit-Log-Spec.md), [Queue-Continuation-Spec.md](3-Resources/Second-Brain/Docs/Queue-Continuation-Spec.md): phase tags, skip/stall dispositions, continuation eligibility for skips (see **Logs, telemetry, and tracking** above).
- **No** [dispatcher.mdc](.cursor/rules/always/dispatcher.mdc) change for this pivot.
- [.cursor/sync](.cursor/sync) per backbone-docs-sync.

## Summary


| Topic             | Decision                                                                                                                                                             |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Pass order        | **Config** `repair_first` (default) vs `forward_first`; **plus** blocking-repair exception before forward when `forward_first`.                                      |
| Hard-block stall  | Repair loop may **fail to clear**; lines with **explicit** “queue agent may skip” callout can be **skipped** under defined stall rules; no silent skip without flag. |
| Layer 1 structure | **Internal todos:** `queue-phase-initial` + `queue-phase-cleanup` (todo-orchestrator).                                                                               |
| Dispatcher        | Unchanged (single `Task(queue)`).                                                                                                                                    |
| Logs / telem      | **Accounted in plan:** Watcher-Result tags, audit `disposition` / phase, continuation rows for skips, dispatch_ledger ordinal, Errors/Feedback for stall paths.      |


