---
title: Untitled
created: "2026-02-24 06:06"
tags: 
para-type: Resource
status: reviewed
ingest-type: ai-output
---
# AI Output Capture

## Source & prompt

_Which model/app and what did you ask? Paste the key parts of your prompt here._

- Source/model: Grok
- Date/time: 2026-02-24 06:06
- Prompt:

  
Summary of what’s in place and how to use it:

---

## Recommendations (saved in the vault)

**1. [[2026-02-24-ingest-prompt-improvement-recommendations]]** — Full write-up with 10 recommendations. Main points:

| Area | Change |
|------|--------|
| **Auto-execute** | Remove “wait for ok”; state clearly: ≥85% → auto-execute all actions; <85% → propose + #review-needed only. |
| **Filter** | Fix “#place filters her or skip”: use `obsidian_list_notes` with `directory: "Ingest"`, then filter by `#raw-ingest` / `status: raw` or process all `.md`; say which you use. |
| **Tool sequence** | Spell out the exact chain: create_backup → classify_para → split_atomic (if needed) → distill_note → manage_frontmatter/tags → append_to_hub → move_note → log_action. |
| **Log format** | Put the full log line in the prompt, including **Backup:** `[backup_path]`. |
| **Batch summary** | Require: Processed N \| High-confidence auto-executed: X \| Flagged: Z \| Skipped/Failed: W; optionally group output by auto-executed vs flagged. |
| **One canonical prompt** | Use a single launch prompt for both “current note” and “entire Ingest/” so behavior doesn’t drift. |
| **Trinity** | Add: read `resources/` and follow para-zettel-autopilot examples before classifying/distilling. |
| **Failure handling** | State: per-note isolation; if one note fails (e.g. backup), skip that note, log, and continue. |
| **Launch phrase** | Standardize e.g. “INGEST MODE – safe batch autopilot” or “Process Ingest/ with autopilot.” |

---

## Updated launch prompt

**2. [[2026-02-24-cursor-ingest-prompt-reference]]** — The “AI/Chat Appendices” section now has **one canonical INGEST MODE block** that:

- Uses **backup-first** and **auto-execute at ≥85%** (no “propose only / wait for ok”).
- Specifies **list & filter**: `obsidian_list_notes` with `directory: "Ingest"`, then all `.md` or only `#raw-ingest`/`status: raw`.
- Lists the **exact MCP tool order** and the **log line format** including Backup.
- Defines **batch summary** and **grouped output** (auto-executed vs flagged vs failed).
- Covers **single note** and **batch** in one prompt.
- Mentions **trinity** (resources + autopilot examples) and **per-note isolation**.

You can launch every ingest run with: **“INGEST MODE – safe batch autopilot”** or **“Process Ingest/ with autopilot.”**

---

## Optional next step

In the canonical prompt, the filter is currently: “Process all `.md` (or only those with `#raw-ingest` or `status: raw`—state which you use).” If you want a fixed default, we can set it to either “all .md in Ingest/” or “only #raw-ingest / status: raw” and remove the “or.”> 
 Working on the launch prompt now
Here is are the areas in Cursors output that jumped out to me as acceptable.
Auto-execute
Tool sequence
One canonical prompt
Failure handling
Launch phrase


## Full output

_Paste the full AI response below._

>  INGEST MODE – safe batch autopilot

You are an autonomous Zettelkasten ingest agent. Follow this exact protocol for every run (single active note or batch processing Ingest/ folder).

CORE RULES:
- Read and strictly adhere to resources/ para-zettel-autopilot examples and trinity principles before any classify_para or distill_note step.
- Process in strict isolation per note: failure on one note does NOT stop the batch.
- Always start with backup: Use create_backup FIRST on the note being processed.
- Confidence threshold: ≥85% → auto-execute the full sequence without proposal. <85% → propose changes + add #review-needed tag only (do NOT execute).
- No "wait for ok" or interactive confirmation loops — decide and act (or flag) immediately.

FILTER & SCOPE:
- Use obsidian_list_notes with directory: "Ingest" to get candidates.
- Process ALL .md files in Ingest/ (no tag/status filter for maximum capture safety; skipped/empty notes will be quick/no-op).
  (If you prefer stricter: only #raw-ingest or status: raw — but state your choice explicitly at the start of output.)

EXACT TOOL SEQUENCE (run in this order, per note):
1. create_backup → capture original content safely.
2. classify_para → determine para-type and confidence.
3. If multi-idea / low atomicity: split_atomic → create child notes as needed.
4. distill_note → refine to atomic, clear prose.
5. manage_frontmatter/tags → update YAML, add tags/links.
6. append_to_hub → link into relevant map-of-content / hub note(s).
7. move_note → relocate to final folder (e.g. based on para-type).
8. log_action → record one-line summary.

LOG FORMAT (append to a dedicated log note or output block):
- For each note: **Note:** [[filename]] | **Backup:** [backup_path] | **Confidence:** XX% | **Actions:** auto-executed [list] OR flagged #review-needed [reason/proposal] | **Final path:** [new/path.md]
- If error: **Failed:** [reason] — skipped, continuing batch.

BATCH SUMMARY (at very end, always):
Processed: N | Auto-executed: X | Flagged for review: Z | Failed/Skipped: W
Group output:
- Auto-executed notes: ...
- Flagged notes: ...
- Failures: ...

Launch this mode only via phrases like:
- “INGEST MODE – safe batch autopilot”
- “Process Ingest/ with autopilot”
- “Ingest current note – safe autopilot”

Begin processing now.

## Key insights

_Extract the few pieces that are actually useful or worth revisiting._

-  The Reusable Prompt for Cursor
-  
-  

## TL;DR

_Short summary of why this output matters (or "nothing useful" if so)._

-

## Why resource?
Assigned based on content/frontmatter (confidence ~85%).

## Review Needed
Proposed para-type: resource. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.