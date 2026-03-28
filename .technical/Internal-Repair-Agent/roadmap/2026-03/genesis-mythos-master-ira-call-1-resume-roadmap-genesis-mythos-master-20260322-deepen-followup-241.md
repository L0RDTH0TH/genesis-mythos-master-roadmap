---
created: 2026-03-22
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-roadmap-genesis-mythos-master-20260322-deepen-followup-241
ira_call_index: 1
status: repair_plan
risk_summary: { low: 3, medium: 3, high: 1 }
validator_report_path: .technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260322T173500Z.md
parent_run_id: queue-eat-20260322-pr1-a7f3c2b1
---

# IRA call 1 — validator-driven (roadmap_handoff_auto)

## Context

RoadmapSubagent invoked IRA after nested `roadmap_handoff_auto` **first pass** with `ira_after_first_pass: true`. Verdict: **high** / **block_destructive**, primary **`contradictions_detected`**: **D-042** asserts **3.2.1** § Algorithm is aligned with **3.2.2** P1–P6 denial vocabulary, but **3.2.1** still shows a regen FAIL branch collapsing to **`REGEN_PRECONDITIONS_FAILED` or `REGEN_SCOPE_OVERFLOW`**, which cannot emit P2–P6 failures (e.g. `OVERRIDE_MANIFEST_BYPASS`, `REGEN_HASH_CHAIN_DRIFT`, `REGEN_IDEMPOTENCY_VIOLATION`). Secondary codes: **`missing_task_decomposition`** (open Tasks without frozen registry/goldens), **`safety_unknown_gap`** (canonical preimage / scattered TBD). Run **241** consistency block in `roadmap-state.md` still has a placeholder **IRA / validator trace** line.

## Structural discrepancies

1. **Dual truth:** `decisions-log.md` **D-042** vs `phase-3-2-1-...-0210.md` algorithm sketch (lines ~63–64) vs `phase-3-2-2-...-1735.md` P1–P6 table.
2. **Task honesty:** Two unchecked Tasks on **3.2.2** are correct as open work; risk is **false completion** or narrative that treats slice as closed while HR 92 < min_handoff_conf 93.
3. **Automation trace gap:** `roadmap-state.md` § **2026-03-22 17:35** lacks concrete validator/IRA links (placeholder text).
4. **TBD sprawl:** Canonical hashing formula and registry rows remain **TBD** without a single owning deferral anchor in decisions-log (feeds `safety_unknown_gap`).

## Proposed fixes

See structured `suggested_fixes` in parent return (low → medium → high apply order for Roadmap subagent).

## Notes for future tuning

- **Post-first-pass IRA** surfaced a recurring pattern: decision rows that claim "supersedes / aligned" before sibling note bodies are patched — consider a little-val or validator grep for "aligned in-vault" cross-checked against linked note anchors.
- **Handoff vs execution readiness:** Keep `handoff_readiness` honest below `min_handoff_conf` but ensure **no** downstream copy implies gate passage (validator already flagged this).
