---
name: distill-highlight-color
description: Applies Highlightr colors to note content after distill using master key and project highlight_key; uses color theory (analogous for related ideas, complementary for contrasts). Supports 50–70% coverage target (configurable), perspective param for lens-focused analogous mapping, and coverage_adapted logging. Use when running full-autonomous-ingest or autonomous-distill pipelines, after obsidian_distill_note or standard distill layers.
---

# distill-highlight-color

## When to use

- After `obsidian_distill_note` in the ingest pipeline, or after standard distill layers in the autonomous-distill pipeline.
- Only when confidence is **≥80%** (structural highlight edits align to **≥85%** per pipeline reference where applicable); otherwise skip or propose only.

## Parameters (optional)

- **Coverage**: Target **50–70%** of meaningful spans (configurable via [Second-Brain-Config](3-Resources/Second-Brain-Config.md) `depths.highlight_coverage_min` or skill/run param). When content length or complexity is available (e.g. via readability-flag integration), **auto-adjust** within this range and log as **coverage_adapted: X%** (e.g. 62%) in the pipeline log for MOC.
- **Perspective**: When set (e.g. `perspective: "combat systems"` or `perspective: "performance"`), map **lens-focused** spans to analogous colors—same theme = same hue family. Perspective narrows which spans get highlighted and how they are grouped by color. Read from note frontmatter **`highlight_perspective`** when not passed explicitly.

## Instructions

1. **Read the color key**: Use [Highlightr-Color-Key.md](3-Resources/Highlightr-Color-Key.md) — read **both** the semantic table (Section 1) and the **exact Highlightr storage format section** (Section 2). The pipeline must use **only** the format specified there (inline CSS or CSS classes from the key). **Never** use `==text==^{color}` or native Obsidian `==text==` for semantic highlights. If the note has frontmatter `highlight_key`, use it for project overrides; otherwise fall back to the master key. If the note has **`highlight_perspective`**, use it for lens-focused analogous mapping.

2. **Color theory**:
   - **Analogous colors** (e.g. blue–green): use for related ideas, continuity, same theme across sections or linked project files. When **perspective** is set, apply analogous colors for spans that match the lens.
   - **Complementary colors**: use for contrasts, tension, opposing ideas (e.g. pain points vs benefits).

3. **Apply highlights**:
   - Use chain-of-thought to pick spans (key concepts, quotes, actions, caveats, etc.) and assign colors from the key. Aim for **50–70% coverage** of meaningful content unless config or param overrides.
   - Wrap each span in the **exact format from the key**, and **always** add `data-highlight-source="agent"` to every `<mark>` so agent highlights can be distinguished from user (Highlightr UI) highlights (see Highlightr-Color-Key Section 3). Example: `<mark data-highlight-source="agent" style="background: #...">text</mark>` for inline CSS, or `<mark data-highlight-source="agent" class="hltr-yellow">text</mark>` if CSS classes are enabled. Do not use `==text==^{color}`.
   - Apply via `obsidian_search_replace` (path, old_text, new_text) for each span, or batch via `obsidian_update_note` if doing many edits. **Requires backup first** (obsidian_create_backup) before in-place edits.

4. **Observability**: Log **coverage %** (and **coverage_adapted** when adaptive) and **perspective** used in [Distill-Log.md](3-Resources/Distill-Log.md) so MOC queries (e.g. Vault-Change-Monitor) can aggregate.

5. **Verify**: Re-read the note to confirm highlights are applied correctly and no structure was broken.

## MCP tools

- `obsidian_read_note` — read note and color key docs
- `obsidian_search_replace` — wrap spans in the key's storage format (e.g. `<mark style="background: #...">` or `<mark class="...">` from Highlightr-Color-Key.md Section 2) (destructive; backup first)
- `obsidian_update_note` — alternative for bulk highlight edits (destructive; backup first)

## Confidence gate

**≥80%**: Execute highlight edits. **<80%**: Propose spans and colors only; do not write.

## Reference

- [3-Resources/Highlightr-Color-Key.md](3-Resources/Highlightr-Color-Key.md) — master key (Section 1 semantics + Section 2 exact storage format), project-specific guidelines, `highlight_key` fallback.
