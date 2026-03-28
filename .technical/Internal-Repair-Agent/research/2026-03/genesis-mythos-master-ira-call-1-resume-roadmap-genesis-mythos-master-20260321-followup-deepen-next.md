---
created: 2026-03-21
pipeline: research
project_id: genesis-mythos-master
queue_entry_id: resume-roadmap-genesis-mythos-master-20260321-followup-deepen-next
ira_call_index: 1
status: repair_plan
risk_summary: { low: 2, medium: 4, high: 0 }
validator_report_path: 3-Resources/Second-Brain/Validator-Reports/research_synthesis/genesis-mythos-master-20260321T233500Z.md
reason_codes: [safety_unknown_gap]
---

# IRA — research (validator first pass)

## Context

Post–nested-validator cycle (`ira_after_first_pass: true`) for `research_synthesis` on `phase-2-3-1-emg-schema-bindings-research-2026-03-21-2310.md`. Verdict: `needs_work`, `safety_unknown_gap`. Contaminated-report rule: treat validator output as a weak lower bound. Repairs are scoped to the synthesis note, its raw bundle, and the nested research Run-Telemetry mirror only (no roadmap phase notes, PMG, or roadmap-state).

## Structural discrepancies

1. **Normative safety hole:** Phase 2.3 objectives require documenting **float / GPU fence** before hashing derived emergence state; the synthesis never specifies when EMG-1 hashing is allowed vs forbidden, or how non-bit-exact paths interact with allow-lists and `tolerance_tier`.
2. **Evidence ladder:** A Medium general testing article is presented at the same rhetorical level as RFC 8785 and primary tooling docs, inflating perceived authority for a fail-closed sim contract.
3. **Self-admitted incompleteness:** Section 5 lists "next artifacts" as bullets only; the validator treats that as the synthesis still **promising** tertiary deliverables without delivering **draft** table / EXAMPLE row / alphabet in-vault (within allowed paths, embed drafts in the synthesis note).
4. **Raw gap:** Raw bundle omits captures for **FP / GPU determinism** primaries; synthesis cannot cite what raw does not hold.
5. **Telemetry gap:** Nested research telemetry does not record validator `needs_work` / IRA handoff for traceability.

## Proposed fixes

See parent return `suggested_fixes` (mirrored intent). Apply low-risk items first; snapshot or backup per vault policy before editing Ingest notes.

## Notes for future tuning

- Research skill should default-include a **determinism tier** subsection whenever `replay_*hash` or canonical bytes appear in the query or parent phase objectives.
- Template a **source tier** callout (normative / tooling / optional blog) in agent-research notes to prevent evidence inflation.
