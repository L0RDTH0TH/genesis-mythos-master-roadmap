---
title: User Flow — Prompt-Crafter (High-Level)
created: 2026-03-06
tags: [pkm, second-brain, prompt-crafter, user-flow, level-1]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/README]]", "[[Prompt-Crafter-Structure-High-Level]]", "[[Commander-Plugin-Usage]]"]
---

# User Flow — Prompt-Crafter (High-Level)

This document describes the **user's path** through the prompt-crafter (laptop-only): how the user crafts a prompt with pinned params, what they see (preview vs queue append), and the main gates (validation, merge with user_guidance). It answers "what does the user do to get consistent MCP params, and what happens when they run EAT-QUEUE?" at a high level.

---

## User starts crafting (trigger → assembly)

- **User runs a Commander macro** (e.g. Craft Prompt, Craft Ingest Default)  
  Macro prompts for **pipeline** (ingest | organize) and **profile** (default | project-priority). Assembly pulls from [[3-Resources/Second-Brain-Config|Second-Brain-Config]] prompt_defaults and [[3-Resources/Second-Brain/Templates#Prompt-Components (laptop)|Templates/Prompt-Components]]. Output is a crafted prompt string (trigger + params).

- **User may paste to Cursor** or use **Craft and Queue** to append to `.technical/prompt-queue.jsonl` with validated params. If validation fails, macro aborts and logs to Prompt-Log.md; no queue append.

- **No macro** — User can still type a mode (e.g. INGEST MODE) in Cursor; the agent uses Config defaults when no queue params are present (fallback chain: queue params → user_guidance → Config → MCP defaults).

---

## Main gate: validation before use

- **Before paste or queue append**: Params are checked (e.g. max_candidates ≤10, rationale_style in allowed enum per MCP-Tools). **Invalid** → abort; log to Prompt-Log.md (and optionally Errors.md per Error Handling Protocol). **Valid** → paste or append.

- **When EAT-QUEUE runs**: auto-eat-queue validates merged params (queue + user_guidance + Config) against MCP-Tools contracts before dispatching. **Invalid** → skip that entry; append to Errors.md; append failure to Watcher-Result. **Valid** → pass merged params into the pipeline; classify_para, propose_para_paths, subfolder_organize receive them.

So: the user either gets a working crafted prompt/queue entry (valid) or sees an abort/failure and a log entry (invalid).

---

## Ingest / organize with crafted params (user outcome)

- **Phase 1 (INGEST MODE or queue entry mode INGEST MODE)**  
  Agent runs full-autonomous-ingest with **crafted params** (e.g. context_mode: strict-para, max_candidates: 7). User sees the same as before: classify → enrich → organize proposal → Decision Wrapper A–G. Params make path proposals more stable; they do **not** auto-approve. User still checks one option and sets approved: true.

- **Phase 2 (EAT-QUEUE)**  
  Step 0 processes approved wrappers (apply-mode move/rename). Other queue entries (e.g. DISTILL MODE, ORGANIZE MODE) run with their merged params. User sees Watcher-Result line(s) and note(s) in PARA (or wrapper archived).

So: crafting gives **consistent params**; the rest of the flow (Decision Wrapper, approval, EAT-QUEUE apply) is unchanged from the user's perspective.

---

## Safety invariants the user can rely on (prompt-crafter)

- **No move without approval** — Crafted params influence proposals only. approved: true is still required for any move/rename (Pipelines § Phase 2). No auto-approval injection from params.
- **Invalid params never dispatch** — EAT-QUEUE rejects invalid params pre-dispatch; the user sees a failure line in Watcher-Result and an entry in Errors.md instead of a bad run.
- **Merge, don't override** — When the note has user_guidance (or queue prompt), it is **merged** with crafted params (e.g. appended to rationale_style); user_guidance is never overwritten by defaults.
