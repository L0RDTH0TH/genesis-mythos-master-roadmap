---
title: Run-Telemetry — Layer 1 queue dispatch (gmm recal host fallback)
created: 2026-03-22
tags: [run-telemetry, queue, genesis-mythos-master]
---

# Queue EAT-QUEUE — 2026-03-22

| Field | Value |
|-------|-------|
| actor | layer1_queue |
| project_id | genesis-mythos-master |
| queue_entry_id | gmm-post-a1b-deepen-recal-20260322T123500Z |
| parent_run_id | l1-eatq-20260322-gmm-recal |
| timestamp | 2026-03-22T18:35:00.000Z |

## Summary

- Step 0 wrappers: no `approved: true` wrappers under `Ingest/Decisions/`.
- **Dispatch:** `Task(subagent_type: roadmap)` **failed** (invalid enum on host).
- **Fallback:** `Task(subagent_type: generalPurpose)` with full RoadmapSubagent hand-off — **invoked_ok**.
- **Post–little-val:** skipped (no `validator` Task type on host).
- **A.7:** Consumed recal line; appended follow-up `gmm-deepen-post-recal-20260322T1830Z` (RESUME_ROADMAP deepen).

## dispatch_ledger (ordered)

1. `dispatch_pipeline` | `subagent_type_requested`: roadmap | `outcome`: task_error | `host_error_raw`: Invalid enum value (Expected generalPurpose \| explore \| shell \| best-of-n-runner)
2. `dispatch_pipeline` | `subagent_type_requested`: generalPurpose | `outcome`: invoked_ok | `queue_entry_id`: gmm-post-a1b-deepen-recal-20260322T123500Z
3. `post_little_val_validator` | `outcome`: skipped | `reason`: host_enum_missing / synthetic validator_context only
