### **Shared mental model: the three passes**

Here’s the simplest way to line it up with how the queue rules are actually written.

- **Pass 1 – Primary dispatch (forward work)**
  - Take the **ordered queue** (after dedup + repair‑first sub‑sort) for this EAT‑QUEUE run.
  - For a single entry in order, Layer 1 **calls the real pipeline subagent** (e.g. `Task(roadmap)` for RESUME_ROADMAP / ROADMAP_MODE) and waits for its return.
  - The roadmap subagent does all its work (deepen, recal, advance, repairs inside itself), may return `queue_followups` (new forward or recal entries) and `little_val_ok`/`validator_context`.
- **Pass 2 – Post–little‑val hostile validation + tiered decision**
  - For entries where the roadmap subagent said “little_val_ok + validator_context present”, Layer 1 runs the **hostile validator Task** (`roadmap_handoff_auto`) in its own context.
  - It interprets the verdict by tier:
    - **Low/log_only** → no queue‑level repair; forward work stands.
    - **Medium/needs_work** (non‑blocking codes) → note advisory (`missing_roll_up_gates`, etc.), but don’t block or rewrite.
    - **High/block_destructive** / hard codes (`state_hygiene_failure`, `contradictions_detected`, `incoherence`, etc.) → **append a repair‑class queue entry in memory** (`repair-l1postlv-`*, `repair-recal-*`, `repair-handoff-audit-*`) with `queue_priority: "repair"` / `validator_repair_followup: true`.
- **Pass 3 – Repair‑first execution and merge / write‑back**
  - Still inside the same EAT‑QUEUE run, Layer 1 now:
    - **Re‑orders the in‑memory queue** so any newly added **repair entries** for a project run **before** further deepen/advance entries for that project.
    - **Dispatches those repair entries** (again via `Task(roadmap)`, but now in “repair mode”) and interprets their `queue_followups` the same way (ideally `queue_next: false` so they are terminal). Note* should currently be limited to aprox. 2 queue items max in pass 3.
  - Only after this repair‑first loop finishes does Step 8:
    - Re‑read `.technical/prompt-queue.jsonl`.
    - Drop entries that succeeded this run (processed_success_ids).
    - Keep any lines appended during the run (e.g. forward deepen/recal follow‑ups that survived tiering).
    - Re‑write the queue file.

