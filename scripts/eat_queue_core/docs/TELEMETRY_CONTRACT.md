# EAT-QUEUE harness telemetry (eat_queue_core)

Harness-only contract for **audit JSONL**, **task-handoff-comms**, and **Watcher-Result** lines emitted by `scripts/eat_queue_core/` (`append_entries`, `pool_sync` dedupe, `full_cycle` plan pass). Queue agent rules are unchanged; operators drive behavior via CLI and normal EAT-QUEUE cycles.

## Emission points

| Surface | Path (typical) | Record types / role |
|--------|----------------|---------------------|
| Audit JSONL | `{technical_bundle_root}/prompt-queue-audit.jsonl` | `a5b_enqueue_dedupe`, `pool_sync_dedupe` |
| Comms | `{technical_bundle_root}/task-handoff-comms.jsonl` | `intent_actual_receipt` (append_entries / plan) |
| Watcher | `3-Resources/Watcher-Result.md` (or `parallel_execution.watcher.canonical_path`) | One line per telemetry event; `trace` holds JSON |

## Audit rows (`a5b_enqueue_dedupe`)

- `queue_entry_id`, `dedupe_attempted`, `dedupe_suppressed`, `suppressed_by` (human-oriented enum: `origin_id`, `fuzzy_guidance`, `none`, …)
- `audit_suppressed_by` — machine-stable string when suppressed, e.g. `a5b_dedupe_jaccard_origin`
- `inline_drain_budget_remaining`, `max_inline_a5b_effective`, `pass3_repair_count_used`
- `parent_run_id`, optional `origin_request_id`

## Audit rows (`pool_sync_dedupe`)

- `record_type: pool_sync_dedupe`
- Per suppressed line: `queue_entry_id`, `suppressing_queue_entry_id`, `audit_suppressed_by`, counts aligned with `dedupe_entries` output

## task-handoff-comms (`intent_actual_receipt`)

- Top-level fields include `queue_entry_id`, `parallel_track`, `queue_lane`, `inline_drain_budget_remaining` when applicable
- `body` JSON: `dedupe_*`, `audit_suppressed_by`, `provisional_reason` when used

## Watcher-Result line shape

Format (single line, parse-safe):

```text
requestId: <id> | status: success | failure | message: "..." | trace: "..." | completed: <ISO8601>
```

### `trace` payload keys (non-exhaustive)

- `source`: `eat_queue_core_append_entries` | `eat_queue_core_full_cycle`
- `record_type`: `harness_append_telemetry` | `intent_actual_receipt`
- `queue_entry_id`, `parent_run_id`, `parallel_track`, `queue_lane`
- `dedupe_attempted`, `dedupe_suppressed`, `suppressed_by`, `audit_suppressed_by`
- `inline_drain_budget_remaining`, `max_inline_a5b_effective`, `pass3_repair_count_used`
- `provisional_reason` (plan / option-evaluation paths)

**Invariant:** `trace` must be **single-line JSON** with internal quotes escaped so the fixed `message | trace | completed` layout is not broken. No raw newlines inside `trace`.

## Conservative timestamp fallback (origin window)

When a queue entry has **no** parseable `timestamp` / `effective_ts` / `params.timestamp` (and no reliable time embedded in `id`), the harness treats that side of the pair as **in-window** for origin-window dedupe. Legacy PQ lines without timestamps therefore do **not** get false-negative suppression from the window filter; dedupe still applies when the same `origin_request_id` and fuzzy-matched guidance align within the compared set.

## Common mistakes

| Mistake | What happens | Fix |
|--------|----------------|-----|
| Pasting **`grep`** / **`--inline-grep`** on the same line as `append_entries` | Confusing errors or wrong tool | Two commands: `append_entries` (heredoc / `--lines-file`), then `grep` alone |
| Running `append_entries` with no stdin and no `--lines-file` | `append_entries_stdin_required` | Use heredoc, pipe, or `--lines-file` |
| Expecting `parallel-context.yaml` when it was never created | stderr: synthetic defaults for lane | Normal; use `--lane godot` or add the YAML |

Shell helper (vault root): `scripts/eat_queue_core/examples/preflight_godot_append_dryrun.sh`

## Operator verification (short)

1. **Parallel context:** If `.technical/parallel/<lane>/parallel-context.yaml` is absent, pass **`--lane godot`** (or sandbox, etc.) so the harness synthesizes `parallel_track` and `resolved_prompt_queue_path` (stderr notes when a `--parallel-context-file` path was missing). Alternatively set **`--queue .technical/parallel/godot/prompt-queue.jsonl`** explicitly.
2. `harness snapshot --lane godot` → JSON file; `append_entries --require-snapshot-json` before mutating PQ.
3. `grep -E 'dedupe_suppressed|inline_drain_budget_remaining' 3-Resources/Watcher-Result.md`
4. `grep pool_sync_dedupe .technical/parallel/<track>/prompt-queue-audit.jsonl`

**Dry-run append (no PQ writes):** pipe one JSONL object on stdin, use **`--lines-file`**, or a **heredoc**. Running `append_entries` in an interactive shell **without** stdin or `--lines-file` exits immediately with `append_entries_stdin_required` (avoids blocking on empty TTY). Keep **`snapshot`** and **`grep`** on separate lines—do not concatenate commands.

```bash
PYTHONPATH=. python3 -m scripts.eat_queue_core.harness append_entries --vault-root . --lane godot --dry-run <<'EOF'
{"id":"dry-test-1","mode":"HANDOFF_AUDIT_REPAIR","params":{"origin_request_id":"o-test","user_guidance":"sample"}}
EOF
```
