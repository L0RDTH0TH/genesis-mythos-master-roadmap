---
created: 2026-03-22
pipeline: research
project_id: genesis-mythos-master
queue_entry_id: gmm-a1b-bootstrap-deepen-20260322T122045Z
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 5
  medium: 0
  high: 0
validator_report_path: .technical/Validator/research-synthesis-genesis-mythos-master-20260322T130800Z-first.md
parent_run_id: l1-eatq-20260322-gmm-a1b-bootstrap
---

# IRA — research synthesis repair (call 1)

## Context

Research pipeline invoked IRA after nested `research_synthesis` validator first pass (`ira_after_first_pass: true`). Verdict: **medium** / **needs_work** / **primary_code: safety_unknown_gap**. The synthesis note `Ingest/Agent-Research/phase-3-4-9-task-decomposition-junior-handoff-research-2026-03-22-1245.md` is structurally honest on D-044/D-059 but underspecifies Post-`recal` hygiene vs phase **3.4.8**, uses ambiguous wikilinks in boilerplate, and presents synthetic task IDs without an explicit table-level disclaimer.

## Structural discrepancies

1. **HYG-1** row says "compare **4 fields**" without naming `last_ctx_util_pct`, `last_conf`, `current_subphase_index`, `last_auto_iteration` (authoritative in phase 3.4.8 Given/When/Then).
2. Section 5.2 table uses bare filenames; section 5.3 uses `[[decisions-log]]` — multi-project vault ambiguity.
3. **HYG-1** / **DLG-1** / **TREE-1** labeled illustrative in section 5.0 prose but table reads like canonical backlog keys.
4. **INVEST — Independent** bullet is normative methodology without vault tie-down.

## Proposed fixes

See caller `suggested_fixes[]` (apply only under `Ingest/Agent-Research/**` per Research nested rules).

## Notes for future tuning

- Paste key names from the linked phase note or block-quote the checkbox to avoid copy-paste drift.
- Prefer full vault-relative paths in automation-facing handoff tables.

