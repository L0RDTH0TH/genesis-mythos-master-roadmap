---
title: Deprecated and Vestigial Audit
created: 2026-03-08
tags: [pkm, second-brain, audit, deprecated, vestigial]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/README]]"]
---

# Deprecated and Vestigial Audit

Reference for deprecated path names, vestigial logging, root files, and path references. Use this note to avoid reintroducing deprecated patterns.

## Folder and path blacklist

**Do not use or reference:** `00 Inbox`, `10 Zettelkasten`, `99 Attachments`, `99 Templates`. Use only canonical names: **Ingest** (not 00 Inbox), **Templates** (not 99 Templates), **5-Attachments** or **Attach** (not 99 Attachments). There is no Zettelkasten root — use PARA roots and subfolders only. See [[.cursor/rules/always/mcp-obsidian-integration|mcp-obsidian-integration]] and [[3-Resources/Second-Brain/Vault-Layout|Vault-Layout]].

## MCP tool naming

- **propose_para_paths** — correct MCP tool name (descriptor `propose_para_paths.json`). Do not use the legacy name `obsidian_propose_para_paths` in new docs or code.

## Where audits are recorded

- **Second Brain audit reports** (point-in-time; not evergreen docs): moved to **4-Archives/Resources/Second-Brain-Audits/** — [[4-Archives/Resources/Second-Brain-Audits/System-Audit-Report-2026-03-06|System-Audit-Report-2026-03-06]], Flow-Graphs-Audit, Architecture-Graphs-Audit.
- **Backups and snapshots:** [[3-Resources/Backup-Log|Backup-Log]] — snapshot paths, retention.
- **Errors and failures:** [[3-Resources/Errors|Errors]] — pipeline failures, error_type, recovery.

## Roadmap and one-shot

- **ROADMAP MODE** is multi-run only. One-shot is **deprecated**; use **ROADMAP-ONE-SHOT** only if required. See [[3-Resources/Second-Brain/Roadmap-Quality-Guide|Roadmap-Quality-Guide]].
