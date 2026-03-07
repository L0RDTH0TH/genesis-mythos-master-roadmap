---
title: Prompt-Log
created: 2026-03-06
tags: [second-brain, prompt-crafter, logs]
para-type: Resource
status: active
links: ["[[3-Resources/Second-Brain/Logs|Logs]]", "[[3-Resources/Vault-Change-Monitor|Vault-Change-Monitor]]"]
---

# Prompt-Log

Crafted/merged params, validation outcome, and merge trace for prompt-crafter and EAT-QUEUE runs that use queue `params` or prompt-crafter assembly. Append per craft or per EAT-QUEUE when params are merged or validated. Dataview aggregate in [[3-Resources/Vault-Change-Monitor|Vault-Change-Monitor]] MOC for "crafted runs this week."

## Log line structure

| Field | Description |
|-------|-------------|
| timestamp | ISO 8601 or YYYY-MM-DD HH:MM |
| pipeline | mode (e.g. INGEST MODE, ORGANIZE MODE) |
| params | Params as used (merged from queue + user_guidance + Config) |
| source | macro \| default |
| outcome | valid \| invalid |
| merge_trace | Optional: when guidance-aware merge applied |

## Example

`2026-03-06 12:00 | pipeline: INGEST MODE | params: {"context_mode":"strict-para","max_candidates":7} | source: macro | outcome: valid | merge_trace: user_guidance merged into rationale_style`
