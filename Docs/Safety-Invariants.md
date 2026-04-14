# Safety Invariants

**Version: 2026-03 – post-subagent migration**

Consolidated safety invariants for all subagents and the Queue. Full logic lives in the rules; this doc is the single reference.

---

## Backups

- **Before any destructive operation** (move, rename, delete, large overwrite), ensure a recent backup: `obsidian_ensure_backup` (preferred) or `obsidian_create_backup` (when ensure indicates missing or stale).
- **If backup creation fails:** Abort destructive steps for that note; log with `#review-needed`; continue with next note in batch.
- **Reference:** core-guardrails.mdc, mcp-obsidian-integration.mdc.

---

## Curator git hygiene (agents)

- After **mutating vault files**, agents **must** run **`./scripts/curator_snapshot.sh`** (private **`curator`** remote, branch **`main`**) per [[.cursor/rules/agents/curator-mandatory-backup|curator-mandatory-backup]] before claiming **Success**. If push fails, report **`task_error`** — do **not** treat the session as stably backed up.
- **Delete intent** remains **move-to-trash** only — [[.cursor/rules/agents/execution-safety-blacklist|execution-safety-blacklist]]; **GitForge** / public export is a **separate** remote path.

---

## Per-change snapshots

- **Before:** move, rename, split, structural distill, append_to_hub, or other destructive/structural step — call obsidian-snapshot skill with **type per-change** for the target note when **confidence ≥ 85%**.
- **If snapshot fails:** Skip the destructive action; log `#review-needed`.
- **Location:** `Backups/Per-Change/`; append-only; never edit or delete from pipelines.
- **Reference:** core-guardrails, mcp-obsidian-integration.

---

## Confidence bands

| Band | Range | Behavior |
|------|-------|----------|
| **High** | ≥ 85% | Destructive actions allowed **only after** per-change snapshot; dry_run then commit for moves. |
| **Mid** | 68–84% | At most **one** non-destructive refinement loop per note per run; proceed only if post_loop_conf ≥ 85%; else create Decision Wrapper (e.g. Ingest/Decisions/Refinements/). |
| **Low** | < 68% | No destructive action; create Decision Wrapper (e.g. Ingest/Decisions/Low-Confidence/); propose only. |

- **Decay rule:** If post_loop_conf ≤ pre_loop_conf, fall back to user decision: no destructive action for that note; log best-guess and #review-needed where appropriate.
- **Loop logging:** Record in pipeline log and/or obsidian_log_action: `loop_attempted`, `loop_band`, `pre_loop_conf`, `post_loop_conf`, `loop_outcome`, `loop_type`, `loop_reason`.
- **Reference:** Parameters.md, confidence-loops.mdc.

---

## Critical invariant

**No destructive action** unless **both**:

1. Confidence for that action is in the **high band** (≥ 85%) for that pipeline, **and**
2. A **per-change snapshot** for that note has been created successfully in the current run.

If either fails: skip the destructive action; log #review-needed; continue with non-destructive alternatives.

---

## Parallel track PQ (central pool fanout)

When **`queue.central_pool_fanout_enabled`** is true and **`queue.pool_sync_strict_central_only`** is **false** (default), **`pool_sync`** (**A.0.4**) **must not** drop valid per-track **PQ** lines solely because they are missing from the **central pool** — those **lane-only** rows are **merged** back after applying the pool subset (see [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]] § Lane-only preservation). Strict central-only mode is **opt-in** for debugging or forced resync.

### Queue file bytes (single writer)

Concrete read/write of **`.technical/prompt-queue.jsonl`** (per-track or pool), checksum boundaries, and **A.7** rewrites are implemented in **`scripts/eat_queue_core`** (**`python3 -m scripts.eat_queue_core.harness`**) invoked from the Queue rule — not ad-hoc parallel editors. This aligns **Nested subagent policy** (only Layer 1 orchestrates queue files) with **single-writer** bytes on disk. See [[3-Resources/Second-Brain/Docs/Queue-Harness-Architecture|Queue-Harness-Architecture]].

---

## Nested subagent policy (orchestration safety)

- **Single orchestrator**: Only the **main agent + Queue rule** are allowed to orchestrate:
  - Read or write `.technical/prompt-queue.jsonl` or `3-Resources/Task-Queue.md`.
  - Decide which pipeline subagent runs.
  - Append to `3-Resources/Watcher-Result.md` or create Decision Wrappers under `Ingest/Decisions/**`.
- **Nested subagents = helpers only**:
  - Pipeline subagents may call **nested subagents** only as documented in the nested subagent whitelist (see [[3-Resources/Second-Brain/Docs/Subagent-List|Subagent-List]]). As of the Research-layer migration there are exactly **three** sanctioned helper subagents: **Internal Repair Agent (IRA)**, **Validator**, and **Research**.
  - Nested subagents must behave like **pure functions**: they read only the inputs handed to them and return **structured results** to their caller; they must not:
    - Read or write queue files or Task-Queue.
    - Append to `Watcher-Result.md`.
    - Create or apply Decision Wrappers.
    - Mutate roadmap state files (`roadmap-state.md`, `workflow_state.md`) or other global coordination artifacts.
- **Depth and fan-out limits**:
  - Recommended maximum depth: **3 levels** — main agent → Queue/Dispatcher → pipeline subagent → nested helper subagent (IRA / Validator / Research).
  - Fan-out: parents may call several nested helpers in parallel for **local analysis** (e.g. multiple research lookups), but must not chain nested agents to re-orchestrate pipelines.
- **Dependent nested helper serialization (invariant):**
  - For roadmap and research pipelines, the validator report is a required input to IRA. Dependent helpers (Validator → IRA → second Validator) must be launched and awaited sequentially. IRA must see the final validator output from this run. Parallel execution of this chain is not permitted; violation must be recorded as `task_error` or surfaced as `#review-needed`.
- **Prompt-level safeguard**:
  - Each pipeline subagent’s high-level instructions must reinforce:
    - *“You may ONLY call the specific nested subagent types listed in your 'Subagent nesting' section, and ONLY for the narrow purposes described. NEVER write to queues, watcher logs, roadmap files, or create decision wrappers — those are RESERVED for the top-level orchestrator. Return results as structured data only.”*

---

## Analysis-Only Runs

Analysis-only runs are **strictly limited**. They may **not** be used for RESUME_ROADMAP deepen, mint, or any action that normally triggers nested helpers in **balance** mode.

If the environment prevents real Task launches for mandatory helpers (Validator, IRA, or Research when selected), the run **must** fail with `task_error` rows recorded in `nested_subagent_ledger` — it must **not** gracefully degrade to `analysis_only` while silently skipping those helpers.

**Forbidden in balance mode for deepen-class tasks:**

- Treating "cannot safely perform mutations" as a reason to set `nested_cycle_applicable: false`.
- Using `environment_inline_only_no_safe_mutation` (or similar reason codes) to skip mandatory Validator/IRA Task launches.
- Claiming that citing the Safety-Contract or this document allows an exemption when the contract actually requires attempting the helper Task calls.

---

## Helper profiles, mandatory helpers, and honesty (no pretending)

This section summarizes the **helper profile** rules from [[3-Resources/Second-Brain/Subagent-Safety-Contract|Subagent-Safety-Contract]] and [[3-Resources/Second-Brain/Docs/Pipeline-Validator-Profiles|Pipeline-Validator-Profiles]] so they are visible from one place.

- **Profiles:** Every Task launch runs under a **pipeline profile**:
  - `fast` — minimal helper set.
  - `balance` — default helper set; recommended for normal runs.
  - `extreme` — maximal helper set; strictest enforcement and observability.
- **Helper graphs per profile:**
  - For each pipeline mode, the helper graph defines which nested helpers (Validator, IRA, Research) are **selected** for that profile.
  - Once a helper is **selected** for the active profile, it becomes **mandatory** for that run:
    - The caller **must** attempt a real `Task(subagent_type: ...)` for that helper (**attempt-before-skip**).
    - If the Task host rejects the call or the tool is missing, the step must be recorded as `outcome: task_error` with `host_error_class` / `host_error_raw` in `nested_subagent_ledger`, and the overall status must be `#review-needed` or `failure` — not Success.
    - It is **never** permissible to silently skip a mandatory helper or to claim it ran without a real Task call.
- **Profile semantics:**
  - `balance` / `extreme`:
    - All helpers selected in the helper graph for that profile are **hard mandatory** for the run.
    - Skipping them is only permitted via recorded `task_error` with concrete host error details; Success is blocked when a mandatory helper is missing or only marked `skipped` without an allowed reason code.
  - `fast`:
    - May select a smaller helper graph, but for any helper that **is** selected, the same mandatory semantics apply.
- **No misrepresentation / honesty gate:**
  - No subagent may:
    - Report **Success** with `little_val_ok: true` when a mandatory helper step was never actually attempted as a Task call and has no valid `task_error` ledger row.
    - Use `outcome: invoked_ok` or `invoked_empty_ok` with `task_tool_invoked: false` on mandated helper steps (see [[3-Resources/Second-Brain/Docs/Nested-Subagent-Ledger-Spec|Nested-Subagent-Ledger-Spec]] Attestation invariants).
    - Use `outcome: skipped` + `task_tool_invoked: false` on a required helper step unless `detail.reason_code` is in the documented allowlist (material gate, legacy clean skip, chain consumables, etc.).
  - When these honesty conditions are not met, the run **must** be treated as `#review-needed` or `failure`; Layer 1 strict gates (`queue.strict_nested_return_gates`) prevent queue entries from being cleared as successful in this state.

These profile and honesty rules apply **in addition to** the backup, snapshot, and confidence-band invariants above; they do not weaken any existing safety guarantees.

---

## Rationale honesty (`option_evaluation`)

When [[3-Resources/Second-Brain/Second-Brain-Config|Second-Brain-Config]] **`queue.rationale_enforcement_enabled`** is **true**, queue entries subject to [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]] § **`params.option_evaluation`** must satisfy:

- **Verbatim anchor:** **`rationale`** must contain a **substring** that appears **verbatim** in the file resolved by **`master_goal_ref`** (after normalizing vault-relative paths). This is a **cheap structural** anti-fabrication check — it does not prove semantic correctness.
- **Score sanity:** If **every** **`alternatives[]`** item includes **`alignment_score`**, **`chosen`** must identify an alternative whose score **equals the maximum** among alternatives (ties allowed).
- **Structural validity:** **`chosen`** must match one **`alternatives[].id`**; **`validator_ref`**, when present, should point to a real validator report path or a **`task_correlation_id`** present in **task-handoff-comms** (best-effort verification in harness).

Violations produce **`divergence_codes`** on **`intent_actual_receipt`** rows (e.g. **`rationale_quote_missing`**, **`alignment_score_mismatch`**, **`option_evaluation_invalid`**) per Queue-Sources; runs may still complete with **`status_class: provisional_success`** unless Layer 1 strict policy is enabled.

---

## No shell vault ops

- **Never** use shell **`cp`** or non-trash **`mv`** to mutate Obsidian vault note content for pipelines — use MCP tools with backup and snapshot gates.
- **Delete intent:** **Never** use **`rm`**, **`rm -rf`**, **`rmdir`**, **`find ... -delete`**, or shell **`unlink`** on vault paths. **Rewrite** removal as **move-to-trash**: relocate under **`.trash/<timestamp>/`** and append **`.trash/TRASH-MANIFEST.log`** per [[.cursor/rules/agents/execution-safety-blacklist|execution-safety-blacklist]]; use **`./scripts/move-to-trash.sh`** from vault root when shell is required.
- **Exception (narrow shell `mv`):** Only **`scripts/move-to-trash.sh`** may use `mv` toward **`.trash/`** for delete intent. **Exception:** Documented, **user-invoked** attachment-move skill (Ingest → 5-Attachments/) only; backup and logging still apply.
- **Reference:** [[.cursor/rules/agents/execution-safety-blacklist|execution-safety-blacklist]], [[3-Resources/Second-Brain/Docs/Backup-and-Recovery-Strategy|Backup-and-Recovery-Strategy]] § Move-to-trash and Obsidian trash.

---

## Version control vs sync (operator-level)

- **MCP backups and per-change snapshots** (sections above) still govern **pipeline** destructive steps. They do **not** replace **whole-vault** version history.
- **Private git on `Curator`** (with Obsidian Git or manual commits) is the recommended **recoverable** layer for the full vault tree. **Syncthing** is convenience sync across devices — **not** a substitute for `git reset` / clone recovery when history matters. **Public export** (`gmm-roadmap-export` → `genesis-mythos-master-roadmap`) is for collaboration and published contracts, not private full-vault backup. See [[3-Resources/Second-Brain/Docs/Backup-and-Recovery-Strategy|Backup-and-Recovery-Strategy]].
- **Agents:** **Never** use shell `rm -rf` or bulk destructive commands on vault roots; use **move-to-trash** for delete intent (see above). **Human-operated** Curator + documented restore order closes whole-vault recovery gaps.
- **Reference:** [[3-Resources/Second-Brain/Vault-Layout|Vault-Layout]] (`.stignore` / Syncthing and `.git/`).

---

## Structure before move

- Before any `obsidian_move_note` to a new directory:
  1. Call **obsidian_ensure_structure** with `folder_path` = parent of target path.
  2. Call **obsidian_move_note** with `dry_run: true`; review effects.
  3. Then call **obsidian_move_note** with `dry_run: false` to commit.
- **Post-move:** Set **para-type** (and **project-id** when under 1-Projects/; **status: archived** when under 4-Archives/) on the note at the new path per mcp-obsidian-integration.

---

## Exclusions and protected paths

**Do not move, rename, or delete:**

- `Backups/**` (Per-Change, Batch, Archives).
- `3-Resources/Watcher-Signal.md`, `3-Resources/Watcher-Result.md`, `Ingest/watched-file.md`.
- Any note with frontmatter **watcher-protected: true**.
- MCP backup directories in `~/.cursor/mcp.json`.

**Do not process as primary pipeline input:** Notes under `Ingest/Decisions/**` (consumed by Step 0 and path-apply logic).

- **Reference:** core-guardrails, Vault-Layout.md.

---

## Error Handling Protocol

On **any** pipeline or workflow step failure:

1. **Trace:** Timestamp (ISO 8601), pipeline name, stage/step, affected note path(s), sanitized error message (no secrets).
2. **Summary:** Error type; root cause; impact; suggested fixes; recovery (e.g. restore from Backups/Per-Change/).
3. **Log (owned by top-level run):** Append one entry to **`3-Resources/Errors.md`** (heading, inline table, #### Trace, #### Summary). **Only the main agent / Queue rule** should create or update this note; nested subagents must instead return structured failure details to their caller.
4. **Pipeline log:** One-line reference in the relevant pipeline log, written from the orchestrating context (not from deeply nested helpers).
5. **Error Decision Wrapper:** When appropriate, create under **`Ingest/Decisions/Errors/`** (wrapper_type: error; options A–G recovery-focused); ensure CHECK_WRAPPERS exists; append Watcher-Result line for wrapper creation.
6. **Severity high:** Set approval pending, add #review-needed; skip destructive steps for that note; continue with next.
7. **Fallbacks first:** Before writing an error entry, attempt fallbacks (e.g. obsidian_ensure_structure then retry move); only after exhausting fallbacks, log to Errors.md.

- **Reference:** mcp-obsidian-integration § Error Handling Protocol.

---

## Watcher-Result contract

- On run finish (queue-based or direct), append **one line per requestId** to **`3-Resources/Watcher-Result.md`**:

  ```
  requestId: <id> | status: success|failure | message: "..." | trace: "..." | completed: <ISO8601>
  ```

- Create the file if missing; append only; do not overwrite.
- **Reference:** watcher-result-append.mdc.

---

## Run Telemetry Summary (EAT-QUEUE)

- After **A.7** (queue rewrite), when **`telemetry_summary`** gates pass, Layer 1 **overwrites** **`3-Resources/Second-Brain/Docs/Core/Run-Telemetry-Summary.md`** via **`scripts/generate_telemetry_summary.py`** (see [[.cursor/skills/telemetry-summary/SKILL.md|telemetry-summary]], [[.cursor/rules/agents/queue.mdc|queue.mdc]] **Run Telemetry Summary**).
- **Not** a substitute for append-only **Watcher-Result** lines — it is a **derived**, **committed** first surface for operators and **GitHub / Grok** (copied next to **Watcher-Result** in [[3-Resources/Second-Brain/Docs/git-push-workflow-2026-04-02-0446|Git push workflow]] Step 1).
- **Speed** runs skip when **`telemetry_summary.skip_on_speed_mode`** is **true** (aligned with GitForge **A.7a**).
- Script failure **must not** roll back **A.7**; log **`telemetry-summary-failure`** to **Errors.md** best-effort.

---

## Roadmap state

- **Before mutating:** Read `roadmap-state.md` and `workflow_state.md` under `1-Projects/<project_id>/Roadmap/`.
- **Snapshot:** Snapshot state **before and after** every update (per-change).
- **Parse failure:** If roadmap-state.md or workflow_state parse fails → abort roadmap pipeline; log to Errors.md with #state-corrupt; create Decision Wrapper under Ingest/Decisions/Errors/ as appropriate.
- **Reference:** mcp-obsidian-integration, Roadmap subagent.

---

## Restore

- **Restore** from snapshots is **user-triggered only**. No auto-restore.
- **Reference:** mcp-obsidian-integration (restore-queue mode).

---

## Snapshot triggers (by pipeline)

Per-change snapshot is required **before** the following. Batch frequency is per pipeline (e.g. every 3–5 notes for ingest/distill/organize; once per archive sweep for archive). <!-- Gap filled from old Cursor-Skill-Pipelines-Reference.md -->

| Pipeline | Per-change before | Batch |
|----------|-------------------|-------|
| full-autonomous-ingest | split_atomic, distill_note rewrite, append_to_hub, task-reroute target append, move_note, rename_note | Every 5 notes |
| autonomous-distill | First structural rewrite (distill layers, layer-promote, heavy update_note) | ~Every 3 notes |
| autonomous-archive | After archive-check ≥85% but before subfolder-organize / summary-preserve / move | Once per sweep |
| autonomous-express | Large appends (related-content-pull, express-mini-outline, call-to-action-append); also version-snapshot | Optional per batch |
| autonomous-organize | obsidian_rename_note (when name-enhance), obsidian_move_note (when path_conf ≥85%) | ~Every 3 notes |
| roadmap (multi-run) | Every roadmap-state.md and workflow_state update; before phase-X-output overwrite | Per phase or RECAL run |

---

## Log format and loop fields

Pipeline log line format and loop fields (loop_attempted, loop_band, pre_loop_conf, post_loop_conf, loop_outcome, loop_type, loop_reason) are defined in **Cursor-Skill-Pipelines-Reference** § Log format, backup path, and loops. Include **backup path** in the log entry (e.g. in the `changes` string) when a backup was created. <!-- Gap filled from old Cursor-Skill-Pipelines-Reference.md -->
