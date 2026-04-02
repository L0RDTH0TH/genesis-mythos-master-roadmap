---
created: 2026-03-30
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-recal-contradictions-gmm-20260330T221500Z
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 1
  medium: 0
  high: 0
validator_report_path: .technical/Validator/roadmap-handoff-auto-genesis-mythos-master-20260401T001500Z-conceptual-v1-post-recal.md
---

# IRA — roadmap / RESUME_ROADMAP(recal) — call 1

## Context

RoadmapSubagent invoked IRA after the first nested `roadmap_handoff_auto` pass (`ira_after_first_pass: true`). The validator reported **`missing_roll_up_gates`** (primary) and **`safety_unknown_gap`**, with **`recommended_action: needs_work`**. The operator **already edited** the `2026-04-01 00:10` **recal** row in `workflow_state.md` to remove the misleading **`need_class: incoherence`** pairing. Current vault state shows that row using **closure-oriented resolver metadata** (`recal_hygiene_applied: true`, historical `prior_l1_post_lv_gate_signature`, explicit prose: **not** an active incoherence-class block). The validator note’s complaint about `need_class: incoherence` appears **stale relative to the updated row**.

## Structural discrepancies (vs validator narrative)

1. **`safety_unknown_gap` (likely cleared in-tree):** The cited audit-hostile pairing (“incoherence-class need” + “superseded / drift 0.00”) is **no longer present** on the `2026-04-01 00:10` log row in the current `workflow_state.md` snapshot.
2. **`missing_roll_up_gates`:** Remains a **conceptual-track advisory** (execution rollup / compare-table / sealed-bundle closure deferred). `roadmap-state.md` already documents the **conceptual waiver**; this is **not** a dual-truth structural contradiction with `workflow_state` / Phase 2 cursor.
3. **Timestamp hygiene (minor):** `roadmap-state.md` frontmatter **`last_run: 2026-04-01-0000`** still reflects the **00:00** deepen/anchor event, while the latest **state-changing** workflow log row for narrative hygiene is **`2026-04-01 00:10`** (recal). Validator flagged this as **optional** monotonicity, not routing contradiction.

## Proposed fixes (for RoadmapSubagent to apply under gates)

| # | risk | target | action |
|---|------|--------|--------|
| 1 | low | `1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md` | Optional: **`adjust_frontmatter`** — set `last_run` to a stamp **≥** the `2026-04-01 00:10` recal boundary (e.g. `2026-04-01-0010` if that matches project `last_run` format), **only if** project policy treats `last_run` as “last structural hygiene event” rather than “last queue-anchor restamp.” **Constraint:** preserve snapshot-before-write rules for roadmap-state. |

**No further MCP edits are required** to resolve the **incoherence-class resolver** issue; the operator adjustment already addresses it.

## Notes for future tuning

- **Validator vs operator latency:** Hostile reports can describe rows that were fixed **after** the validator run. Final compare (`compare_to_report_path`) should treat **closure** when workflow resolver text explicitly marks **historical trigger** vs **outcome**.
- **`missing_roll_up_gates` on conceptual_v1:** Tiered handling should continue to treat as **advisory** when waiver + phase-note deferrals are explicit (avoid spinning RECAL solely on this code).
- **Template:** Consider standardizing resolver keys for post-recal rows: `outcome_class: contradictions_cleared | hygiene_repair` vs provenance fields like `prior_l1_post_lv_gate_signature` so automations do not grep **gate_signature** as an **active** need.
