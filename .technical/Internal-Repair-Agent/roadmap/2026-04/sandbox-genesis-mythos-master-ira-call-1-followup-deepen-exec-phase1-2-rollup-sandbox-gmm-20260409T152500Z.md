---
created: 2026-04-09
pipeline: roadmap
project_id: sandbox-genesis-mythos-master
queue_entry_id: followup-deepen-exec-phase1-2-rollup-sandbox-gmm-20260409T152500Z
ira_call_index: 1
status: repair_plan
risk_summary: { low: 4, medium: 1, high: 0 }
validator_report_note: "3-Resources/Second-Brain/Validator-Reports/roadmap_handoff_auto/sandbox-genesis-mythos-master-20260409T173500Z-exec-v1-post-repair.md"
primary_code: safety_unknown_gap
---

# IRA — sandbox-genesis-mythos-master (validator-driven, execution slice)

## Context

RoadmapSubagent invoked IRA after nested `roadmap_handoff_auto` with **severity: medium**, **recommended_action: needs_work**, **primary_code: safety_unknown_gap**. Residual themes: (1) secondary **1.2** lifecycle clarity (frontmatter vs § Rollup completion), (2) **`observed_at_tick`** traceability vs stub boundary, (3) optional evidence-hook hygiene on **1.2.1** GWT-1-2-1-Exec-A.

**Read-only inspection (2026-04-09):** Current `Phase-1-2-PresentationEnvelope-Stub-Roadmap-2026-04-06-1200.md` frontmatter shows **`status: complete`**, **`progress: 100`**, not the validator’s quoted **`in-progress` / `85`** — likely **post-validator human/agent repair** or validator snapshot lag. **`stubMapSampleToReadout`** now surfaces **`observed_at_tick`** via **`readout_text`** (`@tick=` substring), not only a comment. Treat the validator report as a **minimum**; remaining work is **explicit automation contract** and **testable stub rules** so `safety_unknown_gap` cannot reappear on compare pass.

## Structural discrepancies

1. **Stale vs live frontmatter:** Validator `gap_citations` quote **in-progress / 85** disagrees with live **complete / 100** on **1.2** — second pass should confirm **no regression**; add **machine-facing prose** so automation/juniors do not depend on frontmatter drift alone.
2. **Lifecycle semantics:** `[[roadmap-state-execution]]` Phase 1 summary + `[[workflow_state-execution]]` cursor **`1.1`** post-rollup are **consistent** with “rollup done, next deepen elsewhere” but are **split across files** — needs a **single authoritative sentence** on the **1.2** note tying rollup closure to cursor semantics.
3. **`observed_at_tick`:** No longer purely “implicit” in narrative if **`readout_text`** embeds tick — still **execution_v1**-thin without a **named testable rule** in § Risk register or an explicit **projection rule** line in the schema table.
4. **GWT-1-2-1-Exec-A:** Evidence column is **long** and **workflow-log-heavy** — brittle vs parent § Tertiary children + parent rollup.

## Proposed fixes (caller applies under guardrails)

See structured return `suggested_fixes` in parent pipeline message; risks tagged below.

## Notes for future tuning

- When IRA runs **after** a repair wave, embed **`validator_report_timestamp`** or **content hash** in hand-off to detect **stale gap_citations**.
- Consider a **single** optional frontmatter key e.g. `secondary_rollup_closed: true` for execution secondaries to disambiguate **container in-progress** vs **secondary rollup** without reading full body.
