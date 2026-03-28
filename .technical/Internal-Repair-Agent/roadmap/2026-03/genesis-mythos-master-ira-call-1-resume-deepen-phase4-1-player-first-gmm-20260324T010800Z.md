---
created: 2026-03-24
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-deepen-phase4-1-player-first-gmm-20260324T010800Z
parent_task_correlation_id: 984ca677-0f9f-44dd-a0e3-e10ab1e19522
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 3
  medium: 1
  high: 0
validator_report_path: .technical/Validator/roadmap-auto-validation-20260324T021200Z-p4-1-secondary-first.md
validator_primary_code: missing_roll_up_gates
---

# IRA — roadmap — genesis-mythos-master — post-validator pass 1

## Context

RoadmapSubagent completed nested **`roadmap_handoff_auto`** (Phase **4.1** secondary, first pass). Verdict: **`severity: medium`**, **`recommended_action: needs_work`**; primary code **`missing_roll_up_gates`**, with **`missing_acceptance_criteria`** and **`safety_unknown_gap`**. State is internally consistent (no incoherence / block_destructive). **`ira_after_first_pass: true`** — this IRA cycle supplies **concrete vault-honest documentation fixes** so the second validator pass can compare against the same report without expecting fake **REGISTRY-CI PASS**, **rollup HR ≥ 93**, or new **D-044** / **D-059** outcomes.

## Structural discrepancies (expanded beyond validator minimum)

1. **Roll-up table is a naked stub:** **`G-P4-1-ADAPTER-CORE`** / **`G-P4-1-RIG-NEXT`** lack an explicit **FAIL** status, **numbered closure gaps**, and **checkable acceptance criteria** that a junior can verify in-vault without implying repo CI.
2. **T-P4-04** WBS row is still generic "placeholder" prose — missing explicit **`@skipUntil(D-032)`** ownership, link to **`replay_row_version`** coordination on **3.1.1**, and explicit "no golden / no Lane-C until D-032" language already true elsewhere on the note.
3. **`safety_unknown_gap`:** Pre-deepen research is **non-normative**; drift scalars are **qualitative_audit_v0** (already noted in **roadmap-state**). Traceability for **deferred nested `research_synthesis`** should be echoed on the **phase 4.1 secondary** surface or **roadmap-state Notes** so the hole is explicit, not only in validator prose.
4. **distilled-core** Phase **4.1** bullets still show **HR 84** in places while the canonical phase note frontmatter has **`handoff_readiness: 87`** — documentation drift (not a numeric gate claim).

## Proposed fixes (for RoadmapSubagent apply order: low → medium)

See structured **`suggested_fixes`** in the parent return block. Summary:

| # | Target | Risk | Intent |
|---|--------|------|--------|
| 1 | Phase 4.1 secondary note | medium | Replace naked roll-up stub with **Status = FAIL (stub)**, **numbered gap list**, and **explicit AC bullets** per gate (vault-checkable only). |
| 2 | Phase 4.1 secondary note | low | Rewrite **T-P4-04** evidence row: **D-032**-blocked stub plan + **3.1.1** link; no CI/golden claims. |
| 3 | roadmap-state.md Notes | low | One bullet: cite validator path, reason codes, **research_synthesis** deferral / non-normative research. |
| 4 | distilled-core.md | low | Align Phase **4.1** **HR** to **87**; add one clause: **G-P4-1-*** roll-up rows remain **FAIL/stub** until evidence. |

## Notes for future tuning

- Secondary notes should default to **Status column** (**PASS** / **FAIL (stub)**) on roll-up tables whenever **`min_handoff_conf`** is in play — avoids "stub" sections with no machine-readable posture.
- **T-P4-*** rows should always carry **`@skipUntil(D-xxx)`** when literals are deferred, not the word "Placeholder" alone.
