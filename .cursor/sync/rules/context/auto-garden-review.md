---
description: "When user says GARDEN REVIEW (or aliases) or queue mode GARDEN-REVIEW, run obsidian_garden_review and use the report to feed distill/organize batches. Dedicated context rule for deterministic dispatch."
globs: []
alwaysApply: false
---

# Auto-garden-review (context rule)

- **Purpose**: When the user triggers **GARDEN REVIEW** (or aliases) or when EAT-QUEUE dispatches **mode: GARDEN-REVIEW**, run the Garden review flow: call **`obsidian_garden_review`**, then use the report to feed autonomous-distill and/or autonomous-organize batches. This rule gives **deterministic dispatch** (context rule + queue alias).
- **Reference**: See [Cursor-Skill-Pipelines-Reference](3-Resources/Cursor-Skill-Pipelines-Reference.md) and [Pipelines](3-Resources/Second-Brain/Pipelines.md). MCP safety: obey [mcp-obsidian-integration](.cursor/rules/always/mcp-obsidian-integration.mdc).

## How to activate

- **Trigger phrases** (case-insensitive): **GARDEN REVIEW**, **run garden review**, **orphans and distill candidates**, **garden health**, **vault orphans**, **distill candidates sweep**.
- **Queue**: Append an entry with **`mode: "GARDEN-REVIEW"`** to `.technical/prompt-queue.jsonl` (e.g. from Watcher or Commander); optional **`source_file`** (scope/folder path) or **`params`** (scope, focus, output_path, auto_apply). EAT-QUEUE dispatches to this rule.

## Behavior

1. **Resolve scope and focus**: From queue entry `params` or prompt: `scope` (e.g. `"all"`, `"folder:Ingest"`, `"tag:xyz"`), `focus` (`orphans` | `distill_candidates` | `weak_links` | `all`), optional `output_path`, optional `auto_apply`. Default **`auto_apply: false`** during initial adoption.
2. **Call MCP**: **`obsidian_garden_review`**(scope, focus, output_path, auto_apply). If `source_file` is a folder path, use it as scope (e.g. `folder:1-Projects/MyProject`).
3. **Downstream**: Use the returned report to feed **autonomous-distill** and/or **autonomous-organize** batches (e.g. list of note paths from report → run distill or organize on that set). Do not auto-apply structural changes unless user has set `auto_apply: true` in params; suggest batching and log to Feedback-Log or Organize-Log.
4. **Logging**: Append a short entry to Feedback-Log.md or Organize-Log.md (scope, focus, report path if output_path set, batch suggestions).

## Observability

- Log **scope**, **focus**, **output_path** (if used), and **batch suggestions** (count of notes for distill/organize) so MOC or Dataview can aggregate Garden review runs.

## Exclusions

- No note-specific exclusions; flow is vault- or scope-level. Exclude Backups/, Templates/, and **/Log*.md from any batch list derived from the report when feeding distill/organize.
