---
description: "When user says CURATE CLUSTER (or aliases) or queue mode CURATE-CLUSTER, run obsidian_curate_cluster and analyze the report (gaps, merges, synthesis); optional split/MOC/merge. Dedicated context rule for deterministic dispatch."
globs: []
alwaysApply: false
---

# Auto-curate-cluster (context rule)

- **Purpose**: When the user triggers **CURATE CLUSTER** (or aliases) or when EAT-QUEUE dispatches **mode: CURATE-CLUSTER**, run the Curate cluster flow: call **`obsidian_curate_cluster`**, then analyze the report and optionally call obsidian_split_atomic, obsidian_generate_moc, or propose merges. This rule gives **deterministic dispatch** (context rule + queue alias).
- **Reference**: See [Cursor-Skill-Pipelines-Reference](3-Resources/Cursor-Skill-Pipelines-Reference.md) and [Pipelines](3-Resources/Second-Brain/Pipelines.md). MCP safety: obey [mcp-obsidian-integration](.cursor/rules/always/mcp-obsidian-integration.mdc).

## How to activate

- **Trigger phrases** (case-insensitive): **CURATE CLUSTER #tag**, **suggest gaps and merges**, **cluster curate #tag**, **theme gaps #tag**, **merge suggestions 3-Resources/…**.
- **Queue**: Append an entry with **`mode: "CURATE-CLUSTER"`**; optional **`params`** (query, note_list, actions) or **`prompt`**. EAT-QUEUE dispatches to this rule.

## Behavior

1. **Resolve query and actions**: From queue `params` or prompt: `query` (tag or folder), optional `note_list`, `actions` (suggest_gaps, suggest_merges, generate_synthesis). Default no auto_apply.
2. **Call MCP**: **`obsidian_curate_cluster`**(query, note_list, actions). Returns Markdown report.
3. **Analyze report**: Parse report; identify clusters, gaps, merge suggestions. Optionally call obsidian_split_atomic, obsidian_generate_moc, or surface merge proposals. Suggest **`auto_apply: false`** by default.
4. **Logging**: Append short entry to Feedback-Log.md (query, actions, follow-up proposed).

## Exclusions

No note-specific exclusions. When proposing splits or MOC, respect backup/snapshot and dry_run rules.
