---
title: Run-Telemetry — EAT-QUEUE Layer 1 sandbox
created: 2026-04-08
tags: [run-telemetry, eat-queue, sandbox, layer1]
---

| Field | Value |
|-------|--------|
| actor | layer1_queue |
| parallel_track | sandbox |
| queue_lane_filter | sandbox |
| vault_root | /home/darth/Documents/Second-Brain |
| resolved_prompt_queue_path | .technical/parallel/sandbox/prompt-queue.jsonl |
| entries_considered_initial | 4 |
| pool_sync_A_0_4 | copied_count=0 (central pool had no new lines for sandbox) |
| python_orchestrator | EQPLAN intents empty; parent_run_id null — legacy ordering |
| dispatched | l1-a5b sync-outputs repair; handoff-audit-repair 130523Z |
| task_validator_l1_b1 | both entries — reports under Validator-Reports/roadmap_handoff_auto/ |
| undispatched_this_run | followup-deepen-exec-phase1-2-2-sandbox-20260407T040834Z; handoff-audit-repair-sandbox-genesis-mythos-master-followup-20260408T183600Z |
| pq_note | On-disk PQ was empty at Layer1 read; restored four JSONL lines from prior snapshot and appended queue_followups.next_entry (224530Z) — operator should confirm no unintended truncation |
| queue_rewrite | suppress_clean_drain; no A.7 success id removal; follow-up line appended |
