---
created: 2026-03-27
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-deepen-post-d110-temporal-coherence-gmm-20260327T190700Z
ira_call_index: 1
status: repair_plan
risk_summary: { low: 1, medium: 1, high: 2 }
---

# IRA — genesis-mythos-master (validator-driven, call 1)

## Context

RoadmapSubagent invoked IRA after the first nested `roadmap_handoff_auto` pass (`ira_after_first_pass: true`). The validator report at `.technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260327T190700Z-d110-deepen-first.md` records **`severity: medium`**, **`recommended_action: needs_work`**, **`primary_code: missing_roll_up_gates`**, plus **`safety_unknown_gap`**. Cross-surface machine cursor authority is **aligned** (workflow_state frontmatter, roadmap-state stamps, distilled-core parity strings, phase 4.1.5 note / D-114). Residual codes reflect **honest execution-deferred** rollup/registry/replay debt on **conceptual_v1**, not a broken structural contract.

## Structural discrepancies

1. **Dominant code (`missing_roll_up_gates`)**: Phase note `handoff_gaps` and unchecked acceptance item still record D-032/D-043 literals and REGISTRY-CI / HR<93 — **intentional** on conceptual track; validator correctly refuses to certify execution closure.
2. **`safety_unknown_gap`**: End-to-end audit replay closure remains outside the observability slice; traceability is present, definition-of-done at repo boundary is not closed.
3. **Reader hazard (optional hardening)**: `workflow_state.md` **Log** row **2026-03-27 20:10** (D-111 / `handoff-audit`) still narrates **"terminal live cursor after D-112 deepen"** with older queue ids. Live authority is **`last_auto_iteration: resume-deepen-post-d110-temporal-coherence-gmm-20260327T190700Z`** @ **4.1.5** per frontmatter and **D-114** (newer **19:07** deepen row supersedes D-112 as "terminal" for skimmers). This is **not** a YAML contradiction but **ankle-biting** prose per validator section (1d).

## Proposed fixes (for Roadmap subagent / operator — IRA does not apply)

| # | risk | action_type | target_path | description |
|---|------|-------------|-------------|-------------|
| 1 | low | rewrite_log_entry | `1-Projects/genesis-mythos-master/Roadmap/workflow_state.md` | In the **Status / Next** cell for the **2026-03-27 20:10** row, replace the "terminal live cursor after D-112 deepen …" phrasing with **explicit deferral to YAML + D-114**: e.g. state that **live machine cursor** = frontmatter **`last_auto_iteration`** + **`current_subphase_index`**, with **D-114** (`resume-deepen-post-d110-temporal-coherence-gmm-20260327T190700Z`) as the current terminal deepen anchor; keep D-111/D-112 as **historical audit** context only. |
| 2 | medium | write_log_entry | `1-Projects/genesis-mythos-master/Roadmap/decisions-log.md` | **If** the operator chooses a **documented policy exception** for REGISTRY-CI HOLD (validator next_artifact 1d first bullet), append a **scoped** decision with **expiry**, **owner**, and **what evidence would satisfy** — vault prose alone does not clear the hold. |
| 3 | high | cross_track_followup | execution repo / CI (out of vault) | Materialize **REGISTRY-CI** evidence per rollup tables **or** treat as explicit migration work to execution track — **not** a single conceptual deepen edit. |
| 4 | high | owner_bound_artifact | TBD path (vault or repo) | **D-032 / D-043 bridge:** minimal replay-literal freeze **or** dated `@skipUntil(D-032)` unblock criteria **with measurable exit** — requires owner binding; cannot be "fixed" by tightening observability prose alone. |

### Constraints (fix #1)

- **Only** after **per-change snapshot** of `workflow_state.md` per core guardrails.
- **Do not** change **Timestamp**, **Action**, or **Iter Phase** columns unless a separate reconciliation audit proves error.
- **Do not** change frontmatter **`last_auto_iteration`** in the same edit unless a separate machine-cursor advance is intended (this IRA is **skimmer prose only**).

## Notes for future tuning

- **`missing_roll_up_gates`** will recur on **conceptual_v1** while rollup/CI debt is vault-honest; treat **`needs_work`** as **expected** unless execution artifacts land — second validator pass should **`compare_to_report_path`** and diff **only** new drift, not re-litigate deferred gates.
- Consider a **lint** or deepen template reminder: **historical** `handoff-audit` rows should **append** "superseded by D-11x / YAML" when a newer deepen row advances the cursor.

## IRA outcome

**status:** `repair_plan` — one **low**-risk skimmer fix is actionable; rollup/registry/replay items remain **execution-deferred** (medium/high follow-ups), consistent with the validator's own conceptual-track interpretation.
