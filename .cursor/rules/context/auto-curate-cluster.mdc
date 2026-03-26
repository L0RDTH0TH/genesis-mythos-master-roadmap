---
description: "When user says CURATE CLUSTER (or aliases) or queue mode CURATE-CLUSTER, run obsidian_curate_cluster and analyze the report (gaps, merges, synthesis); optional split/MOC/merge. Dedicated context rule for deterministic dispatch."
globs: []
alwaysApply: false
---

# Auto-curate-cluster (context rule)

- **Purpose**: When the user triggers **CURATE CLUSTER** (or aliases) or when EAT-QUEUE dispatches **mode: CURATE-CLUSTER**, run the Curate cluster flow: call **`obsidian_curate_cluster`**, then analyze the report (gaps, merges, synthesis) and optionally call obsidian_split_atomic, obsidian_generate_moc, or propose merges. This rule gives **deterministic dispatch** (context rule + queue alias).
- **Reference**: See [Cursor-Skill-Pipelines-Reference](3-Resources/Cursor-Skill-Pipelines-Reference.md) and [Pipelines](3-Resources/Second-Brain/Pipelines.md). MCP safety: obey [mcp-obsidian-integration](.cursor/rules/always/mcp-obsidian-integration.mdc).

## How to activate

- **Trigger phrases** (case-insensitive): **CURATE CLUSTER #tag**, **suggest gaps and merges** (for 3-Resources or folder), **cluster curate #tag**, **theme gaps #tag**, **merge suggestions 3-Resources/…**.
- **Queue**: Append an entry with **`mode: "CURATE-CLUSTER"`** to `.technical/prompt-queue.jsonl`; optional **`params`** (query, note_list, actions) or **`prompt`** (e.g. tag or folder). EAT-QUEUE dispatches to this rule.

## Behavior

1. **Resolve query and actions**: From queue entry `params` or prompt: `query` (tag, e.g. `#productivity`, or folder path, e.g. `3-Resources`), optional `note_list` (JSON array of paths), `actions` (e.g. `suggest_gaps,suggest_merges,generate_synthesis`). Default **no auto_apply**; client LLM analyzes the report.
2. **Call MCP**: **`obsidian_curate_cluster`**(query, note_list, actions). Returns a Markdown report with note paths and short summaries.
3. **Analyze report**: Parse the report; identify clusters, gaps, and merge suggestions. Optionally call **obsidian_split_atomic**, **obsidian_generate_moc**, or surface merge proposals (e.g. in a callout or Feedback-Log). Suggest **`auto_apply: false`** by default during initial adoption; document in report §2 and §8 per pipeline reference.
4. **Logging**: Append a short entry to Feedback-Log.md (query, actions, report excerpt or path if saved, and any follow-up actions proposed).

## Observability

- Log **query**, **actions**, and **follow-up proposed** (split/MOC/merge counts) so MOC or Dataview can aggregate Curate cluster runs.

## Exclusions

- No note-specific exclusions; flow is query/folder-level. When proposing splits or MOC, respect backup/snapshot and dry_run rules from mcp-obsidian-integration.
