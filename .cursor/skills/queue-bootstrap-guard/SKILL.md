---
name: queue-bootstrap-guard
description: Optional Layer 0 preflight — ensure dirname(PQ) exists and create an empty prompt-queue file when missing. No JSONL payload; no RESUME_ROADMAP synthesis. A.1b in queue.mdc owns bootstrap lines. Neutral Watcher-Result only when observability is needed.
---

# queue-bootstrap-guard

## When to use

- **Optional** — when tooling or hosts require **PQ** to exist on disk before Layer 1 reads it, but the contract is still **empty input** until **A.1b** may append a line.
- **Inputs:** Vault-relative **`pq_path`** (e.g. **`.technical/prompt-queue.jsonl`** or **`resolved_prompt_queue_path`** from **`## parallel_context`** in the Layer 0→1 hand-off per [[.cursor/rules/always/dispatcher.mdc|dispatcher.mdc]]), **`vault_root`**.
- **Not a substitute** for [[.cursor/rules/agents/queue.mdc|queue.mdc]] **A.1b** empty-queue continuation bootstrap.

## Instructions

1. **Resolve path:** Use **`pq_path`** as given (vault-relative). Do **not** infer **`project_id`** or lane from file contents — this skill **does not parse** the queue file.

2. **Ensure parent directory:** Create **`dirname(pq_path)`** if missing (e.g. `obsidian_ensure_structure` with **`folder_path`** = parent, or host-safe directory create). No shell **`rm`** / **`cp`** on vault paths per [[.cursor/rules/always/core-guardrails.mdc|core-guardrails]].

3. **Missing file only:** If **`pq_path`** does **not** exist, create an **empty** file at that path (zero bytes **or** a single newline only). **Do not** write JSON, **`RESUME_ROADMAP`**, **`mode`**, **`id`**, or any queue entry — **forbidden.** Bootstrap line synthesis stays in **A.1b** only.

4. **If file exists:** Do **not** overwrite or truncate. Read is **not** required for this skill; optional existence check only.

5. **Watcher-Result (optional):** If the operator wants a trace that the shell was created, append **one** neutral line to **`3-Resources/Watcher-Result.md`** — use canonical path per [[.cursor/rules/always/watcher-result-append.mdc|watcher-result-append]] (or mirrors when parallel applies). Example shape:
   - `requestId: queue-bootstrap-guard | status: success | message: "ensured empty PQ path exists" | trace: "<pq_path>" | completed: <ISO8601>`
   - Keep **`message`** / **`trace`** parse-safe; no loud or alarm copy.

6. **Delegation boundary:** **Never** synthesize **`RESUME_ROADMAP`** or call **`Task(roadmap)`** from this skill. After ensure, proceed with normal **`Task(queue)`** hand-off per dispatcher.

## Forbidden

- Writing a hardcoded or lane-guessed JSONL seed line.
- Parsing queue lines to choose **`project_id`** or **`params`**.

## Reference

- [[.cursor/rules/agents/queue.mdc|queue.mdc]] **A.1**, **A.1b**
- [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]] § Empty-queue bootstrap
- [[.cursor/agents/queue.md|agents/queue.md]] Return — Prompt-queue empty guard
