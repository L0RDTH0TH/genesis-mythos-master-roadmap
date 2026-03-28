---
created: 2026-03-22
pipeline: research
project_id: genesis-mythos-master
queue_entry_id: resume-roadmap-genesis-mythos-master-20260322-deepen-followup-suggested-247
ira_call_index: 1
status: repair_plan
risk_summary: { low: 4, medium: 2, high: 0 }
validator_report: .technical/Validator/research-synthesis-genesis-mythos-master-20260322T081500Z.md
synth_note: Ingest/Agent-Research/phase-3-3-3-migration-playbook-golden-harness-research-2026-03-22-0815.md
parent_run_id: l1-eatq-20260322-8c4e91a0
---

# IRA — research (validator-driven, call 1)

## Context

Nested Research run for `genesis-mythos-master`, hand-off `linked_phase: Phase-3-3-3-migration-playbook-execution-and-golden-harness`, queue entry `resume-roadmap-genesis-mythos-master-20260322-deepen-followup-suggested-247`. Invoked after first-pass `research_synthesis` validator with `primary_code: safety_unknown_gap`, `missing_task_decomposition`, severity medium, `needs_work`. Validator output is treated as a **minimum** bar; gaps expanded per IRA mandate.

## Structural discrepancies

1. **Overclaim / safety_unknown_gap:** Protobuf migration doc cited as if it normatively constrains project `migration_id` registry columns; it is at best a **Tier C analogy**.
2. **Process gap vs 3.3.2 research integration:** Body lacks explicit **Tier A / B / C** labeling on claim blocks; only a flat Sources list.
3. **missing_task_decomposition:** Golden harness describes a largely happy path; no explicit **negative fixture matrix** (INCOMPATIBLE, registry mismatch, regen-lane open, trace/version dishonesty) with expected fail-closed outcomes.
4. **3.3.1 step collapse:** Harness step 4 bundles "step 2 + dual-hash steps" without matching `phase-3-3-1` algorithm numbering (matrix vs dual-hash as distinct post-migration checks).
5. **Traceability:** `linked_phase` string does not resolve to an in-repo roadmap file; synthesis cannot fix the missing `1-Projects/.../Roadmap/` artifact under IRA path constraints — must be **surfaced inside the synthesis** as an explicit hand-off dependency for Roadmap/deepen.

## Proposed fixes (for Research caller to apply)

| # | Risk | Target | Summary |
|---|------|--------|---------|
| 1 | low | synthesis note | Insert Tier A/B/C legend; prefix major sections (sections 1–5) with tier tags. |
| 2 | low | synthesis note | Rewrite Protobuf paragraph: Tier C, "analogy only," no "upstream stresses your registry shape." |
| 3 | low | synthesis note | Replace harness section 3 step 4 with explicit ordered checklist: re-run matrix (3.3.1 step 2) on post-migration bundle, then dual-hash verification (step 3), then idempotency or rehydrate guards per 3.3.1 sketch. |
| 4 | medium | synthesis note | Add "Negative and regen-lane fixtures" subsection: at least three scenarios with expected codes (INCOMPATIBLE with no migration; MIGRATE_REQUIRED with registry or step mismatch; regen lane not closed per 3.2.x ordering; optional trace missing versus claimed version). |
| 5 | low | synthesis note | Add second external cite for golden or snapshot drift policy (for example Jest snapshots, pytest-snapshot, or an institutional update-goldens runbook) as Tier B. |
| 6 | medium | synthesis note | Add "Hand-off traceability (Tier C)" block: state that Phase 3.3.3 roadmap note path is absent in vault; deepen must create canonical note or retarget `linked_phase`; do not treat this synthesis as canonical anchor until resolved. |

## Notes for future tuning

- Research validator first-pass plus `ira_after_first_pass` should keep flagging **analogy-as-evidence** when external URLs support internal enums.
- Consider a **research_synthesis** lint: every `linked_phase` slug should either resolve to a wiki path in the synthesis frontmatter or carry `roadmap_anchor_pending: true`.
