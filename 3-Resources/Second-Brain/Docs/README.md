# Second Brain Subagents Documentation

**Version: 2026-03 – post-subagent migration**

> **On GitHub** ([genesis-mythos-master-roadmap](https://github.com/L0RDTH0TH/genesis-mythos-master-roadmap)): this folder is part of a **published export** that also contains the **Genesis Mythos** `Roadmap/` and project goal files. For what the *repository* is (product + automation), read the **[root `README.md`](../README.md)** first.

High-level overview and quick-start for the Second Brain vault’s Cursor native subagent architecture. Use this as the entry point; then follow links to Architecture, Pipelines, Rules, and User Flows.

---

## Purpose

This folder documents the **post-migration** system: Cursor’s native subagents (`.cursor/agents/*.md`) plus the Queue/Dispatcher rule (`.cursor/rules/agents/queue.mdc`). Pipelines (ingest, roadmap, distill, express, archive, organize, research) run either as delegated subagents or via legacy rules in `.cursor/rules/legacy-agents/`.

**Canonical location:** All documentation lives in this folder (`Docs/`). Subagent-specific docs (architecture, list, creating, delegation, safety, migration, examples) live in **`Docs/Subagents/`**; pipelines, rules, skills, and user flows live at `Docs/Pipelines/`, `Docs/Rules/`, `Docs/Skills/`, `Docs/User-Flows/`. No documentation should be created outside `Docs/`.

---

## Quick start

1. **Run a pipeline once**  
   Say **INGEST MODE**, **DISTILL MODE**, **Resume roadmap**, etc. The main agent routes via system-funnels and delegates to the matching subagent (or legacy rule).

2. **Process the queue**  
   Say **EAT-QUEUE** or **Process queue**. The Dispatcher loads the Queue rule → Step 0 (wrappers) → read `.technical/prompt-queue.jsonl` → validate, order, dispatch by mode → one line per entry to `Watcher-Result.md`.

3. **Craft a queue entry (preferred)**  
   Say **We are making a prompt** (or CODE/ROADMAP variant). The question-led Prompt-Crafter runs; after Q&A it appends one JSONL line to the queue only after you confirm. Then run **EAT-QUEUE** to execute.

---

## Document map

| Document | Purpose |
|----------|---------|
| [GitHub-Export-Repository-README](GitHub-Export-Repository-README.md) | Source for **root `README.md`** on [genesis-mythos-master-roadmap](https://github.com/L0RDTH0TH/genesis-mythos-master-roadmap) (product + repo layout + branches); copied during vault → export sync |
| [Architecture](Architecture.md) | Delegation flow, Mermaid diagram, Queue vs direct triggers |
| [Subagent-List](Subagent-List.md) | Table: name, description, responsibilities, triggers |
| [Creating-Subagents](Subagents/Creating-Subagents.md) | How to add or change a subagent; template, **Harness requirements**, conventions ([stub](Creating-Subagents.md) for legacy path) |
| [Delegation-Patterns](Delegation-Patterns.md) | Hand-off structure, fallback, queue dispatch |
| [Safety-Invariants](Safety-Invariants.md) | Backups, snapshots, confidence bands, Watcher, Errors |
| [Subagent-Layers-Reference](Subagent-Layers-Reference.md) | Indexed layer model (L0–L2), helper family, conditional obligation, TodoWrite |
| [Harness-Patterns-and-Guidelines](Harness-Patterns-and-Guidelines.md) | Pipeline skeleton, return contract (`nested_subagent_ledger`, `blocked_scope`), skill harness, queue **A.5i** telemetry |
| [Prompt-Craft-Subagent](Prompt-Craft-Subagent.md) | Machine recovery queue crafting (`Task(prompt_craft)`); not the question-led crafter |
| [Entire-System-Reference](Entire-System-Reference.md) | Full-system canonical contract: funnels, queues, CODE PARA, roadmap, safety, observability |
| [CODE-PARA-System](CODE-PARA-System.md) | Canonical CODE lane: PARA mapping, queue routing, safety gates |
| [Roadmapping-System](Roadmapping-System.md) | Canonical roadmap lane: setup/resume, dual-track, state authority |
| [Queue-Continuation-Spec](Queue-Continuation-Spec.md) | Machine-readable `queue_continuation` + `queue-continuation.jsonl`; empty-queue bootstrap (config-gated) |
| [Conceptual-Autopilot-Verification-Checklist](Conceptual-Autopilot-Verification-Checklist.md) | Manual EAT-QUEUE checks for conceptual **`effective_track`** autopilot + **`conceptual_target_reached`** |
| [Migration-Guide](Migration-Guide.md) | Before → after: monolithic rules to subagents |
| [Examples](Examples.md) | Concrete usage: INGEST, RESUME-ROADMAP, DISTILL LENS, EAT-QUEUE |
| [Pipelines/Queue-Pipeline](Pipelines/Queue-Pipeline.md) | Step 0, two queues, dispatch, Watcher-Result, clear/tag |
| [Pipelines/Research-Pipeline](Pipelines/Research-Pipeline.md) | RESEARCH-AGENT queue-only flow, project_id + linked_phase, research-agent-run |
| [User-Flows/EAT-QUEUE-Flow](User-Flows/EAT-QUEUE-Flow.md) | EAT-QUEUE user journey: Step 0 → read → dispatch → Watcher-Result |
| [Rules/Always-Rules-Overview](Rules/Always-Rules-Overview.md) | Index of all always rules (and context entry points) with one-line purpose |
| [Skills/Queue-and-Shared-Skills](Skills/Queue-and-Shared-Skills.md) | Step 0 skills, queue-cleanup, obsidian-snapshot, task/roadmap queue skills |
| [Operations/Backup-and-Restore](Operations/Backup-and-Restore.md) | Backups, snapshots, retention, RESTORE MODE, Restore-Queue — single reference |
| [Operations/Logs-and-Observability](Operations/Logs-and-Observability.md) | Where logs live, Backup-Log, Errors, Vault-Change-Monitor, rotation |
| [Operations/Errors-and-Recovery](Operations/Errors-and-Recovery.md) | Error Handling Protocol, Errors.md structure, recovery options |
| [Reference/Where-to-Find](Reference/Where-to-Find.md) | Index: config, MCP, vault, queue, logs, backup, errors, triggers — find any doc |

### By topic

| Topic | Where to look |
|-------|----------------|
| Pipelines (steps, skills, confidence) | [Pipelines/](Pipelines/) — includes **Queue** and **Research** |
| Always-on rules (dispatcher, guardrails, Watcher, system-funnels, confidence-loops) | [Rules/](Rules/) — see **Always-Rules-Overview** for full list |
| Skills (roadmap, distill, ingest, queue/Step 0, shared) | [Skills/](Skills/) — see **Queue-and-Shared-Skills** for queue and cross-cutting |
| User flows (EAT-QUEUE, Decision Wrappers, roadmap resume, **Prompt Crafter**) | [User-Flows/](User-Flows/) |
| CODE automation model (PARA + queue + guardrails) | [CODE-PARA-System](CODE-PARA-System.md) |
| Roadmap automation model (setup/resume + dual track) | [Roadmapping-System](Roadmapping-System.md) |
| Full-system canonical model (all lanes + orchestration + safety) | [Entire-System-Reference](Entire-System-Reference.md) |
| **Backup and restore** (BACKUP_DIR, snapshots, retention, restore) | [Operations/Backup-and-Restore](Operations/Backup-and-Restore.md) |
| **Logs and observability** (log locations, Backup-Log, rotation) | [Operations/Logs-and-Observability](Operations/Logs-and-Observability.md) |
| **Errors and recovery** (Error Protocol, Errors.md, recovery) | [Operations/Errors-and-Recovery](Operations/Errors-and-Recovery.md) |
| **Where to find anything** (config, MCP, queue, triggers, full index) | [Reference/Where-to-Find](Reference/Where-to-Find.md) |

---

## Key concepts

- **Main agent** loads core guardrails (persona, PARA, safety). For queue triggers it runs the **Dispatcher** → **Queue rule** → dispatch by mode. For direct triggers it follows **System Funnels** and delegates to the right pipeline subagent.
- **Hand-off contract:** Delegation uses the mandatory hand-off prompt from [Subagent-Safety-Contract](../Subagent-Safety-Contract.md).
- **Two queues:** `.technical/prompt-queue.jsonl` (pipeline modes); `3-Resources/Task-Queue.md` (task/roadmap modes). Queue writes are laptop-only; mobile = observe + fill Ingest.

---

## See also

- [Second Brain README](../README.md) — backbone index, trigger cheat sheet, full documentation index
- [Backbone](../Backbone.md) — system flow, safety, multi-run roadmap, links to all backbone docs
- [Rules](../Rules.md) — always and context rules map; trigger → rule
- [Pipelines](../Pipelines.md) — trigger → pipeline, flows, safety
- [Skills](../Skills.md) — skills by pipeline and slot; full skills table
- [Logs](../Logs.md) — pipeline logs, Errors.md, observability
- [Queue-Sources](../Queue-Sources.md) — mode → file, validation, RESUME-ROADMAP append, canonical order
- [Parameters](../Parameters.md) — confidence bands, RESUME-ROADMAP params, context-tracking, research params, handoff, re_try_max_loops
- [Vault-Layout](../Vault-Layout.md) — folder roles, roadmap state artifacts, Ingest/Decisions subfolders
- [User-Questions-and-Options-Reference](../User-Questions-and-Options-Reference.md) — question-led crafter §1, Decision Wrappers §2, options A–G
- [Cursor-Skill-Pipelines-Reference](../Cursor-Skill-Pipelines-Reference.md) — canonical pipeline order, skill slots, snapshot triggers table, apply-from-wrapper table
- [Triggers-Quick-Reference](../Triggers-Quick-Reference.md) — quick trigger cheat sheet, log format
