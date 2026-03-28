---
created: 2026-03-24
pipeline: research
project_id: genesis-mythos-master
queue_entry_id: resume-deepen-post-recal-p4-1-1-gmm-20260324T021500Z
ira_call_index: 1
status: repair_plan
risk_summary: { low: 1, medium: 0, high: 0 }
parent_run_id: 4023e922-cf0e-4b45-a660-6903caea3adb
validator_report_path: .technical/Validator/research-synthesis-genesis-mythos-master-phase-4-1-1-20260324T000000Z.md
---

# IRA call 1 — research (post–first-pass validator)

## Context

Research pipeline invoked IRA after hostile `research_synthesis` validator pass (`primary_code: safety_unknown_gap`, `needs_work`). Caller stated the three `next_artifacts` items were applied inline in `Ingest/Agent-Research/phase-4-1-1-adapter-preimage-stable-layout-cqrs-research-2026-03-23-2205.md`. Read-only verification against that file and the frozen validator report confirms the **definition-of-done** checklist is satisfied in the body; one **residual** basename-only wikilink remains in **Sources** (same target as the fixed “Prior synthesis” line).

## Structural discrepancies

1. **Resolved (no further action required for validator DoD):** Full-path wikilink for prior synthesis in **Vault anchor** (`[[Ingest/Agent-Research/phase-4-primary-perspective-control-research-2026-03-24]]`).
2. **Resolved:** Watcher-Result traceability — paragraph cites `3-Resources/Watcher-Result` and a concrete `requestId` plus “verify file before external comms.”
3. **Resolved:** D-045 vs Lane-C scope — explicit sentence separating **3.2.3** regen/golden deferrals from 4.1.1 Lane-C **D-032** / **D-043** / preimage-freeze anchors.
4. **Residual (optional polish):** **Sources** still lists `[[phase-4-primary-perspective-control-research-2026-03-24]]` without folder path — same ambiguity class as the original validator citation.

## Proposed fixes

| # | risk | target | action |
|---|------|--------|--------|
| 1 | low | Synthesis note | Replace basename-only prior-synthesis link in `## Sources` with full `Ingest/Agent-Research/...` path to match § Vault anchor. |

## Notes for future tuning

- Research synthesis templates should default **all** cross-links to agent-research notes with full `Ingest/Agent-Research/` paths when basename collisions are possible.
- Second validator pass can treat “Sources” as in-scope for `safety_unknown_gap` if basename-only links persist after body fixes.
