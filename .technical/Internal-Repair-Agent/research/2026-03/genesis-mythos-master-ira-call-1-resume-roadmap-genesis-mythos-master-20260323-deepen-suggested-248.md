---
created: 2026-03-23
pipeline: research
project_id: genesis-mythos-master
queue_entry_id: resume-roadmap-genesis-mythos-master-20260323-deepen-suggested-248
ira_call_index: 1
status: repair_plan
risk_summary: { low: 3, medium: 4, high: 0 }
parent_run_id: pr-qeat-20260323-resume-248
validator_report: .technical/Validator/research-synthesis-genesis-mythos-master-20260323T120500Z-nested-predeepen-248-first.md
---

# IRA call 1 — research / nested pre-deepen (248)

## Context

Validator-driven invocation after first `research_synthesis` pass (`severity: medium`, `needs_work`). Primary code `safety_unknown_gap`: the synthesis note `Ingest/Agent-Research/phase-3-3-4-secondary-closure-rollup-research-2026-03-23.md` states HR/EHR integers and rollup arithmetic without in-note citations to the exact primary fields. Secondary `missing_task_decomposition`: no numbered deepen WBS with acceptance criteria. Spot-check against vault frontmatter shows **3.3.1–3.3.3** values **90/58, 89/56, 88/54** and **3.1.7 / 3.2.4** **93/68** and **92/61** respectively — numbers are **plausibly correct** but still **epistemically unmoored** in the synthesis until footnoted. Apply targets for this hand-off: **only** `Ingest/Agent-Research/**` and `.technical/Run-Telemetry/**` (no phase note edits).

## Structural discrepancies

1. **Unsourced numerics** — Table rows and narrative assert HR/EHR and min/floor math without `handoff_readiness:` / `execution_handoff_readiness:` pointers.
2. **Weak decision traceability** — `[[decisions-log|D-0xx]]` aliases without heading anchors or quoted stubs inside the research artifact.
3. **Missing compressed factual payload** — Validator `next_artifacts` require per-tertiary digests and explicit REGEN-DUAL scoring rule.
4. **No deepen WBS** — Pending decisions listed as bullets, not a numbered task list with acceptance criteria.

## Proposed fixes

See parent return payload `suggested_fixes[]` (ordered low → medium → high for application).

## Notes for future tuning

- Research synthesis template should require **footnote or inline cite** for any integer carried from phase frontmatter on first draft.
- Consider a `research_synthesis` checklist in the research skill: "every HR/EHR → path + YAML key or delete."
