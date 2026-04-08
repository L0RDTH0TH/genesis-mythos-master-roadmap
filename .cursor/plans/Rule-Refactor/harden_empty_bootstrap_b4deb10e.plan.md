---
name: Harden Empty Bootstrap
overview: Patch the dual-track empty-queue bootstrap path so lane runs can synthesize one safe RESUME_ROADMAP entry when both lane PQ and lane QCONT have no usable records, then document and validate the behavior.
todos:
  - id: patch-a1b-flow
    content: Refactor A.1b in queue.mdc to avoid early return on missing/empty QCONT and complete no-record fallback chain
    status: completed
  - id: add-config-knob
    content: Add and document empty_queue_bootstrap_create_missing_qcont in Second-Brain-Config queue_continuation
    status: completed
  - id: update-queue-docs
    content: Update Queue-Sources.md with hardened dual-track empty bootstrap behavior and field expectations
    status: completed
  - id: update-operator-doc
    content: Update Dual-track-EAT-QUEUE-Operator.md with post-drain self-seed expectations under lane runs
    status: completed
  - id: verify-scenarios
    content: Validate lane-empty scenarios for sandbox/godot and confirm synthesized continuation + logs
    status: completed
isProject: false
---

# Harden Empty-Queue Bootstrap (Dual-Track, Hardened)

## Scope

Implement a targeted Layer 1 fix so `EAT-QUEUE lane <track>` recovers from total drain (`lane PQ empty` + `lane QCONT missing/empty/no eligible record`) with a deterministic, lane-aware continuation when configured. Eliminate the current A.1b short-circuit as the blocking failure mode.

## Files To Change

- [.cursor/rules/agents/queue.mdc](/home/darth/Documents/Second-Brain/.cursor/rules/agents/queue.mdc)
- [3-Resources/Second-Brain/Queue-Sources.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Queue-Sources.md)
- [3-Resources/Second-Brain/Second-Brain-Config.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Second-Brain-Config.md)
- [3-Resources/Second-Brain/Docs/Dual-track-EAT-QUEUE-Operator.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Docs/Dual-track-EAT-QUEUE-Operator.md)

## Implementation Plan

### 1) Replace A.1b short-circuit with staged fallback flow

In `queue.mdc` A.1b, replace the current step-2 early-return semantics with hardened staged fallback while preserving existing safety and contracts.

- Keep existing gates:
  - `empty_queue_bootstrap_enabled`
  - lane/track resolution from A.0x (`PQ`, `QCONT`, `parallel_context`, `queue_lane_filter`)
- Replace current early stop logic with staged fallback:
  - Treat missing/unreadable/empty QCONT as no-record context (not terminal, no immediate OPERATOR ALARM return).
  - Optionally create missing QCONT when config allows (see step 2).
  - Attempt eligible continuation candidate from QCONT tail as today.
  - If no candidate exists, run existing no-record branches in order:
    - PromptCraft no-record path (if enabled)
    - Deterministic no-record synthesis (if enabled)
- Ensure deterministic synthesis uses lane-aware inputs:
  - `project_id` from active lane context (`lane_project_id` from handoff/config resolution)
  - `params.action` from `queue_continuation.bootstrap_action`
  - `params.roadmap_track` from `queue_continuation.bootstrap_track`
  - `queue_lane` set to active lane when lane-filtered run
- Ensure deterministic guidance source remains track-aware:
  - build from the track-resolved workflow cursor file used by existing deterministic path semantics.
- Preserve anti-respawn guard (`workflow_cursor_at_completion` same-cursor dedup) before append.
- Preserve append behavior and Watcher/Audit semantics already defined in A.1b/A.5g.

### 2) Add explicit config knob for missing-QCONT handling

In `Second-Brain-Config.md` queue continuation block, add a documented flag:

- `empty_queue_bootstrap_create_missing_qcont: true` (default)

Behavior contract:

- When true and active QCONT path is missing, Layer 1 may initialize it as empty machine log file and continue bootstrap fallback logic.
- When false, Layer 1 skips file initialization but still treats missing QCONT as no-record context (not immediate abort).

### 3) Document the hardened bootstrap behavior

Update `Queue-Sources.md` queue-continuation section to reflect:

- Dual-track hardened no-record flow in A.1b.
- Lane-specific deterministic synthesis requirements (`project_id`, `action`, `roadmap_track`, `queue_lane`).
- Clarify ordering relationship: lane hydration (A.0.4) happens before A.1b candidate/bootstrap resolution.
- State explicitly that hydration copies existing pool lines only; bootstrap synthesis is the lane recovery path when no candidate exists.

### 4) Update operator guide expectations

In `Dual-track-EAT-QUEUE-Operator.md`, add explicit operator-facing behavior:

- With lane trigger + config enabled, an empty lane can self-seed one continuation line via hardened bootstrap path when no continuation record is available.
- Keep existing warning that bare `EAT-QUEUE` bypasses per-lane path.

### 5) Validation plan (post-implementation)

Run controlled checks in lane bundles:

- Preconditions:
  - Parallel mode on, lane triggers used.
  - Simulate empty lane PQ and missing/empty lane QCONT.
- Execute:
  - `EAT-QUEUE lane sandbox`
  - `EAT-QUEUE lane godot`
- Verify:
  - One synthesized `RESUME_ROADMAP` line appears in each lane PQ when no real candidate exists.
  - Line includes expected lane/project/action/track fields.
  - No immediate A.1b abort on missing/empty QCONT.
  - No OPERATOR ALARM from the old step-2 short-circuit path.
  - No legacy-path leakage on lane runs.
  - Watcher/Audit entries are present and parse-safe.
  - Next normal run populates QCONT through A.5e as expected.
  - With `empty_queue_bootstrap_create_missing_qcont: false`, bootstrap still proceeds via no-record logic (without file creation).

## Notes / Non-goals

- No change to queue schema compatibility.
- No change to wrapper processing, subagent contracts, or snapshot/backup guardrails.
- Legacy single-queue behavior remains intact when parallel routing is not active.
- Keep terminology and canonical paths aligned to current repo docs (`3-Resources/Second-Brain/...`), not alternate doc-root aliases.

