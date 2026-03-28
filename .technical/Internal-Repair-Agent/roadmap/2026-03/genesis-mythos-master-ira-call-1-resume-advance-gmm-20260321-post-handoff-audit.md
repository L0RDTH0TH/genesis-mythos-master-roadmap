---
created: 2026-03-21
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-advance-gmm-20260321-post-handoff-audit
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 2
  medium: 4
  high: 0
validator_report_path: .technical/Validator/roadmap-auto-validation-20260321T234500Z.md
parent_run_id: l1-eatqueue-20260321-resume-advance-gmm
---

# IRA call 1 — roadmap / RESUME_ROADMAP advance-phase (post nested validator)

## Context

After macro **advance-phase 2 → 3** (`resume-advance-gmm-20260321-post-handoff-audit`), the first **`roadmap_handoff_auto`** pass reported **severity: medium**, **recommended_action: needs_work**, with **primary_code: `missing_task_decomposition`** plus **`safety_unknown_gap`** and **`missing_risk_register_v0`**. State files are internally consistent (`current_phase: 3`, `completed_phases: [1, 2]`, workflow log row matches). The failure mode is **handoff quality**: Phase 3 primary is still a **thin container** (three top-level tasks only), with **no secondary roadmap stubs**, **no explicit roll-up gate table** tying Phase 3 simulation work to **EMG-2 / 2.3.3–2.3.4** execution artifacts, **no risk register v0**, and **ambiguous vault posture** on **D-022 / numeric F** while **2.3.4** still shows **execution_handoff_readiness: 66** and open execution checklists. Contaminated-report rule applied: treat validator gaps as a **weak minimum**; this plan **expands** beyond the report where structure still under-specifies delegatability.

## Structural discrepancies

1. **Primary decomposition gap:** Only `phase-3-living-simulation-and-dynamic-agency-roadmap-2026-03-19-1101.md` exists under `Phase-3-Living-Simulation-and-Dynamic-Agency/`; Dataview subphase table has **no secondary rows**.
2. **Cross-phase dependency clarity:** Macro advance is documented in `roadmap-state.md`, but Phase 3 head note does not **surface** "assumes vs blocked until" vs **fixtures PR + green `AlignAndVerify` + WA log + wiki G-EMG2 row** from **2.3.3 / 2.3.4**.
3. **Risk visibility:** No **risk register v0** (drift vs determinism, DM override vs replay, tick/perf, persistence, EMG-2 execution unknowns).
4. **Decision hygiene:** **D-022** remains a stub ("no numeric F committed"); **D-024** already records **provisional F=85** in 2.3.2 — without an explicit **Phase 3 NON-HOLD / parallel track** statement, operators may read **safety_unknown_gap** as "do not deepen Phase 3 until repo green."
5. **distilled-core / graph:** Mermaid ends at Phase 2.3; **Phase 3** is not yet reflected in the dependency graph (optional follow-up, lower priority than stubs + gates).

## Proposed fixes (for Roadmap subagent application)

See parent return `suggested_fixes[]` JSON-shaped list; apply in **low → medium** order when snapshots and confidence gates pass.

## Notes for future tuning

- **Pattern:** `advance-phase` after a tertiary **handoff_readiness** threshold can leave **execution_handoff_readiness** low; validator should keep flagging **safety_unknown_gap** until either execution catches up or vault notes **explicitly** declare parallel vs blocking posture.
- **Pattern:** New macro phase heads should default-create **≥2 secondary stubs** in the same run as advance, or treat **missing_task_decomposition** as expected until first **deepen** — product choice: either automate stub creation on advance or tighten validator only after first Phase 3 deepen.
