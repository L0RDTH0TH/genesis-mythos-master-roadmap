---
created: 2026-03-22
pipeline: research
project_id: genesis-mythos-master
queue_entry_id: resume-roadmap-genesis-mythos-master-20260322-deepen-followup-suggested-246
ira_call_index: 1
status: repair_plan
risk_summary: { low: 4, medium: 4, high: 1 }
parent_run_id: pr-eatq-20260322T2355Z-resume-genesis-246
validator_report_path: 3-Resources/Second-Brain/Validator-Reports/research_synthesis/genesis-mythos-master-20260322T235900Z-research-synthesis-first.md
primary_code: safety_unknown_gap
---

# IRA report — research (validator-driven) — call 1

## Context

Post–first-pass `research_synthesis` validation returned **severity medium**, **recommended_action needs_work**, **primary_code safety_unknown_gap**. The synthesis note `Ingest/Agent-Research/phase-3-3-2-persistence-bundle-versioning-research-2026-03-22.md` is structurally valid markdown but **under-delivers** on its own §5 artifact list, leaves §6 as bare TBDs while claiming **`research_focus: junior_handoff`** and **`research_escalations_used: 0`**, and mixes **vendor-grade** citations with a **single-author blog** without epistemic tiering. This IRA pass proposes **in-note-only** repairs (caller applies under `Ingest/Agent-Research/**`); no edits to roadmap phase notes or `decisions-log.md` in this pass.

## Structural discrepancies

1. **Definition-of-done gap:** §5 promises `CompatibilityMatrix_v0` example, migration playbook, and concrete stubs; body contains **none** of these (only prose + tables).
2. **Unresolved safety decisions exposed as TBD:** §6 lists three blocking choices (on-disk format, matrix placement, regen-lane interaction) with **no default hypothesis** or traceability path for juniors.
3. **Evidence weighting:** youngju.dev is presented **peer** to Axon/protobuf.dev without **tier labels** or demotion to supplementary.
4. **Metadata vs content:** `junior_handoff` + zero escalations **contradicts** explicit “not closed” gaps and missing stubs.
5. **Dependency narrative:** Golden vectors blocked on D-032/D-043 is named; validator asks for **parallel clarity** on what remains unblocked for 3.3.2 drafting.
6. **Sparse matrix:** §2 defines abstract row/column model but lacks **one concrete evaluated row** (even fictional IDs).

## Proposed fixes

See structured return `suggested_fixes[]` in parent hand-off consumption; each maps 1:1 to an apply step on the research note path only.

## Notes for future tuning

- **Research synthesis validator → IRA:** When `research_focus: junior_handoff`, treat empty §5 stubs as **automatic** `safety_unknown_gap` unless an explicit “deferred to child note” subsection exists with a linked path.
- **Citation linter (optional):** Tag external links in agent-research notes with `evidence_tier: primary|secondary|opinion` in a small convention to prevent blog-as-vendor inflation.
- **Escalation semantics:** If the run stops with open product decisions, `research_escalations_used` should reflect **internal escalation to IRA/repair** or **explicit user-visible deferral**, not stay at `0` by default.
