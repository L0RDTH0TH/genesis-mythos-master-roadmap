---
name: telemetry-summary
description: "Generates canonical EAT-QUEUE Run Telemetry Summary MD (clean first surface + decisions table + Watcher excerpt). Invoked by Layer 1 after A.7 when gates pass; idempotent overwrite; optional archive; dry-run supported."
---

# Run Telemetry Summary

**Purpose:** After each **EAT-QUEUE** Part **A** run completes **A.7** (queue rewrite), produce a **single canonical** markdown file for operators and **Grok-visible** export: **`3-Resources/Second-Brain/Docs/Core/Run-Telemetry-Summary.md`** (overwrites). Optional **timestamped** copy under **`telemetry_summary.archive_dir`** when **`archive_enabled: true`**.

**Normative:** [[.cursor/rules/agents/queue.mdc|queue.mdc]] **Run Telemetry Summary** (post-A.7, pre–A.7a); Config [[3-Resources/Second-Brain/Second-Brain-Config|Second-Brain-Config]] § **`telemetry_summary`**.

## When to run (Layer 1)

Run **after** successful **A.7** write and **before** **A.7a** GitForge when **all** of the following hold:

1. Second-Brain-Config **`telemetry_summary.enabled`** is **true**.
2. Same structural prerequisites as **A.7a** items **1–2** (A.7 succeeded; audit batch complete when audit enabled — see queue.mdc **A.7a**).
3. **`telemetry_summary.invoke_on_empty_queue`** is **false** (default) → **`processed_success_ids`** non-empty **or** documentable consumption (mirror **gitforge.invoke_on_empty_queue** semantics).
4. **`telemetry_summary.invoke_only_on_clean_success`** is **true** (default) → **`any_prompt_queue_dispatch_failure`** is **false**.
5. **`effective_pipeline_mode`** is **`balance`** or **`quality`** when **`telemetry_summary.skip_on_speed_mode`** is **true** (default); **`speed`** → **skip** summary generation.
6. If **`telemetry_summary.require_gitforge_enabled`** is **true** (default **false**): also require **`gitforge.enabled`** **true** (strict alignment with GitForge).

**Idempotency:** Each run **overwrites** the canonical path with the **latest** run’s snapshot (not append-in-place for the canonical file). **Archive** lines are **append-only** (new file per run) when enabled.

## Implementation (script)

From **vault root**:

```bash
python3 scripts/generate_telemetry_summary.py \
  --vault-root "<vault_root>" \
  --lane "<queue_lane_filter or legacy>" \
  --pipeline-mode "<effective_pipeline_mode>" \
  --technical-bundle-root "<dirname(PQ) vault-relative>" \
  --watcher-path "<parallel_execution.watcher.canonical_path or default>" \
  --run-trigger "EAT-QUEUE Part A"
```

- **`--dry-run`**: print markdown to **stdout** only; **no** file writes.
- **`--no-archive`**: skip archive even if **`archive_enabled`** in Config.

**Decisions table** reads **`eat-queue-decisions.jsonl`** colocated with **PQ** (`dirname(PQ)`). **Watcher** excerpt uses **`watcher.canonical_path`**. **JSONL links** include **`task-handoff-comms.jsonl`** beside the bundle.

## Output structure (required sections)

1. **Header:** `# EAT-QUEUE Run Telemetry Summary — [ISO timestamp] [lane] [pipeline_mode]`
2. **Overview** — run trigger, tasks / success / failure summary, key decisions, outcomes, errors summary.
3. **Atomized Decisions** — table from **`eat-queue-decisions.jsonl`** + audit context.
4. **Full Telemetry & Logs** — HTML `<details>` with Watcher-Result excerpt + JSONL path links.
5. **Raw Sources** — links to Watcher-Result (canonical + mirrors) and per-track **PQ** bundle root.

## Failure handling

Script failure **must not** roll back **A.7**. Log **`error_type: telemetry-summary-failure`** to **Errors.md** (best-effort) and continue to **A.7a** when applicable.

## References

- [[3-Resources/Second-Brain/Docs/git-push-workflow-2026-04-02-0446|Git push workflow]] — integration mirror includes **`Docs/Core/Run-Telemetry-Summary.md`**
- [[3-Resources/Second-Brain/Docs/Safety-Invariants|Safety-Invariants]] — Watcher + telemetry summary contract
