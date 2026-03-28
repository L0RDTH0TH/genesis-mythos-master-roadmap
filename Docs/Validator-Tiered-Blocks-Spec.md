---
title: Validator tiered blocks and queue pivots
created: 2026-03-20
tags: [second-brain, validator, queue, architecture]
para-type: Resource
status: active
links:
  - "[[3-Resources/Second-Brain/Validator-Reference|Validator-Reference]]"
  - "[[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]]"
  - "[[3-Resources/Second-Brain/Subagent-Safety-Contract|Subagent-Safety-Contract]]"
---

# Validator tiered blocks and queue pivots

This note is the **feature spec** for tiered validator handling: **reason-code routing**, **scoped blocks**, **repair-first queue ordering**, and **Layer 1 pivots**. Pipeline rules and queue rules implement this spec; [[3-Resources/Second-Brain/Validator-Reference|Validator-Reference]] remains the contract for severity / `recommended_action` strings.

---

## 1. Definitions

### 1.1 Incoherence

**Incoherence** means a hostile reader **cannot reliably restate system boundaries and responsibilities** from the artifacts under review **without guessing**, and the failure is **not** reducible to:

- a single **contradiction** (two explicit incompatible claims → use `contradictions_detected`), nor  
- **missing artifacts** only (sections/checklists not yet written → `needs_work`).

**Operational test:** Given only the validated slice, can a senior engineer write one short paragraph stating what is in-scope, out-of-scope, and who owns which seams? If **no** without invention → incoherence-class.

### 1.2 Contradiction

**Contradiction:** Two or more **explicit** claims in validated artifacts that **cannot all be true** (phase vs phase, phase vs `roadmap-state` / `workflow_state`, phase vs master goal, intra-note label vs body). Use **`reason_code: contradictions_detected`**.

### 1.3 Safety-critical vs safety-unknown

- **`safety_critical_ambiguity`:** Ambiguity or unknowns such that **continuing automated destructive work** (deepen, move, large overwrites) risks **wrong structure, dual truth, or destructive thrash**. Maps to **high** / `block_destructive` when automation would compound harm.
- **`safety_unknown_gap`:** Floating scope holes, pending decisions **without** a decision id / wrapper / explicit deferral contract, or weak roll-up traceability **without** a direct logical contradiction. Typically **medium** / `needs_work`, not `block_destructive`, unless paired with a true block condition.

### 1.4 Severe state hygiene

**`state_hygiene_failure`:** Conflicting **canonical** truth sources, broken timeline/order of state, or hygiene failures **severe enough** that automation cannot pick a single reconciled story without human or RECAL-class intervention.

---

## 2. Closed-set `reason_codes` and `primary_code`

Validators SHOULD emit codes from this set for roadmap handoff types (extend only via Validator-Reference + this spec):

| `reason_code` | Typical use |
|---------------|-------------|
| `contradictions_detected` | Explicit incompatible claims |
| `state_hygiene_failure` | Canonical state / timeline / dual-truth |
| `safety_critical_ambiguity` | Automation-unsafe ambiguity |
| `safety_unknown_gap` | Gaps, deferrals, weak traceability (usually needs_work) |
| `incoherence` | Boundaries unrestatable per §1.1 |
| `missing_*` / checklist codes | Completeness (e.g. `missing_task_decomposition`) → usually needs_work |

**`primary_code` (when multiple codes):** Order of precedence for **routing Layer 1 pivots** and **hard-block** decisions:

1. `state_hygiene_failure`  
2. `contradictions_detected`  
3. `incoherence`  
4. `safety_critical_ambiguity`  
5. else highest-severity finding among remainder (e.g. `safety_unknown_gap` alone does not force block_destructive).

Document `primary_code` in the validator return / report when more than one code is present.

---

## 3. Action matrix (roadmap_handoff_auto and aligned types)

| `reason_code` (primary) | Typical `severity` | Typical `recommended_action` | Nested pipeline Success? | Allowed non-blocked pivot (same project) |
|-------------------------|-------------------|--------------------------------|----------------------------|----------------------------------------|
| `state_hygiene_failure` | high | `block_destructive` | No | `recal`, `handoff-audit`; optional `sync-outputs` |
| `contradictions_detected` | high | `block_destructive` | No | `recal`, `handoff-audit` (+ citations / report path in `user_guidance` or `prompt`) |
| `incoherence` | high | `block_destructive` | No | `recal`, `resume-from-last-safe` with guidance; `#review-needed` |
| `safety_critical_ambiguity` | high | `block_destructive` | No | Wrapper or audit; `recal` if drift-wide |
| `safety_unknown_gap` | medium | `needs_work` | Yes (if little val ok) | Next `deepen` with `next_artifacts`; log `#review-needed` |
| Missing-artifact codes only | medium | `needs_work` | Yes (if little val ok) | Continue roadmap / ingest per queue |

**Tiered Success gate (pipelines):** After the **final** nested validator pass, claim **Success** only if **not** (`severity: high` **or** `recommended_action: block_destructive`) **unless** the only remaining findings are `needs_work` with **no** primary_code in the hard-block rows above. Concretely: **high** or **`block_destructive`** → **no Success**; **`needs_work`** alone → **Success allowed** when little val ok (roadmap and other pipelines per Subagent-Safety-Contract).

**Post–little-val (Layer 1):** Same signals; Layer 1 **appends repair follow-ups** and applies **repair-first sort** (Queue-Sources, queue.mdc). It does **not** call IRA.

---

## 4. Scoped block contract

- **Block scope:** `(project_id, optional phase/slice ids, validation_type)` derived from validator report + queue entry.
- **Frozen for automation:** Further **`RESUME_ROADMAP` `deepen`** (or `advance-phase`) that **depends** on the contradicted / incoherent / unsafe spine **for that scope** until repair completes or human overrides.
- **Allowed without waiting:** Other **`project_id`s**; modes that do not assume the frozen contract (e.g. **INGEST_MODE** on unrelated notes, **DISTILL_MODE** on Resources, **RESEARCH_AGENT** for another project); **`RESUME_ROADMAP`** with **`action: recal`**, **`handoff-audit`**, **`sync-outputs`**, **`resume-from-last-safe`** when scoped to reconcile.

Pipeline returns SHOULD include **`blocked_scope`** in structured return metadata: `{ "project_id": "...", "phase_ids": [], "paths": [] }` when a hard block applies.

---

## 5. Repair-first (same scope)

When a **hard block** or surviving **`contradictions_detected`** applies to scope S:

1. Layer 1 **appends** a **repair** queue line for the same `project_id` (and optional `params.phase` / guidance from report): prefer **`RESUME_ROADMAP`** with **`params.action: recal`** or **`handoff-audit`** (or **`sync-outputs`** when appropriate).
2. **Repair lines MUST sort before** other **`RESUME_ROADMAP`** lines for the **same** `project_id` that would **deepen** or **advance** the same spine.  
   **Rationale:** `RECAL-ROAD` normalizes to `RESUME_ROADMAP`, so mode-order alone does not separate recal from deepen — use **`queue_priority: repair`** (integer, lower = earlier) or **`validator_repair_followup: true`** plus **sub-sort** in auto-eat-queue (see Queue-Sources).
3. **Orthogonal** entries (other projects / no dependency) **continue** in canonical order without waiting for S’s repair.
4. **Pass 3 (inline repair drain, same EAT-QUEUE run):** After Layer 1 **A.5b** (or repair-class **A.5d** recovery) appends a **`RESUME_ROADMAP`** repair line, **`queue.inline_a5b_repair_drain_enabled`** (Second-Brain-Config) gates whether **Pass 3** runs: re-read **`prompt-queue.jsonl`**, tag **`dispatch_pass: inline`**, and dispatch **`Task(roadmap)`** on the new **`id`** before **A.7**, within **`max_repair_roadmap_dispatches_per_project_per_run`** (shared with cleanup-pass repair dispatches) and **`max_inline_a5b_repair_generations_per_run`**. See [[.cursor/rules/agents/queue.mdc|queue.mdc]] **A.4c**, **A.5.0**, **A.5b**.

---

## 6. Chained queue entries

When `mode` is **`PRIMARY-DEP-...`** (chain):

- **Dependencies** run first per existing chain rules.
- If **primary** returns **hard block** (`severity: high` or `recommended_action: block_destructive`) **after** dependencies succeeded: **do not re-run** dependencies; append **repair** follow-up for primary’s `project_id` per §5; set primary line **`queue_failed: true`** **or** **consume** primary + append repair only — per chosen A.7 policy in Queue-Sources / queue.mdc (**default recommendation:** consume primary id from success set only when repair line is appended with same logical intent; else mark `queue_failed` for human visibility).
- If primary **fails before** dependencies: **abort** remaining chain segments for that `chain_id`; log Watcher-Result with `segment` and failure.

---

## 7. Implementation map

| Artifact | Role |
|----------|------|
| [[3-Resources/Second-Brain/Validator-Reference\|Validator-Reference]] | Severity strings, true BLOCK list, pointer here |
| [[3-Resources/Second-Brain/Queue-Sources\|Queue-Sources]] | Optional queue fields, JSONL examples, A.7 |
| [[3-Resources/Second-Brain/Docs/Queue-Pivot-Examples\|Queue-Pivot-Examples]] | Repair-first vs continue; regression checklist |
| `.cursor/rules/agents/queue.mdc` | Layer 1 post-lv, append follow-up, messaging |
| `.cursor/rules/context/auto-eat-queue.mdc` | Sort, repair-first tie-break, chains |
| [[3-Resources/Second-Brain/Subagent-Safety-Contract\|Subagent-Safety-Contract]] | Pipeline return metadata, Layer 1 fields |
| `.cursor/rules/agents/validator.mdc` | Code mapping and calibration |
| Pipeline `*.mdc` / `agents/*.md` | Tiered Success gate, `blocked_scope` |

---

## 8. Config keys (optional)

See [[3-Resources/Second-Brain/Parameters|Parameters]] / [[3-Resources/Second-Brain-Config|Second-Brain-Config]]:

- `max_incoherence_retries` — cap guided retries for `incoherence` (default 0–1). **Wiring:** Roadmap subagent applies the decrement contract in `.cursor/agents/roadmap.md` § **Incoherence bounded retry** (and `roadmap.mdc`); Layer 1 **A.5b** uses the same formula on post–little-val repair lines when `primary_code` is `incoherence` (see Queue-Sources § Tiered validator queue fields).
- `validator.tiered_blocks_enabled` — if false, fall back to legacy “high or block_destructive always no Success” (optional kill-switch).
