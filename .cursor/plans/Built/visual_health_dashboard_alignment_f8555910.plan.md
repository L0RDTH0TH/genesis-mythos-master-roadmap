---
name: Visual Health Dashboard alignment
overview: "Align the Visual Health Dashboard draft with your vault's actual conventions: TL;DR in callouts/body (not frontmatter), Highlightr colors in body syntax (not tags), and actionable flags in frontmatter (not tags). The plan specifies exact query changes and where to place the note."
todos: []
isProject: false
---

# Visual Health Dashboard — Vault-aligned plan

Your draft assumes different storage patterns than the vault uses. Below is what actually exists and how to change each section so the dashboard works without changing your pipelines.

---

## Vault conventions (verified)


| Dashboard section    | Draft assumption                                               | Actual in vault                                                                                                                                                                           |
| -------------------- | -------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **TL;DR**            | Frontmatter `tldr::` / `TL;DR::` or inline field               | **Body only**: section `## TL;DR` and callout `> [!summary] TL;DR` (from [callout-tldr-wrap](.cursor/skills/callout-tldr-wrap/SKILL.md)); no frontmatter field                            |
| **Highlightr**       | Tags `#highlightr/red` or inline `highlightr-red::`            | **Body only**: Highlightr syntax `==text==^{Red}` (and ^{Green}, ^{Purple}, etc.) from [distill-highlight-color](.cursor/skills/distill-highlight-color/SKILL.md); no tags or frontmatter |
| **Actionable flags** | Tags `#needs-simplify`, `#resurface-candidate`, `#next-action` | **Frontmatter**: `needs-simplify: true`, `resurface-candidate: true`; tasks in **frontmatter** `next-actions` (string/array), not a tag                                                   |
| **Project grouping** | Folder or `project::`                                          | **Frontmatter** `project-id` (e.g. `Test-Project`) and PARA folders `1-Projects/`, `2-Areas/`, `3-Resources/`                                                                             |


---

## 1. TL;DR coverage

**Change:** TL;DR is not in frontmatter. Detection must use **note content**.

- **Option A (recommended):** Use **DataviewJS** and `dv.io.load(file.path)` to read each note’s content and treat as “has TL;DR” if it contains `> [!summary] TL;DR` (or optionally `## TL;DR` with content below). Count and divide by total core notes for percentage.
- **Option B (future):** Have the **callout-tldr-wrap** skill set a frontmatter field (e.g. `has-tldr: true`) when it runs, then query that in DQL. Existing notes would need a one-time backfill or stay counted via Option A.

**Scope:** Restrict “core notes” to the same scope as pipelines: `1-Projects`, `2-Areas`, `3-Resources` (exclude `4-Archives`, `Backups`, `Templates`, `Ingest`, `**/Log*.md`, `**/* Hub.md`) so the percentage matches “notes that could be distilled.”

**Fix for inline quick stat:** The draft’s inline `dv.pages().where(p => p.tldr || p["TL;DR"])` will always be 0. Replace with a DataviewJS block that does the content-based count and then render the same inline text (or a single JS block that outputs both the paragraph and the percentage).

---

## 2. Highlightr usage by color

**Change:** There are no `#highlightr/red` tags or `highlightr-red::` fields. Colors exist only in the body as `==...==^{Color}`.

- Use **DataviewJS** only: for each color in [Highlightr-Color-Key](3-Resources/Highlightr-Color-Key.md) (Red, Orange, Yellow, Green, Blue, Purple, Cyan, Pink, Grey), load each note’s content with `dv.io.load(p.file.path)` and count matches with a regex like `/\^{Red}/g` (or `/\^{color}/gi`). Aggregate by color across the vault (or per folder/project).
- Remove the draft’s DQL `TABLE` that uses `file.etags` and `#highlightr/red`; it will return no rows.

**Output:** A table or list: Color → number of notes that contain that color at least once (and optionally total occurrence count per color).

---

## 3. Actionable / review candidates

**Change:** Use **frontmatter**, not tags.

- **needs-simplify:** `WHERE needs-simplify = true` (or `p.needs-simplify` in JS).
- **resurface-candidate:** `WHERE resurface-candidate = true` (or `p["resurface-candidate"]`).
- **next-actions:** Notes that have non-empty `next-actions` frontmatter. In DQL you can use `WHERE next-actions` (truthy) or in JS `p["next-actions"]` and check length/content. No `#next-action` tag exists.

**Summary counts:** Replace tag-based `contains(p.file.tags, "#needs-simplify")` with:

- `dv.pages().where(p => p["needs-simplify"] === true).length`
- `dv.pages().where(p => p["resurface-candidate"] === true).length`
- `dv.pages().where(p => p["next-actions"] && (Array.isArray(p["next-actions"]) ? p["next-actions"].length > 0 : String(p["next-actions"]).trim().length > 0)).length` (or simpler if you standardize on one format)

**List query:** Use `WHERE needs-simplify OR resurface-candidate OR next-actions` (and ensure frontmatter field names match) instead of `contains(file.tags, ...)`.

---

## 4. Inconsistent highlight patterns per project / area

**Change:** Keep grouping by top-level PARA folder or by project.

- **By folder:** `FLATTEN split(file.folder, "/")[0] AS projectGroup` is correct for `1-Projects`, `2-Areas`, `3-Resources` (first path segment). Restrict `FROM` to those folders.
- **By project:** Use frontmatter `project-id` (e.g. `FLATTEN project-id AS projectGroup` or in JS group by `p["project-id"]`). Note: `project-id` is the actual field name in your notes (e.g. [2026-02-25-distill-messy.md](1-Projects/Test-Project/2026-02-25-distill-messy.md)).

**Highlight columns:** The draft’s DQL uses `r["highlightr-yellow"]` and tags again; these are empty. To show “notes with Red/Green/etc. per group” you must either:

- Use **DataviewJS** only: group pages by folder or `project-id`, then for each group load content and count `^{Red}`, `^{Green}`, etc., and render a table, or
- Add a **derived frontmatter** field in a future pipeline (e.g. `highlight-colors: ["Red","Green"]`) and query that (optional, not required for v1).

So for “inconsistent highlight patterns,” the first version should be DataviewJS: for each project/folder, count notes that contain each color (content scan), then show table: Folder/Project | Total notes | Red | Green | Purple | …

---

## 5. Where to put the note and scope

- **Path:** Create the dashboard as **[3-Resources/Visual-Health-Dashboard.md](3-Resources/Visual-Health-Dashboard.md)** (consistent with your plan’s “e.g. 3-Resources/Visual-Health.md” and your draft name). Implementation uses **Option B**: a shared script **3-Resources/_dv-visual-health-dashboard.js** loaded via `dv.view()` for sections 1, 2, and 4 (see Implementation addendum).
- **Scope for “core notes”:** Same as pipeline rules: `1-Projects`, `2-Areas`, `3-Resources`; exclude `4-Archives`, `Backups`, `Templates`, `Ingest`, `**/*Log*.md`, `**/* Hub.md` so the dashboard reflects “active” notes.

---

## 6. Thresholds and next steps (from your draft)

- **TL;DR:** You can add a threshold alert (e.g. “Needs work if < 70%”) in the same DataviewJS that computes the percentage; use the 85% / 60% bands from the draft or align with [Cursor-Skill-Pipelines-Reference](3-Resources/Cursor-Skill-Pipelines-Reference.md) (e.g. 85% “good”).
- **Standardization:** Your pipelines already use `==...==^{Color}` and [Highlightr-Color-Key](3-Resources/Highlightr-Color-Key.md); no extra “distill rule to normalize” is required for the dashboard—only the queries need to read body content.
- **Optional:** Add `has-tldr: true` in **callout-tldr-wrap** for future notes so a simple DQL fallback exists and content scan is only for legacy notes; document in the skill and in this dashboard.

---

## Summary of edits to the draft

1. **Section 1 (TL;DR):** Replace frontmatter/inline-field check with DataviewJS content scan for `> [!summary] TL;DR` (and optionally `## TL;DR`). Fix inline quick stat to use the same logic.
2. **Section 2 (Highlightr):** Remove tag- and inline-field-based DQL; use DataviewJS + `dv.io.load` + regex for `^{Red}`, `^{Green}`, etc., and optionally include Cyan, Pink, Grey from the color key.
3. **Section 3 (Actionable):** Switch all queries from `contains(file.tags, "#...")` to frontmatter: `needs-simplify`, `resurface-candidate`, `next-actions`.
4. **Section 4 (Per-project highlights):** Keep folder/project grouping; replace highlight columns with DataviewJS content-based counts per group (or defer to a “per-project highlight stats” JS block).
5. **Scope:** Apply a consistent “core notes” filter (PARA active roots, minus exclusions) in every block.
6. **File:** Save as `3-Resources/Visual-Health-Dashboard.md`.

If you want, the next step can be a single concrete note body (all DataviewJS blocks filled in and DQL fixed) ready to paste into that file.

---

## Implementation addendum (paste-ready code + fixes)

Your recommendations are aligned with the plan: DataviewJS for 1/2/4, reusable core filter, traffic-light thresholds (≥85% / ≥60% / <60%), start with sections 1 and 3, future-proof with `has-tldr: true` in callout-tldr-wrap. Below are the adjustments needed so the paste-ready blocks work in Obsidian.

### Scope / helper in each block

**Issue:** In Dataview, each `dataviewjs` block runs in isolation. A `function isCoreNote(p)` defined in the first block is **not** visible in sections 1, 2, 3 (inline), or 4.

**Chosen approach: Option B** — Use a shared JS file loaded via `dv.view()` for sections 1, 2, and 4. See **"Option B: Shared dv.view() script"** below for full structure. Section 3 remains: DQL LIST plus one small DataviewJS block for the three summary counts (with core filter inlined in that block).

### Section 1 (TL;DR)

- In the TL;DR block, `total` is used but only defined in the “Core Scope” block. **Add inside the TL;DR block:** `const total = corePages.length;` before computing `percentage`.
- Inline quick stat: the draft uses `isCoreNote` in the inline expression; that’s a different scope and won’t see the helper. Prefer dropping the inline and keeping one TL;DR block that outputs both the paragraph and the “X% have TL;DR” line, or use a second small block that redefines `isCoreNote` and does the same count for the “quick stat” line.

### Section 3 (Actionable)

- **DQL LIST:** To restrict to core notes in DQL, use:
`FROM "1-Projects" OR "2-Areas" OR "3-Resources"` and add the same exclusions via `WHERE` (e.g. `AND !contains(file.path, "Backups") AND !contains(file.path, "Log")` etc.) so the list isn’t vault-wide.
- **Summary counts:** The inline expressions use `isCoreNote(p)`, which isn’t defined in that context. Either:
  - Move the three counts into one small DataviewJS block that defines `isCoreNote` and then does `dv.paragraph("needs-simplify: " + ...)` etc., or
  - Inline the filter logic in each expression (no helper).
- **next-actions count:** `dv.func.length` isn’t standard. Use:  
`(Array.isArray(p["next-actions"]) ? p["next-actions"].length : String(p["next-actions"] || "").trim().length) > 0`.

### Section 4 (Per-project)

- In Option B, section 4 is rendered inside the shared script; `corePages` and `isCoreNote` are already in scope. No separate block needed in the dashboard note.

### Which section to refine first

- **Recommended order:** Get **section 1 (TL;DR %)** and **section 3 (actionable list + counts)** working first. They give quick wins; section 3 can be DQL + one JS block for the three counts with core filter inlined. Then add **section 2 (highlight counts)**. Add **section 4 (per-group table)** last (most I/O).

### Per-group thresholds (section 4)

- You can add simple alerts, e.g.:
  - “Flag group if any single color is used in >50% of its notes” (possible over-reliance on one color).
  - Or “Flag if group has 0 highlights” (needs distill).
- Implement by computing the table in JS, then adding a column or a sentence under the table: e.g. `if (data.colors[color] / data.total > 0.5) → "⚠️ Red-heavy"` per row.

---

## Option B: Shared dv.view() script (detailed)

Single shared script that defines the core filter once and renders sections 1, 2, and 4. The dashboard note stays minimal: one view call, then section 3 (DQL + one JS block for counts).

### Script location and API

- **Path:** `3-Resources/_dv-visual-health-dashboard.js` — **use the `.js` extension in the file name**. Vault-root relative; **no leading slash** in the call.
- **Invocation from dashboard:** One `dataviewjs` block: `await dv.view("3-Resources/_dv-visual-health-dashboard", { dv });` — extension is optional in the call (Dataview tries both with and without `.js`), but naming the file with `.js` avoids ambiguity.
- **Do not use dot-prefixed folders** (e.g. `._scripts/`) — Dataview explicitly blocks them.
- **Troubleshooting:** If you get "custom view not found", double-check the path is exact (case-sensitive on some systems) and restart Obsidian after creating the file.
- **Input:** The script receives `input` with at least `dv`. The script uses `dv` for `dv.pages()`, `dv.io.load()`, `dv.paragraph()`, `dv.table()`, `dv.header()`, etc.

### Script structure (pseudocode)

1. **Unpack input:** `const { dv } = input;`
2. **Robustness at top:** If `!dv`, output error paragraph and `return`. Define `function isCoreNote(p) { ... }` (exclude 4-Archives, Backups, Templates, Ingest, `Log*.md`, `*Hub.md`). Then `const corePages = dv.pages().where(isCoreNote);` — optional for debugging: `.limit(50)` then remove later. If `corePages.length > 1500`, output "⚠️ Vault too large for full content scan" and `return`.
3. **Helpers:** `const total = corePages.length;` and (for section 3 if counts in script) `function hasNextActions(p) { const val = p["next-actions"]; if (!val) return false; if (Array.isArray(val)) return val.length > 0; return String(val).trim().length > 0; }`.
4. **Section 1 — TL;DR:** Loop over `corePages`, `await dv.io.load(p.file.path)`. Use a **forgiving regex**: match `> \[!summary\][\s-]*TL;DR` (i), or `##\s*TL;DR` (i), or `>\s*TL;DR` (i). Count `withTldr`. Percentage + traffic lights (≥85% Good, ≥60% Fair, <60% Needs work).
5. **Section 2 — Highlightr:** Colors array as above. For each color, match with **case-insensitive** regex: `new RegExp('\\^\\{' + color.trim() + '\\}', 'i')`. Count notes, sort descending, output per color with count > 0.
6. **Section 4 — Per-project table:** Group by `p.file.folder.split("/")[0]`, load content per page, count per color (same regex). **Per-group alert (simple):** find dominant color and maxColorPct; if maxColorPct > 0.5 → alert = "⚠️ {dominantColor}-heavy ({pct}%)"; else if all color counts 0 → "No highlights". Add "Alert" column to table.
7. **Optional:** After the table, add **Actionable summary** (section 3 counts): `dv.header(2, "Actionable Summary");` then needs-simplify, resurface-candidate, next-actions (using `hasNextActions(p)`) counts and one `dv.paragraph`. Then the dashboard note's section 3 is **only** the DQL LIST (no separate counts block).

All I/O stays inside the script; single `await dv.view(...)` from the dashboard.

### Dashboard note layout (3-Resources/Visual-Health-Dashboard.md)

- **Header + description:** Title, last refreshed `dv.current().file.mtime`, short blockquote.
- **Block 1 (DataviewJS):** `await dv.view("3-Resources/_dv-visual-health-dashboard", { dv });`  
Renders: core scope line, section 1 (TL;DR % + status), section 2 (highlight counts), section 4 (per-group table + Alert column). **Optional:** include Actionable summary counts in the script so the dashboard only needs the view + DQL list.
- **Section 3 — Actionable:** A **DQL** block for the list: `FROM "1-Projects" OR "2-Areas" OR "3-Resources"` with `WHERE (needs-simplify = true OR resurface-candidate = true OR next-actions)` and path exclusions, `LIST file.link`, `SORT file.mtime DESC`, `LIMIT 20`. If the shared script does **not** output the three summary counts, add one DataviewJS block that defines `isCoreNote` (or inlines the filter) and `hasNextActions(p)`, then outputs needs-simplify / resurface-candidate / next-actions counts.

### Files to create

- **Create:** `3-Resources/_dv-visual-health-dashboard.js` (the view script).
- **Create/update:** `3-Resources/Visual-Health-Dashboard.md` (markdown + one view block + section 3 DQL + section 3 counts block).

### Optional: project-id grouping in section 4

- To group by `project-id` instead of top-level folder, in the script use `const group = p["project-id"] || p.file.folder.split("/")[0] || "No project";` when building the groups object. Rest of table logic unchanged.

---

## Last-minute tweaks & implementation notes

Paste-ready details for the shared script and section 3.

### At top of shared script (right after `const { dv } = input;`)

```js
if (!dv) {
  dv.paragraph("Error: dv object not passed to view script.");
  return;
}

function isCoreNote(p) {
  const path = p.file.path;
  if (path.startsWith("4-Archives/") || path.startsWith("Backups/") || path.startsWith("Templates/") || path.startsWith("Ingest/")) return false;
  if (path.match(/Log.*\.md$/) || path.match(/Hub\.md$/)) return false;
  return path.startsWith("1-Projects/") || path.startsWith("2-Areas/") || path.startsWith("3-Resources/");
}

const corePages = dv.pages().where(isCoreNote);  // .limit(50) for initial testing — remove later
if (corePages.length > 1500) {
  dv.paragraph("⚠️ Vault too large for full content scan — consider backfilling frontmatter fields.");
  return;
}
const total = corePages.length;
```

### TL;DR detection (forgiving)

```js
if (content.match(/>\s*\[!summary\]\s*[\s-]*TL;DR/i) || content.match(/##\s*TL;DR/i) || content.match(/>\s*TL;DR/i)) {
  withTldr++;
}
```

Catches `> [!summary]- TL;DR`, `> TL;DR`, and minor spacing/case variations.

### Highlight color regex (case & spacing)

```js
if (content.match(new RegExp(`\\^\\{${color.trim()}\\}`, 'i'))) {
  counts[color]++;
}
```

Use `color.trim()` if the pipeline ever adds spaces to color names.

### next-actions count helper (section 3)

Use in the shared script (if outputting actionable summary) or in the dashboard’s small JS block:

```js
const hasNextActions = p => {
  const val = p["next-actions"];
  if (!val) return false;
  if (Array.isArray(val)) return val.length > 0;
  return String(val).trim().length > 0;
};
// e.g. dv.pages().where(p => isCoreNote(p) && hasNextActions(p)).length
```

### Per-group Alert column (simple)

Add after building color counts for a group; then append `alert` to the row:

```js
let alert = "";
let maxColorPct = 0;
let dominantColor = "";
for (let c of colors) {
  const pct = data.total > 0 ? (data.colors[c] / data.total) : 0;
  if (pct > maxColorPct) {
    maxColorPct = pct;
    dominantColor = c;
  }
}
if (maxColorPct > 0.5) {
  alert = `⚠️ ${dominantColor}-heavy (${Math.round(maxColorPct*100)}%)`;
} else if (Object.values(data.colors).every(v => v === 0)) {
  alert = "No highlights";
}
```

### Optional: actionable summary in shared script

After the per-project table, add:

```js
dv.header(2, "Actionable Summary");
const ns = corePages.where(p => p["needs-simplify"] === true).length;
const rc = corePages.where(p => p["resurface-candidate"] === true).length;
const na = corePages.where(p => hasNextActions(p)).length;
dv.paragraph(`**needs-simplify:** ${ns}  |  **resurface-candidate:** ${rc}  |  **next-actions (non-empty):** ${na}`);
```

Then section 3 in the dashboard note is only the DQL LIST (with FROM + exclusions).