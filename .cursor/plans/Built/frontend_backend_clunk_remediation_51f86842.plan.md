---
name: Frontend Backend Clunk Remediation
overview: "A plan to reduce mobile and backend clunk in the Second Brain: improve pending-queue feedback and modal/toolbar UX (frontend) and optimize queue processing, confidence/safety, and pipeline structure (backend) while preserving manual-first philosophy and batch safety."
todos: []
isProject: false
---

# Frontend & Backend Clunk Remediation Plan

This plan maps your analysis to the existing vault and rules, then outlines concrete remediations. It keeps the **manual-first** philosophy (no auto-processing on queue append) and **batch safety** (dry_run, snapshots, confidence bands) while reducing taps, context switches, and backend overhead.

---

## Current state (brief)

- **Queues**: Two entry points — [3-Resources/prompt-queue.jsonl](3-Resources/prompt-queue.sample.jsonl) (Watcher/EAT-QUEUE; sample only in repo) and [3-Resources/Task-Queue.md](3-Resources/Task-Queue.md) (task/roadmap). Processors: [.cursor/rules/context/auto-eat-queue.mdc](.cursor/rules/context/auto-eat-queue.mdc) (prompt queue) and [.cursor/rules/context/auto-queue-processor.mdc](.cursor/rules/context/auto-queue-processor.mdc) (Task-Queue). Results go to [3-Resources/Watcher-Result.md](3-Resources/Watcher-Result.md) and [3-Resources/Mobile-Pending-Actions.md](3-Resources/Mobile-Pending-Actions.md).
- **Mobile UX**: [3-Resources/Mobile-Toolbar-Task-Commands.md](3-Resources/Mobile-Toolbar-Task-Commands.md) documents toolbar commands and already suggests grouping under "Roadmap Tools"; no in-note pending banner or one-tap Process Queue yet.
- **Config**: [3-Resources/Second-Brain-Config.md](3-Resources/Second-Brain-Config.md) — hub names, archive/highlight/graph; no queue-related or confidence-band toggles.
- **Exclusions**: Listed per-rule (e.g. [.cursor/rules/context/auto-archive.mdc](.cursor/rules/context/auto-archive.mdc)) and summarized in [3-Resources/Second-Brain/Vault-Layout.md](3-Resources/Second-Brain/Vault-Layout.md); not a single machine-readable source.
- **Pipelines**: Long chains in [3-Resources/Cursor-Skill-Pipelines-Reference.md](3-Resources/Cursor-Skill-Pipelines-Reference.md); backup/snapshot/dry_run mandated in [.cursor/rules/always/mcp-obsidian-integration.mdc](.cursor/rules/always/mcp-obsidian-integration.mdc); confidence bands in [.cursor/rules/always/confidence-loops.mdc](.cursor/rules/always/confidence-loops.mdc) and [3-Resources/Second-Brain/Parameters.md](3-Resources/Second-Brain/Parameters.md).

### Enhancements (this revision)

1. **Banner cleanup automation** — auto-queue-processor: post-process step (success > failure) to remove pending callouts via MCP search_replace.
2. **Queue-cleanup skill** — New [.cursor/skills/queue-cleanup/SKILL.md](.cursor/skills/queue-cleanup/SKILL.md); slot after dedup in auto-eat-queue; auto-mark failed entries, append to Errors.md; config **auto_cleanup_after_process: true**.
3. **Batch backup thresholds** — mcp-obsidian-integration: **batch_size_for_snapshot** (e.g. 5); queue > N → BATCH_SNAPSHOT_DIR; else per-change.
4. **Proposal escalation** — Templates: "re-queue after edit" in proposal callout; **approved: true** in frontmatter → next EAT-QUEUE auto-processes.
5. **Testing guide** — README.md: new section "Testing Remediations" (happy path, edge cases, low-conf loop, batch snapshot).
6. **Versioning** — .cursor/sync/changelog.md for rule/skill changes (e.g. "auto-eat-queue v1.1: fast-path").
7. **Mermaid** — Script (e.g. Python) or document manual refresh steps in Backbone.md.

---

## Part 1: Frontend clunk

### 1.1 Pending queue feedback (highest impact)

**Goal**: After queuing (e.g. Task Complete, Add Item), user sees clear feedback and a one-tap path to "Process Queue" without leaving the note.


| Remediation                   | Implementation                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **In-note pending banner**    | When the Watcher plugin (or equivalent) appends to Task-Queue, it **or** a Cursor-side rule can append a temporary callout to the **affected note** (or to Mobile-Pending-Actions.md). Standard: `> [!note] Pending: \<mode\> queued — run **PROCESS TASK QUEUE** or **EAT-QUEUE** to apply.` Document this contract in [3-Resources/Mobile-Toolbar-Task-Commands.md](3-Resources/Mobile-Toolbar-Task-Commands.md) and in [3-Resources/Mobile-Pending-Actions.md](3-Resources/Mobile-Pending-Actions.md) so the Watcher plugin (or a custom hook) can write it. Cursor agent: when processing queue, **remove** or replace the pending callout from the note after successful processing (so it doesn’t pile up). |
| **Banner cleanup automation** | In [.cursor/rules/context/auto-queue-processor.mdc](.cursor/rules/context/auto-queue-processor.mdc): add a **post-process step** after logging and Mobile-Pending-Actions update. **Only if** success count > failure count for the run: scan affected notes (from processed queue entries) and use MCP `**obsidian_search_replace`** to remove pending callouts matching the standard pattern. Prevents clutter when users forget to process; skipped when failures dominate.                                                                                                                                                                                                                                    |
| **One-tap "Process Queue"**   | Document in Mobile-Toolbar-Task-Commands.md: add a **persistent** "Process Queue" (or "EAT-QUEUE") icon to the mobile toolbar (e.g. gear/sync) via Obsidian Commander / Advanced Toolbar; on tap, run command that triggers processing (e.g. opens Cursor with "Process queue" or invokes local script). Implementation is **plugin/settings**; backbone docs describe the UX contract.                                                                                                                                                                                                                                                                                                                           |
| **Opt-in nudge**              | Add to [3-Resources/Second-Brain-Config.md](3-Resources/Second-Brain-Config.md): optional `queue_nudge_after_seconds` (e.g. 30) and `queue_nudge_enabled: true                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |


**Failure visibility**: Ensure task/roadmap skills (e.g. task-complete-validate) always append to Mobile-Pending-Actions.md with **failure reason** (e.g. "Failed: Subtasks incomplete"). Already in [.cursor/rules/context/auto-queue-processor.mdc](.cursor/rules/context/auto-queue-processor.mdc); verify and document in Mobile-Pending-Actions.md that "Last processed" shows both success and failure lines.

### 1.2 Modal-heavy inputs (Add Roadmap Item, Expand Road, Reorder, Merge)

**Goal**: Fewer fields, less scrolling/keyboard occlusion, and optional inline bypass.


| Remediation                | Implementation                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Progressive disclosure** | Document in [3-Resources/Mobile-Toolbar-Task-Commands.md](3-Resources/Mobile-Toolbar-Task-Commands.md) or a new "Modal UX" subsection: prefer stepped modals (e.g. 1: Select roadmap from context → 2: Section → 3: Details). Watcher/plugin should pass **cursor context** (current note path, frontmatter) so Cursor can pre-fill; document that queue payload may include `source_file`, `project_id` from current note.                                            |
| **Context-aware defaults** | Use existing MCP/classify: e.g. `classify_para` / frontmatter to infer `project-id`; default primary path to current file or project roadmap. Document in [3-Resources/Second-Brain/Parameters.md](3-Resources/Second-Brain/Parameters.md) or Queue-Sources: optional fields for queue entries (`source_file`, `project_id`, `cursor_line`) and that the processor uses them for defaults.                                                                             |
| **Inline fallback**        | Add optional **inline queue** format: e.g. in-note line `#queued-add: New item description` or `#queued-expand: Section name — bullet1; bullet2`. Document in [3-Resources/Second-Brain/Queue-Sources.md](3-Resources/Second-Brain/Queue-Sources.md) and in Mobile-Toolbar-Task-Commands: "Add Item" can have a toggle "Quick add (inline)" that inserts such a line; queue processor (or a separate sweep) parses and creates entries. Keeps modal for complex cases. |


### 1.3 Toolbar overcrowding


| Remediation               | Implementation                                                                                                                                                                                                                                                                                                                                         |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Nested sub-menus**      | Already suggested in [3-Resources/Mobile-Toolbar-Task-Commands.md](3-Resources/Mobile-Toolbar-Task-Commands.md). Strengthen: "Prioritize **Task Complete** and **Process Queue** on main bar; group TASK-ROADMAP, Add Roadmap Item, Expand Road, Reorder, Duplicate, Merge, Export, Progress under one 'Roadmap Tools' icon (Commander/Note Toolbar)." |
| **Contextual visibility** | Document in [3-Resources/Second-Brain/Vault-Layout.md](3-Resources/Second-Brain/Vault-Layout.md): "Toolbar: Optional context-based visibility — e.g. show Roadmap Tools only when note has `para-type: Roadmap` or path under `1-Projects/…/Roadmap/`. Configure via Commander/plugin settings."                                                       |
| **Voice/shortcut**        | One-line in Mobile-Toolbar-Task-Commands: "Power users: use command palette or mobile voice (e.g. Siri shortcut) to run 'Process queue' or 'Task Complete' to reduce toolbar reliance."                                                                                                                                                                |


### 1.4 Lower clunk (report/export, proposals)


| Remediation                      | Implementation                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Export/Progress output**       | In [.cursor/rules/context/auto-queue-processor.mdc](.cursor/rules/context/auto-queue-processor.mdc) (EXPORT-ROADMAP, PROGRESS-REPORT): require that the skill/handler **appends an in-note callout** to the roadmap or a dedicated note, e.g. `> [!success] Progress report generated — [[path/to/export]]`. Document in [3-Resources/Second-Brain/Templates.md](3-Resources/Second-Brain/Templates.md) under a "Result callouts" section.                                                             |
| **Proposal callout**             | Add to [3-Resources/Second-Brain/Templates.md](3-Resources/Second-Brain/Templates.md): standard **Proposal** callout format for low-confidence outputs, e.g. `> [!proposal] Title — Approve/Process (optional button link).` So pipeline logs and Mobile-Pending-Actions can reference a consistent pattern for "needs approval" items.                                                                                                                                                                |
| **Proposal re-queue after edit** | In Templates.md: add a **"re-queue after edit"** flag in the proposal callout (e.g. "Add `approved: true` to frontmatter and run EAT-QUEUE to process"). When user adds `**approved: true`** to the note's frontmatter, the **next EAT-QUEUE** run (or a pre-dispatch scan in auto-eat-queue) detects it and auto-processes that note. Document in Queue-Sources and auto-eat-queue: scan for notes with `approved: true` and a matching proposal id/tag, then inject a queue entry or process inline. |


---

## Part 2: Backend clunk

### 2.1 Queue processing overhead

**Goal**: Lighter path for single-item mobile runs; clearer single source; optional cleanup.


| Remediation                    | Implementation                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Fast-path for single entry** | In [.cursor/rules/context/auto-eat-queue.mdc](.cursor/rules/context/auto-eat-queue.mdc): after parse/validate, **if valid entry count === 1**, skip dedup and sort; dispatch immediately. Same in [.cursor/rules/context/auto-queue-processor.mdc](.cursor/rules/context/auto-queue-processor.mdc) for Task-Queue.md (single line → dispatch). Preserves full dedup/sort for batch.                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **Unified queue (optional)**   | Document in [3-Resources/Second-Brain/Queue-Sources.md](3-Resources/Second-Brain/Queue-Sources.md): "Unified option: single append-only file (e.g. Task-Queue.md with JSON lines for both pipeline and task modes) to reduce Watcher branches; current two-file design remains supported." If you later merge, one queue file + one processor rule; update Watcher to append to that file only.                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **Queue-cleanup skill**        | New skill **[.cursor/skills/queue-cleanup/SKILL.md](.cursor/skills/queue-cleanup/SKILL.md)**. **Slot**: after dedup (and before or after sort) in [.cursor/rules/context/auto-eat-queue.mdc](.cursor/rules/context/auto-eat-queue.mdc). Behavior: sweep entries that failed validation or dispatch; **auto-mark** them `queue_failed: true` if not already; **append** a short summary to [3-Resources/Errors.md](3-Resources/Errors.md) for review (e.g. "Queue cleanup: N failed entries marked; see queue file."). **Trigger**: optional config in [3-Resources/Second-Brain-Config.md](3-Resources/Second-Brain-Config.md): `auto_cleanup_after_process: true` — when true, run queue-cleanup after each EAT-QUEUE run; when false, only when user runs "Clear queue" or "Queue cleanup". Document in Queue-Sources and Cursor-Skill-Pipelines-Reference. |
| **Async signaling**            | In [3-Resources/Second-Brain/Logs.md](3-Resources/Second-Brain/Logs.md): "When queue backlog > N (e.g. 5), optionally append a Watcher-Signal line to nudge processing." Document only; actual nudge can be Watcher or cron.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |


### 2.2 Confidence loops and safety redundancy

**Goal**: Fewer redundant backups when batching; optional tunable bands and loop-skip; assistive proposal re-queue.


| Remediation                  | Implementation                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Batch-optimized backups**  | In [.cursor/rules/always/mcp-obsidian-integration.mdc](.cursor/rules/always/mcp-obsidian-integration.mdc): document that **batch runs** (e.g. >3 notes in one pipeline run) should use **one** `obsidian_ensure_backup` at start (or `create_backup` once per batch) and prefer **batch snapshots** (BATCH_SNAPSHOT_DIR) for the group; per-note per-change snapshots still before each destructive step. Add optional env/docs: `MAX_BACKUP_AGE_MINUTES` (e.g. 2880) so ensure_backup is not called every note.                                                                        |
| **Batch backup thresholds**  | In [.cursor/rules/always/mcp-obsidian-integration.mdc](.cursor/rules/always/mcp-obsidian-integration.mdc): add a **config var** (e.g. in Second-Brain-Config or MCP env) `**batch_size_for_snapshot: 5`**. When **queue length (or batch size) > this value**, use **BATCH_SNAPSHOT_DIR** for the run (one batch snapshot for the group); when **≤ this value**, use **per-change** snapshots per note as today. This fine-tunes overhead: large batches get one batch snapshot; small/mobile single-item runs stay per-change. Document in Parameters.md and mcp-obsidian-integration. |
| **Tunable bands**            | In [3-Resources/Second-Brain-Config.md](3-Resources/Second-Brain-Config.md): add optional `confidence_bands` (e.g. `mid: [80, 90]`, `high_threshold: 90`). Rules and skills **read** these when present; fallback to current 72–84 and 85. Document in [.cursor/rules/always/confidence-loops.mdc](.cursor/rules/always/confidence-loops.mdc) and [3-Resources/Second-Brain/Parameters.md](3-Resources/Second-Brain/Parameters.md).                                                                                                                                                     |
| **Loop-skip flag**           | In [.cursor/rules/always/confidence-loops.mdc](.cursor/rules/always/confidence-loops.mdc): add frontmatter `**loop-skip: true`** (or `skip_refinement_loop: true`): when set, skip the mid-band refinement loop for that note (trusted path). Document in Parameters.md and pipeline reference.                                                                                                                                                                                                                                                                                         |
| **Proposal auto-escalation** | In confidence-loops: **opt-in** behavior: when a proposal is logged (low confidence), append a **refine-proposal** queue entry (e.g. to Task-Queue or prompt-queue) with note path and proposal id so user can "Process queue" later to re-run refinement. Document in Queue-Sources and Parameters; implement in the pipeline that writes proposals.                                                                                                                                                                                                                                   |


### 2.3 Pipeline and skill chain complexity

**Goal**: Easier debugging and one place for exclusions; no mandatory MCP API changes.


| Remediation                | Implementation                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Modular pipelines**      | In [3-Resources/Cursor-Skill-Pipelines-Reference.md](3-Resources/Cursor-Skill-Pipelines-Reference.md) and [3-Resources/Second-Brain/Pipelines.md](3-Resources/Second-Brain/Pipelines.md): describe **sub-pipelines** (e.g. "ingest-core": backup → classify → enrich → organize; "ingest-post-process": split → distill → hub → move). Same order, but clearer phases for debugging. Optional "slot (after)" in [3-Resources/Second-Brain/Skills.md](3-Resources/Second-Brain/Skills.md) for reordering. |
| **Centralized exclusions** | Add **exclusions** section to [3-Resources/Second-Brain/Configs.md](3-Resources/Second-Brain/Configs.md) (or new [3-Resources/Second-Brain/exclusions.yaml](3-Resources/Second-Brain/exclusions.yaml)): list Backups/, **/Log*.md, **/* Hub.md, Watcher paths, watcher-protected. Context rules and pipeline reference **reference** this single list; keep existing Excludes sections in rules as the authoritative copy but document "see Configs.md / exclusions.yaml for canonical list."            |
| **MCP call optimization**  | Document only in [3-Resources/Second-Brain/Logs.md](3-Resources/Second-Brain/Logs.md) or MCP-Tools: "Monitor MCP-Health for bottlenecks; future option: bundle classify_para + subfolder_organize into one 'organize-para' tool to reduce roundtrips." No code change in this plan.                                                                                                                                                                                                                      |


### 2.4 Logging and restore


| Remediation            | Implementation                                                                                                                                                                                                                                                                                                                                                                                               |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Log rotation**       | New **log-rotate** skill (or a section in snapshot-sweep): when triggered (e.g. monthly or by "Rotate logs" command), copy current Ingest-Log, Archive-Log, etc. to an archive path (e.g. `3-Resources/Logs-Archive/Ingest-Log-YYYY-MM.md`) and truncate or start fresh. Document in [3-Resources/Second-Brain/Logs.md](3-Resources/Second-Brain/Logs.md) and pipeline reference.                            |
| **Restore-queue mode** | Document in [.cursor/rules/always/mcp-obsidian-integration.mdc](.cursor/rules/always/mcp-obsidian-integration.mdc) or a short "Restore" section: **restore-queue** mode: user maintains a list (e.g. in Errors.md or a Restore-Queue.md) of snapshot paths to restore; processor reads list and runs restore steps (read snapshot → write to original path) one-by-one. No auto-restore; explicit user list. |


---

## Part 3: Documentation and sync

- **Backbone**: Update [3-Resources/Second-Brain/Backbone.md](3-Resources/Second-Brain/Backbone.md), [3-Resources/Second-Brain/README.md](3-Resources/Second-Brain/README.md) with links to Queue-Sources, Parameters, Config (new queue/confidence options), Vault-Layout (toolbar), Templates (callouts), Logs (rotation, health).
- **Sync**: Per [.cursor/rules/always/backbone-docs-sync.mdc](.cursor/rules/always/backbone-docs-sync.mdc), update [.cursor/sync/](.cursor/sync/) for any changed rules/skills.
- **Mermaid**: Refresh diagrams in Queue-Sources (fast-path branch), Parameters (tunable bands), Vault-Layout (toolbar) where needed.

### Testing guide

- Add a new section **"Testing Remediations"** in [3-Resources/Second-Brain/README.md](3-Resources/Second-Brain/README.md). Include:
  - **Happy path**: Queue a single Task Complete on mobile → verify in-note pending banner appears → tap one-tap Process Queue (or run EAT-QUEUE in Cursor) → verify task marked complete and **banner cleanup** removes the pending callout; check Mobile-Pending-Actions and Watcher-Result.
  - **Edge cases**: (1) Low-conf loop — trigger a note in mid-band (72–84%); verify proposal callout and that adding `approved: true` then EAT-QUEUE re-processes. (2) Success ≤ failure — run with one success and one failure; verify banner cleanup does **not** remove pending callouts from the failed item's note. (3) Queue-cleanup with `auto_cleanup_after_process: true` — run EAT-QUEUE with a failed entry; verify queue-cleanup marks it and appends to Errors.md.
  - **Batch snapshot threshold**: Run with queue size > `batch_size_for_snapshot` (e.g. 5); verify BATCH_SNAPSHOT_DIR is used; run with 1–2 items and verify per-change snapshots only.

### Versioning rules and skills

- In [.cursor/sync/](.cursor/sync/): add **changelog.md** (or [.cursor/sync/changelog.md](.cursor/sync/changelog.md)) to record rule/skill changes with a simple version and one-line description. Example entries: "auto-eat-queue v1.1: Added fast-path for single entry"; "auto-queue-processor v1.1: Banner cleanup post-step (success > failure)"; "queue-cleanup skill v1.0: New skill, slot after dedup; auto_cleanup_after_process config." Keep chronological; reference from backbone-docs-sync so doc updates note changelog when rules/skills change.

### Mermaid diagram refresh

- **Option A (script)**: If feasible, add a small script (e.g. Python in a `code_execution` or `scripts/` folder) that reads pipeline/skill metadata and **regenerates** Mermaid diagrams into the relevant .md files (Queue-Sources, Parameters, Pipelines, Vault-Layout). Document script location and usage in Backbone.
- **Option B (manual)**: Document in [3-Resources/Second-Brain/Backbone.md](3-Resources/Second-Brain/Backbone.md) **manual steps** for refreshing Mermaid: list which docs contain diagrams (Queue-Sources, Parameters, Pipelines, Vault-Layout, Logs), and a short checklist (e.g. "After changing pipeline order, update Cursor-Skill-Pipelines-Reference and Queue-Sources canonical-order diagram"). Prefer manual steps if auto-gen is not implemented.

---

## Implementation order (suggested)

1. **Config and docs** — Second-Brain-Config (nudge, bands, **auto_cleanup_after_process**, **batch_size_for_snapshot**), Queue-Sources (fast-path, unified option, cleanup), Parameters (tunable bands, loop-skip), Templates (proposal + result callouts + **re-queue after edit** / **approved: true**), Vault-Layout (toolbar/contextual).
2. **Queue rules** — auto-eat-queue: single-entry fast-path; **queue-cleanup skill** (slot after dedup; trigger via **auto_cleanup_after_process**); optional scan for **approved: true** to re-process proposals. auto-queue-processor: single-entry fast-path; **banner cleanup** post-step (success > failure, MCP search_replace). mcp-obsidian-integration: **batch_size_for_snapshot** (if queue > N use BATCH_SNAPSHOT_DIR, else per-change).
3. **Mobile feedback** — Mobile-Pending-Actions and Mobile-Toolbar-Task-Commands: in-note pending banner contract, one-tap Process Queue, failure visibility; optional inline #queued-add in Queue-Sources.
4. **Confidence** — confidence-loops: loop-skip flag; proposal **approved: true** → next EAT-QUEUE auto-processes; Config reading of bands.
5. **Exclusions and pipelines** — Configs.md or exclusions.yaml; Pipelines.md / Cursor-Skill-Pipelines-Reference sub-pipelines and slots.
6. **Logs and restore** — log-rotate skill, restore-queue mode doc; Logs.md and MCP rule.
7. **Backbone and sync** — Backbone (incl. **Mermaid manual steps** or script doc), README (**Testing Remediations** section), sync folder, **.cursor/sync/changelog.md** for rule/skill versioning, diagrams.

---

## Out of scope (by design)

- **No auto-run on queue append** — Processing still requires user to trigger "EAT-QUEUE" or "Process queue"; nudge is optional and assistive.
- **No removal of dry_run or per-change snapshots** — Safety invariants unchanged.
- **No Obsidian plugin code** — Toolbar and modal behavior are documented contracts; implementation is Obsidian/Commander/Watcher.
- **No mandatory MCP server changes** — Only docs and rule/skill text; optional env (MAX_BACKUP_AGE_MINUTES) if server supports.

