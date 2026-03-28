---
created: 2026-03-24
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: repair-handoff-audit-state-hygiene-layer1-20260324T031800Z
ira_call_index: 1
status: repair_plan
risk_summary: { low: 3, medium: 3, high: 1 }
validator_report_path: .technical/Validator/roadmap-handoff-auto-genesis-mythos-master-20260324T034500Z-repair-state-hygiene-followup.md
ira_after_first_pass: true
---

# IRA — roadmap (validator first pass) — genesis-mythos-master

## Context

Post–state-hygiene **`roadmap_handoff_auto`** report **`.technical/Validator/roadmap-handoff-auto-genesis-mythos-master-20260324T034500Z-repair-state-hygiene-followup.md`** returns **medium / `needs_work`** with **`primary_code: missing_roll_up_gates`** and **`missing_acceptance_criteria`**, **`safety_unknown_gap`**. Phase **4.1** secondary [[phase-4-1-player-first-perspective-read-model-and-rig-contracts-roadmap-2026-03-24-1201]] already documents **HR 87 < 93**, **REGISTRY-CI HOLD**, and **D-062** honesty guards; tertiary **4.1.1** / **4.1.1.1** contain preimage + registry sketch. Operator constraint for this cycle: **doc-only / traceability fixes only** — **do not** fabricate **CI PASS**, **REGISTRY-CI PASS**, or rollup **PASS** rows that imply macro closure.

## Structural discrepancies

1. **Roll-up table vs acceptance bullets:** The **Acceptance criteria (vault-only)** subsection already wiki-links **4.1.1**, **4.1.1.1**, and **decisions-log**, but the **Roll-up gate** table still shows **FAIL (stub)** without an **evidence column** — hostile readers treat that as missing links even though links exist below.
2. **Executable vs vault-only:** **`missing_acceptance_criteria`** (residual) is the **T-P4-04** / **Lane-C** / **ReplayAndVerify** slice under **`@skipUntil(D-032)`**; vault-only bullets can be misread as replay acceptance closed.
3. **`safety_unknown_gap`:** Qualitative drift scalars and **D-032/D-043** literal replay unknowns are partly in [[roadmap-state]] Notes but should be surfaced on the **4.1 secondary** in one compact traceability line.
4. **Cross-phase:** Validator next-artifact **4** requires **Phase 4 primary** not to silently absorb **4.1** work as clearing **G-P4-PLAYER** / **G-P4-REGISTRY-CI** — confirm explicit cross-link if absent or stale.

## Proposed fixes

See structured **`suggested_fixes`** in the parent agent return. Ordered **low → medium → high** by blast radius. **None** of these change gate rows to **PASS**; they improve honest labeling, evidence density, and audit traceability.

## Notes for future tuning

- Consider a template pattern for secondary notes: rollup table always includes **Evidence (wikilinks)** + **Macro blocked by** columns so **`missing_roll_up_gates`** is not triggered by table-vs-prose split.
- When **`drift_metric_kind: qualitative_audit_v0`**, duplicate a one-line comparability guard on secondaries that emit **handoff_readiness** to reduce **`safety_unknown_gap`** noise.
