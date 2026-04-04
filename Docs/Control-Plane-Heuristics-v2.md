---
title: Control plane heuristics v2
created: 2026-03-29
tags: [second-brain, roadmap, queue, heuristics, dual-track]
para-type: Resource
status: active
links:
  - "[[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]]"
  - "[[3-Resources/Second-Brain/Parameters|Parameters]]"
  - "[[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]]"
  - "[[3-Resources/Second-Brain/Docs/Queue-Continuation-Spec|Queue-Continuation-Spec]]"
  - "[[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Spec|Validator-Tiered-Blocks-Spec]]"
---

# Control plane heuristics v2

Normative spec for **deterministic** control-plane behavior: iteration caps, dual-track gate resolution, phased scoring weights, nightly ledger, validator routing extensions, and structured observability. **LLM** supplies semantic content; **rules / agents / optional script** compute caps, scores, and routes from logs and Config.

**Safety:** Control plane **never** overrides [[3-Resources/Second-Brain/Subagent-Safety-Contract|Subagent-Safety-Contract]] / core guardrails: ≥85% destructive work, snapshots/backups, repair-first queue ordering, frozen conceptual write guards. Waivers apply **only** to **track-inappropriate progression artifacts** (e.g. pseudo-code requirements on conceptual slices).

---

## 1. Iteration semantics

**`iteration`:** One complete deepen–research cycle inside a **single** `Task(subagent_type=roadmap)` invocation: section selection → deepen → nested validators/IRA → final return. **Per-iteration / adaptive caps** are enforced at **RoadmapSubagent** (or skills it invokes), counting deepen cycles **within that Task**.

**`roadmap_task_dispatch`:** One Layer 1 dispatch that runs `Task(roadmap)` for a queue entry. **`queue.control_plane_v2.global_max_roadmap_task_dispatches_per_eat_queue_run`** (when set) caps dispatches **per EAT-QUEUE run** at Layer 1 only.

---

## 2. Structured observability (Roadmap return + Layer 1)

RoadmapSubagent **must** emit fenced YAML (or equivalent contract block) including when control plane v2 is active:

| Field | Required | Description |
|-------|----------|-------------|
| `control_plane_version` | yes | `"v2"` when this spec applies |
| `effective_cap_used` | yes | Integer cap applied this Task after adaptive formula; use `null` if adaptive cap disabled |
| `stagnation_severity` | yes | `none` \| `mild` \| `moderate` \| `chronic` |
| `stagnation_cluster_id` | yes | String hash/id or `null` |
| `routing_decision` | yes | Validator matrix outcome: `consume`, `repair_followup`, `block_destructive`, `prompt_craft`, `defer_to_next_eat`, or `not_applicable` |
| `effective_track` | yes | `conceptual` \| `execution` for this run |
| `gate_waived` | when applicable | Array, e.g. `["pseudo_code_requirement"]` |
| `waiver_reason` | when `gate_waived` non-empty | e.g. `conceptual_track` |
| `section_score_breakdown` | optional | Dict for debugging / replay |

Layer 1 merges these into **queue-continuation** rows and **`.technical/control-plane-nightly.jsonl`** when those artifacts are written.

---

## 3. Dual-track gate resolution

### 3.1 Track detection

1. **Run-level:** `effective_track` from `roadmap-state.md` `roadmap_track` with `params.roadmap_track` override per Queue-Sources.
2. **Per-subphase** (when `roadmap.control_plane_v2.dual_track_enforcement` is `per_subphase`): subphase note frontmatter **`track`**: `conceptual` \| `execution` \| `hybrid` — use for **artifact gates** on that slice; if absent, inherit `effective_track`.
3. **`hybrid`:** Default **conceptual** for pseudo-code waiver unless Config/spec documents execution milestone (e.g. explicit MOC marker).

### 3.2 Advance-phase ([[.cursor/skills/roadmap-advance-phase/SKILL|roadmap-advance-phase]])

| Track | Phases 5–6 gate |
|-------|------------------|
| **conceptual** | **handoff-audit(current_phase) ≥ 85%** — **no** depth-4 pseudo-code block requirement. |
| **execution** | **handoff-audit ≥ 85%** **and** at least one depth-4 note with pseudo-code under current phase (unchanged). |

Phases 1–4: unchanged (70% / coverage OR wrapper).

### 3.3 Deepen pre-create (depth ≥ 4)

| Track | Rule |
|-------|------|
| **execution** | Handoff/confidence pre-create gate before minting depth ≥4 children (e.g. parent &lt; 75% → Decision Wrapper). |
| **conceptual** | **No** execution-style pre-create block for pseudo-code depth; do **not** apply the same blocking wrapper **solely** for missing technical/pseudo-code readiness. Parent hard gates in §2.5 conflict rules still win. |

### 3.4 Validator routing (conceptual + missing pseudo-code)

When nested validator returns **`needs_work`** with **primary_code** (or reason cluster) indicating **missing pseudo-code / depth-4 artifact**, and **`effective_track === conceptual`**: **`routing_decision = consume`** with trace tag **`conceptual_track_compliant`** (tiered Success gate unchanged: `needs_work` without high/block may still allow Success). **Execution** track: keep **repair_followup** behavior for those codes.

See [[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Spec|Validator-Tiered-Blocks-Spec]] and `.cursor/rules/agents/queue.mdc` A.5b.

---

## 4. Adaptive per-subphase cap

```
effective_cap = floor(base_cap * (1 - H) * P * V)
effective_cap = clamp(effective_cap, min_cap, max_cap)
```

- `base_cap`, `min_cap`, `max_cap`, `H`, `P`, `V`: from Config `roadmap.control_plane_v2.adaptive_cap` (see Second-Brain-Config).
- **H:** circling history from Watcher-Result + continuation window.
- **P, V:** spine progress and confidence-velocity multipliers.

When adaptive cap is **disabled** (missing Config or `base_cap: 0`), agents omit or set `effective_cap_used: null`.

---

## 5. Phased section scoring

Eight components: `pri`, `unc`, `iter`, `stag`, `decay`, `bal`, `rb`, `cont` → linear `S = Σ w_i * term_i` with **`roadmap.control_plane_v2.scoring.phase_weights`**: rows **early** (spine &lt; 40%), **mid**, **late** (&gt; 70%).

**`track_compliance_bonus`:** On **conceptual** slices without depth-4 pseudo-code, add configured bonus so scoring does not penalize missing execution artifacts.

---

## 6. Stagnation v2

- **§77b** (roadmap-deepen): same-target window + flat Confidence → `stagnation_suspected`.
- **`stagnation_severity`:** `none` \| `mild` \| `moderate` \| `chronic` from Config thresholds + optional **primary_code cluster** repeat count over last M runs (`stagnation_v2` block).
- Emit `stagnation_cluster_id` when cluster logic runs; else `null`.

---

## 7. Nightly ledger

**Path:** `.technical/control-plane-nightly.jsonl` (append-only).

**Line schema (minimum):** `schema_version`, `control_plane_version`, `completed_iso`, `eat_queue_run_id`, `queue_entry_id`, `project_id`, `disposition`, `final_subphase_key`, `blocked_subphases` (array), `effective_cap_used`, `stagnation_severity`, `stagnation_cluster_id`, `routing_decision`, `effective_track`, optional `gate_waived`, `waiver_reason`, `remaining_repair_budget`, `notes_machine`.

**Fallback:** If read fails or `nightly_ledger.enabled: false`, Layer 1 uses **workflow_state Log tail + Watcher-Result tail** for **de-prioritization hints only** (non-blocking). Set `layer1_control_plane.ledger_fallback: true` on hand-off.

---

## 8. Optional Python engine

**Path:** `.technical/scripts/heuristic_engine.py` — reads JSON stdin with **`adaptive_cap_config`** (from **`roadmap.control_plane_v2.adaptive_cap`**) and optional **`tail_hints`** (`circling_score`, `progress_mult`, `velocity_mult`); prints JSON with **`effective_cap_used`**, **`H`**, **`P`**, **`V`**. Used when **`queue.control_plane_v2.use_python_engine: true`**; **inline** computation remains valid when the script is absent or fails.

---

## 9. References

- [[3-Resources/Second-Brain-Config|Second-Brain-Config]] — `roadmap.control_plane_v2`, `queue.control_plane_v2`
- `.cursor/skills/roadmap-deepen/SKILL.md` — §77b, §2.5, pre-create gate
- `.cursor/skills/roadmap-advance-phase/SKILL.md` — advance gates
- `.cursor/agents/roadmap.md` — return payload, smart dispatch
