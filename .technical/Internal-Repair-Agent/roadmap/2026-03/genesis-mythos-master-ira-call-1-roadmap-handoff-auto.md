---
created: 2026-03-31
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: "-"
ira_call_index: 1
status: repair_plan
risk_summary: {low: 0, medium: 0, high: 0}
validator_primary_code: safety_unknown_gap
---

# IRA — roadmap_handoff_auto (validator first pass)

## Context

Roadmap subagent invoked IRA after **roadmap_handoff_auto** first pass for **genesis-mythos-master** (conceptual track, gate **conceptual_v1**). Validator verdict: **severity** medium, **recommended_action** `needs_work`, **primary_code** `safety_unknown_gap`. The report states cross-artifact alignment (roadmap-state, workflow_state, distilled-core, decisions-log) on **current_phase 4**, **roadmap_track: conceptual**, **current_subphase_index 4.2**, tertiaries **4.2.1–4.2.3** complete, drift **0.0**, and **no** contradiction-class conflict. The open item is **explicit**: secondary **4.2 rollup** (NL + GWT-4.2 vs 4.2.1–4.2.3) is **not** yet logged complete; **RECAL-ROAD** is queued ahead per workflow hygiene.

## Structural discrepancies

- **None requiring automated “repair” edits.** The validator frames the gap as **completion unknown** until RECAL runs and the secondary 4.2 deepen updates roadmap-state / distilled-core / CDR — i.e. **forward pipeline work**, not a stale or contradictory registry row.
- **`safety_unknown_gap`** here encodes **pending conceptual closure**, not **state_hygiene_failure** or **incoherence** (report explicitly excludes block_destructive-class codes from the four state inputs).

## Proposed fixes

**None.** Per IRA scope, no low-risk file-level structural repairs are indicated; applying fake “complete” markers without running the scheduled **RESUME_ROADMAP** / deepen steps would be **high** blast-radius and would misrepresent vault truth.

**Caller guidance (orchestration, not IRA apply steps):**

1. **RECAL-ROAD** at ~80% ctx util when autopilot threshold is met; ensure Consistency / workflow narrative reflects **drift_score_last_recal** (or explained delta).
2. **Secondary 4.2 rollup** on the Phase-4-2 roadmap note — NL checklist + GWT-4.2 vs 4.2.1–4.2.3; **handoff_readiness** on secondary 4.2; atomized **CDR** per Vault-Layout when deepen requires it.
3. **Post-rollup**: reconcile **workflow_state** last row and **distilled-core** canonical routing so **current_subphase_index** matches **4.3** mint or Phase 4 primary rollup / advance; clear stale queue **user_guidance** vs vault cursor if that failure mode reappears.

## Notes for future tuning

- **`safety_unknown_gap`** on conceptual_v1 will often mean “rollup not written yet” while state is **consistent** — second-pass validator should **compare_to_report_path** without expecting IRA **suggested_fixes** when the first pass already listed **next_artifacts** only.
- Consider distinguishing **forward_work_pending** (aligned state, incomplete rollup) from **unknown_safety** (ambiguous or unreadable state) in gate catalog copy to reduce unnecessary IRA invocations.
