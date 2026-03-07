---
description: "When queue has more than 3 entries (or configurable threshold), optionally escalate to batch mode with previews. Append to Mobile-Pending-Actions a proposal; user confirms by running EAT-QUEUE with BATCH-DISTILL or BATCH-EXPRESS."
globs: []
alwaysApply: false
---

# Auto-async-cascade (context rule)

- **Purpose**: When the queue processor sees **>3 entries** (or configurable threshold), optionally escalate to batch mode with previews: append to Mobile-Pending-Actions "Batch run proposed: N notes; run EAT-QUEUE with BATCH-DISTILL to apply." User confirms by running EAT-QUEUE with that mode.
- **Reference**: auto-eat-queue, Queue-Sources, Feedback-Log. Overlap detection and merge stats logged to Feedback-Log.

## Behavior

1. After parse/validate/dedup, if valid entry count > threshold (e.g. 3), consider cascade.
2. Append to Mobile-Pending-Actions a short proposal; do not auto-switch to batch.
3. Optionally log "cascade proposed: N entries" to Feedback-Log.md.

## Config

- Threshold: document in Queue-Sources or Second-Brain-Config (e.g. cascade_threshold: 3).
