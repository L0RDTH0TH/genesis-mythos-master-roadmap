---
name: Heuristic Control Plane v2
overview: v2 control plane + dual-track gate resolution — execution keeps pseudo-code/depth-4 gates; conceptual uses NL/handoff/confidence only; waivers observable; phased scoring, ledger, routing matrix, iteration defs; Safety-Invariants unchanged.
todos:
  - id: spec-v2-doc
    content: Control-Plane-Heuristics-v2.md — iteration defs, dual-track gates, weight schedule, ledger, observability + waivers
    status: completed
  - id: dual-track-gates
    content: roadmap-advance-phase + Parameters + deepen pre-create — branch gates by effective_track / per-subphase tag
    status: completed
  - id: nightly-ledger
    content: control-plane-nightly.jsonl + fallback; merge gate_waived into rows
    status: completed
  - id: adaptive-caps-config
    content: adaptive_cap; enforce at RoadmapSubagent; global Task cap at L1
    status: completed
  - id: scoring-config
    content: phase_weights + track_compliance_bonus (conceptual without pseudo-code)
    status: completed
  - id: stagnation-v2
    content: §77b + stagnation_severity + cluster; observability fields on return
    status: completed
  - id: queue-l1-ledger
    content: queue.mdc — ledger, fallback, continuation merge, dual-track routing row
    status: completed
  - id: validator-matrix
    content: Tiered-Blocks + A.5b — missing_pseudo_code + conceptual → consume
    status: completed
  - id: optional-python
    content: Inline v2 first; heuristic_engine.py + parity after
    status: completed
  - id: backbone-sync
    content: Parameters, Dual-Roadmap-Track cross-links, sync, changelog
    status: completed
isProject: false
---

# Control plane heuristics — v2 implementation draft

## Position vs v1

v1: hard caps, wire `stagnation_suspected`, global EAT-QUEUE budget, static weighted score, static if-then validator routing.

**v2** adds: adaptive caps, phased scoring, predictive stagnation, mandatory nightly ledger + fallback, risk-aware routing, explicit **iteration** semantics, structured observability — plus **dual-track gate resolution** so conceptual work is not blocked by execution-only artifact rules.

All control-plane outputs remain **recomputable from logs**. **Safety-Invariants** (85% destructive, snapshots, repair-first, frozen conceptual) stay **out of scope for waiver**; waivers apply only to **track-inappropriate progression artifacts** (see §13).

---

## Problem folded in: dual-track gate mismatch (root cause)

**Symptom:** Same subphase (e.g. 4.1.5) circles; confidence plateaus (~93%); stagnation and repair loops repeat; overnight queue stalls.

**Mechanism (as diagnosed):** [roadmap-advance-phase](.cursor/skills/roadmap-advance-phase/SKILL.md) and related **phase-complete / target-reached / handoff-readiness** paths require **depth-4 pseudo-code** for phases 5–6 (and execution-style checks elsewhere). That is appropriate on the **execution** track. On the **conceptual** track, pseudo-code is often **not required** per [Dual-Roadmap-Track](3-Resources/Second-Brain/Docs/Dual-Roadmap-Track.md) / Parameters — but **late-phase and validator “needs_work” paths** can still behave as if every subphase must satisfy execution artifacts. The model may withhold top-band confidence when it “knows” a structural requirement is unmet → mid/high band churn → `stagnation_suspected` → more repairs without clearing the real blocker.

**Fix locus:** Not a prompt-only tweak — fold **deterministic track-aware gate resolution** into the control plane + **roadmap-advance-phase** + **validator routing** + **structured returns** so conceptual progression does not depend on pseudo-code.

---

## 1. Definitions and data sources

### 1.0 Iteration semantics (normative)

`**iteration` (per-subphase / deepen budget):** One complete deepen–research cycle inside a **single** `Task(subagent_type=roadmap)` invocation: section selection → LLM deepen → nested validators/IRA → final return. Enforce adaptive/effective caps at **RoadmapSubagent**.

`**roadmap_task_dispatch` (global budget):** One Layer 1 `Task(roadmap)` dispatch. Global cap counted **only at Layer 1**.

### 1.1 Data sources


| Source                                                                | Use                              |
| --------------------------------------------------------------------- | -------------------------------- |
| [Watcher-Result](3-Resources/Watcher-Result.md)                       | Circling hints, streaks          |
| [queue-continuation.jsonl](.technical/queue-continuation.jsonl)       | Merge observability + waivers    |
| `workflow_state.md` / execution mirror                                | Log tail, fallback blocked hints |
| [Run-Telemetry](.technical/Run-Telemetry/)                            | Optional `primary_code` cluster  |
| [control-plane-nightly.jsonl](.technical/control-plane-nightly.jsonl) | Inter-task `blocked_subphases`   |
| `roadmap-state.md` (and execution copy)                               | `roadmap_track`, phase, MOC      |
| Subphase note frontmatter                                             | Optional `track: conceptual      |
| [Second-Brain-Config](3-Resources/Second-Brain-Config.md)             | `control_plane_v2`, `roadmap.*`  |


### 1.2 Mandatory observability (structured returns)

RoadmapSubagent return YAML **must** include:


| Field                     | Required                     | Notes                                     |
| ------------------------- | ---------------------------- | ----------------------------------------- |
| `control_plane_version`   | yes                          | e.g. `"v2"`                               |
| `effective_cap_used`      | yes                          | after adaptive formula                    |
| `stagnation_severity`     | yes                          | `none`                                    |
| `stagnation_cluster_id`   | yes                          | string or `null`                          |
| `routing_decision`        | yes                          | matrix outcome                            |
| `effective_track`         | yes                          | `conceptual`                              |
| `gate_waived`             | when applicable              | array, e.g. `["pseudo_code_requirement"]` |
| `waiver_reason`           | when `gate_waived` non-empty | e.g. `conceptual_track`                   |
| `section_score_breakdown` | optional                     | debug / replay                            |


Layer 1 copies these into continuation JSONL and nightly ledger when present.

### 1.3 Safety boundary

Control plane influences **section selection**, **caps**, **validator routing**, **progression artifact requirements per track**. It **must not** override: <85% destructive bar, snapshots/backups, repair-first ordering, frozen conceptual **write** guards.

---

## 2. Adaptive per-subphase caps

(Unchanged from prior draft.)

- `effective_cap = floor(base_cap * (1 - H) * P * V)` clamped to `[min_cap, max_cap]`.
- Enforce **per iteration** at RoadmapSubagent; **global** roadmap Task cap at Layer 1.

---

## 3. Multi-factor scoring (phased weights + track compliance)

### 3.1 Components (eight)

Same eight terms as before: `pri`, `unc`, `iter`, `stag`, `decay`, `bal`, `rb`, `cont` → linear `S` with phase-dependent `w1`…`w7`.

### 3.2 Phased weight schedule

Early (<40% spine): heavy `unc` + `pri*decay`. Mid: `iter` + `stag`. Late (>70%): `bal` + `cont`. Config: `roadmap.control_plane_v2.scoring.phase_weights`.

### 3.3 `track_compliance_bonus` (dual-track)

- If **effective subphase track** is **conceptual** (§9) and **no** depth-4 pseudo-code block is present on the slice: add configurable `**track_compliance_bonus`** (e.g. **+0.3** on a normalized 0–1 scale, or fold as extra term `w8*track_bonus`) so scoring does not keep re-selecting a slice “punished” for missing execution-only artifacts.
- If **execution**: bonus **0** (execution slices still compete on real artifact progress).

---

## 4. Predictive stagnation

§77b + cluster `primary_code` → `stagnation_severity`; escalation table unchanged.

---

## 5. Nightly ledger

Mandatory when enabled; fallback to workflow_state + Watcher tail; **merge `gate_waived` / `waiver_reason` / `effective_track`** into ledger lines for downstream tasks.

---

## 6. Risk-aware validator routing (matrix) — dual-track extension

**Base inputs:** `repair_budget_remaining`, `confidence_trend`, `is_last`.

**Dual-track row (insert after severity / block rules, before generic `needs_work`):**

- If `**needs_work`** AND **primary_code** (or reason cluster) ∈ **missing pseudo-code / depth-4 artifact** family **AND** `**effective_track === conceptual`** (from hand-off or subphase tag): `**route = consume`** with machine tag `**conceptual_track_compliant`** in trace (tiered blocks still allow Success when little_val ok per existing contract). Do **not** force **repair_followup** solely for missing pseudo-code on conceptual.
- If `**execution`**: keep existing **repair_followup** behavior for those codes.

Document full ordering in [Validator-Tiered-Blocks-Spec](3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Spec.md) + [queue.mdc](.cursor/rules/agents/queue.mdc) A.5b.

---

## 7. Python helper

Inline first; optional `heuristic_engine.py` + parity; include dual-track branch in same logic.

---

## 8. Config keys (draft)

`roadmap.control_plane_v2` (existing blocks) **plus:**

- `dual_track_enforcement`: `strict`  `lenient`  `per_subphase` (default **per_subphase**)
- `conceptual_pseudo_code_optional`: bool (default **true** for conceptual track progression; log warning if operator sets **false**)
- `scoring.track_compliance_bonus`: float (default e.g. 0.3 on normalized scale, or document as `w8`)

**Naming note:** `conceptual_pseudo_code_optional: true` means “conceptual slices are **not** blocked for advancement/target by absence of pseudo-code,” not “skip validators entirely.”

---

## 9. Dual-track gate resolution (normative)

### 9.1 Track detection (deterministic)

1. **Run-level:** Read `roadmap-state.md` `roadmap_track` + `params.roadmap_track` override (existing Queue-Sources resolution).
2. **Subphase-level (when `dual_track_enforcement: per_subphase`):** If subphase note has frontmatter `**track`**: `conceptual`  `execution`  `hybrid` — use it for **gate** selection on that slice. If absent, inherit **effective_track** for the run.
3. `**hybrid`:** Use config table: default treat as **conceptual** for pseudo-code waiver unless section heading/MOC marks execution milestone (document explicit rule in spec — e.g. hybrid + phase ≥5 → execution artifacts required).

### 9.2 Gate sets


| Track                   | Phase advance (5–6) / pseudo-code                                                                                                                                                                            | Handoff / confidence                                                         |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------- |
| **Conceptual**          | **No** depth-4 pseudo-code requirement for advance, slice exit, or conceptual target reached; use NL completeness, checklists, **handoff-audit ≥85%**, conceptual subphase exit + stagnation per Parameters. | Same bands as today; no execution-artifact inflation.                        |
| **Execution**           | Keep **roadmap-advance-phase**: phases 5–6 need **≥85%** + depth-4 pseudo-code block.                                                                                                                        | Unchanged.                                                                   |
| **Pre-create (deepen)** | **Execution** only: handoff/confidence gate before depth ≥4 children. **Conceptual:** no execution-only pseudo-code pre-create rule.                                                                         | Parent <75% and other hard gates still win over caps (existing deepen rule). |


### 13.3 Structured waiver

When a gate is skipped or downgraded because of track:

- Set `**gate_waived: ["pseudo_code_requirement"]`** (or enumerated list).
- Set `**waiver_reason: conceptual_track`** (or `per_subphase_tag`).
- Log to Watcher-Result / ledger so the **next** queue entry does not re-escalate “missing pseudo-code” for that slice.

### 13.4 Files to align

- [roadmap-advance-phase/SKILL.md](.cursor/skills/roadmap-advance-phase/SKILL.md) — branch step 4 on **effective_track** / phase tree root (conceptual vs execution).
- [roadmap-deepen/SKILL.md](.cursor/skills/roadmap-deepen/SKILL.md) — pre-create gate text: execution-only.
- [Parameters.md](3-Resources/Second-Brain/Parameters.md) — cross-link “conceptual target / advance does not require pseudo-code.”
- [Dual-Roadmap-Track](3-Resources/Second-Brain/Docs/Dual-Roadmap-Track.md) — one paragraph pointer to control-plane §13.
- [agents/roadmap.md](.cursor/agents/roadmap.md) / [roadmap.mdc](.cursor/rules/agents/roadmap.mdc) — return YAML includes §1.2 + waivers; smart dispatch respects track for validator follow-ups.

---

## 9. Implementation order

1. **Spec** — `Control-Plane-Heuristics-v2.md`: §1.0, §1.2, §5 fallback, **§13 dual-track**.
2. **Dual-track gates** — advance-phase + deepen pre-create + Parameters/Dual-Roadmap doc (stops false circling fastest).
3. **Validator matrix row** — conceptual + missing_pseudo → consume.
4. **Ledger** — store `gate_waived`, `effective_track`.
5. **Scoring** — `track_compliance_bonus`.
6. **Caps / stagnation / Python** — as before.

---

## 11. Success criteria (v2)

- Conceptual phases 5–6 can **advance** / exit slice **without** pseudo-code when NL + handoff + confidence criteria met.
- Validator `**needs_work`** for missing pseudo-code on conceptual does not **by itself** trigger endless repair loops (`routing_decision` = consume with tag).
- Ledger + continuation show `**gate_waived`** for audit.
- Execution track behavior **unchanged** for artifact requirements.

---

## 11. Non-goals

- ML / embedding learning.
- Auto-unfreeze conceptual frozen notes.
- Replacing full ROADMAP_HANDOFF_VALIDATE narrative.
- **Safety-Invariants** — no waiver of 85% destructive, snapshots, repair-first, or frozen-note **destruction** rules.
- **Waivers apply only** to **progression artifact mismatches** where **track** explicitly does not require those artifacts.

---

## 12. Files to touch (execution checklist)


| File                                                            | Change                                      |
| --------------------------------------------------------------- | ------------------------------------------- |
| `3-Resources/Second-Brain/Docs/Control-Plane-Heuristics-v2.md`  | New — full normative spec including §13     |
| `3-Resources/Second-Brain/Docs/Dual-Roadmap-Track.md`           | Pointer to control-plane §13                |
| `3-Resources/Second-Brain/Queue-Sources.md`                     | Hand-off fields, `effective_track`, waivers |
| `3-Resources/Second-Brain-Config.md`                            | `control_plane_v2` + dual_track keys        |
| `3-Resources/Second-Brain/Parameters.md`                        | Conceptual vs execution gate summary        |
| `.cursor/skills/roadmap-advance-phase/SKILL.md`                 | Branch gates by track                       |
| `.cursor/skills/roadmap-deepen/SKILL.md`                        | Pre-create execution-only; §77b             |
| `.cursor/rules/agents/roadmap.mdc` + `agents/roadmap.md`        | Returns, dispatch                           |
| `3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Spec.md` | Dual-track matrix row                       |
| `.cursor/rules/agents/queue.mdc` + `agents/queue.md`            | Ledger, continuation                        |
| `3-Resources/Second-Brain/Docs/Queue-Continuation-Spec.md`      | Optional schema fields                      |
| `.technical/scripts/heuristic_engine.py`                        | After inline, include track branch          |
| `.cursor/sync/` + `changelog.md`                                | Backbone sync                               |


---

*Reduced profile: disable adaptive factors; ledger off + fallback only; **dual_track_enforcement: strict** reverts to legacy unified gates only if explicitly chosen (not default).*