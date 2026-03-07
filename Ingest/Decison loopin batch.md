---
title: Untitled
created: "2026-03-03 21:10"
tags: 
para-type: Ingest
status: ingest
ingest-type: ai-output
proposal_path: Ingest/Decisions/Ingest-Decisions/Decision-for-decison-loopin-batch--2026-03-07-0541.md
decision_candidate: true
decision_priority: high
---
# AI Output Capture

## Source & prompt

_Which model/app and what did you ask? Paste the key parts of your prompt here._

- Source/model:
- Date/time: 2026-03-03 21:10
- Prompt:

>  
Here’s how **batch ingest** and the **Decision user loop** work together in your setup.

---

## Summary

- **Batch ingest** = Phase 1 only: many `Ingest/*.md` notes are processed in one run; for **each** note a **Decision Wrapper** is created/updated; **no** moves/renames.
- **Decision user loop** = you review wrappers in `Ingest/Decisions/`, set `approved: true` and pick an option (A–G or `approved_path`); **Phase 2** runs only after that, via EAT-QUEUE (and CHECK_WRAPPERS).

So: batch ingest fills the loop with wrappers; the loop is the gate before any move; applying decisions can happen in batch when you run EAT-QUEUE.

---

## 1. What batch ingest does (Phase 1 only)

When you run **INGEST MODE** (e.g. “INGEST MODE – safe batch autopilot” or “Process Ingest”):

- The pipeline runs on **multiple** `Ingest/*.md` notes (e.g. up to 5 per run, per `para-zettel-autopilot`).
- For **each** note it: backup → classify_para → frontmatter-enrich → subfolder-organize → optional split/distill/hub/task-reroute → **create/refresh a Decision Wrapper**.
- **Universal Decision Wrapper (since 2026-03-03)**: every Ingest note that doesn’t already have an approved decision gets a wrapper, regardless of confidence. So a batch of 5 notes → 5 wrappers under `Ingest/Decisions/`.
- **No move/rename in Phase 1**: all path decisions are only recorded in the wrapper (options A–G); the original note stays in `Ingest/`.
- After creating wrappers, the rule ensures a **CHECK_WRAPPERS** queue entry exists so the next EAT-QUEUE run will consider wrappers.

So **batch ingest** = “run Phase 1 on many notes and create one Decision Wrapper per note.”

---

## 2. What the Decision user loop is

- **Wrappers** live in `Ingest/Decisions/` (e.g. `Decision-for-<slug>--<date>.md`), with lettered options A–G (candidate PARA paths) and `original_path` pointing to the Ingest note.
- **Your part**: open a wrapper, choose an option (e.g. option A) and set `approved: true` (and optionally `approved_path` or “Thoughts”).
- **Phase 2 (apply-mode)** runs only when EAT-QUEUE (or the CHECK_WRAPPERS logic) sees an **approved, unprocessed** wrapper. Then it:
  - Resolves `hard_target_path` from your choice,
  - Runs apply-mode ingest on the **original** note (snapshot, then `obsidian_move_note` / `obsidian_rename_note` into that path),
  - Marks the wrapper as processed and moves it to `4-Archives/Ingest-Decisions/`.

So the **Decision user loop** = “review wrapper → approve and choose path → next EAT-QUEUE applies that decision (Phase 2).”

---

## 3. How they interact

- **Batch ingest (Phase 1)**  
  - Produces **many wrappers** in one run (one per note in the batch).  
  - Does **not** move anything; it only proposes paths via wrappers.

- **Decision user loop**  
  - You approve wrappers one-by-one (or in bulk by editing several and setting `approved: true`).  
  - Approvals are the **only** trigger for Phase 2 moves.

- **EAT-QUEUE / CHECK_WRAPPERS**  
  - **Step 0 (always-check wrappers)** runs at the start of every EAT-QUEUE: it scans `Ingest/Decisions/`, and for every wrapper with `approved: true` and not yet processed, it runs **apply-mode ingest** for that note (move + archive wrapper).  
  - So in **one** EAT-QUEUE run you can **apply** many decisions (batch apply), even though each decision was made by you in the loop.

So:

- **Batch ingest** → creates many wrappers (batch of “proposals”).
- **Decision user loop** → you approve and choose paths (no batch requirement; you can do one or many).
- **EAT-QUEUE** → in one run it can apply **all** approved wrappers (batch apply of your decisions).

Ordering is enforced so that CHECK_WRAPPERS / wrapper processing is done **before** other queue entries (e.g. further INGEST MODE work), and destructive ingest moves for a note under `Ingest/` only happen when that note’s decision comes from an approved wrapper (via CHECK_WRAPPERS or an injected wrapper-based INGEST MODE entry). So batch ingest and the Decision user loop “play together” by: batch creating wrappers, then you approving in the loop, then EAT-QUEUE batching the apply step for all approved wrappers.

## Full output

_Paste the full AI response below._

>  

## Key insights

_Extract the few pieces that are actually useful or worth revisiting._

-  
-  
-  

## TL;DR

_Short summary of why this output matters (or "nothing useful" if so)._

-

## Review Needed
Proposed para-type: archive. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.