---
created: 2026-03-20
pipeline: research
project_id: genesis-mythos-master
queue_entry_id: resume-roadmap-genesis-mythos-master-phase2-deepen-20260319-2035-followup
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 2
  medium: 5
  high: 1
validator_report_path: 3-Resources/Second-Brain/Validator-Reports/research_synthesis/genesis-mythos-master-20260320T000000Z.md
synth_note: Ingest/Agent-Research/phase-2-1-5-spawn-commit-research-2026-03-19-2035.md
---

# IRA — research synthesis repair (Phase 2.1.5 / deepen injection)

## Context

ResearchSubagent produced `phase-2-1-5-spawn-commit-research-2026-03-19-2035.md` for queue entry `resume-roadmap-genesis-mythos-master-phase2-deepen-20260319-2035-followup`. Hostile validator `research_synthesis` returned **medium / needs_work** with reason codes `safety_unknown_gap`, `missing_command_event_schemas`, and `missing_task_decomposition`. This IRA call is **validator-driven** (`ira_after_first_pass: true`). The synthesis is directionally useful (Unity ECB) but **under-evidenced**, uses **non-phase terminology** (`idempotency_ledger_key`), leans on a **GitHub issue** for idempotency claims, and omits **replay-harness** and **schema-level** content required for safe roadmap-deepen injection.

## Structural discrepancies

1. **Provenance gap:** Section "Raw sources (vault)" states no raw captures — violates deepen handoff expectation for auditable quotes.
2. **Schema drift:** Bullet ties idempotency to `idempotency_ledger_key`; phase normative vocabulary is `spawn_idempotency_key := (stream_id, spawn_batch_id, spawn_row_stable_id, spawn_commit_semver)` and related fields — no mapping table.
3. **Weak idempotency anchor:** Bevy issue #20321 is discussion, not shipped API invariant — alone it cannot support "must not duplicate" language for injection.
4. **Coverage vs phase title:** Phase emphasizes **replay harness**; synthesis has no subsection on golden vectors, double-apply, or snapshot diff tied to `replay_spawn_commit` pseudo-code.
5. **No decomposed tasks:** "Industry patterns" claim without checklist mapping external practices → concrete engineering tasks / acceptance checks.

## Proposed fixes

See structured `suggested_fixes` in parent return payload (same ordering: low → medium → high preference for application).

## Notes for future tuning

- **research-agent-run** should default to at least one **Raw/** capture or mandatory inline fenced excerpt when `web_search` is the only tool — empty raw section should fail pre-validator gate.
- Validator reason code **`missing_command_event_schemas`** maps cleanly to a **template subsection** in synth notes: "Normative field glossary (read-only from phase)" + "External analogy → field mapping" to reduce schema drift in deepen chains.
- Repeated **Unity-only** ECS analogies for this project suggest a **second-engine** minimum in Param-Table or research skill checklist when `linked_phase` mentions replay.
