---
title: User Flow — Prompt-Crafter (Detailed)
created: 2026-03-06
tags: [pkm, second-brain, prompt-crafter, user-flow, level-3]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/README]]", "[[Prompt-Crafter-Structure-Detailed]]", "[[Queue-Sources]]", "[[auto-eat-queue]]"]
---

# User Flow — Prompt-Crafter (Detailed)

This document is the full breakdown of **user choices** and **system response** for the prompt-crafter: every Commander option, validation outcome, queue payload shape, EAT-QUEUE merge and dispatch, guidance-aware merge, logging (Prompt-Log, Errors, Watcher-Result), and error paths. Use it to implement macros, debug param flow, or trace why an entry was rejected.

---

## Commander macro: full option set (user → system)

- **Macro:** "Craft Prompt" (or "Prompt Craft"). Documented in [[3-Resources/Plugins-Usage/Commander-Plugin-Usage|Commander-Plugin-Usage]] § Prompt-crafter macros.
- **User is presented with:** Pipeline picker (ingest | organize) and profile picker (default | project-priority). Optional: "Preview Assembly" vs "Craft and Queue."
- **User choices and system response:**
  - **Pipeline: ingest, Profile: default** → Assembly from prompt_defaults.ingest. Output: trigger phrase (e.g. INGEST MODE) + params object { context_mode, max_candidates, rationale_style }.
  - **Pipeline: ingest, Profile: project-priority** → Merge prompt_defaults.profiles.project-priority over ingest. Output: params include context_mode: project-strict, max_candidates: 5.
  - **Pipeline: organize, Profile: default** → prompt_defaults.organize. Output: trigger + params { context_mode: organize, max_candidates: 5 }.
  - **Preview Assembly** → Paste assembled prompt to temp note; no queue append. commander_macro: craft_prompt_preview. No validation required for paste-only.
  - **Craft and Queue** → Validate params (max_candidates ≤10; rationale_style in ['concise','detailed','bullet','technical']; context_mode allowed). If **invalid**: abort; append to Prompt-Log.md (timestamp, pipeline, params, source: macro, outcome: invalid); do not append to queue. If **valid**: append one line to `.technical/prompt-queue.jsonl`: `{"mode":"INGEST MODE","source_file":"<path>","id":"<requestId>","params":{...}}` (and optional prompt); append to Prompt-Log (outcome: valid).
- **Sub-macros:** "Craft Ingest Default", "Craft Organize Custom" — Same flow with pipeline/profile fixed; user only chooses Preview vs Craft and Queue and (if queue) source_file.

---

## Queue entry shape and validation (full)

- **Queue line (example):** `{"mode":"INGEST MODE","source_file":"Ingest/My-Note.md","id":"req-1","params":{"context_mode":"strict-para","max_candidates":7,"rationale_style":"concise"}}`
- **Validation (EAT-QUEUE step 5, auto-eat-queue):**
  - **Merge** in order: 1. Queue entry params 2. user_guidance from note at source_file (merge, do not overwrite) 3. Config prompt_defaults for mode (or profile if specified) 4. MCP tool defaults.
  - **Contract check:** rationale_style in ['concise','detailed','bullet','technical']; max_candidates within MCP range (e.g. ≤10 per doc); context_mode allowed for the tool.
  - **If invalid:** Skip dispatch for this entry; append to 3-Resources/Errors.md per Error Handling Protocol (pipeline, stage, affected path, suggested fix); append to Watcher-Result: `requestId: <id> | status: failure | message: "invalid params: ..." | trace: ... | completed: <ISO8601>`. Continue to next entry.
  - **If valid:** Pass merged params into pipeline context; run pipeline (classify_para, propose_para_paths, subfolder_organize receive params).

---

## Guidance-aware merge (detailed)

- **Trigger:** Note at source_file has user_guidance frontmatter, or queue entry has non-empty **prompt** field, or note has tag #guidance-aware (guidance-aware.mdc).
- **Behavior:** feedback-incorporate (or equivalent) loads guidance. Merge: append user_guidance text to rationale_style if compatible (e.g. "concise + explain rankings"). Do not override user_guidance; inject defaults only where missing.
- **Logging:** Full merged params (including merge result) written to Prompt-Log.md: timestamp, pipeline, params (as used), source (macro | default), outcome (valid), merge_trace (e.g. "user_guidance merged into rationale_style").
- **User choices:** (A) Add user_guidance to note and/or prompt to queue entry. (B) Omit for default-only params. For (A), next EAT-QUEUE run is guidance-aware; merge and log apply.

---

## Error paths (user-visible)

| Scenario | System response | User sees |
|----------|-----------------|-----------|
| **Macro: invalid params** | Abort; no queue append; log to Prompt-Log (outcome: invalid). | Error message or log; no new queue line. |
| **EAT-QUEUE: invalid merged params** | Skip entry; append to Errors.md; append failure to Watcher-Result. | Watcher-Result line: status: failure, message re params. Errors.md entry with trace and suggested fix. |
| **EAT-QUEUE: source_file missing** | Skip entry; Watcher-Result failure "source_file not found." | Same as above; no pipeline run. |
| **Unknown mode** | Skip entry; Watcher-Result failure "unknown or invalid mode." | Same. |

---

## Prompt-Log and audit (user/debugger)

- **When written:** Per craft (Craft and Queue) and per EAT-QUEUE run when params are merged or validated.
- **Fields:** timestamp (ISO 8601 or YYYY-MM-DD HH:MM), pipeline, params (as used), source (macro | default), outcome (valid | invalid), merge_trace (optional).
- **User/debugger:** Open 3-Resources/Prompt-Log.md to see which params were used and whether validation passed. Vault-Change-Monitor MOC can aggregate "crafted runs this week" via Dataview.

---

## Cross-references

- Structure (what exists): [[Prompt-Crafter-Structure-Detailed]]
- Queue contract and fallback: [[Queue-Sources]]
- Dispatch and validation: [[.cursor/rules/context/auto-eat-queue|auto-eat-queue]]
- Commander macro setup: [[3-Resources/Plugins-Usage/Commander-Plugin-Usage|Commander-Plugin-Usage]]
- Guidance contract: [[.cursor/rules/always/guidance-aware|guidance-aware]]
- Error Handling Protocol: [[.cursor/rules/always/mcp-obsidian-integration|mcp-obsidian-integration]] § Error Handling Protocol
