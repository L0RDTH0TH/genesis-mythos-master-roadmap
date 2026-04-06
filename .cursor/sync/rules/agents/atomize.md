# AtomizeSubagent (context rule)

- **Subagent**: AtomizeSubagent. Autonomous-atomize (obsidian_split_atomic + split-link-preserve) with no moves, renames, or PARA reclassification. Shared split stage for Ingest and direct PARA runs.
- **Reference**: 3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference, 3-Resources/Second-Brain/Pipelines, 3-Resources/Second-Brain/Queue-Sources.
- **Depends on**: core-guardrails, confidence-loops, guidance-aware, mcp-obsidian-integration, watcher-result-append. **Subagent nesting**: AtomizeSubagent is a helper pipeline only; it must not orchestrate other pipelines or touch queues/Decision Wrappers and instead returns structured split results to its caller.

## How to activate

- **Manual**: “ATOMIZE MODE – safe batch autopilot”, “atomize this note”, or similar on a note under 1-Projects/, 2-Areas/, or 3-Resources/.
- **Queue**: `{"mode":"ATOMIZE_MODE","source_file":"…"}` dispatched via EAT-QUEUE / Queue-Dispatcher.

## Scope

- Includes: Ingest/ notes (when called from ingest Phase 1 post-process) and PARA notes under 1-Projects/, 2-Areas/, 3-Resources/.
- Excludes: 4-Archives/, Backups/, Templates/, Log notes, hubs, watcher-protected notes.

## Behavior (summary)

- Backup source note (create_backup).
- Optional classify_para when no upstream confidence is provided; otherwise reuse ingest_conf.
- Confidence gate:
  - ≥85% → eligible for split after snapshot.
  - 68–84% → one atomize-refine loop; proceed only if post_loop_conf ≥85%.
  - <68% → no split; propose-only.
- Snapshot (obsidian-snapshot, type "per-change") before obsidian_split_atomic when effective confidence ≥85%.
- obsidian_split_atomic on the source note → get child note paths (or discover them from folder).
- split-link-preserve: set split_from on children; update parent ## Splits section; optional split_into frontmatter, respecting its own confidence gate.
- Log and Run-Telemetry: log note path, children count, confidence; write one Run-Telemetry note when invoked from queue.

