---
created: 2026-03-22
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-roadmap-genesis-mythos-master-20260322-deepen-followup-239
parent_run_id: pr-queue-20260322-resume-genesis-239
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 2
  medium: 4
  high: 0
validator_report_path: .technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260322T232030Z.md
---

# IRA report — roadmap — genesis-mythos-master — call 1

## Context

Post–nested-validator **roadmap_handoff_auto** (`needs_work`, primary `contradictions_detected`, secondary `safety_unknown_gap`). Validator correctly flags **stale YAML on the Phase 3.1 secondary parent** (`phase-3-1-simulation-tick-scheduler-and-time-quanta-roadmap-2026-03-21-2346.md`): `handoff_readiness: 88` and gaps implying **≥93 roll-up still pending**, while the **same file’s** tertiary roll-up table and **[[phase-3-1-7-phase-3-1-secondary-closure-rollup-and-advance-readiness-roadmap-2026-03-22-0122]]** + **D-038** assert **rollup HR 93** and **6/6 PASS**. Under the **contaminated-report rule**, treat validator findings as a **weak minimum**: also align **distilled-core** Phase 3.1 summary language, add an **explicit operator guardrail** (normative vs execution), and **pin G-P3.1-GOLDEN** draft state in **decisions-log** so nothing reads as a frozen registry row.

## Structural discrepancies

1. **Frontmatter vs body (secondary 3.1):** YAML advertises HR **88** and “roll-up to ≥93 pending”; body table row **3.1.7** shows **93** / rollup authority / **6/6 PASS** — **Dataview and automation see false “still at 88”.**
2. **Cross-artifact narrative:** **distilled-core** Phase 3.1 bullet still says “roll-up **toward** ≥93” without stating **achieved rollup authority on 3.1.7 / D-038** — weak inconsistency with **3.1.7** and **D-038**.
3. **Operator ambiguity (`safety_unknown_gap` expansion):** **advance-phase** eligibility (**HR 93** rollup) can be misread as **execution** closure; **3.1.7** already states **EHR 68** — need a **single normative locus** (decisions-log or state note) repeating the split **before** operators queue advance.
4. **G-P3.1-GOLDEN:** Cited as **draft** in **3.1.7** and **D-038**; validator may under-count risk of **implicit freeze** — require **explicit deferral / tracking ID** in **decisions-log**.

## Proposed fixes (for RoadmapSubagent apply order: low → medium)

| # | risk | action_type | target_path | description |
|---|------|-------------|-------------|-------------|
| 1 | low | adjust_frontmatter | `1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/phase-3-1-simulation-tick-scheduler-and-time-quanta-roadmap-2026-03-21-2346.md` | Set **`handoff_readiness: 93`** (rollup-aligned). Add **`handoff_readiness_scope`** mirroring **3.1.7** (G-P3.1-* 6/6 PASS; advance gating per **D-038**; per-tertiary HR 91–93 superseded for advance). Add **`execution_handoff_readiness: 68`** (or equivalent numeric) **or** a single frontmatter line pointing to **3.1.7** for EHR. **Replace** `handoff_gaps` entries that claim **pending ≥93 roll-up** with gaps that match **3.1.7**: execution debt + **G-P3.1-GOLDEN** draft + pointer to **D-038**. |
| 2 | low | adjust_frontmatter | *(same secondary note)* | Optional **`handoff_authority_note`** or rely on scope field: “Roll-up authority: **[[phase-3-1-7-...-0122]]**; secondary YAML follows rollup.” **Constraints:** apply only after per-change snapshot per roadmap rules. |
| 3 | medium | write_log_entry | `1-Projects/genesis-mythos-master/Roadmap/decisions-log.md` | Add **D-039** (or next free ID): **Operator guardrail — normative vs execution for Phase 3.1 advance.** One paragraph: **`advance-phase` (3.1→3.2) eligibility** uses **rollup `handoff_readiness: 93`** on **3.1.7** per **D-038**; **does not** mean **execution_handoff_readiness** or repo goldens are green; composite **EHR 68** and **3.1.7 `handoff_gaps`** govern execution work. **Links:** **[[phase-3-1-7-phase-3-1-secondary-closure-rollup-and-advance-readiness-roadmap-2026-03-22-0122]]**, **D-038**. |
| 4 | medium | write_log_entry | *(same decisions-log)* | Add **D-040** (or extend **D-038** with dated sub-bullet if IDs constrained): **G-P3.1-GOLDEN** — state **`status: draft`**, **non-frozen**, reconcile naming with **2.2.3** / **D-020** before any narrative implies registry freeze; **owner** + **reopen** condition (e.g. wiki row materialized in **2.2.3**). |
| 5 | medium | adjust_frontmatter / body_edit | `1-Projects/genesis-mythos-master/Roadmap/distilled-core.md` | Update **Phase 3.1 (simulation_tick_scheduler)** bullets (YAML list + prose) from “roll-up **toward** ≥93” to **rollup closure achieved** via **3.1.7** / **D-038**, **HR 93** vs **EHR 68**, link **3.1.7**. |
| 6 | medium | set_context_metrics or write_log_entry | `1-Projects/genesis-mythos-master/Roadmap/workflow_state.md` | If the project uses **workflow_state** frontmatter for operator hints: add **`operator_advance_guardrail: "See decisions-log D-039; normative HR 93 ≠ EHR 68."`** **or** append **one** new **## Log** row after next roadmap run documenting the guardrail — **only if** it does not fight the 12-column schema (prefer **decisions-log D-039** as primary locus). **Constraints:** snapshot before/after per roadmap invariants. |

## Notes for future tuning

- **roadmap-deepen / hand-off-audit** should treat **secondary** notes with roll-up tables as **“rollup child present”** and either auto-sync **handoff_readiness** from rollup note or emit **#review-needed** when secondary HR < rollup HR.
- Consider a **lint** in little-val for **roadmap-level: secondary** notes: if body contains **### Tertiary roll-up** with HR ≥ min_handoff_conf, frontmatter **`handoff_readiness`** must not lag rollup row for the designated rollup tertiary.

## Machine return (summary)

- **status:** `repair_plan`
- **suggested_fix_count:** 6 (2 low, 4 medium; #6 optional if D-039 is sufficient)
