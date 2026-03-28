---
created: 2026-03-23
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-roadmap-genesis-mythos-master-20260323-deepen-suggested-248
ira_call_index: 1
status: repair_plan
risk_summary: {low: 3, medium: 1, high: 0}
validator_branch: validator-driven
ira_after_first_pass: true
---

# IRA call 1 — genesis-mythos-master — queue 248 (post–first-pass `roadmap_handoff_auto`)

## Context

RoadmapSubagent invoked IRA after the **first** nested `roadmap_handoff_auto` pass for **RESUME_ROADMAP** deepen **3.3.4** (`resume-roadmap-genesis-mythos-master-20260323-deepen-suggested-248`). Verdict: **medium** / **needs_work**; **primary_code** `missing_task_decomposition`; **secondary** `safety_unknown_gap`. Machine cursor and workflow_state **12:00** row for queue **248** are consistent with frontmatter (`current_subphase_index` **3.3.4**, context columns populated). Rollup **HR 92** < **min_handoff_conf 93** is correctly documented; that is **not** an IRA “fix HR” target without operator/policy change.

## Structural discrepancies (re-verified vs vault)

1. **Decisions list monotonicity (validator citation D-050 vs D-038):** In the **current** `decisions-log.md`, **D-037 → D-038 → D-039** precede later rows and **D-050** appears **after** **D-049**. The validator’s “D-050 then D-038” consecutive-row failure mode is **not** present in the artifact as read for this IRA call — consistent with parent having already reordered **D-037/D-038** ahead of **D-039** and eliminating the post–D-050 inversion.

2. **3/3 vs 3/5 arithmetic (safety_unknown_gap):** `phase-3-3-4-...-2026-03-23-1200.md` now carries an explicit **Machine rule (reconciles with D-050)** block and frontmatter `handoff_readiness_scope` uses **3/5 normative PASS (vault draft) + 2 HOLD** language aligned with **D-050**’s five-row inventory. Residual risk is **wording skim**, not raw contradiction.

3. **missing_task_decomposition:** The **Tasks** section still uses **`[ ]`** for items that are **textually** scoped as **DEFERRED (D-044)**, **DEFERRED (D-020 / 2.2.3)**, and **DEFERRED (handoff_gate)**. Hostile validators and auditors often treat **open checkboxes** as “execution not closed” even when labels say DEFERRED — same class of gap as prior tertiaries (e.g. **3.3.1** DEFERRED ledger pattern in `roadmap-state` consistency reports).

4. **D-044 evidence / registry-CI:** There is still **no** logged **RegenLaneTotalOrder_v0** **A** or **B** adoption line under **D-044** (operator fork). **G-P3.3-REGISTRY-CI** correctly remains **HOLD**. IRA **must not** suggest wording that implies CI PASS or fixture existence without evidence.

## Proposed fixes (for Roadmap subagent apply; ordered low → medium)

See structured `suggested_fixes` in the parent return payload. Summary:

- **Low:** Check **DEFERRED** tertiary tasks on **3.3.4** as **`[x]`** while preserving **DEFERRED** and decision ids in the line text (vault-honest “closure of documentation,” not execution closure).
- **Low:** Optional one-line **status sub-bullet** under **D-044** in `decisions-log.md`: “As of 2026-03-23: **RegenLaneTotalOrder_v0** A/B **not** selected in-vault; **G-P3.3-REGEN-DUAL** remains **HOLD**.” (No fake A/B.)
- **Low:** No edit needed for **decisions-log** D-order if current monotonic scan is confirmed after snapshot; if a **compare-final** validator still embeds a stale excerpt, ensure **second pass** uses fresh file read.
- **Medium:** Add a **short, explicit vault-only waiver** paragraph (rollup note or **Handoff notes** in `decisions-log`) for **G-P3.3-REGISTRY-CI**: fixtures + path-scoped CI **TBD**; **no** “PASS” or “green CI” claim until **2.2.3** / **D-020** evidence — scope-limited, honest.

## Notes for future tuning

- **Post-IRA apply pattern:** When tertiaries use **DEFERRED**, standardize on **`[x]` + DEFERRED tag** or a dedicated **DEFERRED ledger** subsection so `missing_task_decomposition` does not fire on honest holds.
- **Validator excerpts:** First-pass reports may quote **pre-repair** row order; **compare_to_report_path** second pass should diff against **current** file content to avoid false regression on already-fixed ordering.
