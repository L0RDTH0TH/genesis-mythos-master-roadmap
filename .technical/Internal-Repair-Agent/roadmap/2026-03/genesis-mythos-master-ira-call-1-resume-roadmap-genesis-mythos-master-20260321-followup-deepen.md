---
created: 2026-03-21
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-roadmap-genesis-mythos-master-20260321-followup-deepen
ira_call_index: 1
status: repair_plan
risk_summary: { low: 3, medium: 1, high: 0 }
parent_run_id: pr-eatq-20260321-resume-gmm-deepen
validator_report_path: .technical/Validator/roadmap-auto-validation-20260321T220500Z.md
---

# IRA call 1 — genesis-mythos-master (post–first-pass validator)

## Context

Invocation **(B)** after nested `roadmap_handoff_auto` first pass with **`ira_after_first_pass: true`**. Verdict: **`severity: medium`**, **`recommended_action: needs_work`**, **`primary_code: missing_task_decomposition`**, plus **`safety_unknown_gap`**. Artifacts reviewed: validator report; `distilled-core.md` dependency mermaid (ends at Phase 2.2.4); Phase 2.3 secondary note (`progress: 0`, open Tasks, `handoff_gaps` for EMG bindings, EMG-2 floor **F** TBD); `decisions-log.md` (through **D-021** only). Validator explicitly states **roadmap-state** / **workflow_state** alignment for the deepen snapshot is OK — no state-hygiene repair requested.

## Structural discrepancies

1. **Roll-up visualization gap:** `distilled-core.md` mermaid `flowchart TD` stops at **`Phase2_2_4`**; Phase **2.3** exists in narrative/`core_decisions` but not in the dependency graph (traceability vs validator `safety_unknown_gap`).
2. **Task decomposition vs opening slice:** Phase 2.3 **Tasks** are unchecked; `progress: 0` matches exploratory status but feeds **`missing_task_decomposition`** until EMG rows are bound to a concrete in-vault table/anchor or tertiaries.
3. **Decision traceability:** No **D-022** (or equivalent) for EMG adoption / freeze intent; validator **`next_artifacts`** calls for a decision id when floors freeze — a **stub** now preserves trace without falsifying frozen bindings.
4. **Residual unknowns (not auto-fixable in one edit):** Numeric floor **F** and normative schema field paths remain **TBD** until human/tertiary closure; fixes below **document** placeholders, not production values.

## Proposed fixes

| Order | Risk | Target | Summary |
|-------|------|--------|---------|
| 1 | low | `distilled-core.md` | Add **`Phase2_3`** mermaid node and edge **`Phase2_2_4 --> Phase2_3`** (label consistent with existing node style). |
| 2 | low | `decisions-log.md` | Append **D-022 stub**: intent to record EMG-1..3 bindings + floor **F** when 2.3.x tertiaries freeze; link Phase 2.3 secondary; **no** claimed numeric freeze yet. |
| 3 | low | Phase 2.3 secondary note | Add **`### EMG binding table (v0 stub)`** with a small markdown table (EMG-1..3 × placeholder column for schema field / pseudo-code row / status). Reword the three **Tasks** bullets to wiki-link to this section (same-note `[[#...]]` anchor) so checkboxes track decomposition without inventing repo paths. |
| 4 | medium | Phase 2.3 secondary note (optional) | Tighten **`handoff_gaps`** frontmatter entry to reference **D-022** + in-note stub table (still TBD) — cross-file consistency; skip if frontmatter churn is undesirable in one run. |

## Notes for future tuning

- When first secondary slice for a macro phase lands, **distilled-core** mermaid and **core_decisions** bullets should be updated in the **same** deepen or a follow-up RESUME_ROADMAP to avoid recurring **`safety_unknown_gap`** on diagram lag.
- **`missing_task_decomposition`** on opening slices may stay **needs_work** until tertiaries exist; tiered Success gate still allows pipeline Success — IRA fixes focus on **traceability** (anchors, D-number stub, graph edge), not pretending closure.
