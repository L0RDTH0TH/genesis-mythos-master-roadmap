---
title: Python queue orchestrator (eat_queue_core)
created: 2026-04-04
updated: 2026-04-14
tags:
  - second-brain
  - eat-queue
  - queue
  - layer1
para-type: Resource
status: reference
source: "Deterministic EQPLAN + Layer 1 Task dispatch (harness migration)"
---

# Python queue orchestrator

Deterministic **`eat_queue_run_plan.json`** (**EQPLAN**) is produced and consumed by **`scripts/eat_queue_core`**. Layer 1 **must** use the **harness** CLI — see [[3-Resources/Second-Brain/Docs/Queue-Harness-Architecture|Queue-Harness-Architecture]] — with **`queue.python_orchestrator_enabled: true`** in [[3-Resources/Second-Brain/Docs/Core/Second-Brain-Config|Second-Brain-Config]] (machine-readable **`queue:`** block). There is **no** supported path where Layer 1 assigns dispatch order from a raw **PQ** read without **EQPLAN** (except **queue.mdc** **A.1 → A.2** after empty **`intents`** for **A.1b** visibility).

## CLI entry point

Prefer the unified harness:

```bash
PYTHONPATH=. python3 -m scripts.eat_queue_core.harness full_cycle --vault-root . ...
PYTHONPATH=. python3 -m scripts.eat_queue_core.harness plan --emit .technical/eat_queue_run_plan.json ...
```

Legacy **`python3 -m eat_queue_core plan`** (with **`PYTHONPATH=scripts`**) remains compatible where documented in tests; new operator docs reference **`harness`**.

## Central pool hydration (`pool_sync`)

When **`queue.central_pool_fanout_enabled`** is **`true`** and **`full_cycle`** runs with **`--lane`** and **`--queue`** pointing at a **per-track** `prompt-queue.jsonl`, **`run_full_eat_queue_cycle`** **merges** the lane-filtered central pool into the track file before planning (same filter as Layer 1 **A.2a**), **preserving lane-only** rows unless **`queue.pool_sync_strict_central_only`** is **`true`**. With **`--apply-cleanup`**, consumed ids are removed from **both** the track **PQ** and the central pool (`apply_queue_cleanup_dual_track`).

Layer 1 runs **`harness pool_sync`** per **A.0.4** when fanout is enabled (or standalone **`pool_sync`** module — equivalent hydration).

## Pre-run ritual (normal EAT-QUEUE)

1. From vault root, run **`harness full_cycle`** (or **`plan`** when debugging) so **EQPLAN** is **fresh** for the current **PQ** bytes and lane filter. If the command exits non-zero, **stop** and fix the queue or config; do not invoke **`Task(queue)`** with a stale or missing manifest when the plan is required for dispatch.
2. Invoke **EAT-QUEUE** / **`Task(queue)`** as usual. Layer 1 executes **`intents`** in array order.

```bash
PYTHONPATH=. python3 -m scripts.eat_queue_core.harness plan \
  --vault-root . \
  --emit .technical/eat_queue_run_plan.json \
  --parent-run-id "eatq-$(date +%Y%m%dT%H%M%SZ)" \
  --lane sandbox \
  --verbose
```

Requires: `pip install -r scripts/eat_queue_core/requirements.txt` and **`PYTHONPATH=.`** at repo root for **`scripts.eat_queue_core`**.

## `queue_rewrite_ids` and Pass 3

Plans emitted by **`full_cycle`** / enriched manifests should include **`queue_rewrite_ids`** = **`consumed_ids`** ∪ Pass 3 repair **`queue_entry_id`** values so repair lines do not leak to the next run. **`harness rewrite_consumed --plan <EQPLAN>`** applies the same id set as **A.7**.

## Post–A.7 GitForge (`post_queue_gitforge`)

After **A.7** (and optional telemetry summary per **queue.mdc**), balance/quality runs invoke **`python3 -m scripts.eat_queue_core.harness post_queue_gitforge`** — not part of **EQPLAN** — with JSON hand-off and optional **`--parallel-context-file`**. See [[3-Resources/Second-Brain/Docs/Queue-Harness-Architecture|Queue-Harness-Architecture]] § GitForge harness.

## Safety

- **EQPLAN missing / unreadable** → Layer 1 **Watcher-Result** advisory + regenerate via **`harness full_cycle`** — **do not** invent ordering from **PQ** alone.
- **`harness verify`** (optional) + **`queue.mutation_recovery_mode`** handle external **PQ** byte drift; see Queue-Harness-Architecture.

## Related

- [[Queue-Harness-Architecture|Queue-Harness-Architecture]] — sequence, mutation recovery
- [[Queue-Sources|Queue-Sources]] — prompt queue contract
- [[Subagent-Safety-Contract|Subagent-Safety-Contract]] — Task hand-off
