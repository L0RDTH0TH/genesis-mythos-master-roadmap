---
name: name-enhance
description: Proposes or applies a better note filename (and optionally frontmatter title) from content and context, with layered protections so MOCs, hubs, index/home, and project-root notes are not auto-renamed unless there is explicit intent. Use during ingest (propose only), organize (opportunistic), or NAME-REVIEW queue (explicit sweeps).
---

# name-enhance

## When to use

- **Ingest** (context `ingest`): After frontmatter-enrich, before subfolder-organize; when current filename stem is vague/untitled. **Never applies rename in ingest** — returns suggested_name for subfolder-organize to use in move path. See [[3-Resources/Second-Brain/Naming-Conventions|Naming-Conventions]].
- **Organize** (context `organize`): During autonomous-organize, after subfolder-organize and before optional obsidian_rename_note; opportunistically improve name when vague or confidence very high.
- **Name-review** (context `name-review`): When processing NAME-REVIEW queue mode; apply renames for Regular notes when confidence ≥85% (with snapshot). Log to Name-Review-Log or Organize-Log.

## Inputs

- **path** (required): Vault-relative note path.
- **context**: `ingest` | `organize` | `name-review`.
- **explicit_rename_request** (optional): Caller passes a dict (e.g. `{ target: "Old MOC", new: "New MOC Name" }`) so the skill does not parse ingest content every time. When present, use it to allow apply for that target (MOC/project root/index). Skill may also parse ingest note content or frontmatter for convenience (see Explicit request parsing below).

## Role detection

Detect the note's role to apply protection rules:

| Role | Detection (heuristic) |
|------|------------------------|
| **Hub** | Filename matches `* Hub.md` → do not rename (excluded). |
| **Index / Home / Dashboard** | Filename matches exactly or alias-linked as vault entry point (e.g. Home.md, Index.md, Vault-Map.md) → protect like Hub. |
| **MOC** | Filename matches `* MOC.md` or similar; or frontmatter/link pattern (e.g. moc-for, linked as "X MOC"). |
| **Project root** | Note path is `1-Projects/<ProjectName>/<ProjectName>.md` or similar (single note at project root level). |
| **Regular** | Everything else. |

## Confidence tiers

Make decisions explicit; document in logs.

| Confidence (Regular notes) | Action (Regular) | Action (protected roles w/o explicit request) |
| -------------------------- | ----------------- | --------------------------------------------- |
| ≥ 90% | Auto-apply (with snapshot) | Proposal only |
| 85–89% | Apply in ingest/organize; propose in name-review | Proposal only |
| 70–84% | Proposal + log (mid-priority fix candidate) | Proposal only |
| < 70% | No suggestion (too vague/uncertain) | No suggestion |

**Ingest**: Skill never applies rename; always proposal only. Subfolder-organize commits the name via move when suggested_name and confidence ≥85% and not protected.

## Vague detection

Treat as vague (candidate for name-enhance) when filename **stem** (no extension) matches (case-insensitive or normalized):

- `Untitled`, `Untitled N`, `Untitled Document`, `Untitled Document N`, `Untitled-*`
- `Note`, `Document`, `New Note`, `New`, `Scratch`, `temp`, `test`, `clip`, `paste`, `idea`, `thought`
- Empty stem or numeric-only (e.g. `1`, `42`)

In `name-review` context, optionally suggest for any note (not only vague).

## Explicit request parsing (forgiving)

- **Caller**: Pass `explicit_rename_request` as optional dict → cleanest; skill uses it when present.
- **Ingest note content**: Look for patterns such as "rename MOC … to …", "change project … name to …", "retitle … as …".
- **Ingest note frontmatter**: `rename_request: { target: "Old MOC", new: "New MOC Name" }` (structured).

When a protected note (MOC, project root, index) is the target of an explicit request, allow apply per confidence tiers; otherwise proposal only.

## Output shape

Return (for UX and logging) a structure like:

```json
{
  "suggested_name": "my-new-idea-about-x-2025-03-01-1430.md",
  "applied": false,
  "confidence": 92,
  "protection_triggered": null,
  "reason": "Suggested from first heading; ingest context so not applied",
  "old_stem": "Untitled 7"
}
```

- **suggested_name**: Full filename in `kebab-slug-YYYY-MM-DD-HHMM.md` format (slug first, date and time at end) per Naming-Conventions.
- **applied**: true only when obsidian_rename_note was called (never true in context `ingest`).
- **protection_triggered**: `null` or string (e.g. `"moc-without-request"`, `"hub"`, `"index"`, `"project-root"`).
- **old_stem**: Current filename without extension.

## Instructions (logic)

1. **Read note**: `obsidian_read_note(path)`. Get current filename (stem = old_stem), frontmatter `title`, `created`, first heading, TL;DR or first paragraph.
2. **Detect role**: Hub, Index/Home/Dashboard, MOC, Project root, Regular. If Hub or Index/Home/Dashboard → return output with `protection_triggered` set, no apply. If MOC or project root and no `explicit_rename_request` (and none parsed from ingest) → proposal only, set `protection_triggered` accordingly.
3. **Vague detection**: Per list above. In `name-review` context, may suggest for any note.
4. **Derive suggested name**: Build `kebab-slug-YYYY-MM-DD-HHMM.md` per [[3-Resources/Second-Brain/Naming-Conventions|Naming-Conventions]] (date and time at end):
   - Date/time: created frontmatter > file creation date/time > ingest/now; time 24h (HHMM), use 0000 when unknown.
   - Slug: first real heading > TL;DR > first sentence; max ~60–70 chars; lowercase kebab; remove leading/trailing stop-words; disambiguate if too generic. Same-minute: distinct time or slug-2, slug-3 or content-based.
5. **Apply per confidence tiers**: For apply (organize or name-review only, and only for Regular or protected-with-request): call **obsidian-snapshot** (per-change) then `obsidian_rename_note(path, new_name)`. After successful rename: **sync frontmatter title** — read the note (or use returned new path if MCP provides it), then call **`obsidian_manage_frontmatter`** to set `title` to the humanized version of the new slug; if current `title` differed significantly, optionally set `old_title` to the previous title for search continuity. In **ingest** context never call obsidian_rename_note.
6. **Log**: To Ingest-Log, Organize-Log, or Name-Review-Log (and Backup-Log if snapshot created). Include suggested_name, applied, confidence, protection_triggered, old_stem.

## Frontmatter sync (required after rename)

After every successful **`obsidian_rename_note`** (when the skill applies the rename in organize or name-review context), sync frontmatter **title** from the new slug. If `title` exists in frontmatter and differs significantly from the new slug, set `title` to the humanized version of the new slug via **`obsidian_manage_frontmatter`**; optionally set `old_title` to the previous title for search continuity. If the note has no `title` key, set it to the humanized slug so future renames have a clear sync target. Use the note path after rename (same path if rename is in-place, or the path returned by the MCP if different).

## MCP tools

- `obsidian_read_note` — read note content and frontmatter.
- `obsidian_rename_note` — rename note in place (same folder). Use only when applying (organize/name-review) and after per-change snapshot.
- `obsidian_manage_frontmatter` — after rename, set `title` (and optionally `old_title`) on the note so frontmatter stays consistent with the new filename.

## Snapshot

Before **obsidian_rename_note** when applying: call **obsidian-snapshot** skill with `type: "per-change"` for the target note. If snapshot fails, do not rename; log #review-needed.

## Tuning confidence heuristics

Over time, compare **proposals** (suggested_name with applied: false or confidence in 70–89% band) vs **actual usage** (user renames, or applied: true). Log to Ingest-Log, Organize-Log, or Name-Review-Log with suggested_name, applied, confidence, old_stem so you can:

- Raise or lower the apply threshold (e.g. 85% → 88% if too many renames are reverted; or 82% if too few vague names get fixed).
- Adjust vague-detection list (add/remove stems) based on what users actually rename.
- Optionally read `confidence_bands` from Second-Brain-Config for name-enhance (high_threshold for apply) when documented there.

## Backbone

- Add to Cursor-Skill-Pipelines-Reference skill table; add to [[3-Resources/Second-Brain/Skills|Skills]]; sync to `.cursor/sync/skills/name-enhance.md`.
- Pipelines: full-autonomous-ingest (name-enhance propose only); autonomous-organize (opportunistic name-enhance); NAME-REVIEW queue (batch name-enhance).
