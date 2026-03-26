# Dispatcher Rule

**Version: 2026-03 – post-subagent migration**

Summarizes the always-on dispatcher rule that routes queue-related triggers to the Queue/Dispatcher subagent.

---

## Purpose

Quick reference for what the dispatcher does and which triggers it handles. Full rule: `.cursor/rules/always/dispatcher.mdc`.

---

## Role

- **Recognize** queue-related triggers and route them to the **Queue/Dispatcher subagent** (`.cursor/rules/agents/queue.mdc`).
- **All other triggers** (INGEST MODE, DISTILL MODE, EXPRESS MODE, ARCHIVE MODE, ORGANIZE MODE, roadmap modes, GARDEN REVIEW, CURATE CLUSTER, etc.) continue to map to their context rules per **system-funnels.mdc** (no change).

---

## Queue triggers → Queue rule

When the user instruction contains any of these (case-insensitive):

- **EAT-QUEUE** *(canonical)*
- **Process queue**
- **EAT-CACHE** / **eat cache**
- **PROCESS TASK QUEUE**

then:

1. **Load and follow** the **Queue/Dispatcher subagent**: `.cursor/rules/agents/queue.mdc`.
2. That rule is responsible for:
   - **EAT-QUEUE / Process queue / EAT-CACHE:** Step 0 (always-check wrappers), read `.technical/prompt-queue.jsonl` (or pasted EAT-CACHE payload), parse/validate/dedup/order, dispatch by mode, Watcher-Result, clear passed / tag failed.
   - **PROCESS TASK QUEUE:** Read `3-Resources/Task-Queue.md`, dispatch by mode (TASK-ROADMAP, TASK-COMPLETE, ADD-ROADMAP-ITEM, etc.), Watcher-Result, Mobile-Pending-Actions.
3. Do **not** run queue or task-queue logic in the current rule set; run it only inside the Queue rule flow.

---

## Delegation and fallback

- **Real subagents:** Pipeline execution (ingest, roadmap, distill, express, archive, organize, research) MAY be delegated to `.cursor/agents/<name>.md` using the mandatory hand-off template from Subagent-Safety-Contract.
- **Fallback:** When not delegating, run the pipeline from `.cursor/rules/legacy-agents/<name>.mdc`.
- **Rollback:** To revert to rule-based mode only, comment out or rename `.cursor/agents/*.md` so Cursor stops using them; ensure dispatcher/queue flow uses legacy-agents/ for pipeline execution.
