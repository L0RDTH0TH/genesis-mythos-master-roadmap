---
title: Feedback Log
created: 2026-03-01
tags: [pkm, second-brain, logs, feedback, observability]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/Logs]]"]
---

# Feedback Log

`2026-03-28T22:20:00Z` — **conceptual_execution_gate_advisory** — queue_entry_id `followup-deepen-post-d129-workflow-log-reconcile-gmm-20260328T220800Z` — effective_track conceptual — primary_code `missing_roll_up_gates` (+ `safety_unknown_gap` in reason_codes) — A.5b.0 skip auto-repair append (L1 post-LV report `.technical/Validator/roadmap-handoff-auto-genesis-mythos-master-20260328T221000Z-layer1-postlv-d129.md`).

`2026-03-28T22:20:00Z` — **ledger_semantic_attestation_soft** — queue_entry_id `followup-deepen-post-d129-workflow-log-reconcile-gmm-20260328T220800Z` — Roadmap return: `nested_validator_first` outcome `not_applicable` / `task_tool_invoked: false` (L2 Task(validator) unavailable); strict_nested_return_gates false — consumption allowed per queue.mdc A.5 (b0)(iii) soft path.

`2026-03-29T00:15:00Z` — **tiered_post_little_val_repair_append** — queue_entry_id `followup-deepen-post-d132-bounded-415-gmm-20260328T191600Z` — A.5b.3 appended `repair-l1-postlv-notes-skimmer-d132-gmm-20260329T001000Z` (handoff-audit) after L1 post-LV hard block primary_code `state_hygiene_failure`; report `.technical/Validator/roadmap-handoff-auto-genesis-mythos-master-20260328T222030Z-conceptual-v1-post-l1-little-val-d132.md`. Also merged Layer-2 `queue_followups` line `followup-deepen-post-d135-bounded-415-continue-gmm-20260328T235959Z`.

`2026-03-28T22:45:00Z` — **conceptual_execution_gate_advisory** — queue_entry_id `resume-deepen-followup-post-d123-bounded-415-gmm-20260328T190000Z` — effective_track conceptual — primary_code `missing_roll_up_gates` — A.5b.0 skip auto-repair append (L1 post-LV third pass; report `.technical/Validator/roadmap-handoff-auto-genesis-mythos-master-20260328T221530Z-third-pass-compare-d134-conceptual-v1.md`).

`2026-03-28T23:40:00Z` — **ledger_semantic_attestation_soft** — queue_entry_id `followup-deepen-post-d130-continuation-bounded-415-gmm-20260328T124500Z` — Roadmap return nested_subagent_ledger: nested_validator_first / nested_validator_second / ira_post_first_validator rows with invoked_ok and task_tool_invoked false (host Task(validator) unavailable in L2); strict_nested_return_gates false — consumption allowed per queue.mdc (b0)(iii) soft path.

`2026-03-28T03:15:00Z` — **conceptual_execution_gate_advisory** — queue_entry_id `repair-l1-postlv-state-hygiene-post-d112-phase4-gmm-20260327T221000Z` — effective_track conceptual — primary_code `missing_roll_up_gates` — A.5b.0 skip auto-repair append (L1 post-LV duplicate pass).

`2026-03-26T23:55:00Z` — **conceptual_execution_gate_advisory** — queue_entry_id `followup-recal-post-413-shallow-deepen-gmm-20260326T233500Z` — effective_track conceptual — primary_code `missing_roll_up_gates` — A.5b.0 skip auto-repair append.

`2026-03-26T16:05:00Z` — **conceptual_execution_gate_advisory** — queue_entry_id `resume-deepen-post-recal-distilled-yaml-gmm-20260326T041500Z-followup` — effective_track conceptual — primary_code `missing_roll_up_gates` — A.5b.0 skip auto-repair append.

`2026-03-26T12:30:00Z` — **conceptual_execution_gate_advisory** — queue_entry_id `followup-recal-post-deepen-0408-gmm-20260326T041500Z` — effective_track conceptual — primary_code `missing_roll_up_gates` — A.5b.0 skip auto-repair append.

Aggregated user-refinement stats, loop outcomes, and queue analytics. Used for MOC aggregation (e.g. [Vault-Change-Monitor](3-Resources/Vault-Change-Monitor.md)) and evolution monitoring.

## Purpose

- **Loop outcomes**: Log when mid-band loops run (pre_loop_conf, post_loop_conf, loop_outcome, loop_type).
- **User refinements**: e.g. "40% of previews refined — consider increasing default depth"; aggregate from pipeline runs and queue-cleanup.
- **Queue analytics**: Batch merge counts (overlap detection), preview caps, commander_macro stats (e.g. "Most used: Queue Perspective (15x this week)").
- **Dataview-friendly fields**: drift_avg, loop_refinements_count, and other numeric/categorical fields for queries.

## Format (per entry)

One line or short block per run; no PII. Example fields:

- timestamp (ISO 8601 or YYYY-MM-DD HH:MM)
- pipeline or source (e.g. queue-cleanup, async-loop, distill)
- loop_attempted, pre_loop_conf, post_loop_conf, loop_outcome, loop_reason
- drift_avg (when applicable)
- loop_refinements_count (when applicable)
- commander_macro (when Commander-triggered)
- summary (one-line, e.g. "User refines 40% of previews")

## Queue (append-only)

- 2026-03-24T02:12:00Z — EAT-QUEUE Layer 1: consumed `resume-deepen-phase4-primary-post-advance-idempotent-gmm-20260324T001800Z`; post–little-val `roadmap_handoff_auto` hard block `contradictions_detected`; A.5b appended repair `RESUME_ROADMAP` `handoff-audit` (`repair-handoff-audit-contradictions-layer1-20260324T021200Z`); merged pipeline `queue_followups` recal (`resume-recal-post-p4-1-1-deepen-gmm-20260324T002000Z`).

## Rotation

- Rotate with [log-rotate](.cursor/skills/log-rotate/SKILL.md) (e.g. monthly or with other pipeline logs). See [Logs.md](3-Resources/Second-Brain/Logs.md) for rotation spec.

## See also

- [Logs](3-Resources/Second-Brain/Logs.md) — all log destinations and rotation
- [Parameters](3-Resources/Second-Brain/Parameters.md) — Async-Loop Flow, confidence bands
- [Queue-Sources](3-Resources/Second-Brain/Queue-Sources.md) — queue modes and Commander-Sourced
