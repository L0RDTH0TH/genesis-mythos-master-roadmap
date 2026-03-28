---
description: "When a note has user highlights (e.g. <mark> without data-highlight-source), allow queue or trigger to run highlight-seed-enhance. Do not auto-run on every save; only on explicit trigger or queue (e.g. SEEDED-ENHANCE mode). Glob or frontmatter #has-user-highlights can identify candidates."
globs:
  - "1-Projects/**/*.md"
  - "2-Areas/**/*.md"
  - "3-Resources/**/*.md"
  - "Ingest/**/*.md"
  - "!4-Archives/**"
  - "!Backups/**"
  - "!**/Log*.md"
  - "!**/* Hub.md"
alwaysApply: false
---

# Mobile-seed-detect (context rule)

- **Purpose**: When a note has **user highlights** (plain `<mark>` with no `data-highlight-source`), allow the agent to run **highlight-seed-enhance** via explicit trigger or queue. Do **not** auto-run on every save; only when user says "Enhance highlights from seeds", "SEEDED-ENHANCE", or when a queue entry with mode **SEEDED-ENHANCE** targets this note (e.g. `source_file` set).
- **Reference**: [highlight-seed-enhance](.cursor/skills/highlight-seed-enhance/SKILL.md), [Queue-Sources](3-Resources/Second-Brain/Queue-Sources.md). MCP safety: [mcp-obsidian-integration](.cursor/rules/always/mcp-obsidian-integration.mdc).
- **Mobile vs laptop**: Mobile can **add content** (e.g. `<mark>`) into notes in Ingest or elsewhere. **Triggering** SEEDED-ENHANCE is a **laptop** action: user runs EAT-QUEUE with a queue that references that note, or Plan-mode CODE → DISTILL/SEEDED-ENHANCE. See [Mobile-Migration-Spec](3-Resources/Second-Brain/Mobile-Migration-Spec.md).

## How to activate

- **Trigger phrases**: "Enhance highlights from seeds", "SEEDED-ENHANCE", "run seed enhance on this note", or process a queue entry with `mode: "SEEDED-ENHANCE"` and optional `source_file`.
- **Glob / discovery**: To **find** notes that have user highlights (for batch queue or manual run), scan for notes containing `<mark` in source but without `data-highlight-source` in the same `<mark>` (or use a tag like `#has-user-highlights` if you add it in a prior pass). Do not auto-queue every such note on save; only queue when user explicitly requests "queue SEEDED-ENHANCE for notes with user highlights" or similar.

## Behavior

1. When the user (or queue) requests SEEDED-ENHANCE for a note (or current note), verify the note has at least one user `<mark>` (no `data-highlight-source`).
2. If none, skip or reply that no user seeds were found.
3. If present, run **highlight-seed-enhance** skill: treat user marks as cores, extend with AI (analogous color, optional drift), snapshot before edits, log seed count to Organize-Log or Feedback-Log.

## Observability

- Log **seed detections** (e.g. count of user marks, note path) in Organize-Log.md or Feedback-Log.md when SEEDED-ENHANCE runs. Enables MOC aggregation and testing (e.g. mobile add `<mark>`, laptop enhance).

## Exclusions

Exclude 4-Archives, Backups, Logs, Hub notes. Do not process notes with `watcher-protected: true`.
