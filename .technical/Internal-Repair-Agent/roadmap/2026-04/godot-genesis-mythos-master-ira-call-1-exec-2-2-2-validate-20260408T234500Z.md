---
created: 2026-04-08
pipeline: roadmap
project_id: godot-genesis-mythos-master
queue_entry_id: exec-2-2-2-validate-20260408T234500Z
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 1
  medium: 1
  high: 0
validator_report: 3-Resources/Second-Brain/Validator-Reports/roadmap_handoff_auto/godot-genesis-mythos-master-exec-2-2-2-validate-20260408T234500Z.md
---

# IRA report — godot-genesis-mythos-master (execution 2.2.2 tertiary)

## Context

Post–nested-validator IRA cycle for **RESUME_ROADMAP** on the **execution** track. First-pass **`roadmap_handoff_auto`** reported **`severity: medium`**, **`recommended_action: needs_work`**, **`primary_code: missing_task_decomposition`**, **`reason_codes`:** `missing_task_decomposition`, `safety_unknown_gap`. Scope: tertiary note **`Phase-2-2-2-Execution-Validate-Classify-Schema-and-Hook-Mapping-Roadmap-2026-04-08-2330.md`** lacks hostile-required **Test plan** and **Executable acceptance criteria**; **`roadmap-state-execution.md`** **Notes** still imply “next … mint execution **2.1**” beside **Phase summaries** that authoritatively say next deepen **2.2.3**.

## Structural discrepancies

1. **Tertiary task/test decomposition:** Phase note has **`## Roll-up gates`**, **`## Pseudocode`**, defer tables, and **Related**, but **no** `## Test plan` or `## Executable acceptance criteria` (validator `missing_task_decomposition`).
2. **Execution state narrative hygiene:** `roadmap-state-execution.md` line under **Handoff-audit repair (2026-04-08 12:58Z)** claims next structural action “remains **mint execution 2.1**” while **Phase summaries** and **`workflow_state-execution`** cursor say **2.2.3** next — **`safety_unknown_gap`** / grep hazard.

## Proposed fixes (for RoadmapSubagent apply)

| # | Target | Action | Risk |
|---|--------|--------|------|
| 1 | `.../Phase-2-2-2-Execution-Validate-Classify-Schema-and-Hook-Mapping-Roadmap-2026-04-08-2330.md` | Insert **`## Test plan`** and **`## Executable acceptance criteria`** after the roll-up / defer content and **before** `## Related` (or immediately after `## Roll-up gates` block per house style). **Test plan** (minimal per validator): matrix **dry-run vs execute** for validation/classify/map paths; harness/fixture id or path; **failure injection** rows for reject paths and `classification_ambiguous`. **Executable AC:** checklist mapping each **`G-2.2.2-*`** to **observable evidence** (logs, artifact paths, harness outputs — not owner_signoff alone). Optionally bump **`handoff_readiness`** in frontmatter after content matches ≥90 narrative if pipeline rules allow. | **low** |
| 2 | `.../Roadmap/Execution/roadmap-state-execution.md` | **Supersede** the stale bullet clause on **Handoff-audit repair (2026-04-08 12:58Z)** that says next action remains **mint execution 2.1**: prefix with **`SUPERSEDED (2026-04-08)`** — current canonical next action: deepen **2.2.3** per **Phase summaries** and **`current_subphase_index: "2.2.3"`** in [[workflow_state-execution]]; keep historical text in-line or one fenced **Historical** line so grep does not treat 2.1 as live directive. | **medium** |

## Notes for future tuning

- Execution tertiaries should default-in **Test plan** + **Executable AC** in the same pass as gate tables to avoid **`missing_task_decomposition`** on **`execution_v1`**.
- When queue reconcile notes (e.g. “stale 2.1 target”) land in phase bodies, mirror a one-line **SUPERSEDED** touch on **roadmap-state-execution** **Notes** if old repair bullets still mention pre-reconcile cursors.
