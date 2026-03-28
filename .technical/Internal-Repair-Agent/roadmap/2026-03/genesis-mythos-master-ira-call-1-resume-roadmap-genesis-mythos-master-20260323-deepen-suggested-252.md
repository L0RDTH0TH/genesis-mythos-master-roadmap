---
created: 2026-03-23
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-roadmap-genesis-mythos-master-20260323-deepen-suggested-252
parent_run_id: queue-eat-20260323-252-a7f3c1
ira_call_index: 1
status: repair_plan
risk_summary: { low: 1, medium: 0, high: 0 }
validator_report_path: .technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260323T193000Z-first.md
ira_after_first_pass: true
---

# IRA — roadmap — genesis-mythos-master — call 1 (post nested `roadmap_handoff_auto` first pass)

## Context

Invocation followed **Validator→IRA** default (`ira_after_first_pass: true`) after first-pass report `roadmap-auto-validation-genesis-mythos-master-20260323T193000Z-first.md` (`state_hygiene_failure`, `missing_task_decomposition`, `safety_unknown_gap`, **high** / **block_destructive**). The parent run had **already reconciled** `workflow_state.md` YAML and `roadmap-state.md` **Latest deepen** cursor to **3.4.3** / queue **252** / `iterations_per_phase."3": 19`. On-disk verification shows **no remaining YAML vs log-tail mismatch** for the fields the validator cited (subphase index, `last_auto_iteration`, phase-3 iteration count, `last_ctx_util_pct` / `last_conf`).

## Structural discrepancies

1. **Stale validator snapshot (supersedes `state_hygiene_failure` on current disk):** First-pass verbatim citations (3.4.2, queue 251, `iterations_per_phase."3": 18`) **do not match** current `workflow_state.md`. Treat as **time-ordered race**, not live drift.
2. **Narrative drift in `roadmap-state.md` (weak minimum expansion):** **Phase summaries** bullet for Phase 3 still reads as if **3.4.1** were the live tertiary slice, while **Notes** + `workflow_state` agree on **3.4.3**. That contradicts the vault's own "Authoritative cursor" contract for human scanners.
3. **`missing_task_decomposition` (tertiary 3.4.3):** The phase note already carries a **Task ledger (DEFERRED / BLOCKED)** table aligned to **D-037** / **D-032/D-043** / **D-044**; open `- [ ]` lines are **not** naked (each cites a decision). Residual risk: hostile validators that pattern-match unchecked boxes without reading the ledger.
4. **`safety_unknown_gap`:** **D-044** **RegenLaneTotalOrder_v0** A/B remains **operator-gated** per `decisions-log.md` (explicit traceability sub-bullet). No safe vault auto-fix without a recorded operator choice; expanding this as "still true" is **correct minimum**, not pleasantness.

## Proposed fixes (for RoadmapSubagent apply path)

| # | Risk | Action | Target |
|---|------|--------|--------|
| 1 | **low** | Refresh **Phase 3** line under `## Phase summaries` so present-tense scope matches **current tertiary 3.4.3** (and secondary **3.4**), without removing historical detail from **Notes** / consistency rows. | `1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md` |

**Constraints (fix #1):** Apply only if `version` / `last_run` still match the 19:30 reconcile block (avoid clobbering a newer edit). Snapshot before/after per roadmap invariants.

## Notes for future tuning

- **Post-deepen YAML sync:** Ensure `roadmap-deepen` (or immediate postcondition) writes **all** machine fields (`current_subphase_index`, `last_auto_iteration`, `iterations_per_phase`, context mirrors) in the **same** commit as the log row so first-pass validators do not read half-updated state.
- **Phase summaries hygiene:** After each deepen that moves tertiary index, bump the **Phase summaries** one-liner in the same run as **Latest deepen** to prevent dual narrative.
- **Tertiary task pattern:** When DEFERRED tables exist, optional leading callout under `## Tasks` ("unchecked items gated by § Task ledger") reduces false **missing_task_decomposition** positives.
