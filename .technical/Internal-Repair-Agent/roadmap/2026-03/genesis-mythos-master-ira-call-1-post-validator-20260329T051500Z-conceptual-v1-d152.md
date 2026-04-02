---
created: 2026-03-28
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: post-validator-roadmap-handoff-20260329T051500Z-d152
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 2
  medium: 1
  high: 0
validator_report_path: .technical/Validator/roadmap-handoff-auto-genesis-mythos-master-20260329T051500Z-conceptual-v1-post-d152-consolidated-forward-first.md
reason_codes:
  - missing_roll_up_gates
  - safety_unknown_gap
---

# IRA call 1 — post–nested-validator (conceptual_v1, D-152 slice)

## Context

First `roadmap_handoff_auto` pass (gate `conceptual_v1`) after RESUME_ROADMAP deepen completed with **medium** / **needs_work**: primary **`missing_roll_up_gates`**, secondary **`safety_unknown_gap`**. The report treats D-152 cross-file coherence as strong and explicitly frames rollup / REGISTRY-CI / min_handoff_conf as **execution-deferred**, not conceptual blockers. **`ira_after_first_pass: true`** — this IRA cycle is mandated even though the slice is internally consistent.

## Structural discrepancies

1. **`missing_roll_up_gates` (code vs prose):** The *reason code names* absent satisfied execution gates (HR ≥ `min_handoff_conf`, REGISTRY-CI closure). Vault prose already states **HR 92 < 93** and **REGISTRY-CI HOLD** and **`execution_handoff_readiness: 44`** on the phase note. There is no "missing sentence" problem to repair without either (a) real execution evidence or (b) a formal policy exception recorded with non-vault proof pointers — **vault-only edits cannot honestly clear this code.**

2. **`safety_unknown_gap`:** The validator did not read `prompt-queue.jsonl` (forbidden). The latest `workflow_state.md` **## Log** row documents **`next_queue_suggestion`** for Layer-1 Pass 3 **`inline_a5b_repair_drain`** but does **not** record an **attested outcome** of that check (verified / deferred / N/A). Structural closure for the second validator pass therefore requires **evidence-backed** logging after Layer 1 (or operator) actually inspects queue state — not speculative prose.

## Proposed fixes (for Roadmap / Layer 1 to apply under guardrails)

| Order | risk_level | action_type | target_path | description | constraints |
|----|-----|-----|----|----|----|
| 1 | low | write_log_entry | `1-Projects/genesis-mythos-master/Roadmap/workflow_state.md` | Append one **## Log** table row (or equivalent append-only audit block) recording **Layer-1 queue hygiene attestation** after a real read of `.technical/prompt-queue.jsonl` (and any configured queue-audit artifact): e.g. `pass3_inline_a5b_repair_drain: verified|deferred`, `duplicate_consolidated_forward_deepen_present: true|false`, `evidence: <Run-Telemetry path or queue-audit line id>`. | **Only if** the queue inspection actually occurred in the same run or an immediately prior Layer-1 pass; **never** assert `verified` without traceable evidence. |
| 2 | low | write_log_entry | `1-Projects/genesis-mythos-master/Roadmap/decisions-log.md` | Add a compact decision stub (next D-id) that **links** the validator report path and the new workflow log row / telemetry id, stating that **`safety_unknown_gap`** was closed by queue attestation **or** remains open with explicit deferral reason. | Apply only when the workflow_state row from fix 1 exists; keep body minimal to avoid bulk edits to frozen conceptual phase bodies. |
| 3 | medium | set_context_metrics | `1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md` | After the **next** non-advancing deepen, perform the validator's **skimmer stress-test**: reconcile **Phase 4 Machine cursor** paragraph vs `workflow_state.md` frontmatter (`last_run`, context fields) and patch **only** if a concrete mismatch is found (single paragraph or table cell). | Snapshot `roadmap-state.md` before/after per roadmap state invariants; **no** wholesale rewrite of deepen block stack. |

## Notes for future tuning

- **`missing_roll_up_gates` on conceptual_v1** will keep firing until execution track supplies CI/registry evidence or a documented exception with external pointers; treating it as a signal to **recal** on conceptual track is **explicitly disallowed** per project D-060 / queue guidance — orchestration should tier it as advisory only.
- Consider having Layer 1 always emit one **queue_audit_echo** field into Run-Telemetry when EAT-QUEUE finishes Pass 3 repair drain, so Roadmap can cite it without re-reading the queue in the Roadmap Task.

## IRA outcome

**status:** `repair_plan` — two low-risk, one medium-risk **conditional** vault edits; **no** recommendation to clear rollup gates via prose alone or to **recal** solely for **`missing_roll_up_gates`** on conceptual track.
