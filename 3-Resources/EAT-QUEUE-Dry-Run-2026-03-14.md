# EAT-QUEUE dry run — prompt-queue.jsonl (lines 1–2)

**Date:** 2026-03-14  
**Source:** `.technical/prompt-queue.jsonl` lines 1–2  
**Trigger:** EAT-QUEUE (Prompt-queue flow). No files or queue are modified; this is a trace-only dry run.

---

## Queue entries (input)

| # | id | mode | source_file / params |
|---|----|------|----------------------|
| 1 | `roadmap-setup-2026-03-12` | ROADMAP MODE | source_file: `1-Projects/genesis-mythos-master/Source-genesis-mythos-master-goal-unaltered-capture-2026-03-07-0033-2026-03-08-0900-2026-03-11-0533.md`, params: `project_id: genesis-mythos-master` |
| 2 | `resume-roadmap-genesis-mythos-master-2026-03-12` | RESUME-ROADMAP | params: `action: deepen`, `project_id: genesis-mythos-master`, `enable_context_tracking: true`, `enable_research: true`, `handoff_gate: true`, `min_handoff_conf: 93`, `queue_next: true` |

---

## Flow trace

### Step 0 — Always-check wrappers

- **Handler:** Queue/Dispatcher subagent (runs before reading queue).
- **Action:** Enumerate `Ingest/Decisions/**`; apply any approved/unprocessed wrappers (path-apply, re-try, re-wrap); set `approved_wrappers_remaining`.
- **Dry run:** No change to queue; assume no approved wrappers → proceed to A.1.

---

### A.1 — Read queue

- **Source:** `.technical/prompt-queue.jsonl`.
- **Result:** 2 non-empty lines (line 3 blank); 2 parseable entries.

---

### A.2 — Parse and validate

- **Line 1:** `JSON.parse` ✓; `mode` present (string) ✓; not `queue_failed` ✓ → **valid**.
- **Line 2:** `JSON.parse` ✓; `mode` present ✓; not `queue_failed` ✓ → **valid**.
- **Valid count:** 2 → no fast-path; continue to A.3, A.4.

---

### A.3 — Dedup

- **Rule:** Same `(mode, prompt, source_file)` → keep first.
- **Entry 1:** mode ROADMAP MODE, source_file set, no prompt.
- **Entry 2:** mode RESUME-ROADMAP, no source_file, no prompt.
- **Result:** No duplicate; both kept.

---

### A.4 — Ordering (canonical pipeline order)

- **Order (Queue-Sources / auto-eat-queue):** … → ROADMAP MODE (7a) → RESUME-ROADMAP (8) → …
- **Sorted order:**  
  1. **Entry 1** — ROADMAP MODE  
  2. **Entry 2** — RESUME-ROADMAP  

---

### A.5 — Dispatch (with pre-dispatch checks)

#### Entry 1 — ROADMAP MODE (`roadmap-setup-2026-03-12`)

- **CHECK_WRAPPERS no-op:** No (not INGEST MODE + CHECK_WRAPPERS).
- **source_file:** `1-Projects/genesis-mythos-master/Source-genesis-mythos-master-goal-unaltered-capture-...md` — would be verified to exist in vault; if missing → skip, Watcher-Result failure.
- **Mode:** ROADMAP MODE → **known**.
- **Params merge:** Entry `params: { project_id: "genesis-mythos-master" }`; merge with Config `prompt_defaults.roadmap` (entry overrides). Valid.
- **Roadmap normalization:** N/A (already ROADMAP MODE).
- **RESUME-ROADMAP bootstrap:** N/A (this entry is ROADMAP MODE).
- **Match mode → pipeline:**  
  **ROADMAP MODE → Roadmap subagent (setup).**
- **Subagent delegation (subagent information):**
  - **Preferred:** Delegate to **real subagent** at **`.cursor/agents/roadmap.md`** using the **mandatory hand-off template** from [[3-Resources/Second-Brain/Subagent-Safety-Contract]].
  - **Fallback:** If delegation is not used, run from **`.cursor/rules/legacy-agents/roadmap.mdc`**.
  - **Hand-off contents (what would be passed):**
    - **Task:** "Run ROADMAP MODE setup for project genesis-mythos-master: Phase 0 + workflow_state + roadmap-generate-from-outline; do not append RESUME-ROADMAP."
    - **Original queue entry:** Full JSON for entry 1 (mode, source_file, params, id).
    - **Critical invariants:** Backup + per-change snapshot before destructive actions; confidence gates; Error Handling Protocol; Watcher-Result one-line with `requestId: roadmap-setup-2026-03-12`; read roadmap-state.md and workflow_state.md when relevant; append log row before returning.
    - **Relevant state files:** `1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md` (create if missing), `1-Projects/genesis-mythos-master/Roadmap/workflow_state.md`, source note at `source_file`.
  - **Return:** One-paragraph summary; any new wrapper or queue entry; Success / #review-needed / failure; Watcher-Result line; workflow_state log row if state mutated.
---

#### Entry 2 — RESUME-ROADMAP (`resume-roadmap-genesis-mythos-master-2026-03-12`)

- **CHECK_WRAPPERS no-op:** No.
- **source_file:** Empty → no file check.
- **Mode:** RESUME-ROADMAP → **known**.
- **Params merge:** Entry params (action, project_id, enable_context_tracking, enable_research, handoff_gate, min_handoff_conf, queue_next) + Config; **RESUME-ROADMAP context-tracking:** `params.action` is "deepen" → if `enable_context_tracking` not explicitly false, set `params.enable_context_tracking = true` (already true in entry). Valid.
- **Roadmap normalization:** N/A (already RESUME-ROADMAP).
- **RESUME-ROADMAP + approved roadmap-next-step wrapper:** Scan `Ingest/Decisions/Roadmap-Decisions/` for roadmap-next-step, same project, approved, not processed. If found → resolve approved_option → params.action, mark processed, move wrapper to archive; then dispatch. (Dry run: assume none found.)
- **RESUME-ROADMAP bootstrap:**
  - **project_id:** `genesis-mythos-master` (from params).
  - **State check:** `1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md` — currently **missing** in vault.
  - **In real run:** Because entries are processed in order, **Entry 1 (ROADMAP MODE)** runs first and creates roadmap-state. So when we reach Entry 2, state **may already exist**. Bootstrap rule: "If state is missing, scan current queue for ROADMAP MODE same project_id; if found and not yet processed, dispatch that ROADMAP MODE entry now." Here, ROADMAP MODE was already processed (entry 1), so we do **not** re-dispatch ROADMAP MODE; we proceed to dispatch RESUME-ROADMAP (state expected after entry 1).
- **Match mode → pipeline:**  
  **RESUME-ROADMAP → Roadmap subagent (continue).**
- **Subagent delegation (subagent information):**
  - **Preferred:** Delegate to **real subagent** at **`.cursor/agents/roadmap.md`** using the **mandatory hand-off template** from [[3-Resources/Second-Brain/Subagent-Safety-Contract]].
  - **Fallback:** **`.cursor/rules/legacy-agents/roadmap.mdc`**.
  - **Hand-off contents (what would be passed):**
    - **Task:** "Run RESUME-ROADMAP for project genesis-mythos-master: single action from params (action: deepen); pre-deepen research if enabled; run roadmap-deepen; append RESUME-ROADMAP to queue when queue_next !== false."
    - **Original queue entry:** Full JSON for entry 2 (mode, params, id).
    - **Critical invariants:** Same as above; requestId: `resume-roadmap-genesis-mythos-master-2026-03-12`; read roadmap-state and workflow_state first; append log row before returning.
    - **Relevant state files:** `1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md`, `1-Projects/genesis-mythos-master/Roadmap/workflow_state.md`, `1-Projects/genesis-mythos-master/Roadmap/decisions-log.md`, `1-Projects/genesis-mythos-master/Roadmap/distilled-core.md`.
  - **Return:** One-paragraph summary; any new wrapper or queue entry (e.g. follow-up RESUME-ROADMAP appended by roadmap-deepen); Success / #review-needed / failure; Watcher-Result line; workflow_state log row.

---

### A.6 — Log

- **Per entry:** Append one line to `3-Resources/Watcher-Result.md`:  
  `requestId: <id> | status: success|failure | message: "..." | trace: "..." | completed: <ISO8601>`.
- **Dry run:** No file write.

---

### A.7 — Clear passed entries only

- **processed_success_ids:** Built from entries that completed with status success.
- **Re-read** prompt-queue.jsonl; drop lines whose `id` is in processed_success_ids; keep others (and any pipeline-appended lines); add failed/skipped from original run with `queue_failed: true`. If `approved_wrappers_remaining`, append one CHECK_WRAPPERS entry.
- **Dry run:** No file write.

---

## Subagent summary

| Entry | Mode | Subagent (real) | Subagent (fallback) | Role |
|-------|------|------------------|----------------------|------|
| 1 | ROADMAP MODE | `.cursor/agents/roadmap.md` | `.cursor/rules/legacy-agents/roadmap.mdc` | Setup: Phase 0, roadmap-generate-from-outline |
| 2 | RESUME-ROADMAP | `.cursor/agents/roadmap.md` | `.cursor/rules/legacy-agents/roadmap.mdc` | Continue: one action (deepen), roadmap-deepen, optional research |

- **Queue/Dispatcher subagent** is the one that *runs* this flow: [[.cursor/rules/agents/queue.mdc]]. It does **not** execute roadmap logic itself; it delegates to the **Roadmap subagent**.
- **Hand-off:** Delegation uses the mandatory hand-off prompt structure in [[3-Resources/Second-Brain/Subagent-Safety-Contract]] (task, queue entry, critical invariants, relevant state files, return format).
- **Roadmap subagent** owns `roadmap-state.md` and `workflow_state.md` under `1-Projects/<project_id>/Roadmap/` and runs skills: roadmap-generate-from-outline (setup), roadmap-deepen, roadmap-resume, research-agent-run (pre-deepen), etc.

---

## Dry-run result

- **No files modified.** Queue, Watcher-Result, and project state are unchanged.
- **If run for real:** Entry 1 would run first (Roadmap setup); then Entry 2 (RESUME-ROADMAP deepen), with bootstrap satisfied by Entry 1 having created state. Both would be delegated to the Roadmap subagent (real or legacy) with the hand-off structure above.

---

## Primary agent’s POV

What the **main Cursor agent** (the one you talk to) does and sees when you say **EAT-QUEUE**:

1. **Trigger**
   - User message contains “EAT-QUEUE” (or Process queue / EAT-CACHE).
   - The **dispatcher** (always-on) matches and says: do **not** run queue logic in the current rule set; **load and follow** the Queue/Dispatcher subagent (`agents/queue.mdc`).

2. **Role switch**
   - The same agent process now **follows the Queue subagent rule**. It runs Part A (Prompt-queue flow) from that rule. So from the primary’s POV: “I am now the Queue/Dispatcher; I own Step 0 → A.1 through A.7.”

3. **What the primary does as Queue**
   - Runs Step 0 (always-check wrappers).
   - Reads `.technical/prompt-queue.jsonl`, parses, validates, dedups, orders.
   - For **each** entry: pre-dispatch checks (source_file, mode, params, bootstrap if RESUME-ROADMAP), then **match mode → pipeline → delegate**.

4. **What “delegate” looks like from the primary’s POV**
   - Delegation is **same process, different instructions**: the primary (still as Queue) builds the **hand-off prompt** from Subagent-Safety-Contract (task, full queue entry, invariants, state files, return format) and then **runs the Roadmap agent’s instructions** (from `.cursor/agents/roadmap.md` or legacy `roadmap.mdc`) in that context.
   - So the primary **does not** “call another process” or “wait for a separate agent.” It **switches context**: “For this entry I now follow the Roadmap agent rule with this hand-off; when that rule’s work is done (summary, status, Watcher-Result line, any queue append), I resume the Queue flow.”
   - After each delegation it: appends a line to Watcher-Result (using the returned or inferred status), then continues to the next entry or to A.7.

5. **End of run**
   - After all entries: build `processed_success_ids`, re-read the queue file, rewrite it (drop passed, keep pipeline-appended, add CHECK_WRAPPERS if needed). Queue subagent flow ends; the primary is back to normal (no role switch until the next trigger).

**In short:** The primary agent is the single execution context. It first acts as **Queue** (orchestration only), then for each roadmap entry it temporarily acts as **Roadmap** (with a clear hand-off), then goes back to **Queue** to log and clear. It never “sees” a separate subagent process—only a change of which rule set and which context (hand-off) it is following.
