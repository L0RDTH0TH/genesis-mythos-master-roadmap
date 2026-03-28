---
created: 2026-03-21
pipeline: research
project_id: genesis-mythos-master
queue_entry_id: resume-roadmap-genesis-mythos-master-20260321-followup-deepen-next-followup
ira_call_index: 1
status: repair_plan
risk_summary: { low: 2, medium: 1, high: 0 }
validator_report_path: .technical/Validator/research-synthesis-genesis-mythos-master-20260321T233200Z.md
synth_note_path: Ingest/Agent-Research/phase-2-3-3-emg2-alignment-golden-gate-wiring-research-2026-03-21-2315.md
---

# IRA report — research synthesis (validator-driven, call 1)

## Context

Research pipeline invoked IRA after the first hostile `research_synthesis` pass (`primary_code: safety_unknown_gap`, `needs_work`). The validator report predates a **post-report patch** to the synthesis note. Current content includes vault excerpt bullets, a single v0 loader contract for inline `lore_json` / `sim_json`, a full **G1** JSON example, and demoted external links (background reading). Those changes **substantially close** the four `next_artifacts` in the validator YAML. Residual risk is **honest scope**: the note still reads as normative for a **future** genesis-mythos harness; this vault’s `.github/workflows/test.yml` does not implement `ReplayAndVerify` or EMG gates — without saying so, a hostile second pass can still raise `safety_unknown_gap` (implied repo claims).

## Structural discrepancies (post-patch)

1. **Traceability gap:** Golden / EMG policy is inferable from phase wikilinks but not explicitly tied to decisions-log rows **D-020** (intent replay CI), **D-021** (fixture/workflow backlog caveat), **D-024** (EMG-2 draft + not frozen for CI).
2. **CI evidence boundary:** No explicit statement that **this vault’s** workflow at `.github/workflows/test.yml` is **unittest-only** (`python -m unittest discover …`); EMG registry wiring remains roadmap-normative / backlog per D-021.
3. **Optional completeness:** Only **G1** is exemplified; failure-path shapes (`BELOW_FLOOR`, `INVALID_EMG2_SLICE`) are described in prose/table but not shown as minimal JSON — second validator may still ask for an **F1**-style instance.

## Proposed fixes (for caller to apply on synth note)

| # | Risk | Action |
|---|------|--------|
| 1 | low | Add short “Evidence / VCS boundary” paragraph: cite vault `.github/workflows/test.yml` scope; anchor policy to decisions-log **D-020**, **D-021**, **D-024**. |
| 2 | low | In “Raw sources (vault)” or under “Vault excerpts”, one sentence: normative excerpts live in § Vault excerpts; raw list is index + trace. |
| 3 | medium | Optional fenced **F1** (or **F2**) minimal JSON showing `golden_expectations` for `BELOW_FLOOR` or `INVALID_EMG2_SLICE`. |

## Notes for future tuning

- **`safety_unknown_gap` after content fixes** often means missing **negative knowledge** (“what this repo’s CI does *not* do yet”) rather than missing more lore.
- For research to deepen handoffs, pre-empt compare-to-report regressions by a one-line “addresses report … next_artifacts” only if factually true.
