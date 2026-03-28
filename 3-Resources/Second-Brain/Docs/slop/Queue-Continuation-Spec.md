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

**Not** a substitute for [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]] `queue_followups` / `queue_next` — those remain the primary continuation mechanism. This artifact is for **traceability** and **config-gated bootstrap** only.

## Canonical object: `queue_continuation`

Emitted as a **fenced YAML block** at the end of a **RoadmapSubagent** return (after prose), root key **`queue_continuation`**. Layer 1 may **normalize** or **append** a derived object when the pipeline omits it (Queue-computed minimal record).

### Fields (schema_version 1)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `schema_version` | int | yes | Must be `1` for this spec revision. |
| `source` | string | yes | `roadmap_task_return` \| `layer1_post_a5b` \| `layer1_empty_bootstrap` \| `layer1_computed` |
| `queue_entry_id` | string | yes | The `id` of the queue entry that triggered this run. |
| `project_id` | string | when roadmap-scoped | Slug, e.g. `genesis-mythos-master`. |
| `suppress_followup` | bool | yes | `true` when no `queue_followups.next_entry` was emitted by policy for this completion. |
| `suppress_reason` | string | yes | See **Suppress reason enum** below. |
| `continuation_eligible` | bool | yes | `true` **only** when auto-bootstrap may apply (narrow); default **`false`**. |
| `suggested_next` | object | no | Optional hint: `{ "mode": "RESUME_ROADMAP", "params": { ... } }`. Queue **always** validates before append. |
| `rationale_short` | string | no | Human summary for logs; not parsed for policy. |
| `completed_iso` | string | recommended | ISO 8601 UTC when the run completed (for TTL checks). |

### Suppress reason enum

| Value | Meaning |
|-------|---------|
| `explicit_queue_next_false` | User/crafter or params set `queue_next: false` — **terminal** for bootstrap. |
| `target_reached` | Canonical roadmap target satisfied; no further RESUME_ROADMAP. |
| `handoff_gate` | Handoff gate satisfied; follow-up suppressed per policy. |
| `hard_ceiling` | Iteration / context ceiling; RECAL or wrapper instead of deepen follow-up. |
| `repair_only` | Run was repair-oriented; no automatic deepen follow-up. |
| `post_little_val_hard_block_consumed` | Layer 1 appended A.5b repair; original entry consumed. |
| `pipeline_failure` | Task returned failure / `#review-needed` without success path. |
| `other` | Use with `rationale_short`; **`continuation_eligible` must be `false`** unless narrowly justified in docs. |

## Invariants

1. **`continuation_eligible: true` MUST NOT** appear when **`suppress_reason === explicit_queue_next_false`**.
2. **`continuation_eligible: true` MUST NOT** appear when **`suppress_reason === target_reached`**.
3. Roadmap **must** set **`continuation_eligible`** consistently with [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]] § **`queue_next`**, § **When does the system stop appending**, and § **RESUME_ROADMAP params**.
4. Default for any ambiguous case: **`continuation_eligible: false`**.

## Durable log: `.technical/queue-continuation.jsonl`

- **Format:** One JSON object per line (JSONL), append-only.
- **Writer:** Queue/Dispatcher (Layer 1) after each queue entry reaches a **terminal state for that EAT-QUEUE dispatch** (success after post–little-val + A.5b, or failure logged), when **`queue_continuation.continuation_log_enabled`** is **true** under the **`queue_continuation`** block in [[3-Resources/Second-Brain-Config|Second-Brain-Config]].
- **Content:** Merge parsed **`queue_continuation`** from the pipeline return (if present) with Layer 1 fields: `queue_entry_id`, `parent_run_id` if known, optional post–little-val summary.
- **Reader:** Layer 1 **A.1b** — when **`prompt-queue.jsonl`** has **zero valid entries** after A.2 parse and **`queue_continuation.empty_queue_bootstrap_enabled`** is **true**, tail-read the log (last **N** lines from **`queue_continuation.empty_queue_bootstrap_tail_lines`**, default **50**), select the newest record where **`continuation_eligible === true`**, **`suppress_reason`** is not `explicit_queue_next_false` or `target_reached`, and **`completed_iso`** is within **`empty_queue_bootstrap_max_age_minutes`**.

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

- Orchestration: [[.cursor/rules/agents/queue.mdc|queue.mdc]] **A.1b**, **A.5b** (hard-block gate), continuation log append.
- Pipeline: [[.cursor/agents/roadmap.md|roadmap.md]] — end-of-return **`queue_continuation`** block.
- Config: [[3-Resources/Second-Brain-Config|Second-Brain-Config]] § **queue_continuation**.
