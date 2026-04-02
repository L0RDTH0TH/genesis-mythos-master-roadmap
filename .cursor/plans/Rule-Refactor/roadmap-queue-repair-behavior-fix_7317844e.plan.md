---
name: roadmap-queue-repair-behavior-fix
overview: "Align Layer-1 queue handling and the roadmap subagent with the intended three-pass contract: one primary roadmap dispatch per run, repair-first cleanup, and terminal repair entries with no unintended forward deepens."
todos:
  - id: cap-pass1-roadmap-dispatch
    content: Add and enforce per-project cap of one primary roadmap Task in Pass 1 inside queue.mdc A.5.0 and sync the change to .cursor/sync/rules/agents/queue.md.
    status: completed
  - id: repair-terminal-behavior
    content: Adjust roadmap subagent (roadmap.md/roadmap.mdc) so repair-class RESUME_ROADMAP runs set suppress_followup true and do not emit queue_followups next_entry, except for incoherence retries.
    status: completed
  - id: pass3-repair-loop-bounds
    content: Refine Pass 3 inline repair drain loop in queue.mdc to dispatch only repair-class entries for each project and mark them consumed after one run, updating processed_success_ids accordingly.
    status: completed
  - id: stale-resume-handling
    content: Add explicit stale-target/no-op handling in roadmap subagent so reconciled conceptual deepens (like 4.1 rollup) are treated as terminal and do not emit new follow-ups.
    status: completed
  - id: docs-sync-validators-queue
    content: Update Queue-Sources and Validator-Tiered-Blocks-Spec to reflect the clarified three-pass contract and repair semantics, then mirror changes into .cursor/sync files.
    status: in_progress
isProject: false
---

### Goal

Align the queue dispatcher and roadmap subagent with the documented three-pass contract so that:

- Pass 1 dispatches at most one primary roadmap Task per EAT-QUEUE run per project.
- Pass 2 runs post–little-val hostile validation and decides required repairs.
- Pass 3 runs only the required repair-class items for that entry/project and treats them as terminal, without emitting unintended deepen/recal follow-ups.
- Stale or already-reconciled conceptual deepen entries (like the 4.1 rollup case) are consumed cleanly instead of re-spinning.

### Files to change

- `/.cursor/rules/agents/queue.mdc` and `/.cursor/sync/rules/agents/queue.md` – Layer 1 EAT-QUEUE implementation (A.4c, A.5.0, Pass 1/2/3 dispatch, repair-first sub-sort, caps).
- `/.cursor/agents/roadmap.md` and `/.cursor/rules/agents/roadmap.mdc` – RoadmapSubagent queue_followups and queue_continuation behavior, especially for repair-class actions.
- `3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Spec.md` and `3-Resources/Second-Brain/Queue-Sources.md` – Clarify the Pass 1/2/3 contract and the difference between in-run inline repair vs independent roadmap entries.
- (Optional cleanup) `Untitled.md` or any scratch note that partially documents the passes, once the canonical docs are updated.

### Concrete changes

- **Pass 1 primary-cap enforcement (queue.mdc)**
  - In A.5.0, use the existing `roadmap_tasks_invoked_this_eat_queue_run` counter to enforce a hard cap of **one primary roadmap Task per project per EAT-QUEUE run** in the **initial pass**:
    - When matching modes in A.4c / A.5.0 for Pass 1, before calling `Task(roadmap)`, check the map `roadmap_tasks_invoked_this_eat_queue_run[project_id]`.
    - If it is `>= 1` for that project, **skip dispatch** for further RESUME_ROADMAP/ROADMAP_MODE entries in Pass 1, leaving them for a later EAT-QUEUE run; mark them neither success nor failure so they remain in the queue.
    - Keep the existing behavior for non-roadmap modes.
- **Pass 3 repair-only semantics (queue.mdc)**
  - In the Pass 3 generation loop (A.5.0 “Pass 3 generation loop”), ensure that:
    - Only entries tagged as **repair-class** (`queue_priority: "repair"` or `validator_repair_followup: true`) are eligible for Pass 3 roadmap dispatch.
    - Pass 3 will dispatch **all repair-class entries for the current project that were appended or present this run**, subject to the existing generation cap, but **must not** dispatch additional forward-only deepen/recal entries beyond what those repairs explicitly and intentionally emit.
    - After a repair entry has been successfully dispatched once in Pass 3, add its id to `processed_success_ids` and do not admit it to another inline generation within the same run.
- **Repair entries as terminal (roadmap.md + queue.mdc)**
  - In `roadmap.md`/`roadmap.mdc`:
    - Detect when the current RESUME_ROADMAP run is **repair-class**: e.g. incoming queue entry has `queue_priority: "repair"` or `validator_repair_followup: true`, or action comes from the incoherence bounded retry / handoff-audit repair paths.
    - For such runs, after applying the repair and passing little-val/validator gates:
      - Set `queue_continuation.suppress_followup: true` with a terminal `suppress_reason` (e.g. `"repair_only"`).
      - Omit `queue_followups.next_entry` (or set `suppress_next: true`) so Layer 1 has no forward deepen/recal to append.
    - Only the **incoherence bounded retry** path should still be allowed to emit a repair-class recal follow-up, as already specified.
  - In `queue.mdc`:
    - In the mapping from Task return to `queue_continuation`, assert that when a roadmap return has `queue_priority: "repair"` / `validator_repair_followup: true` **and** a terminal `suppress_reason` like `"repair_only"`, Layer 1 must **not** manufacture additional forward follow-ups for that id.
- **Stale structural no-op handling (roadmap.md)**
  - In RoadmapSubagent’s RESUME_ROADMAP deepen branch, add explicit handling for **stale entries** where the requested `current_subphase_index` in `user_guidance`/params does not match authoritative state:
    - If a RESUME_ROADMAP entry is determined to be a **no-op** because the target work is already structurally complete and reconciled (like the 4.1 rollup that is now reconciled into Phase 5.1.3), treat this run as a **ledger-only repair/no-op**:
      - Do not perform structural writes.
      - Return Success or `#review-needed` with `queue_continuation.suppress_followup: true`, `suppress_reason: "repair_only"` or `"superseded"`.
      - Do not emit a new deepen/recal `queue_followups.next_entry` for that stale target.
- **Doc and sync updates**
  - Update `Queue-Sources.md` and `Validator-Tiered-Blocks-Spec.md` to clearly describe:
    - The three-pass model with **one primary roadmap Task per project per EAT-QUEUE run**.
    - That Pass 3 is **bounded by the repair list produced by Tiered Validator**, not by an arbitrary numeric count.
    - That repair-class entries are expected to be **terminal** for that run (no extra forward work), except for the explicitly documented incoherence retry path.
  - Mirror any rule changes from `.cursor/rules/agents/queue.mdc` and `.cursor/rules/agents/roadmap.mdc` into the corresponding `.cursor/sync/rules/...` files to keep backbone docs in sync.

### Risks and verification

- **Risks**: Overly aggressive caps could stall legitimate multi-entry roadmap work if misapplied; terminalizing repair entries could accidentally drop intended follow-ups if the detection logic is too broad.
- **Verification**:
  - Re-run EAT-QUEUE on a controlled test queue containing: a forward deepen, a hard-blocking validator result that produces repairs, and a stale RESUME_ROADMAP deepen for an already-complete slice.
  - Confirm via `queue-continuation.jsonl`, Run-Telemetry, and prompt-queue contents that:
    - Only one primary roadmap entry per project is dispatched in Pass 1.
    - All repair-class entries from the validator are dispatched in Pass 3 and then consumed.
    - Repair entries do not emit unsolicited deepen/recal follow-ups.
    - Stale structural entries are consumed with no new forward work.

