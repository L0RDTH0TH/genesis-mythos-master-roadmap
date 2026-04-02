---
title: Pipeline and Workflow Errors
created: 2026-02-26
para-type: Resource
status: active
tags: [errors, pipelines, cursor, obsidian, review]
---

# Pipeline and Workflow Errors

Central log for **traced errors** from ingest, distill, archive, express, organize, and supporting workflows. Each error entry includes a trace (sanitized), summary (root cause, impact, suggested fixes, recovery), and optional link to pipeline-specific logs.

- **Dataview:** Query by table columns `pipeline`, `severity`, `approval`, `timestamp`, `error_type` (or `#review-needed` in text) to surface pending review or high-severity items.
- **Recovery:** Use RESTORE MODE to rollback from a per-change snapshot when documented in the entry.
- **PromptCraft / recovery queue:** When logging failures from **PromptCraftSubagent** (e.g. `lint_blockers`, Task launch failure, or pre-append lint rejection), include **`error_correlation_id`** from the hand-off / `prompt_craft_request` block in the Trace and Summary so recovery runs can be correlated with the original pipeline failure. Prefer `error_type` values such as `prompt-craft-failure` or `prompt-craft-lint` alongside the standard categories in the Error Handling Protocol ([[.cursor/rules/always/mcp-obsidian-integration|mcp-obsidian-integration]]).

## Error entry format

Each new error is appended as follows (no fenced YAML per entry):

### YYYY-MM-DD HH:MM — Short Title

| Field | Value |
|-------|-------|
| pipeline | autonomous-distill |
| severity | high |
| approval | pending |
| timestamp | 2026-02-26T19:30:00Z |
| error_type | mcp-api |
| commander_macro | (optional; set when error occurred in a Commander-triggered run, e.g. "Async Approve") |

#### Trace

- Timestamp, pipeline, stage, affected note path(s).
- Raw error message or stack (sanitized).

#### Summary

- **Root cause:** …
- **Impact:** …
- **Suggested fixes:** …
- **Recovery:** …

(Entries follow below, appended by the agent.)

### 2026-03-21 23:59 — EAT-QUEUE: Task tool unavailable (Roadmap dispatch)

| Field | Value |
|-------|-------|
| pipeline | queue-eat-queue (Layer 1) |
| severity | medium |
| approval | pending |
| timestamp | 2026-03-21T23:59:00Z |
| error_type | mcp-dispatch |

#### Trace

- Pipeline: EAT-QUEUE / prompt-queue only; vault `/home/darth/Documents/Second-Brain`.
- Stage: A.5 dispatch after parse/order; intended `Task(subagent_type: roadmap)` for queue entry `resume-advance-gmm-20260321-post-handoff-audit` (`RESUME_ROADMAP`, `params.action: advance-phase`, `project_id: genesis-mythos-master`).
- Host: Cursor Queue subagent context has no callable `Task` tool; dispatch aborted per `.cursor/rules/agents/queue.mdc` (no same-run fallback).
- Secondary entry `resume-roadmap-genesis-mythos-master-20260322-deepen-followup-234` not dispatched this run (per-project serialism — same project, later timestamp).

#### Summary

- **Root cause:** Layer 1 orchestrator cannot invoke the Cursor `Task` tool from this execution context, so the Roadmap subagent was not launched.
- **Impact:** `advance-phase` queue line remains in `.technical/prompt-queue.jsonl`; deepen follow-up line also remains (was correctly deferred under serialism).
- **Suggested fixes:** Run EAT-QUEUE from a parent agent/session where the `Task` tool is enabled for `subagent_type: roadmap`, or process the queue from the main Cursor agent that dispatches Layer 1 with Task available.
- **Recovery:** No vault mutation attempted; no snapshot/rollback needed. Re-run EAT-QUEUE when Task dispatch is available.

### 2026-03-22 06:59 — Roadmap nested Task unavailable (queue 252)

| Field | Value |
|-------|-------|
| pipeline | queue / RESUME_ROADMAP |
| severity | medium |
| approval | pending |
| timestamp | 2026-03-22T06:59:00Z |
| error_type | mcp-api |

#### Trace

- Queue entry: `resume-roadmap-genesis-mythos-master-20260323-deepen-suggested-252` (`RESUME_ROADMAP`, `action: deepen`, `project_id: genesis-mythos-master`, `enable_research: true`).
- Layer 1: `Task(subagent_type: roadmap)` **invoked_ok**; RoadmapSubagent returned **`#review-needed`** with `reason_code: nested_task_unavailable` — nested **`Task(validator)`** / **`Task(internal-repair-agent)`** not available inside the Roadmap subagent host context.
- Subagent reports material work: Phase **3.4.3** tertiary note `phase-3-4-3-living-world-facet-manifest-catchup-and-replay-parity-roadmap-2026-03-23-1810.md`, workflow_state / roadmap-state updates, per-change backups. **Do not** blindly re-dispatch the same queue line without checking vault state (duplicate deepen risk).

#### Summary

- **Root cause:** Cursor nested subagent session lacks callable `Task` for Validator/IRA while Roadmap contract requires Validator→IRA→Validator after deepen.
- **Impact:** Mandatory `roadmap_handoff_auto` cycle incomplete; Layer 1 did not run post–little-val validator (no `validator_context`). `.technical/prompt-queue.jsonl` line **252** left in place per A.7 (not success).
- **Suggested fixes:** Run roadmap/validator from a context where nested `Task` is enabled; or manually run **ROADMAP_HANDOFF_VALIDATE** / validator pass for `genesis-mythos-master`; edit or remove queue line **252** after reconciling vault.
- **Recovery:** Inspect roadmap-state and new 3.4.3 note; use Per-Change backups if rollback needed. Reference subagent Run-Telemetry `.technical/Run-Telemetry/Run-20260323T181000Z-genesis-mythos-master-roadmap-resume-252.md` if present.

### 2026-03-22 18:35 — EAT-QUEUE Task(roadmap) enum missing

| Field | Value |
|-------|-------|
| pipeline | queue-dispatcher |
| severity | low |
| approval | n/a |
| timestamp | 2026-03-22T18:35:00Z |
| error_type | mcp-dispatch |

#### Trace

- Cursor **Task** tool rejected `subagent_type: roadmap` (host enum: generalPurpose \| explore \| shell \| best-of-n-runner only).
- Queue entry `gmm-post-a1b-deepen-recal-20260322T123500Z` dispatched via **Task(generalPurpose)** with RoadmapSubagent hand-off per PromptCraft-style fallback.
- Subagent returned **#review-needed**: nested `Task(validator)` / `Task(internal-repair-agent)` also unavailable; **roadmap_handoff_auto** cycle not executed in L2.

#### Summary

- **Root cause:** Host Cursor configuration does not expose pipeline subagent types on the Task tool.
- **Impact:** Layer 1 skipped post–little-val **Task(validator)**; consumption + **queue_followups** deepen line still applied; operators should enable full subagent enum or run **ROADMAP_HANDOFF_VALIDATE** manually if a hostile pass is required.
- **Suggested fixes:** Enable `roadmap` / `validator` Task types in Cursor agents project settings when available.
- **Recovery:** Next line in `.technical/prompt-queue.jsonl` is `gmm-deepen-post-recal-20260322T1830Z` (RESUME_ROADMAP deepen).

### 2026-03-24 09:32 — RESUME_ROADMAP returned review-needed

| Field | Value |
|-------|-------|
| pipeline | queue-dispatcher |
| severity | medium |
| approval | pending |
| timestamp | 2026-03-24T09:32:21Z |
| error_type | nested-attestation-soft-failure |

#### Trace

- Queue entry: `layer1-followup-recal-gmm-20260324T091206Z` (`RESUME_ROADMAP`, `action: recal`, `project_id: genesis-mythos-master`).
- Roadmap subagent returned `status: review-needed` with `little_val_ok: true` and a populated `validator_context`, but nested validator cycle was not executed (`nested_validator_first.task_tool_invoked: false`).
- Queue action taken: entry marked `queue_failed: true`; Watcher-Result failure appended; one follow-up `RESUME_ROADMAP deepen` line appended with a fresh id.

#### Summary

- **Root cause:** Roadmap subagent could not complete mandatory nested validator cycle in its run context.
- **Impact:** This recal line was not consumed as success and is now retained as failed; one follow-up deepen line was queued for the next pass.
- **Suggested fixes:** Run EAT-QUEUE in a context where nested validator chain is available, or enqueue an explicit validator pass for roadmap handoff before continuing recal-heavy iterations.
- **Recovery:** Review updated roadmap/workflow state and validator artifacts, then retry with full nested validation capability.


### 2026-03-24 23:51 — Queue post–little-val: Task tool lacks validator enum

| Field | Value |
|-------|-------|
| pipeline | queue-dispatcher |
| severity | low |
| approval | n/a |
| timestamp | 2026-03-24T23:51:10Z |
| error_type | task-tool-schema |

#### Trace

- EAT-QUEUE dispatched Roadmap Task successfully for `repair-l1-postlv-contradictions-gmm-20260325T014200Z`.
- Post–little-val `Task(subagent_type: validator)` rejected: enum allows only generalPurpose \| explore \| shell \| best-of-n-runner.
- Layer 1 ran equivalent pass via `Task(generalPurpose)` with ValidatorSubagent preamble; report `.technical/Validator/roadmap-handoff-auto-layer1-repair-l1-20260325T031000Z.md`.

#### Summary

- **Root cause:** Host Task API in this Cursor build does not expose `validator` as a subagent_type.
- **Impact:** Post–little-val validator still executed under generalPurpose; queue consumption proceeded per `strict_nested_return_gates: false`.
- **Suggested fixes:** Enable `validator` in Task enum for Layer 1, or document generalPurpose fallback as supported for post-LV only.
- **Recovery:** None required if report path exists and Watcher-Result lines were appended.
