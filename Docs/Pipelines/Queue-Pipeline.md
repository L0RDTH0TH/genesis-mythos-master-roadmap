# Queue Pipeline (EAT-QUEUE / PROCESS TASK QUEUE)

**Version: 2026-03 – post-subagent migration**

Describes the Queue/Dispatcher flow: Step 0 (always-check wrappers), two queues (prompt-queue.jsonl vs Task-Queue.md), parse/validate/order, dispatch by mode, Watcher-Result, clear passed / tag failed. The Queue runs in the main agent; it does not run as a separate subagent.

---

## Purpose

Single reference for what runs when you say **EAT-QUEUE** or **PROCESS TASK QUEUE**: which rule runs, Step 0 semantics, two-queue routing, mode normalization and dispatch, and where to find validation and RESUME-ROADMAP append rules.

---

## Triggers

- **EAT-QUEUE** *(canonical)*, **Process queue**, **EAT-CACHE** / **eat cache** → Prompt-queue flow (Part A).
- **PROCESS TASK QUEUE** (or EAT-QUEUE with clear intent for the task queue) → Task-queue flow (Part B).

The **Dispatcher** (`.cursor/rules/always/dispatcher.mdc`) routes these phrases to the **Queue rule** (`.cursor/rules/agents/queue.mdc`).

**Overnight / anti-circle:** One EAT-QUEUE session caps **`Task(roadmap)`** invocations (**queue.mdc** **A.5.0.2**; default from Second-Brain-Config). Remaining roadmap lines stay on disk for the next message. Roadmap deepen uses per-subphase caps and stagnation-driven slice exit (Parameters § Anti-Circling & Overnight Safety; **roadmap-deepen**). See also [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]].

---

## Two queues

| Queue | File | Modes |
|-------|------|--------|
| **Prompt queue** | `.technical/prompt-queue.jsonl` | INGEST MODE, ROADMAP MODE, RESUME-ROADMAP, DISTILL MODE, EXPRESS MODE, ARCHIVE MODE, ORGANIZE MODE, RESEARCH-AGENT, SEEDED-ENHANCE, NORMALIZE-MASTER-GOAL, etc. (canonical order in Queue-Sources). |
| **Task queue** | `3-Resources/Task-Queue.md` | TASK-ROADMAP, TASK-COMPLETE, ADD-ROADMAP-ITEM, EXPAND-ROAD, REORDER-ROADMAP, DUPLICATE-ROADMAP, MERGE-ROADMAPS, EXPORT-ROADMAP, PROGRESS-REPORT. |

## Harness (single writer; Part A)

Normative **PQ** reads, **EQPLAN** emission, optional **snapshot** / **verify**, **append_entries** (Step 0 / mid-run), and **rewrite_consumed** (**A.7**) go through **`python3 -m scripts.eat_queue_core.harness`**. Layer 1 does **not** define dispatch order independently of **EQPLAN** except where **queue.mdc** explicitly allows (e.g. empty **`intents`** → **A.1b**). See [[3-Resources/Second-Brain/Docs/Queue-Harness-Architecture|Queue-Harness-Architecture]] and **queue.mdc** **A.0.5**.

---

## Prompt-queue flow (Part A) — steps

Step IDs match **`.cursor/rules/agents/queue.mdc`**. **A.7a** (GitForge) follows **A.7**; there is **no** A.8.

1. **A.0 — Always-check wrappers (runs first, every run)**  
   Enumerate `Ingest/Decisions/**`. For each wrapper with `approved: true` (or `re-wrap: true` / `re-try: true`) and not processed: use **feedback-incorporate** → apply per wrapper_type (ingest apply-mode, phase-direction, handoff-readiness, organize, archive, distill-apply-from-wrapper, express-apply-from-wrapper, low-confidence, error). Update wrapper; **move wrapper to** `4-Archives/Ingest-Decisions/` (ensure_structure, per-change snapshot, move dry_run then commit). Set **approved_wrappers_remaining** if any approved unprocessed wrappers remain. Then proceed to A.1 (no dependency on queue file containing CHECK_WRAPPERS).

2. **A.1 — Read queue**  
   Read `.technical/prompt-queue.jsonl` (or use pasted EAT-CACHE payload). If missing/unreadable, treat as empty; optionally append to Watcher-Result; exit.

3. **A.2 — Parse and validate**  
   Require `mode` (string). Filter out `queue_failed === true` / "queue-failed" tags. If zero valid entries, exit. Fast-path: if valid entry count === 1, skip dedup/order and go to A.5.

4. **A.3 — Dedup**  
   Same (mode, prompt, source_file) → keep first by timestamp. Do not drop same source_file with different modes. Optional: when `auto_cleanup_after_process`, after **A.7** run **queue-cleanup** skill.

5. **A.4 — Ordering**  
   CHECK_WRAPPERS meta-entries first, then canonical pipeline order per [Queue-Sources](../../Queue-Sources.md) (INGEST MODE → FORCE-WRAPPER → … → RESUME-ROADMAP → … → DISTILL → EXPRESS → ARCHIVE → … → CURATE-CLUSTER).

6. **A.5 — Dispatch (with pre-dispatch checks)**  
   For each entry: CHECK_WRAPPERS no-op; verify source_file exists if non-empty; validate mode and merged params. **A.4z — Effective pipeline profile:** merge **`effective_pipeline_mode`** and **`effective_profile_snapshot`** into roadmap and research **`Task`** hand-offs (`layer1_resolver_hints` / `## effective_pipeline_profile`). **Nested attestation (b0), post–little-val (b1), A.5b–A.5h** (tiered outcome, follow-ups, PromptCraft, continuation, gate record, audit, nightly ledger) live under **A.5** in `queue.mdc`. **Post–little-val (b1):** roadmap-class entries may **profile-skip** Layer 1 hostile validator per `l1_post_lv_policy` unless **`validator_context.force_layer1_post_lv`**; see [[3-Resources/Second-Brain/Docs/Pipeline-Validator-Profiles|Pipeline-Validator-Profiles]] and `.cursor/rules/agents/queue.mdc` **A.5 (b1)**. **Normalize aliases:** RECAL-ROAD, REVERT-PHASE, SYNC-PHASE-OUTPUTS, HANDOFF-AUDIT, RESUME-FROM-LAST-SAFE, EXPAND-ROAD → set `mode: "RESUME_ROADMAP"` and merge `params.action` (and phase/userText as needed). **RESUME-ROADMAP:** approved roadmap-next-step wrapper → resolve approved_option to params.action; context-tracking default-on; bootstrap (if no roadmap-state.md, dispatch ROADMAP MODE same project from queue first if present). **Match mode to pipeline:** delegate to `.cursor/agents/<name>.md` (or legacy-agents) per Subagent-Safety-Contract. Guidance-aware: feedback-incorporate when prompt or user_guidance present; pass guidance_text and hard_target_path. Process one entry fully before the next.

7. **A.5i — Layer 2 return harness validation**  
   After **A.5 (b0)**–**(b1)** / **A.5b** for a pipeline **Task** disposition, **before** primary **Watcher-Result** **(c)**: parse return for **`nested_subagent_ledger`**, **`blocked_scope`** (required on hard-block path), attestation; honor **`queue.harness_validation_mode`** (`advisory` \| `strict`). For decision-writing outputs, also parse decision completeness signals (`decision_option_class`, `decision_rationale_present`, `decision_linkages_present`, `decision_world_impact_required`, `decision_world_impact_present`, `decision_hygiene`) and keep them parse-safe in `trace`. See [[3-Resources/Second-Brain/Docs/Harness-Patterns-and-Guidelines|Harness-Patterns-and-Guidelines]] §4 and `queue.mdc` **A.5i**.

8. **A.6 — Log**  
   Append one line per processed request to `3-Resources/Watcher-Result.md`: `requestId: <id> | status: success|failure | message: "..." | trace: "..." | completed: <ISO8601>` (ledger / harness tags per `queue.mdc` **A.6**).

9. **A.7 — Clear passed entries only**  
   Build processed_success_ids from entries that completed with status success. **Re-read** `.technical/prompt-queue.jsonl`. Omit lines whose id is in processed_success_ids; keep all other lines (including pipeline-appended). Add failed/skipped entries with `queue_failed: true`. If approved_wrappers_remaining, append one CHECK_WRAPPERS entry. Write merged content back.

10. **A.7a — GitForge (optional)**  
    One **`Task(gitforge)`** after successful **A.7** when Config gates pass (`queue.mdc` **A.7a**).

---

## Task-queue flow (Part B)

- **B.1** — Read `3-Resources/Task-Queue.md`; parse JSON lines; require `mode`.
- **B.2** — Dispatch by mode (TASK-ROADMAP, TASK-COMPLETE, ADD-ROADMAP-ITEM, EXPAND-ROAD, REORDER-ROADMAP, etc.) to the corresponding skills (roadmap-ingest, task-complete-validate, add-roadmap-append, expand-road-assist, etc.).
- **B.3** — Append one line per processed entry to Watcher-Result; update `3-Resources/Mobile-Pending-Actions.md`.
- **B.4** — Optional banner cleanup on affected notes.
- **B.5** — Optional clear processed entries from Task-Queue.md.

---

## Safety

- Step 0 always runs first so approved wrappers are never stuck. Missing queue file or zero valid entries → exit after Step 0. Missing source_file or unknown mode → skip entry, log failure, continue. All destructive work is in downstream pipelines/skills; the Queue rule only orchestrates (read, validate, order, dispatch, log, clear/tag).

---

## References

- [Harness-Patterns-and-Guidelines](../Harness-Patterns-and-Guidelines.md) — pipeline skeleton, **`blocked_scope`**, **A.5i**, **`harness_validation_mode`**
- [Pipeline-Validator-Profiles](../Pipeline-Validator-Profiles.md) — `pipeline_mode`, `effective_profile_snapshot`, L1 skip / escalation
- [Queue-Sources](../../Queue-Sources.md) — canonical order, validation, RESUME-ROADMAP append, remove-stale
- [Rules/Dispatcher-Rule](../Rules/Dispatcher-Rule.md)
- [User-Flows/EAT-QUEUE-Flow](../User-Flows/EAT-QUEUE-Flow.md)
- `.cursor/rules/agents/queue.mdc`, `.cursor/rules/context/auto-eat-queue.mdc`
