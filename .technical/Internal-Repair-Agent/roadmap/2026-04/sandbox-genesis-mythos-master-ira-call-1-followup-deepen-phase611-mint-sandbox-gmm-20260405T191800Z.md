---
created: 2026-04-05
pipeline: roadmap
project_id: sandbox-genesis-mythos-master
queue_entry_id: followup-deepen-phase611-mint-sandbox-gmm-20260405T191800Z
ira_call_index: 1
status: repair_plan
risk_summary: { low: 3, medium: 1, high: 0 }
validator_report_path: .technical/Validator/roadmap-handoff-auto-sandbox-gmm-20260405T201530Z-phase611-post-mint.md
---

# IRA — sandbox-genesis-mythos-master (validator-driven, post–6.1.1 mint)

## Context

Nested **`roadmap_handoff_auto`** first pass reported **`contradictions_detected`** / **`state_hygiene_failure`** (primary) with **`needs_work`**. **workflow_state.md** and **roadmap-state.md** agree **`current_subphase_index: "6.1.2"`** after tertiary **6.1.1** mint (**2026-04-05 19:18**). **distilled-core.md** still narrates **pre-mint** cursor (**`6.1.1`**, “next mint tertiary **6.1.1**”) in multiple **core_decisions** bullets and Phase **5** / **6** rollup prose — dual routing truth vs authoritative state. Separately, **GWT-6.1.1-B** strict reading flags **Binding** table cells that use bold **2.7.1** / **2.7.3** without inline `[[Phase-2-7-*]]` wikilinks. **Execution track** (`Roadmap/Execution/**`) must not be edited for this repair bundle.

## Structural discrepancies

1. **distilled-core.md** — Stale **`current_subphase_index: "6.1.1"`** and “next **tertiary 6.1.1**” strings in **`core_decisions`** (e.g. Phase 4.2 historical bullet, Phase 5 primary rollup, Phase 5.2 rollup) and in **Phase 5** / **Phase 6** section headers/body (**lines ~61, 67, 77, 124, 128, 130** per repo grep).
2. **distilled-core.md** — Missing or incomplete **`core_decisions`** rollup for **tertiary 6.1.1** mint + CDR link (validator asked to mirror **roadmap-state** Phase 6 bullet).
3. **Phase-6-1-1** note — **Binding** table middle column lacks explicit Obsidian wikilinks to **2.7.1** / **2.7.3** canonical notes despite **GWT-6.1.1-B** (“vocabulary + wikilink”).
4. **missing_roll_up_gates** — Advisory on conceptual track; **not** a structural repair target for this pass (secondary **6.1** NL+GWT deferred per policy).

## Proposed fixes

See parent return **`suggested_fixes`** YAML (ordered **low → medium**). Apply under normal roadmap snapshot/backup gates; **no** **`Roadmap/Execution/**`** edits.

## Notes for future tuning

- After **deepen** mints that advance **`current_subphase_index`**, add a **distilled-core** sync check to **roadmap-deepen** post-append or a little-val row for **distilled-core vs workflow_state** cursor parity (same failure mode as validator cites).
- Consider templating “authoritative cursor” snippets so **one** source (workflow_state) is quoted verbatim in rollup surfaces.
