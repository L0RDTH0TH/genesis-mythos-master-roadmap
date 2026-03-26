# Delegation Patterns

**Version: 2026-03 – post-subagent migration**

How the main agent delegates to subagents: hand-off structure and queue dispatch (subagent-only; no inline fallback).

---

## Preferred path

The main agent **delegates** to `.cursor/agents/<name>.md` using the **mandatory hand-off prompt** from [Subagent-Safety-Contract](../Subagent-Safety-Contract.md). That prompt includes:

- **Task:** Clear one-sentence goal.
- **Original request / queue entry:** Full queue JSON or user prompt excerpt.
- **Critical invariants:** Backup + per-change snapshot before destructive actions; confidence gates per Parameters; shared Error Handling Protocol; Watcher-Result one-line format with requestId; for roadmap: read roadmap-state.md and workflow_state.md first, append log row when state is mutated.
- **Relevant state files:** List of 2–5 paths (e.g. roadmap-state.md, Task-Queue.md).
- **Return format:** One-paragraph summary; any new Decision Wrapper path or queue entry; Success / #review-needed / failure.

---

## Fallback (deprecated)

**Same-run / legacy fallback** (running the pipeline from `.cursor/rules/legacy-agents/<name>.mdc` when the Task tool was unavailable) has been **removed from production**. All pipeline dispatch is via the **Task** subagent tool only. See [[4-Archives/Resources/Second-Brain-Deprecated/Queue-Same-Run-Fallback-2026-03-17]] for the archived specification.

---

## Rollback

To **disable native subagents** (e.g. for reference): rename or remove `.cursor/agents/*.md`. Pipeline dispatch still requires the **Task** subagent tool; there is no production path that runs pipelines inline. Legacy rules remain for reference. See [[4-Archives/Resources/Second-Brain-Deprecated/Queue-Same-Run-Fallback-2026-03-17]].

---

## Nested subagents as optional accelerators

- **Experimental capability**: Nested subagent calls (a pipeline subagent calling another subagent) are treated as an **optimization**, not a requirement. All critical safety and coordination logic (backups, snapshots, PARA moves, queue I/O, Watcher-Result) remain implemented in the main agent + Queue rule and in the primary pipeline subagents. As of the Research-layer migration there are exactly **three** sanctioned nested helper subagents: **Internal Repair Agent (IRA)**, **Validator**, and **Research**; all other cross-pipeline work must go through the queue + chain_request pattern.
- **Fallback behavior**:
  - If a nested subagent type is unavailable, misconfigured, or repeatedly fails, the caller **must degrade gracefully**:
    - Skip the nested call for that run; or
    - Fall back to simpler, inline reasoning inside the caller pipeline.
  - Pipelines must **not** make correctness or safety depend solely on nested agents; at worst, losing a nested helper should reduce depth/quality, not break invariants.
- **Ownership**:
  - Nested subagents never take over orchestration; they do not read/write queue files, create Decision Wrappers, or write to `Watcher-Result.md`.
  - All such responsibilities stay with the main agent / Queue rule, which already follow the Error Handling Protocol and Watcher-Result contract.

---

## Queue flow

The **Queue rule** runs in the main agent. It does not invoke a separate subagent for itself. It:

1. Step 0: always-check wrappers (enumerate Ingest/Decisions/**, apply approved, re-wrap, path-apply).
2. Read queue (prompt-queue.jsonl or Task-Queue.md).
3. Parse, validate, dedup, order.
4. For **each** queue entry: dispatch by mode by **calling the Task tool** (hand-off to the pipeline subagent). No inline execution; if the Task tool is unavailable or fails, the entry is treated as failed.
5. Append Watcher-Result line per requestId; clear passed entries.

Queue rule = orchestrator; pipeline subagents = executors per mode.

---

## What gets passed

- **To the subagent:** Queue entry (id, mode, params, source_file, prompt); requestId (usually entry `id`) for Watcher-Result; relevant state files (e.g. roadmap-state.md, workflow_state.md for roadmap).
- **From the subagent:** One-paragraph summary; any new Decision Wrapper path or queue entry; status (Success / #review-needed / failure). When requestId was provided, the subagent (or Queue on its behalf) appends one line to `3-Resources/Watcher-Result.md` in the required format.
- **Guidance-aware runs:** When the queue entry has non-empty `prompt` or the note at `source_file` has `user_guidance` (or tag `#guidance-aware`), the Queue runs **feedback-incorporate** and passes `guidance_text` and `hard_target_path` into the pipeline context. Guidance is a soft hint only; it must not override safety (backup, snapshot, confidence bands). See guidance-aware.mdc and Parameters.
