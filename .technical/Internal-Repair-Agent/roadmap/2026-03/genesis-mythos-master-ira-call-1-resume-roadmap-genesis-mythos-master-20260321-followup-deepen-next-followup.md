---
created: 2026-03-21
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-roadmap-genesis-mythos-master-20260321-followup-deepen-next-followup
parent_run_id: eatq-20260321-gmm-l1-2249
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 3
  medium: 4
  high: 1
validator_report_path: .technical/Validator/roadmap-auto-validation-20260321T230500Z.md
---

# IRA report — roadmap / RESUME_ROADMAP — genesis-mythos-master (call 1)

## Context

Post–first-pass `roadmap_handoff_auto` for Phase 2.3.3 (`ira_after_first_pass: true`). Validator returned **medium / needs_work** with primary **`missing_task_decomposition`** plus **`missing_risk_register_v0`** and **`safety_unknown_gap`**. State files (`workflow_state`, `roadmap-state`, `decisions-log` D-025) are **internally consistent**; the gap is **tertiary execution honesty**: `handoff_readiness: 94` is scoped to normative design in frontmatter, but **all Tasks checkboxes are open**, there is **no risk table**, **no enum↔harness mapping**, **no WA run log**, and **no registry row or approved stand-in** beyond narrative TBD. Per contaminated-report rule, treat validator gaps as a **weak minimum** — expect additional blind spots (e.g. readers skimming only the score, missing link from research synthesis to checkable artifacts).

## Structural discrepancies

1. **Task surface vs delegatability:** Four coarse tasks are all `[ ]` with no vault-completable substeps; validator understates “no closed execution steps.”
2. **Risk posture:** `handoff_gaps` mentions enum drift but there is no **Risk register v0** (owner / mitigation / review trigger).
3. **Score semantics:** `handoff_readiness_scope` exists, but **`safety_unknown_gap`** correctly flags that **94** can be misread as junior-ready for VCS/CI without a paired **execution** readiness signal.
4. **Registry bridge:** D-025 admits wiki **G-EMG2-*** pending; validator allows **deferral with decision id + owner + expiry** — that explicit deferral row is not present in the Phase 2.2.3 registry table (only implied in 2.3.3 prose).
5. **WA matrix:** Intent documented; **no logged run** or explicit “not yet executed” ledger in the slice note.
6. **Enum contract:** No table mapping `golden_expectations.reason_code` strings to implementation enums (validator next_artifact).

## Proposed fixes (for RoadmapSubagent to apply under guardrails)

Apply in stable order **low → medium → high** when snapshots and confidence gates pass. Skip individual steps only when a gate fails, not because of risk label alone.

| # | risk | action_type | target_path | description |
|---|------|-------------|-------------|-------------|
| 1 | low | adjust_frontmatter | phase-2-3-3-emg-2-ci-golden-registry-row-and-fixture-hardening-roadmap-2026-03-21-2249.md | Add **`execution_handoff_readiness`** (integer 0–100 or string tier) **or** dual keys **`normative_handoff_readiness`** / **`execution_handoff_readiness`** so the numeric **94** cannot be read as VCS closure. Optional top-of-body `[!warning]` mirroring scope. |
| 2 | low | append_section | same | **## Risk register (v0)** — table: Risk, Owner, Mitigation, Review trigger/date. |
| 3 | low | append_section | same | **## Harness enum contract (v0)** — `golden_expectations.reason_code` ↔ implementation enum literal; link 2.3.2 outcomes. |
| 4 | medium | rewrite_section | same — `### Tasks` | **Decompose** tasks into **vault-now** vs **VCS-PR** substeps; **Vault fixture stand-ins** (fenced JSON from research synthesis); check off vault work only. |
| 5 | medium | write_log_entry | decisions-log.md | **D-026:** approved vault stand-in until VCS; owner; expiry; link to canonical JSON; CI still required for execution readiness. |
| 6 | medium | append_section | phase-2-2-3-ci-golden-registry-and-boundary-regression-gates-roadmap-2026-03-21-1205.md | **G-EMG2-ALIGN** row **DEFERRED** + owner + expiry + links to 2.3.3 / D-026. |
| 7 | medium | append_section | phase 2.3.3 note | **## WA matrix execution log** — first row **PENDING** / **NOT RUN**. |
| 8 | high | adjust_frontmatter | distilled-core.md | Phase 2.3 bullet: **dual readiness** + D-026 + risk register; sync `core_decisions` with body. |

**Constraints:** Snapshot targets before structural edits; re-run little val → final validator with `compare_to_report_path` pointing at initial report.

## Notes for future tuning

- Lint: `handoff_readiness ≥ 90` with `progress: 0` and all tasks open → warn on CI slices.
- Schema: optional `execution_handoff_readiness` in validator expectations for tertiary EMG notes.

Full paths under vault: `1-Projects/genesis-mythos-master/Roadmap/...` (see JSON in parent agent return).
