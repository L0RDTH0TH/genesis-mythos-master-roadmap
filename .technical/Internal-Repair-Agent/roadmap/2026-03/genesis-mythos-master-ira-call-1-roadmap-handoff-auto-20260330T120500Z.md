---
created: 2026-03-30
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: roadmap-handoff-auto-genesis-mythos-master-20260330T120500Z
ira_call_index: 1
status: repair_plan
risk_summary: { low: 3, medium: 1, high: 0 }
validator_report: .technical/Validator/roadmap-handoff-auto-genesis-mythos-master-20260330T120500Z-conceptual-v1-phase33.md
---

# IRA — genesis-mythos-master (validator-driven, conceptual track)

## Context

Invocation follows nested **`roadmap_handoff_auto`** with **`effective_track: conceptual`**, **`primary_code: safety_unknown_gap`**, secondary **`missing_roll_up_gates`**. The validator report treats cross-artifact coherence as intact for Phase 3.3 rollup; **`needs_work` / medium** is driven primarily by **two NL open questions** on the Phase **3.3** secondary note that are not yet sealed as **D-*** decisions, **accepted deferrals** with scope bounds, or **CDR-linked** resolutions. **`missing_roll_up_gates`** is explicitly **execution-advisory** on conceptual_v1 (`GMM-2.4.5-*` reference-only); it **must not** be repaired by demanding execution rollup / registry / CI closure.

## Structural discrepancies

1. **safety_unknown_gap:** `## Open questions` on the Phase **3.3** secondary note lists two items without explicit **decision ids** in [[decisions-log]] or bounded deferral language with operator pick.
2. **missing_roll_up_gates (conceptual):** Advisory only — not a conceptual completion bar. Any “fix” must **reinforce dual-track waiver**, not introduce execution-closure obligations.
3. **Tooling (informational):** Validator notes queue/hand-off paths that omit `Phase-3-Living-Simulation-and-Dynamic-Agency/` are incorrect for tooling — **IRA does not target queue files**; operators should fix hand-off templates separately.

## Proposed fixes (roadmap tree only)

Apply in order **low → medium** when gates pass. **Do not** treat **`missing_roll_up_gates`** as requiring execution artifact closure on conceptual.

| # | risk | target | action |
|---|------|--------|--------|
| 1 | low | `1-Projects/genesis-mythos-master/Roadmap/decisions-log.md` | Append structured entries (existing **Decisions** / **Conceptual autopilot** style) assigning **D-3.3.*** ids for: (a) minimum **consequence granularity** (NPC vs faction vs region) before execution prototypes; (b) **vitality** determinism vs **operator bias** knobs with replay bounds — **or** explicit **accepted conceptual deferral** rows with scope ceiling and link from Phase 3.3. |
| 2 | medium | `1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-3-Vitality-Consequence-and-Persistence-Cohesion/Phase-3-3-Vitality-Consequence-and-Persistence-Cohesion-Roadmap-2026-04-03-0005.md` | After decisions exist: edit **`## Open questions`** — either **remove** resolved bullets and point to **D-*** ids / CDRs, or **retitle** to **Accepted deferrals (conceptual)** with one line each binding scope (matches validator `next_artifacts` “definition_of_done”). Per-change snapshot before structural body edit. |
| 3 | low | `1-Projects/genesis-mythos-master/Roadmap/Conceptual-Decision-Records/` (new note) | Optional: atomized **CDR** per deepen pattern (`parent_roadmap_note`, `amends_section`) for each resolved question if you prefer CDR over inline-only closure. |
| 4 | low | Same Phase **3.3** secondary note (callout / Scope) | **Dual-track only:** add or tighten a short explicit line that **execution rollup / registry / CI / `GMM-2.4.5-*` proof closure** remains **out of conceptual completion criteria** (echoes [[distilled-core]] waiver); **does not** satisfy validator by “closing” execution gates — only documents conceptual waiver for handoff readers. |

## Notes for future tuning

- Recurring **`safety_unknown_gap`** when **Open questions** stay pure NL at secondary rollup depth — enforce **D-*** or **deferral** pattern before claiming rollup-complete in automation.
- Keep **`missing_roll_up_gates`** tiered routing: on **`effective_track: conceptual`**, pipeline should not escalate to **block_destructive** for execution-style closure debt.
