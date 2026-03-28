---
name: Subagent documentation suite
overview: Create a code-first documentation suite in 3-Resources/Second-Brain/Docs/Subagents/ (eight files), then enrich it from old docs to close gaps. Execution is deferred until plan mode is off; this plan specifies exact content and structure for each file.
todos: []
isProject: false
---

# Subagent Documentation Suite — Plan

Version: 2026-03 — post-subagent migration. This plan specifies the exact documentation to create; **no file writes occur until plan mode is turned off**.

---

## Phase 1 — Code-first documentation (source of truth: current codebase only)

**Create folder:** `3-Resources/Second-Brain/Docs/Subagents/` (create if missing). **All new documentation must live under Docs/; never create doc files under Second-Brain root or outside Docs/.**

**Strict order:** Write the eight files below in sequence. Base content **only** on:

- `.cursor/agents/*.md` (ingest, distill, express, archive, organize, roadmap, research)
- `.cursor/rules/agents/queue.mdc` (Queue/Dispatcher)
- `.cursor/rules/always/dispatcher.mdc`, `core-guardrails.mdc`, `system-funnels.mdc`, `watcher-result-append.mdc`
- `3-Resources/Second-Brain/Subagent-Safety-Contract.md`
- `3-Resources/Second-Brain/Queue-Sources.md` (modes, routing)
- `3-Resources/Second-Brain/Parameters.md` (confidence bands, RESUME-ROADMAP params)
- `3-Resources/Second-Brain/Vault-Layout.md` (folder roles, protected paths)
- `.cursor/rules/context/auto-eat-queue.mdc` (Step 0, dispatch table) — for Queue behavior only

Do **not** pull content from old README, Cursor-Skill-Pipelines-Reference, or other legacy docs in Phase 1.

---

### 1. README.md

- **Purpose blurb:** Entry point for the Subagents documentation; orients readers to the post-migration subagent architecture.
- **Sections:**
  - Version line: `Version: 2026-03 — post-subagent migration`
  - What are subagents: Cursor native subagents (`.cursor/agents/*.md`) + Queue/Dispatcher rule; delegation vs legacy fallback (`.cursor/rules/legacy-agents/*.mdc`).
  - How to use this folder: Links to Architecture, Subagent-List, Creating-Subagents, Delegation-Patterns, Safety-Invariants, Migration-Guide, Examples.
  - Key concepts: Main agent → Dispatcher (queue triggers) or System Funnels (direct triggers) → pipeline subagents; hand-off contract (Subagent-Safety-Contract); two queues (prompt-queue.jsonl, Task-Queue.md).
  - One short bullet list of trigger families: EAT-QUEUE / PROCESS TASK QUEUE → Queue; INGEST MODE, DISTILL MODE, etc. → pipeline subagents; “We are making a prompt” → Prompt-Crafter (no subagent).

---

### 2. Architecture.md

- **Purpose blurb:** High-level architecture: main agent, dispatcher, queue processor, and pipeline subagents; single Mermaid diagram.
- **Version:** 2026-03 — post-subagent migration.
- **Sections:**
  - **Overview:** Main agent (Thoth-AI) always loads core guardrails, persona, PARA; then either runs Queue/Dispatcher (for queue triggers) or follows system-funnels for direct triggers. Queue rule runs in main context; it does Step 0 (wrappers), reads queue, dispatches by mode to pipeline subagents. Pipeline subagents are Cursor native (`.cursor/agents/<name>.md`) or legacy (`.cursor/rules/legacy-agents/<name>.mdc`).
  - **Mermaid diagram (required):** One flowchart. Nodes: `User`, `MainAgent`, `Dispatcher`, `QueueRule`, `PipelineSubagents` (or one box “Ingest | Distill | Express | Archive | Organize | Roadmap | Research”). Edges: User → MainAgent; MainAgent → Dispatcher (when EAT-QUEUE / PROCESS TASK QUEUE); Dispatcher → QueueRule; QueueRule → PipelineSubagents (dispatch by mode); for direct triggers, MainAgent → PipelineSubagents (via system-funnels). Label edges: “EAT-QUEUE / PROCESS TASK QUEUE”, “INGEST MODE / DISTILL MODE / …”, “return: summary + Watcher-Result”.
  - **Queue vs direct:** Table: Trigger type | Router | Who runs pipeline. Rows: Queue (EAT-QUEUE, etc.) | Dispatcher → Queue rule | Queue dispatches to subagent; Direct (INGEST MODE, etc.) | System-funnels | Main agent delegates to subagent.
  - **File locations:** Table: Component | Location. Queue rule: `.cursor/rules/agents/queue.mdc`. Pipeline subagents: `.cursor/agents/<name>.md` (prefer), `.cursor/rules/legacy-agents/<name>.mdc` (fallback). Safety contract: `3-Resources/Second-Brain/Subagent-Safety-Contract.md`.

---

### 3. Creating-Subagents.md

- **Purpose blurb:** How to add or clone a subagent; template and conventions.
- **Version:** 2026-03 — post-subagent migration.
- **Sections:**
  - **When to add a subagent:** New pipeline that owns destructive or stateful work (e.g. a new pipeline type); otherwise extend an existing subagent or add a skill.
  - **Cursor native subagent (.md):** Create `.cursor/agents/<name>.md` with YAML frontmatter: `name`, `description`, `model: inherit`, `background: false`. Body: role, “Obey Subagent-Safety-Contract”, flow/steps, return format (one-paragraph summary, wrapper/queue created, Success / #review-needed / failure, Watcher-Result when requestId).
  - **Agent rule (.mdc) for Queue:** If the new pipeline is dispatched from the queue, add a row to the dispatch table in `queue.mdc` (and in auto-eat-queue if referenced) mapping mode → subagent or skill.
  - **Legacy fallback:** Copy or adapt from `.cursor/rules/agents/_template.mdc`; put pipeline rule in `.cursor/rules/legacy-agents/<name>.mdc` so that when delegation is off, the main agent can run the same flow from the rule.
  - **Register in system-funnels:** Add trigger phrases and mode(s) in `system-funnels.mdc` and, if queue-driven, in `queue.mdc` ordering and dispatch.
  - **Checklist:** Safety contract obeyed; backup/snapshot/confidence bands; Error Handling Protocol; Watcher-Result; no shell vault mutations.

---

### 4. Subagent-List.md

- **Purpose blurb:** Quick reference table of all subagents and the Queue rule; when each is used and key responsibilities.
- **Version:** 2026-03 — post-subagent migration.
- **Single table** with columns: **Name** | **Description** | **When used** | **Key responsibilities** | **Example invocation**
- **Rows (from codebase):**
  - **Queue (Dispatcher)** — Processes prompt queue and task queue; Step 0 wrappers, read/validate/order, dispatch by mode, Watcher-Result, clear passed. EAT-QUEUE, Process queue, EAT-CACHE, PROCESS TASK QUEUE. Example: “EAT-QUEUE”
  - **Ingest** — Full-autonomous-ingest: Ingest/ processing, Phase 1 propose + Decision Wrapper, Phase 2 apply-mode. INGEST MODE, Process Ingest, run ingests; queue mode INGEST MODE. Example: “INGEST MODE” or queue entry `{"mode":"INGEST MODE","source_file":"Ingest/Note.md"}`
  - **Distill** — Autonomous-distill: progressive summarization, highlights, TL;DR, readability; distill-apply-from-wrapper. DISTILL MODE, distill this note, DISTILL LENS, HIGHLIGHT PERSPECTIVE; queue DISTILL MODE, BATCH-DISTILL. Example: “DISTILL LENS: beginner”
  - **Express** — Autonomous-express: related content, outline, CTA, version snapshots; express-apply-from-wrapper. EXPRESS MODE, express this note, EXPRESS VIEW; queue EXPRESS MODE, BATCH-EXPRESS. Example: “EXPRESS VIEW: stakeholder”
  - **Archive** — Autonomous-archive: move completed/inactive to 4-Archives/, summary preservation, ghost-folder sweep. ARCHIVE MODE, archive this note; queue ARCHIVE MODE. Example: “ARCHIVE MODE”
  - **Organize** — Autonomous-organize: re-classify, re-path, frontmatter-enrich, name-enhance, move in 1/2/3. ORGANIZE MODE, re-organize this note; queue ORGANIZE MODE; FORCE-WRAPPER with source under 1/2/3. Example: “ORGANIZE MODE”
  - **Roadmap** — ROADMAP MODE = setup (Phase 0, roadmap-state, workflow_state, roadmap-generate-from-outline); RESUME-ROADMAP = one action per run (default deepen). ROADMAP MODE, Resume roadmap, RESUME-ROADMAP; queue ROADMAP MODE, RESUME-ROADMAP (and aliases). Example: “RESUME-ROADMAP” or “ROADMAP MODE”
  - **Research** — Queue-only RESEARCH-AGENT: project_id + linked_phase, research-agent-run, queue INGEST/DISTILL for new notes. Queue mode RESEARCH-AGENT, RESEARCH-GAPS. Example: queue entry `{"mode":"RESEARCH-AGENT","source_file":"1-Projects/X/Roadmap/Phase-1.md"}`

---

### 5. Delegation-Patterns.md

- **Purpose blurb:** How the main agent delegates to subagents; hand-off structure and fallback.
- **Version:** 2026-03 — post-subagent migration.
- **Sections:**
  - **Preferred path:** Main agent delegates to `.cursor/agents/<name>.md` using the mandatory hand-off prompt from Subagent-Safety-Contract (task, queue entry, critical invariants, state files, return format).
  - **Fallback:** When delegation is not used (e.g. Cursor context), run the pipeline from `.cursor/rules/legacy-agents/<name>.mdc`; same behavior, no separate “subagent process.”
  - **Rollback:** To disable native subagents: rename or remove `.cursor/agents/*.md` so only legacy rules run; dispatcher and queue still use the same mode → pipeline mapping via legacy-agents.
  - **Queue flow:** Queue rule runs in main agent; it does not “invoke a subagent process” for itself—it runs the steps (Step 0, read, parse, order, dispatch). For each queue entry, it delegates execution to the corresponding pipeline subagent (ingest, roadmap, etc.) via hand-off or legacy rule.
  - **What gets passed:** Queue entry (id, mode, params, source_file, prompt); requestId for Watcher-Result; relevant state files (e.g. roadmap-state.md, workflow_state.md for roadmap). Subagent returns: one-paragraph summary, any wrapper/queue entry created, status, and appends Watcher-Result line when requestId present.

---

### 6. Safety-Invariants.md

- **Purpose blurb:** Exhaustive list of safety invariants all subagents and the Queue must obey; no duplication of logic, only consolidation and references.
- **Version:** 2026-03 — post-subagent migration.
- **Sections (each with short subsections or tables):**
  - **Backups:** Before any destructive operation, ensure backup (obsidian_ensure_backup / obsidian_create_backup). If backup fails, abort destructive steps for that note, log #review-needed. Reference: core-guardrails, mcp-obsidian-integration.
  - **Per-change snapshots:** Before move, rename, split, structural distill, append_to_hub: obsidian-snapshot type per-change when confidence ≥85%. Snapshot failure → skip destructive action, log #review-needed. Snapshots under Backups/Per-Change/; append-only. Reference: core-guardrails, mcp-obsidian-integration.
  - **Confidence bands:** High ≥85%: destructive only after snapshot. Mid 68–84%: at most one non-destructive refinement loop; proceed only if post_loop_conf ≥85%; else Decision Wrapper. Low <68%: no destructive action; Decision Wrapper. Decay: post_loop_conf ≤ pre_loop_conf → user decision, no destructive action. Reference: Parameters.md, confidence-loops.
  - **Critical invariant:** No destructive action unless (1) confidence in high band and (2) per-change snapshot succeeded in current run.
  - **No shell vault ops:** No cp/mv/rm on vault; all moves/renames via MCP (obsidian_move_note, etc.) with backup and snapshot gates. Exception: documented attachment-move skill, user-invoked.
  - **Structure before move:** obsidian_ensure_structure(parent of target) then obsidian_move_note dry_run then commit. Post-move frontmatter: para-type, project-id when under 1-Projects/, status archived when under 4-Archives/.
  - **Exclusions and protected paths:** Backups/**, Watcher-Signal.md, Watcher-Result.md, Ingest/watched-file.md, watcher-protected: true; do not move/delete. Do not process Ingest/Decisions/** as primary input. Reference: core-guardrails, Vault-Layout.
  - **Error Handling Protocol:** On failure: Trace (timestamp, pipeline, stage, path(s), message); Summary (error_type, root cause, impact, suggested fixes, recovery); log to 3-Resources/Errors.md (heading, inline table, #### Trace, #### Summary); one-line ref in pipeline log; create error Decision Wrapper under Ingest/Decisions/Errors/ when appropriate; severity high → #review-needed, skip destructive for that note. Progressive fallbacks before logging. Reference: mcp-obsidian-integration § Error Handling Protocol.
  - **Watcher-Result contract:** On run finish (queue or direct), append one line per requestId: `requestId: <id> | status: success|failure | message: "..." | trace: "..." | completed: <ISO8601>`. Path: 3-Resources/Watcher-Result.md. Reference: watcher-result-append.mdc.
  - **Roadmap state:** Read roadmap-state.md and workflow_state.md before mutate; snapshot state before and after update; on parse failure abort and log #state-corrupt. Reference: mcp-obsidian-integration, roadmap subagent.
  - **Restore:** User-triggered only; no auto-restore. Reference: mcp-obsidian-integration.

---

### 7. Migration-Guide.md

- **Purpose blurb:** Before/after for teams or future readers; how pipelines moved from monolithic rules to subagents.
- **Version:** 2026-03 — post-subagent migration.
- **Sections:**
  - **Before → After comparison table:** One table. Columns: **Pipeline / area** | **Before** | **After**. Rows: Ingest → “Single rule (e.g. para-zettel-autopilot / auto-ingest)” → “Ingest subagent (agents/ingest.md) + legacy-agents/ingest.mdc”; Distill → “auto-distill context rule” → “Distill subagent + legacy”; Express → “auto-express” → “Express subagent + legacy”; Archive → “auto-archive” → “Archive subagent + legacy”; Organize → “auto-organize” → “Organize subagent + legacy”; Roadmap → “auto-roadmap / roadmap context” → “Roadmap subagent + legacy”; Research → “inline or single rule” → “Research subagent (queue-only) + legacy”; Queue → “Inline in main rule set / auto-eat-queue” → “Queue rule (agents/queue.mdc) in main agent; dispatcher routes EAT-QUEUE here.”
  - **What stayed the same:** Same pipelines (full-autonomous-ingest, autonomous-distill, etc.); same skills in `.cursor/skills/`; same always rules (core-guardrails, confidence-loops, mcp-obsidian-integration, watcher-result-append); same queue files and mode contracts (Queue-Sources); same safety (Subagent-Safety-Contract aligns with existing guardrails).
  - **What changed:** Execution can run in Cursor native subagent context (agents/*.md) with clean context; fallback to legacy-agents/*.mdc when not delegating; single place for hand-off contract (Subagent-Safety-Contract); dispatcher explicitly routes queue triggers to Queue rule.
  - **Rollback:** Remove or rename `.cursor/agents/*.md`; keep `.cursor/rules/legacy-agents/*.mdc` and queue.mdc; behavior reverts to rule-only execution.

---

### 8. Examples.md

- **Purpose blurb:** Concrete usage examples for common flows: INGEST MODE, RESUME-ROADMAP deepen, DISTILL LENS, EAT-QUEUE, etc.
- **Version:** 2026-03 — post-subagent migration.
- **Sections (each with 1–2 short numbered steps + example trigger or payload):**
  - **INGEST MODE:** User says “INGEST MODE” or “Process Ingest.” System-funnels route to Ingest subagent (or legacy ingest rule). Subagent lists Ingest, runs Phase 1 (classify, frontmatter-enrich, propose path, create Decision Wrapper) or Phase 2 apply (when Step 0 had an approved wrapper). Example: “Process Ingest” → Ingest runs on Ingest/*.md.
  - **RESUME-ROADMAP deepen:** User runs EAT-QUEUE with a line `{"mode":"RESUME-ROADMAP","project_id":"my-project","id":"req-1"}` (action default deepen). Queue rule runs Step 0, reads queue, dispatches to Roadmap subagent. Roadmap reads roadmap-state and workflow_state, runs one deepen step, updates state, may append next RESUME-ROADMAP to queue, returns summary and appends Watcher-Result.
  - **DISTILL LENS:** User says “DISTILL LENS: beginner” on a note. System-funnels route to Distill subagent. Subagent sets distill_lens and runs autonomous-distill (layers, highlight, TL;DR, readability). Example: “DISTILL LENS: beginner” with current note.
  - **EXPRESS VIEW:** User says “EXPRESS VIEW: stakeholder high-level” or queue entry with express_view. Express subagent runs related-content-pull, express-mini-outline, express-view-layer, call-to-action-append.
  - **EAT-QUEUE (batch):** User says “EAT-QUEUE.” Dispatcher loads Queue rule. Step 0: scan Ingest/Decisions/**, apply approved wrappers (move note, archive wrapper). Read prompt-queue.jsonl, parse/validate/dedup/order, dispatch each entry by mode to the right subagent; append Watcher-Result per id; clear passed entries.
  - **PROCESS TASK QUEUE:** User says “PROCESS TASK QUEUE.” Queue rule reads Task-Queue.md, dispatches by mode (TASK-ROADMAP, TASK-COMPLETE, ADD-ROADMAP-ITEM, EXPAND-ROAD, etc.), runs the corresponding skills, appends Watcher-Result and updates Mobile-Pending-Actions.
  - **RESEARCH-AGENT (queue):** Queue entry `{"mode":"RESEARCH-AGENT","source_file":"1-Projects/X/Roadmap/Phase-2.md","id":"req-2"}`. Queue dispatches to Research subagent. Research resolves project_id and linked_phase from path, runs research-agent-run, queues INGEST (and optionally DISTILL) for new notes, appends Watcher-Result.

---

## Phase 2 — Gap analysis and enrichment

**Only after** all eight files above are written and saved:

1. **Read old documentation** (priority order):
  - `3-Resources/Second-Brain/README.md`
  - `3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference.md`
  - `3-Resources/Second-Brain/Queue-Sources.md` (full file)
  - `3-Resources/Second-Brain/Parameters.md` (full file)
  - `3-Resources/Second-Brain/Vault-Layout.md` (full file)
  - Context rules: `auto-eat-queue.mdc`, `auto-roadmap.mdc`, `plan-mode-prompt-crafter.mdc`, other `auto-*.mdc` as needed
  - Any file that still mentions “auto-distill”, “auto-roadmap”, “auto-ingest” in a way that implies behavior not covered in the new docs
2. **Compare and list gaps:** Concepts or invariants in old docs missing or unclear in Subagents/*; safety or edge cases only in old docs; valid trigger phrases or modes not documented; terminology drift; explanations that were clearer in old docs.
3. **Update and enrich** the eight Subagents files:
  - Add sections, tables, or warnings where a gap is closed.
  - Preserve the clean structure (no reversion to “old chaos”).
  - Mark each addition with an HTML comment: `<!-- Added from old docs to fill gap: <short description> -->` immediately before the added block.

---

## Phase 3 — Final output

After Phase 1 and Phase 2 are complete, the only response to emit is:

**“Fresh subagent documentation generated and gap-enriched in 3-Resources/Second-Brain/Subagents/”**

Then stop (no extra commentary unless the user asks).

---

## File and style checklist

- Every file: version line at top; purpose blurb at top.
- Markdown: `#` for main sections, `##` for subsections, `###` for sub-subsections.
- Tables for lists/comparisons (Subagent-List.md is one table).
- At least one Mermaid diagram in Architecture.md (main → dispatcher → subagents → return).
- Language: precise, professional, beginner-friendly (familiar with Obsidian/Cursor).
- Bullet and numbered lists; concrete trigger phrases and examples throughout.
- No long walls of text (break with table, list, code block, or diagram before ~10–15 lines).
- Safety-Invariants.md: exhaustive (backups, snapshots, confidence bands, watcher contract, error protocol, exclusions, roadmap state, restore).

---

## Key codebase references (for implementer)


| Need                 | Location                                                                                                         |
| -------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Subagent definitions | `.cursor/agents/ingest.md`, `distill.md`, `express.md`, `archive.md`, `organize.md`, `roadmap.md`, `research.md` |
| Queue / dispatch     | `.cursor/rules/agents/queue.mdc`                                                                                 |
| Routing              | `.cursor/rules/always/dispatcher.mdc`, `system-funnels.mdc`                                                      |
| Safety contract      | `3-Resources/Second-Brain/Subagent-Safety-Contract.md`                                                           |
| Guardrails           | `.cursor/rules/always/core-guardrails.mdc`, `mcp-obsidian-integration.mdc`                                       |
| Watcher              | `.cursor/rules/always/watcher-result-append.mdc`                                                                 |
| Modes and routing    | `3-Resources/Second-Brain/Queue-Sources.md`                                                                      |
| Legacy fallback      | `.cursor/rules/legacy-agents/*.mdc`                                                                              |
| Template             | `.cursor/rules/agents/_template.mdc`                                                                             |


