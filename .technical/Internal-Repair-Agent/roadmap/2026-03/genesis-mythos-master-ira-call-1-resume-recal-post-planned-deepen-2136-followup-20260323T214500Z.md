---
created: 2026-03-23
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-recal-post-planned-deepen-2136-followup-gmm-20260323T214500Z
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 4
  medium: 4
  high: 2
validator_report_path: .technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260323T220500Z-recal-2136-followup-first.md
parent_run_id: 57a442d3-c2d3-43dd-b9c2-77ec23f17fa2
tags: [internal-repair-agent, roadmap, genesis-mythos-master, recal, validator-branch-b]
---

# IRA call 1 — roadmap_handoff_auto first pass (post-2136Z RECAL)

## Context

RoadmapSubagent completed **RESUME_ROADMAP** `action: recal` for **`resume-recal-post-planned-deepen-2136-followup-gmm-20260323T214500Z`** after shallow **3.4.9** deepen **`resume-deepen-post-recal-planned-pc349-gmm-20260323T213600Z`** (Ctx **96%**). Nested **roadmap_handoff_auto** first pass returned **severity medium**, **recommended_action needs_work**, **primary_code missing_roll_up_gates**, **reason_codes**: `missing_roll_up_gates`, `missing_task_decomposition`, `safety_unknown_gap`. **Contaminated-report rule** applied: validator output is treated as a **minimum**; structural debt is **at least** that set, plus any cross-surface inconsistencies below.

Artifacts reviewed: validator report; [[workflow_state]] (physical last deepen row + **2026-03-23 22:00** `recal` row); [[roadmap-state]] rollup authority index + drift notes; [[decisions-log]] **D-044**/**D-059**/**D-055**; [[distilled-core]] `core_decisions` Phase **3.4.9** YAML string (DoD mirror + trace cites).

## Structural discrepancies (expanded)

1. **Roll-up macro gates (primary):** Rollup **HR 92** vs **`min_handoff_conf` 93** with **G-P3.2-/3.3-/3.4-REGISTRY-CI** **HOLD** is **consistent** across [[roadmap-state]] machine table, [[workflow_state]] **22:00** `recal` narrative, and decisions rows — **not** a prose bug; it is **real blocking debt** until repo/CI evidence or a **documented policy exception**.
2. **missing_task_decomposition:** Phase **3.4.9** bundles many trace IDs in one YAML string; Validator DoD mirror remains **`[ ]`** in prose semantics (clear only when REGISTRY-CI clears or mirror is **formally retired** with a decisions-log anchor).
3. **safety_unknown_gap:** [[roadmap-state]] already disclaims **`qualitative_audit_v0`** for **`drift_score_last_recal`** / **`handoff_drift_last_recal`**, but there is still **no versioned drift spec + input hash** artifact to make future comparability **machine-checkable** (validator **next_artifacts** item 4).
4. **Under-reported / watchlist (contamination expansion):**
   - **Composite execution_handoff_readiness** and per-tertiary **EHR** strings in [[distilled-core]] vs rollup table — ensure no sentence implies **advance-phase** eligibility while REGISTRY-CI **HOLD** persists (narrative already mostly aligned; spot-check on next edit).
   - **Historical RECAL** blocks in [[roadmap-state]] that still say "D-044 / D-059 open" — [[roadmap-state]] Notes already flag **archived narrative** vs **2026-03-23** picks; any **new** automation should prefer the **live** Note, not stale callout text alone.
   - **Second nested validator pass** should cite **`compare_to_report_path`** **and** this IRA report path in **`nested_subagent_ledger`** / consistency notes for audit closure.

## Proposed fixes (for Roadmap subagent; doc-only where stated)

| # | risk | action_type | target_path | description |
|---|------|-------------|-------------|-------------|
| 1 | low | write_log_entry | `1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md` | In the **Nested validation (…214500Z…)** paragraph (or equivalent latest RECAL block), append **one explicit wikilink** to this IRA report: `[[.technical/Internal-Repair-Agent/roadmap/2026-03/genesis-mythos-master-ira-call-1-resume-recal-post-planned-deepen-2136-followup-20260323T214500Z]]`, plus the first-pass validator path already in frontmatter of the validator report. **Constraints:** only if that block exists for this queue id; idempotent if link already present. |
| 2 | low | write_log_entry | `1-Projects/genesis-mythos-master/Roadmap/workflow_state.md` | Add a **Notes** bullet (timestamp **2026-03-23 22:05 UTC** or next free line): cites **`queue_entry_id`**, **`parent_run_id`**, **`pipeline_task_correlation_id`**, first validator **`.technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260323T220500Z-recal-2136-followup-first.md`**, and this IRA path — **traceability only**, no gate claims. |
| 3 | low | adjust_frontmatter | `1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md` | Add optional keys **`drift_spec_version: qualitative_audit_v0`** (if not redundant with `drift_metric_kind`) and **`drift_input_hash: pending`** (or `null` with comment in body) so automation can distinguish "disclaimed qualitatives" from "hash-backed drift" without implying numeric comparability. **Constraints:** snapshot before edit per roadmap invariants. |
| 4 | low | write_log_entry | `1-Projects/genesis-mythos-master/Roadmap/decisions-log.md` | Under **D-055** (or a single **Machine traceability** sub-bullet), append one line: **IRA call 1** for **`resume-recal-post-planned-deepen-2136-followup-gmm-20260323T214500Z`** → this report path; **needs_work** unchanged; **no** REGISTRY-CI clearance. |
| 5 | medium | adjust_frontmatter | `1-Projects/genesis-mythos-master/Roadmap/distilled-core.md` | In `core_decisions` Phase **3.4.9** entry: **split** the mega-string into **two YAML list items** — (a) live cursor + ctx + queue ids, (b) Validator DoD mirror + REGISTRY-CI debt + compare-final cites — so `missing_task_decomposition` has **atomic** checklist targets. **Constraints:** preserve meaning; no HR inflation. |
| 6 | medium | recompute_phase_metadata | `1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/phase-3-4-9-post-recal-task-decomposition-junior-handoff-bundle-roadmap-2026-03-22-1225.md` | Add a short **Validator DoD mirror (machine)** subsection: one **`[ ]` row per** rollup **HOLD** (**G-P3.2-REGISTRY-CI**, **G-P3.3-REGISTRY-CI**, **G-P3.4-REGISTRY-CI**) + link to [[phase-2-2-3-ci-golden-registry-and-boundary-regression-gates-roadmap-2026-03-21-1205]] / **D-020**; optional **`[x]`** only with PR/CI links. **Alternative:** decisions-log **retirement** row that points replacement artifact — per validator **next_artifacts** item 3. |
| 7 | medium | write_log_entry | `.technical/Validator/` (next compare-final report body, when second pass runs) | Ensure **compare_to** section lists **first-pass path + this IRA path + applied fix ids** (even if empty) so regression guard is **three-way** (214200Z compare-final ↔ 220500Z first ↔ IRA). *If `.technical/Validator` is subagent-only, Roadmap return payload should carry the same tuple.* |
| 8 | high | external_repo_evidence | *(repo / CI — outside vault narrative)* | **Clear REGISTRY-CI HOLD** per validator **next_artifacts** item 1: checked-in fixtures + path-scoped **ReplayAndVerify** (or documented waiver in decisions-log + rollup notes). **Only** then may rollup tables record **PASS** / **HR ≥ 93** with evidence links. **risk high:** blast radius across Phase 3 secondaries and CI policy. |
| 9 | high | adjust_frontmatter | `1-Projects/genesis-mythos-master/Roadmap/decisions-log.md` | **Optional policy exception** path: if operator accepts **advance** or **handoff** waiver without repo green, add a **dated decision row** explicitly waiving **G-P*.*-REGISTRY-CI** with scope + expiry + owner — **never** silently bump rollup HR in vault-only prose. **Constraints:** operator authorship; pairs with roadmap-state rollup table waiver row per validator DoD. |

## Notes for future tuning

- **D-060** high-util **`recal`** chains are doing honest **drift refresh**; nested validator **needs_work** will **repeat** until **REGISTRY-CI** or **policy exception** — IRA doc-only stubs should **not** be mistaken for closure.
- Prefer **atomic** `core_decisions` lines per phase to reduce **`missing_task_decomposition`** false negatives on long YAML strings.
- Consider a **single** vault or `.technical` **drift spec note** (inputs: audit skill version, phase note set hash, decisions-log hash) referenced from [[roadmap-state]] frontmatter when **`drift_input_hash` graduates from `pending`**.

## Structured return (summary)

- **status:** `repair_plan`
- **suggested_fix_count:** 9 (low 4, medium 4, high 2)
- **rationale:** First-pass **roadmap_handoff_auto** correctly flags persistent **rollup HR / REGISTRY-CI** debt and **qualitative drift** epistemology; vault-side work is **traceability + decomposition + optional drift metadata** — **not** fabricating **D-044**/**D-059** or lifting HR without evidence.
