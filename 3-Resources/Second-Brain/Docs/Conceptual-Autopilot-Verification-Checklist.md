---
title: Conceptual autopilot — verification checklist
created: 2026-03-25
tags: [second-brain, roadmap, queue, conceptual-track]
para-type: Resource
status: active
links:
  - "[[3-Resources/Second-Brain/Parameters|Parameters]] § Conceptual autopilot"
  - "[[3-Resources/Second-Brain/Parameters|Parameters]] § Conceptual subphase exit"
  - "[[.cursor/rules/agents/roadmap.mdc|roadmap.mdc]] § Smart dispatch"
  - "[[3-Resources/Second-Brain/Docs/Queue-Continuation-Spec|Queue-Continuation-Spec]]"
---

# Conceptual autopilot — manual verification

Run on a laptop with **Cursor `Task(queue)`** available and **`1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md`** with **`roadmap_track: conceptual`** (or equivalent **`effective_track`** from Layer 1).

1. **Enqueue** one **`RESUME_ROADMAP`** line with **`params.action: auto`** (or omit action), **`project_id: genesis-mythos-master`**, **`queue_next: true`**.
2. **EAT-QUEUE** once; confirm RoadmapSubagent **does not** create **`Ingest/Decisions/Roadmap-Decisions/`** roadmap-next-step wrappers **only** because confidence was low (autopilot should pick **deepen** / resolver action and append **`decisions-log.md` § Conceptual autopilot**).
3. After a nested **`roadmap_handoff_auto`** pass with **execution-only** **`needs_work`** (e.g. **`missing_roll_up_gates`**), confirm the **next** appended follow-up is **not** **`recal`**-only churn unless **`need_class`** / **`primary_code`** indicates coherence repair.
4. When floors in **Parameters § Conceptual autopilot** / **`roadmap.conceptual_design_handoff_min_readiness`** are met and coherence is clean, confirm return includes **`queue_continuation.suppress_reason: conceptual_target_reached`** or **`target_reached`** and **no** Layer 1 **A.5c.1** synthetic line appears in **`Errors.md`** as **`queue_next_contract_violation_recovered`** for that completion.
5. **Conceptual subphase exit:** With **`roadmap.conceptual_subphase_exit_enabled`** left at default (**true**) or explicitly **true**, and a slice that satisfies **Parameters § Conceptual subphase exit**, confirm the appended **`queue_followups.next_entry`** advances **`params.next_subphase_index`** / next structural target (not infinite polish on the same **`current_subphase_index`**) and **`decisions-log.md` § Conceptual autopilot** records **`subphase_slice_exit: true`** when the rewrite applies.
6. **Execution track** control: a project with **`roadmap_track: execution`** should **still** use Decision Wrappers on low confidence per **roadmap.mdc**.
7. **No-churn streak guard:** With **`queue.conceptual_same_subphase_streak_threshold`** at default (**2**), confirm Layer 1 does not allow repeated same-subphase deepen/recal follow-ups beyond threshold when no hard blocker is present; appended follow-up should pivot to next-node deepen and include trace marker **`[layer1_same_subphase_pivot]`**.
8. **High-util recal precedence:** With high context utilization and no hard blocker, confirm conceptual subphase-exit precedence still moves forward (rewrite to next-node deepen when predicate passes) when **`roadmap.conceptual_subphase_exit_override_high_util_recal: true`**.

Log outcome in project **`Run-Telemetry`** or **`decisions-log`** as an operator note when satisfied.
