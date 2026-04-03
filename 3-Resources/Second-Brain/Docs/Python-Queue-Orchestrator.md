---
title: Python queue orchestrator (eat_queue_core)
created: 2026-04-04
tags:
  - second-brain
  - eat-queue
  - queue
  - layer1
para-type: Resource
status: reference
source: "Phase 3 bridge — deterministic plan + Layer 1 Task dispatch"
---

# Python queue orchestrator

Deterministic **`eat_queue_run_plan.json`** is produced by the **`scripts/eat_queue_core`** package (`python -m eat_queue_core plan`). Layer 1 (Queue subagent) may **consume** that file when [[3-Resources/Second-Brain/Second-Brain-Config|Second-Brain-Config]] **`queue.python_orchestrator_enabled`** is **`true`**. See [[.cursor/rules/agents/queue.mdc|queue.mdc]] **A.0.5**.

## Pre-run hook (recommended)

From the vault root, generate the plan **before** EAT-QUEUE. If `plan` exits non-zero, **stop** and fix the queue or plan; do not invoke **`Task(queue)`** with a stale or missing manifest.

**Reactive full cycle (Pass 3 drain / `queue_rewrite_ids`):** Prefer **`python3 -m scripts.eat_queue_core.full_cycle`** (repo root, **`PYTHONPATH=.`**) with **`--action`**, **`--profile`**, **`--max-passes=2`** — see [[.cursor/rules/agents/queue.mdc|queue.mdc]] **A.0.5**. Re-invoke after Layer 1 mid-run repair append when pass 1 had no Pass 3 intents.

```bash
python -m eat_queue_core plan \
  --queue .technical/prompt-queue.jsonl \
  --emit .technical/eat_queue_run_plan.json \
  --parent-run-id "$(date +eatq-%Y%m%dT%H%M%SZ)" \
  --verbose && echo "✅ Plan ready – now invoke EAT-QUEUE / Task(queue)"
```

Requires: `pip install -r scripts/eat_queue_core/requirements.txt` and `PYTHONPATH=scripts` (or equivalent) so `eat_queue_core` resolves.

## Testing the bridge

First runs should keep **`python_orchestrator_enabled: false`** in Config and validate **`eat_queue_core plan`** output only. Flip the flag to **`true`** only after you confirm **one clean repair cycle** end-to-end (plan → EAT-QUEUE → Watcher-Result → queue rewrite).

```bash
# Generate plan (from vault root)
PYTHONPATH=scripts python3 -m eat_queue_core plan \
  --queue .technical/prompt-queue.jsonl \
  --emit .technical/eat_queue_run_plan.json \
  --parent-run-id "eatq-$(date +%Y%m%dT%H%M%SZ)" \
  --verbose

# Then run EAT-QUEUE / Task(queue) as usual
```

## When to enable `python_orchestrator_enabled`

Keep **`false`** (default) until you have **tested a full EAT-QUEUE cycle** with the repair scenario and confirmed Watcher-Result / queue rewrite behavior. Then set **`true`** in Second-Brain-Config under the **`queue:`** block (see machine-readable YAML in Config).

## Safety

- **Flag off** or **plan file missing** → Layer 1 uses **legacy** LLM-driven ordering (**A.1** onward); no breaking change.
- **Flag on** and plan present → Layer 1 must follow **A.0.5** in `queue.mdc` (exact **`intents`** order; no overriding **`queue_pass_phase`**, **`pass_id`**, or **`dispatch_ordinal`** from the manifest).

## Related

- [[Queue-Sources|Queue-Sources]] — prompt queue contract
- [[Subagent-Safety-Contract|Subagent-Safety-Contract]] — Task hand-off
