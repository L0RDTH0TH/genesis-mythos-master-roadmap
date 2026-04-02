---
name: dynamic-roadmap-helper-enforcement
overview: Make roadmap deepen runs dynamically enforce nested helpers and follow-up queue contracts so late-phase conceptual steps cannot silently skip validators/research or drop queue_next follow-ups.
todos:
  - id: inspect-roadmap-agent-and-queue-dispatcher
    content: Inspect roadmap agent helper-selection logic and queue dispatcher RESUME_ROADMAP handling.
    status: completed
  - id: design-dynamic-helper-selection-policy
    content: Design a dynamic helper-selection policy for roadmap deepens based on phase, context utilization, drift, and gate signals.
    status: completed
  - id: implement-helper-graph-and-task-harden-wiring
    content: Implement dynamic helper graph in roadmap agent and ensure selected helpers are mandatory via Task harden.
    status: completed
  - id: tighten-queue-next-enforcement
    content: Adjust queue dispatcher to enforce RESUME_ROADMAP queue_next follow-up presence or mark violations.
    status: completed
  - id: wire-config-signals-and-update-docs
    content: Wire config-driven signals into helper selection and update Second-Brain documentation and sync copies.
    status: completed
isProject: false
---

### Goal

Align RESUME_ROADMAP deepen behavior with the Subagent Safety Contract and Second-Brain-Config so that:

- Nested helpers (validator, IRA, research) are **selected dynamically** based on phase/tech-level, context utilization, drift, and gate streaks.
- Once selected, helpers are **mandatory**: Task must be attempted or the run cannot claim Success.
- RESUME_ROADMAP runs that declare `queue_next: true` cannot finish with a clean Success while leaving the prompt queue empty for that project.

### Step 1: Inspect current roadmap helper selection and queue-next handling

- **Read** the roadmap agent definition file (e.g. `[.cursor/agents/roadmap.md](.cursor/agents/roadmap.md)` or its `.mdc` legacy if present) to see:
  - How it decides when to call nested validator, IRA, or research for conceptual deepens.
  - What metadata it writes into its `queue_followups` / `queue_next` fields.
- **Read** the queue dispatcher rule `[.cursor/rules/agents/queue.mdc](.cursor/rules/agents/queue.mdc)` sections that handle:
  - RESUME_ROADMAP dispatch under `pipeline_mode: balance`.
  - `synthesize_followup_when_queue_next_true` and `assert_followup_presence_after_resume_success` behavior.
- **Inspect** recent entries in `[.technical/task-handoff-comms.jsonl](.technical/task-handoff-comms.jsonl)` around the `pipeline_task_correlation_id` from the 5.2 deepen row in `workflow_state.md` to verify which helpers (if any) were actually invoked.

### Step 2: Design dynamic helper selection policy for roadmap deepens

- Define a small, explicit **helper-selection function** (conceptual, then implemented inside the roadmap agent) that takes as inputs:
  - `phase_number` / tech level (1–5+),
  - `current_subphase_index`,
  - context utilization vs `roadmap.prompt_defaults.roadmap.context_util_threshold`,
  - drift / gate streak / same-subphase streak signals available from `workflow_state` / state.
- For each combination of these signals, decide which helpers become **selected (and thus mandatory)** under `pipeline_mode: balance`, e.g.:
  - Early phases, low util → minimal helpers.
  - Late phases (5+), high util or near pseudo-code depth → nested validator + possible research always selected.
  - Repeated same-subphase with low structural delta → escalate to validator + IRA.
- Document this mapping back into `3-Resources/Second-Brain/Docs/Pipeline-Validator-Profiles.md` (or equivalent doc) so the behavior is explicit.

### Step 3: Implement dynamic helper graph inside roadmap agent

- In the roadmap agent implementation file, introduce a **helper-graph builder** that:
  - Reads `pipeline_mode` and `validator_profiles` from `Second-Brain-Config`.
  - Applies the dynamic helper-selection policy from Step 2 to mark each helper as selected/not-selected for the current deepen run.
- Ensure that for any helper marked **selected**:
  - The roadmap subagent routes its call through the **Task harden pass** with `desired_subagent_type` set appropriately (`validator`, `research`, `internal-repair-agent`).
  - It records `task_tool_invoked: true` or `outcome: task_error` in its nested ledger when the Task call is attempted.
  - A missing or failed helper prevents the roadmap run from returning `Success` with `little_val_ok: true`.

### Step 4: Tighten queue_next follow-up enforcement for RESUME_ROADMAP

- In the queue dispatcher rule, locate the code path that handles:
  - RESUME_ROADMAP entries with `queue_next !== false`.
  - `synthesize_followup_when_queue_next_true` and `assert_followup_presence_after_resume_success`.
- Adjust logic so that after a **successful** RESUME_ROADMAP run:
  - The dispatcher explicitly checks the current queue contents for a same-project RESUME_ROADMAP follow-up.
  - If none exists and `queue_next !== false`, it **must** either:
    - Synthesize and append a follow-up line (logging `queue_next_contract_violation_recovered`), or
    - Treat the run as a contract violation (log error, mark queue_failed, and avoid claiming a clean Success).
- Ensure this enforcement does **not** double-append when the roadmap agent already returned a valid follow-up in its `queue_followups` metadata.

### Step 5: Wire dynamic signals into helper selection (late conceptual focus)

- Use existing signals from `Second-Brain-Config` and roadmap parameters:
  - `roadmap_tech_progression` and `tech_levels` (Phase 5+ ⇒ pseudo-code tier).
  - `prompt_defaults.roadmap.context_util_threshold` and per-run ctx util from `workflow_state`.
  - `roadmap.control_plane_v2.adaptive_cap`, stagnation and same-subphase thresholds.
- In the helper-graph builder, add explicit rules such as:
  - If phase ≥5 **and** ctx util ≥ threshold → nested validator **selected**.
  - If phase ≥5 and same-subphase streak or gate-block streak active → nested validator + IRA **selected**.
  - If RECAL-ROAD recommended by previous runs → research helper **selected** for the next deepen.
- Make sure these selections feed into Task-harden so that, once selected, helpers are treated as mandatory.

### Step 6: Update docs and cross-references

- Update or add sections in:
  - `[3-Resources/Second-Brain/Docs/Pipeline-Validator-Profiles.md](3-Resources/Second-Brain/Docs/Pipeline-Validator-Profiles.md)` to describe the new dynamic helper selection rules for roadmap.
  - `[3-Resources/Second-Brain/Docs/Control-Plane-Heuristics-v2.md](3-Resources/Second-Brain/Docs/Control-Plane-Heuristics-v2.md)` to document how adaptive caps, drift, and context-util signals influence helper selection.
  - `[3-Resources/Second-Brain/Queue-Sources.md](3-Resources/Second-Brain/Queue-Sources.md)` to capture the stricter RESUME_ROADMAP `queue_next` follow-up enforcement.
- Ensure `.cursor/sync/` copies of any modified rules/skills are updated per `backbone-docs-sync.mdc`.

### Step 7: Sanity-check with a dry conceptual scenario

- Without actually running pipelines, construct a **thought experiment** run:
  - Phase 5.2 deepen with high ctx util and prior RECAL-post-5.1.2 row.
- Walk through:
  - Expected helper-selection outputs (which helpers are selected and why).
  - Expected Task-handoff sequence and nested helper calls.
  - Expected queue state before/after (RESUME_ROADMAP line consumed, follow-up synthesized or preserved).
- Compare against the bad 5.2 run to confirm the new logic would:
  - **Refuse** to report Success without required helpers being invoked, and
  - **Guarantee** a follow-up RESUME_ROADMAP line when `queue_next` is true.

