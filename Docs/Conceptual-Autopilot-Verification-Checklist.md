---
title: Conceptual autopilot — verification checklist
created: 2026-03-25
tags: [second-brain, roadmap, queue, conceptual-track]
para-type: Resource
status: active
links:
  - "[[3-Resources/Second-Brain/Parameters|Parameters]] § Conceptual autopilot"
  - "[[.cursor/rules/agents/roadmap.mdc|roadmap.mdc]] § Smart dispatch"
  - "[[3-Resources/Second-Brain/Docs/Queue-Continuation-Spec|Queue-Continuation-Spec]]"
---

# Conceptual autopilot — manual verification

Run on a laptop with **Cursor `Task(queue)`** available and **`1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md`** with **`roadmap_track: conceptual`** (or equivalent **`effective_track`** from Layer 1).

1. **Enqueue** one **`RESUME_ROADMAP`** line with **`params.action: auto`** (or omit action), **`project_id: genesis-mythos-master`**, **`queue_next: true`**.
2. **EAT-QUEUE** once; confirm RoadmapSubagent **does not** create **`Ingest/Decisions/Roadmap-Decisions/`** roadmap-next-step wrappers **only** because confidence was low (autopilot should pick **deepen** / resolver action and append **`decisions-log.md` § Conceptual autopilot**).
3. After a nested **`roadmap_handoff_auto`** pass with **execution-only** **`needs_work`** (e.g. **`missing_roll_up_gates`**), confirm the **next** appended follow-up is **not** **`recal`**-only churn unless **`need_class`** / **`primary_code`** indicates coherence repair.
4. When floors in **Parameters § Conceptual autopilot** / **`roadmap.conceptual_design_handoff_min_readiness`** are met and coherence is clean, confirm return includes **`queue_continuation.suppress_reason: conceptual_target_reached`** or **`target_reached`** and **no** Layer 1 **A.5c.1** synthetic line appears in **`Errors.md`** as **`queue_next_contract_violation_recovered`** for that completion.
5. **Execution track** control: a project with **`roadmap_track: execution`** should **still** use Decision Wrappers on low confidence per **roadmap.mdc**.

Log outcome in project **`Run-Telemetry`** or **`decisions-log`** as an operator note when satisfied.
