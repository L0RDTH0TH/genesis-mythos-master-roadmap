# Where to Find (Documentation Index)

**Version: 2026-03**

Single index so the needle is always in the haystack: where to look for config, MCP, vault layout, queue, logs, backup, errors, and triggers. If it’s documented anywhere in the Second Brain, this page points you there.

---

## Operations (backup, logs, errors)

| Need | Doc |
|------|-----|
| **Backup and restore** (BACKUP_DIR, snapshots, retention, RESTORE MODE, Restore-Queue) | [Operations/Backup-and-Restore](../Operations/Backup-and-Restore.md) |
| **Logs and observability** (where each log lives, Backup-Log, Vault-Change-Monitor, rotation) | [Operations/Logs-and-Observability](../Operations/Logs-and-Observability.md) |
| **Errors and recovery** (Errors.md structure, Error Handling Protocol, recovery options) | [Operations/Errors-and-Recovery](../Operations/Errors-and-Recovery.md) |
| **Full log table, example line, Error entry structure** | [Logs](../../Logs.md) |
| **Enhanced snapshots** (include snapshot dirs in external backups; paths, tool suggestions) | [3-Resources/enhanced-snapshots.md](../../../enhanced-snapshots.md) |

---

## Config and parameters

| Need | Location |
|------|----------|
| **Second Brain config** (batch_size_for_snapshot, hub_names, prompt_defaults, crafting, etc.) | [Second-Brain-Config](../../Second-Brain-Config.md) |
| **Parameters** (confidence bands, RESUME-ROADMAP params, context-tracking, research, handoff, re_try_max_loops) | [Parameters](../../Parameters.md) |
| **MCP server config** (BACKUP_DIR, SNAPSHOT_DIR, BATCH_SNAPSHOT_DIR in env) | `~/.cursor/mcp.json` (obsidian-para-zettel-autopilot → env) |

---

## MCP and tools

| Need | Location |
|------|----------|
| **MCP tools** (obsidian_*, backup, move, classify, etc.) | [MCP-Tools](../../MCP-Tools.md) |
| **Configs** (MCP, plugins, paths) | [Configs](../../Configs.md) |

---

## Vault and layout

| Need | Location |
|------|----------|
| **Vault layout** (folder roles, roadmap state artifacts, Ingest/Decisions, Backups) | [Vault-Layout](../../Vault-Layout.md) |
| **Folder blacklist** (never use 00 Inbox, 10 Zettelkasten, 99*) | [mcp-obsidian-integration](../../../../.cursor/rules/always/mcp-obsidian-integration.mdc) § Folder blacklist |

---

## Queue and modes

| Need | Location |
|------|----------|
| **Queue sources** (mode → file, validation, RESUME-ROADMAP append, canonical order, Task-Queue) | [Queue-Sources](../../Queue-Sources.md) |
| **Queue alias table** (RECAL-ROAD, REVERT-PHASE, etc. → RESUME-ROADMAP params) | [Queue-Alias-Table](../../Queue-Alias-Table.md) |
| **Prompt queue file** | `.technical/prompt-queue.jsonl` |
| **Task queue** | `3-Resources/Task-Queue.md` |

---

## Pipelines, rules, skills

| Need | Location |
|------|----------|
| **Canonical pipeline order, skill slots, snapshot triggers, apply-from-wrapper** | [Cursor-Skill-Pipelines-Reference](../../Cursor-Skill-Pipelines-Reference.md) |
| **Trigger → pipeline** (high-level) | [Pipelines](../../Pipelines.md) |
| **Trigger → rule** (always + context) | [Rules](../../Rules.md) |
| **Skills by pipeline and slot; full skills table** | [Skills](../../Skills.md) |
| **Snapshot triggers by pipeline** | [Safety-Invariants](../Safety-Invariants.md) § Snapshot triggers |
| **Structure harness** (pipeline skeleton, `blocked_scope`, Layer 1 **A.5i**, skill `SKILL.md` harness block) | [Harness-Patterns-and-Guidelines](../Harness-Patterns-and-Guidelines.md) |

---

## Triggers and prompts

| Need | Location |
|------|----------|
| **Quick trigger cheat sheet** | [Triggers-Quick-Reference](../../Triggers-Quick-Reference.md) |
| **Question-led Prompt Crafter** (questions, param order, §1) | [User-Questions-and-Options-Reference](../../User-Questions-and-Options-Reference.md) §1 |
| **Decision Wrappers** (options A–G, §2) | [User-Questions-and-Options-Reference](../../User-Questions-and-Options-Reference.md) §2 |
| **Prompt Crafter param table** (question_order, accepts_manual_text) | [Prompt-Crafter-Param-Table](../../Prompt-Crafter-Param-Table.md) |

---

## Safety and invariants

| Need | Location |
|------|----------|
| **Safety invariants** (backups, snapshots, confidence bands, exclusions, Error Protocol, restore) | [Safety-Invariants](../Safety-Invariants.md) |
| **Core guardrails** (persona, PARA, confidence loops, MCP safety) | [Rules/Core-Guardrails](../Rules/Core-Guardrails.md) |
| **MCP integration** (backup gate, dry_run, ensure_structure, fallback table, restore-queue) | [mcp-obsidian-integration](../../../../.cursor/rules/always/mcp-obsidian-integration.mdc) |

---

## Docs folder (this tree)

| Need | Location |
|------|----------|
| **Docs entry point** | [Docs/README](../README.md) |
| **Architecture, subagents, delegation** | [Architecture](../Architecture.md), [Subagent-List](../Subagent-List.md), [Delegation-Patterns](../Delegation-Patterns.md) |
| **Pipelines** (Queue, Research, Ingest, Distill, Archive, Express, Organize, Roadmap) | [Pipelines/](../Pipelines/) |
| **User flows** (EAT-QUEUE, Decision Wrappers, Prompt Crafter, Roadmap resume, Mobile seed) | [User-Flows/](../User-Flows/) |
| **Rules overview** | [Rules/Always-Rules-Overview](../Rules/Always-Rules-Overview.md) |
| **Skills overviews** | [Skills/](../Skills/) |
