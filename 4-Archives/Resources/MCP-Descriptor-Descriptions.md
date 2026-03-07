---
title: MCP Descriptor Descriptions
created: 2026-02-25
tags: [mcp, cursor, second-brain]
para-type: Resource
status: active
links: [[Resources Hub]]
---

# MCP Descriptor Descriptions

Suggested `description` text for Obsidian PARA-Zettel MCP tools when descriptors have empty strings. Apply these in the MCP server repo or in the project mcps cache if editable.

- **obsidian_classify_para**: Classify note into PARA and detect project context. ALWAYS prefer linking to EXISTING projects over creating new ones. Output strict JSON only:
  - `para_type`: "Project" | "Area" | "Resource" | "Archive"
  - `project_name`: exact existing project name or null
  - `subfolder_hint`: "Audits" | "Tasks" | "Actions" | "Reviews" | null
  - `confidence`: 0–100
  - `reasoning`: short explanation
  - **STRICT PRIORITY RULES:** (1) First scan for mentions of known projects (e.g. 1-Projects/); (2) audit/review/report → Resource, project_name = audited project, subfolder_hint: Audits; (3) mostly tasks/action list + project mention → Resource, subfolder_hint: Tasks; (4) NEW Project only if new goals/deadlines and no existing project reference; (6) never use 'Audit', 'Tasks', 'Review' as project_name.
  - **Confidence scoring:** 90–100 = strong match to existing project; 85–89 = reasonable inference; 75–84 = plausible but weak linkage; ≤74 = truly ambiguous. **Bonuses (+10–15):** title has "audit"/"review"/"test"/"notes on"/"summary of"/"log" → Resource + existing project; many `- [ ]`/TODO → Resource + Tasks; mention of known hub/project name → +15. Never below 80 if any existing project/area weakly referenced; default floor for Ingest/ notes is 75 unless content-free.
- **obsidian_split_atomic**: "Split a multi-idea note into atomic child notes; split_on (default '## ') defines section boundary; returns child paths."
- **obsidian_append_to_hub**: "Append a wikilink and summary to a hub/MOC note (hub_name, e.g. 'Resources Hub' or 'Resurface')."

**obsidian_ensure_structure** already includes `folder_path` in the schema (optional vault-relative path to create recursively).
