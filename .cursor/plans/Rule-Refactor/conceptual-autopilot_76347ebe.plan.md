---
name: conceptual-autopilot
overview: "Make the conceptual roadmap an autonomous control-loop: it should choose the best option/action when multiple alternatives exist, continue without getting stuck on execution-only gates, and stop only when the master goal is ready for technical design handoff. Selected decisions must be logged to the per-project roadmap `decisions-log.md` file."
todos:
  - id: conceptual-smart-dispatch-bypass-wrappers
    content: Modify `smart dispatch` in `/.cursor/rules/agents/roadmap.mdc` so conceptual track never creates Decision Wrappers on low confidence; instead select top candidate using `layer1_resolver_hints` and proceed, logging the decision.
    status: completed
  - id: conceptual-stop-criterion
    content: Implement a conceptual-specific `Target reached` check in `/.cursor/rules/agents/roadmap.mdc` tied to validator/handoff evidence (execution-only gaps advisory, coherence blockers hard). Update `Parameters.md`/config if a conceptual threshold knob is needed.
    status: completed
  - id: decision-logging-to-decisions-log
    content: Add per-decision logging into `1-Projects/<project_id>/Roadmap/decisions-log.md` for conceptual autopilot choices (selected action/option, evidence used, links to validator/handoff artifacts).
    status: completed
  - id: validator-and-return-handling-conceptual
    content: Audit and adjust `validator` and `roadmap return` handling so conceptual does not enqueue repair/recal churn caused solely by execution-only advisory `needs_work` outcomes.
    status: completed
  - id: queue-followup-churn-stop
    content: Update `/.cursor/rules/agents/queue.mdc` follow-up synthesis so it stops appending deepen/recal churn once roadmap subagent signals conceptual completion via `queue_continuation`/`suppress_reason`.
    status: completed
  - id: docs-sync
    content: "Update docs and `.cursor/sync/` mirrors: `Pipelines.md` / `Cursor-Skill-Pipelines-Reference.md` / relevant rules, plus `.cursor/sync/changelog.md` entries."
    status: completed
  - id: verification-plan-run
    content: "Perform one manual conceptual EAT-QUEUE loop test on `genesis-mythos-master` and confirm: terminal stop, no wrapper fatigue, decisions logged, and no execution-only block_destructive on conceptual."
    status: completed
isProject: false
---

## Scope

- Only the conceptual track should behave as “autopilot” (fast, low-friction, no wrapper fatigue).
- Execution track keeps the existing gates and wrapper/repair semantics.

## Workstreams

### 1. Conceptual smart-dispatch: never stall on low confidence

- Update conceptual behavior in `.cursor/rules/agents/roadmap.mdc` (smart dispatch Step 5, currently “Low confidence → create Decision Wrapper”).
- New rule: when `effective_track: conceptual`, replace “create wrapper” with “pick the best next action and proceed” using the best available evidence:
  - Prefer `layer1_resolver_hints.effective_action` / `need_class` / `effective_target` when present.
  - Else use the same heuristic currently used to populate wrapper options (next-step decision scoring), but pick the top candidate even if below the wrapper threshold.
  - Hard-stop only on conceptual coherence blockers (contradictions/incoherence/state-hygiene/safety ambiguity). Everything else should log and continue.
- Keep wrapper creation for execution track and for cases where no evidence candidate can be selected safely.

Files to adjust:

- `[/.cursor/rules/agents/roadmap.mdc](.cursor/rules/agents/roadmap.mdc)`
- `[/.cursor/agents/roadmap.md](.cursor/agents/roadmap.md)`

### 2. Conceptual completion/stop criterion tied to validator output

- Update smart-dispatch Step 4 (“Target reached?”) so conceptual “complete” maps to “master goal is ready for design-team technical implementation” (your definition).
- Implement `conceptual_target_reached` as:
  - Use handoff readiness (from `handoff-audit` / validator reports) as the primary signal.
  - When validator gaps are execution-only, treat them as non-blocking for stop (but still log them).
  - Require the conceptual coherence gate to be satisfied (no open contradictions/incoherence/state hygiene blockers).
- Add a conceptual-specific threshold knob (or reuse existing `min_handoff_conf`, but computed under conceptual effective_track).

Files to adjust:

- `[/.cursor/rules/agents/roadmap.mdc](.cursor/rules/agents/roadmap.mdc)`
- `[3-Resources/Second-Brain/Parameters.md](3-Resources/Second-Brain/Parameters.md)`
- `[3-Resources/Second-Brain-Config.md](3-Resources/Second-Brain-Config.md)` if a dedicated conceptual threshold is needed.

### 3. Decision logging: persist selected option/action into the project decisions file

- Ensure every conceptual “picked optimal option/action” writes a record to:
  - `[1-Projects/<project_id>/Roadmap/decisions-log.md](1-Projects/genesis-mythos-master/Roadmap/decisions-log.md)`
- Record fields to log per decision:
  - timestamp, queue_entry_id/action, effective_track
  - chosen option letter/action (if wrapper-style options exist) or chosen action enum (deepen/recal/advance-phase/etc.)
  - the gating/validator evidence used (e.g. primary_code / key reason_codes)
  - whether any execution-only gaps were treated as advisory
  - link to the relevant validator report and/or handoff-audit output.
- Prefer to implement this in the roadmap orchestration layer (roadmap subagent) so it logs the “decision made” even when no wrapper is created.

Files to adjust:

- `[/.cursor/rules/agents/roadmap.mdc](.cursor/rules/agents/roadmap.mdc)`
- `[/.cursor/agents/roadmap.md](.cursor/agents/roadmap.md)`
- If needed, extend `[/.cursor/skills/hand-off-audit/SKILL.md](.cursor/skills/hand-off-audit/SKILL.md)` so the decisions-log append includes the conceptual decision context.

### 4. Keep existing gate semantics, but make them non-blocking at low confidence for conceptual

- Confirm `.cursor/rules/agents/validator.mdc` + `.cursor/agents/validator.md` already downgrade execution-only gaps on conceptual to `medium/needs_work` and never force `block_destructive` by those codes alone.
- Update roadmap subagent return handling so conceptual does not repeatedly queue `recal`/repair follow-ups solely due to advisory `needs_work` outcomes.

Files to adjust:

- `[/.cursor/rules/agents/validator.mdc](.cursor/rules/agents/validator.mdc)`
- `[/.cursor/agents/validator.md](.cursor/agents/validator.md)`
- `[/.cursor/rules/agents/roadmap.mdc](.cursor/rules/agents/roadmap.mdc)`

### 5. Queue follow-up behavior: stop churn once conceptual target reached

- Update queue follow-up synthesis (Layer 1 `A.5c`/`A.5c.1`) so when conceptual target is reached (or effectively reached), Layer 1 does not keep appending “deepen/recal repair style” follow-ups.
- The best source of truth for “target reached” is the roadmap subagent’s return (queue continuation + suppress_reason / suppress_followup).

Files to adjust:

- `[/.cursor/rules/agents/queue.mdc](.cursor/rules/agents/queue.mdc)`
- `[3-Resources/Second-Brain/Docs/Queue-Continuation-Spec](3-Resources/Second-Brain/Docs/Queue-Continuation-Spec)` if the stop/terminal suppress enums need conceptual-only refinements.

## Implementation order

1. Update roadmap smart-dispatch (conceptual low-confidence wrapper bypass) + stop criterion.
2. Add/extend decision logging into `decisions-log.md`.
3. Verify validator downgrades and adjust roadmap return handling to avoid conceptual churn.
4. Update Layer-1 follow-up synthesis to respect the conceptual termination signal.
5. Docs/sync updates.

## Verification

Manual checks (no code required after changes):

- Run EAT-QUEUE with a conceptual RESUME_ROADMAP deepen loop on `1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md` where `roadmap_track: conceptual`.
- Observe that:
  - conceptual progresses without repeatedly creating roadmap decision wrappers
  - the system eventually sets roadmap-state `status: complete` (or the next intended state) once the master goal is “design-team ready” conceptually
  - `1-Projects/<project_id>/Roadmap/decisions-log.md` contains records of each conceptual decision made by the autopilot
  - execution-only validator gaps do not generate block_destructive or repair-first churn on conceptual.

Success metric:

- After N conceptual iterations (choose N based on your typical churn history), queue tail stops appending deepen/recal loops and you see terminal completion/suppress_reason consistent with stop condition.

