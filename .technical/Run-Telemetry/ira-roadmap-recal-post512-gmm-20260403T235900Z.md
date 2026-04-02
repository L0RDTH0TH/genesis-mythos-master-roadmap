---
actor: internal-repair-agent
project_id: genesis-mythos-master
queue_entry_id: followup-recal-post-512-high-util-gmm-20260403T233500Z
parent_run_id: eatq-20260331-layer1-gmm-recal
timestamp: 2026-03-31T12:00:00Z
ira_call_index: 1
status: repair_plan
suggested_fix_count: 0
---

# Run-Telemetry — IRA (roadmap, recal post-512)

- **Pipeline:** roadmap  
- **Mode:** RESUME_ROADMAP (`params.action: recal`)  
- **Invocation:** post-first nested validator (`ira_after_first_pass: true`)  
- **Validator report:** `.technical/Validator/roadmap-handoff-auto-recal-post512-gmm-20260403T235900Z.md`  
- **IRA outcome:** `repair_plan` with **zero** additional `suggested_fixes` — vault edits applied before IRA already address **`state_hygiene_failure`** narrative gaps; **`safety_unknown_gap`** noted as residual advisory (drift asserted in Consistency reports row).
