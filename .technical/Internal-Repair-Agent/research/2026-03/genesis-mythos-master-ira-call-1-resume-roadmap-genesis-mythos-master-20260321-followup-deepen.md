---
created: 2026-03-21
pipeline: research
project_id: genesis-mythos-master
queue_entry_id: resume-roadmap-genesis-mythos-master-20260321-followup-deepen
ira_call_index: 1
status: repair_plan
risk_summary: { low: 2, medium: 3, high: 0 }
validator_report_path: .technical/Validator/research-synthesis-genesis-phase23-20260321T223000Z-initial.md
parent_run_id: pr-eatq-20260321-resume-gmm-deepen
---

# IRA report — research synthesis repair (call 1)

## Context

Research nested validator pass on `Ingest/Agent-Research/phase-2-3-validate-co-authored-world-emergence-research-2026-03-21-2230.md` returned **needs_work** (primary: `missing_task_decomposition`, secondary: `safety_unknown_gap`). The note mixes solid external framing with **un-backed Genesis-specific claims**, a **Sources** list that outruns declared Raw captures, **no executable emergence metrics** tied to Phase 2.2 harness IDs, and frontmatter **`sanity_check_rating`** (epistemic slop). IRA call 1 proposes **synthesis-note-only** edits so a second validator pass can re-check traceability and task decomposition.

## Structural discrepancies

1. **Task decomposition gap**: Section 4 "Concrete design hooks" stops at slogans; no ≥3 metrics with inputs/units/pass-fail mapped to **G1–G3 / F1–F2** (or successor IDs).
2. **Safety / unknown coupling**: "Implications for Genesis Mythos" and body text assert internal architecture (stage pipeline, IntentAnnotate, ReplayAndVerify) **without** `[[wiki-link]]` or repo path per claim.
3. **Source integrity**: Footer **Sources** lists URLs not mirrored in "Raw sources (vault)" without a **synthesis-only** flag or traceability table.
4. **Self-grade**: `sanity_check_rating` is an unverifiable numeric marketing field.

## Proposed fixes

See structured `suggested_fixes` returned to the Research subagent (same content as parent hand-off). Apply in order **low → medium** when gates allow; snapshot synthesis note before edits per MCP rules.

## Notes for future tuning

- Research validator **ira_after_first_pass** should keep producing **next_artifacts**; IRA should default to **append_section** over rewriting history so Raw links stay stable.
- Recurrent pattern: **agent-research** notes listing many URLs while Raw bundle stays small — enforce traceability block at synthesis time in the research skill.
