---
created: 2026-04-08
pipeline: roadmap
project_id: godot-genesis-mythos-master
queue_entry_id: followup-deepen-exec-p213-tertiary-godot-20260408T224100Z
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 2
  medium: 2
  high: 1
validator_primary_code: missing_roll_up_gates
---

# IRA — roadmap / RESUME_ROADMAP (post-first-validator, execution track)

## Context

Nested `roadmap_handoff_auto` returned **`needs_work`** with **`primary_code: missing_roll_up_gates`** plus **`safety_unknown_gap`**. Iter **17** in `workflow_state-execution` matches tertiary **2.1.4** mint; `roadmap-state-execution` already states Phase 2 chain gates **`phase2_gate_validation_parity`** (in-progress) and **`phase2_gate_replay_traceability`** (open) until tertiary **2.1.5** lands. The hostile validator correctly refuses **execution-chain closure** while **2.1.5** is unminted and while **2.1.4** replay/diff content is **junior stub** without concrete engine/repo anchors.

**Operator policy for this cycle:** advisory execution-deferred gates (Dual-Roadmap-Track) — **do not** invent repo paths or demand implementation proof in-vault; prefer **low-risk narrative alignment** on execution state and **explicit vault-level bindings** for stubs.

## Structural discrepancies

1. **`missing_roll_up_gates`:** Roll-up truth is **already** in `roadmap-state-execution` Phase 2 bullet, but the **Execution gate tracker** in `workflow_state-execution` does **not** list the Phase 2 **chain** gates (`phase2_gate_*`), so machine roll-up visibility is weaker than rollup anchors for Phase 1.
2. **`safety_unknown_gap`:** `Phase-2-1-4-Execution-Bundle-Identity-Seam-Catalog-Stability-and-Replay-Diff-Roadmap-2026-04-08-2241.md` cites PASS rows against **stub** pseudocode (`## Replay / diff pseudocode (junior-dev stub)`) without an explicit **advisory binding** table that ties names to **in-vault** evidence anchors (validator treats this as unknown safety surface).
3. **Definition of done (validator `next_artifacts`):** Real closure requires **mint 2.1.5** + evidence rows — cannot be fully satisfied by copy edits alone.

## Proposed fixes

See parent return `suggested_fixes[]`. Apply in **low → medium → high** order; snapshot execution state + 2.1.4 note before edits per roadmap guardrails.

## Notes for future tuning

- When **`handoff_readiness`** is high but content is stub-heavy, add a standard **“advisory artifact binding”** subsection in execution tertiaries so `safety_unknown_gap` resolves without fake repo paths.
- Consider a **Phase 2 chain gate** mini-table template in `workflow_state-execution` for any execution project using `phase2_gate_*` tokens.
