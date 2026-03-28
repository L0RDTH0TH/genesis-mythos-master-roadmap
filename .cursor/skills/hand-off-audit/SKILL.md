---
name: hand-off-audit
description: Evaluates phase trace for junior-dev delegatability (traceability, pseudo-code, interfaces, acceptance criteria, no open forks). Outputs handoff_readiness and handoff_gaps on phase notes; logs to decisions-log; used when handoff_gate_enabled or RESUME-ROADMAP with focus handoff-readiness.
---

# hand-off-audit

## When to use

- After core phase generation in **roadmap-generate-from-outline** (mandatory post-processing), per phase (when `handoff_gate_enabled` or queue `handoff_gate: true`).
- From **roadmap-resume** when RESUME-ROADMAP is run with `focus: "handoff-readiness"` or `handoff_focus: true`.
- On-demand: queue mode **HANDOFF-AUDIT** or Commander "Audit hand-off".

**Pipeline slot:** After roadmap-generate-from-outline in [Cursor-Skill-Pipelines-Reference](3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference.md) § Roadmap pipelines (e.g. step 4: audit → refine if mid/low).

## Parameters

- **project_id** (required): Project containing the Roadmap folder; from trigger (note path, queue payload `project_id`, or `source_file` under the project).
- **phase_number** or **phase note path** (optional): Specific phase to audit; when absent, audit current phase from roadmap-state or all phases up to current.
- **roadmap_dir** (optional): Override path; default `1-Projects/{project_id}/Roadmap/`.

## Instructions

1. **Resolve phase tree**: Default **`roadmap_dir`** = `1-Projects/{project_id}/Roadmap/`. **Dual track:** When **`params.roadmap_track`** is **`execution`** or **`roadmap-state.md`** **`roadmap_track`** is **`execution`**, resolve phase notes under **`roadmap_dir/<execution_subfolder>/`** (default **`Execution`**); otherwise under **`roadmap_dir`**. **Resolve phase and traverse trace**: Resolve phase roadmap note (and optionally phase-X-output). Traverse trace via **obsidian_read_note** chain (root to leaf): follow wiki-links and headings for subphase → tertiary → task → pseudo-code. Log full trace path for auditability. **MOC violation check (optional):** When auditing, if the phase or any secondary roadmap note's folder has child notes but the parent note lacks a Dataview block listing them, flag as violation (see [roadmap-validate](.cursor/skills/roadmap-validate/SKILL.md) step 5 and [Roadmap-Quality-Guide](3-Resources/Second-Brain/Roadmap-Quality-Guide.md) § MOC violation check); log to Errors.md with `error_type: roadmap-moc-missing` and optionally create a Decision Wrapper.

2. **Evaluate heuristics**: Assess full trace, pseudo-code/algos (tech_level-aware per phase frontmatter), interfaces/hooks/contracts, acceptance criteria per task, open forks. Apply **handoff_heuristics_weights** from Second-Brain-Config roadmap block when present. Apply **positive bonus heuristics**: +12% if Mermaid sequence/flow diagram exists for the trace; +10% if every non-trivial task has at least one acceptance criterion; +8% if modularity seams have a 1–2 line "swap example" comment. Resolve thresholds from **handoff_thresholds_by_tech** by phase tech_level when present; else use global high/mid_min/mid_max from config.

3. **Compute scores**: Compute **handoff_readiness** (0–100) and **handoff_gaps** (array of short strings, e.g. "Phase-3 tick loop lacks pseudo-code", "Simulation flavor fork unresolved").

4. **Write to phase note frontmatter**: Set `handoff_readiness`, `handoff_gaps`; optionally **handoff_traces** (array of `{ path, readiness, gaps }`) for multi-trace phases. Snapshot the phase note before frontmatter write when same run performs other edits (per [mcp-obsidian-integration](.cursor/rules/always/mcp-obsidian-integration.mdc)).

5. **Append to decisions-log.md**: One line per phase with `#handoff-review`, link to phase note, handoff_readiness, first 1–2 gaps; **log full trace path** for auditability. If gaps were fixed in a refinement run, cross-post a short summary to **distilled-core.md**.

6. **Log to pipeline log**: Append to Ingest-Log or Roadmap-Log (or 3-Resources/Decisions-Log if present) with phase path, handoff_readiness, handoff_gaps count.

## Mid-band refinement loop (70–84%)

- Refinement loops attempt to fill gaps (e.g. propose pseudo-code stubs via guidance); future iterations may add explicit auto-stub generation.
- Generate previews with filled gaps; use **guidance-aware** merge for `user_guidance` (e.g. "Prioritize JS stubs for controls"). If **post-refinement ≥ high threshold** (85% or per-tech) → auto-apply and commit (with snapshot). **Safety:** Always snapshot the phase note before preview append. Refinement loop cap: 2 (or 3 when auto-stub generation is enabled in config).

## Low band (<70%)

- Append `#handoff-needed` to decisions-log. Queue a **TASK-ROADMAP** (or EXPAND-ROAD) entry for the gapped trace (e.g. "Fill pseudo-code for sim tick") so the loop closes autonomously where possible.

## MCP tools

- `obsidian_read_note` — read phase roadmap note, phase-X-output, and trace chain (subphase → tertiary → task).
- `obsidian_update_note` / `obsidian_manage_frontmatter` — write handoff_readiness, handoff_gaps, handoff_traces to phase note.
- `obsidian_log_action` — log to pipeline log.
- obsidian-snapshot skill — per-change snapshot of phase note before frontmatter write when same run does other edits.

No moves or deletes.

## Reference

- [Parameters](3-Resources/Second-Brain/Parameters.md) § Hand-off readiness (roadmap).
- [Second-Brain-Config](3-Resources/Second-Brain-Config.md) roadmap block: handoff_gate_enabled, handoff_thresholds_by_tech, handoff_heuristics_weights.
- Hand-off Readiness Integration plan.
