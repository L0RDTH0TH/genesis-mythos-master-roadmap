# EAT-QUEUE Flow

**Version: 2026-03 – post-subagent migration**

Describes the user journey for processing the queue: user says EAT-QUEUE → Dispatcher → Queue rule → Step 0 → read queue → dispatch by mode → one line per entry to Watcher-Result. Covers both prompt queue and (briefly) PROCESS TASK QUEUE.

---

## Purpose

Single reference for the “process the queue” flow so users and pipeline authors see the full sequence from trigger to Watcher-Result and queue file update.

---

## Flow overview

1. **User says EAT-QUEUE** (or "Process queue", "EAT-CACHE", "eat cache"). Optionally pastes an EAT-CACHE payload (YAML with `queued_prompts`) instead of reading the file. **Lane-scoped prompt queue (optional):** **`EAT-QUEUE lane sandbox`**, **`EAT-QUEUE lane godot`**, **`EAT-QUEUE lane shared`**, **`EAT-QUEUE lane default`** — Layer 0 parses the token after **`lane`** and passes **`queue_lane_filter`** to the Queue subagent (see [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]] § Queue lanes, [[.cursor/rules/always/dispatcher.mdc|dispatcher]]). **`sandbox`** / **`godot`** (and other non-`shared`, non-`default` allowed lanes such as **`core`**) dispatch **`target ∪ shared`**. **`shared`** alone dispatches only **`shared`**. **`default`** alone dispatches only **`default`**. Plain **EAT-QUEUE** without **`lane`** leaves **`queue_lane_filter`** unset and processes **all** entries. Invalid lane names → do **not** launch the Queue subagent; log **Errors.md** / Watcher-Result with a clear typo message (validate against **`queue.allowed_lanes`** in [[3-Resources/Second-Brain/Second-Brain-Config|Second-Brain-Config]]).

   **Parallel dual-track (v1):** When **`parallel_execution.enabled`** is **true** in [[3-Resources/Second-Brain/Second-Brain-Config|Second-Brain-Config]], Layer 0 also passes **`## parallel_context`** (YAML) with resolved **PQ** paths for **`sandbox`** / **`godot`** so each chat reads/writes its own **`.technical/parallel/<track>/prompt-queue.jsonl`**. Use **two chats**: **`EAT-QUEUE lane sandbox`** vs **`EAT-QUEUE lane godot`**. **GitForge** shares **`.technical/.gitforge.lock`** — one track may skip git if the other holds the lock. **Watcher-Result:** canonical path plus optional mirrors **`Watcher-Result-sandbox.md`** / **`Watcher-Result-godot.md`** when **`parallel_execution.watcher.enable_mirrors`** is **true**. See [[3-Resources/Second-Brain/Docs/git-push-workflow-2026-04-02-0446|git-push-workflow]] § Parallel dual-track.

2. **Dispatcher** (always rule) routes to the **Queue rule** (`.cursor/rules/agents/queue.mdc`). The Queue rule runs in the main agent (via **`Task(queue)`** subagent).

3. **Step 0 — Always-check wrappers (runs first, every EAT-QUEUE run)**  
   Enumerate all markdown under `Ingest/Decisions/**`. For each wrapper with `approved: true` (or `re-wrap: true` / `re-try: true`) and not processed: resolve approved_option/approved_path via feedback-incorporate; apply per wrapper_type (ingest apply-mode, phase-direction, handoff-readiness, organize, archive, distill-apply-from-wrapper, express-apply-from-wrapper, low-confidence, error). Update wrapper (used_at, processed: true); move wrapper to `4-Archives/Ingest-Decisions/` (ensure_structure, per-change snapshot, move dry_run then commit). Set **approved_wrappers_remaining** if any approved unprocessed wrappers remain. Proceed to read queue (no dependency on queue file containing a CHECK_WRAPPERS entry).

4. **Read queue**  
   Read **PQ** (legacy `.technical/prompt-queue.jsonl` or per-track path from **A.0x** / **`parallel_context`**) or use pasted EAT-CACHE payload. If missing or unreadable, treat as empty; optionally append to Watcher-Result; exit.

5. **Parse, validate, lane filter, dedup, order**  
   Require `mode` (string). Filter queue_failed / "queue-failed". When **`queue_lane_filter`** is set on the hand-off, keep only entries matching **A.2a** in [[.cursor/rules/agents/queue.mdc|queue.mdc]] (union rules for `shared`). Dedup by (mode, prompt, source_file). Order: CHECK_WRAPPERS first, then canonical pipeline order per Queue-Sources (INGEST MODE → … → RESUME-ROADMAP → … → DISTILL → EXPRESS → ARCHIVE → …). Fast-path: if exactly one valid entry **after lane filter**, skip dedup/order and dispatch immediately. **EAT-CACHE:** apply the same **`queue_lane_filter`** (if any) to **`queued_prompts`**.

6. **Dispatch**  
   For each entry: CHECK_WRAPPERS no-op; verify source_file if non-empty; validate mode and merged params; normalize aliases (e.g. RECAL-ROAD → RESUME-ROADMAP + action recal); run RESUME-ROADMAP pre-dispatch (approved roadmap-next-step wrapper, context-tracking default-on, bootstrap when state missing). Match mode to pipeline; **delegate** to `.cursor/agents/<name>.md` (or run `.cursor/rules/legacy-agents/<name>.mdc`) with hand-off prompt. Guidance-aware: feedback-incorporate when prompt or user_guidance present. Process one entry fully before the next.

7. **Watcher-Result**  
   After each processed entry, append one line (format: `requestId: <id> | status: success|failure | message: "..." | trace: "..." | completed: <ISO8601>`) to the **canonical** path (**`parallel_execution.watcher.canonical_path`** when parallel enabled, else **`3-Resources/Watcher-Result.md`**), and to per-track mirror files when Config **`enable_mirrors`** is **true** and **`parallel_track`** is set.

8. **Clear passed entries only**  
   Build processed_success_ids from entries that completed with status success. **Pre-write re-read:** Immediately before building the merged file body, **re-read** **PQ** from disk. Omit lines whose `id` is in processed_success_ids; keep all other lines verbatim. Add failed/skipped entries with `queue_failed: true`. If approved_wrappers_remaining, append one CHECK_WRAPPERS entry. Write merged content back to **PQ**.

---

## PROCESS TASK QUEUE

When the user says **PROCESS TASK QUEUE** (or EAT-QUEUE with clear intent for the task queue), the Queue rule runs the **Task-queue flow**: read `3-Resources/Task-Queue.md`, parse JSON lines, dispatch by mode (TASK-ROADMAP, TASK-COMPLETE, ADD-ROADMAP-ITEM, EXPAND-ROAD, etc.) to the corresponding skills, append one line per entry to Watcher-Result, update `3-Resources/Mobile-Pending-Actions.md`, optional banner cleanup and clear processed entries.

---

## Key points

- **Queue lanes:** Dual-track runs use **`queue_lane`** on JSONL lines and **`EAT-QUEUE lane <name>`** so two chats can process disjoint subsets safely; with **`parallel_execution`**, each track uses its own **PQ** file under **`.technical/parallel/<track>/`**; see [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]] § Parallel execution.
- **Step 0 runs first** every EAT-QUEUE run; approved wrappers are never stuck even if the queue file is empty.
- **One line per requestId** in Watcher-Result; requestId = queue entry `id`.
- **Two queues:** **PQ** (pipeline modes) vs Task-Queue.md (task/roadmap modes). Which file is **PQ** depends on **A.0x** (legacy vs parallel bundle).
- **Laptop-only:** Queue files are written from the laptop only. Mobile = observe + fill Ingest.

---

## References

- [Pipelines/Queue-Pipeline](../Pipelines/Queue-Pipeline.md)
- [Rules/Dispatcher-Rule](../Rules/Dispatcher-Rule.md)
- [Rules/Watcher-Result-Contract](../Rules/Watcher-Result-Contract.md)
- [Queue-Sources](../../Queue-Sources.md)
