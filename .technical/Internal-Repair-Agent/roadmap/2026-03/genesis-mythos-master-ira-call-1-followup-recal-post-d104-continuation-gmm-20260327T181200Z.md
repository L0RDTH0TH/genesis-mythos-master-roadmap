---
created: 2026-03-27
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: followup-recal-post-d104-continuation-gmm-20260327T181200Z
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 2
  medium: 1
  high: 0
---

## Context

IRA invoked post-first-validator for `RESUME_ROADMAP` with `action: recal` on conceptual track. Validator result is advisory (`needs_work`, `primary_code: missing_roll_up_gates`) and explicitly preserves conceptual non-closure semantics. Goal here is coherence/parity improvement only, with no execution closure inflation.

## Structural discrepancies

1. Advisory debt tuple appears repeatedly but is not consistently anchored to one canonical wording block across all core surfaces.
2. The validator asks for explicit mapping from conceptual 4.1.5 contract rows to future execution proof points; current references exist, but mapping is diffuse rather than bounded in one artifact.
3. Cross-surface parity appears maintained, but there is no single machine-checkable parity checklist line that can be re-used in future recal runs.

## Proposed fixes

1. **Create a bounded parity mapping artifact for 4.1.5 (conceptual-only).**
   - `action_type`: `recompute_phase_metadata`
   - `target_path`: `1-Projects/genesis-mythos-master/Roadmap/phase-4-1-5-control-selection-observability-and-advisory-gates-roadmap-2026-03-27-0320.md`
   - `risk_level`: `medium`
   - `description`: Add one compact "Conceptual->Execution Proof Map (advisory)" table linking each active 4.1.5 conceptual contract row to required execution evidence loci (repo/CI/proof artifact placeholders), with all rows marked `execution-deferred` and `not closure evidence`.
   - `constraints`:
     - Preserve explicit text: `rollup HR 92 < 93`, `REGISTRY-CI HOLD`, `missing_roll_up_gates`, `safety_unknown_gap` as OPEN/advisory.
     - Do not add PASS/closed wording for rollup or registry gates.

2. **Normalize one canonical advisory debt tuple in `roadmap-state` run narrative.**
   - `action_type`: `rewrite_log_entry`
   - `target_path`: `1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md`
   - `risk_level`: `low`
   - `description`: Ensure the current recal run narrative includes a single canonical debt tuple string and references the same tuple format used in validator report and workflow row, reducing drift in future audits.
   - `constraints`:
     - Narrative-only normalization; no machine cursor changes.
     - Keep `effective_track: conceptual` and advisory framing intact.

3. **Add parity checksum line in `workflow_state` for this recal row.**
   - `action_type`: `set_context_metrics`
   - `target_path`: `1-Projects/genesis-mythos-master/Roadmap/workflow_state.md`
   - `risk_level`: `low`
   - `description`: Append a short parity-check clause for the `followup-recal-post-d104-continuation...` row indicating `(roadmap-state debt tuple == workflow_state debt tuple == distilled-core debt tuple)` to make later validator checks mechanically easier.
   - `constraints`:
     - Must include `no machine cursor advance`.
     - Must not alter `handoff_readiness`, thresholds, or gate verdict values.

## Notes for future tuning

- Repeated advisory tuple drift is a recurring source of `needs_work` despite conceptually-correct runs; a reusable "advisory debt tuple macro" could reduce false variance.
- For conceptual recal actions, validator expectations are best met by bounded parity artifacts, not additional closure language.
