---
name: helper-proof-of-attempt-hardening
overview: Define and wire a combined helper hardening contract that requires proof-of-attempt for mandatory subagents and adds concrete enforcement in roadmap and queue agents.
todos:
  - id: spec-proof-attempt
    content: Add Mandatory helper proof-of-attempt section to Subagent-Safety-Contract with required ledger fields and invariants.
    status: completed
  - id: docs-fallback-honesty
    content: Tighten Safety-Invariants docs to bind inline fallback and material_state_change_asserted to helper proof-of-attempt rules.
    status: completed
  - id: roadmap-prompt-harden
    content: Harden roadmap agent prompt with anti-rationalization language and a concrete nested helper Task launch template.
    status: completed
  - id: queue-post-return-gate
    content: Add post-return validation in QueueSubagent that rejects balance-mode roadmap results when mandatory helpers were not actually attempted.
    status: completed
  - id: ledger-examples
    content: Add valid and forbidden nested_subagent_ledger examples illustrating the new invariants.
    status: completed
isProject: false
---

# Helper Proof-of-Attempt Hardening Plan

### Goal

Combine a **core Cursor-side contract** (mandatory helper proof-of-attempt and honesty rules) with **Grok-style wiring** (roadmap prompt hardening, safety invariants, and queue post-return checks) so the system cannot claim successful roadmap deepens without actually launching mandatory nested helpers.

### 1. Core contract: helper proof-of-attempt (spec layer)

- **Add a new section** to `3-Resources/Second-Brain/Subagent-Safety-Contract.md` (or its iteration-2 equivalent) titled `Mandatory helper proof-of-attempt`:
  - Define required ledger fields: `helper_mandatory`, `subagent_type`, `task_tool_invoked`, `outcome`, `task_error_code`, `contract_satisfied`, `little_val_final_ok`.
  - State the invariant: for any helper where `helper_mandatory: true` and `subagent_type` is non-null:
    - It is illegal to use `outcome: invoked_ok | failed` unless `task_tool_invoked: true` and a real `Task(subagent_type)` call occurred.
    - If `task_tool_invoked: false`, only `outcome: blocked | skipped_by_operator` are allowed, and `contract_satisfied` and `little_val_final_ok` must both be `false`.
  - Forbid `outcome: not_applicable` for mandatory helpers.
  - Define the shape of **analysis-only** runs: all mandatory helpers marked `blocked` with `task_error_code: analysis_only_contract_not_evaluated`, and prose must call the run advisory, never a deepen/handoff.
  - Define the roll-up rule: `contract_satisfied: true` is only legal if all mandatory helpers have `task_tool_invoked: true` and `outcome: invoked_ok | failed`, with no blocked/skipped/na states.

### 2. Safety invariants: fallback + honesty tightening

- **Update `3-Resources/Second-Brain/Docs/Safety-Invariants.md`** to explicitly tie inline fallback to the proof-of-attempt rule:
  - Clarify that `full_run_inline` (Cursor Read/ApplyPatch fallback) exists only to replace MCP IO, **not** helper Task calls.
  - State: MCP unavailability or inline fallback never waives mandatory helpers in balance/extreme modes; if helper Task calls fail, the run must be `#review-needed` and cannot clear the queue as Success.
  - Add the rule that `material_state_change_asserted: true` is only valid when a full mandatory helper cycle has run and a structural edit is ledgered after it.
  - Cross-reference the new `Mandatory helper proof-of-attempt` section and the nested ledger spec.

### 3. RoadmapSubagent: prompt hardening and helper launch template

- **Edit `.cursor/agents/roadmap.md`** to inject a strong anti-rationalization block near the top:
  - Explicitly forbid patterns like “treat as analysis-only but set `material_state_change_asserted: true`”, “create 5.1 note and pretend states are correct”, and “set nested_validator_skipped_material_gate while speaking as if validator ran”.
  - Restate that in balance mode the roadmap agent must always attempt nested `Task(validator)`, `Task(internal-repair-agent)`, and structural little-val for applicable deepens, regardless of MCP/inline IO mode.
- **Define a concrete nested helper launch template** in the roadmap agent docs section:
  - Show a minimal YAML/JSON structure for `task_handoff` with `subagent_type`, `pipeline_mode_used: "balance"`, `required: true`, and `fallback_mode: "none"` (disallow generalPurpose emulation for mandatory helpers).
  - Require that every mandatory helper step records a ledger row with `task_tool_invoked: true` after a successful `Task` call, or a row with `task_error_code` if the call fails.
- **Align roadmap ledger writing logic** with the core contract:
  - Ensure any step with `helper_mandatory: true` never writes `outcome: not_applicable`.
  - Ensure analysis-only partial deepens for things like 5.1 note restoration are labeled advisory (`contract_satisfied: false`, `little_val_final_ok: false`) and never consume queue entries as fully successful deepens.

### 4. QueueSubagent: post-return enforcement for roadmap entries

- **Extend `.cursor/agents/queue.md`** with a `Post-Roadmap Return Validation` section:
  - After any `Task(roadmap)` call that returns Success, parse `nested_subagent_ledger` in the roadmap return.
  - If `pipeline_mode_used === "balance"` and any mandatory helper step shows `task_tool_invoked: false` without a valid `task_error_code` from the host, treat the roadmap result as invalid:
    - Do not clear the queue entry as processed-success.
    - Append a `queue_failed` / `#review-needed` style Watcher-Result and Errors.md entry citing `balance_mode_helper_skip_detected`.
    - Optionally synthesize `queue_followups.next_entry` to preserve continuation rather than killing the queue.
- Make QueueSubagent explicitly reference the `Mandatory helper proof-of-attempt` section and `Safety-Invariants` so Layer 1 is the final honesty gate, not just an orchestrator.

### 5. Cross-file doc sync and examples

- **Add short cross-links** in `Subagent-Safety-Contract.md` to:
  - `Docs/Safety-Invariants.md` (for honesty + fallback rules), and
  - the roadmap/queue agent files as the canonical examples of enforcing the contract.
- Optionally, **add a tiny worked example** to the nested ledger spec:
  - Show one valid ledger snippet (mandatory helper run with `task_tool_invoked: true` and `outcome: invoked_ok`).
  - Show one explicitly invalid pattern (mandatory helper with `task_tool_invoked: false`, `outcome: not_applicable`), marked as forbidden by the new invariants.

### Todos

- **spec-proof-attempt**: Add the `Mandatory helper proof-of-attempt` section to the Subagent-Safety-Contract, defining required fields and invariants.
- **docs-fallback-honesty**: Strengthen `Docs/Safety-Invariants.md` with explicit inline-fallback and `material_state_change_asserted` rules tied to helper attempts.
- **roadmap-prompt-harden**: Harden `.cursor/agents/roadmap.md` with anti-rationalization language, helper launch template, and correct analysis-only labeling.
- **queue-post-return-gate**: Update `.cursor/agents/queue.md` to perform post-return ledger validation for roadmap entries and reject any balance-mode result that skipped mandatory helpers.
- **ledger-examples**: Add at least one valid and one forbidden nested_subagent_ledger example to the ledger spec to make the new invariants concrete.

