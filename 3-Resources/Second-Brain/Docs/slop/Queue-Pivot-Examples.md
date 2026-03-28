---
title: Queue pivot examples (tiered validator / repair-first)
created: 2026-03-20
tags: [second-brain, queue, validator, repair-first]
para-type: Resource
status: active
links:
  - "[[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Spec|Validator-Tiered-Blocks-Spec]]"
  - "[[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]]"
  - "[[3-Resources/Second-Brain/Tests-Validator|Tests-Validator]]"
---

# Queue pivot examples (tiered validator / repair-first)

Short **regression-oriented** examples for Layer 1 behavior after **post–little-val** hard blocks. Canonical field definitions and A.7 policy: [[3-Resources/Second-Brain/Queue-Sources#Tiered validator queue fields (Layer 1)|Queue-Sources § Tiered validator queue fields]].

## Repair-first vs orthogonal “continue”

| Situation | Queue behavior |
|-----------|----------------|
| Same **`project_id`**, multiple `RESUME_ROADMAP` lines (one **repair** flagged, one **deepen**) | **Repair first** — sub-sort in `queue.mdc` **A.4** runs repair (`queue_priority: "repair"` or `validator_repair_followup: true`) **before** deepen for that project in the **same** EAT-QUEUE pass. |
| **Project A** blocked, **Project B** unrelated | **Continue** — B’s entries run in normal canonical order; A’s repair does not block B. |
| Post–little-val **hard block** on roadmap pipeline | Layer 1 **appends** a repair line (e.g. `params.action: recal` or `handoff-audit`), **consumes** the triggering entry id (`processed_success_ids`), does **not** auto re-dispatch deepen for that same line. |

## JSONL snippets

**1. Repair after `contradictions_detected` (appended by Layer 1)**

See the full one-liner example in Queue-Sources (same `project_id`, `queue_priority: "repair"`, report link in `user_guidance`).

**2. Manual craft (equivalent intent)**

User or crafter may append the same shape; flags **`validator_repair_followup: true`** are enough for sort if `queue_priority` is omitted (prefer both for clarity).

## Checklist (manual test)

1. Queue two lines: `RESUME_ROADMAP` **deepen** and **repair** for the same `project_id`.
2. Run EAT-QUEUE; confirm **repair** dispatches **before** **deepen** when both are dispatchable in one pass (respect per-project serialism in **A.4**).
3. After a forced post–little-val hard block, confirm Watcher-Result **segment: VALIDATE** and Feedback-Log / Prompt-Log pivot line per [[3-Resources/Second-Brain/Logs#Tiered validator / queue pivot (Layer 1)|Logs § Tiered validator / queue pivot]].

See also [[3-Resources/Second-Brain/Tests-Validator#Phase 2 — tiered blocks and Layer 1 pivot|Tests-Validator § Phase 2]].
