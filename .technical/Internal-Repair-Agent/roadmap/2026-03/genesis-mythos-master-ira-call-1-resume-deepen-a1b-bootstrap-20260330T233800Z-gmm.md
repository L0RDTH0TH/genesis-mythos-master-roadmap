---
created: 2026-03-30
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-deepen-a1b-bootstrap-20260330T233800Z-gmm
ira_call_index: 1
status: repair_plan
risk_summary: { low: 2, medium: 1, high: 0 }
validator_report_path: .technical/Validator/roadmap-handoff-auto-genesis-mythos-master-20260330T234200Z-conceptual-v1-post-2-2-1.md
---

# IRA — roadmap / RESUME_ROADMAP deepen (post-first validator)

## Context

RoadmapSubagent invoked IRA after the first nested `roadmap_handoff_auto` pass reported `safety_unknown_gap` (medium, `needs_work`). The validator snapshot predates Layer 2 reconciliation: **`workflow_state.md`** last log row for `queue_entry_id: resume-deepen-a1b-bootstrap-20260330T233800Z-gmm` already reflects **`gate_signature: none`** plus **`queue_origin: layer1_a1b_empty_queue_bootstrap`**, matching the stated intent (A.1b lineage without repeating the bootstrap resolver class). **`decisions-log.md`** includes an operator pick closing pattern-only grounding for the same queue id. Remaining structural debt is **cross-artifact echo** (decisions-log deepen bullet still cites the old bootstrap `gate_signature`) and **machine-auditable deferrals** for two open questions still prose-only in the 2.2.1 phase note.

## Structural discrepancies

1. **Stale resolver echo in decisions-log** — The **Deepen (`resume-deepen-a1b-bootstrap-20260330T233800Z-gmm`)** bullet still records `gate_signature: empty-queue-bootstrap|genesis-mythos-master|conceptual|20260330`, while **`workflow_state`** last row uses `gate_signature: none` and `queue_origin: layer1_a1b_empty_queue_bootstrap`. Auditors grepping `gate_signature` get conflicting stories.
2. **Open questions not keyed** — `Phase-2-2-1-Intent-Envelope-Normalization-and-Identity-Binding-Roadmap-2026-03-30-2338.md` lists two bullets under **Open questions** without `D-*` ids, execution-defer tags, or decisions-log rows, leaving `safety_unknown_gap` partially unbound even after the operator pick on research grounding.
3. **Validator report is historical** — The frozen validator note remains accurate as *what was true at first pass*; the second pass should use `compare_to_report_path` to record regression or improvement; no IRA action on `.technical/Validator/` content.

## Proposed fixes (suggested_fixes)

| # | description | action_type | target_path | risk_level | constraints |
|---|-------------|-------------|-------------|------------|-------------|
| 1 | Replace the stale resolver snippet on the **Deepen (resume-deepen-a1b-bootstrap-20260330T233800Z-gmm)** line so it matches **`workflow_state`**: `gate_signature: none`, `queue_origin: layer1_a1b_empty_queue_bootstrap`, `effective_track: conceptual`, `gate_catalog_id: conceptual_v1`. Optionally one clause: “resolver telemetry reconciled post-validator per IRA cycle.” | rewrite_log_entry | `1-Projects/genesis-mythos-master/Roadmap/decisions-log.md` | low | Snapshot decisions-log before edit; single-bullet edit only for this queue id. |
| 2 | Add two **decision-defer rows** (or one combined row) under **## Conceptual autopilot** or adjacent decisions section: `D-2.2.1-intent-id-scope` and `D-2.2.1-dedupe-window`, each stating deferral to execution track / future RESUME_ROADMAP with links to phase note Open questions and optional validator ref. | write_log_entry | `1-Projects/genesis-mythos-master/Roadmap/decisions-log.md` | medium | Prefer new lines; do not remove operator pick; keep grep-stable `queue_entry_id` where relevant. |
| 3 | In the **2.2.1** phase note, under **Open questions**, prefix each bullet with the matching **`D-2.2.1-*`** id (or wikilink to the new decisions-log rows) so “deferred” is machine-auditable. | adjust_frontmatter / section_markers | `1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/Phase-2-2-Intent-Resolver-and-Hook-Mapping/Phase-2-2-1-Intent-Envelope-Normalization-and-Identity-Binding-Roadmap-2026-03-30-2338.md` | medium | Conceptual note may be frozen — if `frozen: true`, do **not** overwrite body; instead add **Conceptual-Amendments** atom per Vault-Layout with `parent_roadmap_note` + `amends_section: Open questions`. |

## Notes for future tuning

- When **`queue_entry_id`** encodes **bootstrap**, normalize **resolver telemetry** in one place first (**workflow_state**), then **propagate the same tuple** to decisions-log in the same commit to avoid hostile-validator churn.
- Consider a small **roadmap-deepen** or **logging** convention: on `gate_signature` reconciliation, auto-append a one-line **decisions-log echo** or flag `resolver_reconciled: true` in workflow frontmatter.

## Rationale (summary)

Layer 2 already satisfied **research_or_operator_close** (operator pick) and **resolver_telemetry_reconcile** in **`workflow_state`**. IRA closes the remaining **traceability gap** by aligning **decisions-log** with **`workflow_state`** and promoting **open questions** from prose-only to keyed deferrals, which directly addresses **`next_artifacts.open_questions_auditable`** without requiring new Agent-Research notes in this cycle.
