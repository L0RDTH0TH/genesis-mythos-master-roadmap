---
created: 2026-04-09
pipeline: roadmap
project_id: godot-genesis-mythos-master
queue_entry_id: godot-exec-p1-2-20260409
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 2
  medium: 1
  high: 0
validator_report_path: .technical/Validator/roadmap-auto-validation-godot-exec-p1-2-20260409T000000Z-pass1.md
---

# IRA — godot-genesis-mythos-master (execution Phase 1.1 / 1.2)

## Context

Nested **Validator** pass 1 (`roadmap_handoff_auto`, execution / Phase 1.2 mint) returned **medium** / **needs_work** with **primary_code** `missing_roll_up_gates` plus `missing_handoff_readiness` (Phase 1.2 `handoff_readiness: 84` vs default **85** floor) and `safety_unknown_gap` (Phase 1.1 stale “future 1.2” wording while **1.2** exists). Operator constraint: **do not** claim **GMM-2.4.5-*** closure; prefer low-blast-radius edits first.

## Structural discrepancies

1. **Handoff floor:** `Phase-1-2-Registry-Telemetry-Stubs-Sandbox-AB-Parity-Roadmap-2026-04-09-0000.md` frontmatter **`handoff_readiness: 84`** undercuts execution default **≥ 85** cited in the validator report.
2. **Traceability debt:** `Phase-1-1-Godot-Engine-Binding-Surfaces-Sandbox-AB-Parity-Roadmap-2026-04-08-2300.md` § A/B parity still says mapping may be documented in a **future 1.2** slice; **1.2** is minted and already holds stub path table + schema language.
3. **Roll-up gates (honest minimum):** **`GMM-2.4.5-*`** rows remain **TBD/Deferred** in 1.2 (correct — not closure). Validator still flags **`missing_roll_up_gates`** until either owned next steps exist or a **scoped execution-track deferral** is recorded outside the slice (per report `next_artifacts`).

## Proposed fixes

| Order | Risk | Target | Summary |
| --- | --- | --- | --- |
| 1 | low | Phase 1.2 note | `handoff_readiness: 84` → `85` only if operator accepts that stub completeness + explicit deferrals justify the execution floor (no rollup closure implied). |
| 2 | low | Phase 1.1 note | Replace “future **1.2**” sentence with wikilink to Phase 1.2 + clarify stubs vs full mapping/compare closure. |
| 3 | medium | `decisions-log.md` | Append one **D-Exec-*** row: Phase 1.2 satisfies stub/path/deferral obligations; **GMM-2.4.5-*** rollup/compare/CI closure **remains open** until script/CI/lane-B milestones — cites 1.2 + validator path. |

## Notes for future tuning

- Execution mints that sit at **84** with explicit deferrals may repeatedly trip **`missing_handoff_readiness`**; either calibrate `handoff_readiness` at author time to **≥ 85** when stub scope is complete, or record a **decisions-log** exception when sub-floor is intentional.
- Phase **sibling** notes should be scanned after each new execution slice mint for **forward-reference** drift (“future X”) and updated to **wikilinks**.
