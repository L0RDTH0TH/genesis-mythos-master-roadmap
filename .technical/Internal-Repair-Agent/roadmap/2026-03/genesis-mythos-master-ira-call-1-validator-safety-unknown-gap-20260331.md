---
created: 2026-03-31
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: validator-post-safety-unknown-gap-252
ira_call_index: 1
status: repair_plan
risk_summary: { low: 3, medium: 2, high: 1 }
validator_report_path: 3-Resources/Second-Brain/Validator-Reports/roadmap_handoff_auto/genesis-mythos-master-20260331T223200Z-2-5-2-conceptual-v1.md
primary_code: safety_unknown_gap
---

# IRA — genesis-mythos-master (validator-driven, post–first-pass)

## Context

Roadmap nested validator `roadmap_handoff_auto` reported **`severity: medium`**, **`recommended_action: needs_work`**, **`primary_code: safety_unknown_gap`**, with secondary **`missing_roll_up_gates`** (advisory on conceptual track). The host invoked IRA after the first validator pass to turn **`next_artifacts`** into an apply-ordered repair plan. Canonical state in **`roadmap-state.md`** and **`workflow_state.md`** already agrees: **`current_subphase_index: "2.5.2"`** is the last minted deepen target in the log row, with **next: 2.5.3**; Phase 2 summary lists tertiary **2.5.2** minted. The gaps are **rollup narrative** in **`distilled-core.md`**, **metric semantics** on the **2.5.2** phase note, and **CDR validation tag** consistency in **`decisions-log.md`**.

## Structural discrepancies

1. **Stale distilled rollup:** `distilled-core.md` section heading still reads **“Phase 2.5 telemetry slice (2.5.1–2.5.2 in progress)”**, implying the 2.5.1–2.5.2 span is unfinished, while state and phase notes show **2.5.1** and **2.5.2** minted and workflow cursor at **2.5.3**.
2. **Frontmatter metric clash:** Phase **2.5.2** note has **`progress: 38`** and **`handoff_readiness: 86`** without an on-note rubric; readers infer incompatible stories.
3. **CDR validation bar:** `decisions-log.md` lists **2.5.2** CDR as **`validation: pattern_only`** immediately adjacent to **2.5.1** **`evidence_backed_conceptual`**, without explaining why the bar differs for sibling tertiaries.

**Non-issues (this pass):** No edit proposed for **`roadmap-state.md`** or **`workflow_state.md`** — validator found no contradiction with cursor narrative. **`missing_roll_up_gates`** is execution-deferred per catalog; optional stub below is **high** risk and optional.

## Proposed fixes (apply order: low → medium → high)

See structured `suggested_fixes` in the Roadmap subagent return payload (mirror below).

### Low

1. **`distilled-core.md`** — Rename section (~line 61) to a state-aligned title (e.g. **Phase 2.5 telemetry slice (2.5.1–2.5.2 minted; next 2.5.3)**). Adjust the paragraph to state both tertiaries are minted and the **active deepen cursor** is **2.5.3** under secondary **2.5**, matching `roadmap-state` Phase 2 bullet and `workflow_state` last log row.
2. **`decisions-log.md`** — Under the **2.5.2** decision-record line, add a **one-line clarification** that **`pattern_only`** here means the CDR captures NL + checklist pattern continuity atop **2.5.1** sink-binding evidence, whereas **`evidence_backed_conceptual`** on **2.5.1** marked the first-class sink-binding claims (or equivalent accurate distinction). Do not rewrite CDR bodies from IRA.
3. **`Phase-2-5-2-Cross-Sink-Correlation-and-Deterministic-Timeline-Ordering-Roadmap-2026-03-31-2200.md`** — Insert a short **`> [!note] Metrics rubric`** (or `### Metrics rubric`) immediately after the title block: **`progress`** = approximate slice checklist / AC row fill density for this tertiary; **`handoff_readiness`** = delegatability score from hand-off-audit dimensions (orthogonal to progress). Snapshot before edit per roadmap MCP rules.

### Medium

4. **Same 2.5.2 phase note** — After the rubric is visible, **either** (a) leave numbers unchanged if the rubric resolves the absurdity, **or** (b) with backup + snapshot, **reconcile** `progress` and/or `handoff_readiness` so the pair is not prima facie contradictory (e.g. re-run **hand-off-audit** skill and adopt its `handoff_readiness`, or adjust `progress` to match documented checklist completion). **Constraint:** only if post-rubric human or pipeline agrees; do not auto-inflate readiness.
5. **Secondary 2.5 note** (`Phase-2-5-Deterministic-Decision-Telemetry-and-Post-Commit-Audit-Bridge-Roadmap-2026-03-31-1307.md`) — If its summary line still implies the whole **2.5** chain is “opening” only, add **one sentence** that **2.5.1** and **2.5.2** tertiaries are minted and **2.5.3** is next (only if stale on read).

### High

6. **Optional execution handoff** — When **`effective_track`** becomes **execution**, add a short **roll-up stub** (primary Phase 2 outcome rows satisfied by **2.5.2**) per Dual-Roadmap-Track. **Not** required for conceptual **`needs_work`** closure; skip if snapshots or confidence fail.

## Notes for future tuning

- **roadmap-deepen / distilled-core:** After each tertiary mint under **2.5.x**, run a **distilled-core Phase 2.5** subsection refresh (or queue **sync-outputs**) so rollup cannot lag state.
- **CDR skill:** When emitting `validation:` tags, prefer a **one-line reason** in `decisions-log` when sibling slices use different validation enums (reduces `safety_unknown_gap` recycling).
- **Progress vs HR:** Template or `roadmap-Quality-Guide` could standardize the two fields for tertiary notes to avoid “metric theater” flags.
