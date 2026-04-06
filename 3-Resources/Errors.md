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

### 2026-04-05 23:35 — EAT-QUEUE lane godot: Phase 6.1 mint — nested Task unavailable + L1 contradictions_detected

| Field | Value |
|-------|-------|
| pipeline | queue-eat-queue (Layer 1) |
| severity | high |
| approval | pending |
| timestamp | 2026-04-05T23:35:00Z |
| error_type | state-inconsistent |

#### Trace

- **PQ:** `.technical/parallel/godot/prompt-queue.jsonl`; **queue_lane_filter:** `godot`; **parallel_track:** `godot`.
- **A.0.4:** `pool_sync` hydrated godot PQ from central pool (1 line copied).
- **Consumed id:** `followup-deepen-phase6-61-mint-slice-manifest-godot-gmm-20260405T151000Z` (`RESUME_ROADMAP` deepen, `pipeline_mode: balance`, `project_id: godot-genesis-mythos-master`).
- **Roadmap `Task` return:** `#review-needed`; nested `Task(validator)` / IRA / second validator → `task_error` (`task_tool_not_exposed_in_session`); ledger records `task_tool_invoked: true` with host rejection; structural `little_val_ok: true`; Phase 6.1 secondary + CDR minted per subagent summary.
- **L1 `Task(validator)` `roadmap_handoff_auto`:** report `.technical/Validator/roadmap-handoff-auto-gmm-l1postlv-phase6-1-godot-20260405.md`; **high** / `block_destructive`; **primary_code:** `contradictions_detected` (distilled-core Phase 6 cursor authority vs `workflow_state` **6.1.1**).
- **A.7:** Dual cleanup removed consumed id from pool + godot PQ; appended **repair-first** `repair-l1postlv-distilled-core-contradiction-godot-20260405T233500Z` (`handoff-audit`) then forward `followup-deepen-phase611-mint-first-tertiary-godot-gmm-20260405T224800Z` (`deepen`). **GitForge** skipped (`invoke_only_on_clean_success`).

#### Summary

- **Root cause:** Roadmap subagent session could not run nested `Task` for balance-mode validator/IRA cycle; L1 hostile pass then flagged **contradictions** in rollup authority between `distilled-core.md` and live workflow cursor.
- **Impact:** Phase 6.1 artifacts are on disk but attestation is **provisional**; next godot-lane pass should run **handoff-audit** repair before tertiary **6.1.1** deepen unless operator reorders.
- **Suggested fixes:** Run **EAT-QUEUE lane godot**; reconcile `distilled-core.md` per validator report; use Task-capable host for balance nested cycles when possible.
- **Recovery:** Validator report path above; Watcher-Result canonical + `Watcher-Result-godot.md` (VALIDATE + primary for same `requestId`).

### 2026-04-05 09:57 — GitForge skipped (sandbox lock held / timeout)

| Field | Value |
|-------|-------|
| pipeline | queue-eat-queue (Layer 1 A.7a) |
| severity | low |
| approval | n/a |
| timestamp | 2026-04-05T09:57:00Z |
| error_type | gitforge-task-failure |

#### Trace

- After successful sandbox prompt-queue **A.7**, **`Task(gitforge)`** ran with `mode: balance`; `scripts/gitforge_lock.py acquire` for track **sandbox** exited **1** (lock held or 30s timeout). No commit, push, or export. Queue consumption **not** rolled back.

#### Summary

- **Root cause:** Concurrent or stale **`.technical/.gitforge.lock`** (or another process holding the sandbox GitForge lock).
- **Impact:** Vault git/export tail did not run; roadmap queue state remains as written.
- **Suggested fixes:** Retry GitForge when idle; clear stale lock if safe; see `agents/gitforge.md` and git-audit-log entry for **2026-04-05 09:57 UTC**.
- **Recovery:** Manual `git status` / export push if needed; optional re-run EAT-QUEUE with only GitForge tail is not supported — run dedicated GitForge or clear lock.

### 2026-04-05 23:50 — Godot lane EAT-QUEUE: Phase 6.1.1 deepen provisional (L1 state_hygiene_failure)

| Field | Value |
|-------|-------|
| pipeline | queue-eat-queue (Layer 1 godot track) |
| severity | high |
| approval | pending |
| timestamp | 2026-04-05T23:50:00Z |
| error_type | state-inconsistent |

#### Trace

- **PQ:** `.technical/parallel/godot/prompt-queue.jsonl`; **queue_lane_filter:** `godot`; **parallel_track:** `godot`.
- **A.0.4:** `pool_sync` ran (`copied_count: 0`); **EQPLAN** missing → legacy dispatch.
- **A.4c `repair_first`:** Neither queue line had `queue_priority: repair`; timestamp order gave sole **initial** slot to `followup-deepen-phase611-mint-first-tertiary-godot-gmm-20260405T224800Z` (deepen); `repair-l1postlv-*` (handoff-audit) **not dispatchable** this pass (no cleanup slot under `repair_first`).
- **`Task(roadmap)`:** Subagent reported structural work + `#review-needed`; nested `Task(validator)` / IRA → `task_error` (`task_tool_not_exposed_in_session`); ledger rows `task_tool_invoked: true` + `task_error`.
- **`Task(validator)` L1 `roadmap_handoff_auto`:** report `.technical/Validator/roadmap-handoff-auto-gmm-20260405T234500Z-l1postlv-followup-deepen-phase611.md`; **high** / `block_destructive`; **primary_code:** `state_hygiene_failure`, `contradictions_detected` (workflow_state body vs frontmatter / distilled-core dual truth).
- **A.5d:** `suppress_clean_drain`; **did not** add `followup-deepen-phase611-*` to `processed_success_ids`.
- **Queue restore:** Godot **PQ** was found **empty** mid-run (prior wipe); restored **two** JSONL lines from hand-off snapshot and merged ids into central **pool** (3 lines total with sandbox).
- **GitForge:** skipped (`invoke_only_on_clean_success`).

#### Summary

- **Root cause:** Balance nested helpers unavailable in roadmap subagent session; L1 hostile pass flagged **state hygiene / contradictions** after deepen attempt; track **PQ** had been cleared elsewhere — restored for operator continuity.
- **Impact:** Entry **not consumed**; next **EAT-QUEUE lane godot** should prefer **handoff-audit** repair (consider tagging `queue_priority: repair` or **`forward_first`** in Config for blocking repairs before forward deepen).
- **Suggested fixes:** Reconcile `workflow_state.md` / `distilled-core.md` per validator report; run **handoff-audit** repair line first; use host where nested `Task(validator)` works for balance roadmap runs.
- **Recovery:** Validator report path above; Watcher-Result + `Watcher-Result-godot.md` (VALIDATE + primary **failure** for same `requestId`).

### 2026-04-05 10:26 — EAT-QUEUE lane godot: Task(roadmap) not exposed to Layer 1 host

| Field | Value |
|-------|-------|
| pipeline | queue-eat-queue (Layer 1 godot track) |
| severity | medium |
| approval | pending |
| timestamp | 2026-04-05T10:26:30Z |
| error_type | mcp-dispatch |

#### Trace

- **PQ:** `.technical/parallel/godot/prompt-queue.jsonl`; **central pool:** `.technical/prompt-queue.jsonl`; **queue_lane_filter:** `godot`; **parallel_track:** `godot`.
- **Step 0:** No `Ingest/Decisions/**` wrapper had frontmatter `approved: true` (no apply-from-wrapper work).
- **A.0.4:** `pool_sync` **ok** (`copied_count: 2`; ids `repair-l1postlv-distilled-core-contradiction-godot-20260405T233500Z`, `followup-deepen-phase61-rollup-post-611-godot-gmm-20260406T000000Z`).
- **EQPLAN:** `.technical/parallel/godot/eat_queue_run_plan.json` **missing** → legacy LLM/dispatch path (Config `python_orchestrator_enabled: true` but no plan file).
- **Dispatch:** Cursor Queue subagent session has **no** callable `Task` tool → **no** `Task(subagent_type: roadmap)` per entry; **A.7** **not** applied (`processed_success_ids` empty).
- **Watcher-Result:** canonical + `Watcher-Result-godot.md` failure lines for both queue `id`s; **eat_queue_run_id** `eatq-20260405T102630Z-godot-l1`.

#### Summary

- **Root cause:** Layer 1 orchestrator cannot invoke nested pipeline subagents without the host `Task` tool; this run stopped after hydration and ordering.
- **Impact:** Both godot RESUME_ROADMAP lines remain in **PQ** and pool; no roadmap mutations from this pass.
- **Suggested fixes:** Re-run **EAT-QUEUE lane godot** from a parent Cursor agent where `Task(queue)` / nested `Task(roadmap)` is available, or generate **EQPLAN** via `scripts.eat_queue_core.full_cycle` if using the Python orchestrator bridge.
- **Recovery:** No vault rollback needed; duplicate **Watcher-Result** lines for the same `requestId` are acceptable for audit when re-dispatching after a host fix.

### 2026-04-06 11:06 — EAT-QUEUE godot: nested_attestation_failure after Task(roadmap) (balance deepen)

| Field | Value |
|-------|-------|
| pipeline | queue-eat-queue (Layer 1 godot track) |
| severity | medium |
| approval | pending |
| timestamp | 2026-04-06T11:06:14Z |
| error_type | state-inconsistent |

#### Trace

- **parent_run_id:** `layer1-eatq-godot-20260406T120500Z`
- **A.0.4:** `pool_sync` copied 5 ids into `.technical/parallel/godot/prompt-queue.jsonl`
- **A.0.5:** `full_cycle` wrote `.technical/parallel/godot/eat_queue_run_plan.json` (4 intents)
- **Task(roadmap):** queue_entry_id `followup-deepen-phase61-rollup-post-611-godot-gmm-20260406T000000Z` — `roadmap_core` ran; **nested_validator_first / ira_post_first_validator / nested_validator_second** → `task_tool_invoked: false`, `task_error` (Task unavailable in roadmap subagent host); `task_harden_result.contract_satisfied: false`
- **Task(validator) L1:** `roadmap_handoff_auto` → `severity: medium`, `primary_code: state_hygiene_failure`, `recommended_action: needs_work`; report `.technical/Validator/roadmap-handoff-auto-gmm-l1postlv-phase61-followup-20260406T120500Z.md`
- **A.7:** **not** consumed (FINAL GATEKEEPER + hygiene provisional); pass3 intents **not** dispatched in this session
- **Telemetry:** `.technical/Run-Telemetry/godot/queue-layer1-eatq-godot-20260406T110614Z.md`

#### Summary

- **Root cause:** Roadmap subagent host cannot nest `Task(validator)` / `Task(internal-repair-agent)`; balance micro_workflow attestation fails despite `roadmap_core` + `little_val_ok`.
- **Impact:** deepen line and remaining repair lines stay on **PQ** and central pool; Watcher-Result canonical + `Watcher-Result-godot.md` (VALIDATE then primary **failure**).
- **Suggested fixes:** Run balance roadmap from a Cursor configuration where roadmap subagent can call nested `Task`, or temporarily use **speed** profile / Config that does not require nested helper proof for this host.
- **Recovery:** Review validator report; optional manual hygiene edit to `roadmap-state` consistency bullet cited in report.

### 2026-04-06 16:20 — EAT-QUEUE sandbox: nested_attestation_failure + L1 state_hygiene_failure (deepen 6.1.2)

| Field | Value |
|-------|-------|
| pipeline | queue-eat-queue (Layer 1 sandbox track) |
| severity | medium |
| approval | pending |
| timestamp | 2026-04-06T16:20:00Z |
| error_type | state-inconsistent |

#### Trace

- **queue_entry_id:** `followup-deepen-phase612-sandbox-gmm-20260406T004500Z`
- **parent_run_id:** `l1-sandbox-eatq-20260406T150000Z`
- **A.0.4:** `pool_sync` hydrated sandbox **PQ** from central pool
- **Task(roadmap):** balance deepen; `nested_validator_first` / `ira_post_first_validator` / `nested_validator_second` → `task_tool_invoked: false`, `task_error` `helper_launch_surface_missing` / `task_tool_not_available_in_context`
- **Task(validator) L1 (b1):** `roadmap_handoff_auto` → `severity: medium`, `recommended_action: needs_work`, `primary_code: state_hygiene_failure`, `reason_codes` include `missing_roll_up_gates`, `safety_unknown_gap`
- **Report:** `3-Resources/Second-Brain/Validator-Reports/roadmap_handoff_auto/sandbox-genesis-mythos-master-20260406T160500Z-l1postlv-b1-deepen-612.md`
- **Queue writes:** appended `followup-deepen-phase613-sandbox-gmm-20260406T083000Z`, `repair-l1-handoff-audit-sandbox-gmm-612-hygiene-20260406T161500Z` to central pool; re-ran `pool_sync` for sandbox **PQ**
- **A.7:** **did not** add `612` to `processed_success_ids` (FINAL GATEKEEPER + nested attestation + hygiene provisional)

#### Summary

- **Root cause:** Roadmap subagent host cannot nest `Task(validator)` / `Task(internal-repair-agent)`; L1 hostile validator still found `state_hygiene_failure` (workflow_state callout vs live cursor).
- **Impact:** Entry **612** remains on **PQ** and central pool; **613** deepen follow-up and **handoff-audit** repair queued; Watcher-Result canonical + `Watcher-Result-sandbox.md` (VALIDATE then primary **failure**).
- **Suggested fixes:** Run balance roadmap from a host where nested `Task` is available; run **handoff-audit** repair first; align Phase 5 “Authoritative cursor” callout in `workflow_state.md` with frontmatter `6.1.3`.
- **Recovery:** No automatic rollback; use validator report and repair queue entry.

### 2026-04-05 18:09 — Godot lane deepen nested attestation (Task absent in roadmap subagent)

| Field | Value |
|-------|-------|
| pipeline | EAT-QUEUE / RESUME_ROADMAP |
| severity | medium |
| approval | pending |
| timestamp | 2026-04-05T18:09:24Z |
| error_type | state-inconsistent |

#### Trace

- Queue entry: `followup-deepen-phase61-rollup-post-611-godot-gmm-20260406T000000Z`
- Roadmap subagent reported `nested_task_tool_absent_in_session` for nested_validator_first / IRA / second validator (balance deepen).
- Layer 1 post–little-val: `contract_satisfied: false`, `primary_code: safety_unknown_gap`, report `.technical/Validator/l1postlv-b1-phase61-rollup-nested-task-absent-godot-20260406T180500Z.md`.

#### Summary

- **Root cause:** Roadmap Task subagent host lacks nested `Task(validator)`/`Task(IRA)` in schema; balance-mode attestation chain could not run.
- **Impact:** Entry not consumed at A.7; workflow_state log row + roadmap-state bump still applied idempotently; operator must re-run deepen on Task-capable host or adjust profile.
- **Suggested fixes:** Run same queue line from parent chat with full Task nesting; or temporary `pipeline_mode: speed` only if policy allows (not recommended without human gate).
- **Recovery:** Re-queue unchanged line remains on `.technical/parallel/godot/prompt-queue.jsonl`.

### 2026-04-07 10:35 — Sandbox pool-remint-613 balance nested Task unavailable (nested attestation)

| Field | Value |
|-------|-------|
| pipeline | EAT-QUEUE / RESUME_ROADMAP |
| severity | high |
| approval | pending |
| timestamp | 2026-04-07T10:35:00Z |
| error_type | mcp-api |

#### Trace

- **Queue entry id:** `pool-remint-613-sandbox-gmm-20260406120002Z`
- **Lane:** `sandbox`, **parallel_track:** `sandbox`, **PQ:** `.technical/parallel/sandbox/prompt-queue.jsonl`
- **Task(roadmap):** balance deepen; `nested_validator_first`, `ira_post_first_validator`, `nested_validator_second` → `task_tool_invoked: false`, `outcome: task_error`, `host_error_class: nested_task_unavailable`
- **Task(validator) L1 (b1):** completed; `roadmap_handoff_auto` → `needs_work`, `primary_code: missing_roll_up_gates` (advisory on conceptual track)
- **A.7:** **did not** consume `613`; removed `pool-remint-612` from sandbox PQ + central pool only
- **Watcher-Result:** `nested_attestation_failure` primary line for `613` (canonical + sandbox mirror)

#### Summary

- **Root cause:** Roadmap subagent runtime cannot invoke nested `Task(validator)` / `Task(internal-repair-agent)`; balance-mode ledger attestation chain incomplete despite vault writes.
- **Impact:** Entry **613** retained on **PQ** and central pool for retry; **612** consumed successfully; follow-up `followup-deepen-phase611-after-612-outoforder-…` remains on sandbox PQ.
- **Suggested fixes:** Re-run **613** from a Cursor host where roadmap subagent can nest `Task` helpers; or operator verifies vault artifacts manually and uses `speed` profile only if policy allows.
- **Recovery:** Re-dispatch `pool-remint-613` after nested Task availability is restored; see Nested-Subagent-Ledger-Spec attestation invariants.

### 2026-04-07 10:55 — EAT-QUEUE Layer1 Task(roadmap) unavailable (host)

| Field | Value |
|-------|-------|
| pipeline | EAT-QUEUE / queue_dispatch |
| severity | high |
| approval | pending |
| timestamp | 2026-04-07T10:55:00Z |
| error_type | mcp-dispatch |

#### Trace

- **Context:** Queue/Dispatcher subagent run for `EAT-QUEUE lane sandbox`; **A.0.4** `pool_sync` ran; **followup-deepen-phase611-after-612-outoforder-sandbox-gmm-20260407T100000Z** was re-appended to **central** `.technical/prompt-queue.jsonl` after fanout had dropped a sandbox-only line (operator intent preserved).
- **Failure:** Cursor **`Task`** tool not exposed to the queue subagent host — **`Task(subagent_type: roadmap)`** could not be issued for **`pool-remint-613-sandbox-gmm-20260406120002Z`**.
- **Proof-on-failure:** Watcher-Result + this entry; **no** queue consumption (**A.7** skipped).

#### Summary

- **Root cause:** Host capability gap — pipeline dispatch requires real `Task` launch per dispatcher.mdc / queue.mdc; no same-run fallback.
- **Impact:** Both sandbox PQ lines remain for a future run; second line **A.4c** `repair_first` non-dispatchable in initial pass (logged as skip success in Watcher-Result).
- **Suggested fixes:** Re-run **EAT-QUEUE lane sandbox** from a Layer 0 chat where **`Task(queue)`** and nested **`Task(roadmap)`** are available.
- **Recovery:** Same queue file state; no A.7 rewrite applied this run.

### 2026-04-07 13:35 — EAT-QUEUE sandbox phase611 nested attestation + L1 state_hygiene_failure

| Field | Value |
|-------|-------|
| pipeline | EAT-QUEUE / queue_dispatch |
| severity | medium |
| approval | pending |
| timestamp | 2026-04-07T13:35:00Z |
| error_type | state-inconsistent |

#### Trace

- **Queue entry id:** `followup-deepen-phase611-after-pool-remint-613-20260407T123000Z`
- **Lane:** `sandbox`, **PQ:** `.technical/parallel/sandbox/prompt-queue.jsonl`
- **Task(roadmap):** returned `#review-needed`; `nested_validator_first` / `ira_post_first_validator` / `nested_validator_second` → `task_tool_invoked: false`, `nested_task_unavailable`
- **Task(validator) L1 (b1):** `roadmap_handoff_auto` → `needs_work`, `primary_code: state_hygiene_failure` (workflow_state embedded note vs YAML/Log); report `.technical/Validator/roadmap-handoff-auto-sandbox-gmm-20260407T131500Z-l1postlv-followup-deepen-phase611.md`
- **A.7:** triggering id **not** consumed; appended follow-up deepen secondary 6.1 rollup + `repair-l1-hygiene-workflow-state-embedded-sandbox-20260407T133100Z` to sandbox PQ and central pool

#### Summary

- **Root cause:** Roadmap subagent host cannot nest `Task(validator)` / `Task(IRA)`; balance ledger incomplete. Independent L1 validator additionally flagged **state_hygiene_failure** on coordination surfaces.
- **Impact:** Primary queue line retained; repair and forward follow-ups queued; `suppress_clean_drain=true`.
- **Suggested fixes:** Run `repair-l1-hygiene-workflow-state-embedded-sandbox` handoff-audit; align `workflow_state.md` embedded callout; re-run roadmap deepen when nested `Task` is available or use policy-approved profile.
- **Recovery:** Next **EAT-QUEUE lane sandbox** processes repair-first ordering per A.4c.

### 2026-04-07 17:00 — EAT-QUEUE Task(queue) aborted; Layer 0 manual hand-off close (sandbox)

| Field | Value |
|-------|-------|
| pipeline | queue-eat-queue (Layer 0 → Layer 1) |
| severity | medium |
| approval | pending |
| timestamp | 2026-04-07T17:00:00Z |
| error_type | mcp-dispatch |

#### Trace

- **Context:** Operator **aborted** Cursor **`Task(subagent_type: queue)`** before the Queue/Dispatcher subagent returned (miss-click). **`handoff_out`** existed for correlation **`33fb2a1d-ef37-4bcf-b17c-bdc2caa9f462`** (retry after prior abort) with **no** Layer 1 **`return_in`**.
- **Layer 0 manual completion:** Appended **`return_in`** to **`.technical/parallel/sandbox/task-handoff-comms.jsonl`**, **Watcher-Result** + **Watcher-Result-sandbox** (VALIDATE + primary `failure` for **`followup-deepen-phase611-after-pool-remint-613-20260407T123000Z`**, `completed: 2026-04-07T17:00:00.000Z`), and **Run-Telemetry** `[[.technical/Run-Telemetry/sandbox/queue-layer0-manual-eatq-recovery-20260407T170000Z|queue-layer0-manual-eatq-recovery-20260407T170000Z]]`.
- **Disposition (no new L1 run):** Aligns with last completed Layer 1 pass **`eatq-layer1-sandbox-20260407T150500Z`** — nested roadmap **`task_tool_invoked: false`** on mandatory nested steps; L1 **`roadmap_handoff_auto`** **`severity: high`**, **`primary_code: contradictions_detected`**, **`state_hygiene_failure`**; entry **not** in **`processed_success_ids`**; **A.7** leaves **all three** lines on **`.technical/parallel/sandbox/prompt-queue.jsonl`**.

#### Summary

- **Root cause:** **`Task(queue)`** invocation did not finish; Layer 1 queue processor never ran for that attempt.
- **Impact:** **No** queue rewrite; sandbox **PQ** unchanged (three lines). Audit trail closed in **task-handoff-comms** + Watcher + telemetry.
- **Suggested fixes:** Re-run **`EAT-QUEUE lane sandbox`** when **`Task(queue)`** is stable; resolve **workflow_state** / roadmap-state hygiene per validator report **`.technical/Validator/roadmap-handoff-auto-sandbox-gmm-20260407T150500Z-l1postlv-phase611-idempotent.md`**.
- **Recovery:** N/A — manual close only; no vault rollback.

### 2026-04-07 18:35 — EAT-QUEUE sandbox RESUME_ROADMAP nested attestation + L1 state_hygiene_failure (phase611)

| Field | Value |
|-------|-------|
| pipeline | queue-eat-queue (Layer 1) |
| severity | medium |
| approval | pending |
| timestamp | 2026-04-07T18:35:00Z |
| error_type | state-inconsistent |

#### Trace

- **PQ:** `.technical/parallel/sandbox/prompt-queue.jsonl` — dispatched **`followup-deepen-phase611-after-pool-remint-613-20260407T123000Z`** (`queue_pass_phase=initial`, `parent_run_id=eatq-sandbox-layer1-20260407T180500Z`).
- **Task(roadmap):** returned `#review-needed`; `nested_validator_first` → `task_error` / `nested_task_unavailable`; balance-mode ledger attestation incomplete.
- **Task(validator) L1 (b1):** `roadmap_handoff_auto` → `severity: medium`, `recommended_action: needs_work`, `primary_code: state_hygiene_failure`, `reason_codes: state_hygiene_failure, contradictions_detected`; report `.technical/Validator/roadmap-handoff-auto-sandbox-gmm-20260407T183000Z-l1postlv-phase61-secondary-rollup-conceptual-v1.md`.
- **A.7:** id **not** consumed; **no** mid-run PQ append (follow-up `next_entry` suppressed while hygiene provisional).

#### Summary

- **Root cause:** Roadmap subagent could not invoke nested `Task(validator)`; L1 hostile validator independently flagged rollup-surface contradictions vs **18:05** cursor.
- **Impact:** Queue line retained; `suppress_clean_drain=true`; three sandbox PQ lines unchanged.
- **Suggested fixes:** Prefer **`repair-l1-hygiene-workflow-state-embedded-sandbox`** (`handoff-audit`) or add **`queue_priority: repair`** so **repair_first** orders hygiene before duplicate deepen lines; align `distilled-core.md` / `workflow_state.md` embedded notes per validator report.
- **Recovery:** Re-run **EAT-QUEUE lane sandbox** after hygiene repair; optional operator edit to mark repair line as repair-class.

### 2026-04-07 21:15 — EAT-QUEUE sandbox RESUME_ROADMAP Task(roadmap) nested_task_unavailable (secondary-61 deepen)

| Field | Value |
|-------|-------|
| pipeline | queue-eat-queue (Layer 1) |
| severity | medium |
| approval | pending |
| timestamp | 2026-04-07T21:15:00Z |
| error_type | mcp-api |

#### Trace

- **PQ:** `.technical/parallel/sandbox/prompt-queue.jsonl` — dispatched **`followup-deepen-secondary-61-rollup-post-611-mint-20260407T133000Z`** (`queue_pass_phase=initial`, `parent_run_id=eatq-sandbox-20260407T210500Z-layer1-p1`).
- **Task(roadmap):** returned `#review-needed`; `nested_validator_first` / `ira_post_first_validator` / `nested_validator_second` recorded **`task_error`** with **`nested_task_unavailable`** (Cursor `Task` tool not exposed in roadmap subagent context).
- **Layer 1 gate:** **No** `processed_success_ids` append; **no** L1 `Task(validator)` **(b1)** — pipeline return was not a tiered Success path with nested ledger satisfied.
- **A.4c:** Remaining **`repair-l1-hygiene-workflow-state-embedded-sandbox-20260407T133100Z`** and **`resume-deepen-phase6-primary-rollup-sandbox-gmm-20260407T194500Z`** **skipped** (`skipped: primary_roadmap_pass1_cap`) same project **repair_first** initial pass.

#### Summary

- **Root cause:** Host/subagent surface for **`Task(roadmap)`** could not invoke nested **`Task(validator)`** / **`Task(internal-repair-agent)`** — balance-mode attestation cannot complete in that environment.
- **Impact:** All **three** sandbox PQ lines **retained**; **A.7** no consumption.
- **Suggested fixes:** Run **EAT-QUEUE** from a Cursor host where **RoadmapSubagent** nested **`Task`** calls succeed; or run operator **VALIDATE** / manual validator pass; see **Nested-Subagent-Ledger-Spec** attestation invariants.
- **Recovery:** Re-dispatch when **`Task`** nesting is available; queue order unchanged (repair line remains for next `repair_first` ordering).

### 2026-04-06 19:32 — EAT-QUEUE sandbox Layer 1 Task(roadmap) not invocable (host)

| Field | Value |
|-------|-------|
| pipeline | queue-eat-queue (Layer 1) |
| severity | high |
| approval | pending |
| timestamp | 2026-04-06T19:32:21Z |
| error_type | mcp-api |

#### Trace

- **PQ:** `.technical/parallel/sandbox/prompt-queue.jsonl` — **A.0.4** `pool_sync` **ok** (`copied_count: 3`).
- **A.4c** (`roadmap_pass_order: repair_first`): initial roadmap slot for **`sandbox-genesis-mythos-master`** → **`followup-deepen-secondary-61-rollup-post-611-mint-20260407T133000Z`** (earliest timestamp among three `RESUME_ROADMAP` lines; **`repair-l1-hygiene-workflow-state-embedded-sandbox-20260407T133100Z`** not tagged `queue_priority: repair`).
- **Dispatch:** Cursor **`Task`** tool **not available** in this Layer 1 execution context — **no** `Task(roadmap)` launch (Proof-on-failure per Subagent-Safety-Contract).
- **A.7:** **no** `processed_success_ids`; PQ **unchanged** (three lines).

#### Summary

- **Root cause:** Queue orchestrator requires **`Task(subagent_type: roadmap)`**; host did not expose the Task API to this run.
- **Impact:** No roadmap work; no Watcher **(b1)** `Task(validator)`; central pool + sandbox PQ retain all three entries.
- **Suggested fixes:** Re-run **EAT-QUEUE lane sandbox** from a Cursor session where **`Task(queue)`** / nested **`Task(roadmap)`** are wired; optional: add **`queue_priority: repair`** on **`repair-l1-hygiene-workflow-state-embedded-sandbox-20260407T133100Z`** so **repair_first** sub-sort prioritizes hygiene before the 13:30 deepen line.
- **Recovery:** Same as impact — re-dispatch when Task is available; no vault rollback.
