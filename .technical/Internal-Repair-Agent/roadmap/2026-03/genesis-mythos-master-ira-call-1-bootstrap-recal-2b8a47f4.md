---
created: 2026-03-22
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: 2b8a47f4-f18e-44c0-9c08-2aa7a07fb02e
ira_call_index: 1
status: repair_plan
risk_summary: { low: 3, medium: 2, high: 1 }
parent_run_id: l1-eatq-20260322-bootstrap-recal-2b8a
validator_first_pass: .technical/Validator/roadmap-auto-validation-20260322T210500Z-gmm-bootstrap-recal-2b8a-first.md
tags: [ira, roadmap, genesis-mythos-master, recal, bootstrap-2b8a]
---

# IRA call 1 — genesis-mythos-master — bootstrap `recal` `2b8a47f4`

## Context

Validator-driven invocation after **first** `roadmap_handoff_auto` pass on **RESUME_ROADMAP** `recal` for queue **`2b8a47f4-f18e-44c0-9c08-2aa7a07fb02e`** (`parent_run_id` **`l1-eatq-20260322-bootstrap-recal-2b8a`**). Verdict: **medium** / **`needs_work`**; **`primary_code`:** **`missing_roll_up_gates`**; **`reason_codes`:** **`missing_roll_up_gates`**, **`missing_task_decomposition`**, **`safety_unknown_gap`**. Contaminated-report rule applied: validator output treated as **weak minimum** — expanded checks on **roadmap-state** (21:05 UTC block), **workflow_state**, **decisions-log**, **phase 3.4.8** / **3.4.9**, **distilled-core**.

**Invariant:** Do **not** fabricate **D-044** **RegenLaneTotalOrder_v0** A/B or **D-059** **ARCH-FORK-01/02** picks. Roll-up **HR 92** vs **`min_handoff_conf` 93** remains **true** structural debt until operator/repo gates clear.

## Structural discrepancies

1. **`safety_unknown_gap` (amplified):** [[roadmap-state]] **§ 2026-03-22 21:05 UTC** uses **`[!success]`** while **Nested validation** is still a **placeholder** (“until host `Task` cycle completes”) even though the **first** validator report already exists on disk — **success-theater** risk vs nested-cycle honesty. Neighbor block (**20:35 UTC**) already lists concrete first / IRA / compare-final paths.
2. **`missing_task_decomposition` (amplified):** [[phase-3-4-8-high-context-util-policy-and-phase-4-stub-readiness-roadmap-2026-03-22-1205]] **Post-`recal` hygiene** rows **1–2** are **`[x]`** but **Evidence** still anchors to **12:25** deepen / **82% / 76 / `gmm-a1b-bootstrap-deepen-20260322T122045Z`** while authoritative **`workflow_state`** cursor is **19:25** deepen · **Ctx 84%** · **`gmm-deepen-post-recal-followup-20260322T1925Z`** — **junior-hazardous** unless reframed as time-stamped baseline **plus** latest **YAML/`## Log` parity** reaffirmation (e.g. cite **`2b8a…`** / **`l1-eatq-20260322-bootstrap-recal-2b8a`**).
3. **`missing_roll_up_gates` (confirmed, not fixable by picks):** **D-046** / **D-050** / **D-055** document **G-P3.2-** / **G-P3.3-** / **G-P3.4-*** rollups **HR 92** **<** **93** with **HOLD** rows pending **D-044** (and registry rows) — consistent with [[decisions-log]]; no vault edit can clear **HOLD** without operator/VCS truth.
4. **Metric drift:** [[distilled-core]] Phase **3.4.9** bullet still says **ctx 82%** for high-util **`recal`** follow-up; **workflow_state** frontmatter / last deepen row show **84%** after **`gmm-deepen-post-recal-followup-20260322T1925Z`**.
5. **Cross-file nested trace:** **workflow_state** Notes (**21:05** `recal` row narrative) attest nested **Task(validator)** / **Task(internal-repair-agent)** but **roadmap-state** consistency block did not yet mirror **concrete** first-pass path for this queue id.

## Proposed fixes

See parent return **`suggested_fixes`** (ordered **low → medium → high**). Skipped: any edit that would **log** **D-044** A/B or **D-059** fork without operator action.

## Notes for future tuning

- When **`ira_after_first_pass: true`**, roadmap pipeline should **pre-fill** `roadmap-state` nested-validation lines with **first-pass path** as soon as the file is written—avoid placeholder under **`[!success]`**.
- **3.4.8** ladder **Evidence** fields should include **“baseline established … / reaffirmed (date) vs last `## Log` row”** pattern whenever **`workflow_log_authority: last_table_row`** advances past the original hygiene closure id.
- Consider a **single** “rollup HOLD dashboard” note or table (read-only index) to reduce repeated prose in **roadmap-state** — optional doc hygiene, not gate closure.
