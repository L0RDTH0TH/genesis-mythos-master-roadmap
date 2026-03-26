# EAT-QUEUE Flow

**Version: 2026-03 – post-subagent migration**

Describes the user journey for processing the queue: user says EAT-QUEUE → Dispatcher → Queue rule → Step 0 → read queue → dispatch by mode → one line per entry to Watcher-Result. Covers both prompt queue and (briefly) PROCESS TASK QUEUE.

---

## Purpose

Single reference for the “process the queue” flow so users and pipeline authors see the full sequence from trigger to Watcher-Result and queue file update.

---

## Flow overview

1. **User says EAT-QUEUE** (or "Process queue", "EAT-CACHE", "eat cache"). Optionally pastes an EAT-CACHE payload (YAML with `queued_prompts`) instead of reading the file.

2. **Dispatcher** (always rule) routes to the **Queue rule** (`.cursor/rules/agents/queue.mdc`). The Queue rule runs in the main agent.

3. **Step 0 — Always-check wrappers (runs first, every EAT-QUEUE run)**  
   Enumerate all markdown under `Ingest/Decisions/**`. For each wrapper with `approved: true` (or `re-wrap: true` / `re-try: true`) and not processed: resolve approved_option/approved_path via feedback-incorporate; apply per wrapper_type (ingest apply-mode, phase-direction, handoff-readiness, organize, archive, distill-apply-from-wrapper, express-apply-from-wrapper, low-confidence, error). Update wrapper (used_at, processed: true); move wrapper to `4-Archives/Ingest-Decisions/` (ensure_structure, per-change snapshot, move dry_run then commit). Set **approved_wrappers_remaining** if any approved unprocessed wrappers remain. Proceed to read queue (no dependency on queue file containing a CHECK_WRAPPERS entry).

4. **Read queue**  
   Read `.technical/prompt-queue.jsonl` (or use pasted EAT-CACHE payload). If missing or unreadable, treat as empty; optionally append to Watcher-Result; exit.

5. **Parse, validate, dedup, order**  
   Require `mode` (string). Filter queue_failed / "queue-failed". Dedup by (mode, prompt, source_file). Order: CHECK_WRAPPERS first, then canonical pipeline order per Queue-Sources (INGEST MODE → … → RESUME-ROADMAP → … → DISTILL → EXPRESS → ARCHIVE → …). Fast-path: if exactly one valid entry, skip dedup/order and dispatch immediately.

6. **Dispatch**  
   For each entry: CHECK_WRAPPERS no-op; verify source_file if non-empty; validate mode and merged params; normalize aliases (e.g. RECAL-ROAD → RESUME-ROADMAP + action recal); run RESUME-ROADMAP pre-dispatch (approved roadmap-next-step wrapper, context-tracking default-on, bootstrap when state missing). Match mode to pipeline; **delegate** to `.cursor/agents/<name>.md` (or run `.cursor/rules/legacy-agents/<name>.mdc`) with hand-off prompt. Guidance-aware: feedback-incorporate when prompt or user_guidance present. Process one entry fully before the next.

7. **Watcher-Result**  
   After each processed entry, append one line to `3-Resources/Watcher-Result.md`: `requestId: <id> | status: success|failure | message: "..." | trace: "..." | completed: <ISO8601>`.

8. **Clear passed entries only**  
   Build processed_success_ids from entries that completed with status success. Re-read `.technical/prompt-queue.jsonl`; omit lines whose id is in processed_success_ids; keep all other lines (including pipeline-appended). Add failed/skipped entries with `queue_failed: true`. If approved_wrappers_remaining, append one CHECK_WRAPPERS entry. Write merged content back.

---

## PROCESS TASK QUEUE

When the user says **PROCESS TASK QUEUE** (or EAT-QUEUE with clear intent for the task queue), the Queue rule runs the **Task-queue flow**: read `3-Resources/Task-Queue.md`, parse JSON lines, dispatch by mode (TASK-ROADMAP, TASK-COMPLETE, ADD-ROADMAP-ITEM, EXPAND-ROAD, etc.) to the corresponding skills, append one line per entry to Watcher-Result, update `3-Resources/Mobile-Pending-Actions.md`, optional banner cleanup and clear processed entries.

---

## Key points

- **Step 0 runs first** every EAT-QUEUE run; approved wrappers are never stuck even if the queue file is empty.
- **One line per requestId** in Watcher-Result; requestId = queue entry `id`.
- **Two queues:** prompt-queue.jsonl (pipeline modes) vs Task-Queue.md (task/roadmap modes). Which queue is used is determined by the trigger (EAT-QUEUE vs PROCESS TASK QUEUE) and by the mode of each entry.
- **Laptop-only:** Queue files are written from the laptop only. Mobile = observe + fill Ingest.

---

## References

- [Pipelines/Queue-Pipeline](../Pipelines/Queue-Pipeline.md)
- [Rules/Dispatcher-Rule](../Rules/Dispatcher-Rule.md)
- [Rules/Watcher-Result-Contract](../Rules/Watcher-Result-Contract.md)
- [Queue-Sources](../../Queue-Sources.md)
