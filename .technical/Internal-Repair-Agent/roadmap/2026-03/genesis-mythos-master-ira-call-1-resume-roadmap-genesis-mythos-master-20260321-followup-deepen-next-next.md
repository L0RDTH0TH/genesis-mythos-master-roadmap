---
created: 2026-03-21
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-roadmap-genesis-mythos-master-20260321-followup-deepen-next-next
ira_call_index: 1
parent_run_id: eatq-20260321-gmm-deepen-2245
status: repair_plan
risk_summary: { low: 2, medium: 3, high: 1 }
validator_report: .technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260321T224530Z.md
primary_code: contradictions_detected
---

# IRA — roadmap — genesis-mythos-master — call 1

## Context

Post-first nested `roadmap_handoff_auto` pass returned **high** / **block_destructive** with **primary_code `contradictions_detected`** plus **`safety_unknown_gap`**. The validator correctly flags that **2.3.1** and **2.3.2** teach incompatible stories for **`AlignmentFn_v0` / EMG-2**: 2.3.1 shows a scalar-returning `AlignmentFn_v0(lore, sim)` with "0..100; floor F is TBD", while 2.3.2 defines `AlignmentFn_v0(...) -> AlignmentOutcome` with `INVALID_EMG2_SLICE` / `BELOW_FLOOR` and frozen RFC 6901 pointers. **`distilled-core.md`** still states Phase 2.3 field bindings are "TBD in 2.3.x tertiaries," which contradicts 2.3.2's normative freeze. The **expected MOC path under `Roadmap/`** does not exist; the live MOC is at project root. Registry **CI row** closure remains explicitly deferred in 2.3.2 `handoff_gaps`—that is **not** a signature fix but must stay **not** misread as "green for implementation."

## Structural discrepancies

1. **API / contract collision (hard block):** `phase-2-3-1-...-2205.md` pseudo-code `EMG2_LoreSimAlignmentScore` → `AlignmentFn_v0(lore, sim)` vs `phase-2-3-2-...-2245.md` `AlignmentFn_v0(lore_json, sim_json, pointers, tier) -> AlignmentOutcome`.
2. **Distilled core drift:** `distilled-core.md` `core_decisions` Phase 2.3 bullet still says bindings **TBD** while 2.3.2 documents frozen pointers + provisional **F**.
3. **Hub path mismatch:** validators / hand-offs expecting `Roadmap/genesis-mythos-master-roadmap-moc.md` get a false "missing MOC"; canonical file is `1-Projects/genesis-mythos-master/genesis-mythos-master-roadmap-moc.md`.
4. **Safety gap (informational):** EMG-2 **golden-registry row** and **`emg2_floor_F_status: frozen`** remain future work per D-023/D-024 promotion—do not conflate with clearing **contradictions_detected**.

## Proposed fixes (for parent application)

Apply in **risk order** (low → medium → high) unless a gate blocks a specific step.

| Risk | Target | Action |
|------|--------|--------|
| low | `distilled-core.md` | Update Phase 2.3 bullet in frontmatter + body: frozen RFC 6901 paths + `AlignmentOutcome` contract + provisional **F** per 2.3.2; link `[[phase-2-3-2-emg-2-floor-frozen-json-pointers-and-alignmentfn-v0-roadmap-2026-03-21-2245]]`; remove "TBD" phrasing that contradicts 2.3.2. |
| low | `phase-2-3-1-...-2205.md` | In `EMG2_LoreSimAlignmentScore` block: **remove** normative `AlignmentFn_v0(lore, sim)` sketch; replace with a **forward reference** to 2.3.2 as the **only** normative `AlignmentFn_v0` + `AlignmentOutcome` definition; keep 2.3.1 focused on matrix shape / PBT alphabet / EMG-1/3. |
| medium | `phase-2-3-1-...-2205.md` | Add one short "superseded by 2.3.2" callout near EMG-2 pseudo-code if any illustrative snippet remains, so readers cannot execute a second contract. |
| medium | `1-Projects/genesis-mythos-master/Roadmap/genesis-mythos-master-roadmap-moc.md` | **Create** a thin hub note at the validator-expected path whose **only** job is to link to the canonical MOC at `[[../genesis-mythos-master-roadmap-moc]]` or full path—satisfies automation without moving the canonical file. Snapshot before write per guardrails. |
| medium | `decisions-log.md` (optional cross-check) | Ensure D-023/D-024 rows explicitly say **2.3.2** owns `AlignmentFn_v0` normative text and 2.3.1 is **binding draft / matrix** only—reduces reintroduction of duplicate API. |
| high | `phase-2-2-3-ci-golden-registry-...-1205.md` | **Only if** claiming CI/registry closure: add EMG-2 row + fixture IDs in VCS + promote `emg2_floor_F_status` per checklist; **otherwise** leave deferred and keep **block_destructive** for "CI-ready EMG-2" claims only—**not** required to clear **signature** contradiction if scopes stay honest. |

## Notes for future tuning

- **Tertiary sequencing:** When 2.3.2 deepens a function introduced in 2.3.1, **template** 2.3.1 to stub or link-only for that function on the same run.
- **Little-val / hand-off paths:** Add canonical MOC path to **project** conventions or emit **both** paths in checklist so "missing MOC under Roadmap/" false negatives stop recurring.
- **Validator agreeability:** Treat `handoff_readiness` at threshold as **narrow** when `handoff_gaps` still cite registry/CI.
