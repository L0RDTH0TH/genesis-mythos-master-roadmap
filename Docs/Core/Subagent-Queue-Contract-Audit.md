# Subagent–Queue Contract Audit

**Date**: 2026-03-14  
**Scope**: Responsibility boundaries between the Queue/Dispatcher (primary) agent and pipeline subagents after migration from rule-based to subagent dispatch.  
**Trigger**: Resume-roadmap “eats” then queues next item; the eaten RESUME-ROADMAP entry is not removed from the queue.  
**Constraint**: Audit only — no code or rule changes in this document.

---

## 1. Executive summary

- **Observed failure**: When EAT-QUEUE runs a RESUME-ROADMAP entry via the Roadmap subagent, the subagent completes (e.g. runs roadmap-deepen), appends a follow-up RESUME-ROADMAP line to `.technical/prompt-queue.jsonl`, but the **original** RESUME-ROADMAP entry remains in the file. So the “eaten” item is never cleared.
- **Root cause (contract)**: **Clearing the eaten entry is the primary agent’s job**, not the subagent’s. The primary must add the current entry’s `id` to `processed_success_ids` when the subagent returns success, then at A.7 re-read the queue, omit lines whose `id` is in `processed_success_ids`, and write back. If the primary does not add that `id` (e.g. after `mcp_task` return), A.7 will not omit the line.
- **Other risks**: Same pattern affects any mode dispatched via `mcp_task` where the subagent appends to the queue (e.g. RESEARCH-AGENT appending INGEST MODE entries). The primary must reliably add the **dispatched** entry’s id to `processed_success_ids` on success regardless of what the subagent appended.

---

## 2. Intended contract (as documented)

### 2.1 Queue file ownership

| Actor | Allowed actions | Documented in |
|-------|-----------------|----------------|
| **Queue/Dispatcher (primary)** | Read full file (A.1). Re-read before write (A.7). **Omit** lines whose `id` is in `processed_success_ids`. Add `queue_failed: true` for failed/skipped. Append CHECK_WRAPPERS line when `approved_wrappers_remaining`. **Write** merged content back. | agents/queue.mdc A.1, A.7 |
| **Pipeline subagents** (e.g. Roadmap, Research) | **Append** one or more lines to `.technical/prompt-queue.jsonl` (read file → append new line(s) → write back). Subagents do **not** remove or rewrite other lines. | roadmap-deepen SKILL step 7; research.mdc “append INGEST MODE”; Queue-Sources |

So: **primary owns “clear passed” (omit by id); subagents may only append.**

### 2.2 Primary’s obligations after dispatch

From `agents/queue.mdc` A.5 and A.7:

- **A.5**: When the entry matches a pipeline mode, call `mcp_task` with hand-off and `subagent_type`. **When mcp_task returns**, use the return (summary, status) to append Watcher-Result (A.6), then continue to next entry; **include this entry in processed_success_ids only when the subagent completed successfully**.
- **A.7**: Build `processed_success_ids` from entries that completed with status success. Re-read `.technical/prompt-queue.jsonl` from disk. Merge: **omit** lines whose `id` is in `processed_success_ids`; keep all other lines (including pipeline-appended). Write merged content back.

So the contract is clear: **on subagent success, the primary must add the current entry’s `id` to `processed_success_ids`**, so that at A.7 the “eaten” line is omitted. The subagent never removes the line it was invoked for.

### 2.3 Subagent return format

From `Subagent-Safety-Contract.md`:

- Return: one-paragraph summary, any new Decision Wrapper or queue entry created, and **Success / #review-needed / failure** status.

The primary is expected to interpret this to decide “subagent completed successfully” and thus add the entry’s `id` to `processed_success_ids`. The contract does not explicitly say: “Primary MUST add entry id to processed_success_ids when status is Success.”

---

## 3. Identified responsibility conflicts and gaps

### 3.1 RESUME-ROADMAP “eaten entry not removed”

| Aspect | Responsibility | Current contract | Gap / risk |
|--------|----------------|------------------|------------|
| Run deepen | Roadmap subagent | roadmap.mdc → roadmap-deepen | None. |
| Append next RESUME-ROADMAP | Roadmap subagent (roadmap-deepen step 7) | Skill appends to `.technical/prompt-queue.jsonl`. | None. |
| **Remove the eaten RESUME-ROADMAP line** | **Primary (Queue)** | A.7: omit lines whose id ∈ processed_success_ids. | **Primary must add this entry’s id to processed_success_ids when mcp_task returns success.** If the primary does not (e.g. does not interpret return as success, or does not add the id in the mcp_task return path), the eaten line is never omitted. |
| Re-read before write | Primary | A.7: re-read from disk so pipeline-appended lines are included. | Correct: re-read captures the subagent’s new line; omit only removes the processed id. |

**Conclusion**: The intended split is correct (primary clears, subagent appends). The failure is that the **primary** does not reliably add the dispatched entry’s `id` to `processed_success_ids` after `mcp_task` returns success. The contract could be strengthened so that “add to processed_success_ids on success” is explicit and tied to the mcp_task return path.

### 3.2 RESEARCH-AGENT and other appenders

| Mode | Subagent appends? | Who must add dispatched id to processed_success_ids? |
|------|-------------------|------------------------------------------------------|
| RESUME-ROADMAP | Yes (roadmap-deepen appends next RESUME-ROADMAP) | Primary | Same as above. |
| RESEARCH-AGENT | Yes (INGEST MODE per new note; may be in-memory or file append) | Primary | When RESEARCH-AGENT runs via mcp_task, the subagent runs in a separate context. If the subagent appends to the queue file, primary still must add the RESEARCH-AGENT entry’s id to processed_success_ids so that entry is removed at A.7. |
| Step 0 (wrappers) | Step 0 can append (e.g. re-try queue entry) | Primary | Step 0 runs in primary; processed_success_ids is for entries processed in the same run. |

So the same rule applies to every pipeline mode dispatched via mcp_task: **on success, primary adds that entry’s id to processed_success_ids.**

### 3.3 Actions that used to live “deep in rules” and are now in subagents

When execution was rule-based, the same process (e.g. Cursor) ran Step 0 → read queue → dispatch (inline) → Step 8 clear. So “add current id to processed_success_ids” and “re-read and omit” were in one flow. After migration:

- **Dispatch** is via `mcp_task` (separate context).
- **Return** is a message (summary + status).
- The primary must **explicitly** add the entry id to `processed_success_ids` when it receives that return. There is no shared variable or automatic “this entry is done.”

So the contract that was implicit in the single-run flow is now a **handoff**: subagent returns success/failure; primary must interpret it and update `processed_success_ids`. Any ambiguity in “success” or any omission in the primary’s post-return steps (Watcher-Result, add to processed_success_ids, then continue) can leave the eaten entry in the file.

### 3.4 Subagent-Safety-Contract does not mention queue clearing

The safety contract says subagents must:

- Enforce backup, snapshot, confidence, Error Handling, Watcher-Result.

It does **not** say:

- “Subagents must not remove the queue entry they were invoked for” (they don’t; only primary omits at A.7).
- “Primary is responsible for adding the entry id to processed_success_ids on success.”

Adding a short “Queue clearing” bullet to the contract (primary’s responsibility, subagent only appends) would make the boundary explicit for future changes.

---

## 4. Contract summary table

| Responsibility | Owner | Documented where | Notes |
|----------------|--------|------------------|------|
| Read queue (A.1) | Primary | queue.mdc A.1 | OK. |
| Parse, validate, dedup, order (A.2–A.4) | Primary | queue.mdc A.2–A.4 | OK. |
| Dispatch (build hand-off, call mcp_task) | Primary | queue.mdc A.5 | OK. |
| **On mcp_task return: add entry id to processed_success_ids when status = success** | **Primary** | queue.mdc A.5 (one sentence) | **Critical for “eaten” entry to be removed; easy to miss in implementation.** |
| Append Watcher-Result line (A.6) | Primary | queue.mdc A.6 | OK. |
| Re-read queue, omit by processed_success_ids, write back (A.7) | Primary | queue.mdc A.7 | OK. |
| Append new queue line(s) (e.g. next RESUME-ROADMAP, INGEST MODE) | Subagent (roadmap-deepen, research, etc.) | roadmap-deepen SKILL; research.mdc; Queue-Sources | Subagent appends; primary does not remove the **current** entry — that is done at A.7 by omit. |
| Return summary + status (Success / #review-needed / failure) | Subagent | Subagent-Safety-Contract | Primary uses this to decide success and thus whether to add id to processed_success_ids. |

---

## 5. Recommendations (contract / docs only; no code changes)

1. **Queue rule (agents/queue.mdc)**  
   In A.5, make the mcp_task return path **explicit**:  
   “When mcp_task returns: (1) If the return indicates success, **add this entry’s `id` to `processed_success_ids`** (so A.7 will omit this line). (2) Append Watcher-Result for this entry. (3) Continue to the next entry.”  
   This makes “add id on success” a required step in the return path.

2. **Subagent-Safety-Contract**  
   Add a short “Queue and clearing” invariant:  
   “**Queue clearing**: Only the Queue/Dispatcher (primary) agent removes processed entries from `.technical/prompt-queue.jsonl` (by omitting lines whose id is in processed_success_ids at step A.7). Subagents may **append** lines only; they must not remove or rewrite the entry they were invoked for. The primary must add that entry’s id to processed_success_ids when the subagent returns success.”

3. **Hand-off template (Subagent-Safety-Contract)**  
   In “Return only”, add one line:  
   “Explicit **Success** or **failure** (or **#review-needed**) so the queue processor can add this entry’s id to processed_success_ids on success.”

4. **Cross-reference in roadmap and research**  
   In agents/roadmap.mdc and agents/research.mdc, add a one-line note in “How to activate” or “Queue”:  
   “When dispatched by the Queue subagent: the Queue subagent is responsible for removing this entry from the queue on success (processed_success_ids + A.7); this subagent only appends new lines when applicable.”

These are documentation and contract clarifications only; they do not change code or tool behavior.

---

## 6. References

- `agents/queue.mdc` — A.5 (dispatch, mcp_task return), A.7 (clear passed)
- `agents/roadmap.mdc` — RESUME-ROADMAP, roadmap-deepen, queue_next
- `Subagent-Safety-Contract.md` — hand-off structure, return format, invariants
- `roadmap-deepen` SKILL — step 7 (append RESUME-ROADMAP when queue_next !== false)
- `Queue-Sources.md` — queue_next, single-entry funnel, pipeline-appended lines
- `auto-eat-queue.mdc` — Step 8 (clear passed), processed_success_ids, merge logic
- `.cursor/plans/Rule-Refactor/subagent-parity-superiority-audit.md` — parity audit (EAT-QUEUE, processed_success_ids)
