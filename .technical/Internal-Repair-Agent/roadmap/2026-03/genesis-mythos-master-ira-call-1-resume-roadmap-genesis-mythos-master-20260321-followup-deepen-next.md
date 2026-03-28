---
created: 2026-03-21
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-roadmap-genesis-mythos-master-20260321-followup-deepen-next
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 4
  medium: 3
  high: 1
validator_report_path: .technical/Validator/roadmap-auto-validation-20260321T225000Z.md
parent_run_id: pr-eatq-20260321-gmm-deepen
---

# IRA report — roadmap / RESUME_ROADMAP deepen (validator to IRA #1)

## Context

RoadmapSubagent invoked IRA after the first nested `roadmap_handoff_auto` pass (`ira_after_first_pass: true`). Verdict: **medium**, **needs_work**, primary **`missing_acceptance_criteria`**, also **`safety_unknown_gap`**. Canonical state files agree on `current_subphase_index: 2.3.1`; the failure is **scoring and acceptance closure**, not state hygiene. Tertiary **2.3.1** combines **`handoff_readiness: 94`** with **TBD floor F**, **EXAMPLE** JSON paths, and a **placeholder** emergence hash; secondary **2.3** remains **82** vs **min_handoff_conf 93** while tasks are checked and stub rows read **TBD**. **D-022** / **D-023** correctly document deferral but do not close the automation loop for delegatable handoff.

## Structural discrepancies

1. **Credibility gap (tertiary):** `handoff_readiness: 94` reads like rollup or delegatable readiness while pseudo-code states **F is TBD** and the seed matrix row is **EXAMPLE** plus placeholder hash.
2. **Predicate gap:** Property or acceptance language implies matching when paths are allow-listed, but path cells still use **EXAMPLE** paths; the predicate is not satisfiable from repo truth yet.
3. **Altitude tension (secondary vs tertiary):** Secondary `handoff_readiness: 82` vs tertiary **94** without an explicit cross-note **rubric** mixes signals for automation and humans.
4. **Narrative drift (roadmap-state):** Latest consistency report line claims tertiary **94 ≥ 93** alongside EMG-2 **F** gap; incompatible unless a **draft-score contract** is explicit.
5. **Progress-theater risk (secondary):** Checked tasks plus stub table **TBD** rows lack a one-line caption tying status to **freeze state** versus **draft in 2.3.1**.
6. **Decisions-log:** D-022 and D-023 are honest stubs; they lack a compact **promotion checklist** tying D-022 adoption to frozen paths plus numeric **F**.

## Proposed fixes (for parent to apply)

Apply in **low → medium → high** order when snapshots and gates allow. Targets are roadmap notes under `1-Projects/genesis-mythos-master/Roadmap/` only.

| # | risk | action_type | target | summary |
|---|------|-------------|--------|---------|
| 1 | low | adjust_frontmatter | phase-2-3-1-emg-normative-schema-bindings-and-seed-matrix-v0-roadmap-2026-03-21-2205.md | Add **`handoff_readiness_scope`** (or equivalent): **94 = structural / spec-draft completeness**, not execution-closed handoff until **F**, frozen paths, non-placeholder hash. Expand **`handoff_gaps`**: **F TBD**, **EXAMPLE paths**, **placeholder hash**. |
| 2 | low | recompute_phase_metadata | same 2.3.1 note | Retitle seed matrix section to **illustrative / non-normative until freeze**; label EXAMPLE path and placeholder hash as non-normative (align with D-023). |
| 3 | low | adjust_frontmatter | phase-2-3-validate-co-authored-world-emergence-through-test-seeds-roadmap-2026-03-21-2025.md | Caption under EMG stub table: rows = freeze state; draft bindings in [[phase-2-3-1-emg-normative-schema-bindings-and-seed-matrix-v0-roadmap-2026-03-21-2205]]. |
| 4 | medium | rewrite_log_entry | roadmap-state.md | Rephrase **2026-03-21 22:05** bullet: do not imply **min_handoff_conf 93** met for delegatable execution while F/paths TBD. **Constraint:** edit that subsection only; keep snapshot links. |
| 5 | medium | adjust_frontmatter | 2.3.1 note | **Alt to fix 1:** lower **`handoff_readiness`** to mid-70s–low-80s until F committed. Do not keep contradictory 94 + lowered score without reconciliation. |
| 6 | medium | recompute_phase_metadata | 2.3.1 note | Path binding appendix: symbolic names → wiki links to pseudo-code / Phase 2.2.x rows (paths may stay proposed). |
| 7 | low | write_log_entry | decisions-log.md | Under D-022/D-023: **Promotion checklist** — frozen lore/counter paths; numeric F; real emergence hash; then adopt with evidence. |
| 8 | high | recompute_phase_metadata | 2.3.1 + decisions-log | **Only after owner sign-off:** commit F, freeze paths, real hash, version EMG2 formula; D-022 adoption. **Constraints:** snapshot gates; never invent F/paths. |

## Notes for future tuning

- Split draft vs execution readiness fields on tertiaries.
- Hand-off-audit: treat EXAMPLE/TBD acceptance as execution-block unless scope says draft.
- Deepen template: caption for secondary stubs when TBD persists.

## Machine-readable summary

```json
{
  "status": "repair_plan",
  "ira_call_index": 1,
  "suggested_fix_count": 8,
  "primary_validator_code": "missing_acceptance_criteria"
}
```
