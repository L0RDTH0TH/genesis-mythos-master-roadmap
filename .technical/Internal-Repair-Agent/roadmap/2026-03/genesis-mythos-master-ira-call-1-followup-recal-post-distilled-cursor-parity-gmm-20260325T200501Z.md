---
created: 2026-03-25
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: followup-recal-post-distilled-cursor-parity-gmm-20260325T200501Z
ira_call_index: 1
status: repair_plan
risk_summary: { low: 2, medium: 2, high: 1 }
validator_report_path: .technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260325T213045Z-recal-post-distilled-parity-first.md
---

# IRA — genesis-mythos-master (validator-driven, call 1)

## Context

Hostile `roadmap_handoff_auto` first pass (`…213045Z…`) returned **`needs_work`**, **`primary_code: state_hygiene_failure`**, with explicit gap: `workflow_state.md` **`## Log`** row **2026-03-25 12:00** / conceptual deepen **4.1.1.8** teaches **present-tense** “**Authoritative cursor (YAML)**” = `last_auto_iteration` **`resume-deepen-post-second-pass-needs-work-gmm-20260325T020600Z`**, which **contradicts** live YAML frontmatter **`last_auto_iteration: "eatq-antispin-obs-test-gmm-20260325T180000Z"`** and **`current_subphase_index: "4.1.1.10"`**. Scoped parity on distilled-core / roadmap-state / frontmatter was **not** regressed per validator; the failure is **skimmer/teach-surface** hygiene in one log cell. Other reason codes (**`missing_roll_up_gates`**, **`safety_unknown_gap`**, **`missing_acceptance_criteria`**) are **honest rollup/debt** citations — **no vault prose should claim closure** there without repo evidence.

## Structural discrepancies

1. **Poison teach cell (primary):** `Status / Next` prose in the **4.1.1.8** row equates “Authoritative cursor (YAML)” to **`020600Z`** as if it were the live machine cursor, conflicting with frontmatter **`180000Z`**.
2. **Stale repair narratives (secondary risk):** Rows **15:30** and **15:00** handoff-audit cells **accurately describe** past repairs that aligned text to **`020600Z`** at that time; a fast skimmer may misread them as **current** YAML authority unless context is clear (optional clarification only if second pass still flags).

## Proposed fixes (apply order: low → medium → high)

See structured `suggested_fixes` in parent return JSON; summarized here:

1. **Low —** Rewrite **only** the **4.1.1.8 / 2026-03-25 12:00** row’s **Status / Next** fragment: **remove** unconditional “Authoritative cursor (YAML) = `020600Z`”. **Replace** with (a) explicit pointer that **live** `last_auto_iteration` + `current_subphase_index` are **only** in YAML frontmatter; (b) **historical / as-of** wording for `020600Z` as the deepen id tied to **that** narrative moment; (c) explicit **supersession pointer** to later log rows (**12:00** AppendWitness deepen, **18:15** `eatq-antispin…`) **without** claiming rollup/CI closure.
2. **Low —** Read-only grep of `## Log` for `Authoritative cursor` / teach-style `last_auto_iteration` **literals**; patch any other cell that states a **present-tense** YAML authority string **≠** current frontmatter (expect **none** beyond row 53 after fix 1).
3. **Medium —** If second validator pass still flags **15:30** / **15:00** audit rows: append a **short clause** that those lines are **repair narrative as-of** that timestamp and **do not** override frontmatter (do **not** rewrite factual “we aligned to X at the time” unless misleading).
4. **Medium —** **Procedural:** After edits, RoadmapSubagent runs **snapshot** (pre/post per MCP rules), **little val**, **second** `roadmap_handoff_auto` with `compare_to_report_path` = initial report.
5. **High —** **`missing_roll_up_gates` / `safety_unknown_gap` / `missing_acceptance_criteria`:** treat as **non-vault** closure work (repo/registry/CI evidence or documented policy exception per validator `next_artifacts[4]`). **Do not** “fix” via optimistic prose in `workflow_state`.

## Notes for future tuning

- **Pattern:** “Conceptual deepen” rows with **`no machine cursor advance`** still carried a **synthetic** “Authoritative cursor (YAML)” line that **froze** an old `last_auto_iteration` after later automation advanced the cursor — template should say **never** echo a literal `last_auto_iteration` value in-table except **matching frontmatter** or **explicit historical fence**.
- **roadmap-deepen / handoff-audit:** When prepending rows that advance cursor, consider a **lint** or little-val check: any `## Log` cell containing **`Authoritative cursor`** must either match frontmatter or include **`as-of`** / **`superseded`**.

## Machine return (summary)

- **status:** `repair_plan`
- **Primary actionable gap:** single **4.1.1.8** log cell wording vs frontmatter `eatq-antispin…180000Z`.
