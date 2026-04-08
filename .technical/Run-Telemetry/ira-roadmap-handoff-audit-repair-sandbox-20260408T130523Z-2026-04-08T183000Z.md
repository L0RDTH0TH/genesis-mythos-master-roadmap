---
actor: internal-repair-agent
project_id: sandbox-genesis-mythos-master
queue_entry_id: handoff-audit-repair-sandbox-genesis-mythos-master-20260408T130523Z
parent_run_id: eatq-sandbox-layer1-20260408T183000Z
timestamp: 2026-04-08T18:30:00Z
---

# Run-Telemetry — IRA (roadmap / handoff-audit repair)

| Field | Value |
| --- | --- |
| `ira_call_index` | 1 |
| `status` | repair_plan |
| `suggested_fix_count` | 5 |
| `validator_primary_code` | missing_roll_up_gates |
| `error_category` | — |

**Summary:** Validator-driven IRA after first **roadmap_handoff_auto** pass; repair plan targets **state_hygiene_failure** and **contradictions_detected**; rollup gate codes require **Layer 1 compare** / policy — no **`phase_1_rollup_closed`** flip in suggested fixes.

**Report:** `.technical/Internal-Repair-Agent/roadmap/2026-04/sandbox-genesis-mythos-master-ira-call-1-handoff-audit-repair-20260408T130523Z.md`
