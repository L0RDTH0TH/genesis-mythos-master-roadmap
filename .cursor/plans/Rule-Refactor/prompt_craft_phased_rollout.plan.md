---
name: Prompt craft phased rollout
overview: "Two-phase delivery of PromptCraft recovery: Phase 1 documents contracts and flows; Phase 2 implements agents, queue wiring, Validator, and Config. Goals match the design plan prompt_craft_subagent_ed0935fd.plan.md (same or ~/.cursor/plans/); this file is only the rollout schedule."
todos:
  - id: phase1-contracts
    content: "Phase 1: Subagent-Safety-Contract, Queue-Sources, MCP-Tools, Validator-Reference/spec, pipeline return + L1 flow prose"
    status: completed
  - id: phase1-user-docs
    content: "Phase 1: Docs/Prompt-Craft-Subagent.md, Rules/Pipelines index, Errors.md protocol line, Subagent-Layers-Reference cross-link"
    status: completed
  - id: phase2-agents
    content: "Phase 2: agents/prompt-craft.md + rules/agents/prompt-craft.mdc + Task subagent_type + sync/changelog"
    status: completed
  - id: phase2-queue-l1
    content: "Phase 2: queue.mdc L1 branch — IRA bubble in pipeline return → Task(prompt_craft) → L1 append → eat + caps"
    status: completed
  - id: phase2-pipeline-returns
    content: "Phase 2: Layer 2 prompts/rules — emit structured post-IRA failure bundle (finalize field name + schema)"
    status: completed
  - id: phase2-validator-config
    content: "Phase 2: recovery outcome validation_type + optional pre-append lint; Second-Brain-Config keys; dispatcher/funnels triggers"
    status: completed
isProject: false
---

# Prompt craft subagent — phased rollout

**Source design:** Full behavior, IRA bubble path, Validator semantics, and hand-off shapes live in `**~/.cursor/plans/prompt_craft_subagent_ed0935fd.plan.md`** (copy into this repo’s `.cursor/plans/` if you want a single vault-local design doc). This document only **sequences** work: **Phase 1 = document**, **Phase 2 = build**.

## Goals (unchanged)

1. **PromptCraftSubagent** — Read-mostly helper that turns **failure context** into **merge-aware, linted** queue payload(s) and `**jsonl_lines_suggested`**; does **not** write `prompt-queue.jsonl`; does **not** run pipelines.
2. **Recovery outcome Validator** — After crafted lines are **eaten and executed**, hostile pass answers: **failure + before state**, **crafter’s lines + intent**, **after state** → **did it fix it?**
3. **Pre-append lint (optional)** — Shallow validation of proposed JSONL **before** L1 append; separate from outcome pass.
4. **IRA bubble path** — Layer 2 return includes structured **post-IRA / post–nested-Validator failure bundle** (working name `ira_output_bubble`; **finalize key + schema in Phase 1**). **Layer 1** runs `Task(prompt_craft)` → **L1** read-append-write → continue EAT-QUEUE with repair ordering, `**idempotency_key`**, **max auto-craft per `error_correlation_id`**.
5. **Layer labels** — L0 = Cursor chat, L1 = Queue ([[3-Resources/Second-Brain/Docs/Subagent-Layers-Reference|Subagent-Layers-Reference]]); do not redefine in implementation docs.
6. **Coexistence** — Plan-mode prompt crafter (§1 Q&A) stays human-led in chat; PromptCraft is **machine-routed recovery** (+ optional proactive craft).
7. **Guardrails** — `recovery_auto_append` default **false**; no IRA/Validator → PromptCraft direct calls; no infinite craft loops without policy.

---

## Phase 1 — Document new behavior

**Exit criteria:** A reader can implement Phase 2 without reverse-engineering chat; contracts name fields, owners (L1 vs L2 vs Validator), and ordering.


| Step | Deliverable                                                                                                                    |
| ---- | ------------------------------------------------------------------------------------------------------------------------------ |
| 1.1  | **[[3-Resources/Second-Brain/Subagent-Safety-Contract                                                                          |
| 1.2  | **[[3-Resources/Second-Brain/Queue-Sources                                                                                     |
| 1.3  | **[[3-Resources/Second-Brain/MCP-Tools                                                                                         |
| 1.4  | **[[3-Resources/Second-Brain/Docs/Prompt-Craft-Subagent                                                                        |
| 1.5  | **[[3-Resources/Second-Brain/Rules                                                                                             |
| 1.6  | **Error Handling Protocol** ([[3-Resources/Second-Brain/Errors                                                                 |
| 1.7  | **[[.cursor/rules/always/system-funnels                                                                                        |
| 1.8  | **Second-Brain-Config** (spec in doc) — `recovery_auto_append`, `validator.recovery_outcome.model` (names finalizable in 1.3). |


**Phase 1 does not add** `.cursor/agents/prompt-craft.md`, queue code paths, or Validator runtime — documentation and agreed schemas only.

---

## Phase 2 — Build new behavior

**Exit criteria:** End-to-end dry path: synthetic failure envelope → `Task(prompt_craft)` → L1 append → EAT-QUEUE runs new line(s) → outcome Validator Task → verdict logged.


| Step | Deliverable                                                                                                                                                                                                                                                               |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2.1  | `**.cursor/agents/prompt-craft.md`** + `**.cursor/rules/agents/prompt-craft.mdc`** — Full behavior: merge (`deepMerge` parity with roadmap defaults), per-mode lint, `jsonl_lines_suggested`, `lint_blockers`, `recovery_metadata`; read-only vault except allowed reads. |
| 2.2  | **Task tool** — `subagent_type: prompt_craft` (or document fallback until Cursor enum allows it).                                                                                                                                                                         |
| 2.3  | `**.cursor/rules/agents/queue.mdc`** — After pipeline return matching **post-IRA craft policy**, build hand-off, `Task(prompt_craft)`, pre-append gate if any, **read-append-write** queue, re-sort, continue dispatch; enforce **correlation + cap**.                    |
| 2.4  | **Layer 2 agents/rules** (roadmap first, then others as needed) — Emit **final-named** failure bundle in return text/structure per Phase 1 schema.                                                                                                                        |
| 2.5  | **Validator subagent** + **validator.mdc** — Implement **recovery outcome** `validation_type` + report path; wire L1 (or L0) to call after recovery package completes.                                                                                                    |
| 2.6  | `**3-Resources/Second-Brain-Config.md`** — Apply keys from Phase 1 spec.                                                                                                                                                                                                  |
| 2.7  | **Dispatcher / system-funnels** — Apply trigger text from Phase 1 spec.                                                                                                                                                                                                   |
| 2.8  | `**.cursor/sync/`** + **changelog** — Per backbone-docs-sync.                                                                                                                                                                                                             |
| 2.9  | **Verification** — Fixture run + loop guard (duplicate correlation without new context → no second auto-craft).                                                                                                                                                           |


---

## Dependency

- **Phase 2 depends on Phase 1** for stable names (`validation_type`, pipeline return field name, Config keys). Minor renames in Phase 1 are allowed before any Phase 2 merge.

## Non-goals (both phases)

- PromptCraft does not replace **User-Questions §1** plan-mode crafter.
- No **silent** unbounded craft→append→eat loops.

