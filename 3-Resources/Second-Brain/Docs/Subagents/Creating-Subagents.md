# Creating Subagents

**Version: 2026-03 – post-subagent migration**

How to create or modify a subagent: template, conventions, and registration.

---

## Purpose

When you add a new pipeline or change an existing one, this doc explains where to add the subagent definition, the legacy rule, and how to register triggers and queue modes.

---

## When to add a subagent

- Add a **new subagent** when you introduce a **new pipeline** that owns destructive or stateful work.
- **Extend an existing subagent** when you add steps or modes to ingest, roadmap, distill, etc.
- **Add a skill** under `.cursor/skills/<name>/` and call it from an existing pipeline when you are not defining a new pipeline.

---

## Cursor native subagent (.md)

1. Create **`.cursor/agents/<name>.md`**.
2. YAML frontmatter:
   - `name`: short id (e.g. `ingest`, `distill`)
   - `description`: one sentence (when to use; queue mode if any)
   - `model: inherit`
   - `background: false`
3. Body:
   - State the **role** (e.g. "You are the ingest subagent").
   - Require **obedience to [Subagent-Safety-Contract](../../Subagent-Safety-Contract.md)** (backup, snapshot, confidence bands, Error Handling Protocol, Watcher-Result).
   - Define the **flow** (numbered steps; exclusions; batch and return).
   - **Return format:** One-paragraph summary; any new Decision Wrapper path or queue entry; Success / #review-needed / failure. Append Watcher-Result line when `requestId` is provided.

---

## Agent rule for Queue

If the new pipeline is **dispatched from the queue**:

1. Add a row to the **dispatch table** in `.cursor/rules/agents/queue.mdc` mapping `mode` → subagent (or skill).
2. Add the mode to the **canonical order** in queue.mdc (and in `.cursor/rules/context/auto-eat-queue.mdc` if it drives ordering).

---

## Legacy fallback

1. Copy or adapt **`.cursor/rules/agents/_template.mdc`**.
2. Save as **`.cursor/rules/legacy-agents/<name>.mdc`**.
3. When delegation to `.cursor/agents/<name>.md` is not used, the main agent runs this rule so behavior stays the same.

---

## Register in system-funnels

1. In **`.cursor/rules/always/system-funnels.mdc`**: add **trigger phrases** and the pipeline/subagent they map to; add **queue modes** that route to this subagent.
2. If queue-driven: ensure the mode is in the **ordering** and **dispatch** sections of queue.mdc (and auto-eat-queue.mdc where applicable).

---

## Harness requirements (mandatory scaffolding)

Every **new** `.cursor/agents/<name>.md` and **new** vault-mutating `.cursor/skills/<name>/SKILL.md` must follow [[3-Resources/Second-Brain/Docs/Harness-Patterns-and-Guidelines|Harness-Patterns-and-Guidelines]].

**Subagent (.md):**

| Must include | Reference |
|--------------|-----------|
| Numbered pipeline steps aligned with harness skeleton | Harness §1; [[3-Resources/Second-Brain/Docs/Safety-Invariants|Safety-Invariants]] § Snapshot triggers |
| **TodoWrite** phase todos; no Success while any phase todo `pending` / `in_progress` | [[3-Resources/Second-Brain/Docs/Subagent-Layers-Reference|Subagent-Layers-Reference]] § TodoWrite |
| Explicit gates: backup, snapshot (when ≥85%), confidence band table, Run-Telemetry | [[3-Resources/Second-Brain/Subagent-Safety-Contract|Subagent-Safety-Contract]] |
| Final return: `nested_subagent_ledger` (+ `task_harden_result` when nested **Task** used) | [[3-Resources/Second-Brain/Docs/Nested-Subagent-Ledger-Spec|Nested-Subagent-Ledger-Spec]] |
| **`blocked_scope`** fenced YAML when hard block / tiered freeze path | Harness §2.2; [[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Spec|Validator-Tiered-Blocks-Spec]] §4; [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]] repair-first |

**Skill (`SKILL.md`) that mutates the vault:** Harness subsection (`vault_mutations`, `snapshot_trigger`, …) per Harness §3.

---

## Checklist

- [ ] Subagent doc and legacy rule both require Subagent-Safety-Contract (backup, per-change snapshot, confidence bands, Error Handling Protocol, Watcher-Result).
- [ ] Destructive actions only after backup and (when confidence ≥85%) per-change snapshot.
- [ ] On failure: trace + summary, log to `3-Resources/Errors.md`, one-line ref in pipeline log; error Decision Wrapper under `Ingest/Decisions/Errors/` when appropriate.
- [ ] When `requestId` present, append one line to `3-Resources/Watcher-Result.md` in the required format.
- [ ] No shell `cp`/`mv`/`rm` on the vault; all moves/renames via MCP with backup and snapshot gates (except the documented, user-invoked attachment-move skill).
- [ ] Harness: ledger + conditional **`blocked_scope`** on returns; new skills declare Harness §3 block when touching vault notes.
