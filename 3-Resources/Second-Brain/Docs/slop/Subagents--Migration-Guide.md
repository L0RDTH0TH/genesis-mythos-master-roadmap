# Migration Guide

**Version: 2026-03 – post-subagent migration**

Before → after comparison for teams and future readers: how pipelines moved from monolithic rules to subagents.

---

## Purpose

Quick reference for what changed (and what stayed the same) when the vault migrated from context rules to Cursor native subagents plus legacy fallback.

---

## Before → After comparison

| Pipeline / area | Before | After |
|-----------------|--------|-------|
| **Ingest** | Single rule (para-zettel-autopilot / auto-ingest) | Ingest subagent (`.cursor/agents/ingest.md`) + legacy (`.cursor/rules/legacy-agents/ingest.mdc`) |
| **Distill** | auto-distill context rule | Distill subagent (`.cursor/agents/distill.md`) + legacy (`.cursor/rules/legacy-agents/distill.mdc`) |
| **Express** | auto-express context rule | Express subagent (`.cursor/agents/express.md`) + legacy (`.cursor/rules/legacy-agents/express.mdc`) |
| **Archive** | auto-archive context rule | Archive subagent (`.cursor/agents/archive.md`) + legacy (`.cursor/rules/legacy-agents/archive.mdc`) |
| **Organize** | auto-organize context rule | Organize subagent (`.cursor/agents/organize.md`) + legacy (`.cursor/rules/legacy-agents/organize.mdc`) |
| **Roadmap** | auto-roadmap / roadmap context rule | Roadmap subagent (`.cursor/agents/roadmap.md`) + legacy (`.cursor/rules/legacy-agents/roadmap.mdc`) |
| **Research** | Inline or single rule for RESEARCH-AGENT | Research subagent (queue-only) (`.cursor/agents/research.md`) + legacy (`.cursor/rules/legacy-agents/research.mdc`) |
| **Queue** | Inline in main rule set / auto-eat-queue | Queue rule (`.cursor/rules/agents/queue.mdc`) in main agent; dispatcher routes EAT-QUEUE / PROCESS TASK QUEUE here |

---

## What stayed the same

- **Pipelines:** Same behaviors (full-autonomous-ingest, autonomous-distill, autonomous-express, autonomous-archive, autonomous-organize, multi-run roadmap, RESEARCH-AGENT). Same steps, same skills, same confidence bands and safety gates.
- **Skills:** All under `.cursor/skills/`; subagents and legacy rules call the same skills.
- **Always rules:** core-guardrails, confidence-loops, mcp-obsidian-integration, watcher-result-append still apply; subagents depend on them.
- **Queue files and mode contracts:** `.technical/prompt-queue.jsonl` and `3-Resources/Task-Queue.md`; mode list and routing per Queue-Sources unchanged.
- **Safety:** Subagent-Safety-Contract aligns with existing guardrails (backup, snapshot, confidence bands, Error Handling Protocol, Watcher-Result).

---

## What changed

- **Execution context:** Pipeline execution can run in **Cursor native subagent context** (`.cursor/agents/<name>.md`) when the main agent delegates.
- **Fallback:** When delegation is not used, the same pipelines run from `.cursor/rules/legacy-agents/<name>.mdc`.
- **Hand-off contract:** Single mandatory hand-off structure (task, queue entry, invariants, state files, return format) in Subagent-Safety-Contract.
- **Dispatcher:** Queue triggers (EAT-QUEUE, Process queue, EAT-CACHE, PROCESS TASK QUEUE) are explicitly routed by the dispatcher to the Queue rule; the Queue rule then dispatches by mode to pipeline subagents.

---

## Rollback

To revert to **rule-only** execution: remove or rename `.cursor/agents/*.md`. Keep `.cursor/rules/legacy-agents/*.mdc` and queue.mdc. Dispatcher and Queue use the same mode → pipeline mapping; behavior reverts to pre-migration style.
