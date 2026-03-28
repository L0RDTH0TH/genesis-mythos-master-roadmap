---
title: Queue audit log (prompt-queue movement)
created: 2026-03-29
tags: [second-brain, queue, observability, audit]
para-type: Resource
status: active
links:
  - "[[3-Resources/Second-Brain/Queue-Sources]]"
  - "[[3-Resources/Second-Brain-Config]]"
  - "[[3-Resources/Second-Brain/Docs/Queue-Continuation-Spec|Queue-Continuation-Spec]]"
  - "[[.cursor/rules/agents/queue.mdc|agents/queue.mdc]]"
---

# Queue audit log spec

## Purpose

Durable **movement trace** for `.technical/prompt-queue.jsonl`: when a line is **removed** (consumed) or **appended** during EAT-QUEUE, append a record to **`.technical/prompt-queue-audit.jsonl`**. This is **not** a substitute for [[3-Resources/Second-Brain/Docs/Queue-Continuation-Spec|Queue-Continuation-Spec]] (bootstrap / suppress_followup semantics) or [[3-Resources/Watcher-Result|Watcher-Result]] (outcome one-liners). It preserves **payload snapshots**, **disposition**, **spawn graph**, and **timing** for operators and agents.

## Writer and gate

- **Writer:** Queue/Dispatcher (Layer 1), prompt-queue flow only.
- **Config:** [[3-Resources/Second-Brain-Config|Second-Brain-Config]] § `queue.audit_log_enabled` (default **true**). When **false**, skip all audit appends.
- **Path:** `queue.audit_log_path` (default `.technical/prompt-queue-audit.jsonl`).
- **I/O:** **read-then-append** one JSON object per line (JSONL); **never** rewrite or truncate the audit file in Layer 1.

## Schema version 1

Every record **must** include `schema_version: 1` and `event`.

### Event: `line_removed`

Emitted when a queue line is **omitted** from the rewritten `prompt-queue.jsonl` because it was successfully processed (id in `processed_success_ids`), including tiered-policy consumption after A.5b repair append.

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `schema_version` | yes | int | `1` |
| `event` | yes | string | `line_removed` |
| `eat_queue_run_id` | yes | string | Stable id for **one** EAT-QUEUE invocation (UUID preferred, or `queue-eat-<ISO8601>`). Repeated on all audit rows in that pass. |
| `queue_entry_id` | yes | string | The consumed line’s `id`. |
| `disposition_completed_iso` | yes | string | UTC ISO 8601 when Layer 1 **finished** disposition for this entry (after pipeline + post–little-val + A.5b/A.5c as applicable). |
| `disposition` | yes | string | See **Disposition enum** below. |
| `payload` | if `audit_log_payload_mode: full` | object | Full parsed queue entry object (clone before strip of internal-only fields if any). |
| `payload_metadata` | if `audit_log_payload_mode: metadata_only` | object | Subset: `mode`, `id`, `project_id` (from params or inferred), `source_file`, top-level `params` keys only (values may be truncated strings ≤500 chars in implementation). |
| `payload_timestamp_utc` | if present on line | string | Copy queue entry’s optional `timestamp` (UTC). |
| `payload_local_timestamp` | if present on line | string | Copy optional `local_timestamp`. |
| `dispatch_started_iso` | recommended | string | When Layer 1 began dispatch for this entry (before `Task` for pipeline). |
| `dispatch_completed_iso` | recommended | string | When pipeline + post–little-val steps completed for this entry. |
| `duration_ms_dispatch` | optional | number | Milliseconds between dispatch start and end when both timestamps set. |
| `parent_run_id` | optional | string | Layer 1 / hand-off correlation when known. |
| `spawned_line_ids` | optional | array of string | New line `id`s appended this run tied to this entry (A.5b repair, A.5c `next_entry`, merged follow-ups). |
| `watcher_linked` | optional | bool | `true` if a Watcher-Result line with `requestId` = `queue_entry_id` is expected for this consumption. |

### Event: `line_appended`

Emitted when Layer 1 **appends** a new line to `prompt-queue.jsonl` during the run (repair, follow-up, bootstrap, etc.). **Recommended** whenever `audit_log_enabled` is true so the graph is complete.

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `schema_version` | yes | int | `1` |
| `event` | yes | string | `line_appended` |
| `eat_queue_run_id` | yes | string | Same as the current EAT-QUEUE pass. |
| `queue_entry_id` | yes | string | The **new** line’s `id`. |
| `appended_iso` | yes | string | UTC ISO 8601 when the append was written. |
| `trigger` | yes | string | `layer1_a5b_repair` \| `layer1_a5c_followup` \| `layer1_a5c1_synthesized` \| `roadmap_queue_followups` \| `empty_queue_bootstrap` \| `operator_read_append` \| `other` |
| `parent_queue_entry_id` | optional | string | Consuming or triggering entry id (e.g. repair parent). |
| `payload` or `payload_metadata` | per `audit_log_payload_mode` | object | Same rules as `line_removed`. |

### Disposition enum (`line_removed`)

| Value | Meaning |
|-------|---------|
| `success_consumed` | Normal success; line removed from active queue. |
| `consumed_post_little_val_with_repair` | Original entry consumed per A.7 tiered policy because A.5b appended a repair line. |
| `success_consumed_chain` | Chain entry fully completed (if distinct logging desired). |
| `consumed_forward_slot` | Roadmap line consumed as a **forward-class** initial-slot dispatch under **`forward_first`** (see `queue.mdc` A.4c). |
| `consumed_repair_drain` | Roadmap line consumed in the **cleanup** pass (repair drain). |
| `consumed_inline_repair_drain` | Roadmap line consumed in **Pass 3** (**inline** repair drain after **A.5b** / repair-class **A.5d** append). |

**Optional on `line_removed`:** **`queue_pass_phase`**: `initial` \| `cleanup` \| `inline` — which pass consumed the line.

### Event: `entry_skipped_no_dispatch`

Emitted when Layer 1 **stall-skips** a line (**A.5.0**) without calling **`Task`**.

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `schema_version` | yes | int | `1` |
| `event` | yes | string | `entry_skipped_no_dispatch` |
| `eat_queue_run_id` | yes | string | Current EAT-QUEUE pass id. |
| `queue_entry_id` | yes | string | Skipped line’s `id`. |
| `skipped_iso` | yes | string | UTC ISO 8601 when skip was recorded. |
| `reason` | yes | string | e.g. `hard_block_stall` |
| `queue_pass_phase` | optional | string | `initial` \| `cleanup` \| `inline` |
| `payload_metadata` | optional | object | Per `audit_log_payload_mode`. |

**Note:** Lines that remain in the file with `queue_failed: true` are **not** removed; by default **do not** emit `line_removed` for them unless an implementation explicitly logs a `line_retained_failed` extension in a future schema version.

## Invariants

1. **Append-only:** Never delete or edit prior audit lines from Layer 1.
2. **One `eat_queue_run_id` per EAT-QUEUE pass:** Generate at start of prompt-queue processing (after A.2 parse begins or first valid entry); reuse for every audit row in that pass.
3. **PII / size:** `full` payload may include long `user_guidance`; acceptable for vault-local audit. Use `metadata_only` when storage is a concern.
4. **Cross-check:** `disposition_completed_iso` should align with Watcher-Result `completed` for the same `requestId` (allow small skew for ordering).

## Retention

File grows without bound. Rotate or archive periodically (e.g. [[.cursor/skills/log-rotate/SKILL|log-rotate]] or manual copy to `4-Archives/`). See [[3-Resources/Second-Brain/Logs|Logs]].

## Related

- [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]] — queue entry optional `timestamp` / `local_timestamp`.
- [[3-Resources/Watcher-Result|Watcher-Result]] — per-entry outcome line.
