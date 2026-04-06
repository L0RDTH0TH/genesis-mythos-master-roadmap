---
description: "When queue has more than 3 entries (or configurable threshold), optionally escalate to batch mode with previews. Append to Mobile-Pending-Actions a proposal; user confirms by running EAT-QUEUE with BATCH-DISTILL or BATCH-EXPRESS."
globs: []
alwaysApply: false
---

# Auto-async-cascade (context rule)

- **Purpose**: When the queue processor sees **>3 entries** (or a configurable threshold from Second-Brain-Config), optionally **escalate to batch mode** with previews: append to [Mobile-Pending-Actions](3-Resources/Mobile-Pending-Actions.md) a line such as "Batch run proposed: N notes; run EAT-QUEUE with BATCH-DISTILL to apply." The user confirms by running EAT-QUEUE with that mode (or ignores and processes entries one-by-one).
- **Reference**: [auto-eat-queue](.cursor/rules/context/auto-eat-queue.mdc), [Queue-Sources](3-Resources/Second-Brain/Queue-Sources.md), [Feedback-Log](3-Resources/Feedback-Log.md). Overlap detection and merge stats can be logged to Feedback-Log.

## How to activate

- **Context**: Invoked during EAT-QUEUE when the queue has more than the threshold (e.g. 3) valid entries. Optional: only when a majority of entries are DISTILL or EXPRESS mode so batch is meaningful.

## Behavior

1. **Count**: After parse/validate/dedup, if valid entry count > threshold (e.g. 3), consider cascade.
2. **Propose**: Append to Mobile-Pending-Actions a short line: e.g. "Batch run proposed: N notes (DISTILL/EXPRESS); run EAT-QUEUE with BATCH-DISTILL or BATCH-EXPRESS to apply. Or process entries individually."
3. **No auto-batch**: Do not automatically switch to BATCH-DISTILL/BATCH-EXPRESS; the user must explicitly run with that mode. This rule only **proposes** and **informs**.
4. **Log**: Optionally log "cascade proposed: N entries" to Feedback-Log.md for analytics.

## Config

- **Threshold**: Document in Queue-Sources or Second-Brain-Config (e.g. cascade_threshold: 3). Default 3 if not set.

## Exclusions

Does not apply when queue is empty or has 1–3 entries (unless threshold is lower). Does not override user intent: if user already sent BATCH-DISTILL in the queue, process as usual.
