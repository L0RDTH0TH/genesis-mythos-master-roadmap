# Subagents Documentation

**Version: 2026-03 – post-subagent migration**

High-level overview and quick-start for the Second Brain subagent architecture after migration from monolithic Cursor rules to Cursor native subagents.

---

## Purpose

This folder is the single place for subagent-related docs: who runs what, how delegation works, safety invariants, pipeline steps, rules, skills, and user flows.

---

## Quick-start

| Goal | Action |
|------|--------|
| **Run a pipeline** | Say **INGEST MODE**, **DISTILL MODE**, **EXPRESS MODE**, **ARCHIVE MODE**, **ORGANIZE MODE**, or **Resume roadmap** / **ROADMAP MODE**. Main agent delegates to the matching subagent (or legacy rule). |
| **Process the queue** | Say **EAT-QUEUE** or **Process queue**. Dispatcher loads the Queue rule; it runs Step 0 (wrappers), then reads `.technical/prompt-queue.jsonl` and dispatches each entry by mode to the right subagent. |
| **Process task queue** | Say **PROCESS TASK QUEUE**. Queue rule reads `3-Resources/Task-Queue.md` and runs TASK-COMPLETE, ADD-ROADMAP-ITEM, etc. |
| **Create a new subagent** | See [Creating-Subagents](Creating-Subagents.md). Add `.cursor/agents/<name>.md` and a legacy fallback in `.cursor/rules/legacy-agents/<name>.mdc`. |

---

## What are subagents?

- **Cursor native subagents** (`.cursor/agents/*.md`): ingest, distill, express, archive, organize, roadmap, research. Each defines a pipeline; the main agent can delegate to them with a hand-off prompt.
- **Queue/Dispatcher**: Implemented as a **rule** (`.cursor/rules/agents/queue.mdc`), not a .md subagent. It runs in the main agent when you say EAT-QUEUE or PROCESS TASK QUEUE; it orchestrates Step 0, reads the queue, and dispatches by mode to pipeline subagents.
- **Legacy fallback**: `.cursor/rules/legacy-agents/*.mdc` run the same pipelines when delegation to `.cursor/agents/*.md` is not used.

---

## Document map

| Section | Contents |
|---------|----------|
| **Root** | [Architecture](Architecture.md), [Subagent-List](Subagent-List.md), [Creating-Subagents](Creating-Subagents.md), [Delegation-Patterns](Delegation-Patterns.md), [Safety-Invariants](Safety-Invariants.md), [Migration-Guide](Migration-Guide.md), [Examples](Examples.md) |
| **Pipelines/** | Per-pipeline steps: [Ingest](../Pipelines/Ingest-Pipeline.md), [Roadmap](../Pipelines/Roadmap-Pipeline.md), [Distill](../Pipelines/Distill-Pipeline.md), [Express](../Pipelines/Express-Pipeline.md), [Archive](../Pipelines/Archive-Pipeline.md), [Organize](../Pipelines/Organize-Pipeline.md) |
| **Rules/** | [Dispatcher-Rule](../Rules/Dispatcher-Rule.md), [Core-Guardrails](../Rules/Core-Guardrails.md), [Watcher-Result-Contract](../Rules/Watcher-Result-Contract.md) |
| **Skills/** | Skill domains: [Roadmap](../Skills/Roadmap-Skills-Overview.md), [Distill/Highlight](../Skills/Distill-Highlight-Skills.md), [Ingest/Organize](../Skills/Ingest-Organize-Skills-Overview.md) |
| **User-Flows/** | [EAT-QUEUE Flow](../User-Flows/EAT-QUEUE-Flow.md), [Decision-Wrapper-Flow](../User-Flows/Decision-Wrapper-Flow.md), [Roadmap-Resume-Flow](../User-Flows/Roadmap-Resume-Flow.md), [Mobile-Seed-Enhance-Flow](../User-Flows/Mobile-Seed-Enhance-Flow.md) |

---

## Trigger families

- **EAT-QUEUE / Process queue / EAT-CACHE / PROCESS TASK QUEUE** → Dispatcher → Queue rule → dispatch by mode to subagents or skills.
- **INGEST MODE, DISTILL MODE, EXPRESS MODE, ARCHIVE MODE, ORGANIZE MODE, ROADMAP MODE, Resume roadmap, RESUME-ROADMAP** → System-funnels → main agent delegates to the matching pipeline subagent (or legacy rule).
- **"We are making a prompt"** → Question-led Prompt Crafter (context rule); no subagent. Produces a queue payload; run EAT-QUEUE to execute.

**See also:** [Docs README](../README.md) (entry point); [Backbone](../../Backbone.md) (system flow and safety); [Queue-Sources](../../Queue-Sources.md) (mode → file, validation, RESUME-ROADMAP append); [Parameters](../../Parameters.md) (confidence bands, RESUME-ROADMAP params); [Vault-Layout](../../Vault-Layout.md) (folder roles, protected paths). Post-process stabilizers (variance dampeners) and low-variance post-AI steps are documented in Pipelines and Backbone; subagents obey the same confidence and snapshot rules.
