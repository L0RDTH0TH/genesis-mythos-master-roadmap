---
created: 2026-02-27
tags:
  - watcher
  - eat-cache
  - testing
---

# EAT-CACHE testing

Use this to verify the Watcher queue and EAT-CACHE flow. All mobile triggers append to `.technical/prompt-queue.jsonl`; the single Cursor entry prompt is **EAT-QUEUE**. After running EAT-QUEUE, the agent clears only **passed** entries; failed/skipped entries are written back with `queue_failed: true` and are skipped on the next run. Use **Clear queue** in Obsidian to wipe the queue manually.

## Mock queue

- **Sample file:** `3-Resources/prompt-queue.sample.jsonl` contains 3 lines:
  - Same `source_file` (`3-Resources/MyNote.md`) with two modes: distill, then express.
  - One duplicate (same `id` and same `prompt`+`source_file` as the first line).

## How to test

1. Copy the sample to the live queue:  
   `cp .technical/prompt-queue.sample.jsonl .technical/prompt-queue.jsonl`  
   (or paste the contents into `.technical/prompt-queue.jsonl` in Cursor.)
2. Open Watcher modal (ribbon or command "Prompt Modal"). Check **EAT-CACHE** section: **Pending** should show 3 (or 2 after dedup at read, depending on implementation).
3. Run **EAT-CACHE** (command "EAT-CACHE (copy queue to clipboard)" or modal "Copy queue"). Confirm:
   - Notice: "Pending: N" then "Queue copied to clipboard (M entries). Paste into Cursor plan mode."
   - Pasted YAML has `mode: EAT-CACHE`, `queued_prompts`, and dedup leaves only one of the duplicate pair (M = 2 if dedup on copy).
4. Optional: Clear queue (modal "Clear Queue" or command "Clear queue"). Confirm Notice "Queue cleared." and Pending: 0.
5. Optional: Test append dedup — add the same prompt+source_file again via modal Send; confirm Notice "Already in queue (duplicate)." and no new line added.

## processed-results.log

Agent outputs or manual notes can be appended to `3-Resources/processed-results.log` when the agent misses something or for copy-paste from Cursor. Create the file if it does not exist.
