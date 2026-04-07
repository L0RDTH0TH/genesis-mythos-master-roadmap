---
created: 2026-04-09
pipeline: roadmap
project_id: sandbox-genesis-mythos-master
queue_entry_id: resume-deepen-sandbox-exec-p1-spine-post-telemetry-repair-20260409T120500Z
ira_call_index: 1
status: repair_plan
risk_summary: { low: 2, medium: 2, high: 0 }
validator_report_path: .technical/Validator/roadmap-handoff-auto-sandbox-exec-p1-spine-post-parity-20260409T151500Z.md
parent_run_id: eatq-layer1-sandbox-20260409T120600Z
---

# IRA — sandbox-genesis-mythos-master (call 1, post–roadmap_handoff_auto)

## Context

RoadmapSubagent invoked IRA after the first nested **`roadmap_handoff_auto`** pass (`primary_code: safety_unknown_gap`, `needs_work`). Artifacts confirm: **`roadmap-state-execution.md`** `last_run` is **2026-04-06-1545** while **`workflow_state-execution.md`** ## Log ends at **2026-04-09 15:10** (iter Obj **5**); **Phase 1.2** `handoff_readiness` is **82** (below default execution floor **85**); **Phase 1.1** GWT-1-1-Exec-A still describes the live cursor as mint-time **1.1**; dual **`status`** strings differ between the two state files (`generating` vs `in-progress`). Stub fences 1.1/1.2 are aligned; hygiene gaps drive the verdict.

## Structural discrepancies

1. **Stale `last_run`** — automation treating `last_run` as freshness is misled vs ## Log.
2. **Unexplained dual status** — `roadmap-state-execution` `status: generating` vs `workflow_state-execution` `status: in-progress` without a one-line gloss.
3. **HR below execution floor** — Phase 1.2 `handoff_readiness: 82` vs default **min_handoff_conf 85** unless waived in **decisions-log**.
4. **Stale GWT evidence** — GWT-1-1-Exec-A cites cursor **1.1** at mint **2026-04-08**; **`workflow_state-execution`** now has `current_subphase_index: "1.2.1"`.

## Proposed fixes

See structured `suggested_fixes` in the parent return payload (stable apply order: **1 → 2 → 3 → 4**).

## Notes for future tuning

- After each execution deepen that appends ## Log, **roadmap-deepen** or RoadmapSubagent should bump **`roadmap-state-execution`** `last_run` to the **same monotonic anchor** as the new log row (or deprecate `last_run` in prose if non-canonical).
- GWT “live cursor” rows should reference **`workflow_state-execution`** frontmatter `current_subphase_index` with an explicit **as-of** or be labeled **mint-time snapshot** to avoid narrative drift.
