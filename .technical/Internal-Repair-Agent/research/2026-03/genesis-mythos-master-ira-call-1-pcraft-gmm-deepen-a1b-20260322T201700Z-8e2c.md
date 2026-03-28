---
created: 2026-03-22
pipeline: research
project_id: genesis-mythos-master
queue_entry_id: pcraft-gmm-deepen-a1b-20260322T201700Z-8e2c
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 2
  medium: 2
  high: 0
validator_report_path: .technical/Validator/research-synthesis-genesis-mythos-master-20260322T214500Z-nested-pdeepen-first.md
parent_run_id: pr-eatq-20260322-pcraft-a1b-dispatch
---

# IRA — research / nested_pre_deepen (call 1)

## Context

Nested **research_synthesis** validator (first pass, `ira_after_first_pass: true`) returned **medium** / **needs_work** with **contradictions_detected** and **safety_unknown_gap**. The synthesis `Ingest/Agent-Research/phase-3-4-9-a1b-promptcraft-roll-up-gaps-synthesis-2026-03-22-2145.md` tells juniors to use **full vault paths** in §1 but §2 uses **short wikilinks** for rollup notes; it also claims **Authoritative** / **verbatim policy strings** for **D-046** / **D-050** / **D-055** without in-note quotes. §4 is prose-only and does not bridge to the **machine-facing JSON** already documented on the **3.4.9** phase note. This IRA plan targets **only** the synthesis note under `Ingest/Agent-Research/` (Research subagent applies edits); phase/roadmap files are out of scope for mutation.

## Structural discrepancies

1. **Self-contradiction:** §1 table requires full paths; §2 bullets anchor rollups via `[[...]]` only.
2. **Overstated provenance:** “Authoritative decisions-log rows (verbatim…)” with no fenced excerpts or as-of discipline.
3. **Thin machine bridge:** §4 does not point juniors at the canonical **RESUME_ROADMAP** JSON template location (phase note § Shallow deepen).

## Proposed fixes (apply order: low → medium)

See parent return `suggested_fixes[]` for machine-readable steps. Verbatim source lines for fix 2 (read from `1-Projects/genesis-mythos-master/Roadmap/decisions-log.md` at IRA read time):

- **D-046** — list item starting `- **D-046 (2026-03-22):** **Phase 3.2 secondary closure rollup authority (3.2.4):** …`
- **D-050** — list item starting `- **D-050 (2026-03-23):** **Phase 3.3 secondary closure rollup authority (3.3.4):** …`
- **D-055** — list item starting `- **D-055 (2026-03-23):** **Phase 3.4 secondary closure rollup authority (3.4.4):** …`

**Constraint:** After paste, re-read `decisions-log.md`; if bullets drift, refresh excerpts or fall back to **Paraphrase (unverified)** + new **As-of** timestamp.

## Notes for future tuning

- Research synth notes that cite **D-0xx** should default to **either** a fenced “copied from decisions-log” block with **As-of** **or** explicit **Paraphrase (unverified)** — not both “verbatim” label and paraphrase-only body.
- Template lint: consider a checklist item in research-agent-run for “junior path column uses `1-Projects/...` when table says full paths.”
