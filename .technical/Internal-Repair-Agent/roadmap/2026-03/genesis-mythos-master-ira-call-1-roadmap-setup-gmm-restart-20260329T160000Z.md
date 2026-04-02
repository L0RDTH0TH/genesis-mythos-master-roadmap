---
created: 2026-03-29
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: roadmap-setup-gmm-restart-20260329T160000Z
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 0
  medium: 0
  high: 0
parent_run_id: 859b5404-6168-413b-beef-fe445a961336
validator_report_path: .technical/Validator/roadmap-handoff-auto-genesis-mythos-master-20260329T180500Z-conceptual-v1-queue-roadmap-setup-gmm-restart.md
---

# IRA call 1 — roadmap / ROADMAP_MODE (post-validator, post-Roadmap repairs)

## Context

Validator-driven IRA after first `roadmap_handoff_auto` pass (`conceptual_v1`): **high** / **block_destructive**, **primary_code** `contradictions_detected`, **reason_codes** `contradictions_detected`, `missing_task_decomposition`, `safety_unknown_gap`. Roadmap subagent **already applied** D-027 migration into live `decisions-log.md`, Phase 1 secondary/tertiary notes, `handoff_readiness` / `handoff_gaps` on phase primaries, and `distilled-core` `core_decisions` + body anchors. Live vault was re-read to assess **residual** structural gaps vs the **stale** validator citations.

## Structural discrepancies (vs stale report only)

| Stale claim | Live state (verified) |
|-------------|------------------------|
| No **D-027** in live `decisions-log.md` | **D-027** row present with archive wikilink and PMG alignment text |
| Phase 1 no secondary/tertiary notes | `Phase-1-1-…1731.md`, `Phase-1-2-…1731.md` exist under Phase 1 folder |
| Phase 1 missing `handoff_readiness` | Primary has `handoff_readiness: 72`, `handoff_gaps` populated |
| `distilled-core` `core_decisions: []` | YAML list + body bullets for D-027 and Phase 0 restart |

**Non-stale observation (advisory, not a repeat of the three reason_codes):** Phase 1 `handoff_readiness` (72) is **below** `roadmap.conceptual_design_handoff_min_readiness` (75) in Second-Brain-Config — expected for a **fresh setup** until `hand-off-audit` or deepen adds evidence; it is **not** the same failure mode as “missing handoff fields entirely.” Phases 2–6 remain primary-only; the validator verbatim gap targeted **Phase 1** decomposition only.

## Proposed fixes

**None required for residual closure of the cited validator reason_codes** — `suggested_fixes` returned empty to the caller.

## Notes for future tuning

- Compare-to-initial second validator should treat first-pass verbatim table as **historical**; regression checks should key on **current** paths and frontmatter.
- If `missing_task_decomposition` is later broadened to “every phase folder must have a secondary before setup Success,” encode that explicitly in gate catalog or roadmap-generate-from-outline so setup and validator stay aligned.
