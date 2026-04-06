---
created: 2026-04-08
pipeline: roadmap
project_id: sandbox-genesis-mythos-master
queue_entry_id: unknown-parent-run
ira_call_index: 1
status: repair_plan
risk_summary: { low: 5, medium: 0, high: 0 }
validator_primary_code: missing_roll_up_gates
---

# IRA — post–nested-validator (execution Phase 1)

## Context

Nested `roadmap_handoff_auto` (execution_v1) reported **`missing_roll_up_gates`**: `handoff_readiness: 72` on the execution Phase 1 note is below the execution handoff floor (default **85%**), and **GWT-1-Exec-A** cites **“This note § NL checklist”** while all three NL checklist items remain unchecked — evidence anchor mismatch. Secondary code **`safety_unknown_gap`**: open execution numbering policy (execution-local vs mirrored conceptual subphase indices).

## Structural discrepancies

1. **Roll-up / HR floor:** Frontmatter `handoff_readiness: 72` does not meet `execution_v1` minimum for delegatable handoff when treated as hard gate.
2. **GWT ↔ checklist:** GWT-1-Exec-A claims InstrumentationIntent mapping is evidenced by § NL checklist, but checklist boxes are empty — claim is ahead of artifact state.
3. **Policy ambiguity:** “Open questions” leaves Phase 1 numbering unset for machine-resolvable deepen targeting.

## Proposed fixes (for RoadmapSubagent to apply)

Apply in **stable order** (low-risk first). All targets stay under **`Roadmap/Execution/`** or **`decisions-log.md`** per scope; **no** edits to frozen conceptual phase bodies.

| # | risk | target | action |
|---|------|--------|--------|
| 1 | low | `Phase-1-Execution-Vertical-Slice-Instrumentation-Spine-Roadmap-2026-04-08-2145.md` | **Complete NL checklist** with real vault links: (a) three binding surfaces → link **6.1.1** (manifest/admission/registry), **6.1.2** (bounded tick / sim-visible matrix), **6.1.3** (ObservationChannel / readout / presentation) using canonical active-tree paths under `Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle/`; (b) one minimal vertical-slice happy path as 2–4 sentences in-place; (c) execution-deferred items with pointer to `[[distilled-core]]` deferral language. Check each box **only** when the line under it contains concrete prose + links. |
| 2 | low | Same note — frontmatter | After row 1, set **`handoff_readiness`** to a **defensible** value: **≥ 85** only if checklist + scope honestly support execution binding; if still intentionally skeletal, keep **&lt; 85** and use fix 5 instead of inflating. |
| 3 | low | Same note — GWT table | **Close GWT-1-Exec-A loop:** If checklist is completed with links, leave claim + Evidence “§ NL checklist”. If operator chooses **not** to complete checklist this run, **narrow** GWT-1-Exec-A Evidence to sections that already exist (e.g. “§ Scope + § Handoff from conceptual Phase 6”) and soften Claim to “skeleton maps to conceptual roll-up CDRs” until checklist is closed. |
| 4 | low | `1-Projects/sandbox-genesis-mythos-master/Roadmap/decisions-log.md` | Append **one bullet** under an execution-track heading (e.g. **## Execution track**): resolve numbering policy — **recommended:** “Phase 1 execution uses **execution-local** numbering; conceptual **6.1.x** indices appear **only** as cross-links (default until PMG/MOC alignment).” Resolves **`safety_unknown_gap`**. |
| 5 | low | Same decisions-log or Phase 1 note callout | **Only if** `handoff_readiness` must stay &lt; 85: record operator acknowledgement that this phase is **pre-delegation skeleton** and that the next RESUME will target checklist closure — **or** cite `params`/Config only if project adopts a documented sub-85 execution floor (avoid silent waiver). |

## Notes for future tuning

- Execution mints often score **HR** before checklists are filled; either **default GWT evidence** to Scope/Handoff until NL is done, or **mint with checklist rows pre-filled** as stubs (“TBD + link”) to avoid GWT drift.
- Consider a small **roadmap-deepen** template fragment for execution Phase 1 that **requires** three links before `handoff_readiness` ≥ 85 is allowed in automation.

## Patterns

- `missing_roll_up_gates` + unchecked NL checklist + GWT pointing at checklist → recurrent; fix by **evidence alignment** first.
