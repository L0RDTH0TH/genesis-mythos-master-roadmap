---
name: context-vs-pipeline-audit
description: Compares workflow_state context metrics (Ctx Util %, tokens) with pipeline focus (Distill-Log, Express-Log); outputs delta/overlap to Audit-Context-Focus.md. Use when queue mode AUDIT-CONTEXT is dispatched (post-roadmap stability).
---

# context-vs-pipeline-audit

## When to use

- When **auto-eat-queue** dispatches **mode: AUDIT-CONTEXT** (source_file or project_id).
- Post-roadmap stability: compare what Cursor context used vs what pipelines focused on.

## Inputs

- **project_id** or **source_file**: Target project Roadmap folder (e.g. `1-Projects/<project_id>/Roadmap/`).

## Instructions

1. **Read workflow_state**: From target project `Roadmap/workflow_state.md` read last Log row: **Ctx Util %**, **Leftover %**, **Threshold**, **Est. Tokens / Window**.
2. **Read pipeline logs**: [Distill-Log](3-Resources/Distill-Log.md) and [Express-Log](3-Resources/Express-Log.md) for focus fields (lens, view, highlights, note paths) relevant to the project or time window.
3. **Compute**: Delta / overlap metric (e.g. % of topics or note paths that appear in both context and pipeline focus). Heuristic: compare note paths or keywords in workflow_state context vs log entries.
4. **Output**: Write to **Audit-Context-Focus.md** (under `3-Resources/` or project `Roadmap/`) with summary table and one-line verdict. Create file if missing.

## MCP tools

- `obsidian_read_note` — read workflow_state.md, Distill-Log, Express-Log.
- `obsidian_update_note` — write Audit-Context-Focus.md.

## Reference

- [Vault-Layout § workflow_state](3-Resources/Second-Brain/Vault-Layout.md)
- [Queue-Alias-Table § AUDIT-CONTEXT](3-Resources/Second-Brain/Queue-Alias-Table.md)
