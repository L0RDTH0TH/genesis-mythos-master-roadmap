---
title: Prompt-Crafter Structure — Detailed
created: 2026-03-06
tags: [pkm, second-brain, prompt-crafter, structure, level-3]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/README]]", "[[Prompt-Crafter-Structure-Mid-Level]]", "[[MCP-Tools]]", "[[Cursor-Skill-Pipelines-Reference]]"]
---

# Prompt-Crafter Structure — Detailed

This document lists every file, field, and rule involved in the prompt-crafter: Config block and keys, each template file and its role, queue payload contract and fallback order, validation rules and allowed enums, auto-eat-queue dispatch and Run steps, confidence-loops and Parameters tunables, and cross-references. Use it to implement or debug param assembly and pass-through.

---

## Config: prompt_defaults (full)

**File**: `3-Resources/Second-Brain-Config.md`

| Key | Type | Example / notes |
|-----|------|-----------------|
| prompt_defaults.ingest.context_mode | string | strict-para (ingest/wrapper); fallback organize for re-org |
| prompt_defaults.ingest.max_candidates | number | 7 (wrapper must pad to 7 per Pipelines) |
| prompt_defaults.ingest.rationale_style | string | concise (MCP-Tools optional) |
| prompt_defaults.organize.context_mode | string | organize |
| prompt_defaults.organize.max_candidates | number | 5 |
| prompt_defaults.profiles | object | Named overrides, e.g. project-priority: { context_mode: project-strict, max_candidates: 5 } |

Safety note (in Config or Configs.md): Non-destructive defaults only; params influence proposals but require approved: true for any move/rename per Pipelines § Phase 2. No auto-approval injection.

**Pre-check**: If MCP contracts change (e.g. new param like min_score_threshold in x_semantic_search per MCP-Tools), add to prompt_defaults validation set. Run health_check (per Logs § Health check flow) post-sync.

---

## Template files (full)

**Location**: `Templates/Prompt-Components/`

| File | Content / role |
|------|----------------|
| **Base-Prompt.md** | Assembly-order comment: "# Order: Config defaults → Param-Overrides → Guidance-Default → Validation-Snippet." Canonical trigger placeholder {mode} from Pipelines fixed list. |
| **Param-Defaults.md** | Placeholders {{prompt_defaults.ingest.context_mode}}, etc. Optional Templater dynamic: {{tp.file.content \| yaml_load \| get('prompt_defaults.ingest.context_mode')}}. Validation snippet: max_candidates ≤10 (MCP limit per MCP-Tools). |
| **Param-Overrides.md** | References Config profiles; user-selectable; merge over pipeline default when profile chosen. |
| **Guidance-Default.md** | Fixed string: use note user_guidance when present; else queue prompt; apply guidance_conf_boost if set; do not override user_guidance. |
| **Error-Handling-Template.md** | If invalid: log to Errors.md with trace per mcp-obsidian-integration. |
| **Skill-Chain.md** | Optional; list skills valid for pipeline per Cursor-Skill-Pipelines-Reference. |

Templates.md documents flow and assembly order; no mobile-specific components.

---

## Queue payload and fallback (full)

**File**: `3-Resources/Second-Brain/Queue-Sources.md`

- **Optional field**: `params` (object) on a queue entry. Example: `{"mode":"INGEST MODE","source_file":"Ingest/Note.md","id":"req-1","params":{"context_mode":"strict-para","max_candidates":7}}`.
- **Fallback order**: 1. Queue entry params 2. user_guidance frontmatter (merge) 3. Config prompt_defaults/profiles 4. MCP tool defaults (e.g. max_candidates: 3 per MCP-Tools).
- **Contract validation**: EAT-QUEUE rejects invalid params pre-dispatch (e.g. rationale_style not in ['concise','detailed','bullet','technical'] per MCP-Tools); append to Errors.md.

**File**: `.cursor/rules/context/auto-eat-queue.mdc`

- **Step 5 (Dispatch)** — Before running a pipeline for an entry with `params`: merge per fallback chain; validate merged params against MCP-Tools.md (rationale_style enum; context_mode and max_candidates ranges). If invalid: skip dispatch, append to 3-Resources/Errors.md, append failure to Watcher-Result, continue. If valid: pass merged params into pipeline context.
- **Step 6 (Run)** — Guidance-aware merge: append user_guidance text to rationale_style if compatible; log full merged params to Prompt-Log.md. Do not override user_guidance.

---

## Validation rules (MCP-Tools alignment)

| Param | Allowed / contract |
|-------|---------------------|
| context_mode | wrapper, midband, organize, fallback (propose_para_paths); pipeline-specific (e.g. strict-para for ingest). |
| rationale_style | concise, detailed, bullet, technical (MCP-Tools); default concise when omitted. |
| max_candidates | string "3"–"8" in MCP; doc validation max_candidates ≤10; wrapper uses 7. |

Unknown keys: ignore or log per Error Handling Protocol. Unhandled params → Errors.md.

---

## Confidence and Parameters (full)

- **confidence-loops.mdc**: Optional **crafted-params bump** — when crafted params used, add +5% (or configured value) to pre_loop_conf floor; tunable via Parameters.md (e.g. crafted_params_conf_boost: 5); default 0 if unset.
- **Parameters.md**: crafted_params_conf_boost (0–10); prompt_defaults read by prompt-crafter and rules for MCP pass-through; queue payload overrides take precedence.
- **Pipelines.md**: Param'd MCP calls — always ensure_backup (or create_backup) before any MCP call that uses queue params or prompt-crafter output.

---

## Prompt-Log structure (full)

**File**: `3-Resources/Prompt-Log.md`

| Field | Description |
|-------|-------------|
| timestamp | ISO 8601 or YYYY-MM-DD HH:MM |
| pipeline | mode (e.g. INGEST MODE, ORGANIZE MODE) |
| params | Params as used (merged from queue + user_guidance + Config) |
| source | macro \| default |
| outcome | valid \| invalid |
| merge_trace | Optional; when guidance-aware merge applied |

Append per craft or per EAT-QUEUE when params are merged/validated. Logs.md row: Prompt-Log \| Crafted/merged params, validation outcome, merge trace \| Append per craft/EAT-QUEUE; Dataview aggregate in Vault-Change-Monitor MOC for "crafted runs this week."

---

## Skills and backbone (full)

- **Skills.md**: Row "prompt-crafter \| Assemble/validate params \| Used in ingest/organize pipelines; slots before classify_para" (doc-only; optional skill implementation follow-up).
- **Responsibilities-Breakdown.md**: prompt-crafter \| Assemble/inject params \| Config read, template concat, queue append; owns validation but delegates MCP calls.
- **Backbone.md** § Stack: Prompt-Crafter — Laptop layer for MCP param assembly from config/templates; stabilizes ingest/organize via defaults and validation.
- **Rules.md** § Always-applied: guidance-aware — now merges crafted params with user_guidance.
- **MCP-Tools.md**: obsidian_propose_para_paths — rationale_style optional; defaults to concise.

---

## Cross-references

- Config and consumers: [[Configs]], [[Parameters]]
- Queue and dispatch: [[Queue-Sources]], [[.cursor/rules/context/auto-eat-queue|auto-eat-queue]]
- Commander: [[3-Resources/Plugins-Usage/Commander-Plugin-Usage|Commander-Plugin-Usage]]
- Templates: [[Templates]], `Templates/Prompt-Components/`
- Logs: [[Logs]], Prompt-Log.md
- Testing: [[Testing]] § Fixtures (prompt-crafter subdir, config.yaml + base-prompt.md = expected-queue.jsonl; integration test pad to 7)
