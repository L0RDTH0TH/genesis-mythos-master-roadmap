---
created: 2026-04-07
pipeline: roadmap
project_id: sandbox-genesis-mythos-master
queue_entry_id: post-validator-distilled-core-mismatch-reconciled
ira_call_index: 1
status: repair_plan
risk_summary: { low: 0, medium: 0, high: 0 }
---

# IRA — post-validator distilled-core vs workflow_state (reconciled by Roadmap subagent)

## Context

First nested `roadmap_handoff_auto` pass reported `contradictions_detected` / `distilled_core_vs_workflow_state_mismatch`: narrative in `distilled-core.md` (Phase 3 mega-heading and Phase 5 heading) treated **`current_subphase_index`** as **`6.1`** (next deepen on secondary slice) while **`workflow_state.md`** authoritative cursor was **`"6"`** (primary Phase 6 rollup next, after secondary **6.1** rollup completion). The Roadmap subagent applied targeted edits to **`distilled-core.md`** so the live routing prose matches **secondary 6.1 rollup complete** and **next RESUME = Phase 6 primary rollup** vs rolled-up **6.1**.

## Structural discrepancies (pre-repair; closed)

1. **Stale cursor in distilled-core:** Mega-heading / Phase 5 heading implied **`6.1`** as the workflow cursor while **`workflow_state`** frontmatter had **`current_subphase_index: "6"`**.
2. **Semantic gap:** Confusing “next deepen target” (**6.1** chain) with **subphase index** after rollup closure — index **`6`** is the canonical primary-container cursor post-**6.1** rollup per project convention.

## Proposed fixes

**None.** On-disk verification (2026-04-07) shows:

- `1-Projects/sandbox-genesis-mythos-master/Roadmap/workflow_state.md`: `current_phase: 6`, `current_subphase_index: "6"` (comment: secondary 6.1 rollup complete; next Phase 6 primary rollup).
- `distilled-core.md` **## Phase 3 living simulation** mega-heading and **## Phase 5 rule system integration** heading: **`current_subphase_index: "6"`**, secondary **6.1** noted **complete** where relevant, next step **Phase 6 primary** rollup.

Manual / Roadmap-subagent repair is sufficient for this mismatch; second validator pass should re-check `distilled_core_vs_workflow_state_mismatch` only if new edits regress routing prose.

## Notes for future tuning

- **Patterns:** Rollup-completion events often require flipping **`current_subphase_index`** from **`6.1`** → **`6`**; validators should treat **6.1** mentions in distilled-core as **historical slice labels** when paired with explicit “rollup complete” + **`"6"`** cursor, not as a second live cursor.
- **Automation:** Consider a one-line **“authoritative cursor”** stub in distilled-core Phase 0 anchors that is mechanically copied from **`workflow_state`** frontmatter on each deepen (reduces mega-heading drift).
