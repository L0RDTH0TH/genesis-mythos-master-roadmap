---
name: Roadmap Standard Dataview Enhancements
overview: Enhance Roadmap-Standard-Format and the Example Roadmap with Dataview-focused structure (per-phase queries, phase descriptions, sub-roadmap pattern, pipeline sync guidance), optional frontmatter for future-proofing, and conservative nice-to-haves—without adding new pipeline steps or inventing dependency patterns.
todos: []
isProject: false
---

# Roadmap Standard Format: Dataview Focus and Strategic Tweaks

## Scope and constraints

- **No new pipeline steps**: Only documentation and example changes; existing skills (roadmap-ingest, add-roadmap-append, expand-road-assist) already respect sections—document how they stay in sync.
- **Safety**: Preserve backup/snapshot/dry_run invariants per [Backbone.md](3-Resources/Second-Brain/Backbone.md) and [mcp-obsidian-integration](.cursor/rules/always/mcp-obsidian-integration.mdc). Document re-queue + dry_run for phase add/remove.
- **Extensibility**: New frontmatter fields are optional; pipelines ignore when absent. No auto-splitting unless `#needs-process` (unchanged).
- **Dataview syntax**: Example queries will use patterns that work in Obsidian Dataview; any `GROUP BY` or link-based queries will be validated or documented as "adjust per your Dataview/Tasks plugin version" where the exact API differs (e.g. `file.section` vs `meta(section)`).

---

## 1. Update [3-Resources/Roadmap-Standard-Format.md](3-Resources/Roadmap-Standard-Format.md)

### 1.1 Structure section

- **Phase descriptions (prose slot)**  
After "Subphases" and before "Tasks", add:
  - Recommend a short prose paragraph after each `## Phase N` (e.g. goals, risks, scope).
  - State that autonomous-distill can refine this prose when `#needs-process` is set.
  - Optional frontmatter: `phase_desc_conf: N` (0–100)—if present and below 72%, EAT-QUEUE refinement is propose-only (tie to [Parameters.md](3-Resources/Second-Brain/Parameters.md) low band). Omit if not using.
- **Per-phase Dataview block**  
Add new subsection "Per-phase Dataview (optional)":
  - After the phase description, an optional Dataview block can list subtasks, progress, or linked sub-roadmaps so the roadmap acts as a living dashboard.
  - Include **two concrete example snippets** that work in standard Obsidian Dataview/Tasks:
    - **In-file tasks for this note**: Keep existing `TASK WHERE file.path = this.file.path`; add a variant that filters incomplete only, e.g. `TASK WHERE file.path = this.file.path AND !completed`.
    - **Sub-roadmap links (MOC pattern)**: Use a query that lists notes in the same Roadmap folder that are linked from the current note (e.g. `LIST FROM [[this.file.link]]` or backlink-style; avoid `contains(links, this.file.name)` if that is not valid—use `outlinks` or `file.link` pattern per Dataview docs).
  - If per-section grouping is desired, add a note: "For grouping by heading/section, use Dataview's `meta(section)` or your Tasks plugin's section field if available; syntax may vary by plugin version."
  - **Future-proofing**: Optional frontmatter `dataview_focus: ["tasks" | "subphases" | "progress"]`—pipelines may use this to choose which query variant to insert when `#needs-process` is set; optional `min_conf: 85` to filter tasks by confidence if task frontmatter carries confidence (document as optional; pipelines ignore if absent).
  - **Progress (nice-to-have)**: One optional snippet for completion percentage (e.g. TABLE with completed/total) with a note: "Requires Tasks plugin; adjust to your Tasks/Dataview API."

### 1.2 Sub-roadmap pattern

- Add subsection **"Sub-roadmap notes (optional)"**:
  - Each phase may link to a separate note (e.g. `[[Phase-1-Sub-Roadmap]]`) that holds that phase’s description, tasks, and its own Dataview. Clicking the link opens the sub-roadmap; [roadmap-checklist](.cursor/skills/roadmap-checklist/SKILL.md) already follows `[[links]]` recursively.
  - Optional frontmatter: `sub_roadmaps: ["Phase-1-Sub-Roadmap.md", ...]` for Dataview aggregation across roadmaps; pipelines (e.g. add-roadmap-append) may append links when confidence ≥85%. Document as optional.

### 1.3 Pipeline behavior when adding/removing phases

- Add section **"When phases are added or removed"**:
  - Re-queue via **TASK-ROADMAP** (or add/expand via ADD-ROADMAP-ITEM / EXPAND-ROAD); run EAT-QUEUE so roadmap-ingest (or relevant skill) re-parses and updates the roadmap.
  - For reorders: REORDER-ROADMAP uses **dry_run first** per [mcp-obsidian-integration](.cursor/rules/always/mcp-obsidian-integration.mdc); no new behavior, just document it here.
  - Optional frontmatter `phase_index: true`: document that queue modes (e.g. REORDER-ROADMAP) can use this as a hint to refresh a phase index or Dataview-friendly structure when present; pipelines implement when needed (no mandate).

### 1.4 Frontmatter

- Extend the Frontmatter table/list to include optional fields (all optional, pipelines ignore if absent):
  - `dataview_focus`, `min_conf`, `phase_desc_conf`, `sub_roadmaps`, `phase_index`
  - Nice-to-have (short line each): `resurface_after: YYYY-MM-DD`, `archive_prep: true` (autonomous-archive); `highlight_perspective: [lens]` (distill-highlight-color); dependency gating `(depends on: ^id, min_conf: 85%)` in task line—document as optional and tie to [Parameters.md](3-Resources/Second-Brain/Parameters.md).

### 1.5 Observability (just-in-case)

- **Progress log**: Add optional "Progress Log" pattern—a `### Progress Log` section with a Dataview that aggregates from pipeline logs (e.g. `TABLE ... FROM "3-Resources/*-Log.md" WHERE ...`) referencing [Logs.md](3-Resources/Second-Brain/Logs.md); note that exact field names depend on log format.
- **Feedback callout**: Recommend an optional `> [!feedback]` at the end of the roadmap: "Add notes here; re-queue via EAT-QUEUE for refinement." Align with [Templates.md](3-Resources/Second-Brain/Templates.md) result callouts (proposal, preview, success); add `[!feedback]` to Templates as an optional roadmap callout type if not already present.

### 1.6 Quick-start

- Update the numbered list to mention: (1) phase description prose after each phase heading, (2) optional Dataview block per phase, (3) optional link to sub-roadmap note. Keep existing steps 1–4 and add one line pointing to the Example.

---

## 2. Update [1-Projects/Example/Roadmap/Example-Roadmap.md](1-Projects/Example/Roadmap/Example-Roadmap.md)

- **Phase 1**:
  - Add 2–3 sentences of phase description (goals/scope) after `## Phase 1`.
  - Insert one Dataview block after the description (e.g. in-file tasks, incomplete only): use the validated snippet from the standard.
  - Add a link to a sub-roadmap note for Phase 1 (e.g. `[[Example-Phase-1-Sub-Roadmap]]`).
- **Phase 2 and 3**: Optionally add one-line phase descriptions only (no Dataview block in the example to avoid clutter; the standard already documents the pattern).
- **End of file**: Add optional `> [!feedback]` callout: "Add notes here; re-queue via EAT-QUEUE for refinement."
- **Frontmatter**: Add at least one optional field to demonstrate (e.g. `dataview_focus: ["tasks"]` or `sub_roadmaps: ["Example-Phase-1-Sub-Roadmap.md"]`).

---

## 3. Create sub-roadmap example note

- **Path**: `1-Projects/Example/Roadmap/Example-Phase-1-Sub-Roadmap.md`
- **Content**: Short note with `roadmap: true`, `project-id: Example`, title "Example Phase 1 — Sub-roadmap", a brief description of Phase 1 scope, and a small task list or table (can mirror the Phase 1 tasks from the main Example-Roadmap). Optionally one Dataview block (e.g. `TASK WHERE file.path = this.file.path`). Link back to `[[Example-Roadmap]]`.

---

## 4. Documentation cross-links

- **Pipelines.md**: In the task/roadmap row or a short "Roadmap structure" sentence, add a pointer to Roadmap-Standard-Format for "phase description, per-phase Dataview, sub-roadmap pattern, and phase add/remove behavior." No pipeline logic change.
- **Templates.md**: If `[!feedback]` is new, add it under "Result callouts" or "Example callouts" as optional for roadmaps.
- **Parameters.md**: No change; only referenced for confidence bands and optional `phase_desc_conf`/`min_conf` semantics in the standard.

---

## 5. Dataview query validation note

- In Roadmap-Standard-Format, add a short note near the example queries: "If a query fails in your vault, check Obsidian Dataview and Tasks plugin docs for field names (e.g. `meta(section)`, `completed`, `file.outlinks`)." This keeps the plan conservative and avoids hard-coding unstable APIs.

---

## 6. Backbone and sync

- **backbone-docs-sync**: [Roadmap-Standard-Format](3-Resources/Roadmap-Standard-Format.md) lives under `3-Resources/`; it is referenced by Pipelines and skills. Update [3-Resources/Second-Brain/Pipelines.md](3-Resources/Second-Brain/Pipelines.md) as above. If a single source of truth for "roadmap structure" lives in Second-Brain (e.g. Vault-Layout or a doc that duplicates structure), add a line there pointing to Roadmap-Standard-Format for phase/Dataview/sub-roadmap. No change to `.cursor/sync/` unless a rule file is edited (this plan does not edit rules).

---

## Implementation order

1. **Roadmap-Standard-Format.md** — Structure (§1.1), Sub-roadmap (§1.2), Pipeline behavior (§1.3), Frontmatter (§1.4), Observability (§1.5), Quick-start (§1.6), Dataview note (§5).
2. **Example-Roadmap.md** — Phase 1 description, one Dataview block, sub-roadmap link, optional Phase 2/3 one-liners, [!feedback] callout, frontmatter.
3. **Example-Phase-1-Sub-Roadmap.md** — New file (create).
4. **Pipelines.md** — One pointer to Roadmap-Standard-Format for roadmap structure.
5. **Templates.md** — Add [!feedback] for roadmaps if not present.

---

## Out of scope (by design)

- No new MCP tools or skill steps.
- No change to dependency syntax beyond documenting optional `min_conf` in task line.
- No mandatory phase index or auto-refresh; `phase_index` is optional and for future use.
- Progress bar / completion % query is optional and documented as Tasks-plugin-dependent.

