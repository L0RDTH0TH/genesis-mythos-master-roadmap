---
created: 2026-03-22
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-gmm-deepen-followup-post-a1b-20260322T132000Z
ira_call_index: 1
parent_run_id: pr-eatq-resume-gmm-deepen-20260322T1400Z
status: repair_plan
validator_report_path: .technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260322T132030Z-first.md
risk_summary: { low: 2, medium: 5, high: 1 }
---

# IRA — genesis-mythos-master — validator-driven call 1

## Context

Post–first-pass **`roadmap_handoff_auto`** for queue **`resume-gmm-deepen-followup-post-a1b-20260322T132000Z`**. Verdict: **`needs_work`**, **`primary_code: missing_task_decomposition`**, secondary **`safety_unknown_gap`**. Machine cursor (workflow_state vs last log row) was reported consistent; gaps are **traceability / honesty / decomposability** of tertiary **3.4.6** vs **distilled-core**, open Tasks vs DEFERRED contract, lane-A fixture anchor, **D-044** unpicked fork, and **3.4.5** idempotency **TBD**. Contaminated-report rule applied: treat validator findings as a **weak minimum** (expect additional tightening).

## Structural discrepancies

1. **Roll-up desync:** **D-057** exists in **decisions-log** but **distilled-core** `core_decisions` YAML and body **Core decisions** stop at **3.4.5** — breaks distilled core vs phase spine for readers and downstream injectors.
2. **`missing_task_decomposition`:** **3.4.6** `## Tasks` is six naked `[ ]` lines while the note claims execution-facing decomposition; validator requires **either** evidence closure (check + link) **or** explicit **DEFERRED** rows (owner, blocker, unblock, evidence).
3. **`safety_unknown_gap` (lane A):** No canonical **fixture id** + **where it lives** (repo vs vault companion) — harness sketch references fixtures abstractly only.
4. **`safety_unknown_gap` (D-044):** **RegenLaneTotalOrder_v0** A/B still unpinned; validator asks for logged pick **or** wrapper — Roadmap-only scope forbids fabricating A/B; honesty can still be tightened in-vault under **Roadmap/** via **decisions-log** + **3.4.6** guardrails.
5. **`safety_unknown_gap` (idempotency):** **3.4.5** `tool_action_idempotency_key` duplicate semantics **TBD** blocks crisp **T-DM-P02** story; needs explicit cross-link and deferral pointer (still **Roadmap/**).

## Proposed fixes (for Roadmap subagent)

See parent return **`suggested_fixes`** JSON array (apply low → medium → high when gates pass).

## Notes for future tuning

- When a decisions-log row (**D-057**) lands before **distilled-core** sync, add a **roadmap-deepen** or **handoff** checklist step: mirror new D-* in distilled-core same pass.
- Tertiary notes that introduce **T-*** IDs should default to a **DEFERRED ledger** table alongside checklists to satisfy hostile **missing_task_decomposition** without pretending repo work exists.
- **Lane fixture stub** pattern: one frontmatter key (e.g. `lane_a_fixture_id_stub`) could become a little-val / validator field for automation.
