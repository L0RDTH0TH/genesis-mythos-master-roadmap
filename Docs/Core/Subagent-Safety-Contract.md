---
title: Subagent Safety Contract
created: 2026-03-13
tags: [second-brain, subagents, safety]
para-type: Resource
status: active
---

# Subagent Safety Contract

When the main agent delegates to a pipeline subagent (ingest, roadmap, distill, express, archive, organize, research, **validator**), or to the **PromptCraft** helper (queue recovery crafting only), the subagent runs in a **clean context** with no automatic parent rules. For **Validator** (e.g. ROADMAP_HANDOFF_VALIDATE), the queue invokes the subagent with an **explicit model** when the validation type is configured with a fixed model (e.g. Second-Brain-Config § validator.roadmap_handoff.model). **Validator subagents MUST be read-only on input artifacts except the explicit output path** (e.g. the report note); they must not edit phase notes, roadmap-state, or other inputs. This document is the **single source of truth** for safety invariants that every subagent MUST enforce. The main agent MUST use the **Mandatory hand-off prompt structure** (below) when delegating.

## Cursor Task tool: `model` parameter

When Layer 0, Layer 1, or a pipeline invokes the Cursor **Task** tool: **omit** the `model` argument to inherit the parent session's model (default / auto behavior). Pass **`model: "fast"`** only when intentionally using the fast subagent tier. **Do not** pass **`model: "inherit"`** (or any `inherit` string) — it is **not** a valid Task API value and fails schema / parse validation. Validator and other Config-driven dispatches pass the explicit `model` string from Second-Brain-Config (e.g. `validator.roadmap_handoff.model`, `validator.<validation_type>.model`). **Disambiguation:** `.cursor/agents/*.md` YAML frontmatter `model: inherit` is Cursor's convention for **agent definition files**; it must **not** be copied into Task tool JSON arguments.

**Queue mode names** use **underscores** (e.g. `INGEST_MODE`, `RESUME_ROADMAP`, `RESEARCH_AGENT`). Hyphens are reserved for **chain-mode syntax (Phase 3)**: a single queue entry with mode `PRIMARY-DEP1-DEP2-...` runs dependency pipeline(s) first, then the primary with collected results. User-facing examples: `RESUME_ROADMAP-RESEARCH`, `RESUME_ROADMAP-RESEARCH-INGEST`. See Queue-Sources § Chain modes and Queue-Alias-Table § Chain command aliases.

---

## Roadmap MCP vs inline-edit behavior (Task environments)

- **Scope**: This section refines how the **roadmap subagent and its skills** (e.g. `roadmap-deepen`, structural little val, roadmap validators) behave when they run inside a Cursor **Task** environment where Obsidian MCP tools may or may not be available.
- **Single capability probe per roadmap run**:
  - At the **start** of each `Task(subagent_type: "roadmap")` invocation, the roadmap subagent MUST perform **one lightweight capability probe** to determine whether Obsidian MCP tools are usable in this environment (for example, a benign `obsidian_read_note` on a known-safe path or an equivalent no-op) **in `mcp_probe_mode: "auto"`**.
  - **Config toggle (skip/assume mode):**
    - If `Second-Brain-Config.task_harden.mcp_probe_mode` is missing or set to `"auto"`, the roadmap subagent MUST perform the probe call and set `mcp_available` from the probe outcome.
    - If it is set to `"assume_available"`, the roadmap subagent MUST skip the probe call and set `mcp_available: true`.
    - If it is set to `"assume_unavailable"`, the roadmap subagent MUST skip the probe call and set `mcp_available: false`.
  - When `mcp_probe_mode: "auto"`, the probe result MUST be interpreted as:
    - `mcp_available: true` when the representative call succeeds, or
    - `mcp_available: false` only when the host clearly rejects the MCP call or the Obsidian MCP server is unreachable.
  - The probe outcome MUST be cached in a **per-run capabilities object** (e.g. `roadmap_capabilities: { mcp_available: boolean }`, optionally including `probe_skipped: true|false` and `mcp_probe_mode: ...`) and **passed down** to roadmap skills (`roadmap-deepen`, little-val structural checks, roadmap validator glue). Individual skills MUST NOT re-probe Obsidian MCP independently.
- **Two-path contract (preferred vs fallback)**:
  - When `mcp_available: true`:
    - Roadmap skills **must** use the normal **MCP path**:
      - All structural mutations to roadmap artifacts (phase notes, `roadmap-state.md`, `workflow_state.md`, decisions-log, etc.) go through `obsidian_*` tools with backup/snapshot/dry_run gates.
      - Confidence bands, snapshot rules, and destructive-action guards from core-guardrails apply exactly as documented.
  - When `mcp_available: false`:
    - Roadmap skills **must switch to the inline-edit path**, treating Obsidian MCP as temporarily unavailable but **not** treating that as permission to skip the roadmap pipeline **or any mandated nested helper**:
      - Use Cursor’s file tools (`Read`/`ApplyPatch` primitives) to read and write markdown files for roadmap artifacts, while honoring the **intent** of backups/snapshots and confidence bands from core-guardrails as best as the host allows.
      - Continue to uphold the invariant that shell `cp`/`mv`/`rm` are never used on the vault; only inline text edits and non-destructive directory creation are allowed.
      - Continue to run nested helpers (little val structural skill, nested `Task(validator)`, `Task(internal-repair-agent)`, and `Task(research)` when required) exactly as dictated by the helper graph and profile; MCP unavailability alone is **not** a reason to omit these helpers. When the filesystem has fallen back to inline edits (`run_mode: "full_run_inline"`), the roadmap subagent **must still attempt** all required nested helper `Task` calls; if the Task host rejects a helper `subagent_type` or the call fails for host reasons, that step must be recorded as `outcome: task_error` with a concrete `host_error_class` / `host_error_raw`, and the overall status must be `#review-needed` or `failure` rather than Success with helpers silently marked `not_applicable`.
- **Run modes and honesty (roadmap)**:
  - Every roadmap subagent run MUST classify its overall execution into one of:
    - `run_mode: "full_run_mcp"` — structural mutations were performed via Obsidian MCP tools, and all required nested helpers ran or failed with `task_error` in the ledger.
    - `run_mode: "full_run_inline"` — structural mutations were applied via inline edits, and all required nested helpers ran or failed with `task_error` in the ledger.
    - `run_mode: "analysis_only"` — neither MCP nor inline edits could safely mutate the required artifacts for this run; the subagent performed read-only analysis and returned `#review-needed` or `failure` without claiming that deepen/recal/other structural actions actually executed.
  - The roadmap subagent MUST surface `run_mode` in its structured return (e.g. as part of `task_harden_result` or adjacent metadata), and Layer 1 MUST treat `analysis_only` as **non-success** for any queue entry that expected a structural action.
- **Final-success invariants remain in force**:
  - Even in `full_run_inline` mode, roadmap runs MUST:
    - Obey the **little val final-success gate**: never return **Success** when the final little val verdict for this run is `ok: false`.
    - Obey the **nested validator hard-block gate**: never return **Success** when the final nested validator verdict is a hard block (`severity: "high"` or `recommended_action: "block_destructive"`).
  - When helper steps are required by the helper graph/profile but cannot run due to host limits, the ledger MUST record `outcome: task_error` or an allowlisted `not_applicable` reason on those steps; the subagent MUST return `#review-needed` or `failure` rather than pretending that helpers or roadmap-deepen ran successfully. **MCP transport failures are always treated as limits on the filesystem path only, not on the nested-helper path**: a broken or missing Obsidian MCP server **never** converts a required nested validator/IRA/Research step into a permanent `not_applicable`—at most it forces that step into `task_error` with a non-successful overall status.

These roadmap-specific rules refine, but do not weaken, the global MCP & filesystem safety rules in `core-guardrails.mdc`: roadmap subagent and its skills are required to **continue doing the work** (via inline edits when MCP is down) while still upholding backup/snapshot intent, confidence bands, and nested-helper contracts as far as the host environment allows.

---

## Task-`attempt-before-skip` invariant (all Task callers)

- When this contract (or a pipeline / queue rule that cites it) says a subagent **must** be called – for example:
  - Layer 0 → Layer 1 `Task(subagent_type: "queue")` for EAT-QUEUE / PROCESS TASK QUEUE,
  - Layer 1 → pipeline `Task` for modes such as `INGEST_MODE`, `ROADMAP_MODE`, `RESUME_ROADMAP`, `DISTILL_MODE`, `EXPRESS MODE`, `ARCHIVE MODE`, `ORGANIZE MODE`, `RESEARCH_AGENT`, `VALIDATE`, `ROADMAP_HANDOFF_VALIDATE`,
  - Layer 2 → nested helper `Task` for `research_pre_deepen`, `nested_validator_first` / `nested_validator_second`, `ira_post_first_validator`,
- then the caller **MUST attempt a real Cursor `Task` call** with the intended `subagent_type` at least once in that run.
- Callers **MUST NOT** skip a mandated helper or pipeline dispatch purely because schema metadata or examples make that `subagent_type` look unavailable. The only allowed “did not run” outcome for a required helper is a real Task failure, recorded as `outcome: task_error` with a concrete `host_error_class` (e.g. `invalid_enum`, `nested_task_unavailable`, `resource_exhausted`) in the nested ledger and mirrored in [[3-Resources/Second-Brain/Docs/Task-Handoff-Comms-Spec|Task-Handoff-Comms-Spec]] records.
- For any run where this invariant applies, **compliance can be audited** by checking:
  - `.technical/task-handoff-comms.jsonl` for a `handoff_out` / `return_in` pair whose `subagent_type` matches the required helper or pipeline and whose `task_correlation_id` (or `parent_task_correlation_id` for nested helpers) matches the run’s `pipeline_task_correlation_id`, and
  - the pipeline’s `nested_subagent_ledger` (when present) for a step row with `task_tool_invoked: true` or `outcome: task_error` on the mandated helper `step` id.
- When the Task tool itself is genuinely unavailable or rejects the call, callers must:
  - record `task_error` with `host_error_raw` / `host_error_class` in the ledger,
  - append a `handoff_out` / `return_in` pair to `.technical/task-handoff-comms.jsonl`, and
  - **not** claim Success with `little_val_ok: true` when the safety contract still required that helper for this run.

---

## Mandatory helper proof-of-attempt (ledger + contract)

This section makes explicit the **proof-of-attempt requirement** for **mandatory** nested helpers (Validator, IRA, Research) and ties it to the top-level `contract_satisfied` flag. It refines, but does not replace, the honesty rules in [[3-Resources/Second-Brain/Docs/Safety-Invariants|Safety-Invariants]] § Helper profiles and the attestation rules in [[3-Resources/Second-Brain/Docs/Nested-Subagent-Ledger-Spec|Nested-Subagent-Ledger-Spec]].

For every queue-dispatched pipeline run that emits a `nested_subagent_ledger`:

- The top-level ledger object **must** include at least:
  - `helper_mandatory` (implicit in the helper graph / profile and per-step “required this run” rules in the ledger spec),
  - `material_state_change_asserted` (`true` \| `false` \| `unknown`),
  - `little_val_final_ok` (boolean),
  - `little_val_attempts` (int),
  - `ira_after_first_pass_effective` (boolean),
  - `nested_cycle_applicable` (boolean),
  - `pipeline_mode_used` (when available: `fast` \| `balance` \| `extreme` or equivalent),
  - `effective_profile_snapshot` (when available),
  - and an ordered `steps[]` array of step records as in Nested-Subagent-Ledger-Spec.

For any **step** where the helper is **mandatory for this run** (selected in the helper graph for the active profile and marked “required this run” by the ledger heuristics), the following invariants apply:

- It is **illegal** to record:
  - `outcome: invoked_ok` or `invoked_empty_ok` **unless** `task_tool_invoked: true` and a real `Task(subagent_type)` call for that helper occurred in this run.
  - `outcome: skipped` with `task_tool_invoked: false` **unless** `detail.reason_code` is in the documented allowlist for genuine N/A cases (material gate, unfreeze-only, legacy clean log-only IRA skip, chain consumables, etc.).
  - `outcome: not_applicable` on a helper that the helper graph/profile selected as mandatory for this profile and branch.

- When a mandatory helper **cannot** be launched (Task enum rejection, missing tool, resource exhaustion, etc.), the only valid ledger shape is:
  - `task_tool_invoked: false`,
  - `outcome: task_error`,
  - non-empty `host_error_class` / `host_error_raw`,
  - and an appropriate `detail.reason_code` (e.g. `nested_task_unavailable`, `task_enum_rejected`).
  In this case the pipeline **must not** return **Success** for that run; the overall status must be `#review-needed` or `failure`.

Analysis-only or advisory runs (no full helper cycle) **must** make this explicit:

- Set `material_state_change_asserted: false` (or `unknown` when you truly cannot tell), `little_val_final_ok: false` (or omit little val fields when it was never run), and `nested_cycle_applicable: false` when the entire nested cycle was out of scope.
- For helpers that would normally be mandatory under the profile, record **blocked** or **analysis-only** skip rows with:
  - `task_tool_invoked: false`,
  - `outcome: blocked` or `not_applicable`,
  - `detail.reason_code: analysis_only_contract_not_evaluated` (or equivalent),
  - and prose that clearly labels the run as **advisory / analysis-only**, never as a completed deepen / handoff.

Roll-up invariant (parent-facing):

- A pipeline may set `contract_satisfied: true` in its `task_harden_result` **only if all of the following hold**:
  - Every helper that is mandatory under the active profile has a ledger row with `task_tool_invoked: true` and `outcome: invoked_ok | invoked_empty_ok | failed` (or `task_error` when the host rejected the call but the contract allowed a degraded, non-successful exit).
  - No mandatory helper appears only as `skipped` or `not_applicable` without an allowlisted `detail.reason_code`.
  - `nested_cycle_applicable` and `material_state_change_asserted` are consistent with the helper graph and the pipeline’s own contracts for this mode.
- When any mandatory helper violates these conditions, the pipeline **must** set `contract_satisfied: false` in its `task_harden_result` and return a non-success status (`#review-needed` or `failure`); Layer 1 strict gates (`queue.strict_nested_return_gates`) then prevent the queue from consuming the entry as a successful run.

---

## Task harden pass (capability probing, profiles, and launch modes)

All `Task` callers (Layer 0, Layer 1, and Layer 2 nested helpers) MUST route their Task invocations through a **Task harden pass**. The harden pass is a **pure wrapper** around the Cursor Task tool that:

- Probes which `subagent_type` values are actually usable in the current host.
- Caches those capabilities for the rest of the run.
- Normalizes launch decisions (native vs fallback vs skipped) based on an explicit **profile**.
- Decorates hand-offs and returns with machine-readable metadata so deviations from the ideal contract are auditable.

### 1. Capability probe and per-run cache

- **When to probe**
  - On the **first** Task use per conversation/run, the harden pass MUST:
    - Attempt a **no-op Task call** for each expected pipeline subagent type:
      - `queue`, `roadmap`, `ingest`, `distill`, `express`, `archive`, `organize`, `research`, `validator`,
      - plus any additional, explicitly-whitelisted helper types such as `prompt_craft`, `internal-repair-agent`.
    - Use a trivial prompt such as `"ping (capability probe only)"` that makes it clear to the callee that no real work is required.
  - These probe calls exist **only** to discover whether a given `subagent_type` is accepted by the host; pipeline logic MUST ignore their semantic content.

- **Interpreting probe results**
  - The harden pass MUST treat each probe outcome as:
    - **available** when the Task call succeeds (normal return from the subagent, regardless of its textual content).
    - **unavailable** only when the Task host explicitly rejects the `subagent_type` (e.g. enum/validation error, schema mismatch) or when the model signals that the Task tool itself is not usable.
  - Probes MUST NOT infer unavailability from examples, documentation, or schema guesses alone.

- **Capabilities cache (per run, in-memory)**
  - The harden pass maintains an **in-memory** cache for the remainder of the run:
    - `available_subagents: { [subagent_type: string]: boolean }`
      - e.g. `{ queue: true, roadmap: true, validator: false, research: true, ... }`.
    - `raw_errors: { [subagent_type: string]: string }`
      - first failure / rejection message per type, for diagnostics.
  - Once populated, this cache MUST be treated as the single source of truth for whether a given `subagent_type` is usable **in this run**.

- **Guardrail**
  - After the probe:
    - No caller may claim that a particular `subagent_type` is unavailable unless `available_subagents[type] === false` **and** there is a corresponding `raw_errors[type]` describing the Task host rejection.
    - No caller may assume new `subagent_type` values outside this set; use of unknown types is a contract violation.

### 2. Profiles and normalized launch decisions

Every Task launch MUST pass through a small decision function controlled by:

- `desired_subagent_type`: the intended subagent (`roadmap`, `validator`, `archive`, `research`, …).
- `task_role`: role of the caller (e.g. `layer0_chat`, `layer1_queue`, `layer2_roadmap`, `helper_validator`).
- `pipeline_profile`: the active safety/speed tier for this pipeline:
  - `fast` — minimal helper set, softest enforcement, may omit non-critical helpers when allowed by the helper graph.
  - `balance` — default helper set (recommended); full enforcement of all selected helpers and step contracts.
  - `extreme` — maximal helper set (all helpers enabled) with the strictest enforcement and observability.

**Helper graph per profile**

- For each pipeline mode, maintain a **profile-specific helper graph** that lists which nested helpers are:
  - **selected** for that profile (must run when reachable), or
  - **not selected** (optional or unused for that profile).
- Once a helper is selected for the current profile, it becomes **mandatory** for that run:
  - If it appears in the helper graph for this profile and step, failure to run it cleanly MUST block `Success` for that step, even when capability probes indicate the host cannot supply it.
  - When `pipeline_profile === "balance"` or `pipeline_profile === "extreme"`, callers MUST treat **all** selected helpers as **hard mandatory** for that run; skipping them is only allowed via recorded `task_error` with `host_error_class` and `raw_errors[...]` evidence.
  - When `pipeline_profile === "fast"`, callers MAY configure a smaller helper graph, but for any helper that **is** selected, the same mandatory semantics apply (attempt-before-skip + no fake Success).

### 2a. Step-enumerated task descriptions (all profiles)

- **Every Task hand-off MUST enumerate its work as ordered steps**, regardless of profile (`fast`, `balance`, or `extreme`):
  - Use the format **`Step 1: …`**, **`Step 2: …`**, **`Step 3: …`** in execution order.
  - Each step describes a single concrete action or tightly coupled micro-sequence (e.g. “Step 3: If X, do Y; otherwise do Z.”).
  - The step list must cover the full contract for this invocation (including error-handling, logging, and metadata writes that the child is responsible for).
- **Launchers (all layers) MUST**:
  - Include a step-enumerated block in the hand-off for every `Task` invocation, including capability probes when they request any non-trivial work.
  - Treat these steps as **normative** for what counts as the child’s contract on this run (alongside `expected_contract` and the helper graph).
- **Subagents MUST**:
  - Treat the step list as ordered requirements and execute them in sequence unless a hard safety gate or unrecoverable error forces early exit.
  - Reflect any intentionally skipped or aborted step in their narrative summary and, when applicable, in `nested_subagent_ledger` and Run-Telemetry.
- **Contract enforcement across profiles**:
  - For **all profiles** (`fast` / `balance` / `extreme`), a child that claims `contract_satisfied: true` **MUST NOT** have silently skipped a numbered step it could have executed safely.
  - When a numbered step is skipped due to safety gates or host limits, the child **MUST** set `contract_satisfied: false` (or downgrade status to **#review-needed** / **failure**) and surface the reason.
  - Under **`balance`** and **`extreme`**, parents MUST treat **any** `contract_satisfied: false` due to a skipped numbered step as a **hard failure for that run** (no full Success), even if helpers would otherwise be optional; under **`fast`**, parents MAY allow softer behavior only for helpers that were never selected in the profile’s helper graph.

**Branching logic (per launch)**

Given `desired_subagent_type` and the profile/helper graph:

1. If `available_subagents[desired_subagent_type] === true`:
   - Launch Task with that `subagent_type` and the full hand-off prompt.
   - Mark `launch_mode: native_subagent` in both:
     - the hand-off metadata, and
     - the child’s required return footer.

2. If `available_subagents[desired_subagent_type] === false` **and** the helper is **not selected** by the current profile (out of graph):
   - Treat this helper as **out of graph** for this run:
     - Do **not** call Task for it.
     - Do **not** require it for `Success`.
   - Record a ledger row (when applicable) indicating:
     - `outcome: not_applicable`,
     - `task_tool_invoked: false`,
     - `detail.reason_code: helper_not_selected_for_profile`.

3. If `available_subagents[desired_subagent_type] === false` **and** the helper **is selected** by the current profile (mandatory):
   - **Do not** attempt `generalPurpose` emulation for this mandatory helper.
   - Treat the overall step as **blocked**:
     - Mark a ledger row for that helper step with `outcome: task_error`, `task_tool_invoked: false`, `detail.host_error_class: "task_enum_missing"` (or equivalent), and `detail.host_error_raw` from `raw_errors[desired_subagent_type]` when present.
     - Propagate this into the parent status: the pipeline or parent helper MAY NOT return overall `Success` for this step; it MUST return `#review-needed` or `failure`.

4. **Optional generalPurpose fallback (non-mandatory helpers only)**
   - When a helper is **not selected** for the current profile (non-mandatory) but the pipeline wishes to attempt an emulation via `generalPurpose`, it MAY:
     - Launch `Task(subagent_type: "generalPurpose")` with an explicit YAML preamble describing the expected contract.
     - Mark this in the outbound metadata as `launch_mode: generalPurpose_fallback`.
   - The harden pass MUST treat this as a **best-effort** optimization:
     - Fallback results MUST NOT be used to pretend that the ideal helper actually ran.
     - Failure or absence of this fallback MUST NOT be allowed to gate or fake `Success` for any **mandatory** helper.

### 3. Hand-off and return metadata

To make Task launches and their outcomes auditable, the harden pass MUST decorate both outbound prompts and inbound returns.

**Outbound (hand-off decoration — include speed/profile explicitly)**

- For every Task launch (Layer 0, Layer 1, or Layer 2), prepend or append a small YAML block to the prompt that includes at least:

```yaml
task_harden_metadata:
  layer_role: layer0_chat | layer1_queue | layer2_roadmap | layer2_ingest | helper_validator | helper_research | helper_internal_repair_agent | ...
  launch_mode: native_subagent | generalPurpose_fallback
  pipeline_profile: fast | balance | extreme
  expected_contract: "<short identifier, e.g. roadmap_handoff_auto, archive_candidate, distill_readability>"
```

- This block is **advisory** for the child but **normative** for observability:
  - `layer_role` tells observability tools where in the stack the call originated.
  - `launch_mode` binds the invocation to the capability decision taken by the harden pass.
  - `pipeline_profile` makes the **speed/safety tier explicit** on every Task call (`fast` minimal helpers, `balance` full helpers + complete enforcement, `extreme` maximal helpers + strictest enforcement).
  - `expected_contract` names the target contract so validators and auditors can align behavior with specs.

**Inbound (child result decoration)**

- Every subagent (pipeline or helper) MUST end its return with a short, machine-readable footer (e.g. fenced `yaml`) that includes:

```yaml
task_harden_result:
  task_launch_mode: native_subagent | generalPurpose_fallback
  pipeline_profile: fast | balance | extreme
  contract_satisfied: true | false
  nested_subagent_ledger_ref: "<optional pointer or summary>"  # when ledger is present
```

- The child:
  - MUST set `task_launch_mode` to match the outbound `launch_mode` it observed in its hand-off.
  - MUST set `pipeline_profile` to match the outbound `pipeline_profile` it observed in its hand-off (this is how Layer 2 **confirms** which speed tier it actually honored).
  - MUST set `contract_satisfied` to `false` whenever:
    - It skipped a mandatory step it was contracted to perform, or
    - It encountered an unrecoverable error that prevents it from fulfilling its contract.

**Parent-side enforcement**

- The parent harden pass (caller of Task) MUST:
  - Inspect `task_harden_result` on the child’s return.
  - **Refuse** to upgrade a run to full `Success` when:
    - `contract_satisfied: false`, **and**
    - the corresponding helper was mandatory under the active profile, or the pipeline contract labels it “hard gate”.
  - In such cases, it MUST:
    - Mark the parent status as `#review-needed` or `failure`, and
    - Ensure that Layer 1 does not add the originating queue entry to `processed_success_ids` when strict nested gates are enabled.

### 4. Error logging and observability hooks

**Errors.md integration**

- On the **first failure per subagent type** in a run (e.g. `roadmap`, `validator`, `research`, `internal-repair-agent`, `prompt_craft`), the harden pass SHOULD:
  - Append an Errors.md entry summarizing:
    - The attempted `subagent_type`.
    - The host error (`host_error_class`, `host_error_raw`) captured from Task.
    - Whether a `generalPurpose` fallback was attempted and with what outcome.
  - Use `error_type` such as `task_dispatch_failure` or `task_enum_missing`.

**Task-handoff-comms.jsonl**

- The harden pass MUST continue to log every Task call as described in [[3-Resources/Second-Brain/Docs/Task-Handoff-Comms-Spec|Task-Handoff-Comms-Spec]], and additionally:
  - Include `launch_mode` in the JSONL rows (e.g. in a field such as `launch_mode` or within a small `task_harden` object).
  - On `return_in`, include:
    - The parsed `contract_satisfied` flag when present.
    - Any `fallback_reason` (e.g. `helper_not_selected_for_profile`, `task_enum_missing`, `generalPurpose_fallback_failed`).

**Watcher-Result neutrality**

- When a pipeline is degraded because:
  - A mandatory helper was blocked by host capabilities, or
  - A `generalPurpose` fallback failed and the contract remained unsatisfied,
  - the parent MUST keep **Watcher-Result** lines human-neutral but:
    - Include a short machine tag in the `trace` or message such as:
      - `launch_mode=generalPurpose_fallback`,
      - `contract_satisfied=false`,
      - `mandatory_helper_unavailable=validator`.

### 5. Layered responsibilities

- **Layer 0 (chat / manual entry)**
  - MUST use the Task harden pass when launching `Task(subagent_type: "queue")` for EAT-QUEUE / PROCESS TASK QUEUE.
  - MUST run the capability probe once per conversation and pass the resulting capabilities snapshot to Layer 1 as part of the queue hand-off (e.g. under a telemetry or `task_harden_caps` section).

- **Layer 1 (Queue/Dispatcher)**
  - MUST use the provided capabilities snapshot (and update it if it runs additional probes) to decide:
    - Whether to launch `Task(roadmap)`, `Task(validator)`, etc. natively,
    - Whether to attempt an optional `generalPurpose` fallback, or
    - Whether to treat a helper as out-of-graph under the active profile.
  - MUST apply stricter behavior when `queue.strict_nested_return_gates` is enabled:
    - No consuming of entries as `Success` when a mandatory helper shows `contract_satisfied: false` or a required step was skipped.

- **Layer 2 (pipeline subagents and nested helpers)**
  - MUST treat `task_harden_metadata` in their hand-offs as **read-only context**:
    - They MUST NOT re-probe capabilities on their own.
    - They MUST respect `expected_contract` when populating `contract_satisfied`.
  - MUST emit clear `nested_subagent_ledger` entries (where applicable) that distinguish:
    - `invoked_ok` / `task_error` for **native** helper calls.
    - `invoked_ok` / `task_error` for **generalPurpose** fallback calls.
    - `not_applicable` / `skipped` when the host could not supply any Task channel and the helper was not mandatory for this profile.

### 6. Guardrails to prevent capability “lies”

- No agent MAY:
  - Claim that `Task(roadmap)` or `Task(validator)` (or any other enumerated subagent) is unavailable **without**:
    - A prior probe result in the capabilities cache, and
    - A recorded `raw_errors[type]` / Task-Handoff-Comms pair showing the rejection.
- No agent MAY:
  - Report a pipeline run as fully `Success` when a **mandatory** nested helper for that run:
    - Was not launched (no Task-Handoff-Comms pair, no ledger step), and
    - Has no allowed reason code marking it as out-of-graph for this profile.
- Any deviation from the ideal helper graph MUST:
  - Be reflected in the parent status (`#review-needed` or `failure` rather than `Success`), and
  - Leave a durable trail in **Errors.md**, `.technical/task-handoff-comms.jsonl`, `nested_subagent_ledger`, or `.technical/queue-continuation.jsonl` sufficient for later audit.

### 7. Rollout phases (non-invasive → strict → profiled)

- **Phase 1 — Non-invasive wrapper**
  - Implement the Task harden pass as a pure wrapper:
    - Run capability probes and maintain `available_subagents` / `raw_errors`.
    - Decorate hand-offs and returns with `task_harden_metadata` / `task_harden_result`.
    - Log `launch_mode` and basic degradation markers, but:
      - **Do not** yet change success/failure semantics; treat metadata as advisory.

- **Phase 2 — Strict gating**
  - Enable strict enforcement for mandatory helpers:
    - Block `Success` when `contract_satisfied: false` on a mandatory contract.
    - Treat missing Task calls for mandated helpers as structural violations under strict nested gates.

- **Phase 3 — Configurable profiles**
  - Tie the helper graph and strictness into [[3-Resources/Second-Brain-Config|Second-Brain-Config]]:
    - Use config keys such as `pipeline_mode` and `queue.strict_nested_return_gates` to select `fast` / `balance` / `extreme`.
    - Allow high-safety profiles to require maximal helpers and strict gating.
    - Allow experimental or low-safety profiles to run with a smaller helper set and softer fallbacks (while still never falsifying helper usage in logs).

## Reusable Task-launch preamble (for hand-off prompts)

When defining hand-off prompts for Task-based subagents (Layer 0 → Layer 1, Layer 1 → pipelines, Layer 2 → nested helpers), agents SHOULD include or reference the following preamble (adapted to the specific subagent name and type):

> You MUST treat yourself as having been launched via the Cursor Task tool with `subagent_type: "<name>"`.  
> Do NOT claim that the Task tool or this `subagent_type` is unavailable – you must assume the call succeeded, and if anything failed it will appear as a concrete Task error outside your context.  
> Do NOT silently simulate other pipelines or helpers; if validation or repair work is required, it is performed only via your own skills or via nested Task calls that are recorded in the nested_subagent_ledger and Task-Handoff-Comms logs.

Agent files under `.cursor/agents/` and queue / pipeline rules SHOULD reference this preamble (by name) instead of inventing new, weaker language about “trying” to call Task. All three observability pillars – `nested_subagent_ledger`, `Task-Handoff-Comms`, and Run-Telemetry – rely on this invariant.

---

## Mandatory hand-off prompt structure

When the main agent delegates, it MUST prefix the delegation with this structure (copy-paste into every delegation):

```
You are now the {subagent-name} subagent.
Task: {clear one-sentence goal}

Original request / queue entry: {full queue JSON or user prompt excerpt}

**Telemetry (copy into your Run-Telemetry note):** parent_run_id: "<uuid>", queue_entry_id: "<entry.id>", project_id: "<id or '-'>", timestamp: "<ISO8601>", pipeline_task_correlation_id: "<uuid>"
(The primary always populates these in every hand-off; use them as the required fields for your Run-Telemetry note. **pipeline_task_correlation_id** is generated by Layer 1 when dispatching this pipeline `Task`; copy it into comms rows for this run and use it as **parent_task_correlation_id** on every **nested helper** `Task` (validator, IRA, research) per [[3-Resources/Second-Brain/Docs/Task-Handoff-Comms-Spec|Task-Handoff-Comms-Spec]].)

Critical invariants you MUST enforce:
• Always create backup + per-change snapshot before any destructive MCP action (move, rename, write, append, split, etc.)
• Respect confidence gates exactly as defined in Parameters.md
• Use shared Error Handling Protocol on failure
• Write to Watcher-Result.md in the exact one-line format with requestId
• For roadmap: read roadmap-state.md and workflow_state.md first; append log row before returning

Relevant state files (read them now):
{list of 2–5 most important paths, e.g. roadmap-state.md, Task-Queue.md, ...}

Vault layout reference: [[3-Resources/Second-Brain/Vault-Layout]]

Execute the task. Return only:
• One-paragraph summary of what you did
• Any new Decision Wrapper path or queue entry created
• Explicit Success / failure / #review-needed status (required so the queue processor can add this entry's id to processed_success_ids on success and clear it at A.7). Use exact phrases **Success** or **failure** or **#review-needed** so the queue processor can set Run-Telemetry success and optional error_category.
• **Optional:** A **chain_request** object (see § Subagent chaining) if this run needs work from another pipeline before it can finish; the primary will run dependencies then re-launch this subagent with results.
• **RoadmapSubagent — queue continuation:** End the return with a **fenced YAML** block rooted at **`queue_continuation:`** per [[3-Resources/Second-Brain/Docs/Queue-Continuation-Spec|Queue-Continuation-Spec]] (schema_version 1) on every run so Layer 1 can append **`.technical/queue-continuation.jsonl`** and run **empty-queue bootstrap** when configured.
• **RoadmapSubagent — `queue_followups` (RESUME_ROADMAP):** When the queue entry is **`RESUME_ROADMAP`** (chain: **primary** segment) and **`params.queue_next !== false`** (absent = true) and you return **Success**, you **MUST** include **`queue_followups.next_entry`** in the Task return text so Layer 1 **A.5c** can **read-then-append** — unless a **terminal** stop in [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]] § **`effective_followup_required`** applies. Set **`queue_continuation.suppress_followup: false`** when **`next_entry`** is present. If **`next_entry`** is omitted without a terminal reason, Layer 1 **A.5c.1** may synthesize a line (Config **`queue.synthesize_followup_when_queue_next_true`**) and log **`queue_next_contract_violation_recovered`**. Full checklist: [[.cursor/agents/roadmap|agents/roadmap.md]] § Return.
• **Pipeline return metadata (little val + validator):** When you are a **pipeline** subagent (ingest, roadmap, distill, express, archive, organize, research) and you return **Success**, you **MUST** include in your return: **(1)** `little_val_ok: true` or `little_val_ok: false` (true only when the final little val verdict for this run was `ok: true`). **(2)** When `little_val_ok: true`, a **validator_context** object that describes what you validated: `validation_type` (string, per Queue-Sources § Post-pipeline validator), `project_id` (or "-"), and the type-specific params required by the Validator rule for that validation_type (e.g. source_file, proposed_path, para_type, ingest_conf for ingest_classification; source_file for distill_readability; project_id and state paths for roadmap_handoff_auto; synth_note_paths for research_synthesis). You MAY also include `validator_first_pass` metadata (severity, recommended_action, report_path) from your nested validator call so the queue can compare its own hostile pass. When **profile safety escalation** applies ([[3-Resources/Second-Brain/Docs/Pipeline-Validator-Profiles|Pipeline-Validator-Profiles]] §5), set **`validator_context.force_layer1_post_lv: true`** so Layer 1 **does not** profile-skip post–little-val on roadmap-class dispatches. Pipelines that do not use little val (e.g. research) set `little_val_ok: true` when the run succeeded and provide validator_context when a validation_type applies.
• **Validator hard-block explanation (required when severity is high):** If your nested validator (or any validator you ran as part of the pipeline) returned **`severity: "high"`** or **`recommended_action: "block_destructive"`**, you MUST include **one sentence** in your return explaining **why** it is a hard block (e.g. “Hard block because contradictions make the plan non-executable.”). This applies even when your overall status is **#review-needed** (i.e., do not hide the rationale behind “validator_context omitted”). **Do not treat `recommended_action: "needs_work"` as a hard block**; it is non-blocking guidance.

• **Tiered nested validator Success gate (pipelines):** After the **final** nested ValidatorSubagent pass for this run: **never** return **Success** if **`severity: "high"`** or **`recommended_action: "block_destructive"`**. When **Second-Brain-Config** `validator.tiered_blocks_enabled` is **true** (default), you **may** return **Success** if the final verdict is **`recommended_action: "needs_work"`** with **`severity: medium`** (or low) and **not** `block_destructive`, **and** final little val is `ok: true` (for CODE pipelines). This applies most strictly to **`roadmap_handoff_auto`** per [[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Spec|Validator-Tiered-Blocks-Spec]] §3; other `validation_type`s use the same pattern when they emit `needs_work` without high/block. When **`validator.tiered_blocks_enabled`** is **false**, still block Success only on **`high`** / **`block_destructive`** (unchanged). **Return metadata on hard block:** include **`blocked_scope`** `{ project_id, phase_ids?, paths? }` and optional **`validator_primary_code`** when available.

• **Queue (Layer 1) — repair-first (no IRA):** After a pipeline returns Success with `little_val_ok: true` and `validator_context`, when the post–little-val Validator returns **`high`** / **`block_destructive`** or **`primary_code`** in the hard-block set (`contradictions_detected`, `state_hygiene_failure`, `incoherence`, `safety_critical_ambiguity`), the Queue **appends** a **repair** JSONL line (e.g. `RESUME_ROADMAP` with `params.action: recal` or `handoff-audit`, same `project_id`, `user_guidance` citing report path) with **`queue_priority: repair`** (or **`validator_repair_followup: true`**) and **re-sorts** so repair runs **before** other `RESUME_ROADMAP` **deepen** lines for that `project_id`. See Queue-Sources and `queue.mdc`. Queue **never** invokes IRA.

• **validator_context inclusion (best-effort):** Even when returning **#review-needed** or **failure**, include `validator_context` when you have it (so the Queue/Dispatcher can reuse it for consistent follow-up validation or auditing). `validator_context` is strictly **required** for **Success** when `little_val_ok: true`, but it is **recommended** for non-success returns as well.
• **Pipeline subagents — nested_subagent_ledger (required):** On **every** final return for queue-dispatched pipelines that use nested helpers (**`ROADMAP_MODE`**, **`RESUME_ROADMAP`**, **`INGEST_MODE`**, **`ARCHIVE MODE`**, **`ORGANIZE MODE`**, **`DISTILL_MODE`** / **`BATCH_DISTILL`**, **`EXPRESS MODE`** / **`BATCH_EXPRESS`**, **`RESEARCH_AGENT`** / **`RESEARCH_GAPS`**), include a **fenced YAML** block rooted at **`nested_subagent_ledger:`** per [[3-Resources/Second-Brain/Docs/Nested-Subagent-Ledger-Spec|Nested-Subagent-Ledger-Spec]] (`ledger_schema_version: 1`). Populate **`steps`** in **execution order**; **never** omit the block when claiming **Success** with **`little_val_ok: true`** (exempt subcases use explicit **`not_applicable`** rows per spec). Record **`task_error`** with **verbatim** `host_error_raw` (sanitized per spec) when Cursor `Task` rejects nested `subagent_type` or returns `resource_exhausted`. Record **`skipped`** / **`not_applicable`** with verbose **`detail.reason_code`** and **`detail.human_readable`**. Write the same content into the pipeline **Run-Telemetry** note body under **`## Nested subagent ledger`** (Summary, Steps, Raw YAML) per that spec.
• **Host nested Task failure:** If a nested **`Task(validator)`**, **`Task(internal-repair-agent)`**, or **`Task(research)`** fails or is unavailable, **do not** return **Success** with fake **`validator_context`** or an empty ledger. **Attempt** the nested **`Task`** before asserting unavailability; record **`outcome: task_error`** with **`host_error_raw`** and **`host_error_class`** (e.g. **`nested_task_unavailable`**) — **not** **`skipped`** with **`task_tool_invoked: false`** when that helper step was **required** (see [[3-Resources/Second-Brain/Docs/Nested-Subagent-Ledger-Spec|Nested-Subagent-Ledger-Spec]]). Return **`failure`** or **`#review-needed`** with those ledger rows so Layer 1 and operators can see the gap.
• **Layer 1 strict nested return gates (Config):** When [[3-Resources/Second-Brain-Config|Second-Brain-Config]] **`queue.strict_nested_return_gates`** is **true**, the Queue **must not** add the queue entry to **`processed_success_ids`** when the pipeline return claims success with **`little_val_ok: true`** but **`validator_context`** is missing or invalid for that mode, or when **`nested_subagent_ledger`** violates **Attestation invariants** (hollow **`invoked_ok`** / **`invoked_empty_ok`** with **`task_tool_invoked: false`** on mandated helper steps — see `queue.mdc` **A.5 (b0)(iii)**), or when **(b0)(iv)** detects **`skipped`** + **`task_tool_invoked: false`** on a **required** mandated helper step without an allowlisted **`detail.reason_code`** (**`error_type: ledger_nested_helper_skip_without_attempt`**). When strict gates are **true**, **(b0)(iv)** also runs on **`#review-needed`** with **`little_val_ok: true`** so structurally “green” review returns cannot bypass skip-without-attempt detection. When **`queue.strict_nested_ledger_all_pipelines`** is **true**, the same applies for missing or unparseable **`nested_subagent_ledger`** on gated modes. Default **false** preserves legacy skip-and-consume until operators opt in. Continuation log rows for attestation failure use **`suppress_reason: nested_attestation_failure`** ([[3-Resources/Second-Brain/Docs/Queue-Continuation-Spec|Queue-Continuation-Spec]]).
```

---

## Nested subagent ledger (observability)

**All queue-dispatched pipeline subagents** that invoke nested Validator / IRA / Research **MUST** emit **`nested_subagent_ledger`** on every run (Success, **#review-needed**, or **failure**), per [[3-Resources/Second-Brain/Docs/Nested-Subagent-Ledger-Spec|Nested-Subagent-Ledger-Spec]] (normative scope). **RoadmapSubagent** remains subject to the same schema plus roadmap-specific step ids.

**Task hand-off comms (nested helpers):** Before and after **each** nested **`Task(validator)`**, **`Task(internal-repair-agent)`**, or **`Task(research)`**, the **pipeline** MUST append **`handoff_out`** and **`return_in`** records to **`.technical/task-handoff-comms.jsonl`** per [[3-Resources/Second-Brain/Docs/Task-Handoff-Comms-Spec|Task-Handoff-Comms-Spec]], with **`parent_task_correlation_id`** = **`pipeline_task_correlation_id`** from this run’s Layer 1 hand-off. Respect **`task_handoff_comms.enabled`** in Config.

**Layer 1 (Queue)** MUST append **task hand-off comms** for each outbound `Task` it invokes (pipeline dispatch, post–little-val validator, PromptCraft, empty-queue bootstrap) to **`.technical/task-handoff-comms.jsonl`** per [[3-Resources/Second-Brain/Docs/Task-Handoff-Comms-Spec|Task-Handoff-Comms-Spec]] (paired `handoff_out` / `return_in`, full verbatim bodies after sanitization, `task_correlation_id`; for L1→L2 pipeline dispatch the hand-off **must** include **`pipeline_task_correlation_id`** equal to that correlation id). See `.cursor/rules/agents/queue.mdc`.

---

## PromptCraftSubagent (recovery queue crafting)

**Role:** **Read-mostly** helper. Turns **failure context** into **merge-aware, linted** suggested queue JSONL line(s) for recovery. **Not** a pipeline; **not** a substitute for plan-mode question-led crafter ([[3-Resources/Second-Brain/Docs/Prompt-Craft-Subagent|Prompt-Craft-Subagent]]).

**Layering (canonical):** [[3-Resources/Second-Brain/Docs/Subagent-Layers-Reference|Subagent-Layers-Reference]] — **Layer 0** = Cursor chat; **Layer 1** = Queue/Dispatcher; **Layer 2** = pipelines. PromptCraft is invoked by **Layer 0** (manual **REPAIR CRAFT** / **PROMPT CRAFT RECOVERY**) or by **Layer 1** when (a) **`recovery_auto_craft_enabled`** is **true** and a pipeline return includes **`prompt_craft_request`** (**A.5d**), or (b) **`post_little_val_repair_use_prompt_craft`** is **true** and **queue.mdc A.5b** triggers post–little-val repair craft (**hand-off:** **`craft_source: "a5b_post_little_val"`** + **`a5b_repair_context`** — see subsection below), or (c) **`queue_continuation.empty_queue_bootstrap_enabled`** and **`empty_queue_bootstrap_prompt_craft`** are **true** and **queue.mdc A.1b** selects an eligible continuation record (**hand-off:** **`craft_source: "empty_queue_bootstrap"`** + **`empty_bootstrap_context`**). **IRA** and **nested Validator** MUST NOT call PromptCraft; only L0/L1 orchestrate **`Task(prompt_craft)`**.

**Permissions:** May **read** vault notes (Config, workflow_state, roadmap-state, Errors, validator reports) via MCP **read** tools only. **MUST NOT** write `prompt-queue.jsonl`, `Task-Queue.md`, `Watcher-Result.md`, Decision Wrappers, or mutate user roadmap/ingest notes. **MUST NOT** call **`Task`** for pipelines (ingest, roadmap, …). **MUST NOT** nest Validator or IRA.

**Return (required tail):** Structured block in the return message:
- `status`: **Success** | **failure**
- `jsonl_lines_suggested`: string[] (each a single-line JSON object) or `jsonl_line_suggested` (string)
- `warnings`: string[]
- `lint_blockers`: string[] — non-empty ⇒ **Layer 1 MUST NOT append** suggested lines
- `effective_params_preview`: object (optional; merged preview for audit)
- `recovery_metadata`: `{ error_correlation_id, suggested_modes[], rationale_short }` (optional)

**Layer 1 append:** Only **Layer 1** performs **read → append → write** on `.technical/prompt-queue.jsonl` after PromptCraft returns. Use **`idempotency_key`** on appended lines (e.g. `"<error_correlation_id>-prompt-craft"`). Cap auto PromptCraft invocations per correlation: **`max_prompt_craft_per_correlation_per_run`** — for **A.5d**, key = **`error_correlation_id`**; for **A.5b**, key = **`<queue_entry_id>-post-little-val-repair`**; for **A.1b** bootstrap, **`idempotency_key`** is fixed by Layer 1 as **`bootstrap_key`** (see **Empty-queue bootstrap** subsection).

### A.5b hand-off (`craft_source: a5b_post_little_val`, Layer 1 → PromptCraft)

When **queue.mdc A.5b.2** runs, the Queue builds a PromptCraft **prompt** that includes:

- **`craft_source`**: **`"a5b_post_little_val"`**
- **`error_correlation_id`**: **`<queue_entry_id>-post-little-val-<ISO8601>`**
- **`a5b_repair_context`**: object with at least **`repair_policy_action`**, **`primary_code`**, **`post_little_val_report_path`**, **`validation_type`**, **`project_id`**, optional **`source_file`**, **`reason_codes[]`**, **`queue_entry_json`** (excerpt), **`triggering_queue_entry_id`**

PromptCraft returns suggested JSONL per [[3-Resources/Second-Brain/Docs/Prompt-Craft-Subagent|Prompt-Craft-Subagent]]; Layer 1 **normalizes** **`queue_priority`**, **`validator_repair_followup`**, and **`incoherence_retries_remaining`**, then appends or falls back to **A.5b.3** minimal line.

### Empty-queue bootstrap hand-off (`craft_source: empty_queue_bootstrap`, Layer 1 → PromptCraft)

When **queue.mdc A.1b** runs with **`empty_queue_bootstrap_prompt_craft: true`** and selects a continuation record from **`.technical/queue-continuation.jsonl`**, the Queue builds a PromptCraft **prompt** that includes:

- **`craft_source`**: **`"empty_queue_bootstrap"`**
- **`error_correlation_id`**: **`empty-bootstrap-<ISO8601>`** (or run-scoped id; used for **`recovery_metadata`** only)
- **`empty_bootstrap_context`**: object with at least **`continuation_record`** (full parsed JSON object from the log), **`bootstrap_key`** (`empty-bootstrap-<queue_entry_id>-<completed_iso|na>`), optional **`bootstrap_tail_excerpt`**, plus standard vault root and telemetry (**`parent_run_id`**, **`queue_entry_id`**, **`project_id`**)

PromptCraft returns one suggested JSONL line with **`idempotency_key`** equal to **`bootstrap_key`**; Layer 1 uses it as the bootstrap **candidate** when **`lint_blockers`** is empty, else falls back to deterministic **A.1b** step 8. Append vs trace-only follows **`empty_queue_bootstrap_auto_append`**.

### `ira_repair_bundle` and `prompt_craft_request` (Layer 2 → Layer 1)

When a **Layer 2** pipeline exits **`failure`** or **`#review-needed`** after **IRA** ran in that Task and **post-IRA nested Validator** still indicates a hard block or unresolved structural failure, the pipeline **SHOULD** end its return with a **machine-readable block** so Layer 1 can optionally invoke PromptCraft.

**Canonical field name:** **`ira_repair_bundle`** (object). Optional working alias in docs: *IRA output bubble* — same meaning.

**Suggested YAML trailer** (fenced `yaml`, at end of return):

```yaml
prompt_craft_request:
  suggest_prompt_craft: true
  error_correlation_id: "<queue_entry_id>-<ISO8601>"
  failure_envelope:
    pipeline: roadmap
    stage: post_nested_validator
    error_type: structural|validator_hard_block|...
    message_sanitized: "<short string>"
    affected_paths: ["1-Projects/.../Roadmap/workflow_state.md"]
    queue_entry_json: { }  # optional excerpt
    validator_report_path: ".technical/Validator/..."
  ira_repair_bundle:
    ira_report_path: ".technical/Run-Telemetry/..."  # or inline summary
    suggested_fixes_excerpt: "<short>"
    nested_validator_primary_code: "<code>"
    nested_severity: high|medium|low
  craft_intent: "<one line what recovery should achieve>"
```

Layer 1 **parses** this block only when **recovery_auto_craft_enabled** is **true** in Config; otherwise operators may still use Layer 0 **REPAIR CRAFT** with the same fields pasted manually. See [[3-Resources/Second-Brain/Queue-Sources#PromptCraft recovery|Queue-Sources § PromptCraft recovery]].

### Recovery outcome Validator (after crafted lines run)

After Layer 1 has **appended** PromptCraft lines and EAT-QUEUE has **executed** that recovery package, Layer 1 (or Layer 0) **MAY** dispatch **`VALIDATE`** with **`params.validation_type: "recovery_outcome"`** to answer: given **before state**, **crafted plan**, **after state** — **did the failure clear?** See [[3-Resources/Second-Brain/Validator-Reference|Validator-Reference]] § **recovery_outcome**. PromptCraft does **not** run this pass.

---

## Subagent chaining

**Chaining rule (general):** Pipeline/validator subagents do **not** call other pipeline or validator subagents directly. When they need additional pipeline work, they append queue entries + return `chain_request`. The primary (Queue/Dispatcher) continues eating the queue, runs dependencies, then re-launches the original subagent with results + `resume_from_chain_request: true`. One logical chain = one Watcher-Result group via `chain_id`.

**Internal Repair Agent exception:** One allowed nested helper subagent call is to the **Internal Repair Agent (IRA)**:

- **Not dispatched by the Queue:** There is **no** queue mode for IRA (no `prompt-queue.jsonl` line that means “run IRA”). The **Queue/Dispatcher does not call IRA** after a validator run—not after the pipeline’s **nested** validator, and **not** after the Queue’s separate **post–little-val hostile Validator** pass (that pass **must not** trigger IRA; it **may** append **repair** JSONL lines and re-sort per `queue.mdc` **A.5b** — still **no** IRA). The **validator → IRA → apply → (little val) → second nested validator** sequence runs **entirely inside** the **same** pipeline subagent **Task** invocation, via **nested `Task` calls** from the pipeline to the IRA helper (and to ValidatorSubagent), before the pipeline returns to the Queue.
- Callers: roadmap, ingest, archive, organize, distill, express subagents **must** call IRA as a helper **after** little val has failed to reach `ok: true` for that run’s current cycle, per `internal-repair-agent.md` (up to three IRA calls per run, each followed by a fresh little val cycle) — not optional when the contract still allows repair attempts.
- **Default (Config `nested_validator.ira_after_first_pass: true`, overridable per run by queue `params.ira_after_first_pass`):** roadmap, ingest, archive, organize, distill, express, and **research** subagents **must** call IRA **exactly once** after **every** first nested ValidatorSubagent pass in that run (after `little val` has reached `ok: true` for CODE pipelines; research has no little val). Flow: **first validate → IRA → apply `suggested_fixes` (empty allowed) → little val again (CODE only) → second validate** with `compare_to_report_path`. The pipeline **must not** skip IRA on a clean `log_only` first pass when this default is on; IRA may return an empty repair plan. **Legacy opt-out:** when `ira_after_first_pass` is **false** (explicit Config or `params.ira_after_first_pass: false`), skip IRA **and** the second validator **only if** the first pass is a clean bill of health (`recommended_action: "log_only"` with no actionable gaps); any other first-pass result still runs the full **validate → IRA → …** cycle.
- Limits: at most **three** IRA calls per pipeline run (IRA #1–#3) on the **little-val-driven** path, each followed by a fresh little val cycle; no further IRA calls after that.
- Limits (validator-to-IRA path): **exactly one** IRA invocation per such cycle; the caller must not invoke IRA again after the **final** nested validator pass of that cycle. (Preserves the “single hardened validator-to-IRA cycle” invariant.)
- Permissions: IRA is **read-only** on user artifacts (notes, logs, state files, snapshots) and may only write its own report notes and Run-Telemetry; it never touches queues, wrappers, or Watcher-Result.
- **Repair application (risk levels):** Pipeline subagents apply IRA `suggested_fixes` at **any** `risk_level` (`low` / `medium` / `high`) when global **core-guardrails** and that pipeline’s gates pass (backup, per-change snapshot before destructive or structural steps, confidence bands, exclusions). `risk_level` signals blast radius and preferred ordering (typically apply `low` before `medium` before `high`); it is **not** a rule that medium/high fixes must be deferred to a later run. If one suggested fix cannot satisfy its gates, skip **that** fix, log `#review-needed` with `risk_level` and reason, and continue with the rest.
- No further nesting: IRA itself must not call any other subagent (including Validator); it may only use skills.

**Validator nested-call exception:** A second allowed nested helper subagent call is to the **ValidatorSubagent**; this nested hostile gate is **mandatory** for all pipelines that mutate notes/state:

- Callers: roadmap, ingest, archive, organize, distill, express, **and research** **MUST** call ValidatorSubagent **at least once per run** *after* little val has reached `ok: true` for that run’s current cycle (for research, which does not use little val, the call is mandatory whenever a `validation_type` applies, e.g. synthesized notes exist).
- **Mandatory second pass** when the default IRA-after-first-pass policy applies (or when the first pass was not clean under legacy mode): the pipeline **MUST** call ValidatorSubagent a **second** time in the same run after IRA + apply (+ little val for CODE pipelines). The second pass must include `compare_to_report_path` pointing to the first validator report. **Research:** no little val between IRA and second validator; flow is first validate → IRA → apply → second validate.
- Purpose: run a hostile validation pass on the artifacts produced by this run (e.g. ingest classification, distill readability, express summary, archive candidate, organize path, roadmap handoff auto, research synthesis) **before** claiming Success. No sampling or config switches may skip this nested validator call.
- Permissions: ValidatorSubagent remains **read-only** on inputs and may only write its own report note and Run-Telemetry; it never touches queues, wrappers, or Watcher-Result.
- No further nesting: ValidatorSubagent itself must not call any other subagent (including IRA or Research); it may only use skills.

**Research nested-call exception:** A third allowed nested helper subagent call is to the **ResearchSubagent**; this is a bounded helper for inline research, distinct from queue-dispatched `RESEARCH_AGENT` / `RESEARCH_GAPS` modes:

- Callers: roadmap, ingest, archive, organize, distill, and express subagents **may** call ResearchSubagent as a helper when an inline research pass is explicitly enabled for that run (e.g. pre-deepen research, scoped PMG research, or a crafted research flag).
- Limits: at most **two** ResearchSubagent calls per pipeline run (e.g. one primary inline research pass and, optionally, one gap-fill pass). No further ResearchSubagent calls are allowed after that.
- Shape: Nested usage must remain `main → queue → pipeline → research` only. ResearchSubagent must not call other **pipeline** subagents; it **must** call **ValidatorSubagent** and **IRA** when the mandated `research_synthesis` validator→IRA→second-validator cycle applies (see Research agent and this contract § IRA / Validator exceptions).
- Permissions: ResearchSubagent is **read-only** on core project artifacts (PMG, roadmap-state, phase notes, logs, snapshots) and may only write:
  - synthesized research notes and raw notes under `Ingest/Agent-Research/**`, and
  - its own Run-Telemetry note under `.technical/Run-Telemetry/`.
  It must never touch queue files, Decision Wrappers, or Watcher-Result.
- Outputs: When called as a nested helper, ResearchSubagent must return structured **research consumables** (e.g. `injection_block_markdown`, `synth_note_paths`, `key_takeaways`) only; the caller is responsible for integrating these into its artifacts or queuing follow-ups, under the existing safety and validator contracts.

### Dependent Helper Serialization Rule

Dependent chains such as Validator → IRA → second Validator (and any Research validator→IRA→validator synthesis cycle) **must execute sequentially within a single pipeline invocation**.

- Launch `Task(validator)` for the first pass and **await its full structured return** (including severity, primary_code, reason_codes, gap_citations, report_path).
- Use that validator output as **direct input** when launching `Task(internal-repair-agent)` for `ira_post_first_validator`.
- After the IRA returns, run post-IRA little_val, then (when required) launch the second `Task(validator)`.
- Parallel fan-out remains allowed **only** for truly independent local analysis (e.g. multiple unrelated research lookups). It is **not** permitted for the Validator/IRA dependent protocol in balance or extreme modes.

Ledger steps (`nested_validator_first`, `ira_post_first_validator`, `nested_validator_second`) must show non-overlapping `started_iso` / `ended_iso` windows consistent with sequential execution. Overlapping or out-of-order dependent helper timestamps are a contract violation and must be surfaced as `#review-needed` with `detail.reason_code: nested_helper_order_violation`.

**Nested helper ledger attestation:** Pipeline subagents that emit **`nested_subagent_ledger`** must record nested IRA, Validator, and Research **`Task`** invocations honestly per [[3-Resources/Second-Brain/Docs/Nested-Subagent-Ledger-Spec|Nested-Subagent-Ledger-Spec]] **Attestation invariants**; false-green combinations (e.g. **`invoked_ok`** or **`invoked_empty_ok`** with **`task_tool_invoked: false`** on mandated helper steps when those helpers were required) are **invalid** and must not accompany **Success** with **`little_val_ok: true`**. The same applies to **`skipped`** + **`task_tool_invoked: false`** on a **required** step unless **`detail.reason_code`** is allowlisted; use **`task_error`** + **`host_error_raw`** / **`host_error_class`** when **`Task`** is missing or fails (`queue.mdc` **A.5 (b0)(iv)**).

**Rule (Cursor limitation):** Aside from the explicit **IRA**, **Validator**, and **Research** nested-call exceptions above, no subagent ever runs another pipeline or \"calls\" another subagent. If it needs work from another pipeline, it (1) creates the queue items that will produce the required results, (2) pauses and returns a **chain_request** to the primary with current pipeline results up to the request and requested context, (3) primary runs the requested subagent(s), (4) primary re-launches the first subagent with the second agent's results so it can complete its steps, (5) primary continues execution (clear entry, Watcher-Result, next entry).

**chain_request schema (authoritative):**

```yaml
chain_request:
  type: object
  properties:
    requested_pipelines: array of strings   # e.g. ["RESEARCH_AGENT", "INGEST_MODE"]; ordered list to run
    context: object                        # arbitrary JSON-safe data to pass forward (project_id, linked_phase, params, etc.)
    partial_result: string | object        # summary or structured data for resume (roadmap state up to request, etc.)
    queue_items_appended: boolean | array # true = subagent already wrote queue lines; array = optional ids of appended entries
  required: [requested_pipelines, context]
```

**Primary parsing:** Primary MUST treat `requested_pipelines` as the **ordered list of dependencies** to run. If `queue_items_appended` is true, primary assumes the subagent already wrote the corresponding lines to `.technical/prompt-queue.jsonl` and **continues eating from the current position**. Otherwise primary can synthetically dispatch using `context`. **Preferred:** subagents append real queue entries; primary does not synthetic-dispatch.

**Preferred implementation (Option A, post-orchestration):** Subagents **DO NOT** write queue files. On `chain_request`, the primary (Queue/Dispatcher) is the **only** component that appends to `.technical/prompt-queue.jsonl` and/or dispatches dependencies. The recommended flow is:

1. Subagent returns `chain_request` with `requested_pipelines` and `context`. It sets `queue_items_appended: false` (or omits it).
2. Primary appends dependency entries (or dispatches them directly) using `requested_pipelines` and `context`, then continues processing them in order.
3. After dependencies complete, primary re-dispatches the original entry to the first subagent with `resume_from_chain_request: true` and includes collected dependency results in the hand-off.
4. Only after the first subagent’s second return (success) does primary add the original entry id to `processed_success_ids` and clear at A.7.

**Idempotency:** Subagents SHOULD append queue items with a unique **idempotency_key** (e.g. `idempotency_key: "<original_entry_id>-research-pre-deepen"`). Queue processor deduplicates on read for the current logical run: if an entry's idempotency_key matches one already processed in this run (or in processed_success_ids for this chain), skip or merge instead of running again.
**Idempotency (post-orchestration):** Since subagents do not write queue lines, the **primary** should add `idempotency_key` when it appends dependency entries requested by a chain (e.g. `"<original_entry_id>-research-pre-deepen"`). Subagents may still recommend an idempotency_key value in their `chain_request.context`.

**Watcher-Result for chains:** When the current entry is part of a chain, append a Watcher-Result line that includes **chain_id** (original queue entry id that triggered the chain) and **segment** (mode of the current entry, e.g. RESEARCH_AGENT, RESUME_ROADMAP). Example: `requestId: abc123 | chain_id: queue-456 | segment: RESEARCH_AGENT | status: success | message: "..." | trace: "" | completed: <ISO8601>`.

---

## Critical invariants (every subagent)

- **Validator read-only:** Validator subagents **MUST** be read-only on all input artifacts (state files, phase notes, logs) except the **explicit output path** (the report or verdict note). No edits to inputs; only the single report/output file may be created or written.
- **Backup:** Before any destructive operation, ensure backup (`obsidian_ensure_backup` or `obsidian_create_backup`). If backup fails, abort destructive steps for that note, log with #review-needed. (Validator creating a new report file is exempt from backup when that is the only write.)
- **Per-change snapshot:** Before move, rename, split, structural distill, append_to_hub, call obsidian-snapshot (or equivalent) with type per-change when confidence ≥85%. If snapshot fails, skip the destructive action, log #review-needed.
- **Confidence bands:** High (≥85%): allow destructive action after snapshot. Mid (68–84%): at most one non-destructive refinement loop; then snapshot + proceed only if post_loop_conf ≥85%; else create Decision Wrapper. Low (<68%): no destructive action; create Decision Wrapper.
- **little val structural check (false-success guard):**
  - Every pipeline subagent that mutates state or notes for a queue entry (ingest, roadmap, archive, organize, distill, express, **and research when it writes synthesized notes**) **MUST** run the shared little val structural skill **once per run**, after it believes its core work is complete and before it returns a final status. (ResearchSubagent itself may treat a successful run that created synthesized notes as `little_val_ok: true` when little val is not wired for research content, but it must still participate in the validator contracts below.)
  - Callers must pass mode, effective params, ids (`queue_entry_id`, `project_id`, optional `parent_run_id`), and the pipeline-specific artifact paths (logs, state files, target notes, snapshots) as defined in the little val rollout plans.
  - **Final-success invariant:** A pipeline subagent **MUST NOT** return **Success** when the last little val verdict for this run is `ok: false`. Success is only allowed when the final little val verdict is `ok: true`.
  - On `ok: false`, the caller treats this as a potential **false success / structural glitch**:
    - Use `missing[]` + `hint` from little val to attempt targeted structural repair (e.g. append missing log row, backfill metrics, record snapshot marker) and re-run little val.
    - Allow up to the configured **3 little val attempts per cycle** inside the run; if any attempt yields `ok: true`, the run may be returned as Success but should log that a contract glitch was repaired (e.g. `contract_glitch_repaired: true`, `lv_attempts: N`).
    - If, after the allowed attempts, little val still returns `ok: false`, the subagent must **not** claim Success until it has followed `internal-repair-agent.md` (up to three IRA calls per run, each followed by a fresh little val cycle) when that contract still allows repair attempts; only then may it return `#review-needed` or `failure` with a structural-glitch flag.
- **Error Handling Protocol:** On failure, append to 3-Resources/Errors.md (heading, table, Trace, Summary), one-line ref in pipeline log, create error Decision Wrapper under Ingest/Decisions/Errors/ when appropriate.
- **Watcher-Result:** When the delegation prompt includes `requestId`, append one line to 3-Resources/Watcher-Result.md: `requestId: <id> | status: success|failure | message: "..." | trace: "..." | completed: <ISO8601>`.
- **Queue clearing:** Only the Queue/Dispatcher (primary) agent removes processed entries from `.technical/prompt-queue.jsonl` (by omitting lines whose id is in processed_success_ids at step A.7). Subagents may **append** lines only; they must not remove or rewrite the entry they were invoked for. The primary must add that entry's id to processed_success_ids when the subagent returns success. **For chained runs:** the "processed" entry is the **original** chain entry; it is only added to processed_success_ids after the first subagent has been re-invoked (with resume_from_chain_request and collected dependency results) and has returned successfully the second time.
- **Queue clearing / mutation:** Only the Queue/Dispatcher (primary) agent reads/writes `.technical/prompt-queue.jsonl` and `3-Resources/Task-Queue.md`. Subagents must not read or write queue files. The primary removes processed entries by omitting ids in `processed_success_ids` at step A.7. Any follow-ups (next RESUME_ROADMAP, RECAL-ROAD, dependencies for chain_request) are appended by the primary based on subagent return metadata.
- **Run-Telemetry:** Before returning, subagents SHOULD write one Run-Telemetry note to `.technical/Run-Telemetry/` with **required** fields (actor, project_id, queue_entry_id, timestamp; parent_run_id from hand-off) and **any optional fields you have**; omit the rest. See [[3-Resources/Second-Brain/Vault-Layout]] § .technical/Run-Telemetry and [[3-Resources/Second-Brain/Logs#Run-Telemetry|Logs § Run-Telemetry]].
- **Post–little-val hostile validator (queue-level double-check):** The queue **MUST** run the **ValidatorSubagent** once per pipeline run **after** the pipeline returns Success **and** `little_val_ok: true`, using `validator_context` from the pipeline’s return — **except** when **`queue.mdc` A.5 (b1a)** profile gate **skips** L1 for **roadmap-class** entries per [[3-Resources/Second-Brain/Docs/Pipeline-Validator-Profiles|Pipeline-Validator-Profiles]] (`l1_post_lv_policy`). **Non-roadmap** pipelines and **`validator_context.force_layer1_post_lv: true`** always run L1 when other gates pass. This pass is an **independent hostile check**; it MUST be read-only on inputs. When L1 runs after **`force_layer1_post_lv`**, **Watcher-Result** (**`segment: VALIDATE`**) **`message`** **must** begin with **`profile_escalation_full_validation:`** (per `queue.mdc`). **Legacy path:** If `validator_context` is missing, `queue.mdc` may skip this pass and still consume the entry unless **`queue.strict_nested_return_gates`** is **true**. See Queue-Sources § Post-pipeline validator, `queue.mdc` **A.4z** / **(b1)**, Parameters § Pipeline validator profiles.

---

## Roadmap I/O abstraction (conceptual)

- **Purpose**: To keep roadmap logic stable while allowing either Obsidian MCP or inline edits as the underlying mutation mechanism, roadmap skills should behave as if they are calling into a small, abstract “filesystem” interface rather than hard-coding MCP operations.
- **Conceptual interface** (no concrete type required; this is a behavioral contract):
  - `read_note(path)` → markdown string (or structured `{ frontmatter, body }` when needed).
  - `write_note(path, new_content, options)` → write the full new content or a structured merge into the target note.
  - `snapshot_intent(path, kind)` → best-effort signal that a per-change/batch snapshot should exist before/after a structural change (`kind: "per-change" | "batch"`), with the understanding that in MCP-less environments this may be implemented as an inline copy or logged intent instead of `obsidian-snapshot`.
  - `ensure_structure(folder_path)` → ensure parent directories exist before a move/rename-equivalent change.
- **Backends**:
  - **MCP backend** (preferred when `mcp_available: true`):
    - Implements `read_note` / `write_note` / `snapshot_intent` / `ensure_structure` using `obsidian_read_note`, `obsidian_update_note`, `obsidian-snapshot`, `obsidian_ensure_structure`, and related tools, with the full backup/snapshot gates.
  - **Inline-edit backend** (fallback when `mcp_available: false`):
    - Implements `read_note` / `write_note` using Cursor’s `Read`/`ApplyPatch` primitives on markdown files.
    - Implements `snapshot_intent` and `ensure_structure` as best-effort, non-shell operations (e.g. creating lightweight copies or directories via safe file-tool calls) while respecting confidence bands and the “no shell cp/mv/rm” rule.
- **Roadmap skills and helpers**:
  - `roadmap-deepen`, structural little val integrations, and roadmap validator glue SHOULD be written to depend only on this conceptual I/O surface:
    - They decide **what** to change (new workflow_state row, phase note edits, decisions-log bullet, etc.).
    - The chosen backend (MCP or inline) decides **how** to apply those changes to the filesystem.
  - This separation allows the roadmap subagent to switch backends based on the per-run capability probe without duplicating roadmap logic or relaxing any of the safety/validator contracts.

## Rollout and verification notes (Task force-attempt hardening)

- **Phase 1 (roadmap + queue focus):** Prefer to test this contract first on `RESUME_ROADMAP` and related roadmap-class modes. After updating docs/rules, run EAT-QUEUE on a small test queue; confirm that:
  - Every roadmap dispatch that claims to have invoked nested helpers has matching Task-Handoff-Comms rows and `nested_subagent_ledger` entries with `task_tool_invoked: true` or `outcome: task_error`.
  - No run reports roadmap Success with `little_val_ok: true` when nested helpers were required but no Task-Handoff-Comms rows exist for them.
- **Phase 2 (other pipelines):** Extend the same expectations to ingest, archive, organize, distill, express, and research where they are documented to call Validator / IRA / Research as nested helpers.
- **Diagnostics:** When a run fails solely because a required Task call errored (e.g. `host_error_class: invalid_enum` or `nested_task_unavailable`), prefer clear Errors.md entries that name the failing `subagent_type` and recommend operator fixes, and ensure the originating queue entry is left unconsumed for later repair.

### Roadmap MCP fallback scenarios (verification)

- **Scenario A — MCP-healthy Task environment (baseline)**:
  - Conditions: `Task(roadmap)` runs with `mcp_available: true` (either because `mcp_probe_mode: "auto"` and the probe succeeds, or because `mcp_probe_mode: "assume_available"`).
  - Expected behavior:
    - Roadmap subagent reports `run_mode: "full_run_mcp"`.
    - Structural mutations to roadmap artifacts use Obsidian MCP tools (`obsidian_*`), with snapshots and backups enforced per core-guardrails.
    - Required nested helpers (little val, Validator, IRA, Research when applicable) appear as `invoked_ok` / `task_error` steps in `nested_subagent_ledger` with `task_tool_invoked: true`.
- **Scenario B — MCP-broken Task environment with inline fallback (deepening succeeds)**:
  - Conditions: `mcp_available: false` (either because `mcp_probe_mode: "auto"` and the probe fails, or because `mcp_probe_mode: "assume_unavailable"`), but Cursor file tools can still read/write markdown files.
  - Expected behavior:
    - Roadmap subagent reports `run_mode: "full_run_inline"`.
    - Structural mutations to roadmap artifacts are applied via inline edits (`Read`/`ApplyPatch` primitives), and no shell `cp`/`mv`/`rm` is used.
    - Little val and nested Validator/IRA/Research still run (or fail with `task_error`) and are recorded in `nested_subagent_ledger`.
    - Final-success gates are respected: Success only when the final little val verdict is `ok: true` and the final nested validator verdict is not a hard block.
- **Scenario C — MCP-broken Task environment with no safe mutations (analysis-only)**:
  - Conditions: `mcp_available: false`, and attempts to apply inline edits either fail or are blocked by safety gates (e.g. no write permissions, repeated patch conflicts).
  - Expected behavior:
    - Roadmap subagent reports `run_mode: "analysis_only"`.
    - No roadmap files are mutated; any attempted structural changes are abandoned with clear error reporting.
    - Status is `#review-needed` or `failure`, not Success; `little_val_ok` is `false` or omitted when little val could not complete.
    - Layer 1 does **not** treat this entry as fully successful; if follow-up work is needed it is explicit (e.g. via wrappers or manual guidance), not implied.

---

## References

- [[3-Resources/Second-Brain/Parameters]] — confidence_bands, thresholds
- [[3-Resources/Second-Brain/Vault-Layout]] — folder roles, protected paths
- [[.cursor/rules/always/mcp-obsidian-integration]] — Error Handling Protocol, dry_run, post-move frontmatter
