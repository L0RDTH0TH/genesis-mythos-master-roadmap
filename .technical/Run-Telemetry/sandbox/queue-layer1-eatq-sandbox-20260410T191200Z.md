---
title: Queue Layer 1 EAT-QUEUE sandbox
created: 2026-04-10
tags: [run-telemetry, eat-queue, sandbox]
---

# Run telemetry — EAT-QUEUE lane sandbox

| Field | Value |
|-------|--------|
| actor | queue (Layer 1) |
| project_id | sandbox-genesis-mythos-master |
| queue_entry_id | followup-ha-exec-p1-233000z-chain-l1-gate-20260410T182600Z |
| parent_run_id | eatq-sandbox-20260408-p1 |
| parallel_track | sandbox |
| PQ | .technical/parallel/sandbox/prompt-queue.jsonl |
| pool_sync | copied_count=0 preserved_lane_only=3 written_line_count=3 |
| dispatches | Task(roadmap)=1 Task(validator)=1 (L1 post-little-val b1) |
| A.3 | Dedup (mode,prompt,source_file): single dispatch — earliest timestamp |
| A.7 | Consumed id + appended queue_followups.next_entry |
| final_PQ_line_count | 3 |
| nested_validation_passed | true |
| intent_actual_receipt | provisional_success (rollup gates open) |

## layer0_queue_signals

```yaml
no_gain_terminal: false
break_spin_zero_alternates: false
```
