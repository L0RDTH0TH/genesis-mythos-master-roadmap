---
name: roadmap-context-tracking-default
overview: Ensure roadmap context-utilization tracking is enabled by default for all RESUME-ROADMAP deepen runs, and can only be turned off via an explicit, manual override, with docs, config, and queue handling kept in sync.
todos:
  - id: audit-dispatch-merge
    content: Inspect RESUME-ROADMAP dispatcher / auto-eat-queue merge logic and change enable_context_tracking default to true, only allowing explicit params.enable_context_tracking === false to turn it off.
    status: completed
  - id: sync-roadmap-deepen-behavior
    content: Ensure roadmap-deepen reads the merged enable_context_tracking flag and always logs context-utilization columns when true, never re-reading config for this decision.
    status: completed
  - id: update-config-and-parameters-docs
    content: Update Second-Brain-Config.md and Parameters.md to state that context tracking is default-on and can only be disabled via explicit RESUME-ROADMAP queue params.
    status: completed
  - id: fix-plans-rules-examples
    content: Update context-utilization-and-iteration-cap plan, auto-roadmap rule docs, and Queue-Sources examples so they no longer imply opt-in tracking or recommend default-off configs.
    status: completed
  - id: add-validation-and-tests
    content: Add validation for misconfigured enable_context_tracking in config and tests that cover default-on, explicit-off, and threshold-breach behaviors in workflow_state logs.
    status: completed
isProject: false
---

# Roadmap context tracking default-on hardening

## Audit findings

- **Config defaults**: `3-Resources/Second-Brain/Second-Brain-Config.md` already sets `enable_context_tracking: true` in both the `## roadmap` block and `prompt_defaults.roadmap` block, matching the intent that tracking is on by default.
- **Runtime behavior**: `roadmap-deepen` (see `.cursor/skills/roadmap-deepen/SKILL.md` and `.cursor/sync/skills/roadmap-deepen.md`) logs context percentages only when `enable_context_tracking` is true; when false it writes `"-"` in the four context columns, which is what you see in `1-Projects/genesis-mythos-master/Roadmap/workflow_state.md` and the gm-resume16 snapshots.
- **Param merge surface**: The `auto-roadmap` rule and `Queue-Sources.md` treat `enable_context_tracking` as an optional RESUME-ROADMAP param, merged from `params` + `prompt_defaults.roadmap`; there is currently no explicit guard preventing config from setting it to `false`, and examples still show passing `enable_context_tracking: true` to turn tracking on.
- **Spec drift**: The built plan `.cursor/plans/Built/context-utilization-and-iteration-cap_9b1f7a8f.plan.md` still contains an earlier recommendation to set `enable_context_tracking: false` in config, and its test examples emphasize enabling tracking explicitly; this contradicts your current requirement and could reintroduce default-off behavior if re-run.

## Implementation plan

1. **Tighten default semantics in the roadmap dispatcher**

- Update the RESUME-ROADMAP dispatcher (auto-eat-queue / auto-roadmap implementation) so that `enable_context_tracking` is derived as:
  - `true` when `params.enable_context_tracking` is `undefined`, regardless of config; 
  - `false` **only** when `params.enable_context_tracking === false` (explicit manual override in the queue entry);
  - ignore any `prompt_defaults.roadmap.enable_context_tracking` value of `false` when computing the effective flag.
- Ensure `context_util_threshold`, `context_token_per_char`, and `context_window_tokens` still come from params with fallback to `prompt_defaults.roadmap` as today.

1. **Align roadmap-deepen with the new merge contract**

- Verify that `roadmap-deepen` reads a single, already-merged `enable_context_tracking` flag (rather than re-reading config itself); if it still reads config directly, change it to trust the dispatcher’s merged params so there is exactly one source of truth for the on/off decision.
- Confirm that when the merged flag is true, the skill always computes and writes **Ctx Util %**, **Leftover %**, **Threshold**, and **Est. Tokens / Window** into the 10-column log row, and applies the RECAL-ROAD gate as specified.

1. **Update config and parameter docs to forbid default-off**

- In `3-Resources/Second-Brain/Second-Brain-Config.md` and `3-Resources/Second-Brain/Parameters.md`, clarify that:
  - `prompt_defaults.roadmap.enable_context_tracking` is **informational only** and must remain `true` (or be omitted); 
  - the only supported way to disable tracking for a run is to pass `"enable_context_tracking": false` in a specific RESUME-ROADMAP queue entry.
- Explicitly document that any future attempt to set `enable_context_tracking: false` in config is ignored by the dispatcher and should be treated as a misconfiguration.

1. **Clean up plans, rules, and examples that imply default-off or opt-in**

- Edit `.cursor/plans/Built/context-utilization-and-iteration-cap_9b1f7a8f.plan.md` so that:
  - the recommended config snippet uses `enable_context_tracking: true` (or omits the key entirely),
  - its “tracking disabled” test scenario uses an explicit `"enable_context_tracking": false` queue param instead of a config default.
- Update `.cursor/rules/context/auto-roadmap.mdc` and `.cursor/sync/rules/context/auto-roadmap.md` to say that:
  - context tracking is **on by default** for deepen,
  - `params.enable_context_tracking` is intended as a **manual opt-out** for special cases.
- Refresh `3-Resources/Second-Brain/Queue-Sources.md` examples so that RESUME-ROADMAP sample lines either omit `enable_context_tracking` (implicitly on) or show `false` only in a clearly-labeled "debug / special" example.

1. **Add validation and regression tests**

- Extend the RESUME-ROADMAP param validation so that if config contains `enable_context_tracking: false`, it logs a warning (e.g. to `Errors.md` or a roadmap log) and coerces the effective flag to `true` instead of honoring the false.
- Add automated or scripted tests that:
  - enqueue a RESUME-ROADMAP deepen without `enable_context_tracking` and assert that the new `workflow_state` log row has non-`"-"` context columns;
  - enqueue a RESUME-ROADMAP deepen with `"enable_context_tracking": false` and assert that context columns are `"-"` and the gate is not applied;
  - verify that re-running with stale workflow_state / roadmap-state still respects the default-on behavior.

1. **Optional: backfill or annotate older runs**

- Decide whether you want to leave historical rows with `"-"` as-is (simplest), or append a short note to `workflow_state.md` indicating that context utilization tracking was introduced after a given timestamp so consumers don’t misinterpret the older `"-"` values.
- If desired, add a one-time script/skill to mark the introduction point in `genesis-mythos-master` and any future projects so dashboards can filter pre/post-tracking rows correctly.

