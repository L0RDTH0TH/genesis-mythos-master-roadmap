---
name: roadmap-deepen
description: Performs one deepen step for multi-run roadmap — reads workflow_state and roadmap-state, computes next target (phase/subphase per Roadmap Structure), creates folder/note(s), updates workflow_state, appends RESUME-ROADMAP to queue when params.queue_next !== false (required unless explicitly false). Used when RESUME-ROADMAP runs with action "deepen" (default).
---

# roadmap-deepen

## When to use

- When **RESUME-ROADMAP** runs with **params.action: "deepen"** (default). Invoked by auto-roadmap after resolving project_id and reading state.
- One run = one deepen step: create the next level of hierarchy (e.g. first missing secondary under current phase, or next tertiary under current secondary) per [Roadmap Structure](Roadmap Structure.md).

## Inputs

- **project_id** (required): From auto-roadmap (queue payload, source_file, or user).
- **workflow_state path**: `1-Projects/<project_id>/Roadmap/workflow_state.md` (or caller passes resolved path).
- **roadmap-state path**: `1-Projects/<project_id>/Roadmap/roadmap-state.md`.
- **Timestamp / clock source:** Prefer **queue-provided time** so the Log reflects the user's local time when the agent runs in the cloud. Caller may pass **`queue_entry_timestamp`** (UTC ISO 8601 string from the queue entry's `timestamp`), **`local_timestamp`** (string, format `YYYY-MM-DD HH:MM` from the queue entry when present), and **`display_timezone`** (IANA name from Config, e.g. `America/New_York`). Resolve the Timestamp cell in order: (1) if **local_timestamp** is present and valid format (`YYYY-MM-DD HH:MM`, optionally `YYYY-MM-DD HH:MM:SS` trimmed to `HH:MM`) → use it; (2) else if **queue_entry_timestamp** and **display_timezone** are present → convert UTC to that zone (e.g. Python `zoneinfo.ZoneInfo`), format as `YYYY-MM-DD HH:MM`; on conversion failure log to Errors.md (`error_type: display_timezone_invalid` or `timestamp_conversion_failed`) and fall back to (3); (3) else use server "now" formatted as `YYYY-MM-DD HH:MM`. Do not fail the pipeline for timestamp resolution; invalid local_timestamp or display_timezone causes fallback only. See Parameters § Timestamp resolution and Queue-Sources § queue entry fields.
- **params.granularity** (optional): Override per-phase default (secondary-tertiary | tertiary-mid-technical | full-pseudo-code). When absent, use **current_depth** (from current_subphase_index) for content strictness — see Depth-based technical escalation below.
- **params.enable_context_tracking** (optional, bool): This field is expected to be the **effective** flag computed by auto-roadmap (default-on semantics): `true` when tracking should run for this deepen step, `false` only when a specific RESUME-ROADMAP entry explicitly set `enable_context_tracking: false`. The skill must **not** re-read `prompt_defaults.roadmap.enable_context_tracking` or introduce a second source of truth.  
  **Invariant (metrics + timing, when true):**
  - Compute numeric values for:
    - **Ctx Util %**
    - **Leftover %**
    - **Threshold**
    - **Est. Tokens / Window**
    - **Util Delta %** (difference from previous Ctx Util %, or from `last_ctx_util_pct` frontmatter when present).
    - **Confidence** (0–100): agent self-assessed confidence for this deepen iteration’s output (e.g. from self-critique or handoff-style assessment). When tracking is disabled or not computed, use `"-"`.
  - Return these values (and any iteration identifiers) to the caller so it can append a **single, atomic row** to `workflow_state ## Log` that also contains local **Start** / **Completion** timestamps and **Duration**.
  - If metric computation is impossible (e.g. missing workflow_state or required inputs), do **not** append a log row with `"-"` in tracked columns and do **not** advance workflow_state for this run; instead:
    - Surface an error to the caller (e.g. `error_type: context-tracking-missing` or `"context-metrics-failed"`),
    - Log to `3-Resources/Errors.md` with **#review-needed**,
    - Let auto-roadmap treat the run as failed and keep the queue entry with `queue_failed: true`.
  - This skill **MUST NOT** write `"-"` into the four context columns or Util Delta % when `enable_context_tracking == true`; `"-"` in those columns is reserved for the explicit opt-out path when tracking is disabled.
- **params.context_util_threshold** (optional, int %): Utilization % above which deepen should pause and queue RECAL-ROAD instead of another deepen. Defaults from Config `prompt_defaults.roadmap.context_util_threshold` (default **80**) when omitted.
- **params.context_token_per_char** (optional, float): Characters-to-tokens heuristic used when estimating context size; defaults from Config `prompt_defaults.roadmap.context_token_per_char` (default **0.25**, i.e. ~4 chars per token).
- **params.context_window_tokens** (optional, int): Assumed model context window size used as the denominator for utilization; defaults from Config `prompt_defaults.roadmap.context_window_tokens` (default **128000**).
- **params.inject_extra_state** (optional, bool): When **true**, pull and embed extra context (distilled-core, decisions-log tail, sibling summaries, and when phase ≥5 prior-phase folder batch) into the deepen prompt. Target 40–50% util. Default **40–50k tokens** cap; overridable via **params.token_cap** (e.g. `50000`).
- **params.token_cap** (optional, int): Max tokens for injected context block when `inject_extra_state` is true. Default **50000**. Truncation order if over cap: decisions-log tail first, then sibling summaries, then prior-phase content; keep distilled-core full when possible.
- **params.max_depth** (optional, int): Max depth to create in one deepen run (e.g. 4 or 5). When absent, derive from **current_phase**: phase 1–2 → 2, phase 3–4 → 3, phase 5–6 → 4. When set, loop step 5 until depth reaches max_depth or phase segment is complete; one Log row at end.
- **params.branch_factor** (optional, int): Target number of secondaries (or tertiaries per secondary) per node. **Default 4 for phases ≥ 3**. Create up to that many children at current level before moving deeper.
- **params.batch_subphases** (optional, array): e.g. `["3.2","3.3","3.4"]`. Run step 5 serially over each; one workflow_state update at end (one Log row, Target = comma-separated list). Snapshot before batch.
- **params.highlight_angles** (optional, array): e.g. `["narrative","tech","edge-cases"]`. After deepen, for each created/updated roadmap note run **distill-highlight-color** and **highlight-perspective-layer** with those angles. At 70% util, **layer-promote** prunes fade-level (⚪) content.
- **params.recal_util_high_threshold** (optional, int %): Default **70**. When context_util_pct ≥ this value, queue RECAL-ROAD instead of another deepen.
- **params.injected_research_summary** (optional, string): Short research summary block (1–2 sentences per note or combined) passed by auto-roadmap after pre-deepen research; include in Injected context so the model sees it when generating deepen content.
- **params.injected_research_paths** (optional, array of paths): Links to new notes in Ingest/Agent-Research/ created by research-agent-run; include in Injected context (e.g. as wikilinks or paths) when present.
- **params.gaps** (optional, array): From gap-detection step; each element: `id`, `heading`, `type`, `severity`, `excerpt`, `suggested_query_seed`. When present and research is enabled, caller (auto-roadmap) or this skill may invoke research-agent-run in gap-fill mode; this skill uses it when doing mid-deepen gap-fill (see step 4.5).
- **params.research_used** (optional, bool): Set to true when gap-fill research was run this deepen step; written to workflow_state log row for audit.
- **params.conceptual_decision_record_mode** (optional): Overrides Config **`roadmap.conceptual_decision_record_mode`**: **`off`** \| **`best_effort`** \| **`required`**.
- **params.queue_entry_id** (optional): Passed to **conceptual-decision-record** and decisions-log bullet when present.

## Return payload (to caller)

- **`queue_followups`** — per step 7 (when **`params.queue_next !== false`** and context gates allow).
- **`next_structural_target_hint`** — optional; **conceptual** track only; see **§6a**. RoadmapSubagent uses this for **Conceptual subphase exit** ([[3-Resources/Second-Brain/Parameters|Parameters]] § Conceptual subphase exit). When **`conceptual_deepen_cap_reached`** or **`stagnation_suspected`**, still return a hint; if the recomputed next pass would stay on the same slice, set **`same_slice_repeat: true`** but RoadmapSubagent **must** still derive **`params.next_subphase_index`** from Roadmap Structure / MOC order (hint may be stale).
- **`stagnation_suspected`** (bool) — **true** when **§77b** fires; else omit or **false**.
- **`stagnation_severity`** — **`none`** \| **`mild`** \| **`moderate`** \| **`chronic`** per **§77c** (control plane v2).
- **`stagnation_cluster_id`** — string or **`null`**; set when Config **`roadmap.control_plane_v2.stagnation_v2`** drives clustering (else **`null`**).
- **`conceptual_deepen_cap_reached`** (bool) — **true** when **§2.5** forced structural forward due to **`roadmap.conceptual_max_deepen_per_subphase`**; else omit or **false**.
- **`conceptual_decision_record`** — per step **6b** when applicable.

## Dual track (conceptual vs execution)

**Authority:** Read `1-Projects/<project_id>/Roadmap/roadmap-state.md` frontmatter **`roadmap_track`**. If absent → **`conceptual`**. Optional queue override **`params.roadmap_track`** (`conceptual` \| `execution`) may force the active track for **this run only** when the operator must temporarily target one tree (document in Log Status / Next).

| Track | Active workflow state | Active roadmap state | Phase tree root (list/create notes) | Shared context (inject_extra_state) |
|-------|----------------------|----------------------|-------------------------------------|-------------------------------------|
| **conceptual** | `Roadmap/workflow_state.md` | `Roadmap/roadmap-state.md` | `Roadmap/` (exclude `Roadmap/<execution_subfolder>/`) | `Roadmap/distilled-core.md`, `Roadmap/decisions-log.md` |
| **execution** | `Roadmap/<execution_subfolder>/workflow_state-execution.md` | `Roadmap/<execution_subfolder>/roadmap-state-execution.md` | `Roadmap/<execution_subfolder>/` | Same parent `Roadmap/distilled-core.md` and `decisions-log.md` unless execution-local copies exist |

**`execution_subfolder`:** from `prompt_defaults.roadmap.execution_subfolder` in Second-Brain-Config (default **`Execution`**).

**Bootstrap (execution track):** If `roadmap_track` is `execution` and `workflow_state-execution.md` or `roadmap-state-execution.md` is missing under `Roadmap/<execution_subfolder>/`, create them from **`Templates/Roadmap/Execution/`** (never overwrite existing).

**Frozen conceptual guard:** Before any destructive write to a path under `Roadmap/` that is **not** under `Roadmap/<execution_subfolder>/`, read target note frontmatter if the file exists; if **`frozen: true`** and **`roadmap_track: conceptual`**, **do not** write; log to Errors.md, #review-needed, return without advancing state.

**Pre-create gate (step 4):** Run **handoff-audit / confidence** gate before creating depth ≥4 children **on the execution track** as the primary “actual completion” gate. On **conceptual** track, **do not** apply the execution-only pre-create block (no Decision Wrapper **solely** for missing pseudo-code / technical depth-4 readiness); see [[3-Resources/Second-Brain/Docs/Control-Plane-Heuristics-v2|Control-Plane-Heuristics-v2]] §3.3. §2.5 cap-vs-gate conflicts still favor hard quality gates.

**New execution notes:** Set frontmatter **`roadmap_track: execution`**, **`conceptual_counterpart`** (wikilink to the mirrored conceptual note path when known), **`project-id`**, and mirror **`subphase-index`** / **`phase-number`** from the conceptual sibling when minting a counterpart.

## Diminishing returns (advisory)

When **`prompt_defaults.roadmap.diminishing_returns_advisory_enabled`** is true: after computing the new **Status / Next** text for the Log row, evaluate (conceptual **or** execution **active** workflow_state table):

1. Parse the last **`diminishing_returns_window_runs`** data rows (same table).
2. If **≥ `diminishing_returns_same_target_streak`** consecutive rows share the same **Target** cell (or same `current_subphase_index` in frontmatter across those runs), **and** **Confidence** values are numeric with max increase &lt; **`diminishing_returns_confidence_epsilon`** across those rows — **or** `iterations_per_phase[current_phase]` exceeds the **ceiling** of `iteration_guidance_ranges` for **current_depth** — append to **Status / Next**: `advisory: diminishing-returns-suspected (<short reason>)`.
3. Never block deepen solely on this advisory; do not auto-flip `roadmap_track`. Optional: one-line to Mobile-Pending-Actions per operator preference.

### §77b — Stagnation flag (structured return; anti-circle)

Read from [[3-Resources/Second-Brain-Config|Second-Brain-Config]] **`roadmap`** block: **`stagnation_window_runs`** (default **3** when absent), **`stagnation_confidence_delta_max_percent`** (default **5** when absent).

**After** step **6** appends the new **## Log** data row (so the window includes this run):

1. Parse the last **`stagnation_window_runs`** **data** rows of the first **`## Log`** table (exclude header + separator).
2. Require every row’s **Target** cell (fallback: **Iter Phase** if Target column missing) to match the same normalized subphase key (e.g. same `4.1.5` or same phase note slug — be consistent with **Iter Phase** / **`current_subphase_index`** for the active conceptual cursor).
3. Parse **Confidence** from each row (numeric **0–100**). If any row is non-numeric, skip stagnation (do not set the flag).
4. If **`max(Confidence) - min(Confidence) < stagnation_confidence_delta_max_percent`**, set **`stagnation_suspected: true`** on the **overall skill return** to RoadmapSubagent / caller.

This flag is **computed** in deepen; ValidatorSubagent **need not** emit a stagnation code. RoadmapSubagent uses it for slice-exit **(3d)** per [[3-Resources/Second-Brain/Parameters|Parameters]] § Conceptual subphase exit.

### §77c — `stagnation_severity` and `stagnation_cluster_id` (control plane v2)

Always set on the skill return (RoadmapSubagent forwards into **`control_plane_observability`** / **`queue_continuation`**):

1. If **`stagnation_suspected`** is **false** or unset: **`stagnation_severity: none`**, **`stagnation_cluster_id: null`**.
2. If **`stagnation_suspected`** is **true** **and** **`conceptual_deepen_cap_reached`** is **true**: **`stagnation_severity: chronic`**.
3. Else if **`stagnation_suspected`** is **true**: **`stagnation_severity: mild`** (upgrade to **`moderate`** when the same normalized subphase key appears in **≥ `cluster_repeat_threshold`** of the last **`cluster_window_m`** workflow_state Log data rows — read from Config **`roadmap.control_plane_v2.stagnation_v2`**; use defaults **3** / **8** when keys absent).
4. **`stagnation_cluster_id`:** When severity is **`moderate`** or **`chronic`**, set a short stable id e.g. `stag-<project_id>-<current_subphase_index>`; else **`null`**.

### §2.5 — Per-subphase deepen cap (conceptual)

Read **`roadmap.conceptual_max_deepen_per_subphase`** from Second-Brain-Config (**0** or absent = disabled).

**Immediately after** step **2** (paths + reads), **before** **§3.1** conceptual checklist branch:

1. If **`active_track !== conceptual`** or cap is **0**, skip (**`conceptual_deepen_cap_reached`** = false).
2. Else count **existing** data rows in the first **`## Log`** table whose **Iter Phase** cell (trimmed) equals **`current_subphase_index`** from **active** workflow_state frontmatter (string compare).
3. If **`count ≥ conceptual_max_deepen_per_subphase`**: set **`conceptual_deepen_cap_reached: true`** in run context.
4. When **true**, in **§3.1** do **not** enter **`refining_existing_conceptual_target: true`** from NL checklist gaps alone — treat the deepen step as **structural advance**: in **§3 — Compute next target**, prefer the **next sibling** / next structural node per Roadmap Structure (advance **`current_subphase_index`** toward the next MOC child or peer), and in **§5** update the **next** roadmap note / cursor rather than polishing the same slice. Append **`Status / Next`** cue e.g. `subphase_cap_exit: forward` for auditability.

If cap logic conflicts with a hard quality gate (e.g. parent confidence &lt; 75% in **§4**), the existing gate **wins** — log **`#review-needed`** and do not bypass **Decision Wrapper** exits.

## Depth from subphase-index

Derive **current_depth** from **current_subphase_index** (and use for both iteration guidance and content strictness):

- `"1"` or phase-only → depth 1 (high-level phase container)
- `"1.1"` → depth 2 (secondary)
- `"1.1.1"` → depth 3 (tertiary)
- `"1.1.1.1"` → depth 4 (quaternary) → pseudo-code territory
- Deeper (e.g. 1.1.1.1.1) → depth 5, 6, … N (quinary, senary, nth)

Use **iteration_guidance_ranges** from Config (prompt_defaults.roadmap) or workflow_state: **depth_1** … **depth_4_plus** (for depth ≥ 4 use depth_4_plus). These are **guidance only** — do not set status blocked solely because iteration count exceeds the range.

## Depth-based technical escalation

When generating or deepening content, enforce content strictness by **current_depth** (not phase number):

- **current_depth ≥ 4:** Add to context / user_guidance: *"Technical only: pseudo-code blocks, API signatures, edge cases, performance invariants."*
- **current_depth == 3:** Add: *"Mid-technical: interfaces + algorithm sketches."*
- **Depth 1–2:** High-level only (no pseudo-code requirement).

## Instructions

0. **Inject extra state (when params.inject_extra_state === true) and/or research (when params.injected_research_summary or params.injected_research_paths present):**
   - **Research injection (optional):** When caller passes **params.injected_research_summary** or **params.injected_research_paths** (from auto-roadmap after pre-deepen research), include a **Research summary** subsection in the context passed to the deepen prompt: summary text and/or wikilinks/paths to the research notes so the model sees research when generating the next deepen content. If **inject_extra_state** is false, build a minimal block containing only this Research subsection; if true, add it to the full Injected context block below. No change to workflow_state schema; prompt context only.
   - When **params.inject_extra_state === true**: Resolve **token_cap** from params (default **50000**). Read last Log row from workflow_state; if **last run Ctx Util % < 30%** (greedy mode), set effective cap = min(1.5 * token_cap, 0.4 * context_window_tokens).
   - Read **distilled-core.md** from **parent** `Roadmap/` (full). Read **decisions-log.md** (same) and take **last 5–10** bullet entries (tail). List siblings: `obsidian_list_notes` on the parent folder for current target under **active phase tree root** (execution or conceptual); **obsidian_read_note** for 1–2 sibling notes (prev/next by subphase-index); include first ~500 chars or "Summary" section per sibling.
   - **Phase-adaptive (current_phase ≥ 5):** `obsidian_list_notes` on **active root** `Phase-N-*/` for N = current_phase − 1 (and optionally −2); then **obsidian_read_note** batch on listed notes (or summaries). Respect token_cap; truncate prior-phase content if over cap.
   - Concatenate into an **Injected context** block; enforce cap by truncation order: decisions-log tail first, then sibling summaries, then prior-phase content; keep distilled-core full when possible. When **injected_research_summary** or **injected_research_paths** are present, include the Research summary subsection in this block. Pass this block into the deepen prompt/context.
   - **Token audit:** Estimate `injected_tokens = injected_chars * context_token_per_char`. Write to **active** workflow_state: frontmatter **last_injected_tokens** and/or append in Status/Next (e.g. `injected_tokens: 4200`). Document in Vault-Layout § workflow_state.
   - **Drift postcondition:** After the run, if **drift > 0.08** (from roadmap-audit or state), fail postcondition: log to Errors.md with #review-needed and queue RECAL-ROAD; do not treat as success.

1. **Resolve paths**: `roadmapDir = "1-Projects/<project_id>/Roadmap/"`. Read **`roadmap-state.md`** at `roadmapDir`. Set **active_track** = `params.roadmap_track` if present, else frontmatter **`roadmap_track`** (default **`conceptual`**). Set **execution_subfolder** from Config (`prompt_defaults.roadmap.execution_subfolder`, default `Execution`). **phaseTreeRoot** = `roadmapDir + execution_subfolder + "/"` when **active_track** is **`execution`**, else **`roadmapDir`**. **active_workflow_state** = `phaseTreeRoot + "workflow_state-execution.md"` when execution, else `roadmapDir + "workflow_state.md"`. **active_roadmap_state** = `phaseTreeRoot + "roadmap-state-execution.md"` when execution, else `roadmapDir + "roadmap-state.md"`. Read **active_workflow_state** and **active_roadmap_state** (and use Injected context from step 0 when inject_extra_state is true).

1b. **Bootstrap missing roadmap artifacts (template-backed)**

Before reading/using any roadmap artifacts, ensure these files exist under `roadmapDir` (create **only when missing**, never overwrite existing):

- `roadmap-state.md` (create from `Templates/Roadmap/Artifacts/roadmap-state.md`; fill `{{project_id}}`, `{{source_master_goal}}` if known)
- `workflow_state.md` (create from `Templates/Roadmap/Artifacts/workflow_state.md`; fill `{{project_id}}`; preserve the canonical `## Log` header + separator row)
- `decisions-log.md` (create from `Templates/Roadmap/Artifacts/decisions-log.md`; fill `{{project_id}}`)
- `distilled-core.md` (create from `Templates/Roadmap/Artifacts/distilled-core.md`; fill `{{project_id}}` and the four Phase 0 anchor links: master goal, roadmap-state, workflow_state, decisions-log)

When **active_track** is **`execution`**, also ensure under **`roadmapDir + execution_subfolder + "/"`** (create **only when missing**):

- `workflow_state-execution.md` from `Templates/Roadmap/Execution/workflow_state-execution.md`
- `roadmap-state-execution.md` from `Templates/Roadmap/Execution/roadmap-state-execution.md`

Call **obsidian_ensure_structure** with `folder_path` = parent of the execution folder as needed.

**Invariant:** If the **active** workflow_state file exists but is missing the mandatory `## Log` table separator row, treat as a structural defect (log to Errors.md with #review-needed) and do not proceed with a deepen write until it is repaired (this prevents appending rows into a non-table).

2. **Snapshot before any write**: Per [mcp-obsidian-integration](.cursor/rules/always/mcp-obsidian-integration.mdc), call **obsidian-snapshot** (obsidian-snapshot skill, type per-change) for **active_roadmap_state** and **active_workflow_state** (and conceptual `roadmap-state.md` when execution track if you will mutate cross-track references) before creating or updating any note or state file. No structural write without prior snapshot.

3. **Compute next target**: From **active** workflow_state frontmatter: `current_phase`, `current_subphase_index`. From **active** roadmap-state and folder layout under **`phaseTreeRoot`** `Phase-N-<Name>/`, determine:
   - First missing secondary (e.g. Phase-1-1-… folder and Phase-1-1-…-Roadmap-*.md) for current_phase, or
   - Next tertiary under current secondary (e.g. Phase-1-1-1-<Name>.md), or
   - Next phase if current phase is fully deepened (per granularity for that phase).
   - Use [Roadmap Structure](Roadmap Structure.md) path patterns and frontmatter: `roadmap-level` (primary | secondary | tertiary | task), `phase-number`, `subphase-index` (e.g. "1.1", "1.1.1").

  3.1 **Conceptual NL checklist prioritization (refine current node first)**:
  - When **`active_track === conceptual`**, before selecting a *next* missing child node, resolve the existing roadmap note that corresponds to **the current cursor** (**`current_phase`** and **`current_subphase_index`**).
  - Run **conceptual-checklist gap detection** against that *existing* note content using the checklist requirements in **`Conceptual-Execution-Handoff-Checklist.md`** (Scope, Behavior, Interfaces, Edge cases, Open questions, Pseudo-code readiness).
  - If any checklist row is missing or underfilled (word-count < `gap_min_words` and no explicit “none/empty/TBD with contract” phrasing), set an in-run flag in context such as `refining_existing_conceptual_target: true` and treat the **next target** as the same `current_subphase_index` note (i.e. refine in place) instead of creating deeper children.
  - Only advance `current_subphase_index` after the conceptual-checklist gaps for that resolved note are resolved in the refine draft.

4. **Pre-create quality gate (when current_depth ≥ 4):** Before creating a new subphase note at depth ≥ 4:
   - **When `active_track` is `execution`:** Run a quick **handoff-audit** (or equivalent confidence check) on the **parent** secondary/tertiary note (confidence on "technical completeness"). Treat this gate as the primary blocker for minting depth-4+ children until confidence ≥ 75%. If **confidence < 75%**: do **not** create the new subphase. Instead, create a **Decision Wrapper** under `Ingest/Decisions/Roadmap-Decisions/` with **rationale callout** (e.g. `> Architect: Parent 1.2.3 technical completeness 72%; below 75% gate. Wrapper time.`) and options: **A:** Create anyway | **B:** Refine parent first | **C:** Skip to next secondary. Ensure folder (obsidian_ensure_structure for Ingest/Decisions/Roadmap-Decisions/); append CHECK_WRAPPERS and Watcher-Result; exit. If **confidence ≥ 75%**: proceed to step 4.5.
   - **When `active_track` is `conceptual`:** **Skip** this pre-create wrapper gate (proceed to step 4.5). Conceptual deepening uses §3.1 NL checklist and caps; execution-only pseudo-code pre-create does not apply. Log optional `Status / Next` cue `pre_create_gate: skipped_conceptual_track` when useful for audit.

4.5. **Gap analysis and optional gap-fill research (before final write)**  
   - **Hook location**: After the draft content for the new roadmap note(s) is prepared (the in-memory or assembled draft for the target phase/subphase) and **before** step 5 writes the note(s) to the vault. No snapshot or append has occurred yet.
   - **Gap detection**: Run the **gap detection** helper (see [Gap detection design](#gap-detection-design) below or Parameters `gap_min_words`, `research_gap_markers`, `gap_severity_threshold`): walk headings/sections in the draft; flag gaps (e.g. section body word count &lt; gap_min_words, or heading matches markers like "pseudo-code"/"edges"/"examples" with no matching content). Produce a **gaps** array: each element has `id`, `heading`, `type`, `severity`, `excerpt`, `suggested_query_seed`. Store in run context for step 5 and step 6.
   - **Research trigger (depth-aware)**: When **high-severity gaps** exist (severity ≥ gap_severity_threshold), the **caller has enabled research** for this run (params from auto-roadmap: enable_research, util/conf gates already evaluated there), **and `current_depth ≥ 2`** (secondary or deeper; no external gap-fill for primary phase containers): **Before** calling research-agent-run, ensure **project_id** and **linked_phase** are both present (linked_phase = current deepen target — e.g. phase note path or stable id like `Phase-1-1-2` from the target being deepened). **If either is missing**, do **not** call research-agent-run for gap-fill; append to **Errors.md** one entry per [Logs.md § Research error entry format](3-Resources/Second-Brain/Logs.md) with **#research-skipped**, pipeline `roadmap-deepen`, reason e.g. `gap-fill: linked_phase or project_id missing`; then proceed to step 5 (write) without gap_fills. When both are present, call **research-agent-run** with `params.gaps` set to the detected gaps, `origin: "roadmap-deepen"`, **project_id**, and **linked_phase**. Respect `max_gap_fills_per_run` and per-gap token cap. On return, receive **gap_fills** (each: `gap_id`, `filled_markdown`, `sources`, `fill_conf`). Inject each fill into the **draft** (see [Inline injection rules](#inline-injection-rules) below) before step 5 writes. Set **research_used = true** in context. **If research-agent-run returns empty or partial gap_fills** (or throws): **roadmap-deepen** (caller) **MUST** append to Errors.md per Research error entry format (#research-empty or #research-failed, pipeline `roadmap-deepen` or `research-agent-run`, linked_phase, project_id) when the skill did not already log; inject only available fills (fill_conf ≥68%); **proceed to step 5 regardless** — do not block the deepen step.
   - **Check persisted injected_research_paths**: On **any** RESUME-ROADMAP run, **before** running deepen content generation, check workflow_state frontmatter (or Roadmap/research-pending state note) for **injected_research_paths** keyed by project_id + current_phase (and optionally current_subphase_index). These persisted paths are intended for explicit RESEARCH-AGENT runs only, not for an async deepen loop. If present, load those paths into context (injected_research_summary or injected_research_paths) and **clear** the persisted state so the next run does not re-use them. When none of the referenced notes can be found, clear the state and log a small entry (e.g. `research-injected-paths-missing`) instead of silently retrying.
   - **Auto-signal when high-severity gaps found**: When **high-severity gaps** are detected (severity ≥ gap_severity_threshold), **before** or **after** step 5 (and regardless of whether gap-fill research runs this run): (1) **Append a banner/callout** to the **phase note** (the note being deepened or its parent phase note): e.g. `> [!warning] High-severity gaps detected (N). Run "Queue Research: Gaps" or resume deepen to fill.` (2) **Append an entry to Mobile-Pending-Actions** (path per Queue-Sources, e.g. `3-Resources/Mobile-Pending-Actions.md`) with a one-liner and link to the phase note, and optional `project_id`/`linked_phase` so the user (and Commander macro "Show pending gap research") can surface it. This keeps mobile/laptop users prompted when research or approval is needed.
   - **State wiring**: The deepen run context must carry **gaps** (array) and **research_used** (boolean). Step 6 uses these when appending the Log row and when writing workflow_state frontmatter.

5. **Create folder(s) and note(s)**:
   - When **params.batch_subphases** is set (e.g. `["3.2","3.3","3.4"]`), run this step **serially** for each subphase in the batch; one **active** workflow_state update and one Log row at end (Target = comma-separated list). Snapshot before the batch.
   - When **params.max_depth** or **params.branch_factor** is set: create up to **branch_factor** children at the current level (default 4 for phases ≥3), then recurse depth until **max_depth** (or phase-derived: 1–2→2, 3–4→3, 5–6→4). One snapshot before the multi-step run; one Log row at end.
   - Use **obsidian_ensure_structure** for the target phase folder under **phaseTreeRoot** (e.g. `…/Phase-N-<Name>/Phase-N-M-<SecondaryName>/` with prefix **phaseTreeRoot**).
   - Create the roadmap note at the path per Roadmap Structure **under phaseTreeRoot** (e.g. `Phase-N-M-<SecondaryName>-Roadmap-YYYY-MM-DD-HHMM.md` with frontmatter `roadmap-level: secondary`, `phase-number: N`, `subphase-index: "N.M"`). When **active_track** is **`execution`**, add **`roadmap_track: execution`** and **`conceptual_counterpart`** pointing at the parallel conceptual path (derive from mirrored folder path under `Roadmap/` without `Execution/` when minting a mirror).

  - **Conceptual checklist completeness scaffolding (refine mode aware)**:
    - When **`active_track === conceptual`**, ensure the deepened/updated roadmap note (the resolved target note from step 3) includes the NL handoff checklist headings/sections needed by **`Conceptual-Execution-Handoff-Checklist.md`**:
      - one **Scope** paragraph stating what the slice covers and explicitly what it does not cover
      - NL **Behavior** (actors, inputs, outputs, ordering)
      - **Interfaces** (expectations from adjacent slices + outward guarantees)
      - **Edge cases** (failure modes; deferrals labeled TBD if intentional)
      - **Open questions** (remaining ambiguities listed OR explicitly “none” / “empty”)
      - **Pseudo-code readiness** (reader can start sketching without guessing core behavior)
    - If this run is in `refining_existing_conceptual_target` mode, preferentially fill missing/underfilled sections in the existing note rather than only creating deeper children.
    - In this refine mode, use `obsidian_update_note` against the existing resolved target note path (do not mint new child notes) and do not advance `current_subphase_index` in the workflow log until the conceptual-checklist gaps are resolved.
   - **Frozen guard:** If the derived conceptual path would be written (should not occur on execution track), or when on conceptual track the target already exists with `frozen: true`, **abort** the write per Dual track section.
   - **When the created note is a secondary roadmap** (path matches `Phase-N-M-<Name>-Roadmap-*.md`, subphase-index "N.M"): after writing the note, **append** to it a section **"## Tertiary notes"** and a Dataview block FROM that secondary folder with **Level column**: `TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"` with `WHERE roadmap-level = "secondary" OR roadmap-level = "tertiary" OR roadmap-level = "task"`, `SORT subphase-index ASC, file.name ASC`. So every new secondary is created as the bottom MOC (per Roadmap Structure and MOC migration plan).
   - For tertiary notes: create note with tasks in body; frontmatter `roadmap-level: tertiary`, `subphase-index: "N.M.K"`.
   - For **depth-4 (quaternary) task files**: create as separate .md in the same secondary folder. Frontmatter MUST include **roadmap-level: task** (or leaf-task), **subphase-index** with task suffix (e.g. `"1.3.4.1"`), inherited **phase-number**, **project-id**. Each depth-4 note MUST contain an **upward link to parent** tertiary or secondary note (e.g. in frontmatter `links` or in body). Content: pseudo-code/API/edge cases per depth-based technical escalation.
   - Content depth follows **current_depth** (depth-based technical escalation): depth ≥ 4 → pseudo-code/API/edge cases; depth 3 → interfaces + algorithm sketches; depth 1–2 → high-level only. Override via params.granularity when present.
   - **Optional (drift/recal):** After a batch of depth-4 creations, if `iterations_per_phase[current_phase]` exceeds a threshold (e.g. 15 or from Config), append a queue entry for **RESUME-ROADMAP** with **params.action: "recal"** so RECAL-ROAD runs and handoff_drift is refreshed.
   - **Highlight angles (when params.highlight_angles set):** After creating/updating roadmap notes, for each such note run **distill-highlight-color** and **highlight-perspective-layer** with **params.highlight_angles** (e.g. `["narrative","tech","edge-cases"]`). If **context_util_pct ≥ 70%** after the highlight pass, run **layer-promote** to **prune fade-level (⚪) content** automatically; log in **active** workflow_state.

**Before appending the log row** (pre-write gate): When **params.enable_context_tracking === true**: (1) You **MUST** compute: `estimated_tokens` (sum character counts of: the assembled deepen prompt, **active** workflow_state and roadmap-state file bodies, `Roadmap/distilled-core.md`, and any phase/secondary/tertiary notes read this iteration; multiply by `context_token_per_char`), then `context_util_pct`, `leftover_pct`, `context_util_threshold`, and Util Delta % (from previous row or `last_ctx_util_pct` frontmatter). (2) If you have **not** performed this computation, do **not** append the row; do **not** advance **active** workflow_state. Return a clear error to the caller (e.g. `context-metrics-failed` or `context-tracking-missing`) and surface it (Errors.md, #review-needed) so auto-roadmap can mark the run failed. (3) When you append the row, use the **computed numeric values** in the four context columns and Util Delta %; writing `"-"` in those columns when tracking is true is **forbidden**. When **params.enable_context_tracking === false**: writing `"-"` in those columns is allowed. If unsure how to compute character counts, list the sources and estimate; the key is to never write `"-"` in the tracked columns when tracking is enabled. (4) Merge **Diminishing returns (advisory)** text into **Status / Next** when Config flags match.

6. **Update workflow_state**:
   - **Canonical table:** Append the new row only to the **first** `## Log` table in **active_workflow_state** (the one that immediately follows the first YAML frontmatter block). Do not append to any other ## Log section if present.
   - **Table format (Markdown):** The ## Log table must remain valid Markdown. **Preserve the separator row** when updating: if the file has a line `| --- | --- | --- | ... |` (12 cells) immediately after the header, keep it. If it is missing (e.g. legacy or broken file), add it so the table has (1) header row, (2) separator row, (3) data rows. See [Vault-Layout § workflow_state ## Log table format (Markdown)](3-Resources/Second-Brain/Vault-Layout.md).
   - **Append position:** New rows are **appended only at the end** of the table (after the last existing data row). Do not insert the new row between header and first data row or in the middle of existing rows. Use search_replace that targets after the last pipe-delimited line in the first `## Log` block, or reconstruct the table as: header + separator + existing data rows in order + new row.
   - **Example (full table with header + separator + one data row):**
     ```
     | Timestamp | Action | Target | Iter Obj | Iter Phase | Ctx Util % | Leftover % | Threshold | Est. Tokens / Window | Util Delta % | Confidence | Status / Next |
     | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
     | 2026-03-11 21:44 | deepen | Phase-1-1-Key-Abstractions | 1 | 1 | 5 | 95 | 80 | 6400 / 128000 | - | 85 | next deepen |
     ```
   - **Timestamp cell (resolution):** Resolve the value for the **Timestamp** column (or Start Local / Completion Local for extended schema) using the inputs above: (1) **local_timestamp** when present and valid (format `YYYY-MM-DD HH:MM` or `YYYY-MM-DD HH:MM:SS` trimmed to `YYYY-MM-DD HH:MM`); if invalid (wrong format or garbage), optionally log `timestamp-resolution | local_timestamp invalid, using fallback | entry_id: <id>` to Errors.md and fall through. (2) **queue_entry_timestamp** + **display_timezone**: convert UTC to that IANA zone and format as `YYYY-MM-DD HH:MM`; if conversion throws (e.g. unknown IANA name), catch, log to Errors.md with `error_type: display_timezone_invalid`, `display_timezone: <value>`, and #review-needed; use server time for this row. (3) **Server time:** format server "now" as `YYYY-MM-DD HH:MM`. Do not fail the deepen run for timestamp resolution; fallback only. See Parameters § Timestamp resolution.
   - Ensure workflow_state frontmatter includes **chained_branch_count** (int, default 0); reset to 0 when phase advances or RECAL-ROAD runs; increment when a branch-expand is queued (see step 7).
   - **Write last_ctx_util_pct and last_conf** to workflow_state **frontmatter** after appending the new Log row: set **last_ctx_util_pct** to the Ctx Util % value just written for this row (or "-" when tracking disabled). Set **last_conf** to the **Confidence** value just written for this row (0–100 when present, or "-" when tracking disabled or not computed). This allows auto-roadmap to read util and confidence (for util-based research and quality veto) without parsing the table.
   - When **gaps** were detected in step 4.5, append a short **gaps** summary to the new Log row (e.g. in **Status / Next** or a 12th column if schema extended): e.g. `gaps: 2 (examples, pseudocode)` or `gaps: 0`. When **research_used** is true, include that in the same cell or Status / Next (e.g. `research_used; gaps filled: 2`).
   - Increment `iterations_per_phase[current_phase]` (or set to 1 if key missing).
   - Set `current_subphase_index` to the new target (e.g. "1.1" or "1.1.1").
   - Compute **Util Delta %**: current Ctx Util % − previous row Ctx Util % (from last Log row); if no previous row or previous was "-", use "-" or 0. For new implementations, the recommended schema for each appended row in `## Log` is a **single, extended table** with at least: `Iteration ID | Start Local | Completion Local | Duration sec | Action | Target | Iter Obj | Iter Phase | Ctx Util % | Leftover % | Threshold | Est. Tokens / Window | Util Delta % | Confidence | Status / Next`. Include **Confidence** (0–100 or "-") so auto-roadmap can apply the research quality veto from the last row. **Start Local** is the local timestamp when this deepen iteration started, **Completion Local** is the local timestamp when it completed, and **Duration sec** is `(Completion − Start)` in seconds (computed by the caller just before appending). Existing 10/11-column logs remain valid; the next successful deepen run may extend the header and start writing the richer rows (including **Confidence**). When tracking is disabled for a given run, the four context-related columns, Util Delta %, and Confidence should be written as `"-"`, but Start / Completion / Duration should still be populated.
   - **Util-delta alerting (util_delta > 15%):** If **util_delta > 15%** (and numeric): (1) Append to **3-Resources/Errors.md** one line: `util-spike-detected | delta: {delta}% | util: {util}% | phase: {target}` (with actual values; include timestamp if desired). (2) Add **#review-needed** callout to the **phase note** (e.g. roadmap-state.md or current phase roadmap note). Document in Error Handling Protocol.
   - Use obsidian_update_note or equivalent; do not overwrite existing Log rows.
   - Optionally append to **deepen_log** in workflow_state frontmatter (if schema supports): `{ timestamp, depth, reason, parent, confidence_pre }` for audit trail.
   - **Run-Telemetry:** After updating workflow_state, ensure `.technical/Run-Telemetry/` exists (obsidian_ensure_structure or create on first write), then write one note to `.technical/Run-Telemetry/`. **Required fields:** actor: roadmap; project_id, queue_entry_id, timestamp, parent_run_id from the hand-off (if hand-off omits any, use queue entry in context or caller-provided values). **Optional (when available):** estimated_tokens, context_window_tokens, util_pct (from context_util_pct just written), chain_segment (from hand-off or params), workflow_state_link (wikilink to workflow_state ## Log or last row), tool_calls (e.g. counts of obsidian_read_note, obsidian_update_note), internals (confidence, duration_sec, freeform). **Phase 2 (cost):** When a rate table exists (e.g. [Telemetry-Model-Rates](3-Resources/Second-Brain/Telemetry-Model-Rates.md) or Config), set input_tokens = estimated_tokens, output_tokens = 0 or a rough completion estimate, total_tokens, and cost_estimate_usd from the rate table; write these to the Run-Telemetry note. No new computation — reuse existing workflow_state/context numbers. Naming: `Run-YYYYMMDD-HHMMSS-<project_id>-roadmap.md`. See [Logs § Run-Telemetry](3-Resources/Second-Brain/Logs.md) and [Vault-Layout § .technical/Run-Telemetry](3-Resources/Second-Brain/Vault-Layout.md).

6a. **`next_structural_target_hint` (conceptual only):** When **`active_track === conceptual`** and step **6** successfully appended the Log row and updated **`current_subphase_index`**, re-apply **step 3 — Compute next target** **once** using the **updated** **active** workflow_state / roadmap-state (as if starting the **next** deepen run). **Return** in the skill payload **`next_structural_target_hint`**: `{ subphase_index: string, refining_existing_conceptual_target: boolean, same_slice_repeat: boolean }`. Set **`same_slice_repeat: true`** when the recomputed next target would keep working on the **same** `subphase_index` as the post-step-6 cursor (refine-in-place / checklist loop). **Omit** this object when **`active_track !== conceptual`** or step 6 did not complete.

6b. **Conceptual decision record (conceptual track only):** After step 6 succeeds and roadmap note(s) were created/updated in step 5 (not when deepen aborted early, frozen guard, or Decision Wrapper exit). When **`active_track === conceptual`**:
   - Resolve **effective_mode** = `params.conceptual_decision_record_mode` if present, else **`roadmap.conceptual_decision_record_mode`** from [[3-Resources/Second-Brain-Config|Second-Brain-Config]], else **`best_effort`**. If **`off`**, skip this step.
   - Run **[conceptual-decision-record](.cursor/skills/conceptual-decision-record/SKILL.md)**:
     - **parent_roadmap_note:** path to the primary new or updated roadmap note from this iteration (the main deepen artifact; prefer the deepest-created note path).
     - **master_goal:** from `roadmap-state.md` body (`Source master goal:`) or `distilled-core.md` § Phase 0 anchors.
     - **chosen_summary** / **pmg_alignment** / **alternatives:** from this iteration’s reasoning (Architect voice—what was added, 1–2 plausible alternatives and why this path fits the PMG).
     - **evidence_links:** include **`params.injected_research_paths`** / **`injected_research_summary`** when present; set **`validation_status`** to **`cited`** when research notes exist, else **`pattern_only`** or **`needs_human`**.
     - **queue_entry_id:** from **`params.queue_entry_id`** or hand-off when available.
   - On success: append one bullet under **`1-Projects/<project_id>/Roadmap/decisions-log.md` → `## Conceptual autopilot`** (create the section after `## Decisions` if missing):  
     `- **Decision record (deepen):** [[Conceptual-Decision-Records/<basename>]] — queue_entry_id: <id> — validation: <cited|pattern_only|needs_human>`  
     Use **`obsidian_read_note`** + **`obsidian_update_note`** (append); snapshot **decisions-log.md** per MCP safety before append when policy requires.
   - **`best_effort`:** If record creation or decisions-log append fails, log to **Errors.md** (`error_type: conceptual-decision-record-failed`); **do not** roll back deepen; return **`conceptual_decision_record: { path: null, created: false, error }`** in the skill return payload.
   - **`required`:** If record creation fails, return **`conceptual_decision_record_failed: true`** to the caller; RoadmapSubagent **must** treat the deepen run as **failed** (same severity as context-tracking-missing for that policy).
   - Return on success **`conceptual_decision_record: { path: "<vault path>", created: true, validation_status: "<...>" }`** for RoadmapSubagent / Run-Telemetry optional fields.

7. **Iteration guidance, hard caps, and context-utilization gate**:
   - Read **iteration_guidance_ranges** from Config (prompt_defaults.roadmap) or workflow_state: depth_1 … depth_4_plus. Select range by **current_depth** (depth ≥ 4 → depth_4_plus).
   - Compute **iteration_band**: if `iterations_per_phase[current_phase]` is within the range [min, max] for that depth → **within_range**; else → **above_range**. Log iteration_band and current_depth (see step 6). When **above_range**, optionally set **above_guidance: true** in workflow_state frontmatter and/or suggest in the log "Consider recal or advance phase"; leave the actual choice to smart dispatch (RESUME-ROADMAP with no action).
   - **Hard ceiling:** When Config or workflow_state has **max_iterations_per_phase** set (default **80** from `prompt_defaults.roadmap.max_iterations_per_phase`) and `iterations_per_phase[current_phase] ≥ max_iterations_per_phase`, set workflow_state **status** to **blocked** and do **not** append another deepen. Smart dispatch or a follow-up RESUME-ROADMAP run may then choose **recal**, **advance-phase**, or another action.
   - **Context-utilization gate (when tracking enabled):**
     - If `enable_context_tracking` (from **params**, already merged and defaulted by auto-roadmap) is **true**, estimate processing context size for this deepen run by summing character counts for: the assembled deepen prompt, **active** workflow_state and roadmap-state paths, `Roadmap/distilled-core.md`, and any phase/secondary/tertiary notes read this iteration. Compute:
       - `estimated_tokens = total_chars * context_token_per_char` (from params or Config).
       - `context_util_pct = min(100, round(100 * estimated_tokens / context_window_tokens))`.
       - `leftover_pct = 100 - context_util_pct`.
     - Write `context_util_pct`, `leftover_pct`, `context_util_threshold`, and `"<estimated_tokens> / <context_window_tokens>"` into the **Ctx Util %**, **Leftover %**, **Threshold**, and **Est. Tokens / Window** columns for the new log row (see step 6). When tracking is disabled, these four columns should be `"-"`.
     - **Overflow check:** If **estimated_tokens > context_window_tokens × 0.9**, fail: log to 3-Resources/Errors.md with `error_type: context-overflow`, #review-needed, queue RECAL-ROAD.
     - **High-util RECAL gate:** Read **recal_util_high_threshold** from params or Config (default **70%**). If `context_util_pct ≥ recal_util_high_threshold` or `context_util_pct > context_util_threshold`: do not request another deepen follow-up. Instead:
       - Return a **follow-up request** to the caller (RoadmapSubagent / Queue/Dispatcher) for a single **RECAL-ROAD** entry (alias of RESUME-ROADMAP with `params.action: "recal"`), including `reason: "high-context-utilization"` and `util_percent: <context_util_pct>`, along with the usual project identifiers (`source_file` or `project_id`).
       - Update the new log row’s **Status / Next** column to something like `RECAL-ROAD queued (paused-high-util)` and, optionally, set workflow_state frontmatter `status` to `blocked` with a short note.
       - Append a warning callout to the roadmap log (or Ingest-Log) such as: `> [!warning] High context pressure detected (82% / 80% threshold) — RECAL-ROAD queued to distill before further deepening`.
       - Then **return without requesting a deepen** follow-up.
   - **Branch-expand follow-up (util < 50%):** If **context_util_pct < 50%** and **chained_branch_count < 2**: increment `chained_branch_count` in workflow_state; append RESUME-ROADMAP with **params.action: "expand"** targeting new tertiaries created this run. If **chained_branch_count ≥ 2**, fall back to RECAL-ROAD instead. Reset chained_branch_count to 0 when phase advances or RECAL runs.
   - **Required: Request next step (when under caps and below context threshold):** When **params.queue_next !== false** (absent or undefined = true), the follow-up request is **required**, not optional. Only when **params.queue_next === false** (explicitly set) must the pipeline suppress follow-up.
     - This skill **does not** write `.technical/prompt-queue.jsonl`.
     - Instead it returns a `queue_followups` payload to its caller with one of:
       - `next_entry`: `{ mode: "RESUME_ROADMAP", params: <sticky identity params only>, source_file? }`, or
       - `next_entry` for RECAL-ROAD (`mode: "RESUME_ROADMAP", params: { action: "recal", ... }`) when a gate requires recal, or
       - `suppress_next: true` when `queue_next === false` or a hard ceiling blocks further deepen.
     - Identity/sticky params to forward: **project_id** or **source_file**, **profile** (if present), effective **enable_context_tracking**, **queue_next**, and other crafter-locked/static params. Do **not** sticky-write dynamic per-iteration knobs (token_cap, research_* budgets, branch_factor, max_depth, etc.).
     - Include **`next_structural_target_hint`** from **§6a** in the **overall** skill return to RoadmapSubagent (alongside **`queue_followups`**) when computed.

8. **Optional hand-off context**: When auto-roadmap passes **handoff_gate** or **focus: handoff-readiness**, caller may run **roadmap-resume** first for hand-off context, then call this skill. This skill does not run hand-off-audit; it only deepens structure and updates workflow_state.

## Gap detection design

- **Input**: The draft note content (markdown) for the target phase/subphase before it is written. **Mode**: Read **gap_detection_mode** from Parameters (default **heuristic**); reserve **semantic** for a future optional pass (LLM/embedding completeness check).
- **Word-count threshold**: For each section (between two headings or heading and end), count words in the body. If **word count &lt; gap_min_words** (Parameters, default **30**), flag a **gap** of type **thin_explanation** (or infer type from heading; see below).
- **Marker-based detection**: For each heading, check if it contains any of **research_gap_markers** (Parameters, array; default `["pseudo-code", "edges", "examples", "TODO"]`). If it does, check the section body: if there is **no** code fence (```), no bullet list with ≥2 items, and body word count &lt; **gap_min_words** (or &lt; 50 for "examples"/"edges"), flag a gap. **gap_type** from heading: "pseudo-code" → **missing_pseudocode**, "edges" → **missing_edges**, "examples" → **missing_examples**, "TODO" or generic → **thin_explanation**.
  - When **active_track === conceptual**, also treat Conceptual-Execution-Handoff-Checklist row headings as marker headings even if they are not present in `research_gap_markers`:
    - `Pseudo-code readiness` → **missing_pseudocode**
    - `Edge cases` → **missing_edges**
    - `Scope`, `Behavior`, `Interfaces`, `Open questions` → **thin_explanation**
  - For `Open questions`, if the section explicitly declares “none”, “empty”, or an intentional TBD with a contract sentence (e.g. “deferred until X on execution track”), treat it as done for gap purposes.
- **Severity scoring (0–100)**:
  - Base from word count: e.g. `max(0, 100 - (word_count * 2))` so 0 words → 100, 50 words → 0 (tune so &lt; gap_min_words gives high severity).
  - Boost +15 if heading matches a **research_gap_marker** (promised but missing content).
  - Boost by **phase/depth**: e.g. +5 per depth level beyond 2 (depth 3 → +5, depth 4 → +10), or +10 when current_phase ≥ 4 (technical ramp). Cap at 100.
- **Thresholds**: **gap_severity_threshold** (default **60**): gaps with severity ≥ this trigger outward research. **gap_soft_floor** (default **40**): gaps with severity between soft_floor and threshold are logged only (workflow_state gaps summary) but do not trigger research.
- **Output**: **gaps** array; each element: `id` (unique, e.g. `gap_1`), `heading`, `type` (missing_examples | missing_pseudocode | thin_explanation | missing_edges), `severity`, `excerpt` (first 1–2 sentences or 80 chars of body), `suggested_query_seed` (string: heading + key noun from excerpt for query generation). Compact summary for Log row: e.g. `gaps: 2 (examples, pseudocode)`.
- **Mapping to query seeds**: research-agent-run uses **suggested_query_seed** and **type** to build targeted queries (e.g. "open-source pseudo-code for [topic]" for missing_pseudocode, "best-practice [topic] edge cases" for missing_edges). See research-agent-run § gap-fill mode.

## Inline injection rules

- **When**: gap_fills are returned from research-agent-run (gap-fill mode) in step 4.5; inject each **filled_markdown** into the draft **before** step 5 writes the note. Only inject fills with **fill_conf ≥ 68%** (or threshold from Parameters); discard or log low-conf fills.
- **Placement**:
  - **Technical subphases (current_depth ≥ 3)**: Inject **immediately after** the matching section/heading so juniors see code where they need it. Match by **gap_id** → heading/section in draft.
  - **Narrative or depth 1–2**: Group all fills under a single **## External Grounding** (or **### Filled Gaps (External References)**) subsection at an appropriate place (e.g. before "## Tertiary notes" or at end of body). Use subsections **code**, **edges**, **perf** where the fill type suggests it.
- **Structure**: Each injected block must include: (1) the heading or label from research-agent-run (e.g. `## Filled Gap: [local heading fragment] — [short label]`), (2) the explanation/code body, (3) **source citation** on its own line: `[Source: ProjectOrDocName](url)` or `[Source: GitHub repo/path](url)`. When grouping under External Grounding, use the same citation pattern and optional subsections (code, edges, perf).
- **Recalibration marker**: After each injected block, insert an HTML comment on its own line: `<!-- research-gap-fill: <gap_id> -->` (e.g. `<!-- research-gap-fill: gap_1 -->`). This supports future recalibration or replacement without parsing the whole note.

## MCP tools

- `obsidian_read_note` — read workflow_state, roadmap-state, distilled-core, existing phase notes.
- `obsidian_list_notes` — list phase folders and notes under Roadmap/ to compute next target.
- `obsidian_ensure_structure` — create phase/secondary/tertiary folders.
- `obsidian_update_note` — create new roadmap notes (or write new file at path); update workflow_state (append Log row, update frontmatter).
- **obsidian-snapshot** skill — per-change snapshot of roadmap-state and workflow_state before any write.

## Reference

- [Vault-Layout § Roadmap state artifacts](3-Resources/Second-Brain/Vault-Layout.md) — workflow_state schema, dual track, Log columns.
- [Roadmap Structure](Roadmap Structure.md) — folder layout, frontmatter, hierarchy (master → phase → secondary → tertiary → tasks), Execution subtree.
- [Dual-Roadmap-Track](3-Resources/Second-Brain/Docs/Dual-Roadmap-Track.md) — user-facing dual-track summary.
- [dual-roadmap-track](.cursor/rules/context/dual-roadmap-track.mdc) — frozen conceptual / execution enforcement.
- [auto-roadmap](.cursor/rules/context/auto-roadmap.mdc) — calls this skill when RESUME-ROADMAP has action "deepen".
- [Queue-Sources](3-Resources/Second-Brain/Queue-Sources.md) — RESUME-ROADMAP params and queue format.
- [conceptual-decision-record](.cursor/skills/conceptual-decision-record/SKILL.md) — atomized rationale notes after conceptual deepen (step 6b).

