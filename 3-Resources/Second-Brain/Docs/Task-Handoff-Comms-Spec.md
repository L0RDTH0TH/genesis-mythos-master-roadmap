---
title: Task hand-off and agent comms log (spec)
created: 2026-03-22
tags: [second-brain, subagents, observability, task-tool]
para-type: Resource
status: active
links:
  - "[[3-Resources/Second-Brain/Subagent-Safety-Contract|Subagent-Safety-Contract]]"
  - "[[3-Resources/Second-Brain/Logs|Logs]]"
---

# Task hand-off and agent comms log

**Version:** `schema_version: 1`

**Canonical store:** `.technical/task-handoff-comms.jsonl` (append-only JSONL, one JSON object per line).

**Purpose:** Durable **verbatim** record of **Cursor `Task`** hand-offs and returns for orchestration (Layer 0 → Layer 1 → Layer 2 → nested helpers). This is **not** a replacement for [[3-Resources/Second-Brain/Logs#Run-Telemetry|Run-Telemetry]] (per-run metrics and nested ledger in notes), [[3-Resources/Watcher-Result|Watcher-Result]] (one-line UX), or **`nested_subagent_ledger`** (structured attestation in pipeline returns). All may coexist; **task-handoff-comms** is the **full transcript** of Task `prompt` and subagent return text.

**Config:** When [[3-Resources/Second-Brain-Config|Second-Brain-Config]] **`task_handoff_comms.enabled`** is **`false`**, agents **omit** appends to this file (rules still describe the contract).

---

## Scope (normative)

Log **every** orchestration-relevant **`Task`** invocation:

| Caller | Callee | Notes |
|--------|--------|--------|
| Layer 0 (chat) | Layer 1 `Task(queue)` | Per [[.cursor/rules/always/dispatcher.mdc|dispatcher.mdc]] |
| Layer 1 (Queue) | Pipeline subagents (`roadmap`, `ingest`, …) | Same `task_correlation_id` as **`pipeline_task_correlation_id`** in the hand-off |
| Layer 1 | Post–little-val `Task(validator)` | New `task_correlation_id` per invocation |
| Layer 1 | `Task(prompt_craft)` | New `task_correlation_id` per invocation |
| Layer 2 (pipeline) | `Task(validator)`, `Task(internal-repair-agent)`, `Task(research)` | **Required**; set **`parent_task_correlation_id`** = **`pipeline_task_correlation_id`** from the pipeline hand-off |

**No opt-out** for whitelisted nested helpers when the pipeline invokes them.

---

## Write model

For **each** `Task` call, append **two** lines to `.technical/task-handoff-comms.jsonl` (in order):

1. **`record_type: "handoff_out"`** — immediately **before** invoking `Task`: full **`prompt`** string the caller passes (after sanitization).
2. **`record_type: "return_in"`** — immediately **after** `Task` returns (or fails): full return message or **sanitized** host/tool error text.

Both lines share the same **`task_correlation_id`** (new UUID per `Task` invocation).

**Layer 1 → Layer 2:** The correlation id for that dispatch **must** appear in the mandatory hand-off telemetry as **`pipeline_task_correlation_id`** (see [[3-Resources/Second-Brain/Subagent-Safety-Contract|Subagent-Safety-Contract]]) so the pipeline can copy it onto every nested helper comms row as **`parent_task_correlation_id`**.

---

## Record schema (JSON object per line)

| Field | Type | Required | Notes |
|-------|------|----------|--------|
| `schema_version` | int | yes | Currently `1` |
| `task_correlation_id` | string | yes | UUID for this `Task` pair |
| `parent_task_correlation_id` | string \| null | conditional | **Required** on both records of a **nested helper** `Task` (L2→helper): equals **`pipeline_task_correlation_id`** from the L1→L2 hand-off. **`null`** or omit for L0→L1 and L1→L2 **top-level** dispatches |
| `record_type` | string | yes | `handoff_out` \| `return_in` |
| `iso_timestamp` | string | yes | ISO 8601 when the record is written |
| `from_actor` | string | yes | e.g. `layer0_chat`, `layer1_queue`, `layer2_roadmap`, `layer2_ingest`, `helper_validator`, … |
| `to_actor` | string | yes | Target role or `subagent_type` label for the callee |
| `subagent_type` | string | yes | Cursor `Task` `subagent_type` value (e.g. `queue`, `roadmap`, `validator`, `internal-repair-agent`, `research`, `prompt_craft`) |
| `queue_entry_id` | string | yes | From queue entry `id`, or `"-"` when no queue entry (e.g. some L0 paths) |
| `parent_run_id` | string | yes | From hand-off; `"-"` if absent |
| `project_id` | string | yes | From entry or hand-off; `"-"` if N/A |
| `vault_root` | string | yes | Absolute or workspace path for the vault |
| `body` | string | yes | Verbatim prompt (`handoff_out`) or return / error (`return_in`), after sanitization |
| `sanitization_rules_applied` | string[] | yes | e.g. `["strip_secrets", "redact_home"]`; empty array if none |

**Optional (large payloads):**

| Field | Type | When |
|-------|------|------|
| `body_truncated` | boolean | Body exceeded soft cap after truncation for JSONL row |
| `body_sha256` | string | Hash of **full** pre-truncation body (hex) |
| `overflow_path` | string | Path under `.technical/Task-Comms-Overflow/` when full body written to sidecar file |

**Soft cap:** Default **512 KiB** per `body` string in the JSONL row; tunable via **`task_handoff_comms.max_body_bytes`** in Second-Brain-Config. If truncated, set `body_truncated`, `body_sha256`, and optionally write full text to **`overflow_path`** and keep excerpt in `body`.

---

## Sanitization

Align with [[3-Resources/Second-Brain/Docs/slop/Nested-Subagent-Ledger-Spec|Nested-Subagent-Ledger-Spec]] § Sanitization:

- Strip API keys, bearer tokens, long base64.
- Optionally redact home-directory paths per operator policy.
- Preserve **Cursor / Task** verbatim error text where safe (enum errors, `resource_exhausted`, etc.).

List applied rules in **`sanitization_rules_applied`**.

---

## File operations

- **Read → append one or two lines → write** the whole file (same pattern as `prompt-queue.jsonl`). Never overwrite with only new content.
- Ensure **`.technical/`** exists before first write.
- Optional: ensure **`.technical/Task-Comms-Overflow/`** exists before writing overflow files.

---

## Retention and security

- Verbatim logs may contain **sensitive** content; treat like `prompt-queue.jsonl` and backups.
- JSONL grows quickly; operators may **rotate** or archive (e.g. monthly) to `4-Archives` or external backup — user-triggered; see [[.cursor/skills/log-rotate/SKILL.md|log-rotate]] spirit.
- If `.technical` is excluded from Obsidian, Dataview will not index this file; use Cursor, CLI, or a small index note in `3-Resources` if needed.

---

## Example (minimal, two lines)

```json
{"schema_version":1,"task_correlation_id":"550e8400-e29b-41d4-a716-446655440000","parent_task_correlation_id":null,"record_type":"handoff_out","iso_timestamp":"2026-03-22T12:00:00.000Z","from_actor":"layer1_queue","to_actor":"layer2_roadmap","subagent_type":"roadmap","queue_entry_id":"q-abc","parent_run_id":"pr-xyz","project_id":"my-project","vault_root":"/path/to/vault","body":"You are now the roadmap subagent.\nTask: ...","sanitization_rules_applied":[]}
{"schema_version":1,"task_correlation_id":"550e8400-e29b-41d4-a716-446655440000","parent_task_correlation_id":null,"record_type":"return_in","iso_timestamp":"2026-03-22T12:05:00.000Z","from_actor":"layer1_queue","to_actor":"layer2_roadmap","subagent_type":"roadmap","queue_entry_id":"q-abc","parent_run_id":"pr-xyz","project_id":"my-project","vault_root":"/path/to/vault","body":"Summary: ... Success\n...","sanitization_rules_applied":[]}
```

**Nested helper** example: same `queue_entry_id` / `parent_run_id`, new `task_correlation_id`, `parent_task_correlation_id` = the `pipeline_task_correlation_id` from the L1→roadmap dispatch, `from_actor` e.g. `layer2_roadmap`, `to_actor` / `subagent_type` for `validator`.

---

## Related

- [[3-Resources/Second-Brain/Vault-Layout#Folder structure|Vault-Layout § .technical]]
- [[3-Resources/Second-Brain/Subagent-Safety-Contract|Subagent-Safety-Contract]] — hand-off template + `pipeline_task_correlation_id`
- [[.cursor/rules/agents/queue.mdc|queue.mdc]] — Layer 1 dispatch
- [[.cursor/rules/always/dispatcher.mdc|dispatcher.mdc]] — Layer 0 → Layer 1
