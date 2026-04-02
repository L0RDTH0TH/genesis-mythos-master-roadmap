---
created: 2026-03-31
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: followup-deepen-phase4-41-rollup-gmm-20260403T211500Z
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 4
  medium: 1
  high: 0
validator_report_path: .technical/Validator/roadmap-handoff-auto-gmm-20260403T231500Z-followup-deepen-phase5-1-1.md
---

# IRA report — roadmap / Validator→IRA cycle (call 1)

## Context

Roadmap subagent invoked IRA after nested `roadmap_handoff_auto` on **Phase 5.1.1** deepen (`effective_track: conceptual`). The validator returned **medium / needs_work** with **`missing_roll_up_gates`** (advisory on conceptual track) and **`safety_unknown_gap`** (ordinal ambiguity for conflict matrix vs kernel schedule; **GWT-5.1.1-C** evidence chain vs **Given/When/Then**). **Little val** was already structurally aligned; this cycle addresses **NL clarity** so a second validator pass has less agreeability surface—not a claim of execution rollup.

## Structural discrepancies

1. **Advisory `missing_roll_up_gates`:** Vault already waives execution rollup in `roadmap-state.md` Notes; validator still emits the code for execution-handoff traceability—**not** a conceptual contradiction.
2. **Ordinal ambiguity:** **Secondary 5.1** lists **5.1.1+** decomposition of kernel scheduling vs conflict matrix without pinning **5.1.2** vs **5.1.3**; **5.1.1** note uses **5.1.3+** in Out of scope but **5.1.3+** in Downstream—future routing can mis-infer split depth.
3. **GWT-5.1.1-C:** Table maps Evidence to **§ Behavior (3)** (replay identity); **Then** names **Ledger row** / **Rule outcome**—needs explicit bridge so Evidence is not read as replay-only hand-waving.
4. **RECAL ~88%:** `workflow_state` frontmatter **`last_ctx_util_pct: 88`** and **2026-04-03 23:15** log row already recommend **RECAL-ROAD** before more **5.1.x** deepens—operational follow-up, not incoherence.

## Proposed fixes (caller-applied)

See structured **`suggested_fixes`** in parent return payload (risk-tagged). Prefer order: **low** (GWT + waiver gloss + RECAL queue) → **medium** (cross-note ordinal contract) before second validator pass.

## Notes for future tuning

- When **secondary** uses **5.1.1+** and **tertiary** uses **5.1.3+**, add a **single canonical ordinal line** in roadmap-deepen or template for Phase 5.1 to reduce validator **safety_unknown_gap** recurrence.
- For conceptual track, consider emitting **`missing_roll_up_gates`** with sub-field **`conceptual_waiver_ack: true`** in validator payloads when waiver text is grepped—reduces redundant IRA cycles (system-level; not a vault edit here).
