---
created: 2026-03-30
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-gmm-deepen-115-20260330T143100Z
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 3
  medium: 1
  high: 0
validator_report: .technical/Validator/roadmap-handoff-auto-genesis-mythos-master-20260330T150500Z-conceptual-v1.md
ira_after_first_pass: true
---

# IRA — genesis-mythos-master (RESUME_ROADMAP deepen, post-validator)

## Context

Validator-driven IRA after first `roadmap_handoff_auto` pass (`severity: medium`, `recommended_action: needs_work`, `primary_code: missing_roll_up_gates`, `reason_codes`: `missing_roll_up_gates`, `safety_unknown_gap`). State files (`workflow_state.md`, `roadmap-state.md`) align on cursor **1.2** after minting tertiary **1.1.5**. The structural failure mode is **canonical rollup debt**: `distilled-core.md` still reflects only high-level Phase 1, not the closed **1.1.1–1.1.5** layering slice. Secondary gap: **research unbound** and **non-cosmetic open questions** on 1.1.5 map to `safety_unknown_gap`; traceability can be closed on conceptual track via **decisions-log operator pick** (pattern-only affirmation) without rewriting the tertiary body.

## Structural discrepancies

1. **missing_roll_up_gates**: `distilled-core.md` “Core decisions” cites Phase 1 primary only; no paragraph + links summarizing tertiary **1.1.1–1.1.5**, observability correlation / test-seam boundaries, or **slice-complete** meaning before **1.2**.
2. **safety_unknown_gap**: Phase 1.1.5 documents pattern-only alignment and open questions (replay depth, MVP vs full observability). `decisions-log.md` has CDR + deepen bullets for 1.1.5 but **no** grep-stable **Operator pick logged** line for **1.1.5** pattern-only acceptance (contrast **1.1.2** operator pick at 2026-03-30), so validator “pattern-only or bind research” closure is **incomplete** vs [[3-Resources/Second-Brain/Docs/Decisions-Log-Operator-Pick-Convention|Decisions-Log-Operator-Pick-Convention]].
3. **Supporting**: `handoff_readiness: 75` on 1.1.5 is at conceptual floor; advisory only on `conceptual_v1` — do not fake frontmatter bumps without operator intent.

## Proposed fixes (apply order: low risk first)

| # | description | action_type | target_path | risk_level | constraints |
|---|-------------|-------------|-------------|------------|-------------|
| 1 | Append a **Phase 1.1 layering slice (1.1.1–1.1.5)** subsection to `distilled-core.md`: one short paragraph + wiki-links to each tertiary roadmap note under `Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/`; state **observability correlation id** surface, **test seam** boundary (what is asserted where), and that **slice-complete** for 1.1 means cursor advanced to **1.2** (procedural generation graph next). | `markdown_append` | `1-Projects/genesis-mythos-master/Roadmap/distilled-core.md` | low | After `obsidian_ensure_backup` + per-change snapshot on `distilled-core.md` per roadmap MCP rules; append-only; optionally add one line to `core_decisions` frontmatter **only if** it mirrors the new paragraph without contradicting Phase 1 primary. |
| 2 | Under `decisions-log.md` **## Conceptual autopilot**, add **Operator pick logged (2026-03-30):** Phase **1.1.5** — **pattern-only conceptual grounding accepted** for this tertiary slice; closes advisory `safety_unknown_gap` traceability for `queue_entry_id` `resume-gmm-deepen-115-20260330T143100Z` (see `.technical/Validator/roadmap-handoff-auto-genesis-mythos-master-20260330T150500Z-conceptual-v1.md`). | `write_log_entry` | `1-Projects/genesis-mythos-master/Roadmap/decisions-log.md` | low | Single new bullet after existing 1.1.5 lines; do not delete or rewrite prior operator picks. |
| 3 | (Optional) Append a one-line **rollup cross-ref** in `roadmap-state.md` **## Notes** pointing to the new `distilled-core` Phase 1.1 section — **only if** narrative parity with phase summaries is desired. | `markdown_append` | `1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md` | low | Snapshot `roadmap-state.md` before/after per roadmap invariants; skip if team prefers rollup only in distilled-core. |
| 4 | (Optional) Raise **handoff_readiness** above 75 on `Phase-1-1-5-...1431.md`: either run **hand-off-audit** and apply substantive NL edits **or** add a **Conceptual-Amendments** companion with operator deferral for the two open questions — **not** a numeric bump alone. | `recompute_phase_metadata` / `adjust_frontmatter` | `1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-5-Cross-Layer-Observability-Test-Seams-and-Slice-Handoff-Roadmap-2026-03-30-1431.md` | medium | Prefer amendment path if conceptual notes are frozen; avoid cosmetic `handoff_readiness` inflation. |

## Notes for future tuning

- **Rollup drift**: After each closed subphase slice, **roadmap-deepen** or a post-step hook should append/update a **distilled-core** slice rollup to prevent `missing_roll_up_gates` on the next handoff validator.
- **Operator pick parity**: When `validation: pattern_only` is logged for a tertiary, mirror the **1.1.2-style** operator pick line so `safety_unknown_gap` has grep-stable closure without mandatory `Ingest/Agent-Research/` binding.
