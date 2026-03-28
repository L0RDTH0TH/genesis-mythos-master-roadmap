---
name: dynamic-roadmap-params-migration-v2
overview: Second iteration of the RESUME-ROADMAP parameter migration, integrating hardening from roadmap-deepen, Parameters, Logs, and roadmap quality rules.
todos:
  - id: reconfirm-contracts
    content: Reconfirm RESUME-ROADMAP, auto-roadmap, and roadmap-deepen contracts and extract non-negotiable invariants for context tracking, RECAL, and research error handling.
    status: completed
  - id: classify-params-v2
    content: Finalize dynamic vs static vs hardened parameter classification for RESUME-ROADMAP, incorporating Grok decisions and actual skill/rule behavior.
    status: completed
  - id: design-queue-next-handoff
    content: Design precise queue_next + handoff_gate semantics that keep queue_next sticky-true and use handoff readiness as the only automated kill-switch.
    status: completed
  - id: design-dynamic-budgets-shape
    content: Design safe per-iteration derivation rules for budgets (token_cap, research caps) and depth/breadth (max_depth, branch_factor, granularity) that respect existing thresholds and gates.
    status: completed
  - id: smart-dispatch-hardened
    content: Refine smart dispatch for params.action="auto" to use state metrics and wrappers while ensuring actions remain per-iteration and not baked into future entries.
    status: completed
  - id: queue-propagation-v2
    content: Specify which params are forwarded into new RESUME-ROADMAP entries vs recomputed each iteration, and how queue_next interacts with context-util and handoff gates.
    status: completed
  - id: hardening-hooks
    content: Integrate new dynamic behavior with context-tracking postconditions, overflow/high-util RECAL gates, and research error contracts to ensure no safety regressions.
    status: completed
  - id: docs-observability-v2
    content: Plan documentation updates and logging fields to surface dynamic decisions (budgets, branch_factor, enable_research, action, queue_next suppression) in logs and MOCs.
    status: completed
  - id: rollout-validation
    content: Define and run a controlled rollout/validation strategy on a single project, then expand once hardening tests pass.
    status: completed
isProject: false
---

## Dynamic RESUME-ROADMAP Parameters Migration v2 (with Hardening)

### Goals

- **Make key RESUME-ROADMAP params dynamic per iteration** (budgets, depth/breadth, research, action selection) while respecting existing contracts.
- **Keep `queue_next` as a hard safety default** (sticky `true`), with **handoff gate + min_handoff_conf** as the only automated kill-switch for auto-looping, per Grok output.
- Integrate **hardening** from existing rules/skills/docs: context-tracking postconditions, research error contracts, RECAL gates, logging/Errors.md invariants.

### 1. Reconfirm contracts and invariants (no-behavior-regression pass)

- Re-read and align on:
  - `[3-Resources/Second-Brain/Queue-Sources.md](3-Resources/Second-Brain/Queue-Sources.md)` — RESUME-ROADMAP params, queue_next semantics, research fields.
  - `[.cursor/rules/context/auto-roadmap.mdc](.cursor/rules/context/auto-roadmap.mdc)` — RESUME-ROADMAP dispatch, action enum, smart dispatch, context-tracking default-on.
  - `[.cursor/skills/roadmap-deepen/SKILL.md](.cursor/skills/roadmap-deepen/SKILL.md)` — injected state, token_cap, branch_factor, max_depth, RECAL gates, queue_next forwarding, context-utilization gates, mandatory metrics.
  - `[3-Resources/Second-Brain/Parameters.md](3-Resources/Second-Brain/Parameters.md)` — RESUME-ROADMAP params contract, context tracking, research/gap parameters, confidence bands.
  - `[3-Resources/Second-Brain/Roadmap-Quality-Guide.md](3-Resources/Second-Brain/Roadmap-Quality-Guide.md)` — drift/RECAL behavior, phase-complete thresholds.
  - `[3-Resources/Second-Brain/Logs.md](3-Resources/Second-Brain/Logs.md)` — Error entry structure, research error format, util-spike logging.
- Explicitly list **non-negotiable invariants** for the migration (no plan step may violate these):
  - `enable_context_tracking` effective flag: **default-on**, can only be disabled by explicit `enable_context_tracking: false` on a RESUME-ROADMAP entry.
  - Context-tracking postcondition from `Parameters.md` + `roadmap-deepen`: when tracking is true, **no `"-"`** in the four context columns; missing metrics = run failure + Errors.md + queue_failed.
  - Context-utilization gate (high-util RECAL and overflow) must remain active.
  - Research error handling must continue writing standardized `research-empty` / `research-failed` / `research-skipped` entries.
  - Confidence bands and phase-complete thresholds (≥85%) remain unchanged.

### 2. Parameter classification: dynamic vs static vs hardened

- Start from the previous dynamic vs static table + Grok decisions and refine with what the code actually does:
  - **Dynamic per-iteration (recomputed in effectiveParams, not stickied in queue):**
    - Budgets: `token_cap`, `research_max_tokens`, `research_synth_cap_tokens`, `research_result_limit`.
    - Shape: `max_depth`, `branch_factor`, `batch_subphases`, `granularity`.
    - Research behavior: effective `enable_research`, use of `research_auto_keywords`, `research_util_threshold`, `research_conf_veto_threshold`, `research_cooldown`.
    - Action selection when `action: "auto"`.
  - **Static / sticky (per project or crafted run, not auto-flipped):**
    - `queue_next` (sticky-true except when suppressed by handoff gate or explicit false from crafter/wrapper).
    - `profile` name, hard caps (`context_window_tokens`), `enable_context_tracking` effective flag, highlight_angles *set* (weights can be dynamic).
    - Roadmap config thresholds (e.g. `conf_phase_complete_threshold`, `drift_score_threshold`) unless explicitly changed in Config.
  - **Hardened behavior:**
    - Any param that influences **safety gates** (snapshots, destructive vs non-destructive, context tracking on/off) must not be made dynamic in a way that bypasses the existing rules.
- Update the plan text (and later the docs) to include this classification as canonical so future refactors know which params can drift per iteration and which cannot.

### 3. Design `queue_next` + handoff gate semantics (with hardening)

- Formalize the desired behavior using current contracts:
  - `Parameters.md` + Queue-Sources: `queue_next` absent/undefined = **true**.
  - Grok: agent should **not** casually flip `queue_next` off based on stalls; it should require explicit handoff gate or wrapper/user choice.
- New semantics to encode in `auto-roadmap` and respected by `roadmap-deepen`:
  - **Default**: treat `queue_next` as **sticky-true** across deepen iterations.
  - **Handoff kill-switch**:
    - When `handoff_gate` is enabled for this run (per params / Config) and **handoff_readiness ≥ min_handoff_conf** for the relevant phase:
      - Set an internal `effective_queue_next = false` for this iteration.
      - Do **not** append a follow-up RESUME-ROADMAP.
      - Optionally create a small roadmap-next-step or handoff wrapper explaining "Loop stopped: handoff readiness met".
    - Otherwise: `effective_queue_next = true`.
  - **Hardening hooks:**
    - The agent (in crafter or auto-roadmap) must never set queue_next: false based solely on stall patterns, low confidence, high iterations, drift, or any other runtime metric unless the handoff gate condition is explicitly met or the user has chosen false via the crafter’s explicit “Other” path and confirmed it.
    - Do not allow any other part of the code (e.g. context-util gates, iteration ceilings) to flip `queue_next` from true → false silently; instead they must use RECAL or wrappers.
    - Logging: in workflow_state log or Errors.md, include when handoff gate suppressed queue_next (e.g. Status/Next: `handoff_gate: stopped-auto-append`).

### 4. Dynamic budget and depth/breadth derivation with gates

- Use the existing metrics from `roadmap-deepen` + Parameters:
  - `last_ctx_util_pct` and `last_conf` (frontmatter), `iterations_per_phase[current_phase]`, `current_depth`, iteration guidance ranges, RECAL thresholds, research thresholds.
- Design **heuristics that only live inside the effectiveParams layer** and respect all gates:
  - **Budgets (token_cap, research_max_tokens, research_synth_cap_tokens, research_result_limit):**
    - When util is low AND depth ≥ 2 AND last_conf < research_conf_veto_threshold:
      - Allow higher budget values (up to global caps), possibly proportional to leftover_pct.
    - When util is high OR repeated high-util RECALs occurred recently:
      - Clamp budgets near conservative defaults.
    - Ensure any derived `token_cap` cooperates with the **context_window_tokens**-based overflow gate; no derived value may allow bypassing the 0.9×window overflow failure rule.
  - **Depth/breadth (max_depth, branch_factor, batch_subphases, granularity):**
    - When early in phase and within iteration guidance ranges: allow a more aggressive branch_factor / depth.
    - When above iteration guidance range or close to `max_iterations_per_phase`: reduce branch_factor, maybe limit max_depth for this run.
    - Ensure `max_depth` is still bounded by the per-phase defaults in Parameters (1–2→2, 3–4→3, 5–6→4) and never exceeds a safe global max.
  - Encode explicit **guardrails**:
    - Dynamic derivation is allowed **only** within ranges defined in Parameters/Config; never change hard limits in code.
    - When heuristics would choose a value outside allowed ranges, they must clamp and log (e.g. to Feedback-Log or workflow_state Status/Next) rather than silently accept it.

### 5. Smart dispatch: hardened action selection when `action: "auto"`

- Extend the existing smart-dispatch section of `auto-roadmap` using the state+metrics we just aligned:
  - Inputs: `iterations_per_phase`, `current_depth`, roadmap-state / workflow_state status, drift score, handoff_readiness, context utilization trends, existing wrappers.
  - Branching strategy:
    - Use `roadmap-next-step` wrappers first when present and approved (already described in Parameters/Queue-Sources) — still the highest authority.
    - Then consider state: if above `max_iterations_per_phase` or repeatedly above iteration guidance ranges, prefer `recal` or `advance-phase` over further `deepen`.
    - Use drift and handoff_readiness as described in Roadmap-Quality-Guide (e.g. high drift or poor handoff_readiness → wrapper or recal; good metrics → deepen).
  - **Key hardening rule:** when `params.action === "auto"`, the chosen action is **per-iteration**, and must not be written into future queue entries as a permanent override. The next RESUME-ROADMAP with `action: "auto"` must recompute this decision from state.
  - When smart dispatch is below confidence threshold (e.g. <75% clarity), create a roadmap-next-step wrapper (as described in Parameters) rather than guessing.

### 6. Queue propagation rules: what carries forward vs is recomputed

- Encode, at the plan level, how roadmap-deepen should behave when appending follow-up RESUME-ROADMAP entries (building on its existing step 7/8):
  - **Forward (sticky):**
    - Identity: `project_id`, `source_file` (when present), `profile`, `enable_context_tracking` effective flag, any crafter-locked params.
    - Hand-off knobs: `handoff_gate`, `min_handoff_conf` (subject to handoff module’s own dynamics, e.g. tightening over phases).
  - **Recompute per iteration (non-sticky; live in effectiveParams only):**
    - Budgets: `token_cap`, `research_max_tokens`, `research_synth_cap_tokens`, `research_result_limit`.
    - Shape: `max_depth`, `branch_factor`, `batch_subphases`, `granularity`.
    - Research: derived `enable_research` and gap-related params; `research_auto_keywords` remain static but their *interpretation* can be dynamic.
    - `action` when originally `auto`.
  - **Queue_next gate:**
    - Respect the new handoff-gate semantics (`effective_queue_next`), and retain the existing gate that prevents next deepen when context-util thresholds or RECAL triggers fire (they switch to RECAL or blocked status, but do not set queue_next false silently).
  - Plan for explicit documentation changes later, so anyone reading Queue-Sources or roadmap-deepen knows which params are never persisted as sticky overrides.

### 7. Hardening hooks for context tracking and research

- Tie the dynamic behavior back into the strict postconditions we saw:
  - Ensure any new dynamic logic:
    - **Never** causes the code to write `"-"` into Ctx Util/Leftover/Threshold/Est. Tokens columns when tracking is true.
    - **Always** respects the overflow check (`estimated_tokens > 0.9 * context_window_tokens`) and high-util RECAL behavior — these are non-negotiable safety gates.
  - For research-related dynamics:
    - Make sure pre-deepen and gap-fill research flows continue to produce proper Errors.md entries when research fails, is empty, or is skipped (using the standard Research error entry format from Logs.md).
    - Dynamic decisions around `enable_research` must still use `research_conf_veto_threshold`, `research_util_threshold`, `research_cooldown`, and depth ≥ 2 gates as documented in Parameters.
    - Never let dynamic research settings bypass the existing `gap_severity_threshold` / soft floor rules; at most they can adjust thresholds within safe ranges.

### 8. Documentation & observability updates (hardening surfaced)

- Plan doc updates (to be implemented after code changes):
  - `Queue-Sources.md` RESUME-ROADMAP section:
    - Add a short **dynamic vs static param** table.
    - Describe `queue_next` + handoff-gate semantics explicitly.
  - `Parameters.md`:
    - Add notes on dynamic derivation ranges for budgets and depth/breadth parameters.
    - Clarify that dynamic derivation lives in-effectiveParams and must respect existing thresholds and gates.
  - `roadmap-deepen` and `auto-roadmap` skill/rule docs:
    - Add a subsection outlining which params they recompute each iteration and how that interacts with context-tracking, RECAL, and research.
  - Logging:
    - Expand workflow_state log or related logs to optionally record **derived per-run values** (e.g. chosen `token_cap`, `branch_factor`, `enable_research`, `action` when `auto`) in Status/Next or a dedicated column.
    - Add clear messages when handoff gate suppresses queue_next.

### 9. GROK constraints baked into v2

- Keep the prior Grok back-and-forth output included (in this plan and, later, in a design note) as a **decision record**:
  - `queue_next` = sticky-true, only suppressed when handoff gate + min_handoff_conf are met, or via explicit crafter/wrapper choice.
  - Dynamic per-deepen knobs limited to budgets, depth/breadth, research, and effective action.
  - `enable_context_tracking`, profile name, and hard caps remain static safeguards.

### 10. Rollout & validation strategy (with hardening tests)

- Start on a single project and use **before/after** comparison:
  - Run several RESUME-ROADMAP deepen iterations with `action: "auto"` and default params; capture workflow_state logs, context util metrics, RECAL events, and any wrappers.
  - After implementing the dynamic behavior:
    - Verify that:
      - Context-tracking metrics are still populated correctly and gates still fire.
      - RECAL behavior under high util / overflow remains intact.
      - `queue_next` behavior matches the new semantics (sticky-true, only suppressed by handoff gate or explicit false).
      - Research-related errors and gaps still log correctly.
    - Compare drift scores, handoff_readiness, and number of wrappers to ensure quality either improves or at least does not regress.
- Only after this targeted validation, expand to more projects; use existing logs (Errors.md, Ingest-Log, Research-Log, workflow_state logs) and Vault-Change-Monitor views to watch for regressions in drift, context spikes, or stalled roadmaps.

