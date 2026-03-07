---
name: express-apply-from-wrapper
description: Reads an approved Decision Wrapper (wrapper_type mid-band-refinement or force-wrapper, pipeline express), resolves original_path and approved_option, and re-runs autonomous-express on the note with approved_option as express_view override. Invoked by EAT-QUEUE Step 0 when applying an approved refinement wrapper for the express pipeline.
---

# express-apply-from-wrapper

## When to use

- **EAT-QUEUE Step 0** (auto-eat-queue): When processing a wrapper with `approved: true`, `wrapper_type: mid-band-refinement` or `force-wrapper`, and `pipeline: express`, and the user chose an outline/view option.
- After the user has approved a refinement wrapper that proposed express options (e.g. outline style, express_view); this skill runs the actual express pipeline with the chosen option.

## Instructions

1. **Read wrapper**: The wrapper path and frontmatter are in context (Step 0 passes the wrapper being processed). Read frontmatter: `original_path`, `approved_option`, `approved_path`, `user_guidance` (or extract from Thoughts block). Resolve the chosen option (A–G) to an **express_view** or **outline style** value (e.g. option A = "summary", B = "full outline", or option text = view name).

2. **Resolve express params**: Set **express_view** (or equivalent) from `approved_option` / wrapper body so the express pipeline uses the user's choice. If the wrapper body or options describe a view (e.g. "publish-ready", "minimal"), use that as the express_view override.

3. **Re-run autonomous-express**: Run the **autonomous-express** pipeline on the note at `original_path` with:
   - **express_view** override from the resolved option.
   - **user_guidance** from the wrapper's Thoughts block (if any) as soft context.
   - Normal backup/snapshot gates and confidence rules apply; this run may perform the outline/Related/CTA steps that were previously proposed in the refinement wrapper.

4. **No wrapper writes**: This skill does not update or move the wrapper; Step 0 updates the wrapper (e.g. `used_at`, `processed: true`) and moves it to the archive after the express run completes.

## MCP / pipeline

- `obsidian_read_note` — read wrapper and original note when needed.
- The autonomous-express pipeline (auto-express context rule) is run by the agent with the overrides in context; no dedicated MCP for "run express" — the agent executes the pipeline steps (related-content-pull, express-mini-outline, call-to-action-append, etc.) using the overrides.

## Reference

- [Cursor-Skill-Pipelines-Reference](3-Resources/Cursor-Skill-Pipelines-Reference.md) — apply-from-wrapper table; Decision Wrappers (clunk).
- [auto-eat-queue](.cursor/rules/context/auto-eat-queue.mdc) — Step 0 Path-apply branch for pipeline: express.
- [auto-express](.cursor/rules/context/auto-express.mdc) — autonomous-express pipeline; express_view.
