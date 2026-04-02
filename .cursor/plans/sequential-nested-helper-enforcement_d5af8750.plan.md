---
name: sequential-nested-helper-enforcement
overview: Tighten documentation and contracts so validator and IRA nested helpers are required to run sequentially (no async/parallel fan-out) in roadmap and research pipelines, and align ledger/spec language with that requirement.
todos:
  - id: update-safety-contract
    content: Tighten Subagent-Safety-Contract to forbid parallel/async execution of dependent helper chains (validator → IRA → second validator) and scope fan-out to independent helpers only.
    status: pending
  - id: update-roadmap-agent
    content: Update roadmap subagent agent and rule files to state that nested validator and IRA calls for a run must be strictly sequential and awaited in order, and clarify this in the nested_subagent_ledger description.
    status: pending
  - id: update-research-agent
    content: Update research subagent agent file to require sequential helper execution for its validator/IRA cycle and clarify allowed parallelism for independent research helpers.
    status: pending
  - id: update-ledger-spec
    content: If Nested-Subagent-Ledger-Spec.md exists, extend it to state that dependent helper steps are assumed to be serialized and must not be launched in parallel, and recommend ledger fields that make ordering auditable.
    status: pending
isProject: false
---

## Goal

Clarify and enforce that **dependent nested helpers** (especially the Validator → IRA → second-Validator cycle, and any IRA runs that consume validator output) **must execute sequentially**, not in async/parallel, while still allowing parallel fan-out only for truly independent helpers (e.g. separate research lookups).

## Key files to update

- **Subagent safety contract**: `3-Resources/Second-Brain/Subagent-Safety-Contract.md`
- **Global invariants doc** (if present and separate): `3-Resources/Second-Brain/Docs/Safety-Invariants.md`
- **Roadmap subagent agent file**: `.cursor/agents/roadmap.md`
- **Roadmap rules mirror**: `.cursor/rules/agents/roadmap.mdc`
- **Research subagent agent file**: `.cursor/agents/research.md`
- **Nested ledger spec** (if present): `3-Resources/Second-Brain/Docs/Nested-Subagent-Ledger-Spec.md`

## Planned changes

- **Subagent-Safety-Contract.md**
  - Add a concrete **Dependent Helper Serialization Rule** section under the nested-helper / IRA area, with this shape:
    - State that dependent chains such as **Validator → IRA → second Validator** (and Research’s **validator→IRA→validator** synthesis cycle) **must execute sequentially** within a single pipeline invocation.
    - Spell out the required sequence:
      - Launch `Task(validator)` (first pass) and **await full return** (including severity, `primary_code`, `reason_codes`, gap citations, `report_path`).
      - Use that output as direct input when launching `Task(internal-repair-agent)`; only launch IRA **after** the validator return has been incorporated.
      - After IRA returns, run post-IRA little_val, then (when required) launch the second `Task(validator)` with `compare_to_report_path`.
    - Clarify that **parallel fan-out remains allowed only for independent helpers** (e.g. unrelated research lookups), and is **never permitted for the Validator/IRA dependent protocol in balance or extreme modes**.
    - Note that ledger steps (`nested_validator_first`, `ira_post_first_validator`, `nested_validator_second`) are expected to show non-overlapping `started_iso` / `ended_iso` windows consistent with sequential execution, and that overlapping or out-of-order dependent helper timestamps should be treated as a contract breach (e.g. `detail.reason_code: nested_helper_order_violation`, status `#review-needed`).
- **Safety-Invariants doc** (`Docs/Safety-Invariants.md`, if present)
  - Add a short invariant in the nested-helper or roadmap section summarizing:
    - “**Dependent nested helpers must be sequential**: for roadmap and research pipelines, the validator report is an input to IRA; these helpers may not be run in parallel, and IRA must see the final validator output from this run.”
    - Note that violation is a structural error that should be surfaced in Errors/telemetry, not silently tolerated.
- **Roadmap subagent agent + rule** (`.cursor/agents/roadmap.md`, `.cursor/rules/agents/roadmap.mdc`)
  - In the nested helper / balance-mode section of the agent, add a **“Strict Sequential Execution of Dependent Nested Helpers”** paragraph that:
    - Calls out the Validator → IRA → little_val → second Validator protocol as a **single serialized nested cycle**, not a set of independent Tasks.
    - Requires the subagent to:
      1. Launch `Task(validator)` for `nested_validator_first` and **await its full structured return**.
      2. Use that validator output (severity, `primary_code`, `gap_citations`, `report_path`, etc.) as direct input when launching `Task(internal-repair-agent)` for `ira_post_first_validator`.
      3. After IRA returns, run post-IRA little_val, then (if required) the second `Task(validator)`.
      4. Record ledger steps in strict ordinal order with non-overlapping timestamps.
    - Explicitly forbid launching validator and IRA helpers concurrently for the same run, even if the Task tool supports parallel calls; if the host prevents proper sequential Task calls, the agent must record `task_error` for the affected step and return `#review-needed` (never “analysis-only” or skipped helpers while claiming the cycle ran).
  - In the roadmap rule’s `nested_subagent_ledger` section, reinforce that for this dependent cycle:
    - `steps` must appear in that serialized order and, when timestamps are present, they should show non-overlapping execution windows for the dependent helpers.
- **Research subagent agent** (`.cursor/agents/research.md`)
  - Mirror the roadmap requirement for any **research_synthesis** Validator → IRA → Validator cycle:
    - Require the same strict sequence (first validator → IRA → second validator) with awaited Task returns and no concurrent helper calls for the same synthesis run.
    - Clarify that parallel fan-out is still allowed only for **independent** research work (e.g. multiple unrelated queries), not for the dependent validator/IRA protocol itself.
- **Nested-Subagent-Ledger spec** (`Docs/Nested-Subagent-Ledger-Spec.md`)
  - In the ordering / timestamps area, add a short reinforcement that:
    - For dependent steps (`nested_validator_first` → `ira_post_first_validator` → `nested_validator_second`), the ledger **assumes serialized execution**.
    - When `started_iso` / `ended_iso` are recorded, each subsequent step’s `started_iso` should occur after the prior step’s `ended_iso` (or be clearly ordered), and parents must not emit ledger rows that imply overlapping or reversed execution for these dependent helpers.

## Alignment and backstops

- Ensure **QueueSubagent** rules in `[.cursor/rules/agents/queue.mdc](.cursor/rules/agents/queue.mdc)` remain consistent: they already enforce attestation and honesty but do not discuss helper ordering; we will **not** change queue behavior here, only rely on the strengthened contracts to prevent legitimate-but-misleading async helper usage.
- Optionally, add a brief note to the **Error Handling / Observability** section of the safety contract that treating dependent helpers as parallel is a **contract violation** and should surface as `error_type: nested_helper_parallel_violation` or similar when detected in audits, without changing runtime code yet.

