---
name: Second-Brain docs complete coverage
overview: Update all 14 Second-Brain docs with responsibility bullets, usage examples, refreshed Mermaid diagrams, and any missing cross-links so the documentation has complete coverage and is easy to use.
todos: []
isProject: false
---

# Second-Brain Documentation — Complete Coverage Plan

## Scope

- **Location**: [3-Resources/Second-Brain/](3-Resources/Second-Brain/) (14 notes) plus [3-Resources/Cursor-Skill-Pipelines-Reference.md](3-Resources/Cursor-Skill-Pipelines-Reference.md) where it backs Pipelines/Logs.
- **Sync**: Per [backbone-docs-sync](.cursor/rules/always/backbone-docs-sync.mdc), doc-only changes do not require updating `.cursor/sync/`; only rule/skill file changes do. This plan is documentation-only unless you later add or change rules/skills.

---

## 1. README.md

- **Index**: Already links all 14 docs; keep as-is.
- **Mermaid sentence**: Update "Mermaid diagrams live in Backbone, Pipelines, Queue-Sources, Parameters, and optionally Vault-Layout" to state that **Backbone, Rules, Skills, Pipelines, MCP-Tools, Configs, Logs, Vault-Layout, Queue-Sources, Parameters, Templates, Plugins** contain Mermaid where applicable.
- **Add**: Short "How to use this documentation" (2–3 bullets): start at Backbone for system flow; use Rules/Pipelines for triggers; use Skills/MCP-Tools for step-by-step; use Logs/Parameters for observability and tuning.
- **Add**: "Mental model in 60 seconds" (after "How to use"): 1–2 sentences + optional tiny Mermaid — e.g. "New stuff → Ingest/ → INGEST MODE → classify → enrich → distill → organize → hub/link → PARA. Maintenance → open note → DISTILL / HIGHLIGHT / ARCHIVE MODE → EAT-QUEUE." Prose-only is fine if avoiding another diagram.
- **Add**: "Usage at a glance" subsection with one-line usage examples per pipeline (e.g. "**Ingest**: Put file in Ingest/, say **INGEST MODE** or **Process Ingest**.") and pointer to Queue-Sources for queue modes.
- **Add**: "Trigger cheat sheet" — compact 4–6 row table: | Spoken / UI trigger | What actually happens | Typical use-case | (e.g. INGEST MODE → full-autonomous-ingest on Ingest/ → New files dropped; DISTILL MODE → BATCH-DISTILL on open/current folder or selection → Improve existing notes; ARCHIVE MODE → archive-check + move completed notes → Cleanup; EAT-QUEUE → Process next prompt-queue entry → Continue after review/proposal). Makes usage-at-a-glance scannable. Can live in README (visible) with "see Pipelines.md for full trigger table."
- **Add**: "Troubleshooting common failure modes" subsection (very visible): 3–6 concise bullets, e.g. "Note stays in Ingest/ forever → check Watcher-Result, confidence <72%, queue not eaten"; "No frontmatter / missing para-type → always-core rule failed or classify_para skipped"; "Colors not applying → Highlightr disabled, wrong highlight_key, or distill-highlight-color not run"; "Move fails with parent missing → ensure_structure not called (fallback in mcp-obsidian-integration)." Optionally cross-link to Logs.md (error entry format) and Backbone (safety flow).
- **Add**: "Key invariants / safety guarantees" — either a short block here (2–4 bullets) or a single line pointing to Backbone: "See [[Backbone#Key invariants]] for the system's safety promises." Prefer canonical block in Backbone (see §2); README gets one-line pointer.
- **Add (optional)**: "Changelog (doc updates)" — either a short subsection in README (e.g. "2026-03: Responsibility columns & usage examples across docs; trigger/tuning cheat sheets; troubleshooting") or a new **Changelog.md** in Second-Brain/ for version/change log lite (e.g. "2026-03: … ; 2026-02: SEEDED-ENHANCE pipeline"). If Changelog.md is created, add it to the Documentation index in README. Helps track evolution without git archaeology.

---

## 2. Backbone.md

- **Add**: "Key invariants / safety guarantees" block (2–4 bullets) — the one place for "the system will never…" promises. Suggested bullets: (1) Never delete notes (only move to Archives or create snapshots). (2) Never run destructive MCP operations without backup + dry-run check. (3) Never process files already in Backups/, Logs/, or snapshot dirs. (4) Always preserve original file creation time in frontmatter when possible. New users go here for the safety model.
- **Add**: "Component responsibilities" section with bullet lists:
  - **Obsidian vault**: Holds notes (PARA + CODE); all new files land in Ingest/; Backups/ append-only.
  - **Cursor rules**: Always rules apply every run; context rules fire on phrase/glob; no vault cp/mv/rm.
  - **Cursor skills**: Execute pipeline steps (enrich, move, snapshot, etc.); read Second-Brain-Config where applicable.
  - **Obsidian MCP server**: Provides read/update/move/classify/distill/backup tools; backup gate before destructive ops.
  - **Watcher**: Writes Watcher-Signal; reads Watcher-Result; can append to prompt-queue.
  - **Commander**: Surfaces triggers in UI; logs commander_source/commander_macro.
- **Links**: Already links to all backbone docs; add explicit link to Cursor-Skill-Pipelines-Reference (canonical pipeline order and snapshot triggers).
- **Diagrams**: Keep existing three (system flow, safety flow, PARA/CODE); no change unless you add a fourth for "component responsibilities" (optional).
- **Optional**: "Troubleshooting" — if not fully covered in README, add 1–2 bullets here that point to Error Handling Protocol and fallbacks (ensure_structure, dry_run); otherwise README is the single visible place.

---

## 3. Rules.md

- **Always-applied table**: Add a "Responsibilities" column (or a short bullet list below the table): one bullet per rule (e.g. "00-always-core: Persona, Ingest-first, frontmatter on every new .md").
- **Context table**: Add responsibility bullets per row (e.g. "auto-distill: Runs autonomous-distill; backup/snapshot before structural edits; excludes Backups/Logs/Hubs").
- **Add**: "Usage examples" subsection: 2–3 example triggers (e.g. "Say **INGEST MODE** → always-ingest-bootstrap + para-zettel-autopilot → full-autonomous-ingest"; "Say **EAT-QUEUE** with queue populated → auto-eat-queue → dispatch by mode → Watcher-Result").
- **Mermaid**: Keep existing two diagrams; ensure they match current trigger → pipeline list (including SEEDED-ENHANCE, BATCH-DISTILL, etc. if present in auto-eat-queue).

---

## 4. Skills.md

- **Skills table**: Add a "Responsibilities" column: one line per skill (e.g. "frontmatter-enrich: Set status, para-type, created, links from classification; optional project-id").
- **Add**: "Usage examples" subsection:
  - Example 1: "After classify_para in ingest, run **frontmatter-enrich** then **subfolder-organize** to get target path."
  - Example 2: "Before any move in archive, run **summary-preserve** so TL;DR and project colors are kept."
- **Diagrams**: Keep "Skills by pipeline" and "Ingest skill chain" and "Highlighter flow"; verify they match [Cursor-Skill-Pipelines-Reference](3-Resources/Cursor-Skill-Pipelines-Reference.md) skill order (e.g. task-reroute, express-view-layer).

---

## 5. Pipelines.md

- **Trigger table**: Ensure it includes SEEDED-ENHANCE, BATCH-DISTILL, BATCH-EXPRESS, ASYNC-LOOP if they are in auto-eat-queue; add one-line responsibility per pipeline (e.g. "full-autonomous-ingest: Capture → classify → organize → distill → hub → move"). Add line: "For a compact trigger cheat sheet (spoken trigger → what happens → use-case), see README § Trigger cheat sheet."
- **Add**: "Snapshot triggers summary" subsection: copy or summarize the [Snapshot triggers (all pipelines)](3-Resources/Cursor-Skill-Pipelines-Reference.md) table (per-change triggers + batch frequency per pipeline) and link to Cursor-Skill-Pipelines-Reference for full detail.
- **Add**: "Usage examples" subsection: one concrete example per main pipeline (e.g. "**Ingest**: Add `My-Note.md` to Ingest/, run INGEST MODE; note is classified, distilled, and moved to PARA." "**Distill**: Open a note in 1-Projects/…, say DISTILL MODE – safe batch autopilot." "**Archive**: Say ARCHIVE MODE – safe batch autopilot on a folder; notes with no open tasks and status complete are moved to 4-Archives/.").
- **Mermaid**: Keep existing flowcharts; add a small "Snapshot decision" diagram (confidence ≥85% → per-change snapshot → destructive step) if not redundant with Backbone safety flow.

---

## 6. MCP-Tools.md

- **Tool groups table**: Add "Responsibilities" column per group (e.g. "Core: read_note/update_note/search_replace for content; list_notes/global_search for discovery; manage_frontmatter/manage_tags for metadata").
- **Add**: "Usage examples" subsection:
  - Example 1: "Ingest sequence: create_backup → classify_para → (skills use update_note/manage_frontmatter) → subfolder_organize → split_atomic → distill_note → append_to_hub → move_note(dry_run: true) → move_note(dry_run: false) → log_action."
  - Example 2: "Move with missing parent: ensure_structure(folder_path: target_parent) → move_note(path, new_path, dry_run: true) → move_note(..., dry_run: false)."
- **Important parameters**: Keep; add one line each for ensure_backup (max_age_minutes), log_action (include backup_path in changes).
- **Mermaid**: Keep tool groups diagram; keep "Typical ingest MCP sequence."

---

## 7. Configs.md

- **Second-Brain-Config**: Add responsibility bullets (e.g. "hub_names: consumed by append_to_hub; archive: by archive-check; highlight: by distill-highlight-color and layer-promote; depths: async_preview_threshold, batch_size_for_snapshot; graph: MOC strength.").
- **MCP env**: Add one responsibility line per variable (e.g. "BACKUP_DIR: create_backup/ensure_backup write here; required for destructive tools.").
- **Add**: "Example config snippet" (optional): one YAML block for Second-Brain-Config with hub_names, archive age_days, highlight default_key, and batch_size_for_snapshot.
- **Mermaid**: Keep "Config sources and consumers"; ensure Backup and Snap consumers are shown.

---

## 8. Logs.md

- **Pipeline logs table**: Add "Responsibilities" column (e.g. "Ingest-Log: One line per note processed by full-autonomous-ingest; must include backup_path and snapshot path when applicable.").
- **Add**: "Example log line" subsection: one full example following the format from Cursor-Skill-Pipelines-Reference (timestamp | Excerpt | PARA | Changes; include Backup: path | Confidence | Proposed MV | Flag | Loop fields).
- **Add**: Cross-link to "Snapshot triggers" in Pipelines.md or Cursor-Skill-Pipelines-Reference (when to log snapshot path).
- **Mermaid**: Keep log destinations, Error structure, log → MOC, health check flow.

---

## 9. Vault-Layout.md

- **Folder table**: Add "Responsibilities" column (e.g. "1-Projects: Time-bound work; agent moves here from Ingest when para-type=Project; subfolders ≤4 levels." "Ingest: All new/unknown files; agent processes then moves out." "Backups/Per-Change: Append-only; agent writes snapshots here; never process as input.").
- **Add**: "Usage example": "New file → place in Ingest/ → run INGEST MODE → file is classified, distilled, and moved to 1-Projects/…, 2-Areas/…, or 3-Resources/…."
- **Mermaid**: Keep folder tree and exclusions flow.

---

## 10. Queue-Sources.md

- **prompt-queue.jsonl / Task-Queue.md**: Add responsibility bullets (e.g. "Watcher/Commander append to prompt-queue; EAT-QUEUE reads and dispatches; processor writes Watcher-Result per entry." "Task-Queue: PROCESS TASK QUEUE reads; task/roadmap skills consume; Watcher-Result + Mobile-Pending-Actions.").
- **Add**: "Example queue lines" subsection: one example JSON line for prompt-queue (e.g. `{"mode":"DISTILL MODE","source_file":"1-Projects/MyProject/Note.md","id":"req-1"}`) and one for Task-Queue format if different.
- **Mermaid**: Keep full queue processor flow and two entry points; ensure canonical order diagram includes SEEDED-ENHANCE, BATCH-* if applicable.

---

## 11. Parameters.md

- **Confidence bands**: Add responsibility bullets (e.g. "High ≥85%: Pipelines may run destructive steps after per-change snapshot; skills read high_threshold from config if set." "Mid 72–84%: Single refinement loop; loop_* fields written to pipeline log.").
- **Add**: "Example Watcher-Result line": one full line (requestId | status | message | trace | completed).
- **Add**: "Tuning cheat sheet" block — quick table or bullets for realistic adjustments: (1) Increase batch_size_for_snapshot if snapshots become too frequent. (2) Lower async_preview_threshold if you want more aggressive async loops. (3) Change archive age_days (e.g. 90 → 180) for longer project lifecycles. (4) hub_names order affects MOC priority. Keeps Parameters the go-to for "what can I tweak?"
- **Mermaid**: Keep confidence bands, Async-Loop, Watcher-Result structure, queue modes.

---

## 12. Templates.md

- **Add**: "Responsibilities" (short): "Templates/ provides consistent structure for new notes; pipelines and skills assume frontmatter (created, tags, para-type, status) and standard callouts."
- **Add**: "Example callouts" subsection with full text:
  - Proposal: `> [!proposal] Classification / path proposal — Add approved: true to frontmatter and run EAT-QUEUE to process.`
  - Preview: `> [!preview] Pending highlight/distill/express — run EAT-QUEUE after review.`
  - Success: `> [!success] Progress report generated — [[path/to/export]].`
- **Mermaid**: Keep template → new note flow and consistent-formatting backbone.

---

## 13. Color-Coded-Highlighting.md

- **Add**: "Responsibilities" (short): "Highlightr + master key (Highlightr-Color-Key) define semantics; distill-highlight-color and layer-promote apply colors; project highlight_key overrides; analogous = related, complementary = contrast."
- **Add**: One "Usage example" (e.g. "Set frontmatter highlight_perspective: combat or trigger HIGHLIGHT PERSPECTIVE: combat — distill-highlight-color then applies lens-focused analogous colors.").
- **Optional**: Simple Mermaid flow (trigger → distill-highlight-color → layer-promote → note with colors); only if not redundant with Skills.md highlighter flow.

---

## 14. Plugins.md

- **Obsidian (required) table**: Add "Responsibilities" column (e.g. "Dataview: Queries and dashboards; agent does not modify Dataview queries in notes." "Highlightr: Renders colors; agent sets data-highlight-source and class; master key in Highlightr-Color-Key." "Local REST API: MCP uses for all vault writes; API key in MCP env." "Watcher: Writes signal, reads result; agent must not move/delete Watcher paths.").
- **Optional table**: Same for Commander (surfaces triggers; agent logs commander_source/commander_macro).
- **Add**: One usage example (e.g. "After a pipeline run, open Vault-Change-Monitor (Dataview) to see last N log entries; check Watcher-Result for requestId status.").
- **Mermaid**: Keep component and data flow diagram.

---

## 15. Cursor-Skill-Pipelines-Reference.md (targeted)

- **No structural change**; it is the canonical pipeline + snapshot triggers source.
- **Optional**: Add a short "Documentation map" at top linking to Second-Brain/README and Pipelines.md, Logs.md, so readers know where the summary tables live (Pipelines.md, Logs.md) vs full detail (this file).

---

## 16. Diagram and cross-link audit

- **Mermaid**: After edits, ensure every doc that references a flowchart has valid Mermaid (no spaces in node IDs, no reserved words, quoted edge labels where needed per workspace Mermaid rules).
- **Cross-links**: Second-Brain docs already link to each other and to Cursor-Skill-Pipelines-Reference; add:
  - Pipelines.md → Snapshot triggers table (link to Cursor-Skill-Pipelines-Reference § Snapshot triggers).
  - Logs.md → Snapshot triggers (when to log snapshot path) and Pipeline logs table → Cursor-Skill-Pipelines-Reference log format.
  - Backbone.md → Cursor-Skill-Pipelines-Reference (canonical order + snapshot triggers).

---

## Implementation order

1. **README.md** — Index fix, Mermaid list, "How to use," mental model in 60s, usage-at-a-glance, trigger cheat sheet, troubleshooting, pointer to Backbone invariants; optional changelog subsection or note to add Changelog.md.
2. **Backbone.md** — Key invariants / safety guarantees, component responsibilities, link to Cursor-Skill-Pipelines-Reference; optional troubleshooting pointer.
3. **Rules.md** — Responsibility bullets (always + context), usage examples.
4. **Skills.md** — Responsibilities column, usage examples.
5. **Pipelines.md** — Snapshot triggers summary, pipeline responsibilities, usage examples, optional Mermaid.
6. **MCP-Tools.md** — Responsibilities per group, usage examples, parameter notes.
7. **Configs.md** — Responsibilities, example snippet.
8. **Logs.md** — Responsibilities, example log line, snapshot cross-link.
9. **Vault-Layout.md** — Responsibilities per folder, usage example.
10. **Queue-Sources.md** — Responsibilities, example queue lines.
11. **Parameters.md** — Responsibilities, example Watcher-Result line, tuning cheat sheet.
12. **Templates.md** — Responsibilities, example callouts.
13. **Color-Coded-Highlighting.md** — Responsibilities, one usage example; optional diagram.
14. **Plugins.md** — Responsibilities column, usage example.
15. **Cursor-Skill-Pipelines-Reference.md** — Optional "Documentation map" at top.
16. **Changelog.md** (optional) — If not using a README subsection, create `3-Resources/Second-Brain/Changelog.md` with lite version history (e.g. 2026-03: responsibility columns, usage examples, cheat sheets, troubleshooting; 2026-02: SEEDED-ENHANCE pipeline).
17. **Pass**: Mermaid validity and cross-link check across all 14 + reference (+ Changelog if created).

---

## Out of scope (for this plan)

- Creating new notes beyond optional **Changelog.md** (as above).
- Changing `.cursor/rules/` or `.cursor/skills/` content (only docs under 3-Resources/Second-Brain and the one reference doc).
- Modifying MCP server or tool descriptors in `mcps/`.

