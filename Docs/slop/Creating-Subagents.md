# Creating Subagents

**Version: 2026-03 – post-subagent migration**

How to add or clone a subagent; template and conventions.

---

## When to add a subagent

Add a **new subagent** only when you introduce a **new pipeline** that owns destructive or stateful work. Otherwise:

- **Extend an existing subagent** (e.g. add a step or mode to ingest or roadmap).
- **Add a skill** under `.cursor/skills/<name>/` and call it from an existing pipeline; no new subagent.

---

## Cursor native subagent (.md)

1. Create `.cursor/agents/<name>.md`.
2. Add YAML frontmatter:
   - `name`: short identifier (e.g. `ingest`, `distill`)
   - `description`: one sentence for when to use
   - `model: inherit`
   - `background: false`
3. In the body:
   - State the **role** (e.g. "You are the ingest subagent").
   - Require **obedience to [Subagent-Safety-Contract](../Subagent-Safety-Contract.md)** (backup, snapshot, confidence bands, Error Handling Protocol, Watcher-Result).
   - Define the **flow** (numbered steps; exclusions; batch and return).
   - **Return format:** One-paragraph summary; any new Decision Wrapper path or queue entry; Success / #review-needed / failure. Append Watcher-Result line when `requestId` is provided.

---

## Queue dispatch

If the new pipeline is **dispatched from the queue**:

1. Add a row to the **dispatch table** in `.cursor/rules/agents/queue.mdc` mapping `mode` → subagent (or skill).
2. Add the new mode to the **canonical order** (and any Step 0 / wrapper logic) in queue.mdc and, where applicable, in `.cursor/rules/context/auto-eat-queue.mdc`.

---

## Legacy fallback

1. Copy or adapt `.cursor/rules/agents/_template.mdc`.
2. Put the pipeline rule in `.cursor/rules/legacy-agents/<name>.mdc`.
3. When delegation to `.cursor/agents/<name>.md` is not used, the main agent runs this rule so behavior matches (same steps, safety, return format).

---

## Register in system-funnels

1. In `.cursor/rules/always/system-funnels.mdc`: add **trigger phrases** and **queue modes** that map to this subagent.
2. If queue-driven: ensure the mode appears in **ordering** and **dispatch** in queue.mdc (and auto-eat-queue.mdc where applicable).

---

## Checklist

- [ ] **Safety contract:** Subagent and legacy rule both require [Subagent-Safety-Contract](../Subagent-Safety-Contract.md).
- [ ] **Backup/snapshot/confidence:** Destructive actions only after backup and (when confidence ≥85%) per-change snapshot; mid-band single refinement loop; low-band no destructive action.
- [ ] **Error Handling Protocol:** On failure, trace + summary, log to `3-Resources/Errors.md`, one-line ref in pipeline log, error Decision Wrapper under `Ingest/Decisions/Errors/` when appropriate.
- [ ] **Watcher-Result:** When `requestId` is present, append one line to `3-Resources/Watcher-Result.md` in the required format.
- [ ] **No shell vault ops:** No `cp`/`mv`/`rm` on the vault; all moves/renames via MCP with backup and snapshot gates (except the documented, user-invoked attachment-move skill).
