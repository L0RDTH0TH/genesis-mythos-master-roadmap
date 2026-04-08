---
created: 2026-04-08
pipeline: roadmap
project_id: godot-genesis-mythos-master
queue_entry_id: followup-deepen-exec-p212-tertiary-godot-20260408T223000Z
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 2
  medium: 3
  high: 0
validator_primary_code: safety_unknown_gap
---

# IRA — roadmap / RESUME_ROADMAP deepen (post-first-validator)

## Context

RoadmapSubagent invoked IRA after nested `roadmap_handoff_auto` reported **`needs_work`**: **`safety_unknown_gap`** (primary) and **`missing_task_decomposition`**. Iter **15** in `workflow_state-execution` matches tertiary **2.1.2** mint and `roadmap-state-execution` `last_run: 2026-04-08-2230`. Structural tables and `G-2.1.2-*` PASS rows exist; the failure mode is **traceability debt at Phase 2 primary** plus **tertiary completeness bar** (no executable test harness on **2.1.2**).

## Structural discrepancies

1. **`phase2_gate_replay_traceability` (primary):** In `Phase-2-Execution-Procedural-Generation-and-World-Building-Roadmap-2026-04-08-1227.md`, the Primary gate map row lists Evidence as deferred prose only. Closure criteria require **seed id, manifest digest, commit envelope IDs** with **bidirectional** links to evidence notes — not satisfied while the gate remains **open** with only “carry forward” language.
2. **Tertiary **2.1.2**:** `Phase-2-1-2-Execution-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-04-08-2230.md` has AC bullets and pseudocode `assert` blocks but **no** numbered test matrix / executable checklist (cases × expected labels × forbidden S5 token) matching hostile tertiary bar.
3. **Chain scope:** `handoff_gaps` and Phase 2 primary correctly note **2.1.3–2.1.5** pending; validator treats **open replay trace** as execution debt regardless of **2.1.2** slice completeness.

## Proposed fixes

See parent return `suggested_fixes[]` (JSON-shaped in chat). Apply in **low → medium** order unless a gate blocks a step.

## Notes for future tuning

- Execution **v1** treats primary replay-trace rows as **binding**; deepen mints should either attach **minimal bidirectional stub evidence** early or use an explicit **FAIL / scheduled** sub-table with gate IDs until tertiaries exist.
- Add a **test matrix** template to roadmap-deepen / Quality-Guide for **tertiary** depth so `missing_task_decomposition` does not repeat on long notes with pretty tables only.
