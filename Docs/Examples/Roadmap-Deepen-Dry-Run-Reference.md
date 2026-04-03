---
title: Roadmap deepen dry-run railroad (exemplar)
created: 2026-04-02
tags:
  - second-brain
  - eat-queue
  - dry-run
  - roadmap
  - examples
para-type: Resource
status: reference
source: "Illustrative trace; subordinate to queue and roadmap agent contracts. See precedence block."
---

> **Precedence (normative):** This note is **illustrative only**. It **must not** override:
>
> - [[.cursor/agents/queue|FINAL GATEKEEPER (agents/queue.md)]]
> - [[.cursor/rules/agents/queue.mdc|queue.mdc]] (A.5d dispatch / Layer 1 gate)
> - [[3-Resources/Second-Brain/Docs/Safety-Invariants|Safety-Invariants]]
> - [[3-Resources/Second-Brain/Docs/Roadmapping-System|Roadmapping-System]]
>
> Layer 2 balance-mode obligations are defined in [[.cursor/agents/roadmap|agents/roadmap.md]] and [[3-Resources/Second-Brain/Subagent-Safety-Contract|Subagent-Safety-Contract]].

# Roadmap deepen dry-run — Layer 0 through Layer 2 (railroad exemplar)

**Date stamped:** 2026-04-02  
**Scope:** Narrative simulation of processing **one** prompt-queue line for `RESUME_ROADMAP` / `action: deepen` — **no** actual `Task` dispatch, **no** queue file mutation, **no** vault writes.  
**Project:** `genesis-mythos-master` (conceptual track).

---

## Subject queue entry (JSONL line)

```json
{
  "id": "followup-deepen-phase5-51-mint-gmm-20260403T231000Z",
  "mode": "RESUME_ROADMAP",
  "project_id": "genesis-mythos-master",
  "params": {
    "project_id": "genesis-mythos-master",
    "action": "deepen",
    "roadmap_track": "conceptual",
    "queue_next": true,
    "user_guidance": "Mint Phase 5 secondary 5.1 (rule primitives, plugin host, deterministic conflict precedence) from the current Phase 5 primary context. Use existing Phase 5/earlier phase notes and CDRs as authority; do not touch execution track. Note* This is a re-run of an already ran queue item, ignore this and run as if its the first run"
  }
}
```

---

## Layer 0 (dispatcher / chat → Queue subagent)

1. User or dispatcher triggers **EAT-QUEUE** (or equivalent: Process queue, EAT-CACHE with prompt queue).
2. **Layer 0 does not** parse `.technical/prompt-queue.jsonl` or run Step 0 itself; it **calls `Task`** once with `subagent_type: queue` and a hand-off containing vault root, prompt queue path, task queue path, and which queue(s) to process.
3. Optional: append **task-handoff-comms** (`handoff_out` / `return_in`) to `.technical/task-handoff-comms.jsonl` per Task-Handoff-Comms-Spec when enabled in Config.

---

## Layer 1 (Queue / Dispatcher subagent) — high-level pass

### A.0 — Step 0: Decision wrappers

- Scan `Ingest/Decisions/**` for approved / re-wrap wrappers that must run before pipeline dispatch.
- For this dry run: no `roadmap-next-step` wrapper was found that would override `params.action: deepen`.

### A.1–A.2 — Read, parse, validate, dedupe, order

- Read `.technical/prompt-queue.jsonl`.
- Validate `mode`, `id`, required fields per Queue-Sources.
- Order entries per queue processor rules (CHECK_WRAPPERS, mode priority, etc.).

### A.3–A.4 — Resolver / anti-spin (RESUME_ROADMAP)

- When `queue.roadmap_next_need_enabled` (or equivalent) is on, compute **structural_state** from authoritative files:
  - `1-Projects/genesis-mythos-master/Roadmap/workflow_state.md` — e.g. `current_subphase_index: "5.1.1"`, `last_ctx_util_pct`, `last_conf`.
  - `1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md` — `roadmap_track: conceptual`, phase summaries.
- **Reconcile stale `user_guidance`:** queue text may say “mint secondary 5.1”; authoritative cursor may already point at **next tertiary 5.1.1** after secondary 5.1 exists. Resolver sets **`effective_target`** to the vault cursor, not the stale text.
- Emit **`## layer1_resolver_hints`** (fenced YAML) on the Task hand-off to Roadmap subagent, including keys such as: `need_class`, `effective_action`, `effective_target`, `gate_signature`, `effective_track`, `track_lock_explicit` (true when `params.roadmap_track` is explicit), `gate_catalog_id`, etc.

### Dispatch

- Launch **Roadmap subagent** via `Task(subagent_type: roadmap)` with full hand-off + telemetry block (`parent_run_id`, `queue_entry_id`, `project_id`, timestamps).

---

## Layer 2 (Roadmap subagent) — RESUME_ROADMAP `deepen`

### Intake

1. Parse **`## layer1_resolver_hints` first** — resolver hints override stale queue `user_guidance` for scope.
2. Resolve `project_id` → `1-Projects/genesis-mythos-master/Roadmap/`.
3. Read `roadmap-state.md`, `workflow_state.md`, `distilled-core.md` as needed; read parent phase / secondary notes for the active slice.

### Action: deepen (roadmap-deepen skill semantics)

- **Target:** Aligned to **`current_subphase_index`** (e.g. mint or refine **tertiary 5.1.1** under secondary 5.1), not necessarily re-minting secondary 5.1 if already present and complete.
- **Dual track:** `roadmap_track: conceptual` — writes stay on conceptual tree; do not mutate `Roadmap/Execution/` for this entry.
- **Frozen guard:** If a target note exists with `frozen: true` on conceptual track, destructive overwrite is blocked; route to Conceptual-Amendments per Vault-Layout / dual-track rules.

### Context utilization (`enable_context_tracking`)

- Estimate tokens from prompt + state files + notes read; compute `context_util_pct`, `leftover_pct`, threshold columns in workflow_state **Log** when tracking is on.
- **Overflow:** If estimated tokens > ~90% of window → log `context-overflow`, queue RECAL-ROAD, do not deepen further.
- **High-util gate:** If `context_util_pct ≥ recal_util_high_threshold` (default 70%) **or** `context_util_pct > context_util_threshold` (default 80%): return **`queue_followups`** requesting **RECAL-ROAD** (`RESUME_ROADMAP` with `params.action: "recal"`) instead of another deepen follow-up.

### Writes (simulated)

- Snapshot `roadmap-state.md` / `workflow_state.md` before updates (per guardrails).
- Create or update roadmap note(s); append **workflow_state** Log row; update `current_subphase_index` and iteration counters.
- Conceptual track: optional **conceptual-decision-record** + bullet under `decisions-log.md` **Conceptual autopilot** when policy says so.

### Balance mode / nested helpers (vault-specific)

This railroad **narrates** control flow only. It does **not** depict every nested `Task` attempt or ledger row.

### Alignment note (this vault)

- **Balance-mode deepen** must follow **[[.cursor/agents/roadmap|agents/roadmap.md]]** first: real nested **`Task`** calls for **Validator** and **IRA** where the contract requires, with **`nested_subagent_ledger`** attestation (`task_tool_invoked: true` or `task_error` as applicable). “Minimal helpers” or “simulation skipped nested Tasks” wording in informal chat is **non-normative**.
- **Authoritative** obligations for nested helpers and Task hardening live in [[3-Resources/Second-Brain/Subagent-Safety-Contract|Subagent-Safety-Contract]] and [[3-Resources/Second-Brain/Docs/Subagent-Layers-Reference|Subagent-Layers-Reference]]; this exemplar cannot relax them.

### Return payload to Layer 1

- `queue_followups` with `next_entry` (often another `RESUME_ROADMAP` or `recal`) when `queue_next !== false` and gates allow.
- `queue_continuation` for terminal / suppress cases when applicable.
- `nested_subagent_ledger`, `validator_context` as produced by the run.

---

## Back to Layer 1 — post-return (FINAL GATEKEEPER, A.5d family)

1. **Parse** roadmap return: `nested_subagent_ledger`, `queue_continuation`, `queue_followups`, `validator_context`.
2. Run **mandatory independent checklist** (see [[.cursor/agents/queue]] top block and **A.5d** in [[.cursor/rules/agents/queue]]): balance mode deepen requires nested validator steps with real Task invocations where required; hygiene failures are provisional, not blind Success.
3. **Append `queue_followups.next_entry`** to `.technical/prompt-queue.jsonl` when present and valid (read-then-append) **before** or per ordering with post–little-val validator (per queue.mdc merge rules).
4. Post–little-val **Task(validator)** for roadmap when applicable; conceptual track may treat certain execution-only advisories as non-blocking per tiered policy.
5. **Watcher-Result:** append line(s) per `requestId` (queue entry `id`); two lines if VALIDATE segment + primary disposition.
6. **Rewrite queue:** remove consumed `id` from `prompt-queue.jsonl`; preserve unprocessed lines.

---

## One-line outcome summary (this scenario)

- Stale **“mint 5.1 secondary”** guidance is **reconciled** to authoritative **`current_subphase_index`** (e.g. next work at **5.1.1**).
- High context utilization likely triggers **`recal`** follow-up instead of immediate chained deepen.
- Layer 1 remains the **FINAL GATEKEEPER** on roadmap returns; this exemplar **must not** override [[.cursor/rules/agents/queue]] or [[.cursor/agents/queue]].

---

## Related

- Source dry-run note (same narrative origin): [[3-Resources/Second-Brain/Docs/EAT-QUEUE-Dry-Run-Layer0-2-2026-04-02|EAT-QUEUE-Dry-Run-Layer0-2-2026-04-02]]
- User flows: [[3-Resources/Second-Brain/Docs/User-Flows/EAT-QUEUE-Flow|EAT-QUEUE-Flow]]
- Queue pipeline: [[3-Resources/Second-Brain/Docs/Pipelines/Queue-Pipeline|Queue-Pipeline]]
