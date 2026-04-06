---
created: 2026-04-07
pipeline: roadmap
project_id: sandbox-genesis-mythos-master
queue_entry_id: validator-duplicate-drain-20260407T231500Z
ira_call_index: 1
status: repair_plan
risk_summary: { low: 1, medium: 5, high: 0 }
validator_report_path: .technical/Validator/roadmap-handoff-auto-sandbox-gmm-20260407T231500Z-conceptual-v1-duplicate-drain.md
---

# IRA — sandbox-genesis-mythos-master (validator-driven)

## Context

Hostile `roadmap_handoff_auto` report **`primary_code: state_hygiene_failure`** with **`contradictions_detected`**: `distilled-core.md` still routes operators to **next deepen / next RESUME = Phase 6 primary rollup** in the human-facing **Core decisions (🔵)** bullet and in **Phase 3 / Phase 4 / Phase 5** mega-section prose, while **`core_decisions` YAML**, **Phase 6** section, **`workflow_state.md` frontmatter (line 13)**, and **## Log** rows **2026-04-07 21:05** and **22:05** assert **`phase6_primary_rollup_nl_gwt: complete`** and next operator **`advance-phase`** / **`bootstrap-execution-track`** / **RECAL** — single authoritative machine state is **`workflow_state`**; rollup hub must not retain pre-21:05 “next deepen primary” clauses.

## Structural discrepancies

| Location | Issue |
|----------|--------|
| `distilled-core.md` L99 | Core decisions bullet ends with **next deepen Phase 6 primary rollup** — contradicts `core_decisions` Phase 6 entry and `workflow_state` 21:05. |
| `distilled-core.md` L119 | Phase 3 mega-heading: **next RESUME = Phase 6 primary rollup** — stale vs 21:05. |
| `distilled-core.md` L125 | Phase 4 prose: **next RESUME = Phase 6 primary rollup** — stale. |
| `distilled-core.md` L129 | Phase 5 prose: **(next: Phase 6 primary rollup)** — stale. |
| `workflow_state.md` L37 | Top `[!note]` still embeds **18:05** story with **next deepen = Phase 6 primary rollup**; **21:05** supersedes primary rollup pending work — note should stamp or replace that clause. |
| `workflow_state.md` L41–43 | **Phase 6 primary rollup — context preflight** section says live routing **next Phase 6 primary rollup** — contradicts terminal log after 21:05. |

## Proposed fixes

See structured return **`suggested_fixes`** (RoadmapSubagent applies after snapshot + gates; IRA does not edit `1-Projects/**`).

## Notes for future tuning

- After any **secondary 6.1 rollup** row that still says “next primary rollup”, run a **distilled-core** grep for **next RESUME**, **next deepen**, **Phase 6 primary** before handoff validation.
- Prefer **one** replacement template for “post-primary-rollup” operator next steps to avoid drift between YAML `core_decisions`, bullets, and mega-headings.
