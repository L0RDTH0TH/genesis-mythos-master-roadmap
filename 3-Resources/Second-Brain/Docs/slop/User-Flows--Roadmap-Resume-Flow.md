# Roadmap Resume Flow

**Version: 2026-03 – post-subagent migration**

Describes how RESUME-ROADMAP runs: one action per run, smart dispatch from approved roadmap-next-step wrapper, and context-tracking.

---

## Purpose

Single reference for the resume path so users and pipeline authors know how to trigger one deepen (or other action) and how the Queue and Roadmap subagent interact.

---

## Flow overview

1. **Enqueue:** User (or Crafter) appends a line to `.technical/prompt-queue.jsonl` with `mode: "RESUME-ROADMAP"`, `project_id`, optional `params` (e.g. `action: "deepen"`, `enable_research: true`). Or use aliases: RECAL-ROAD, REVERT-PHASE, SYNC-PHASE-OUTPUTS, HANDOFF-AUDIT, RESUME-FROM-LAST-SAFE, EXPAND-ROAD — Queue normalizes these to RESUME-ROADMAP with params.action (and phase/userText as needed).
2. **EAT-QUEUE:** User says **EAT-QUEUE** (or Process queue). Dispatcher loads Queue rule. Queue runs Step 0, then reads queue, parses/validates/orders. **RESUME-ROADMAP bootstrap:** If project has no roadmap-state.md, Queue may scan current queue for ROADMAP MODE same project_id and dispatch that first; on success then proceed to RESUME-ROADMAP.
3. **Pre-dispatch (Queue):** If **approved roadmap-next-step wrapper** exists (Ingest/Decisions/Roadmap-Decisions/, same project, approved, not processed), Queue resolves approved_option to params.action per User-Questions-and-Options-Reference §4, marks wrapper processed, moves wrapper to 4-Archives/Ingest-Decisions/Roadmap-Decisions/, then dispatches with merged params. **Context-tracking:** When mode RESUME-ROADMAP and (action deepen or missing or "auto"), set params.enable_context_tracking = true unless explicitly false.
4. **Dispatch:** Queue delegates to **Roadmap subagent** (or legacy roadmap rule) with task, queue entry, invariants, state files (roadmap-state.md, workflow_state.md), return format.
5. **Roadmap subagent:** Resolves project_id; reads roadmap-state.md and workflow_state.md; merges params (queue entry overrides Config). If **action missing or "auto"** and no wrapper was already applied, runs **smart dispatch**: scan for approved roadmap-next-step wrapper; else read workflow_state and roadmap-state, check if target reached (handoff or structural), decide next step or create Decision Wrapper (options A–G per §4). Validates action; branches by action (deepen, advance-phase, recal, revert-phase, sync-outputs, handoff-audit, resume-from-last-safe, expand, compact-depth). For **deepen:** optionally pre-deepen research (research-agent-run, queue INGEST/DISTILL); optionally roadmap-resume; run **roadmap-deepen** (one step; update workflow_state; append RESUME-ROADMAP to queue when queue_next !== false). **Context-tracking postcondition:** Re-read workflow_state; verify last Log row has valid Ctx Util %, Leftover %, Threshold, Est. Tokens; if tracking was true and any missing → fail run, Errors.md, Watcher-Result failure, #review-needed on roadmap-state.
6. **Return:** One-paragraph summary; any new wrapper or queue entry; Success / #review-needed / failure. Append Watcher-Result line. **Append workflow_state log row** when state was mutated (deepen/advance-phase).

---

## Key points

- **One action per run:** Each RESUME-ROADMAP queue entry triggers exactly one action (e.g. one deepen step). To run multiple steps, enqueue multiple lines or run EAT-QUEUE multiple times (each deepen can append a follow-up RESUME-ROADMAP when queue_next !== false).
- **Smart dispatch:** When action is missing or "auto", the Roadmap subagent (or Queue pre-dispatch) uses an approved roadmap-next-step wrapper if present; otherwise Roadmap decides next step or creates a Decision Wrapper.
- **Snapshot state:** Roadmap subagent snapshots roadmap-state.md (and workflow_state) before and after every update. Parse failure → abort roadmap pipeline; log Errors.md; #state-corrupt.

---

## References

- [Pipelines/Roadmap-Pipeline](../Pipelines/Roadmap-Pipeline.md)
- `.cursor/agents/roadmap.md`
- Queue-Sources (RESUME-ROADMAP params, bootstrap, context-tracking)
- User-Questions-and-Options-Reference §4 (roadmap-next-step options A–G)
