---
name: wire-roadmap-research-sync-v3
overview: Third-iteration roadmap research integration plan that keeps research synchronous, clarifies RESEARCH-AGENT as a one-shot batch mode, and adds explicit shielding against silent failures across research, deepen, ingest, and distill.
todos:
  - id: inspect-current-deepen-path
    content: Inspect current RESUME-ROADMAP deepen runs, queue entries, and workflow_state metrics to confirm baseline behavior without research.
    status: completed
  - id: add-pre-deepen-research-gates-inline-only
    content: Implement enable_research + util/depth-based gating with inline-only research in auto-roadmap’s deepen branch, ignoring async_research.
    status: completed
  - id: wire-research-outputs-into-deepen
    content: Pass injected_research_summary/paths and gaps into roadmap-deepen, guard against stale injected_research_paths, and ensure they are used and logged per SKILL spec.
    status: completed
  - id: implement-research-agent-mode-one-shot
    content: Ensure RESEARCH-AGENT mode in auto-eat-queue dispatches research-agent-run and queues ingest/distill for new research notes without appending follow-up RESUME-ROADMAP entries, and surfaces empty runs as failures.
    status: completed
  - id: tighten-context-util-postconditions
    content: Enforce strict context-tracking postconditions and ensure util metrics drive inline research and RECAL-ROAD behavior as documented, with hard failures when tracked columns are invalid.
    status: completed
  - id: wire-agent-research-ingest-distill
    content: Verify Ingest/Agent-Research notes flow through ingest and distill pipelines without wrappers, with clear logging and an eventual canonical home under the project, plus idempotent distill markers.
    status: completed
  - id: align-mode-success-contracts
    content: Update Mode-Success-Contracts and related docs so RESUME-ROADMAP and RESEARCH-AGENT success definitions match the synchronous research model and observability guarantees.
    status: completed
  - id: update-roadmap-docs-no-async
    content: Update Second-Brain docs (Queue-Sources, Pipelines, Roadmap-Upgrade-Plan, Parameters, Prompt-Crafter docs, Commander flows, Mobile-Pending-Actions semantics) to reflect inline-only research and deprecate async_research.
    status: completed
isProject: false
---

# Wire roadmap research + deepen sync (no-async v3, hardened)

### 1. Verify current RESUME-ROADMAP + deepen behavior

- **Inspect queue and params**: Confirm current RESUME-ROADMAP entries in `.technical/prompt-queue.jsonl` include research-related params (`enable_research`, `research_queries`, `research_distill`, etc.) as described in [3-Resources/Second-Brain/Queue-Sources.md](3-Resources/Second-Brain/Queue-Sources.md). Treat any existing `async_research` values as legacy/no-op.
- **Trace dispatch path**: Follow `auto-eat-queue` dispatch for `mode: "RESUME-ROADMAP"` into the auto-roadmap rule, and from there into `roadmap-deepen` for `params.action: "deepen"`, validating how `enable_context_tracking` is defaulted and how context metrics (Ctx Util %, Leftover %, Threshold, Est. Tokens / Window, Util Delta %) are computed and written to `workflow_state.md`.

### 2. Inline-only pre-deepen research in auto-roadmap (no async)

- **Research gate logic** inside the RESUME-ROADMAP `action: deepen` branch of `.cursor/rules/context/auto-roadmap.mdc`:
  - Use the depth helper `current_depth = 1 + count('.') in current_subphase_index` from `workflow_state` frontmatter, matching [roadmap-deepen/SKILL.md](.cursor/skills/roadmap-deepen/SKILL.md).
  - Read `workflow_state.md` frontmatter (`last_ctx_util_pct`, `iterations_per_phase`) and, if needed, the last row of the first `## Log` table for `Ctx Util %` and any last-row confidence, following the util-based gate spec in `auto-roadmap.mdc` and [Parameters.md](3-Resources/Second-Brain/Parameters.md).
  - Compute `enable_research_from_util` using `research_util_threshold`, `research_conf_veto_threshold`, and `research_cooldown`, then combine with explicit `params.enable_research` and tag/keyword-based triggers (`#research-needed`, `research_auto_keywords`) to derive a final `effective_enable_research` flag. On any parse failure for util/conf, treat as “no util signal” (do not silently auto-enable).
- **Inline-only behavior (async dropped)**:
  - When `effective_enable_research === true`, always call `research-agent-run` **inline** with `project_id`, `linked_phase`, derived `queries`, and any low-util/gap hints.
  - On success, capture returned research note paths and summaries and pass them as `injected_research_paths` / `injected_research_summary` into `roadmap-deepen`.
  - On 0 results, low synthesis confidence, or very small synthesized content, rely on `research-agent-run` to log `#research-failed` or `#research-empty` in [Errors.md](3-Resources/Second-Brain/Errors.md) and proceed to `roadmap-deepen` **without** injected research.
- **Deprecate `async_research` at the gate**:
  - Accept `params.async_research` for backward compatibility but **ignore it** in auto-roadmap: always take the inline research branch when research is enabled; do not append RESEARCH-AGENT from deepen.

### 3. Integrate and shield research-agent-run outputs in roadmap-deepen

- **Honor roadmap-deepen SKILL contract** ([.cursor/skills/roadmap-deepen/SKILL.md](.cursor/skills/roadmap-deepen/SKILL.md)):
  - Use `params.injected_research_summary`, `params.injected_research_paths`, `params.gaps`, and `params.research_used` when present.
  - When injected research is provided, include a **Research summary** subsection in the deepen prompt context (summary text and/or wikilinks/paths) as part of the injected context block.
  - When `params.gaps` is present and research is enabled, call `research-agent-run` in `gap-fill` mode and inject `gap_fills` into the draft content before writing, observing `fill_conf` thresholds and inline injection rules.
- **Wire auto-roadmap ↔ roadmap-deepen parameters**:
  - After inline pre-deepen research, pass `injected_research_summary`, `injected_research_paths`, `gaps`, and `research_used` in `params` to `roadmap-deepen`.
  - Ensure `roadmap-deepen` writes `research_used` and a short gaps summary into the `## Log` row (e.g. in Status / Next) and updates `last_ctx_util_pct` frontmatter to the new Ctx Util %, so the next RESUME-ROADMAP run can use these values for gating.
- **Guard against stale `injected_research_paths`**:
  - When roadmap-deepen reads persisted `injected_research_paths` from `workflow_state` (used only for explicit RESEARCH-AGENT runs), if none of the referenced notes can be found, it must:
    - Clear the persisted paths,
    - Log a small Errors.md entry (e.g. `research-injected-paths-missing`) once for that run,
    - Proceed without research injection (no silent retries).

### 4. RESEARCH-AGENT queue mode as one-shot batch research (hardened)

- **Semantics after async removal**:
  - `mode: "RESEARCH-AGENT"` means: run `research-agent-run` now, write notes to `Ingest/Agent-Research/`, and queue INGEST MODE (and optionally DISTILL MODE when `research_distill: true`) for those notes.
  - It **does not** append RESUME-ROADMAP or advance deepen automatically; RESUME-ROADMAP deepen runs remain the only path that manipulates roadmap structure.
- **EAT-QUEUE dispatch** (per `.cursor/rules/context/auto-eat-queue.mdc`):
  - Resolve `project_id` and `linked_phase` from `source_file` or `params`.
  - Call `research-agent-run` with merged params (`research_tools`, `research_result_limit`, `research_max_tokens`, `low_util`, `gaps`, `origin`, etc.).
  - For each created research note path under `Ingest/Agent-Research/`, append follow-up `INGEST MODE` (and `DISTILL MODE` when requested) into the in-memory queue or queue file, respecting Step 8 re-read/merge semantics so newly appended entries are not lost.
  - On 0 results or low-confidence synthesis, treat the run as **empty/failure**: rely on `research-agent-run` error logging and record a `failure` Watcher-Result line rather than pretending success.
- **Docs alignment for RESEARCH-AGENT**:
  - Update [Queue-Sources.md](3-Resources/Second-Brain/Queue-Sources.md), [Parameters.md](3-Resources/Second-Brain/Parameters.md), [Pipelines.md](3-Resources/Second-Brain/Pipelines.md), and roadmap upgrade plans to remove or clearly mark as historical any text that says RESEARCH-AGENT will append a follow-up RESUME-ROADMAP with `injected_research_paths`.

### 5. Context-utilization, metrics postcondition, and shielding

- **Default-on context tracking at dispatch**:
  - Keep `auto-eat-queue`’s rule that, for RESUME-ROADMAP deepen entries without an explicit `enable_context_tracking: false`, sets `params.enable_context_tracking = true` before calling auto-roadmap so context metrics are always available to the research gate.
- **Strict metrics postcondition in auto-roadmap**:
  - After `roadmap-deepen` returns, re-read `workflow_state.md` and ensure the last `## Log` row has numeric Ctx Util %, Leftover %, Threshold, Est. Tokens / Window, and Util Delta % when `enable_context_tracking` is true.
  - Writing `"-"` into these tracked columns when `enable_context_tracking === true` is forbidden: treat this as a hard failure. In that case:
    - Create a `context-tracking-missing` entry in [Errors.md](3-Resources/Second-Brain/Errors.md),
    - Mark the RESUME-ROADMAP queue entry as `queue_failed: true`,
    - Add a `#review-needed` warning to roadmap-state instead of appending a new deepen.
- **Util-based research gating (no async)**:
  - Ensure the research gate reads only `last_ctx_util_pct` and the latest Log row metrics written by `roadmap-deepen`, and that util/conf thresholds only decide whether to run **inline** research before deepen; there is no alternate async path.

### 6. Ingest/distill interaction for `Ingest/Agent-Research` notes

- **Research note creation and schema**:
  - `research-agent-run` writes notes to `Ingest/Agent-Research/` with frontmatter including `research_query`, `linked_phase`, `project_id`, `created`, `tags: [research, agent-research]`, `research_tools_used`, and `agent-generated: true`, following [Vault-Layout.md](3-Resources/Second-Brain/Vault-Layout.md).
- **Ingest pipeline integration (no wrappers for agent notes)**:
  - Confirm that `Ingest/Agent-Research/`** is in scope for full-autonomous-ingest (no exclusions in rules or globs).
  - For notes tagged `agent-research`, Phase 1 ingest/distill steps (backup, classify_para, frontmatter-enrich, distill_note, `distill-highlight-color`, `next-action-extract`, etc.) run as usual.
  - Phase 2 apply-mode (move/rename) for `agent-research` notes is allowed **without Decision Wrappers**, but still gated by confidence thresholds and per-change snapshots per `mcp-obsidian-integration.mdc`.
  - Decide and document a canonical long-term location (e.g. `1-Projects/<project-id>/Research/Agent-Research/`) and have ingest/organize move these notes there under the above gates.
- **Distill idempotence markers**:
  - When an Agent-Research note completes a successful autonomous-distill pass, set a light marker (e.g. `research_distilled: true`) so:
    - RESEARCH-AGENT with `research_distill: true` doesn’t re-queue redundant distill,
    - BATCH-DISTILL can treat `research_distilled: true` as skip/low-priority.

### 7. Mode success contracts and observability

- **Mode-Success-Contracts alignment**:
  - For RESUME-ROADMAP (deepen): success now means:
    - Deepen completed with valid context metrics and, when research was enabled, **either**:
      - At least one Agent-Research note was written and considered (inline pre-deepen), **or**
      - A research-empty/failure event was logged in Errors.md / Watcher-Result.
  - For RESEARCH-AGENT: success means:
    - ≥1 `Ingest/Agent-Research` note written **and**
    - Corresponding INGEST (and optional DISTILL) queue entries created; otherwise, treat as failure/empty and log accordingly.
- **Logging discipline**:
  - Ensure Watcher-Result entries for both RESUME-ROADMAP deepen and RESEARCH-AGENT clearly state whether research ran, how many notes were created, and whether gap fills were injected, so there is no “did nothing but said success” scenario.

### 8. Commander, Prompt-Crafter, and Mobile consistency

- **Commander / Prompt-Crafter**:
  - Treat `async_research` as deprecated/no-op: do not offer it as a meaningful toggle in Commander flows or prompt-crafter question sets.
  - Ensure any “Queue Research: Phase” macro maps to **RESEARCH-AGENT one-shot** only (no implication of auto-deepen continuation).
- **Mobile-Pending-Actions and gap banners**:
  - When roadmap-deepen gap detection appends high-severity gap banners and `Mobile-Pending-Actions` entries, define clear resolution rules:
    - Consider a gap action “handled” when either gap-fill research has been injected (research_used true, gaps summary updated) or a subsequent deepen run reports `gaps: 0`.
    - After handling, banners and mobile entries should be updated/cleared so mobile users don’t see stale prompts.

### 9. Restore/rollback awareness

- **Snapshots and versions**:
  - Restoring roadmap notes from per-change snapshots or version files does **not** remove Agent-Research notes or undo their ingest/distill; it only rolls back roadmap narrative/structure.
  - Document that discrepancy (older roadmap content + existing research notes) is acceptable and visible through logs; no automatic cleanup should attempt to delete or re-ingest research notes on restore.

