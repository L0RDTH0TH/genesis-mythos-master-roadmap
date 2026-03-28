# Delegation Patterns

**Version: 2026-03 – post-subagent migration**

How the main agent delegates: natural language triggers, slash commands, and queue dispatch.

---

## Purpose

Single reference for preferred path (hand-off to native subagent), fallback (legacy rule), rollback, and what gets passed to/from subagents.

---

## Preferred path

The main agent **delegates** to `.cursor/agents/<name>.md` using the **mandatory hand-off prompt** from [Subagent-Safety-Contract](../../Subagent-Safety-Contract.md):

- **Task:** Clear one-sentence goal.
- **Original request / queue entry:** Full queue JSON or user prompt excerpt.
- **Critical invariants:** Backup + per-change snapshot before destructive actions; confidence gates per Parameters; Error Handling Protocol; Watcher-Result one-line format with requestId; for roadmap: read roadmap-state.md and workflow_state.md first, append log row when state mutated.
- **Relevant state files:** List of 2–5 paths (e.g. roadmap-state.md, Task-Queue.md).
- **Return format:** One-paragraph summary; any new Decision Wrapper path or queue entry; Success / #review-needed / failure.

---

## Fallback (deprecated)

**Same-run fallback** (run pipeline from `.cursor/agents/<name>.md` or `.cursor/rules/legacy-agents/<name>.mdc` when the Task tool was unavailable) has been **removed from production**. All pipeline dispatch is via the **Task** subagent tool only; on failure, the entry is treated as failed. For the archived specification, see [[4-Archives/Resources/Second-Brain-Deprecated/Queue-Same-Run-Fallback-2026-03-17]].

---

## Rollback

To **disable native subagents** (e.g. for tooling reference): rename or remove `.cursor/agents/*.md`. Pipeline dispatch still requires the **Task** subagent tool; there is no production path that runs pipelines inline from legacy-agents. Legacy rules remain for reference only. See [[4-Archives/Resources/Second-Brain-Deprecated/Queue-Same-Run-Fallback-2026-03-17]] for deprecated behavior.

---

## Queue flow

The **Queue rule** runs in the main agent. It runs Step 0 (wrappers), reads the queue, parses/validates/orders, then for **each** entry **dispatches** by mode. For **pipeline modes** (ingest, roadmap, distill, express, archive, organize, research, validator), dispatch is **only via the Task subagent tool**: (1) Build the complete hand-off block per Subagent-Safety-Contract (task, queue entry, invariants, state files, return format). (2) **Call the Task tool** with **prompt** = that hand-off block and **subagent_type** = the pipeline type. The subagent runs in a **separate context** with only that prompt; the queue processor does not run pipeline steps itself. (3) When the Task call returns, the queue processor logs Watcher-Result and continues. If the Task tool is unavailable or a call fails, the entry is **treated as failed** (Watcher-Result, Errors.md, entry not cleared). *(Deprecated same-run fallback: [[4-Archives/Resources/Second-Brain-Deprecated/Queue-Same-Run-Fallback-2026-03-17]].)*

---

## What gets passed

- **To subagent:** Queue entry (id, mode, params, source_file, prompt); requestId (usually entry `id`) for Watcher-Result; relevant state files (e.g. roadmap-state.md, workflow_state.md for roadmap).
- **From subagent:** One-paragraph summary; any new Decision Wrapper path or queue entry; status (Success / #review-needed / failure). When requestId was provided, append one line to `3-Resources/Watcher-Result.md` in the required format.

<!-- Gap filled from old Cursor-Skill-Pipelines-Reference.md / guidance-aware.mdc -->
- **Guidance-aware runs:** When the queue entry has non-empty `prompt` or the note at `source_file` has `user_guidance` frontmatter (or tag `#guidance-aware`), the Queue runs **feedback-incorporate** and passes **guidance_text** and **hard_target_path** into the pipeline context. Guidance is a soft hint only; it must not override safety (backup, snapshot, confidence bands). Merge **agent_reasoning** (AI-only snippets from crafter C choices) as a separate block; do not treat it as human input. See guidance-aware.mdc and Parameters (user_guidance, guidance_conf_boost).
