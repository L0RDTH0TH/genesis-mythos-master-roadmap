---
title: Queue continuation (machine-readable)
created: 2026-03-21
tags: [second-brain, queue, roadmap, observability]
para-type: Resource
status: active
links:
  - "[[3-Resources/Second-Brain/Queue-Sources]]"
  - "[[3-Resources/Second-Brain-Config]]"
  - "[[.cursor/rules/agents/queue.mdc|agents/queue.mdc]]"
---

# Queue continuation spec

## Purpose

When a pipeline run finishes **without** appending a follow-up to `.technical/prompt-queue.jsonl` (e.g. `queue_next: false`, target reached, or repair-only path), operators and Layer 1 need a **machine-readable** record of **why** follow-up was suppressed and whether **optional empty-queue bootstrap** may apply. This spec defines the **`queue_continuation`** object and the durable log **`.technical/queue-continuation.jsonl`**.

**Not** a substitute for [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]] `queue_followups` / `queue_next` — those remain the primary continuation mechanism. Layer 1 **A.5c.1** may still append a synthesized line when Layer 2 omits **`queue_followups`** while **`queue_next !== false`**; continuation rows may record **`suppress_reason: queue_next_contract_violation_recovered`** when Layer 1 merges that outcome (**A.5e**). This artifact is for **traceability** and **config-gated bootstrap** only.

## Canonical object: `queue_continuation`

Emitted as a **fenced YAML block** at the end of a **RoadmapSubagent** return (after prose), root key **`queue_continuation`**. Layer 1 may **normalize** or **append** a derived object when the pipeline omits it (Queue-computed minimal record).

### Fields (schema_version 1)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `schema_version` | int | yes | Must be `1` for this spec revision. |
| `source` | string | yes | `roadmap_task_return` \| `layer1_post_a5b` \| `layer1_empty_bootstrap` \| `layer1_computed` \| `layer1_nested_gate_failure` |
| `queue_entry_id` | string | yes | The `id` of the queue entry that triggered this run. |
| `project_id` | string | when roadmap-scoped | Slug, e.g. `genesis-mythos-master`. |
| `suppress_followup` | bool | yes | `true` when no `queue_followups.next_entry` was emitted by policy for this completion. |
| `suppress_reason` | string | yes | See **Suppress reason enum** below. |
| `continuation_eligible` | bool | yes | `true` **only** when auto-bootstrap may apply (narrow); default **`false`**. |
| `suggested_next` | object | no | Optional hint: `{ "mode": "RESUME_ROADMAP", "params": { ... } }`. Queue **always** validates before append. |
| `rationale_short` | string | no | Human summary for logs; not parsed for policy. |
| `completed_iso` | string | recommended | ISO 8601 UTC when the run completed (for TTL checks). |

### Additive fields (schema_version 1 — anti-spin telemetry)

When **`queue.gate_block_detection_enabled`** or **`queue.spin_detection_enabled`** is true and the dispositioned entry is **`RESUME_ROADMAP`** (primary mode), Layer 1 **A.5e** **must** merge these into the **`.technical/queue-continuation.jsonl`** line (use explicit empty objects when not computed, not omission):

| Field | Type | Required when flags on | Description |
|-------|------|------------------------|-------------|
| `spin_signal` | object | yes | e.g. `flat_delta_streak`, `same_action_class_as_prev`, `suspected_spin`; `{}` if not computed. |
| `gate_block_signal` | object | yes | e.g. `gate_signature`, `gate_streak`, `blocked_track`, `pivot_to_track`, `threshold_met`; `{}` if not computed. |
| `resolver_alignment` | object | yes | `aligned` \| `partially_aligned` \| `overridden_by_user_lock` \| `drifted`, or `{ "skipped": true, "reason": "..." }` when comparison not done. |
| `effective_track` | string | recommended | `conceptual` \| `execution` — copy from Layer 1 **`layer1_resolver_hints`** / Roadmap **`validator_context`** for traceability. |
| `gate_catalog_id` | string | optional | `conceptual_v1` \| `execution_v1` per [[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-By-Track|Roadmap-Gate-Catalog-By-Track]]. |

**`queue_continuation` YAML** in Roadmap Task returns may also carry mirrors of these when the pipeline emits them; Layer 1 merges and wins on missing pipeline fields.

See [[3-Resources/Second-Brain/Docs/Queue-Gate-State-Spec|Queue-Gate-State-Spec]] for durable `gate_streak` storage.

### Suppress reason enum

| Value | Meaning |
|-------|---------|
| `explicit_queue_next_false` | User/crafter or params set `queue_next: false` — **terminal** for bootstrap. |
| `target_reached` | Canonical roadmap target satisfied; no further RESUME_ROADMAP. |
| `conceptual_target_reached` | **Conceptual track only:** design-handoff / `conceptual_design_handoff_min_readiness` floors met; coherence satisfied; execution-only gaps advisory — terminal suppress; Layer 1 **A.5c.1** must **not** synthesize deepen/recal. |
| `handoff_gate` | Handoff gate satisfied; follow-up suppressed per policy. |
| `hard_ceiling` | Iteration / context ceiling; RECAL or wrapper instead of deepen follow-up. |
| `repair_only` | Run was repair-oriented; no automatic deepen follow-up. |
| `post_little_val_hard_block_consumed` | Layer 1 appended A.5b repair; original entry consumed. |
| `pipeline_failure` | Task returned failure / `#review-needed` without success path. |
| `nested_attestation_failure` | Layer 1 refused successful consumption because **`validator_context`** and/or mandatory **`nested_subagent_ledger`** failed **strict nested return gates** ([[3-Resources/Second-Brain-Config|Second-Brain-Config]] § **`queue.strict_nested_return_gates`** / **`queue.strict_nested_ledger_all_pipelines`**) or equivalent **`queue_failed`** path for this entry. Written by Layer 1 **A.5e** merge when `continuation_log_enabled` is true — not emitted by Roadmap pipeline YAML in the failure path. |
| `queue_next_contract_violation_recovered` | Layer 1 **A.5c.1** appended a **synthesized** **`RESUME_ROADMAP`** line because the Roadmap Task return was **Success** with **`queue_next !== false`** but omitted a valid **`queue_followups.next_entry`**. Use when **A.5e** merges / normalizes the continuation row after synthesis (optional override of pipeline-emitted **`suppress_reason`**). **`continuation_eligible`:** **`false`** unless docs specify otherwise. |
| `no_gain_pending_user_gates` | **BREAK-SPIN / no marginal gain:** autonomous iteration without user-set gates would be noise; no alternate deepen targets and **`break_spin_recal_fallback_when_no_alternate`** is **false** — terminal suppress; Layer 1 **A.5c.1** must **not** synthesize deepen/recal. Same class as **`target_reached`** for empty-queue bootstrap (**`continuation_eligible: false`**). |
| `other` | Use with `rationale_short`; **`continuation_eligible` must be `false`** unless narrowly justified in docs. |

## Invariants

1. **`continuation_eligible: true` MUST NOT** appear when **`suppress_reason === explicit_queue_next_false`**.
2. **`continuation_eligible: true` MUST NOT** appear when **`suppress_reason === target_reached`**, **`suppress_reason === conceptual_target_reached`**, or **`suppress_reason === no_gain_pending_user_gates`**.
3. Roadmap **must** set **`continuation_eligible`** consistently with [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]] § **`queue_next`**, § **`effective_followup_required`**, § **When does the system stop appending**, and § **RESUME_ROADMAP params**.
4. Default for any ambiguous case: **`continuation_eligible: false`**.
5. When **`suppress_reason === nested_attestation_failure`**, **`continuation_eligible` MUST be `false`** (same class as **`pipeline_failure`** for empty-queue bootstrap — do **not** auto-continue from this record).
6. When the Task return includes **`queue_followups.next_entry`**, **`suppress_followup` MUST be `false`** and **`suppress_reason` MUST NOT** imply “no follow-up” unless the follow-up object is intentionally void (invalid — do not do this).
7. **Success** + **`params.queue_next !== false`** on the queue entry **requires** **`queue_followups.next_entry`** on the Roadmap return **or** a **terminal** **`suppress_reason`** from the enum above — see Queue-Sources § **`effective_followup_required`**.

**Layer 1 merge (nested attestation):** When a pipeline entry fails strict nested attestation after the pipeline Task returns, Layer 1 appends a JSONL line with **`source: layer1_nested_gate_failure`** (preferred for machine filtering) or **`layer1_computed`** if you collapse sources — spec prefers **`layer1_nested_gate_failure`** for attestation-only rows. Include **`suppress_followup: true`**, **`suppress_reason: nested_attestation_failure`**, **`continuation_eligible: false`**, **`queue_entry_id`**, optional **`rationale_short`** / **`error_type`** (e.g. `missing_validator_context`, `invalid_validator_context`, `nested_ledger_missing_or_unparseable`), **`completed_iso`**. See [[.cursor/rules/agents/queue.mdc|queue.mdc]] **A.5e**.

## Durable log: `.technical/queue-continuation.jsonl`

- **Format:** One JSON object per line (JSONL), append-only.
- **Writer:** Queue/Dispatcher (Layer 1) after each queue entry reaches a **terminal state for that EAT-QUEUE dispatch** (success after post–little-val + A.5b, or failure logged), when **`queue_continuation.continuation_log_enabled`** is **true** under the **`queue_continuation`** block in [[3-Resources/Second-Brain-Config|Second-Brain-Config]].
- **Content:** Merge parsed **`queue_continuation`** from the pipeline return (if present) with Layer 1 fields: `queue_entry_id`, `parent_run_id` if known, optional post–little-val summary.
- **Reader:** Layer 1 **A.1b** — when **`prompt-queue.jsonl`** has **zero valid entries** after A.2 parse and **`queue_continuation.empty_queue_bootstrap_enabled`** is **true**, tail-read the log (last **N** lines from **`queue_continuation.empty_queue_bootstrap_tail_lines`**, default **50**), select the newest record where **`continuation_eligible === true`**, **`suppress_reason`** is not `explicit_queue_next_false`, `target_reached`, **`conceptual_target_reached`**, **`no_gain_pending_user_gates`**, **`pipeline_failure`**, or **`nested_attestation_failure`**, and **`completed_iso`** is within **`empty_queue_bootstrap_max_age_minutes`**.

## Empty-queue bootstrap (Layer 1)

When eligible record found:

1. If **`queue_continuation.empty_queue_bootstrap_prompt_craft`**: `Task(prompt_craft)` with **`craft_source: empty_queue_bootstrap`** (see [[Prompt-Craft-Subagent]] / `.cursor/agents/prompt-craft.md`).
2. Else: build one **minimal** `RESUME_ROADMAP` JSONL line from **`suggested_next`** if present and valid; else from **`project_id`** + default **`params.action: deepen`** + **`params.user_guidance`** citing continuation record and source `queue_entry_id`.
3. **Append** only if **`queue_continuation.empty_queue_bootstrap_auto_append`** is **true**; otherwise append **Watcher-Result** with `message: "empty-queue bootstrap: eligible record found; auto_append false — review or enable empty_queue_bootstrap_auto_append"` and put the suggested JSONL in **`trace`** (mirror **`recovery_auto_append`** false behavior).
4. **Idempotency:** Set **`idempotency_key`** on the bootstrapped line: `empty-bootstrap-<queue_entry_id>-<completed_iso>` so repeat EAT-QUEUE does not duplicate.

## Run-Telemetry (optional mirror)

Optional frontmatter on `.technical/Run-Telemetry/*.md` may duplicate **`queue_continuation_`** prefixed keys for Dataview. See [[3-Resources/Second-Brain/Parameters|Parameters]] § Run-Telemetry. **Canonical** source for bootstrap remains **`queue-continuation.jsonl`** when logging is enabled.

## Examples

### Deepen success, explicit stop

```yaml
queue_continuation:
  schema_version: 1
  source: roadmap_task_return
  queue_entry_id: queue-repair-gaps-deepen-phase2-2-20260320-3
  project_id: genesis-mythos-master
  suppress_followup: true
  suppress_reason: explicit_queue_next_false
  continuation_eligible: false
  rationale_short: "queue_next false per handoff-readiness run; no auto follow-up"
  completed_iso: "2026-03-21T12:15:00.000Z"
```

### Eligible bootstrap (narrow)

```yaml
queue_continuation:
  schema_version: 1
  source: roadmap_task_return
  queue_entry_id: example-id
  project_id: genesis-mythos-master
  suppress_followup: true
  suppress_reason: other
  continuation_eligible: true
  rationale_short: "Operator-flagged optional resume; repair path left queue empty"
  suggested_next:
    mode: RESUME_ROADMAP
    params:
      action: deepen
      project_id: genesis-mythos-master
  completed_iso: "2026-03-21T14:00:00.000Z"
```

## Cross-references

- Durable streaks: [[3-Resources/Second-Brain/Docs/Queue-Gate-State-Spec|Queue-Gate-State-Spec]].
- Orchestration: [[.cursor/rules/agents/queue.mdc|queue.mdc]] **A.1b**, **A.5b** (hard-block gate), continuation log append.
- Pipeline: [[.cursor/agents/roadmap.md|roadmap.md]] — end-of-return **`queue_continuation`** block.
- Config: [[3-Resources/Second-Brain-Config|Second-Brain-Config]] § **queue_continuation**.
