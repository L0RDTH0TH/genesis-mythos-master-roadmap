---
description: Ensures ingest triggers apply the full-autonomous-ingest pipeline
globs: "*"
alwaysApply: true
---

# always-ingest-bootstrap

When the user says **"INGEST MODE"**, **"Process Ingest"**, or **"run ingests"**, first ensure Ingest/ is processed per `ingest-processing.mdc` (non-MD + embedded normalization). After `ingest-processing.mdc` completes (non-MD + embedded normalization), proceed with **Phase 1 of full-autonomous-ingest (propose-only + Decision Wrapper, no moves/renames)** on all `Ingest/**/*.md` (excluding `Ingest/Decisions/**` and watcher/control notes) per `[3-Resources/Cursor-Skill-Pipelines-Reference](3-Resources/Cursor-Skill-Pipelines-Reference.md)`. Ensure `para-zettel-autopilot.mdc` and `mcp-obsidian-integration.mdc` apply. List Ingest notes via `obsidian_list_notes("Ingest")`; defer to the MCP rule and para-zettel-autopilot for exact steps (backup → classify_para → frontmatter-enrich → subfolder-organize → split_atomic → split-link-preserve → distill_note → distill-highlight-color → next-action-extract → task-reroute → append_to_hub → log_action → create/refresh Decision Wrapper for relocation). **Move/rename is performed later in Phase 2 apply-mode ingest runs, triggered by approved Decision Wrappers via EAT-QUEUE.**

