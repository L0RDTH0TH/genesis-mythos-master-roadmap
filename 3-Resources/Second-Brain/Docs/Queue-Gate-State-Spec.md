---
title: Queue gate state (durable anti-spin memory)
created: 2026-03-24
tags: [second-brain, queue, roadmap, anti-spin]
para-type: Resource
status: active
links:
  - "[[3-Resources/Second-Brain/Queue-Sources]]"
  - "[[3-Resources/Second-Brain-Config]]"
  - "[[3-Resources/Second-Brain/Docs/Queue-Continuation-Spec|Queue-Continuation-Spec]]"
  - "[[.cursor/rules/agents/queue.mdc|agents/queue.mdc]]"
---

# Queue gate state spec

## Purpose

Layer 1 anti-spin rules in [[.cursor/rules/agents/queue.mdc|queue.mdc]] require **durable** memory of repeated post–little-val **hard blocks** per `(project_id, gate_signature)` so `gate_streak` survives across EAT-QUEUE runs and inconsistent LLM execution. This spec defines the machine file **`.technical/queue-gate-state.json`** (path override: `queue.gate_state_path` in [[3-Resources/Second-Brain-Config|Second-Brain-Config]]).

**Single writer (recommended):** [[scripts/queue-gate-compute.py|queue-gate-compute.py]] with `--record-outcome` updates this file. Layer 1 **must** invoke that mode after each fully dispositioned RESUME_ROADMAP roadmap dispatch (same moment as A.5e continuation append) when deterministic gate tooling is enabled, **or** apply the **same numeric rules** in prose when the script is disabled (avoid double-increment).

## File format

- **Path:** default `.technical/queue-gate-state.json` under vault root.
- **Encoding:** UTF-8 JSON object.

| Field | Type | Description |
|-------|------|-------------|
| `version` | int | Schema version; use `1`. |
| `entries` | object | Keys = `gate_key` (see below). Values = per-gate records. |

### `gate_key`

String, schema **v2** (when Config **`queue.gate_key_includes_track`** is **true**, default **true**):  
`<project_id>|<effective_track>|<gate_signature>` where **`effective_track`** is `conceptual` or `execution` per [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]] § **`effective_track` resolution**.

Legacy **v1** key (when track dimension disabled): `<project_id>|<gate_signature>`.

- `project_id` — slug, e.g. `genesis-mythos-master`.
- `effective_track` — avoids colliding conceptual vs execution streaks for the same signature.
- `gate_signature` — normalized token from the strongest available evidence, **aligned with queue.mdc** gate_signature precedence: validator `primary_code` when present; else first significant token from `post_little_val_summary` / `suppress_reason` (e.g. `post_little_val_hard_block_consumed` maps to co-occurring `primary_code` when Layer 1 has it); use `unknown` only when no code available.

### Per-entry record

| Field | Type | Description |
|-------|------|-------------|
| `gate_streak` | int | Consecutive hard-block-weighted events (see update rules). |
| `last_queue_entry_id` | string | Last dispatch that affected this key. |
| `last_completed_iso` | string | ISO 8601 UTC. |
| `blocked_track` | string | `conceptual` or `execution` — track in effect when the streak last incremented. |
| `pivot_to_track` | string | Opposite of `blocked_track` when `prefer_track_shift_on_gate_block` is true. |
| `cooldown_remaining` | int | Optional; runs until streak decay after a non-hard-block success. |

## Update rules (must match queue.mdc)

1. **Hard block** (post–little-val tiered hard block for RESUME_ROADMAP, per queue.mdc A.5b): **increment** `gate_streak` for the composite **`gate_key`** (includes **`effective_track`** when **`queue.gate_key_includes_track`** is true); set **`blocked_track`** to **`effective_track`** for that dispatch (see Queue-Sources § **`effective_track` resolution`), not merely absent-queue default; set `pivot_to_track` to the other track when Config `queue.prefer_track_shift_on_gate_block` is true.
2. **Non-hard-block** roadmap completion for that project: **decay** streak for all keys of that `project_id` per `queue.gate_block_same_track_cooldown_runs` (subtract 1 from streak, floor at 0, or reset key when streak hits 0 — implementation in script).
3. **Threshold:** When `gate_streak >= queue.gate_block_streak_threshold` and `queue.gate_block_detection_enabled`, resolver treats `need_class: gate_block` and A.5c must pivot same-track `deepen`/`recal` follow-ups when not user-locked.

## Cross-references

- Script: `scripts/queue-gate-compute.py` — `report`, `validate-line`, `record-outcome`.
- Continuation log: additive fields in [[3-Resources/Second-Brain/Docs/Queue-Continuation-Spec|Queue-Continuation-Spec]] (`gate_block_signal`, etc.).
