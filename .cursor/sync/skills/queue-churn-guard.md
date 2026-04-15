---
name: queue-churn-guard
description: Normalize prompt-queue JSONL lines (mode vs params.action), dedupe HANDOFF repair waves, optional churn metrics — operator + Layer 1 checklist. No harness Python in this slice.
---

# Queue churn guard (normalizer + checklist)

**Config:** [[3-Resources/Second-Brain-Config|Second-Brain-Config]] § **`queue`** (`origin_dedupe_window_hours`, `strict_nested_*`, `assert_a5b_repair_after_hard_block`) and § **`parallel_execution.watcher.mirror_strict`**. **Normative:** [[.cursor/rules/agents/queue.mdc|queue.mdc]] **A.2** (shape), **A.5b.0z** (HANDOFF dedupe), **A.6** (mirrors).

## When to use

- Before manually appending to **PQ** (`.technical/prompt-queue.jsonl` or `.technical/parallel/<track>/prompt-queue.jsonl`).
- After copying lines from another lane or from Prompt Crafter output.
- When **`RESUME_ROADMAP`** + **`params.action: handoff-audit`** appears without **`HANDOFF_AUDIT_REPAIR`** top-level **`mode`**.

## Checklist (dry_run)

1. **Parse** each line as JSON; require **`mode`**, **`id`** (when appending new work).
2. **Normalize mode/action mismatch:** If **`mode === RESUME_ROADMAP`** and **`params.action === handoff-audit`**, set **`mode`** to **`HANDOFF_AUDIT_REPAIR`** (or split into canonical **`RESUME_ROADMAP`** + action per Queue-Sources) so top-level **`mode`** matches intent.
3. **Dedupe HANDOFF:** For **`HANDOFF_AUDIT_REPAIR`** / **`handoff-audit`** with **`params.origin_request_id`**, scan existing **PQ** for same **`origin_request_id`** + fuzzy **`user_guidance`** within **`queue.origin_dedupe_window_hours`** (default **24**) — **skip** duplicate append; log **`dedupe_suppressed_handoff_repair`**.
4. **Lane:** Ensure **`queue_lane`** matches active **`EAT-QUEUE lane <name>`** when using parallel tracks.
5. **Mirror strictness:** If mirror append fails, ensure canonical **Watcher-Result** still gets the line when **`mirror_strict: false`** (log fallback tag).

## Optional churn metric (manual)

Count **`HANDOFF_AUDIT_REPAIR`** lines sharing the same **`origin_request_id`** in **PQ** — target downward after shield rollout.

## Related

- [[.cursor/skills/queue-cleanup/SKILL.md|queue-cleanup]] — mark-only stale rows; never delete JSONL via shell.
- [[3-Resources/Second-Brain/Docs/Core/Parameters|Parameters]] § Queue shield hardening.
