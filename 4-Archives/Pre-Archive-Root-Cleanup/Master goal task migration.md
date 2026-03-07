Master Goal v2** Building a (mostly) fully autonomous, post-capture Second Brain in Obsidian using PARA + Zettelkasten (inspired by Tiago Forte's Building a Second Brain), where:

- Capture and the ingest trigger are the only steps that are always manual.

  You capture into Ingest and you decide when to run ingest (e.g. "INGEST MODE", "Process Ingest", or by opening an Ingest note so the agent runs). A future watcher may support other automation but will not run ingest — ingest is always manually triggered.

  Once you trigger the right pipeline (INGEST, DISTILL, ARCHIVE, ORGANIZE, or EXPRESS MODE), everything runs automatically: organizing into PARA (including intelligent subfolders up to 4 levels), preprocessing Ingest (companion .md for non-markdown, embedded image normalization), atomic splitting, progressive distillation, color-coded highlighting that links and relates ideas across projects, frontmatter enrichment, hub/MOC linking, action extraction, archiving, resurface-candidate marking, and early express/output generation.

- The system is hands-off yet trustworthy:

  * High-confidence (≥85%) actions run only after a per-change snapshot; moves always use dry-run then commit.

  * Mid-confidence (72–84%) triggers a single non-destructive refinement loop (self-critique, alternate paths, re-score); the pipeline proceeds only if the loop raises confidence to ≥85% and a snapshot succeeds.

  * Lower confidence stays propose-only and is logged/flagged (#review-needed).

  * Safety is two-layer: external backup first (Option C – Zero-Manual), then in-vault per-change snapshots before each destructive step.

  * Observability: pipeline logs, loop-outcome fields, and Dataview give you a clear audit trail.

    You get maximum visual and relational clarity at a glance without tag clutter: frontmatter, Dataview tables, callouts, project-linked Highlightr colors (color theory), task lists, and graph hints.

- Highlightr colors are a visual language for idea relationships and usage within and across projects:

  * Analogous schemes → ideas that belong together or build on each other

  * Complementary contrasts → opposing views, tensions, trade-offs

  * Project-specific overrides (highlight_key) → each project can define its own relational color grammar

    Optional flows (e.g. Garden review for distill candidates, Curate cluster for gaps/merges) feed batches into these pipelines.

In short: Turn Obsidian into an external brain that ingests raw material, organizes/distills/expresses it autonomously once you trigger the right pipeline, and presents knowledge in the most scannable, relationally clear, and action-oriented way — so you spend almost no time managing notes and almost all your time thinking, creating, and acting on what matters. Copy the block above into your Master Goal note as-is or adjust wording to taste.    

## Current Goal

Migrate the master goal to include task tracking as a primary focus. We are using dev roadmaps as an example for the structure with phases and sub phases broken into task. We already have plugins we can utilize in; dataview and tasks.