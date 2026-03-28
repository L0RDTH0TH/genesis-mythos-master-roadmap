---
created: 2026-03-23
pipeline: research
project_id: genesis-mythos-master
queue_entry_id: resume-roadmap-genesis-mythos-master-20260323-deepen-suggested-250
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 4
  medium: 5
  high: 0
validator_report: 3-Resources/Second-Brain/Validator-Reports/research_synthesis/genesis-mythos-master-20260323T160500Z-research-synthesis-first.md
synth_note: Ingest/Agent-Research/phase-3-4-1-living-world-slice-taxonomy-research-2026-03-23-1600.md
---

# IRA report — research / validator-driven (call 1)

## Context

Research nested pre-deepen run for **genesis-mythos-master** produced synthesis `Ingest/Agent-Research/phase-3-4-1-living-world-slice-taxonomy-research-2026-03-23-1600.md`. Hostile **research_synthesis** first pass (`severity: medium`, `recommended_action: needs_work`) cited **`safety_unknown_gap`** (primary) and **`missing_task_decomposition`**. IRA treats that verdict as a **floor**: frontmatter **`research_focus: junior_handoff`** + **`research_escalations_used: 0`** is inconsistent with §6 blockers on **D-032** / **D-044**; the slice table is labeled **normative** while registry literals and merge rules are deferred; **§6** defers actionable decomposition entirely to a “tertiary roadmap note”; Gaffer timestep/lockstep URLs are **footer-only**; pseudocode omits **RegenRequest_v0** vs ledger ordering. All repairs below stay **inside** `Ingest/Agent-Research/**` (plus optional Run-Telemetry for apply tracking)—no `roadmap-state`, phase notes, or project `decisions-log` edits by IRA mandate.

## Structural discrepancies (expanded)

1. **Honesty / safety signal**: `junior_handoff` + `research_escalations_used: 0` under-claims dependency on unresolved decision IDs and open registry work.
2. **Normative vs blocked artifacts**: “Recommended slice classes (normative direction)” reads canonical while §6 states registry rows and golden tick are blocked/TBD.
3. **missing_task_decomposition**: No numbered/checklist handoff tasks in the synthesis; “for tertiary roadmap note” leaves the note non-actionable for juniors.
4. **D-044 pin**: §3 names the fork but does not state a **single provisional project story** for same-tick regen vs scalar ordering (validator asked for one paragraph; can live in synthesis with link to `[[decisions-log]]` only as citation, not editing that file).
5. **Machine-checkable stub**: No minimal **`AgencySliceId_v0`** draft rows in-note (validator: 3 rows + `tie_break_key` field names).
6. **Merge matrix**: No explicit commutative / conflict / regen stub for faction vs player-scoped slices.
7. **Source traceability**: Gaffer posts not tied to §1 tick-budget / §2 ordering claims in-body; Daydreamsoft stands alone as lockstep “discipline” anchor.
8. **Golden tick**: No numbered trace (schedule order → streams → intent kinds → regen precondition check locus); only a one-line TBD bullet.
9. **Pseudocode gap**: No `RegenRequest_v0` enqueue vs `AgencySliceApplyLedger_v0` append ordering relative to **D-044** provisional story.

## Proposed fixes (for Research / Ingest to apply)

See structured `suggested_fixes` in parent return payload; summary table:

| # | Risk | Target | Intent |
|---|------|--------|--------|
| 1 | low | synthesis frontmatter | Align `research_escalations_used` and/or `research_focus` with documented D-032/D-044 deps |
| 2 | low | synthesis §1 | Soften/relabel table header (non-canonical until registry) |
| 3 | medium | synthesis §3 | Add **Provisional D-044 story (project)** paragraph + pointer to `[[decisions-log]]` (read-only link) |
| 4 | medium | synthesis new subsection | Draft **`AgencySliceId_v0` stub table** (3 ambient classes + fields) |
| 5 | medium | synthesis new subsection | **Merge matrix** stub (faction × player slice outcomes) |
| 6 | low | synthesis §1–2 | **Weave Gaffer** (one sentence + link) into tick budget / draw-order narrative |
| 7 | medium | synthesis §5–6 | **Extend pseudocode** with regen lane vs ledger step + comment tying to D-044 story |
| 8 | medium | synthesis new §7 | **Actionable task list** (numbered) decomposing §6 into junior-sized items |
| 9 | low | synthesis §6 or new § | **Golden tick** numbered trace (explicit “non-blocking for current scope” where TBD) |
|10 | low | `.technical/Run-Telemetry/` | Optional stub note when fixes applied (actor, ids, `ira_call_index`, synth path) |

## Notes for future tuning

- **research_synthesis** validator: consider a dedicated reason_code for **frontmatter–body mismatch** on `research_escalations_used` to reduce reliance on `safety_unknown_gap` bucket.
- Research agent template: when `linked_phase` references decision IDs in open items, auto-suggest **non-zero** `research_escalations_used` or a `research_open_decisions: [D-032, D-044]` array for machine checks.
