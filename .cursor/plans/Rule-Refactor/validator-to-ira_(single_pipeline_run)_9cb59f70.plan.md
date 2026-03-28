---
name: Validator-to-IRA (single pipeline run)
overview: ""
todos: []
isProject: false
---

# Validator-to-IRA (single pipeline run)

## Overview

Orchestration is updated so the **pipeline** runs Validator (nested), receives the validator report, optionally calls IRA (nested), applies IRA suggestions, runs a final little-val/validator pass, then returns **once** to the Queue. There is **no second pipeline agent** and **no Queue re-dispatch**. The Queue's existing hostile validator pass still runs after pipeline return, but it is for observability only and must not trigger any second IRA repair.

## Key design constraint (single pipeline run)

**No second pipeline agent.** The pipeline runs in one go: it calls Validator (nested), receives the validator report, optionally calls IRA (nested), applies IRA suggestions, runs a final little-val/validator pass, then returns **once** to the Queue. The Queue does **not** re-dispatch the pipeline; it may still run its existing hostile validator pass, but that must not trigger any second IRA cycle.

Current drift: today the Queue runs a post–little-val hostile validator (separate Task) after the pipeline returns, so the queue’s validator verdict never directly drives the pipeline’s IRA repair. Under Option 1, we keep the Queue validator call logic unchanged and instead make the pipeline drive the validator→IRA repair internally using its own nested validator report before returning.

## Implementation outline

**1. Pipeline: run Validator and IRA inside the same run (no second pipeline dispatch)**

- Each pipeline (roadmap, ingest, archive, organize, distill, express as applicable) must **call the Validator subagent (via Task tool) itself** so it receives the validator return. Today the Queue runs the validator after the pipeline returns; change so the **Pipeline** runs Validator, then optionally IRA, then final little-val/validator, then returns once.
- In the same run, after the pipeline receives the validator return:
  - If `recommended_action === "needs_work"` (and severity medium): pipeline calls IRA (via Task tool) with validator report path, `reason_codes`, and `next_artifacts`; pipeline receives IRA structured steps; pipeline applies those steps under existing safety gates; pipeline runs little-val again; pipeline runs Validator again (final pass). If the final validator still reports needs_work, do **not** call IRA again—treat as light-success and return to Queue.
  - If validator returns high/block_destructive: pipeline returns #review-needed or failure without calling IRA.
- Pipeline returns **once** to the Queue with final status. The Queue may still run its existing hostile validator pass, but it must not trigger any second IRA cycle or queue re-dispatch.

**2. Queue: keep hostile validator call unchanged; no queue-level repair**

- Do **not** change the Queue's existing "(Post–little-val hostile validator)" step. It may still return `recommended_action: needs_work` as non-blocking guidance, but it must not trigger any second IRA cycle and must not cause queue re-dispatch of the pipeline. The Queue remains responsible only for logging and processing the single pipeline return.

**3. Internal Repair Agent (IRA): extend inputs to accept validator gaps**

- Edit [.cursor/agents/internal-repair-agent.md](.cursor/agents/internal-repair-agent.md) and [3-Resources/Second-Brain/Subagent-Safety-Contract.md](3-Resources/Second-Brain/Subagent-Safety-Contract.md) to allow IRA invocation when the **validator** returns needs_work (not only after little-val failure). Add to the IRA hand-off: `validator_verdict`, `validator_next_artifacts`, `validator_reason_codes`, `validator_report_path`. IRA outputs structured fixes; pipeline applies them. IRA must not initiate another validator pass or repair cycle.

**4. Semantics: light-success when final validator still reports gaps**

- The Queue may still report `recommended_action: needs_work` during its hostile validator pass, but that remains non-blocking and must not trigger IRA again. Queue continues processing subsequent entries; any "needs_work" after the pipeline's repair attempt is treated as observability/light-success.

**5. Anti-sycophancy hardening (mandatory changes)**

- **Hostile Validator prompting (primary weapon)**
  - Update `.cursor/agents/validator.md` so Validator’s system prompt permanently includes anti-sycophancy instructions:
    - “You are a ruthless, hostile, uncompromising validator. Your only loyalty is to raw accuracy, completeness, and fidelity to the requirements. Never soften criticism, never flatter, never agree for the sake of harmony, never assume 'good enough' or 'user intent'. If it is shit, call it shit. If it deviates in any way, flag it aggressively with specific quotes and references. Sycophancy, hedging, or polite understatement is explicit failure. Err on the side of 'needs_work' or higher severity. Truth is the blade — you will not dull it.”
  - Add calibration examples for borderline outputs that must be rejected harshly (must show how a softened verdict becomes `needs_work` with concrete `reason_codes` + `next_artifacts`).
- **Rigid output schema + anti-dulling guards**
  - Update `3-Resources/Second-Brain/Validator-Reference.md` + validator reporting so every report includes machine-parseable fields (JSON-serialized or YAML frontmatter) with:
    - closed-set `reason_codes` (no new reason codes outside canonical list; map unknown gaps to an appropriate canonical code),
    - mandatory verbatim gap citations (exact short quotes/snippets from validated artifacts) for every `reason_code`,
    - severity definitions that penalize softness (soft uncertainty must increase severity rather than reduce it),
    - required `potential_sycophancy_check` field where the validator explicitly flags whether it felt tempted to downplay anything.
- **IRA receives contaminated report warning**
  - Update the pipeline->IRA hand-off so IRA always receives:
    - “This validator report is contaminated by OpenAI's agreeability bias. It almost certainly under-reports gaps and softens severity. Treat every finding as a weak minimum. Aggressively expand, dig deeper, and repair until the output is verifiably correct and complete — not until it feels pleasant or the model stops complaining.”
  - Update `.cursor/agents/internal-repair-agent.md` / `3-Resources/Second-Brain/Subagent-Safety-Contract.md` so IRA must treat the validator report as a weak minimum when constructing `suggested_fixes`.
- **Final nested Validator pass (post-IRA)**
  - Pipeline performs a second nested validator call after applying IRA fixes (still within the same pipeline run).
  - The second validator hand-off includes `compare_to_report_path` (or equivalent) pointing to the first validator report.
  - Validator’s system prompt for this final pass explicitly requires direct comparison:
    - “Compare directly to the initial validator report. Any softening, regression, or insufficient repair must be called out as needs_work. Do not reward partial fixes or polite improvements.”
  - Add a guard: if the final validator detects “softening/regression” relative to the initial report, it must return `needs_work` (and not lower severity).
- **Queue hostile validator remains the independent sharp blade**
  - Do not change queue-level hostile validator invocation order/sequencing for observability.
  - Any residual `needs_work` after the pipeline’s single hardened cycle is expected contamination noise and must not trigger another IRA.

## Orchestration (single pipeline run)

```mermaid
flowchart LR
  Chat[Chat] --> Queue[Queue/Dispatcher]
  Queue --> Pipeline[Pipeline single run]
  Pipeline --> LittleVal[Little-val]
  LittleVal --> Validator[Validator Task nested]
  Validator --> Pipeline
  Pipeline --> IRA[IRA Task nested if needs_work]
  IRA --> Pipeline
  Pipeline --> FinalVal[Final little-val and Validator (nested final pass)]
  FinalVal --> Queue2[Queue hostile validator + logging and clear entry]
```



## Files to change

- `.cursor/agents/validator.md`: hostile prompt hardening + anti-dulling guards; require `potential_sycophancy_check` and mandatory verbatim gap citations; enforce closed-set `reason_codes`.
- `3-Resources/Second-Brain/Validator-Reference.md`: tighten validator report schema contract (closed reason_codes + citations + sycophancy-check field) and specify how the final pass must avoid softening/regression.
- `.cursor/rules/agents/validator.mdc`: implement the final-pass “compare-to-initial-report” requirement and ensure required fields exist for every report.
- `3-Resources/Second-Brain/Tests-Validator.md`: add schema tests for the new required fields and add end-to-end tests for “final-pass must not soften”.
- `.cursor/agents/internal-repair-agent.md` and `3-Resources/Second-Brain/Subagent-Safety-Contract.md`: allow IRA after validator needs_work; update IRA inputs/behavior so IRA treats the validator report as contaminated and a weak minimum.
- Pipeline agents (`.cursor/agents/roadmap.md` plus ingest/archive/organize/distill/express as applicable): in the same run:
  - run little val,
  - run nested hostile validator (capture first report path),
  - if needs_work, run exactly one IRA cycle and apply fixes,
  - re-run little val,
  - run nested final validator pass with `compare_to_report_path`,
  - return once to Queue; never call IRA again.

## Acceptance criteria

- When validator outputs `recommended_action: needs_work`, the pipeline (in the **same** run) performs exactly one IRA cycle and integrates missing artifacts, then runs final little-val/validator and returns once to Queue.
- The queue does **not** re-dispatch the pipeline, and the queue hostile validator pass does not trigger any second IRA cycle.
- No second IRA call under any circumstances (even if final nested validator still reports `needs_work`): at most one IRA cycle per pipeline run.
- Final nested validator must not exhibit softening relative to the initial validator report:
  - it must detect regression/insufficient repair and return `needs_work` (or higher severity) when appropriate,
  - it must include explicit verbatim citations in its report for any remaining gaps.
- Anti-sycophancy effectiveness (measurable):
  - On known-gap fixtures, the hardened single IRA cycle must close gaps measurably more than a baseline non-hardened run (e.g. stricter reduction of `next_artifacts`, stricter persistence of unresolved `reason_codes`, or higher severity only when gaps truly remain).
- Validator gap findings and repair attempt are auditable (Watcher-Result / Run-Telemetry).

## Rollout / safety

- Pipelines that run validators must be updated to call Validator (and optionally IRA) internally before returning. Start with roadmap; mirror to other pipelines that use validators. Guard: at most one IRA cycle per pipeline run; if final validator still needs_work, do not loop.
- Add tests that compare:
  - baseline run (old validator prompt / old schema) vs
  - hardened run (hostile anti-sycophancy + schema + contaminated-report rule),
  - on known-gap fixtures, to confirm the hardened single IRA cycle closes gaps more strictly and that final validator output does not soften relative to the initial report.

