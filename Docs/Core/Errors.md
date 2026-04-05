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

### 2026-04-03 18:35 — EAT-QUEUE balance nested attestation gap (5.1 secondary rollup)

| Field | Value |
|-------|-------|
| pipeline | queue-dispatcher |
| severity | medium |
| approval | pending |
| timestamp | 2026-04-03T18:35:00Z |
| error_type | state-inconsistent |

#### Trace

- Queue entry `followup-deepen-phase5-51-rollup-nl-gwt-gmm-20260404T181000Z` → `Task(roadmap)` returned `little_val_ok: true` but `nested_subagent_ledger` shows `nested_validator_first` / `nested_validator_second` with `task_tool_invoked: false` (`nested_task_tool_not_bound`).
- Layer 1 `Task(validator)` `roadmap_handoff_auto` ran; report `.technical/Validator/roadmap-handoff-auto-gmm-20260404T182000Z-l1postlv-5-51-rollup.md`; `primary_code: nested_attestation_failure`, `recommended_action: needs_work`.
- `.technical/eat_queue_run_plan.json` unreadable (permission denied); python orchestrator bridge skipped.

#### Summary

- **Root cause:** Roadmap subagent host context lacks nested `Task` for mandatory balance-cycle validators; attestation does not meet Nested-Subagent-Ledger-Spec for clean Success.
- **Impact:** Triggering queue line marked `queue_failed` to avoid spin; Phase 5 primary follow-up appended; vault rollup changes may still need human review of decisions-log hygiene noted in validator report.
- **Suggested fixes:** Run roadmap deepen in a Task-capable host with nested validator/IRA, or treat Layer 1 post-LV as sufficient and keep `queue_failed` semantics for lines that shipped vault edits without nested proof.
- **Recovery:** Inspect validator report; optional manual decisions-log cleanup; next EAT-QUEUE processes `followup-deepen-phase5-primary-rollup-nl-gwt-gmm-20260403T183500Z`.

### 2026-04-04 00:56 — EAT-QUEUE: Task tool unavailable (Phase 5 primary rollup follow-up)

| Field | Value |
|-------|-------|
| pipeline | queue-eat-queue (Layer 1) |
| severity | medium |
| approval | pending |
| timestamp | 2026-04-04T00:56:38Z |
| error_type | mcp-dispatch |

#### Trace

- Pipeline: EAT-QUEUE / prompt-queue only; vault `/home/darth/Documents/Second-Brain`.
- Stage: A.5 dispatch; intended `Task(subagent_type: roadmap)` for queue entry `followup-deepen-phase5-primary-rollup-nl-gwt-gmm-20260403T183500Z` (`RESUME_ROADMAP`, `params.action: deepen`, `project_id: genesis-mythos-master`, `params.pipeline_mode: balance`).
- `layer0_task_correlation_id`: `de580896-4212-4980-a535-57fe7e05f034`.
- Host: Queue subagent context has no callable Cursor `Task` tool; dispatch aborted per `.cursor/rules/agents/queue.mdc` (no same-run fallback).
- A.2: one line filtered (`queue_failed: true`, id `followup-deepen-phase5-51-rollup-nl-gwt-gmm-20260404T181000Z`).

#### Summary

- **Root cause:** Layer 1 cannot invoke `Task(roadmap)` from this execution context, so the Roadmap subagent was not launched.
- **Impact:** `.technical/prompt-queue.jsonl` unchanged; valid follow-up line remains for retry.
- **Suggested fixes:** Run EAT-QUEUE from parent Cursor agent where `Task` is available for `subagent_type: roadmap`.
- **Recovery:** No vault mutation attempted by this dispatch. Re-run EAT-QUEUE when Task dispatch works.

### 2026-04-04 02:04 — EAT-QUEUE: Task tool unavailable (Phase 5.2 post-5.2.3 rollup deepen)

| Field | Value |
|-------|-------|
| pipeline | queue-eat-queue (Layer 1) |
| severity | medium |
| approval | pending |
| timestamp | 2026-04-04T02:04:57Z |
| error_type | mcp-dispatch |

#### Trace

- Pipeline: EAT-QUEUE / prompt-queue only; vault `/home/darth/Documents/Second-Brain`.
- Stage: A.5 dispatch; intended `Task(subagent_type: roadmap)` for `followup-deepen-phase5-52-rollup-post-523-gmm-20260404T235900Z` (`RESUME_ROADMAP`, `action: deepen`, `project_id: genesis-mythos-master`, `pipeline_mode: balance`).
- `layer0_task_correlation_id`: `cdeb5f4b-6c01-4149-ad16-ca5e21566275`.
- Host: no callable Cursor `Task` tool in this Layer 1 context.
- A.0.5: `.technical/eat_queue_run_plan.json` skipped — `parent_run_id` / intent `queue_entry_id` (`followup-deepen-phase5-523-worked-examples-replay-gmm-20260403T213500Z`) stale vs current queue line.
- A.2: filtered `queue_failed` line `followup-deepen-phase5-51-rollup-nl-gwt-gmm-20260404T181000Z`.
- Run-Telemetry: `.technical/Run-Telemetry/queue-eatq-cdeb5f4b-layer1-task-unavailable-20260404T020457Z.md`.

#### Summary

- **Root cause:** Same as prior entries: Queue subagent cannot invoke `Task(roadmap)` here.
- **Impact:** Prompt queue unchanged; operator should regenerate `eat_queue_run_plan.json` after queue edits (`python3 -m scripts.eat_queue_core.full_cycle` or plan build) so orchestrator matches head line, then re-run EAT-QUEUE with Task-capable host.
- **Suggested fixes:** Parent chat dispatches Layer 1 with Task available; refresh Python plan for current JSONL.
- **Recovery:** No pipeline vault work attempted.

### 2026-04-05 01:35 — EAT-QUEUE: Phase 5.2 rollup — balance nested gate + L1 contradictions_detected

| Field | Value |
|-------|-------|
| pipeline | queue-eat-queue (Layer 1) |
| severity | high |
| approval | pending |
| timestamp | 2026-04-05T01:35:00Z |
| error_type | state-inconsistent |

#### Trace

- Queue entry: `followup-deepen-phase5-52-rollup-post-523-gmm-20260404T235900Z` (`RESUME_ROADMAP` deepen, `pipeline_mode: balance`, `project_id: genesis-mythos-master`).
- `layer0_task_correlation_id`: `7a1538b1-cc74-4853-919d-c69e9e01f26d`.
- Roadmap subagent: `contract_satisfied: false`; nested `Task(validator)` / IRA unavailable on runner; ledger steps `nested_validator_*` / `ira_post_first_validator` with `task_tool_invoked: false` and `outcome: task_error`.
- A.5d checklist: balance deepen requires all three nested validator/IRA steps `task_tool_invoked: true` — **failed**; disposition `layer1_nested_gate_failure`, `nested_validation_provisional`.
- L1 `Task(validator)` `roadmap_handoff_auto`: **high** / `block_destructive`, `primary_code: contradictions_detected`; report `.technical/Validator/roadmap-handoff-auto-gmm-20260405T012500Z-followup-deepen-phase5-52-rollup-post-523.md`.
- A.5b.3: appended repair line `repair-l1postlv-phase52-contradictions-distilled-workflow-gmm-20260405T013000Z` (`handoff-audit`). Triggering deepen line **retained** on prompt-queue per A.5d (not consumed).

#### Summary

- **Root cause:** Roadmap runner cannot invoke nested `Task` for balance-mode cycle; independent L1 validator then found coherence contradictions (distilled-core routing vs workflow cursor; Phase 5.2 note status vs body).
- **Impact:** Rollup content may be in vault but attestation and hostile pass are provisional; operator must run repair handoff-audit and reconcile state files before treating Phase 5.2 as closed.
- **Suggested fixes:** Process repair queue line next EAT-QUEUE; patch `distilled-core.md` and Phase 5.2 secondary note frontmatter per validator report; re-run deepen only after nested Task surface works or profile adjusted per ops policy.
- **Recovery:** Validator report path above; per-change snapshots if user restores prior vault versions.

### 2026-04-05 18:20 — EAT-QUEUE lane sandbox: Phase 6.1 mint — balance nested gate provisional + L1 state_hygiene_failure

| Field | Value |
|-------|-------|
| pipeline | queue-eat-queue (Layer 1) |
| severity | high |
| approval | pending |
| timestamp | 2026-04-05T18:20:00Z |
| error_type | state-inconsistent |

#### Trace

- **PQ:** `.technical/parallel/sandbox/prompt-queue.jsonl`; **queue_lane_filter:** `sandbox`; **parallel_track:** `sandbox`.
- **Consumed id:** `followup-deepen-phase6-61-mint-slice-manifest-sandbox-gmm-20260405T151000Z` (`RESUME_ROADMAP` deepen, `pipeline_mode: balance`, `project_id: sandbox-genesis-mythos-master`).
- **Roadmap `Task` return:** `#review-needed`; `nested_validator_first` → `task_error` / `nested_task_unavailable` in L2 host; `ira_post_first_validator` / `nested_validator_second` skipped (prerequisite); **A.5d** balance deepen checklist **not** fully satisfied (provisional).
- **L1 `Task(validator)` `roadmap_handoff_auto`:** report `.technical/Validator/roadmap-auto-validation-20260405T181500Z.md`; **high** / `block_destructive`; **primary_code:** `state_hygiene_failure` (distilled-core vs `workflow_state` / Phase 6.1 cursor; plus `safety_unknown_gap` for missing L2 nested validator artifact).
- **A.5b:** Appended **repair** `repair-l1postlv-sandbox-gmm-distilled-hygiene-6-61-20260405T182000Z` (`handoff-audit`) and roadmap **forward** `followup-deepen-phase6-611-tertiary-sandbox-gmm-20260405T160500Z` to sandbox PQ; **GitForge** skipped (`invoke_only_on_clean_success`).

#### Summary

- **Root cause:** L2 roadmap host could not run nested `Task(validator)`; L1 hostile pass then flagged **state hygiene** (rollup / distilled-core narrative vs live cursor after 6.1 mint).
- **Impact:** Phase 6.1 secondary note may exist on disk, but closure is **provisional** until handoff-audit repair runs and distilled-core is reconciled.
- **Suggested fixes:** Run **EAT-QUEUE lane sandbox** again (repair first); patch `distilled-core.md` per validator report; ensure future roadmap runs use a **Task-capable** host for balance nested cycles.
- **Recovery:** Validator report path above; Watcher-Result pair for same `requestId` (VALIDATE + RESUME_ROADMAP segments).
