---
created: 2026-03-23
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-roadmap-genesis-mythos-master-20260323-deepen-suggested-251
parent_run_id: queue-eat-20260323-resume-gmm-251
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 2
  medium: 1
  high: 1
validator_report_path: .technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260323T180530Z-first.md
---

# IRA call 1 — RESUME_ROADMAP deepen queue 251 (post–first-pass `roadmap_handoff_auto`)

## Context

Nested **roadmap_handoff_auto** first pass returned **high** / **block_destructive** with **primary_code** `state_hygiene_failure` (stale `workflow_state.md` frontmatter vs last `## Log` row), plus `missing_task_decomposition` and `safety_unknown_gap` (D-044 fork, open Tasks). The parent Roadmap subagent **already reconciled** frontmatter **`last_ctx_util_pct` / `last_conf`** to **69 / 84**, appended **Notes** and a per-change snapshot, matching the **2026-03-23 18:05** log row for this queue id. **Little val** was not the IRA trigger here; validator gaps drive this branch.

## Structural discrepancies (current read)

1. **`state_hygiene_failure` (remediated):** Frontmatter **69 / 84** agrees with the last data row of the first `## Log` table and with **roadmap-state.md** RECAL block **2026-03-23 18:05** (69%, 84). Dual-truth on automation fields **no longer present** at IRA read time.
2. **`missing_task_decomposition` (residual):** Phase **3.4.2** still has **three** unchecked `## Tasks` items without an explicit **DEFERRED / WAITING_ON** ledger (validator asked for 3.4.1-style honesty).
3. **`safety_unknown_gap` (residual, expected):** **D-044** documents **RegenLaneTotalOrder_v0** **A/B** as **TBD** in **decisions-log**; phase **3.4.2** `handoff_gaps` correctly flags dual-track interleaving until operator logs **A** or **B**. No vault automation should invent the fork.

## Proposed fixes (for Roadmap subagent apply pass)

| Order | Risk | Action | Target |
|------|------|--------|--------|
| 1 | low | Conditional frontmatter sync | `workflow_state.md` — only if re-read shows mismatch vs last log row |
| 2 | medium | Task ledger (DEFERRED/BLOCKED) | `phase-3-4-2-...-2026-03-23-1805.md` |
| 3 | high | D-044 A/B closure line | `decisions-log.md` — **only after operator choice** |

## Notes for future tuning

- **Race:** First validator pass can read **stale YAML** before deepen’s final write of `last_ctx_util_pct` / `last_conf`; parent-side **reconcile + Notes + snapshot** after first pass matches the pattern used on queues **247**, **250**. Consider ordering validator after FM write or single atomic state commit in roadmap-deepen to reduce repeats.
- **Compare-final:** Second nested validator should use **`compare_to_report_path`:** `.technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260323T180530Z-first.md` per validator next-artifacts.
