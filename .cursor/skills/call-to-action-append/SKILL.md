---
name: call-to-action-append
description: Appends a call-to-action callout at the end of a note (e.g. Share/Publish?) with optional color by action type or project. Use at the end of the autonomous-express pipeline.
---

# call-to-action-append

## When to use

- At the **end** of the autonomous-express pipeline.
- **Always** run when the pipeline is generating express output (no confidence gate).

## Instructions

1. **Choose CTA**: Based on note type and content, pick an appropriate callout, e.g.:
   - `> [!tip] Share/Publish?`
   - `> [!todo] Next step: ...`
   - Customize by project or action type if the note has `project-id` or frontmatter.

2. **Append**: Use `obsidian_update_note`(path, content: "\n\n" + callout_block, mode: append). No overwrite; append only.

3. **Optional**: Color or theme the callout border via CSS snippet tied to project key; document in Highlightr or pipeline reference. This skill only appends the callout text.

## MCP tools

- `obsidian_update_note` — append CTA callout (mode: append)

## Confidence gate

**Always** — append whenever the express pipeline runs.
