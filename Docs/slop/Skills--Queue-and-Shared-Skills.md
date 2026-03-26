# Queue and Shared Skills

**Version: 2026-03 – post-subagent migration**

Summarizes queue/Step 0 and cross-cutting skills not covered in pipeline-specific overviews (Ingest-Organize, Distill-Highlight, Roadmap): feedback-incorporate, apply-from-wrapper, queue-cleanup, obsidian-snapshot, log-rotate, move-attachment-to-99, and task/roadmap queue skills (task-complete-validate, add-roadmap-append, expand-road-assist).

---

## Purpose

Docs/Skills/ has [Roadmap-Skills-Overview](Roadmap-Skills-Overview.md), [Distill-Highlight-Skills](Distill-Highlight-Skills.md), and [Ingest-Organize-Skills-Overview](Ingest-Organize-Skills-Overview.md). This file covers **queue processor** and **shared** skills so the full picture in Skills.md and Cursor-Skill-Pipelines-Reference is reflected in Docs.

---

## Step 0 (always-check wrappers)

Before reading the queue file, the Queue rule enumerates `Ingest/Decisions/**` and applies approved (or re-wrap/re-try) wrappers. Skills involved:

| Skill | When | Purpose |
|-------|------|---------|
| **feedback-incorporate** | Start of queue run or when re-running after async preview | Scan for approved/feedback; load user_guidance or queue prompt; emit guidance_text, hard_target_path, guidance_conf_boost for pipeline context; resolve approved_path / approved_option from wrapper frontmatter (A–G path or re-wrap branch). No destructive writes. |
| **distill-apply-from-wrapper** | When applying approved refinement wrapper (pipeline: distill) | Read wrapper original_path, approved_option; resolve distill_lens/depth; re-run autonomous-distill on original_path with overrides; Step 0 then updates/moves wrapper. |
| **express-apply-from-wrapper** | When applying approved refinement wrapper (pipeline: express) | Read wrapper original_path, approved_option; resolve express_view; re-run autonomous-express on original_path with overrides; Step 0 then updates/moves wrapper. |

Apply-from-wrapper behavior is summarized in [User-Flows/Decision-Wrapper-Flow](../User-Flows/Decision-Wrapper-Flow.md) (wrapper types and apply behavior). Snapshot triggers for pipelines are in [Safety-Invariants](../Safety-Invariants.md) and Cursor-Skill-Pipelines-Reference § Snapshot triggers.

---

## Queue-only skills

| Skill | When | Purpose |
|-------|------|---------|
| **queue-cleanup** | After dedup (optional: when auto_cleanup_after_process in Config) | Mark failed entries queue_failed: true; append summary to Errors.md. |
| **obsidian-snapshot** | Before any destructive step (all pipelines) | Per-change or batch snapshot in Backups/; retention guidance; used by ingest, distill, archive, express, organize. See [Safety-Invariants](../Safety-Invariants.md). |

---

## Task / roadmap queue skills (one-line)

| Skill | Mode(s) | Purpose |
|-------|---------|---------|
| **task-complete-validate** | TASK-COMPLETE | Given filePath and task locator: locate task, detect subtasks; mark [x] only when all subtasks complete. |
| **add-roadmap-append** | ADD-ROADMAP-ITEM | Read secondary note for title/summary; optional duplicate check; append one line to primary roadmap under chosen section (or after task / as sub-task per insertType). |
| **expand-road-assist** | EXPAND-ROAD (RESUME-ROADMAP action: expand) | Parse user text into sub-phases/tasks or suggest breakdown; append under target section/task; link back to roadmap/MOC; phase fork detection (strict/off). |

Full behavior: see [Roadmap-Skills-Overview](Roadmap-Skills-Overview.md) and [Queue-Sources](../../Queue-Sources.md).

---

## Other shared skills

| Skill | When | Purpose |
|-------|------|---------|
| **log-rotate** | Manual / monthly or "Rotate logs" | Copy pipeline logs to Logs-Archive/; truncate or start fresh. |
| **move-attachment-to-99** | User-invoked only (Ingest fallback when MCP move_note fails for binaries) | Fallback move Ingest → 5-Attachments; backup → ensure_structure → shell mv (only exception); update companion .md; scope strictly Ingest/ → 5-Attachments/[subtype]. |

---

## References

- [Pipelines/Queue-Pipeline](../Pipelines/Queue-Pipeline.md) — Step 0, two queues, dispatch
- [User-Flows/Decision-Wrapper-Flow](../User-Flows/Decision-Wrapper-Flow.md) — wrapper types, apply-from-wrapper
- [Safety-Invariants](../Safety-Invariants.md) — snapshot triggers by pipeline
- [Queue-Sources](../../Queue-Sources.md) — mode → file, validation, task/roadmap modes
- [Cursor-Skill-Pipelines-Reference](../../Cursor-Skill-Pipelines-Reference.md) — snapshot triggers table, apply-from-wrapper table
- [Skills](../../Skills.md) — full skills table
