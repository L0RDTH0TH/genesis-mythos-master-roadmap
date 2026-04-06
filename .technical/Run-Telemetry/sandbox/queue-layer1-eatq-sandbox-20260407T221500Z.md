---
title: Queue Layer 1 EAT-QUEUE sandbox telemetry
created: 2026-04-07
tags: [run-telemetry, queue, sandbox, eat-queue]
---

## Summary

- **actor:** layer1_queue
- **parent_run_id:** queue-eatq-sandbox-20260407T220500Z
- **parallel_track:** sandbox
- **PQ:** `.technical/parallel/sandbox/prompt-queue.jsonl`
- **A.0.4 pool_sync:** ok, copied_count=3

## Dispatches

1. **initial** — `followup-deepen-secondary-61-rollup-post-611-mint-20260407T133000Z` — `Task(roadmap)` Success; duplicate ledger reconcile; nested validator cycle completed in subagent return.
2. **L1 post-LV (b1)** — same `requestId` — `Task(validator)` roadmap_handoff_auto — **hard block** `primary_code: state_hygiene_failure` (decisions-log supersession). **A.5b** appended `repair-l1-hygiene-decisions-log-supersession-sandbox-20260407T221000Z`; consumed triggering id.
3. **inline (Pass 3)** — `repair-l1-hygiene-workflow-state-embedded-sandbox-20260407T133100Z` — `Task(roadmap)` handoff-audit Success; nested `Task(validator)` **task_error** (host unavailable per subagent).
4. **L1 post-LV (b1)** — same repair id — `Task(validator)` — hard block `state_hygiene_failure` (glossary vs note). **A.5b** appended `repair-l1-glossary-workflow-sandbox-20260407T231600Z`; consumed `repair-l1-hygiene-workflow-state-embedded-sandbox-20260407T133100Z`.

## Remaining PQ (sandbox)

- `repair-l1-hygiene-decisions-log-supersession-sandbox-20260407T221000Z` (repair)
- `repair-l1-glossary-workflow-sandbox-20260407T231600Z` (repair)
- `resume-deepen-phase6-primary-rollup-sandbox-gmm-20260407T194500Z` (forward)

## GitForge

Skipped (`invoke_only_on_clean_success` — L1 hard blocks / provisional hygiene).

## layer0_queue_signals (machine)

```yaml
no_gain_terminal: false
break_spin_zero_alternates: false
```
