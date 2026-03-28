---
title: "Deprecated — Queue same-run dispatch fallback"
created: 2026-03-17
tags: [second-brain, deprecated, queue, subagent, mcp_task, fallback]
para-type: Resource
status: archived
source: "Production rules removed 2026-03-17; behavior archived for reference only."
links: ["[[3-Resources/Second-Brain/Docs/Subagents/Delegation-Patterns]]", "[[3-Resources/Second-Brain/Subagent-Safety-Contract]]"]
---

# Deprecated: Queue same-run dispatch fallback

**Status:** **Deprecated and removed from production.** This note preserves the former behavior for reference only. The production line no longer supports inline pipeline execution; all pipeline-mode queue entries **must** be dispatched via the **mcp_task** tool (launch explicit subagent). If mcp_task is unavailable or a call fails, the entry is treated as failed (Watcher-Result, Errors.md, entry not cleared).

---

## What was deprecated

**Same-run dispatch (fallback):** When the **mcp_task** tool was **not available** in the environment (tool not exposed, not in allowed tools, or call failed), the queue processor could still run pipeline work by executing it **in the same run** as the orchestrator instead of launching a subagent.

---

## Former behavior (archived specification)

1. **Trigger:** mcp_task was not in the allowed tools for the run, or a call to mcp_task had already failed for that queue entry.
2. **Action:**  
   - Output the **hand-off block** as the first content for this entry (same structure as Subagent-Safety-Contract: task, queue entry, invariants, state files, return format, telemetry block).  
   - Then **execute** the pipeline by following `.cursor/agents/<name>.md` or `.cursor/rules/legacy-agents/<name>.mdc` with that hand-off as the **task context** (i.e. the agent would read the hand-off and run the pipeline steps inline instead of calling mcp_task).
3. **Scope:** Applied to **queue-triggered** pipeline modes (EAT-QUEUE / Process queue / EAT-CACHE) and to **direct triggers** (e.g. user said "Resume roadmap", "INGEST MODE" without EAT-QUEUE) when the dispatcher or system-funnels said "else output hand-off then execute agents/ or legacy-agents/ with that as context".
4. **Chain modes:** For chain entries (e.g. RESUME_ROADMAP-RESEARCH), if mcp_task was not available, the chain could be run via same-run dispatch (dependencies then primary, all inline) instead of calling mcp_task for each segment.

---

## Mode → agent/legacy file (reference only)

| Mode | Agent (preferred when fallback was used) | Legacy rule |
|------|------------------------------------------|-------------|
| INGEST_MODE, FORCE_WRAPPER (ingest) | `.cursor/agents/ingest.md` | `.cursor/rules/legacy-agents/ingest.mdc` |
| ROADMAP_MODE, RESUME_ROADMAP | `.cursor/agents/roadmap.md` | `.cursor/rules/legacy-agents/roadmap.mdc` |
| DISTILL_MODE, BATCH_DISTILL | `.cursor/agents/distill.md` | `.cursor/rules/legacy-agents/distill.mdc` |
| EXPRESS_MODE, BATCH_EXPRESS | `.cursor/agents/express.md` | `.cursor/rules/legacy-agents/express.mdc` |
| ARCHIVE_MODE | `.cursor/agents/archive.md` | `.cursor/rules/legacy-agents/archive.mdc` |
| ORGANIZE_MODE | `.cursor/agents/organize.md` | `.cursor/rules/legacy-agents/organize.mdc` |
| RESEARCH_AGENT | `.cursor/agents/research.md` | `.cursor/rules/legacy-agents/research.mdc` |
| ROADMAP_HANDOFF_VALIDATE, VALIDATE | `.cursor/agents/validator.md` | `.cursor/rules/legacy-agents/validator.mdc` |

---

## Where it was referenced (before removal)

- **Dispatcher** (`.cursor/rules/always/dispatcher.mdc`): "Fallback (mcp_task unavailable)" paragraph; "Same-run only when…" in queue triggers; "Direct triggers: … output hand-off then execute agents/ or legacy-agents/"; "Rollback: … ensure dispatcher/queue flow uses `.cursor/rules/legacy-agents/` for pipeline execution."
- **Queue rule** (`.cursor/rules/agents/queue.mdc`): "Same-run dispatch (fallback only)" bullet; chain mode "only if mcp_task is not available, run the chain via same-run dispatch"; "Match mode to pipeline (… pipeline fallback)" with "When mcp_task is not used (fallback), INGEST_MODE → …".
- **Queue agent** (`.cursor/agents/queue.md`): "Same-run (output hand-off then execute …) only when mcp_task is unavailable or the call failed"; "Fallback to same-run only if …".
- **System-funnels** (`.cursor/rules/always/system-funnels.mdc`): "If mcp_task is unavailable, fall back to same-run: output hand-off then execute agents/ or legacy-agents/"; direct triggers "else output hand-off then execute by following …".
- **Delegation-Patterns** (`3-Resources/Second-Brain/Docs/Subagents/Delegation-Patterns.md`): "Fallback" section (run pipeline from legacy-agents when delegation not used); "Queue flow" fallback sentence ("If mcp_task is unavailable or fails, fall back to same-run dispatch…"); "Rollback" section.

---

## Why deprecated

All pipeline work is required to run **through the subagent** (mcp_task) so that: (1) context and ownership are clear (orchestrator vs pipeline); (2) Run-Telemetry and hand-off contract are consistently applied; (3) no mixed inline execution in the queue run. If mcp_task is unavailable or a call fails, the correct behavior is to **fail the entry** (Watcher-Result, Errors.md, do not clear) and ensure mcp_task is enabled, not to run pipelines inline.

---

## Re-enabling (not recommended)

To restore this behavior you would need to re-introduce the same-run branch in dispatcher.mdc, queue.mdc, queue.md, and system-funnels.mdc, and in Delegation-Patterns.md, using this note as the specification. Production rules and sync copies have been updated to remove all such branches; the live line is **mcp_task only**, fail entry on unavailability or call failure.
