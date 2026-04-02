---
created: 2026-04-02
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-deepen-phase3-312-followup-gmm-20260402T002000Z
ira_call_index: 1
status: repair_plan
risk_summary: { low: 3, medium: 1, high: 0 }
validator_report_path: .technical/Validator/roadmap-handoff-auto-gmm-20260402T002500Z-conceptual-v1-phase-312.md
---

# IRA — roadmap / RESUME_ROADMAP deepen 3.1.2 (validator first pass)

## Context

RoadmapSubagent invoked IRA after nested `roadmap_handoff_auto` pass with `primary_code: safety_unknown_gap`, `recommended_action: needs_work`, `severity: medium`. The validator flagged a **traceability gap**: `decisions-log` and CDR used **`pattern_only`** while the phase note asserted **high `handoff_readiness`** (86 at validation time; parent applied **85**) and an unexplained **`progress`** (46 → parent applied **48**). On-disk review: the **3.1.2** phase note and CDR **Validation evidence** section were partially updated; **`validation_status: pattern_only`** remains on the CDR and the **decisions-log** row still uses the **bare** `validation: pattern_only` token without the reconciling clause the validator asked for. Second pass should compare against the initial report path above.

## Structural discrepancies (post–parent partial apply)

1. **Evidence class vs readiness (residual):** `pattern_only` is still the **canonical label** in CDR frontmatter and decisions-log, while **`handoff_readiness: 85`** reads as “strong handoff.” The expanded CDR prose **explains** the meaning (no `Ingest/Agent-Research/` notes; NL + GWT completeness), but **decisions-log** does not yet **point** to that interpretation in the one-line decision record row—so a hostile compare can still treat this as `safety_unknown_gap` unless the row is tightened or an explicit in-note exception rule is added per validator §1e.
2. **`progress: 48`:** Numeric value moved from 46 to 48 but **semantics** are still not declared in frontmatter or a stable field—validator asked for defined meaning or removal.

## Proposed fixes (for RoadmapSubagent to apply under gates)

| # | risk | action_type | target_path | description |
|---|------|-------------|-------------|-------------|
| 1 | low | rewrite_log_entry | `1-Projects/genesis-mythos-master/Roadmap/decisions-log.md` | On the **Decision record (deepen)** line for `resume-deepen-phase3-312-followup-gmm-20260402T002000Z`, replace bare `validation: pattern_only` with a **reconciling fragment**, e.g. `validation: pattern_only — conceptual NL+GWT complete; no Agent-Research synthesis (see CDR § Validation evidence)`. Ensures the log **cannot** be read as “weak evidence” paired with **85** without pointer. **Constraints:** single-line edit; preserve queue_entry_id link. |
| 2 | low | adjust_frontmatter | `1-Projects/genesis-mythos-master/Roadmap/Conceptual-Decision-Records/deepen-phase-3-1-2-tertiary-tick-scheduling-defer-merge-2026-04-02-0020.md` | Add **additive** frontmatter (do not remove `validation_status` if tooling depends on it), e.g. `readiness_basis: conceptual_nl_gwt_peer_parity` or `handoff_readiness_aligned: true` **or** rename `validation_status` only if conceptual-decision-record skill / Parameters allow a richer enum—otherwise keep `pattern_only` and rely on fix 1 + 3. **Constraints:** snapshot before edit; check skill contract. |
| 3 | low | adjust_frontmatter | `1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Sim-Tick-and-Event-Bus-Spine/Phase-3-1-2-Tick-Scheduling-Defer-Merge-and-Work-Queue-Policy-Roadmap-2026-04-02-0020.md` | Add `progress_semantics: slice_local_tertiary_pct` (or one sentence in `handoff_readiness_note`) so **48** is not arbitrary—e.g. “percent of **this slice’s** required headings/GWT rows satisfied; remaining Phase 3.1 chain is **not** included.” **Constraints:** per-change snapshot if overwriting body/callout. |
| 4 | medium | append_audit_callout | Same phase note path | In `#handoff-review`, add **one explicit sentence**: high readiness here means **conceptual checklist + GWT completeness**, not external-research synthesis; **`pattern_only`** in CDR = no Agent-Research notes—**not** a downgrade of NL depth. Satisfies validator “written exception rule in-note.” **Constraints:** append-only or small callout edit after snapshot. |

## Notes for future tuning

- **Pattern:** Many CDRs use `pattern_only`; peer **handoff_readiness ~85** is normal for conceptual tertiary. Consider a **standard decisions-log suffix** template in Parameters or conceptual-decision-record so `pattern_only` never appears **bare** next to high readiness.
- **Progress:** If `progress` stays numeric, document **one** vault-wide semantics (Parameters § roadmap progress) to avoid repeated `safety_unknown_gap`.

## Rationale (summary)

Parent fixes (85, 48, expanded CDR evidence) **narrow** the gap but do not fully satisfy the validator’s **definition of done** until **decisions-log** and/or phase note **explicitly reconcile** the `pattern_only` label with **85** readiness and **`progress`** meaning. Fixes 1–4 are minimal, ordered **low → medium**, and align with `next_artifacts` from the initial report.
