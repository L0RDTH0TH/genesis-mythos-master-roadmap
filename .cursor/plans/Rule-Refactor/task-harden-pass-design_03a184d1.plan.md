---
name: task-harden-pass-design
overview: Design and roll out a Task harden pass that probes Task subagent capabilities once per run, normalizes launch decisions and metadata for all child Task calls, and logs deviations from the ideal pipeline contract for later audit.
todos:
  - id: capability-probe-wrapper
    content: Implement the Task harden wrapper that probes Task subagent capabilities once per run and caches available_subagents and raw_errors.
    status: completed
  - id: decision-logic-child-launch
    content: Implement normalized decision logic for each child Task launch using desired_subagent_type, task_role, and pipeline profile, including mandatory helper enforcement.
    status: completed
  - id: metadata-hand-off-return
    content: Add YAML metadata blocks to Task hand-offs and enforce machine-readable footers on Task returns for task_launch_mode and contract_satisfied.
    status: completed
  - id: logging-observability
    content: Wire harden pass into Errors.md, task-handoff-comms.jsonl, Watcher-Result, and queue-continuation.jsonl logging with clear degradation markers.
    status: completed
  - id: layer-responsibilities
    content: Update Layer 0, Layer 1 queue/dispatcher, and Layer 2 pipeline agents to honor capabilities snapshot, launch_mode, and nested_subagent_ledger.
    status: completed
  - id: rollout-phases
    content: "Roll out harden pass in three phases: non-invasive wrapper, strict gating, and configurable profiles tied to Second-Brain-Config."
    status: completed
isProject: false
---

# Task Harden Pass for Task-Based Subagents

## Scope and Goal

- **Goal**: Design a Task harden pass that every Layer 0/1/2 agent uses before launching any child agent via Task, so that:
  - It never lies about which `subagent_type` values are actually usable in the current host.
  - It uses safe fallbacks (e.g. `generalPurpose`) when needed, with explicit flags.
  - It records every decision in `task-handoff-comms` / `Errors.md` so you can audit when and why it deviates from the ideal pipeline contract.

## 1. Discover and Cache Task Capabilities Per Run

- **Task schema probe (first use per chat/run)**:
  - On the first Task use in a run, the harden pass attempts a no-op Task call for each expected pipeline subagent (`queue`, `roadmap`, `validator`, `archive`, `distill`, `express`, `organize`, `research`, etc.) with a trivial prompt such as "ping" in a clearly-marked dry mode.
  - It interprets the results only as capability checks: success vs explicit rejection / schema error, not as real work.
- **Capabilities cache (in-memory for the run)**:
  - Maintain `available_subagents: { queue: true/false, roadmap: true/false, validator: true/false, ... }` based on the probe outcomes.
  - Maintain `raw_errors: { roadmap: <first failure message>, validator: <first failure message>, ... }` for diagnostics and logging.
- **Guardrail**:
  - Subsequent Task launches must consult this cache; callers are not allowed to assume or improvise `subagent_type` values outside this set.

## 2. Normalize Launch Decisions Per Child Call

- **Decision wrapper per launch**:
  - For every would-be child launch, pass the request through a small decision function with inputs:
    - `desired_subagent_type` (e.g. `roadmap`, `validator`, `archive`).
    - `task_role` (e.g. `layer1_queue`, `layer2_roadmap`, `helper_validator`).
    - Active pipeline profile (e.g. `pipeline_mode` / speed tier such as `fast`, `balance`, `extreme`).
- **Profile selection vs mandatory semantics**:
  - The active profile only controls which helpers are selected at all for a given pipeline:
    - **fast**: smaller helper set.
    - **balance**: default helper set.
    - **extreme**: maximal helper set.
  - Once a helper is selected for the active profile, it becomes **mandatory** for that run: if it is in the helper graph for this profile, failure to run it cleanly must block `Success` for that step.
- **Branching logic**:
  - If `available_subagents[desired] === true`:
    - Launch Task with that `subagent_type` and the full hand-off prompt; mark `launch_mode: native_subagent`.
  - If `available_subagents[desired] === false` and the helper is **not** selected by the current profile:
    - Treat it as out of graph for this run; do not invoke it and do not let it affect `Success` / failure.
  - If `available_subagents[desired] === false` and the helper **is** selected by the current profile (therefore mandatory):
    - Do **not** attempt `generalPurpose` emulation for that mandatory helper.
    - Treat the overall step as **blocked** and mark the parent pipeline result as `#review-needed` or failure, not `Success`.
    - Set explicit flags, e.g. `nested_validator_first: { task_tool_invoked: false, reason: "task_enum_missing" }`, in the step metadata.

## 3. Explicit Metadata in Hand-Off and Return

- **Hand-off decoration (outbound to child)**:
  - Extend the prompt for all child Task launches with a small YAML block indicating:
    - `layer_role` (e.g. `layer0_chat`, `layer1_queue`, `layer2_roadmap`, `helper_validator`, etc.).
    - `launch_mode` (`native_subagent` vs `generalPurpose_fallback`).
    - `expected_contract` (e.g. `roadmap_handoff_auto`, `archive_candidate`, `distill_readability`).
- **Return decoration (inbound from child)**:
  - Require every child result to include a short, machine-readable footer (or fenced YAML block) like:
    - `task_launch_mode: native_subagent | generalPurpose_fallback`.
    - `contract_satisfied: true | false`.
    - `nested_helper_summary` / `nested_subagent_ledger` if it launched its own helpers.
  - The parent harden pass inspects this metadata and:
    - Refuses to upgrade a partial run to full `Success` when `contract_satisfied: false`.
    - Converts the outcome to `#review-needed` or `queue_failed` per existing queue / pipeline rules.

## 4. Error Logging and Observability

- `**Errors.md` integration**:
  - On the first failure per subagent type (`roadmap`, `validator`, etc.), write a concise entry summarizing:
    - The attempted `subagent_type`.
    - The error message from the Task host (schema rejection, runtime failure, etc.).
    - Whether a `generalPurpose` fallback was attempted and its result.
- `**task-handoff-comms.jsonl` logging**:
  - For every Task launch, append a JSONL entry containing:
    - `task_correlation_id`, `from_actor`, `to_actor`, `subagent_type`, `launch_mode`, and a short `body_preview`.
  - On return, append a corresponding entry with:
    - `task_correlation_id`, `launch_mode`, `contract_satisfied`, and any `fallback_reason`.
- **Watcher-Result neutrality**:
  - Keep `Watcher-Result` lines neutral as per existing spec, but when a pipeline is degraded due to fallback, include a short machine tag in the `trace` (e.g. `launch_mode=generalPurpose_fallback`, `contract_satisfied=false`).

## 5. Layered Responsibilities

- **Layer 0 (chat / manual entry)**:
  - Always routes pipeline modes through `Task(subagent_type: queue)` instead of running pipelines inline.
  - Runs the harden pass once per conversation, building the capabilities snapshot and passing it down in the hand-off to Layer 1.
- **Layer 1 (queue/dispatcher subagent)**:
  - Uses the capabilities snapshot to decide whether to launch `Task(roadmap)`, `Task(validator)`, etc. directly or via `generalPurpose` (when allowed by profile), per step.
  - Applies strict vs soft behavior based on existing `strict_nested_return_gates` and tiered-block configuration.
- **Layer 2 (pipeline subagents)**:
  - Treats `launch_mode` and `layer_role` as read-only context; does not re-probe capabilities.
  - Emits clear `nested_subagent_ledger` entries showing when a nested helper was:
    - Invoked natively.
    - Invoked as `generalPurpose` fallback.
    - Skipped because the host could not supply any Task channel and profile allowed skipping.

## 6. Guardrails to Prevent Misreporting Capabilities

- **Capability truthfulness**:
  - No agent may claim that `Task(roadmap)` or `Task(validator)` (or any other subagent) is unavailable purely from prior assumptions; it must base that on an actual probe result stored in the capabilities cache.
- **Mandatory helper enforcement**:
  - No agent may report a pipeline as fully successful when a mandatory nested helper (e.g. hostile validator) was neither run natively nor via a sanctioned fallback.
- **Deviation logging**:
  - Any deviation from the ideal contract must be reflected in:
    - The parent result status (`#review-needed` / failure), and
    - A logged error or continuation entry (e.g. `Errors.md` / `queue-continuation.jsonl`).

## 7. Minimal Rollout Path

- **Phase 1 – Non-invasive wrapper**:
  - Implement the harden pass as a pure wrapper around existing Task calls:
    - Perform capability probing and caching.
    - Decorate hand-offs and returns with metadata.
    - Log capabilities and `launch_mode` for observability.
  - Do **not** yet change success/failure semantics; treat metadata as advisory.
- **Phase 2 – Strict gating**:
  - Turn on stricter rules:
    - Mandatory nested helpers must either succeed (native or sanctioned fallback) or force `#review-needed` / failure.
    - Block reporting `Success` when `contract_satisfied: false` for mandatory contracts.
- **Phase 3 – Configurable profiles**:
  - Tie behavior into `Second-Brain-Config` (e.g. `pipeline_mode` and `queue.strict_nested_return_gates`):
    - High-safety profiles enforce the strictest interpretation and mandatory helper gating.
    - Experimental or low-safety profiles allow softer fallbacks and skipping non-critical helpers.

## Implementation Notes

- **Key files to update**:
  - Central Task wrapper utilities used by Layer 0 and Layer 1.
  - Agent definitions for Layer 0, queue/dispatcher, and pipeline subagents to consume `launch_mode`, `layer_role`, and `nested_subagent_ledger`.
  - Logging utilities for `Errors.md`, `task-handoff-comms.jsonl`, `Watcher-Result`, and `queue-continuation.jsonl`.
- **Testing strategy**:
  - Unit-test the capability probe and cache behavior for various host Task schemas.
  - Integration-test degraded environments (missing `validator`, missing `roadmap`, etc.) and confirm that:
    - Hardening never claims capabilities that do not exist.
    - Mandatory helpers correctly gate success.
    - All deviations are logged and surfaced as `#review-needed` / failure where appropriate.

