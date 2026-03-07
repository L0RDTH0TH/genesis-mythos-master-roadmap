---
name: distill-apply-from-wrapper
description: Reads an approved Decision Wrapper (wrapper_type mid-band-refinement or force-wrapper, pipeline distill), resolves original_path and approved_option, and re-runs autonomous-distill on the note with approved_option as distill_lens override. Invoked by EAT-QUEUE Step 0 when applying an approved refinement wrapper for the distill pipeline.
---

# distill-apply-from-wrapper

## When to use

- **EAT-QUEUE Step 0** (auto-eat-queue): When processing a wrapper with `approved: true`, `wrapper_type: mid-band-refinement` or `force-wrapper`, and `pipeline: distill`, and `hard_target_path` or path resolution indicates a distill apply (user chose a depth/layer option).
- After the user has approved a refinement wrapper that proposed distill options (e.g. 1/2/3 layers, or a specific distill_lens); this skill runs the actual distill with the chosen option.

## Instructions

1. **Read wrapper**: The wrapper path and frontmatter are in context (Step 0 passes the wrapper being processed). Read frontmatter: `original_path`, `approved_option`, `approved_path`, `user_guidance` (or extract from Thoughts block). Resolve the chosen option (A–G) to a **distill_lens** or **depth/layer** value (e.g. option A = "1 layer", B = "2 layers", C = "3 layers", or option text = lens name).

2. **Resolve distill params**: Set `distill_lens` (or equivalent) from `approved_option` / wrapper body so the distill pipeline uses the user's choice. If the wrapper body or options describe a lens (e.g. "beginner", "executive"), use that as the lens override. If options are depth-only, pass depth/layers to the distill run.

3. **Re-run autonomous-distill**: Run the **autonomous-distill** pipeline on the note at `original_path` with:
   - **distill_lens** (or depth) override from the resolved option.
   - **user_guidance** from the wrapper's Thoughts block (if any) as soft context.
   - Normal backup/snapshot gates and confidence rules apply; this run may perform the structural distill (bold, highlight, TL;DR) that was previously proposed in the refinement wrapper.

4. **No wrapper writes**: This skill does not update or move the wrapper; Step 0 updates the wrapper (e.g. `used_at`, `processed: true`) and moves it to the archive after the distill run completes.

## MCP / pipeline

- `obsidian_read_note` — read wrapper and original note when needed.
- The autonomous-distill pipeline (auto-distill context rule) is run by the agent with the overrides in context; no dedicated MCP for "run distill" — the agent executes the pipeline steps (backup, distill_note with lens/depth, layer-promote, etc.) using the overrides.

## Reference

- [Cursor-Skill-Pipelines-Reference](3-Resources/Cursor-Skill-Pipelines-Reference.md) — apply-from-wrapper table; Decision Wrappers (clunk).
- [auto-eat-queue](.cursor/rules/context/auto-eat-queue.mdc) — Step 0 Path-apply branch for pipeline: distill.
- [auto-distill](.cursor/rules/context/auto-distill.mdc) — autonomous-distill pipeline; distill_lens, depth.
