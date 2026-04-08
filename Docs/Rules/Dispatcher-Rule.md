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

- **EAT-QUEUE** *(canonical)* — includes **EAT-QUEUE BREAK-SPIN** (same pass; optional **`## operator_break_spin`** YAML in the hand-off per [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]])
- **Process queue**
- **EAT-CACHE** / **eat cache**
- **PROCESS TASK QUEUE**

then:

1. **Delegate to the Queue subagent** via the Cursor **`Task`** tool with the hand-off from **dispatcher.mdc** (vault root, queue paths, optional **`## operator_break_spin`** YAML for **BREAK-SPIN**).
2. **The Queue subagent** (`.cursor/rules/agents/queue.mdc`) is responsible for:
   - **EAT-QUEUE / Process queue / EAT-CACHE:** Step 0 (always-check wrappers), read `.technical/prompt-queue.jsonl` (or pasted EAT-CACHE payload), parse/validate/dedup/order, dispatch by mode, Watcher-Result, clear passed / tag failed.
   - **PROCESS TASK QUEUE:** Read `3-Resources/Task-Queue.md`, dispatch by mode (TASK_ROADMAP, TASK-COMPLETE, ADD-ROADMAP-ITEM, etc.), Watcher-Result, Mobile-Pending-Actions.
3. **After `Task(queue)` returns (Layer 0 only):** optional **loud wrap** when **`queue.layer0_escalation_enabled`** — parse **`## layer0_queue_signals`** in the Queue return ([[.cursor/agents/queue.md|agents/queue.md]]); **never** put loud copy in **Watcher-Result** (see **dispatcher.mdc**).
4. Do **not** run queue or task-queue logic in the parent agent; run it only inside the Queue subagent flow.

---

## Cursor Task tool: `model` parameter

- **Omit** `model` on Task calls to inherit the parent session’s model (default / auto).
- Use **`model: "fast"`** only when intentionally selecting the fast subagent tier.
- **Never** pass **`model: "inherit"`** — that string is not a valid Task API value and fails schema validation.
- **Validator** (and similar) dispatches pass the explicit `model` from Second-Brain-Config as documented elsewhere.
- **Not the same as** `.cursor/agents/*.md` YAML frontmatter `model: inherit` (agent file convention only).

Canonical detail: [[3-Resources/Second-Brain/Subagent-Safety-Contract|Subagent-Safety-Contract]] § Cursor Task tool: `model` parameter.

---

## Delegation and fallback

- **Task-only dispatch:** Pipeline execution is delegated via the Cursor **`Task`** tool and **Subagent-Safety-Contract** hand-offs. There is **no** same-run inline pipeline execution and **no** production fallback to `.cursor/rules/legacy-agents/` (legacy rules are reference-only). On `Task` failure, use **Proof-on-failure** ([[3-Resources/Second-Brain/Subagent-Safety-Contract|Subagent-Safety-Contract]] § Proof-on-failure): Task-Handoff-Comms `return_in` when enabled, Errors.md, Watcher-Result; do not clear queue entries as success. **Parallel lanes:** resolved **PQ** and **task-handoff-comms** path per [[.cursor/rules/agents/queue.mdc|queue.mdc]] **A.0x** / **parallel_context** — see full rule [.cursor/rules/always/dispatcher.mdc](.cursor/rules/always/dispatcher.mdc).
