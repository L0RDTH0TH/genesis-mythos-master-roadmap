---
name: Research and Scoping Flows to PMG
overview: Define the two flows (Research Ingest and Scoping toward Project Master Goal), align them with existing pipelines and skills, and specify what to add (research-scope skill, SCOPING MODE queue alias, PMG convention and link-back) so research is ingested as Resources and scoping distills and expresses the road to the PMG for roadmap generation.
todos: []
isProject: false
---

# Research and Scoping Flows Toward Project Master Goal

## High-impact, low-effort tweaks (do these first)

### 1. Make Project Master Goal the explicit default seed for roadmap-generate-from-outline

- **Current state:** The skill looks for any note with `## Phases` or phase-like headings; seed can be in Ingest/ or under the project folder.
- **Tweak:** Add one sentence in the skill description / "When to use" in [.cursor/skills/roadmap-generate-from-outline/SKILL.md](.cursor/skills/roadmap-generate-from-outline/SKILL.md):
  > Preferred seed note = note whose filename contains `Master-Goal` or `MasterGoal` and resides directly under the project root folder (`1-Projects/<project-id>/…`). If multiple candidates, prefer the one with highest `created` timestamp or explicit `roadmap-seed: true` frontmatter.
- **Why:** Removes ambiguity, enforces single source of truth, prevents seeding from a random research note.
- **Where:** Document in [3-Resources/Second-Brain/Skills](3-Resources/Second-Brain/Skills.md) (roadmap-generate-from-outline entry) + add convention bullet in [3-Resources/Second-Brain/README](3-Resources/Second-Brain/README.md) (Trigger cheat sheet) or [Vault-Layout](3-Resources/Second-Brain/Vault-Layout.md).

### 2. Auto-link ingested research notes back to the PMG when project-id matches

- **Current:** `append_to_hub` only appends to generic hubs (Resources Hub, etc.).
- **Tweak:** Extend `append_to_hub` (or add a tiny post-step skill **link-to-pmg-if-applicable**) to:
  - If note has `project-id` frontmatter
  - If a note matching `1-Projects/<project-id>/*Master*Goal*.md` (or `Project-Master-Goal.md`) exists in that project folder
  - Then append `[[<PMG-basename>]]` to the note’s `links:` array (or add a `## Related to Goal` callout with the link)
- **Why:** Bidirectional traceability with minimal effort; research becomes “supporting evidence” for the goal.
- **Safety:** Only append to the **research note**; never insert into the PMG itself unless confidence ≥90% and `user_guidance` explicitly allows it.

### 3. Standardize PMG filename pattern in naming conventions

- **Add to** [3-Resources/Second-Brain/Naming-Conventions](3-Resources/Second-Brain/Naming-Conventions.md):
  - **Project Master Goal notes**
  - Preferred: `<project-slug>-Master-Goal.md` or `Project-Master-Goal.md`
  - Allowed variations: `*Master-Goal*.md`, `*MasterGoal*.md`
  - Discouraged: `Goal.md`, `Roadmap.md` (too generic; name-enhance should propose better)
- **Why:** Makes auto-detection reliable for the seed preference above and for future skills that need to find “the goal note.”

---

## Context and assumptions

- **Research** is done outside the vault (browser, Readwise, etc.) and **ingested** as notes into the vault; pipelines then place them as **Resources** (evergreen refs).
- **Scoping** = distill + express the "road" to the **Project Master Goal (PMG)** so the PMG note becomes the seed for **ROADMAP MODE – generate from outline** (project + Roadmap/ tree).
- PMG is a note such as `1-Projects/<project-id>/Project-Master-Goal.md` (or `*Master*Goal*.md`) with: TL;DR, constraints, one-sentence goal, and optional `## Phases` (headings/bullets) used by [roadmap-generate-from-outline](.cursor/skills/roadmap-generate-from-outline/SKILL.md) to create phase notes.

---

## Flow 1: Research Ingest (external → Resources)

**Purpose:** Raw research lands in `Ingest/`; the system classifies, distills, and proposes a PARA path (typically Resource); after approval and EAT-QUEUE, notes move to `3-Resources/...` (e.g. by theme/project).

**Trigger:** New notes in `Ingest/` + user runs **INGEST MODE** (or "Process Ingest").

**Pipeline:** [full-autonomous-ingest](3-Resources/Cursor-Skill-Pipelines-Reference.md) (unchanged).

**Skills in order (canonical from Cursor-Skill-Pipelines-Reference):**


| Order | Skill / step                                     | Why                                                                                                                       |
| ----- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| 0     | (optional) Non-md + embedded image normalization | Per ingest-processing; companion .md and move to 5-Attachments when applicable.                                           |
| 1     | **create_backup**                                | Safety invariant; gates all destructive steps.                                                                            |
| 2     | **classify_para**                                | Sets `para-type` (Resource for ref material) and can set `project-id` when tied to a project (e.g. minecraft-beta-clone). |
| 3     | **frontmatter-enrich**                           | Sets status, confidence, created, tags, links; optional project-id, priority.                                             |
| 4     | **name-enhance** (propose only)                  | Suggests slug; subfolder-organize uses it in path at ≥85%; no rename in Phase 1.                                          |
| 5     | **subfolder-organize**                           | Builds path (≤4 levels) from para-type + project-id + themes, e.g. `3-Resources/Game-Dev/Voxel-Engines/<note>.md`.        |
| 6     | (confidence/loop)                                | Mid-band: self-critique; high: proceed; low: Decision Wrapper only.                                                       |
| 7     | **split_atomic**                                 | Breaks long dumps into atomic notes (when ≥85%).                                                                          |
| 8     | **split-link-preserve**                          | split_from / split_into; traceability.                                                                                    |
| 9     | **distill_note**                                 | Progressive layers (bold/highlight); supports scoping/reference lens.                                                     |
| 10    | **distill-highlight-color**                      | Project highlight_key + semantic colors.                                                                                  |
| 11    | **next-action-extract**                          | Tasks → checklists + next-actions frontmatter.                                                                            |
| 12    | **task-reroute**                                 | When task-like and ≥78%; find parent, create/append task note; snapshot target.                                           |
| 13    | **append_to_hub**                                | Links to Resources Hub (and optionally project MOC); can be extended to link back to PMG when project-id matches.         |
| 14    | **Decision Wrapper**                             | obsidian_propose_para_paths (wrapper mode) → A–G; no move in Phase 1.                                                     |
| 15    | **log_action**                                   | Ingest-Log with backup path, confidence, proposed path.                                                                   |


**Phase 2 (apply):** User approves wrapper (e.g. Option B = `3-Resources/Game-Dev/...`) and sets `approved: true`; **EAT-QUEUE** runs Step 0 → apply-mode ingest → **move_note** (dry_run then commit) to approved path.

**Optional enhancement (no new pipeline):** Extend **append_to_hub** (or frontmatter-enrich) so that when `project-id` is set, the note gets a `links` entry to the project’s PMG if it exists (e.g. `[[1-Projects/<project-id>/Project-Master-Goal]]`). Implementation: one MCP call or in-skill logic to resolve PMG path from project-id and add to links.

```mermaid
flowchart LR
  External[External research] --> Ingest[Drop in Ingest]
  Ingest --> IngestMode[INGEST MODE]
  IngestMode --> Backup[create_backup]
  Backup --> Classify[classify_para]
  Classify --> Enrich[frontmatter_enrich]
  Enrich --> Name[name_enhance propose]
  Name --> Subfolder[subfolder_organize]
  Subfolder --> Split[split_atomic + split_link_preserve]
  Split --> Distill[distill_note + distill_highlight_color]
  Distill --> Next[next_action_extract + task_reroute]
  Next --> Hub[append_to_hub]
  Hub --> Wrapper[Decision Wrapper]
  Wrapper --> Approve[User approve + EAT-QUEUE]
  Approve --> Move[move_note to 3-Resources]
```



---

## Flow 2: Scoping (distill + express the road to PMG)

**Purpose:** Turn the PMG note (and already-ingested Resources) into a clear, expressed "road" (phases, related refs, outline) so it can seed **ROADMAP MODE – generate from outline**.

**Trigger:** User runs **DISTILL MODE** then **EXPRESS MODE** on the PMG note (e.g. "distill then express the Project Master Goal for OG-Minecraft-Clone"). Optional: a single **SCOPING MODE** trigger that chains both (see below).

**Pipelines:** **autonomous-distill** (on PMG) → **autonomous-express** (on PMG). Chaining order: distill first (refine goal + optional ## Phases, highlights, TL;DR) so express has a clean signal for related content and outline.

### Distill chain (on PMG)


| Order | Skill / step                               | Why                                                                          |
| ----- | ------------------------------------------ | ---------------------------------------------------------------------------- |
| 1     | **create_backup**                          | Safety.                                                                      |
| 2     | **auto-layer-select** (optional)           | Depth (1/2/3 layers) from content; use `distill_lens: scoping` when scoping. |
| 3     | **distill layers**                         | Bold/highlight core goal, constraints, phase bullets.                        |
| 4     | **distill-highlight-color**                | Semantic colors; project highlight_key.                                      |
| 5     | **highlight-perspective-layer** (optional) | Set `highlight_perspective: scoping`; drift/angles for depth.                |
| 6     | **layer-promote**                          | Promote to TL;DR.                                                            |
| 7     | **distill-perspective-refine**             | Depth/drift in TL;DR; use distill_lens when set.                             |
| 8     | **callout-tldr-wrap**                      | Wrap in `> [!summary] TL;DR`.                                                |
| 9     | **readability-flag**                       | needs-simplify when low.                                                     |
| 10    | **log_action**                             | Distill-Log.                                                                 |


### Express chain (on PMG)


| Order | Skill / step                                   | Why                                                                                                                                                                                                                   |
| ----- | ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1     | **create_backup**                              | Safety.                                                                                                                                                                                                               |
| 2     | **version-snapshot**                           | Dated snapshot in Versions/ before appends.                                                                                                                                                                           |
| 3     | **related-content-pull**                       | Pull similar notes via semantic + **project-id** (already includes ingested Resources); append ## Related.                                                                                                            |
| 4     | **research-scope** (new)                       | From PMG: project-id + phase/keywords → search vault for Resources (3-Resources, same project-id or tags) → append **## Scoped Resources** (or augment Related) with links/summaries. Vault-only; no external search. |
| 5     | **express-mini-outline**                       | Mini-outline / "road to goal" (phases, milestones, refs); express_view can be "scoping" to shape sections.                                                                                                            |
| 6     | **express-view-layer** (when express_view set) | Connection strength in Related.                                                                                                                                                                                       |
| 7     | **call-to-action-append**                      | CTA (e.g. "Add phases?", "Run ROADMAP MODE").                                                                                                                                                                         |
| 8     | **log_action**                                 | Express-Log.                                                                                                                                                                                                          |


**Output:** PMG note with: refined goal, optional ## Phases, TL;DR, Related, Scoped Resources, mini-outline. User (or queue) then runs **ROADMAP MODE – generate from outline** with the PMG path; [roadmap-generate-from-outline](.cursor/skills/roadmap-generate-from-outline/SKILL.md) parses phase headings and creates project + Roadmap/ tree.

```mermaid
flowchart LR
  PMG[Project Master Goal] --> Distill[autonomous_distill]
  Distill --> Layers[distill layers + highlight + layer_promote]
  Layers --> Express[autonomous_express]
  Express --> Version[version_snapshot]
  Version --> Related[related_content_pull]
  Related --> ResearchScope[research_scope new]
  ResearchScope --> Outline[express_mini_outline]
  Outline --> CTA[call_to_action_append]
  CTA --> RoadmapMode[ROADMAP MODE generate from outline]
  RoadmapMode --> Tree[Project + Roadmap tree]
```



---

## New skill: research-scope (medium-impact; refined behavior)

**Role:** During express on a PMG (or any note with `is_master_goal: true` / path match), aggregate **already-ingested** Resources relevant to the project and surface them for the PMG (vault-only).

**Slot:** After **related-content-pull**, before **express-mini-outline** in autonomous-express.

**Behavior (refined):**

1. **Detect PMG:** Note path or frontmatter (`is_master_goal: true` or filename pattern `*Master*Goal*.md`).
2. **Read PMG:** project-id, ## Phases or key phrases.
3. **Search vault:** `obsidian_global_search` / `obsidian_list_notes` under `3-Resources/` filtered by project-id and tags/keywords from phases.
4. **Propose-first by default:** Do **not** auto-append `## Scoped Resources` to the PMG on first pass. Instead insert a **proposal callout** in the PMG:

```markdown
   > [!proposal] Scoped Research Suggestions
   > Confidence: 82%
   > Suggested additions:
   > - [[3-Resources/Game-Dev/Perlin-Noise-Implementation.md]] — core terrain gen reference ^[source: project-id + phase "Terrain"]
   > - [[3-Resources/Game-Dev/Minecraft-Beta-1.7-Feature-List.md]] — feature parity target ^[source: tag #minecraft-beta]
   > Add to PMG? (Set approved: true and re-run EXPRESS or EAT-QUEUE to commit.)
   

```

   Only **commit** insert (append actual `## Scoped Resources` section to PMG) on **second pass** after `approved: true` or explicit EAT-QUEUE guidance.
5. **Lightweight source citation:** When listing a resource, append inline `^[source: <reason>]` or footnote-style link (e.g. project-id, tag, or phase name) so the user can trace why it was suggested.
6. **Confidence gates:**

- **≥85%:** Propose insert (callout) **and** auto-append suggested PMG wikilinks to the **research notes’** `links:` array only (not into PMG body unless user approved); optionally add link to PMG in each resource note’s `links` for bidirectionality.
- **68–84%:** Callout proposal only; no auto-append to PMG or to resource notes.
- **<68%:** Do not write to PMG; log to Feedback-Log (or Express-Log) as “low-confidence scoping candidate” with note path and confidence.

**Safety:** Snapshot before any append to PMG when committing on second pass. Never insert into PMG unless user has approved (or confidence ≥90% with explicit user_guidance).

**MCP:** `obsidian_read_note`, `obsidian_global_search`, `obsidian_update_note`, `obsidian_manage_frontmatter` (for appending to resource notes’ links). No new MCP tool required.

**Files to add:**

- [.cursor/skills/research-scope/SKILL.md](.cursor/skills/research-scope/SKILL.md) — full instructions, when to use, propose-then-commit flow, source citation format, confidence gates, logging (Express-Log, Feedback-Log).

---

## SCOPING MODE – queue alias (medium-impact; no new pipeline)

**Decision:** Keep SCOPING MODE as a **queue alias**, not a new pipeline. Reuse existing chains and logging/snapshot behavior.

- **Behavior:** Add to prompt-queue mode handling (e.g. in [auto-eat-queue](.cursor/rules/context/auto-eat-queue.mdc) or dispatch table):
  - `**SCOPING MODE`** (or `**SCOPING`**) → internally dispatch **DISTILL MODE** then **EXPRESS MODE** on the **same note** (PMG).
  - Optional second argument: `**SCOPING MODE <path-to-pmg>`** so the queue can target a specific PMG path.
- **Implementation:** When mode is `SCOPING` or `SCOPING MODE`, resolve `source_file` (or current note) as PMG path; emit or process two logical entries: first DISTILL MODE for that path, then EXPRESS MODE for that path (research-scope runs inside express). No new pipeline code; same snapshot and log behavior as running the two modes in sequence.
- **Where:** Document in [3-Resources/Second-Brain/Queue-Sources](3-Resources/Second-Brain/Queue-Sources.md) and add to the trigger table in [Pipelines](3-Resources/Second-Brain/Pipelines.md) and [Cursor-Skill-Pipelines-Reference](3-Resources/Cursor-Skill-Pipelines-Reference.md).

---

*(Auto-link research → PMG is covered in High-impact tweak #2 above.)*

---

## Where to document and extend


| What                             | Where                                                                                                                                                                                                                                                                                                            |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Flow 1 (Research Ingest)         | [Cursor-Skill-Pipelines-Reference](3-Resources/Cursor-Skill-Pipelines-Reference.md) already describes full-autonomous-ingest; add a short "Research ingest" subsection that states research notes use the same pipeline and typically get para-type Resource and project-id; optional PMG link in append_to_hub. |
| Flow 2 (Scoping)                 | New subsection "Scoping toward PMG" in Cursor-Skill-Pipelines-Reference and in [Pipelines](3-Resources/Second-Brain/Pipelines.md): trigger = DISTILL then EXPRESS on PMG; list express skills including research-scope after related-content-pull.                                                               |
| research-scope skill             | New [.cursor/skills/research-scope/SKILL.md](.cursor/skills/research-scope/SKILL.md); register in [Skills](3-Resources/Second-Brain/Skills.md) and in pipeline table (autonomous-express).                                                                                                                       |
| SCOPING MODE (queue alias)       | [Queue-Sources](3-Resources/Second-Brain/Queue-Sources.md) + dispatch in auto-eat-queue: SCOPING MODE → DISTILL then EXPRESS on same note; Trigger table in Pipelines.md and Cursor-Skill-Pipelines-Reference.                                                                                                   |
| PMG convention / seed preference | [Naming-Conventions](3-Resources/Second-Brain/Naming-Conventions.md) (PMG filename pattern); [Skills](3-Resources/Second-Brain/Skills.md) + roadmap-generate-from-outline SKILL.md (preferred seed sentence); [README](3-Resources/Second-Brain/README.md) or Vault-Layout (trigger cheat sheet bullet).         |
| Responsibilities                 | [Responsibilities-Breakdown](3-Resources/Second-Brain/Responsibilities-Breakdown.md): add row for research-scope; add sentence under autonomous-express that scoping = distill then express on PMG with research-scope.                                                                                          |


---

## Summary: skills in order and pipelines

**Flow 1 – Research Ingest:**  
Pipeline: **full-autonomous-ingest**.  
Skills order: backup → classify_para → frontmatter-enrich → name-enhance (propose) → subfolder-organize → [loop] → split_atomic → split-link-preserve → distill_note → distill-highlight-color → next-action-extract → task-reroute → append_to_hub → Decision Wrapper → log_action. Apply move via EAT-QUEUE after wrapper approval.

**Flow 2 – Scoping:**  
Pipelines: **autonomous-distill** (on PMG) then **autonomous-express** (on PMG).  
Distill: backup → auto-layer-select → distill layers → distill-highlight-color → highlight-perspective-layer → layer-promote → distill-perspective-refine → callout-tldr-wrap → readability-flag → log.  
Express: backup → version-snapshot → related-content-pull → **research-scope** (new) → express-mini-outline → express-view-layer (if set) → call-to-action-append → log.  
Then user runs **ROADMAP MODE – generate from outline** (path = PMG) to create the roadmap tree.

**New:** research-scope skill (propose-first callout, source citation, confidence gates; commit on second pass). **SCOPING MODE** = queue alias that dispatches DISTILL then EXPRESS on PMG. **PMG as default seed** for roadmap-generate-from-outline; **PMG filename** in Naming-Conventions; **auto-link** ingested research notes to PMG when project-id matches (append to research note’s links only; never insert into PMG unless approved).