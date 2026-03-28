---
created: 2026-03-22
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: recal-gmm-post-348-deepen-high-util-20260322T120501Z
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 3
  medium: 2
  high: 0
validator_report_path: .technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260322T120000Z-recal-first.md
parent_run_id: pr-eatq-20260322-gmm-recal
reason_codes:
  - safety_unknown_gap
  - missing_task_decomposition
---

# IRA report — genesis-mythos-master — validator-driven call 1

## Context

Roadmap subagent completed **RESUME_ROADMAP** `action: recal` for **genesis-mythos-master**. Nested **roadmap_handoff_auto** first pass returned **needs_work** / **medium** / **primary_code `safety_unknown_gap`** with secondary **`missing_task_decomposition`**. Invocation used **`ira_after_first_pass: true`**. Validator correctly flags non-reproducible drift scalars, **`last_run: 2026-03-22-1200`** vs a **12:05** deepen narrative block in `roadmap-state.md`, and tertiary execution/task surface on **3.4.8**. This IRA pass proposes **documentation and structural clarity only** — no operator picks for **D-044** / **D-059**, no fabricated task completions.

## Structural discrepancies

1. **`drift_score_last_recal` / `handoff_drift_last_recal`** appear in YAML and prose without an explicit, reader-auditable derivation chain (inputs, tool/skill id, snapshot set, recomputation steps).
2. **`last_run`** (frontmatter) reads **1200** while the consistency section documents a **12:05** deepen subsection immediately after the 12:00 RECAL block — mixed signal for humans and parsers that do not use [[workflow_state]] authority rules.
3. **`missing_task_decomposition`**: Phase **3.4.8** task ladder remains open; validator expects either closed PASS evidence or explicit audit state — absent a labeled structural audit section, "unchecked" reads as undocumented rather than intentionally open.
4. **Execution deferrals** (**EHR 35**, rollup **HR** vs **min_handoff_conf 93**) are scattered; a single visibility line in **workflow_state** Notes reduces **`safety_unknown_gap`** adjacency risk without changing decisions.

## Proposed fixes

See parent return payload **`suggested_fixes`** (stable order, risk-tagged). Apply under normal snapshot + high-band rules; prefer **low** before **medium**.

## Notes for future tuning

- After **RECAL** when **workflow_log_authority** keeps a **deepen** row last, consider having roadmap pipeline **auto-append** a one-line "drift inputs hash / audit run id" when writing drift YAML, so validators need not infer from prose.
- Tertiary notes should reserve a small **structural audit** stub whenever **handoff_gate** is true, so **`missing_task_decomposition`** can downgrade when the gap is "content" but traceability exists.
