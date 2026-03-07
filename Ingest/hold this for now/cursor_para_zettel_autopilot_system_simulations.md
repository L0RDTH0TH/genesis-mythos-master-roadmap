---
proposal_path: Ingest/Decisions/Decision-for-cursor-para-zettel-autopilot-simulations--2026-03-04-0440.md
---
## TL;DR
# PARA-Zettel Autopilot system simulation

---

# PARA-Zettel Autopilot system simulation
_Exported on 3/2/2026 at 05:56:26 EST from Cursor (2.5.26)_

---

**User**

You are simulating the Second Brain PARA-Zettel Autopilot system in an almost-empty vault.

Assume:
- Ingest/ contains: Genesis-Docs-Timeline.md + ~10 flattened genesis-mythos docs (README.md, docs--SYSTEM_IMPLEMENTATIONS.md, docs--WORLD_BUILDER_WIZARD_GUIDE.md, docs--TERRAIN3D_INTEGRATION_GUIDE.md, etc.)
- Genesis-Docs-Timeline.md already
- All Ingest files have only minimal ingest/github-doc tags

First, describe what the system would do right now if the user said "INGEST MODE" without any extra priming or queue entries.
Then simulate a full cleanup / reset state:
- What backups/snapshots would be created?
- Which files would stay in Ingest/ vs get rejected/excluded?
- What confidence bands would most notes land in on first pass?
- What proposal callouts or manual approval steps would appear?

Be brutally honest about how messy / low-confidence the first raw ingest would be in an empty vault.

---

**Cursor**

## 1. What would happen right now if you said “INGEST MODE”?

Assuming your rules/skills are wired as described, with an almost-empty vault and ~10 `Genesis` markdown docs in `Ingest/`:

### High-level flow

- **1) Discover Ingest notes**
  - List `Ingest/*.md` → finds `Genesis-Docs-Timeline.md` + ~10 `docs--*.md` + `README.md`.
  - Treats this as a small ingest batch focused only on Ingest, not the rest of the vault.

- **2) Safety / backup guardrails**
  - Run `obsidian_ensure_backup` (or `obsidian_create_backup` if needed) for the vault or at least `Ingest/`.
  - For each note, before the first destructive step (move, heavy overwrite, multi-step distill that changes structure), create a **per-change snapshot** under `Backups/Per-Change/...`.
  - Because you’re ingesting ~10 notes (above typical `batch_size_for_snapshot` like 5), it would also likely create a **batch snapshot record** in `Backups/Batch/...` summarizing the run.

- **3) Per-note ingest pipeline (roughly this order)**  
  For each `Ingest/*.md`:

  - **Read note content** (titles, headings, code blocks, links).
  - **PARA classification (`obsidian_classify_para`)**:
    - Almost everything looks like **evergreen reference** → classified as `para-type: resource`.
    - It has no existing `Genesis` hub or project to latch onto, so project/area inference is weak:
      - Probably invents something like a conceptual project-id (`genesis-docs` / `world-builder-genesis`) but with low–medium confidence.
  - **Frontmatter enrich (`frontmatter-enrich` skill)**:
    - Add/normalize:
      - `created: <today>`
      - `para-type: resource`
      - `tags: [ingest, github-doc, genesis?]` (based on filenames and minimal tags)
      - Possible guess at `project-id` (e.g. `genesis-engine`) but often in the **mid-confidence band**.
  - **Name suggestions (`name-enhance` skill)**:
    - Most filenames already descriptive (`docs--WORLD_BUILDER_WIZARD_GUIDE.md` etc.), so:
      - It might propose a **cleaner kebab name** (e.g. `world-builder-wizard-guide-YYYY-MM-DD-HHMM.md`).
      - In an empty vault, it will be **very conservative about auto-renaming**, so many renames stay as **proposals / suggestions**, not applied moves.
  - **Subfolder-organize (path proposal + possible move)**:
    - With no existing PARA tree, it must **invent initial structure**:
      - Likely proposes `3-Resources/Genesis/Docs/...` or `3-Resources/Dev-Docs/Genesis/...` style paths.
      - It sees words like `GUIDE`, `IMPLEMENTATIONS`, `INTEGRATION` → strongly “resource-doc” flavored → 3-Resources over 1-Projects.
      - For `Genesis-Docs-Timeline.md`, it may treat it as a **hub/index** and propose something like `3-Resources/Genesis/Genesis-Docs-Timeline.md`.
    - **Path confidence** is mostly **mid-band (72–84%)** for these first proposals because:
      - No neighbors exist yet.
      - No established `Genesis` area/project tree.
  - **Confidence loop (mid-band refinement)**:
    - Notes in 72–84% range trigger **one self-critique loop**:
      - Re-checks headings like “World Builder Wizard”, “Terrain3D Integration”, “Timeline”.
      - Might tighten path names a bit (e.g. add `Engine` or `Godot` to the folder).
      - Often increases confidence a little (e.g. from 76% → 81%), but still not obviously “this is 95% right”.
  - **Distill & highlight (autonomous-distill-like steps inside ingest)**:
    - Generate a **minimal TL;DR** and/or distillation layers:
      - For technical guides → short summary, bullets for key calls, maybe code-section highlights.
    - Apply **color highlighting** (distill-highlight-color) based on inferred project color (probably generic at first).
    - Extract obvious tasks (if any) via `next-action-extract`:
      - Most of these docs are pure reference → few or no tasks.
  - **Task reroute / hubs**:
    - Because these are reference docs with almost no `[ ]` tasks, `task-reroute` probably does little.
    - Genesis-Docs-Timeline may be seen as quasi-hub; it might get a “hub-like” frontmatter but with **low–mid confidence** since it’s the first one.
  - **Move out of Ingest (if allowed by confidence)**:
    - For each note:
      - If classification + path_conf **≥ high threshold (~85%)**, and snapshot success → actually **move** from `Ingest/` to the new path.
      - If still in **mid-band** after loop (72–84%), or snapshot fails → **do not move yet**; instead append a **proposal callout** and keep it in `Ingest/` with `#review-needed` / approval gating.
      - If **<72%**, no move at all; just a proposal + logging.

- **4) Logging / Watcher integration**
  - Append a **run result** line to `3-Resources/Watcher-Result.md` summarizing “INGEST MODE” batch, with `status: success|failure`, very short message, and timestamp.
  - Append one entry per note to an ingest log (e.g. `3-Resources/Ingest-Log.md`) with confidences, paths, and whether it was moved vs left as proposal.

---

## 2. Simulated full cleanup / reset outcome

### 2.1 What backups/snapshots would be created?

- **External backups (BACKUP_DIR)**
  - At least **one vault-level or Ingest-level backup** at the start via `obsidian_create_backup` (if `ensure_backup` reports none recent).
  - This backup includes:
    - All `Ingest/*.md`, notably every Genesis doc and `Genesis-Docs-Timeline.md`.
    - Possibly the entire vault, but in an almost-empty vault that’s cheap.

- **Per-change snapshots (SNAPSHOT_DIR under `Backups/Per-Change/`)**
  - For each note where a **destructive action** happens (move, potential rename, heavy distill rewrite):
    - A **per-change snapshot** is written for that specific file **before** the change.
  - In this scenario:
    - Any note that actually gets moved out of Ingest → **has at least one per-change snapshot**.
    - Notes only getting frontmatter/metadata enrich (non-destructive) might skip per-change snapshots, depending on your exact config; destructive gates are strict, but metadata updates are allowed without snapshots.

- **Batch snapshot (BATCH_SNAPSHOT_DIR under `Backups/Batch/`)**
  - Because the batch (`~10` notes) is larger than the default `batch_size_for_snapshot` (e.g. 5), the system likely:
    - Creates **one batch snapshot note** summarizing:
      - Which Ingest notes were touched.
      - Overall confidence bands.
      - High-level path proposals and moves.
    - This is more of a **run-level checkpoint**, not a copy of each note.

### 2.2 Which files stay in `Ingest/` vs get moved / rejected?

- **Likely moved out of `Ingest/` (high-enough confidence)**  
  These are easiest to classify as `3-Resources` reference docs:

  - `docs--SYSTEM_IMPLEMENTATIONS.md`
  - `docs--WORLD_BUILDER_WIZARD_GUIDE.md`
  - `docs--TERRAIN3D_INTEGRATION_GUIDE.md`
  - Any other `docs--*.md` that are obviously:
    - Tutorials
    - Architecture overviews
    - Integration guides

  **Behavior:**

  - Classified as `para-type: resource`.
  - Proposed path something like:
    - `3-Resources/Genesis/World-Builder/world-builder-wizard-guide-...md`
    - `3-Resources/Genesis/Integration/terrain3d-integration-guide-...md`
  - For a subset where classification + path_conf after loop get **≥85%**, and snapshot succeeds:
    - The system actually **moves them** out of `Ingest/` into the new `3-Resources/...` subtrees.
  - These newly created folders become the **seed PARA structure for Genesis docs**, but it’s all invented on the fly.

- **Likely left in `Ingest/` with proposals (mid or low band)**

  - `README.md`:
    - Filename is generic; content might look like a mixture of:
      - Repo overview
      - Maybe some roadmap-ish or marketing language
    - PARA classifier wavers between:
      - `para-type: project` (if it smells like an active codebase root)
      - `para-type: resource` (if it’s just reference)
    - Confidence often **mid or even low** because there is **no existing Genesis project or area**:
      - Might land \(65–78\%\).
    - Result:
      - Stays in `Ingest/`.
      - Gains **one or more [!proposal] callouts** with suggested path(s).
      - Tagged `#review-needed` or similar for manual decision.

  - `Genesis-Docs-Timeline.md`:
    - Clearly special, but the system **doesn’t know yet** if it’s:
      - A project-level planning doc (1-Projects).
      - A meta-resource/hub note (3-Resources).
    - Likely classification:
      - First pass: `para-type: resource`, `ingest_conf ~75–83%`.
      - After loop: maybe `80–86%` but with uncertainty about whether it’s a hub or just another resource.
    - Behavior:
      - Very plausible **first run leaves it in `Ingest/`** with a strong proposal:
        - e.g. “Treat this as `3-Resources/Genesis/Genesis-Docs-Timeline-...md` (hub)” but held behind manual approval.
      - Or, if it barely crosses the high threshold, it might be moved — but still with callouts that **might be slightly wrong or too opinionated** about its role.

  - Any file whose content mixes:
    - Roadmap-ish language
    - Implementation details
    - Personal notes
    - …will often stay in `Ingest/` after the first run, with proposals rather than moves.

- **Rejected/excluded**
  - Because everything here is valid `.md`:
    - **Nothing is outright rejected or dropped**.
    - “Exclusion” effectively means “left in Ingest with a proposal + manual review flag”.

### 2.3 Confidence bands for these notes (first pass)

Roughly, in an almost-empty vault with only these genesis docs:

- **High-confidence (≥85%)**
  - **Minority** of notes (maybe 2–3 of ~11):
    - The clearest “pure reference” guides (e.g. a well-structured integration guide with clear title and no project/roadmap ambiguity).
  - These are the only ones that are **reliably moved** out of `Ingest/` in the first pass.

- **Mid-band (72–84%)**
  - **Majority** of notes (perhaps 6–7 of ~11):
    - Most `docs--*.md` where:
      - PARA type “resource” is obvious, but
      - The *exact* PARA path (which project/area, how deep, how to name the parent) is guessy.
    - `Genesis-Docs-Timeline.md` very likely lands here.
  - These trigger the **self-critique loop**, but:
    - They still don’t feel solid enough to auto-move confidently in a system with strict safety gates.
    - Many will be left in `Ingest/` pending approval, even if the proposed path is “probably fine”.

- **Low-confidence (<72%)**
  - A **small subset** (maybe 1–2 notes):
    - Usually the most ambiguous ones:
      - `README.md` that looks like it could be:
        - A project root doc (`1-Projects/Genesis-Engine/README-...md`)
        - Or a general overview resource (`3-Resources/Genesis/Overview-...md`).
    - Or any file where structure is minimal (flat text, no headings, no clear domain cues).
  - These get **proposals only**, no destructive actions at all.

### 2.4 Proposal callouts & manual approval steps

On notes not auto-moved, you’d see several layers of “please approve” signals:

- **In-note proposal callouts**
  - For mid-band or low-band notes, appended near the top or bottom, e.g.:

    - A PARA classification callout:
      - “Suggest `para-type: resource` under `3-Resources/Genesis/...` (conf: 78%).”
    - A path proposal callout:
      - “Proposed path: `3-Resources/Genesis/Docs/Terrain3D-Integration-Guide-....md` (path_conf: 81%). Approve to move.”
    - Possibly multiple ranked options if the loop surfaces 2–3 plausible paths.

- **Manual approval levers**
  - One or both of:
    - A frontmatter flag the system expects you to flip:
      - `approved: true` (or a similar field) to accept the proposal on a future run.
    - Clear text inside the proposal callout telling you:
      - “If this looks correct, set `approved: true` in frontmatter or run INGEST MODE again after confirming this path.”

- **Queue / Mobile-Pending-Actions hooks**
  - For especially ambiguous notes (low-confidence):
    - The system may write a preview/proposal entry to a **Mobile-Pending-Actions** note with:
      - Note path
      - Proposed PARA path(s)
      - Confidence scores
      - Short rationale
    - These are then meant to be **reviewed by you**, edited, and later re-queued once you’ve made a decision.

---

## 3. How messy is that first raw ingest in an empty vault?

**Very.** In honest terms:

- **Path invention is guessy.**
  - The system must **invent the entire Genesis PARA subtree** on the fly, with no examples:
    - Names like `3-Resources/Genesis/Docs/` or `3-Resources/Game-Dev/Genesis/` are plausible but arbitrary.
    - There’s a high risk that later, once you actually define a `Genesis` project/area, you’ll want to rename/move everything again.

- **Central vs peripheral docs are hard to distinguish.**
  - `Genesis-Docs-Timeline.md` might be treated as:
    - A regular resource doc
    - A meta-hub
    - A proto-roadmap
  - The system has no real “neighbor fit” yet, so it over-relies on filename words and a few headings.

- **Confidence is mostly mid-band.**
  - Most notes are **“probably resources”** but:
    - The exact **path**, **project-id**, and **hub vs leaf** roles are not clear.
    - So the system litters notes with **proposal callouts** and holds back many moves to avoid unsafe decisions.

- **You end up with:**
  - A handful of moved notes seeding `3-Resources/...`.
  - A **noisy Ingest folder** still containing:
    - Timeline, README, and any cross-cutting docs.
    - Multiple **proposal callouts**, often with slightly different path suggestions.
  - A small constellation of **backups and snapshots** making rollback safe but visually cluttering your logs.

In other words, the first run of “INGEST MODE” in an almost-empty vault with only Genesis docs would be **safe but structurally noisy**: lots of partial organization, many conservative proposals, and only a few confidently moved notes. A second pass, after you hand-curate a couple of key decisions (e.g. “this is the Genesis Area root; these live under 3-Resources/Game-Dev/Genesis”), would dramatically increase confidence and reduce that mess.

---

**User**

Simulate the Second Brain autopilot doing a minimal-guidance ingest + roadmap pass on the current vault state.

Current state:
- Ingest/ has Genesis-Docs-Timeline.md (with project-id: genesis-mythos, para-type: Resource, highlight_perspective: geosynchronous-view) + the usual flattened mythos docs
- No rich frontmatter on most files, no highlight_key, mostly empty PARA folders

Simulate this exact queue being processed via EAT-QUEUE:

{"mode":"INGEST MODE","prompt":"process remaining genesis-mythos docs","source_file":"Ingest/","id":"test-minimal-1"}
{"mode":"HIGHLIGHT PERSPECTIVE","prompt":"geosynchronous-view","source_file":"3-Resources/Genesis-Mythos/","id":"test-minimal-2"}
{"mode":"BATCH-EXPRESS","prompt":"consolidate into single living roadmap note","source_file":"3-Resources/Genesis-Mythos/","id":"test-minimal-3"}
{"mode":"roadmap-ingest","prompt":"parse timeline into phases","source_file":"3-Resources/Genesis-Mythos/Genesis-Docs-Timeline.md","id":"test-minimal-4"}

For each queue entry, describe:
- Which MCP tools/skills would fire
- Expected confidence band before/after any refinement loop
- What the resulting roadmap note would roughly look like (structure, depth, color usage or lack thereof)
- Any proposal/preview callouts or manual approval gates that would appear

Focus on how sparse/minimal the output would be with almost no guidance.

---

**Cursor**

## Overview

You’ve essentially queued: **(1)** minimal ingest, **(2)** apply perspective/highlight, **(3)** lightweight express pass to make a “roadmap” hub, **(4)** then a dedicated roadmap parse on the timeline. With almost no config or existing structure, the system will stay conservative and output a pretty sparse, “first-draft” roadmap.

I’ll walk through each queue entry.

---

## 1) `INGEST MODE` (`id: test-minimal-1`)

**Queue line**

```json
{"mode":"INGEST MODE","prompt":"process remaining genesis-mythos docs","source_file":"Ingest/","id":"test-minimal-1"}
```

### Which MCP tools/skills would fire

Per ingest rules + skills list, roughly in this sequence for each `Ingest/*.md`:

- **Safety / backup**
  - `obsidian_ensure_backup` → possibly `obsidian_create_backup` (vault or `Ingest/`).
- **Core ingest pipeline**
  - `obsidian_list_notes` on `Ingest/`.
  - For each note:
    - `obsidian_read_note`
    - `obsidian_classify_para`
    - `frontmatter-enrich` (skill)
    - `name-enhance` (propose better filename only; conservative on rename)
    - `obsidian_split_atomic` (probably **no-op** here because docs are already fairly atomic and “flattened”)
    - `split-link-preserve` (no-op if no split)
    - `obsidian_distill_note` (short TL;DR / headings-level summary)
    - `distill-highlight-color` (basic/high-level highlighting; no project color tuning yet)
    - `next-action-extract` (almost no tasks; mostly empty or 1–2 technical TODOs if any)
    - `task-reroute` (likely does nothing; these are reference docs, not task dumps)
- **Organizing / moving**
  - `subfolder-organize` (skill) to propose a path under something like `3-Resources/Genesis-Mythos/...`.
  - If `ingest_conf` / `path_conf` ≥ high threshold and destructive step allowed:
    - `obsidian-snapshot` (per-change, skill) on the note.
    - `obsidian_move_note` (first dry_run: true, then dry_run: false if safe).
- **Logging**
  - `obsidian_log_action` for each note.
  - Append one line to `3-Resources/Watcher-Result.md` for `id: test-minimal-1`.

### Confidence band (before / after loop)

- **Before loop**
  - Genesis docs already have `project-id: genesis-mythos` on the timeline and minimal tags on others, so classification is easier than in a truly empty vault:
    - Most `docs--*.md`: `ingest_conf` ~ **78–84%** (upper mid-band).
    - `Genesis-Docs-Timeline.md`: `ingest_conf` ~ **80–86%** (mid/high edge) as a “resource hub”.
- **Refinement loop**
  - For notes in 72–84%:
    - One **ingest-refine** loop per note:
      - Re-checks titles (“WORLD_BUILDER_WIZARD_GUIDE”, “TERRAIN3D_INTEGRATION_GUIDE”, etc.).
      - Leans harder into `3-Resources/Genesis-Mythos/` as the base.
    - After loop:
      - Many rise slightly to **82–88%**.
      - A couple may nudge over the high threshold (~85%) and become eligible for auto-move.
- **Outcome**
  - **High band (≥85%)**: some of the clearly pure reference guides (integration/how-to docs).
  - **Mid band**: the bulk, especially `Genesis-Docs-Timeline.md` and any ambiguous/general docs.
  - **Low band (<72%)**: probably none, unless one file is extremely underspecified.

### Resulting changes (sparse state)

- A handful of genesis docs are **moved** from `Ingest/` to something like:
  - `3-Resources/Genesis-Mythos/Docs/world-builder-wizard-guide-…md`
  - `3-Resources/Genesis-Mythos/Docs/terrain3d-integration-guide-…md`
- Others (including `Genesis-Docs-Timeline.md` if it stays mid-band) **remain in `Ingest/`** with:
  - Frontmatter populated (`para-type: resource`, `project-id: genesis-mythos`, `tags: [ingest, github-doc, genesis-mythos]`).
  - A short TL;DR and minimal highlighting (generic colors).
- PARA folders:
  - A very **thin skeleton** under `3-Resources/Genesis-Mythos/`:
    - Maybe `Docs/`, maybe one or two extra subfolders inferred from filenames (“Integration”, “Architecture”), but nothing rich.

### Proposal/preview callouts & manual approval

On mid-band notes (especially those left in `Ingest/`):

- **[!proposal]**-style callout such as:
  - “Proposed path: `3-Resources/Genesis-Mythos/Docs/terrain3d-integration-guide-...md` (path_conf: 82%).”
- Guidance like:
  - “Set `approved: true` in frontmatter or re-run INGEST MODE after confirming to apply this move.”
- For `Genesis-Docs-Timeline.md`:
  - Might propose treating it as a **hub resource** under `3-Resources/Genesis-Mythos/Genesis-Docs-Timeline-...md`.
  - Still likely **gated behind approval** on this first minimalist run.

Overall it’s a **light touch** ingest: a few moves, shallow summaries, and a lot of “here’s what I *would* do, please confirm”.

---

## 2) `HIGHLIGHT PERSPECTIVE` (`id: test-minimal-2`)

**Queue line**

```json
{"mode":"HIGHLIGHT PERSPECTIVE","prompt":"geosynchronous-view","source_file":"3-Resources/Genesis-Mythos/","id":"test-minimal-2"}
```

### Which MCP tools/skills would fire

Targeting all notes now under `3-Resources/Genesis-Mythos/` (those already moved):

- **Read + scan**
  - `obsidian_list_notes` on `3-Resources/Genesis-Mythos/`.
  - `obsidian_read_note` for each.
- **Highlight / perspective skills**
  - `distill-highlight-color` again, now with the explicit perspective “geosynchronous-view”.
  - `highlight-perspective-layer` (skill):
    - Sets `highlight_angles` and `data-drift-level` attributes in the note.
    - Uses `highlight_perspective: geosynchronous-view` already present on `Genesis-Docs-Timeline.md` as a cue.
- **Optional**
  - May lightly touch `frontmatter-enrich` to persist `highlight_perspective: geosynchronous-view` consistently.

Watcher result line appended for `id: test-minimal-2`.

### Confidence band (before / after loop)

This mode is mostly deterministic styling, not PARA decisions:

- **Before loop**
  - `distill_conf` / similar signals are effectively **high (≥90%)**:
    - You’ve already tagged `highlight_perspective`, and the scope is tightly defined (`3-Resources/Genesis-Mythos/`).
- **Refinement loop**
  - No destructive actions, no path decisions → **no mid-band refinement loop needed**.
  - Remains high-confidence; no gating.

### Resulting highlighting (sparse)

Because you **don’t have a configured `highlight_key` or tuned color scheme**:

- `distill-highlight-color` uses **generic**, default colors (e.g. one or two tones).
- `highlight-perspective-layer`:
  - Adds perspective-related metadata and maybe a faint **drift gradient** (core → periphery).
  - But visually this will be **subtle**:
    - No project-specific accent colors.
    - No elaborate gradient palette beyond a base + slight variants.

Most notes will just get:

- A few highlighted sentences per section.
- Maybe one drift indicator (e.g., attributes or minimal icons if your CSS supports it).

No structure changes, no new sections; just **thin extra markup on existing text**.

### Proposal/preview callouts & manual approval

- Normally none:
  - This pass is not moving or renaming anything.
  - It just annotates highlights/perspective.
- If any note looks too noisy or confusing, the pipeline rules would **log** that, but in practice there’s no explicit approval gate here.

---

## 3) `BATCH-EXPRESS` (`id: test-minimal-3`)

**Queue line**

```json
{"mode":"BATCH-EXPRESS","prompt":"consolidate into single living roadmap note","source_file":"3-Resources/Genesis-Mythos/","id":"test-minimal-3"}
```

### Which MCP tools/skills would fire

For all notes under `3-Resources/Genesis-Mythos/`:

- **Read + related**
  - `obsidian_list_notes` for `3-Resources/Genesis-Mythos/`.
  - `obsidian_read_note` for each.
  - `related-content-pull` (skill):
    - Finds links/semantic siblings across the genesis-mythos docs.
- **Snapshot for major append**
  - `version-snapshot` (skill):
    - Creates a `Versions/` snapshot of the chosen “roadmap” note before major append.
- **Express pipeline**
  - `express-mini-outline` (skill):
    - For each note, but crucially:
      - It **aggregates** outline info into a target “living roadmap” note.
  - `express-view-layer` (optional):
    - Annotates relation strengths in any “Related” sections.
  - `call-to-action-append`:
    - Adds a minimal CTA callout at the end (“Next: flesh out phases”, “Share/publish?”, etc.).
- **Choosing / creating the living roadmap target**
  - It has to pick a **target note** for the roadmap:
    - Most likely:
      - **Option A**: Use `Genesis-Docs-Timeline.md` (if already moved to `3-Resources/Genesis-Mythos/`).
      - **Option B**: Create a new `Genesis-Mythos-Roadmap-…md` under the same folder (or under `1-Projects/`, but that’s less likely without guidance).
    - In minimal-guidance mode it will lean toward:
      - **Reusing `Genesis-Docs-Timeline.md`** as the living roadmap, but **treat changes as preview/proposal** if confidence is not high.
- **Logging**
  - `obsidian_log_action` summarizing express_conf, chosen target, and whether append was committed or previewed.
  - Watcher-result line for `id: test-minimal-3`.

### Confidence band (before / after loop)

- **Primary signal**: `express_conf` (quality and appropriateness of the living roadmap).
- **Before loop**
  - With almost no prior roadmap or project structure:
    - `express_conf` for “this consolidation into a single roadmap is correct” is around **70–80%**:
      - It sees them as related (same project-id, same folder).
      - But it doesn’t know your preferred roadmap structure or phases.
- **Refinement loop (express-soft)**
  - One loop per chosen target note:
    - Re-checks headings in the docs (e.g. “Overview”, “Implementation Details”, “Integration Steps”).
    - Proposes phase-like groupings, e.g.:
      - Phase 1 — Core Engine
      - Phase 2 — World Builder
      - Phase 3 — Integrations & Tooling
    - Might bump `express_conf` into **78–84%**, still mid-band.
- **Outcome**
  - Very likely remains **mid-band**:
    - Enough to produce a **preview roadmap structure**.
    - Too low to confidently overwrite a hub/timeline note with a heavy append without gating.

### What the roadmap note would roughly look like

Assuming it chooses `Genesis-Docs-Timeline.md` as the living roadmap target but stays conservative:

- **Frontmatter tweaks**
  - Might add:
    - `express_view: true`
    - Maybe a `roadmap: true`-style flag (if your config supports it).
- **Structure (minimal)**

At the top or near the top, something like:

- A small, generated **TL;DR / “Roadmap snapshot”** section, e.g.:

  - **`## Roadmap (auto-draft)`**
    - _Phase 1 — Mythos Core & Engine_
      - Link to the core system doc(s).
    - _Phase 2 — World Builder & Authoring_
      - Link to `docs--WORLD_BUILDER_WIZARD_GUIDE.md`.
    - _Phase 3 — Terrain & Integrations_
      - Link to `docs--TERRAIN3D_INTEGRATION_GUIDE.md`, etc.

- **Depth**
  - 1–2 levels:
    - Phases.
    - A few bullets per phase, each bullet likely just:
      - A short label + a wiki-link to the underlying doc.
  - **Little or no task-level decomposition**; mostly “landmark doc” level.

- **Color usage**
  - Very light:
    - Maybe colored callouts around the phases (if `express-mini-outline` uses project color), but because:
      - No `highlight_key`.
      - No project-specific palette defined.
    - It will mostly be **default accent** callouts (e.g. `> [!info]`, `> [!summary]`) rather than a rich gradient scheme.

### Proposal/preview callouts & manual approval

Because `express_conf` stays mid-band:

- The new roadmap section is likely wrapped or prefaced with a **preview/proposal callout**, e.g.:

  - A block at the top:

    - “Auto-generated roadmap draft (express_conf: 81%). Edit, then set `approved: true` to adopt as main roadmap.”

- If the append is deemed too heavy for immediate commit:
  - The pipeline might:
    - Write a **preview-only** roadmap block to `Mobile-Pending-Actions` or a similar note.
    - Insert only a small pointer callout into `Genesis-Docs-Timeline.md`:
      - “Preview roadmap draft available in [[Mobile-Pending-Actions]] (id: …).”
- Either way, you’ll need to **approve** or manually adapt this structure before it becomes “the” canonical roadmap.

Overall, you get a **thin phase outline with links**, clearly marked as auto-draft.

---

## 4) `roadmap-ingest` (`id: test-minimal-4`)

**Queue line**

```json
{"mode":"roadmap-ingest","prompt":"parse timeline into phases","source_file":"3-Resources/Genesis-Mythos/Genesis-Docs-Timeline.md","id":"test-minimal-4"}
```

### Which MCP tools/skills would fire

This uses the dedicated **`roadmap-ingest` skill**:

- **Read / parse**
  - `obsidian_read_note` on `3-Resources/Genesis-Mythos/Genesis-Docs-Timeline.md`.
  - `roadmap-ingest` (skill):
    - Parses headings and bullet structure.
    - Standardizes to **phases / subphases / tasks**:
      - Phases derived from top-level sections / time segments.
      - Subphases based on nested headings or bullets.
      - Tasks derived from explicit todo markers or imperative bullet lines.
- **Output destination**
  - Depending on your skill config, likely:
    - Append a **structured checklist** back into `Genesis-Docs-Timeline.md`, or
    - Create a sibling `Genesis-Docs-Roadmap-…md` and link both ways.
- **Safety**
  - `version-snapshot` on `Genesis-Docs-Timeline.md` (major structural append).
  - `obsidian_screenshot` / `obsidian-snapshot` for per-change snapshot if considered destructive.
- **Logging**
  - `obsidian_log_action` with loop data.
  - Watcher result for `id: test-minimal-4`.

### Confidence band (before / after loop)

- **Before loop**
  - `express_conf` / `roadmap_conf` for “this is actually a roadmap-like timeline I can parse”:
    - Likely around **75–83%**:
      - It knows the note is timeline-ish.
      - But headings might be mixed (some purely descriptive, not phase-oriented).
- **Refinement loop (roadmap-specific)**
  - One pass applying the shared self-critique template:
    - Checks for contradictory signals (e.g. narrative history vs actionable phases).
    - Tests whether headings cluster naturally into phases.
  - After loop:
    - `roadmap_conf` maybe bumps to **80–86%**.
    - Still borderline for fully committing a heavy structural rewrite.
- **Outcome**
  - Many runs will **stay in mid-band**:
    - Enough to propose a roadmap structure.
    - Not enough to silently reframe the entire timeline as a strict checklist without gating.

### What the resulting roadmap structure would roughly look like

Whether in the same note or a sibling note, you’d get a **simple, standardized structure**, e.g.:

- **`## Roadmap Checklist (auto-ingested)`**
  - **Phase 1 — Origins & Core Myth**
    - `[ ] Document primordial entities`
    - `[ ] Validate creation-event consistency`
  - **Phase 2 — World Builder & Geography**
    - `[ ] Finalize world-builder wizard flows`
    - `[ ] Align terrain generation with mythic beats`
  - **Phase 3 — Integrations & Tooling**
    - `[ ] Integrate Terrain3D pipeline`
    - `[ ] Wire Genesis docs into engine docs site`

Key points:

- **Depth**
  - Mostly 2–3 levels:
    - Phase → bullet-style tasks.
  - Subphases appear only if the timeline has clear nested structure.
- **Links**
  - Tasks may link back to source docs:
    - `[ ] Align terrain generation [[docs--TERRAIN3D_INTEGRATION_GUIDE]]`
- **Colors**
  - Still minimal:
    - Checklists in plain markdown.
    - At most, a single callout around the entire checklist (e.g. `[!info] Roadmap (auto-ingested)`).
    - No elaborate color coding of phases because highlight/lens config is still barebones.

### Proposal/preview callouts & manual approval

Given mid-band confidence:

- The entire roadmap section is wrapped in a **proposal / auto-generated** wrapper, e.g.:

  - “Auto-ingested roadmap from timeline (roadmap_conf: 82%). Review before treating as authoritative.”

- There’s likely an explicit manual gate, such as:

  - A note in the callout:
    - “If this roadmap looks right, add `approved: true` in frontmatter to treat these phases as canonical.”
- If the skill writes to a **new note**:
  - The new note title may include “(auto-ingested)” and a suggestion to merge or curate later.
  - `Genesis-Docs-Timeline.md` then gets a small link callout pointing to it.

Net effect: you get a **first-cut checklist roadmap**, clearly labeled as “machine-draft, please curate”.

---

## Big-picture: how minimal does this all feel?

- **Ingest**: a light rehoming of docs into `3-Resources/Genesis-Mythos/` with short TL;DRs and generic highlighting.
- **Highlight perspective**: a thin layer of extra highlight metadata; visually subtle due to lack of project-specific palettes.
- **Batch-express**: a single “living roadmap” section that is:
  - Phase-level only.
  - Mostly just **linked bullets** to genesis docs.
  - Wrapped in a “draft/preview” callout.
- **Roadmap-ingest**: a more structured checklist extracted from the timeline:
  - Clearer phases, but still modest in depth.
  - Conservatively labeled as auto-ingested, requiring approval.

Everything is **safe, mid-confidence, and clearly marked as provisional**—useful scaffolding, but far from a richly colored, fully-trusted roadmap without your manual passes.

---

**User**

Simulate the Second Brain autopilot with basic-level guidance.

Vault state same as before: timeline has geosynchronous-view frontmatter, other Ingest files mostly bare.

Simulate this queue being eaten:

{"mode":"INGEST MODE","prompt":"process remaining genesis-mythos docs with geosynchronous lens: 2D Azgaar maps to Terrain3D open world + lore/combat/equipment/politics systems","source_file":"Ingest/","id":"test-basic-1"}
{"mode":"HIGHLIGHT PERSPECTIVE","prompt":"geosynchronous-view: 2D Azgaar modular maps → Terrain3D open world + lore support systems, combat, equipment, politics","source_file":"3-Resources/Genesis-Mythos/","id":"test-basic-2"}
{"mode":"BATCH-EXPRESS","prompt":"consolidate into single living roadmap note using timeline as backbone; pull related content across all distilled docs","source_file":"3-Resources/Genesis-Mythos/","id":"test-basic-3"}
{"mode":"roadmap-ingest","prompt":"parse timeline + distilled docs into phases: maps, terrain, lore, combat, equipment, politics; output hierarchical checklist","source_file":"3-Resources/Genesis-Mythos/Genesis-Docs-Timeline.md","id":"test-basic-4"}

Step-by-step:
- Confidence improvement from the extra lens phrase?
- How much more structure appears in distill/highlight/roadmap phases?
- Rough shape of the final roadmap note (headings, checklist depth, any Related section?)
- Still any mid-band loops or proposals, or does it mostly hit high confidence?

Compare briefly to the minimal version.

---

**Cursor**

### Overall

With your extra lens text, the autopilot still stays conservative, but it has just enough domain shape to cluster things into “maps → terrain → lore → combat → equipment → politics” and to treat the timeline as the backbone for a single roadmap, instead of scattering half-baked proposals.

---

## 1) `test-basic-1` — `INGEST MODE` (Ingest/)

**Likely tools/skills**

- Backup/snapshot: `obsidian_ensure_backup` → `obsidian_create_backup` if needed; per-note `obsidian-snapshot` before any moves.
- Ingest core:
  - `obsidian_list_notes` on `Ingest/`
  - `obsidian_read_note` for each genesis doc
  - `obsidian_classify_para` (all still mostly `para-type: resource`, project-id `genesis-mythos`)
  - `frontmatter-enrich` (fills `created`, `para-type`, `project-id: genesis-mythos`, tags, maybe `highlight_perspective: geosynchronous-view` inherited from the timeline)
- Naming/paths:
  - `name-enhance` (proposed better slugs, mostly kept as suggestions)
  - `subfolder-organize` (now biased by prompt into something like `3-Resources/Genesis-Mythos/` with subfolders that mirror the phases: `Maps/`, `Terrain/`, `Lore/`, `Combat/`, `Equipment/`, `Politics/`)
- Distill layer:
  - `auto-layer-select` (simple 1–2 layers)
  - `obsidian_distill_note` (short TL;DR & bullets per doc)
  - `distill-highlight-color` (colors anchored to the `geosynchronous-view` lens; maps/terrain vs lore vs combat/etc get more consistent hues)
  - `highlight-perspective-layer` (applies drift-level markers based on the geosynchronous lens)
  - `next-action-extract` (still finds few tasks; most docs remain pure reference)
  - `split_atomic` + `split-link-preserve` only if a doc is obviously multi-topic and long.

**Confidence bands**

- Before loop:
  - `ingest_conf` / `path_conf` for most genesis docs: **low–mid 80s** instead of high 70s:
    - Prompt ties content to a clear system (“2D Azgaar → Terrain3D + systems”), so `subfolder-organize` no longer has to guess the domain; it has six named buckets.
- After single refinement loop (only for 72–84 band):
  - Many docs now cross the **high threshold (≥85%)**:
    - Path proposals like `3-Resources/Genesis-Mythos/Maps/...` or `/Combat/...` feel internally consistent with prompt + filenames.
  - Only edge cases (e.g. hybrid docs or very generic README-like content) remain mid-band.

**Result**

- **Ingest mostly empties**:
  - The majority of flattened genesis docs are moved into `3-Resources/Genesis-Mythos/<Phase>/...` with per-change snapshots.
  - `Genesis-Docs-Timeline.md` is treated as **anchor resource** in `3-Resources/Genesis-Mythos/` and probably moved, since project-id + lens are already there and the prompt explicitly mentions it.
- Remaining in `Ingest/`:
  - Only truly ambiguous notes (e.g. an odd README) stay, with **proposal callouts**:
    - 1–2 suggested paths (e.g. `3-Resources/Genesis-Mythos/Meta/README-...md` vs some project-root path).
    - Manual approval instructions (`approved: true` or re-queue with a mode).

---

## 2) `test-basic-2` — `HIGHLIGHT PERSPECTIVE` (3-Resources/Genesis-Mythos/)

**Likely tools/skills**

- `obsidian_list_notes` / `obsidian_read_note` under `3-Resources/Genesis-Mythos/`
- Distill/highlight:
  - `auto-layer-select` (light)
  - `obsidian_distill_note` (tightens TL;DR sections if missing)
  - `distill-highlight-color` (now explicitly instructed: “geosynchronous-view: 2D Azgaar modular maps → Terrain3D open world + lore support systems, combat, equipment, politics”)
  - `highlight-perspective-layer` (marks drift/angle per section based on which of the six axes it belongs to)
  - `distill-perspective-refine` (optionally tweaks TL;DR callouts to reflect the geosynchronous angle)
  - `readability-flag` for any hard-to-read doc.

**Confidence bands**

- Highlight-related confidence (`distill_conf` / highlighting decisions):
  - Minimal run: mid-band (75–82%).
  - Basic-guidance run: mostly **≥85%**:
    - The lens string itself encodes the six categories, so color-assignments and drift layers have a clear mapping.

**Resulting structure**

- Each doc:
  - Has a **short TL;DR callout** framed by the geosynchronous-view lens (e.g. “From orbit: how maps feed into Terrain3D + systems”).
  - In-text highlights are **more coherent**:
    - One hue for map topology & modularity.
    - A related/analogous hue for Terrain3D technical integration.
    - Distinct but harmonious hues for lore, combat, equipment, politics.
- Proposal/approval:
  - Because this mode is non-destructive (mostly styling/summary), there are almost **no proposal callouts**, just:
    - Occasional readability warnings.
    - Maybe a “preview-only” suggestion for a very ambiguous doc, but that’s rare here.

---

## 3) `test-basic-3` — `BATCH-EXPRESS` (single living roadmap, folder-wide)

**Likely tools/skills**

- Safety:
  - `obsidian_ensure_backup` (batch-level)
  - `version-snapshot` on the note chosen/created as the “living roadmap” before major append.
- Express pipeline:
  - `obsidian_list_notes` + `obsidian_read_note` for `3-Resources/Genesis-Mythos/`
  - `related-content-pull`:
    - Anchors on `Genesis-Docs-Timeline.md` and pulls all genesis docs as related.
  - `express-mini-outline`:
    - Builds a **consolidated outline** using:
      - Timeline order as spine.
      - The six domains (maps, terrain, lore, combat, equipment, politics) as sub-sections.
  - `express-view-layer`:
    - Adds connection-strength markers (e.g. which doc is core vs peripheral for each domain).
  - `call-to-action-append`:
    - A subtle “Next: implement / playtest / publish?” callout.

**Confidence bands**

- Express / roadmap confidence (`express_conf`):
  - Minimal run: ~78–84% for “one roadmap” decision and outline.
  - Basic-guidance run:
    - Prompt directly says “consolidate into single living roadmap note using timeline as backbone”.
    - This resolves the primary ambiguity:
      - Now there is *one obvious target* (either:
        - new `Genesis-Mythos-Roadmap.md`, or
        - the timeline itself, but roadmap-ingest below will more strongly argue for a separate note).
    - `express_conf` ~ **86–92%** after one loop; destructive append (big roadmap content) becomes allowed.

**Roadmap note: rough shape**

- **Location** (high-confidence path, thanks to “roadmap” wording):
  - Likely `1-Projects/Genesis-Mythos/Roadmap/Genesis-Mythos-Roadmap.md`, using your existing `Example-Roadmap.md` structure as a template.
- **Structure** (sparse but coherent):

  - Title & frontmatter:
    - `title: Genesis Mythos – Geosynchronous Roadmap`
    - `project-id: genesis-mythos`
    - `para-type: project` (for roadmap, even though the source docs are resources)
    - `distill_lens: geosynchronous-view`
  - Top sections (inspired by `Example-Roadmap.md`, but lighter):

    - `## Overview`
      - 3–5 bullet summary tying Azgaar → Terrain3D → systems.

    - `## Phases` (timeline backbone + six categories merged):
      - `### Phase 1 – Maps`
        - Checklist items referencing specific docs:
          - `[ ] Import modular Azgaar regions into Godot/Genesis`
          - Links to map-related guides.
      - `### Phase 2 – Terrain`
      - `### Phase 3 – Lore`
      - `### Phase 4 – Combat`
      - `### Phase 5 – Equipment`
      - `### Phase 6 – Politics`
        - Each phase with 3–7 tasks; 2-level nesting at most (phase → subtask).

    - `## Dependencies & Risks` (very short list extracted from integration docs)
    - `## Related Docs`
      - Bulleted wiki-links to the genesis resource docs, grouped by the six axes.
      - Connection indicators colored/annotated via `express-view-layer`.

- **Color usage**

  - The note itself:
    - Uses only **subtle callout tinting** and highlight colors inherited from earlier steps.
    - No fancy project palette beyond what lens + highlight provided.
  - Tasks:
    - Mostly plain markdown checkboxes; a few key ones might be in colored callouts (e.g. `[!important]` style).

- **Approvals / proposals**

  - Because this is a **new note** (or a large append to a clearly-named roadmap path) and you explicitly asked for it:
    - `express_conf` + `path_conf` are high → **no proposal-gated write**, just:
      - Version snapshot
      - Direct write.
  - You might still see a small callout near the top like:
    - “Generated geosynchronous-view roadmap from Genesis-Docs-Timeline.md + related docs. Mark `approved: true` once you’ve skimmed this,”
    - but it would be advisory rather than blocking further use.

---

## 4) `test-basic-4` — `roadmap-ingest` (Genesis-Docs-Timeline → checklist)

**Likely tools/skills**

- `obsidian_read_note` on `Genesis-Docs-Timeline.md`
- `roadmap-ingest` skill:
  - Uses the prompt phases:
    - `maps, terrain, lore, combat, equipment, politics`
  - Parses headings/bullets in the timeline.
  - Maps each item into the most fitting phase.
- Possible follow-ups:
  - Append the resulting checklist **into the new roadmap note** (if configured that way) or into the timeline with links back to the roadmap.
  - `obsidian-snapshot` before this append if it’s major.

**Confidence bands**

- Because the phases are **explicitly given in the prompt** and already match the lens used earlier:
  - `roadmap-ingest` confidence on phase assignment: **high (88–94%)**.
  - Only ambiguous items (multi-domain bullets) get mid-band treatment internally (e.g. “Lore-influenced equipment” tasks might have a small internal conflict, but the system still picks a primary phase).

**Checklist structure**

- In the roadmap note (or timeline) you end up with something like:

  - `## Checklist by Phase`
    - `### Maps`
      - `[ ] Choose base Azgaar world topology`
      - `[ ] Define modular region schema for export`
    - `### Terrain`
      - `[ ] Map regions → heightmaps for Terrain3D`
    - `### Lore`
      - …
    - etc.

- Depth:
  - Typically 2–3 levels deep at most:
    - Phase → group → atomic tasks.
  - No deep Gantt-like nesting; this remains **sparse and implementer-friendly**, not a full PM plan.

- Proposals:
  - Very few:
    - Maybe a short note if some bullets couldn’t be confidently placed in one phase:
      - A callout listing “unplaced” or “cross-phase” items for manual triage.

---

## 5) Comparison to the minimal-guidance run

- **Confidence**:
  - Minimal: most genesis docs and the roadmap idea sit in the **mid band (72–84%)**, with many moves and roadmap structures gated behind proposals.
  - Basic-guidance: your lens + explicit phases push:
    - Folder layout and classification to **mid–high 80s**.
    - Highlighting and roadmap-ingest to **solidly high 80s–low 90s**.
- **Structure**:
  - Minimal: scattered proposals, multiple possible hubs, and a noisy Ingest.
  - Basic-guidance:
    - Ingest almost fully drained into `3-Resources/Genesis-Mythos/<Phase>/...`.
    - A **single, clearly-located living roadmap note** with:
      - Overview
      - Six phase sections
      - Shallow hierarchical checklist
      - Compact Related section.
- **Proposals**:
  - Minimal: lots of [!proposal] callouts, manual approval gates.
  - Basic-guidance: proposals shrink to edge cases (odd docs, cross-phase tasks); the core pipeline runs mostly in the **high-confidence / auto-apply band**.

---

**User**

Simulate the Second Brain autopilot with extensive, high-context guidance — the maximum we would feed it without changing rules/skills.

Vault state: same as above.

Simulate processing this queue:

{"mode":"INGEST MODE","prompt":"process remaining genesis-mythos docs with geosynchronous-view lens. Full context: modular Azgaar 2D fantasy maps → Terrain3D open-world integration (see TERRAIN3D_INTEGRATION_GUIDE), lore support systems, combat/equipment/progression loops, politics/faction simulation, world-builder wizard flow, rendering approach comparisons, SYSTEM_IMPLEMENTATIONS, and the Genesis-Docs-Timeline as chronological backbone. Force para-type: Resource, project-id: genesis-mythos, highlight_key: Genesis-Mythos-Key","source_file":"Ingest/","id":"test-extensive-1"}
{"mode":"HIGHLIGHT PERSPECTIVE","prompt":"geosynchronous-view: 2D Azgaar modular maps → Terrain3D open world pipeline + interconnected lore support systems, combat systems, equipment slots, politics/faction dynamics. Use analogous colors for related systems (maps→terrain, lore→combat), complementary for tensions (e.g. performance vs visual fidelity). Apply data-drift-level 0-3 on core concepts vs supporting details","source_file":"3-Resources/Genesis-Mythos/","id":"test-extensive-2"}
{"mode":"BATCH-EXPRESS","prompt":"consolidate ALL distilled mythos notes into ONE living roadmap note using Genesis-Docs-Timeline as backbone. Run related-content-pull across every phase, express-mini-outline with project colors, version-snapshot first, and append CTA for next implementation steps. Include cross-links and color-coded geosynchronous flow (2D→3D + lore/combat/politics layers)","source_file":"3-Resources/Genesis-Mythos/","id":"test-extensive-3"}
{"mode":"roadmap-ingest","prompt":"parse timeline + every distilled doc into full hierarchical roadmap with phases: 1-Maps (Azgaar modular), 2-Terrain3D integration, 3-Lore support systems, 4-Combat & equipment, 5-Politics & factions, 6-World-builder wizard & rendering. Output standardized phases/subphases/tasks checklist, auto-link to source notes, preserve highlight_perspective and highlight_angles in frontmatter","source_file":"3-Resources/Genesis-Mythos/Genesis-Docs-Timeline.md","id":"test-extensive-4"}

Describe in detail:
- Confidence bands — does extensive context push almost everything to high (≥85%) after loops?
- Quality of highlighting (analogous/complementary usage, drift levels)
- Structure and richness of the final roadmap note (phases, sub-tasks, links, CTAs)
- How well it establishes a reusable vault pattern for future ingests

Compare to minimal and basic versions — is the extra guidance worth it for the first foundational run?

---

**Cursor**

## Overall effect of “maximum guidance”

With that much explicit context, the autopilot stops guessing *what* Genesis-Mythos is and mostly focuses on *organizing and wiring it together*. Confidence jumps, more notes get moved out of `Ingest/`, and the roadmap is richer and more reusable as a pattern—but it still won’t be perfect.

Below is the run-by-run simulation.

---

## 1) `INGEST MODE` — `test-extensive-1`

**Prompt (key effects)**

- Forces:
  - **`para-type: Resource`**
  - **`project-id: genesis-mythos`**
  - **`highlight_key: Genesis-Mythos-Key`**
- Names explicit anchors:
  - Azgaar 2D maps, Terrain3D integration, lore/combat/equipment/politics, world-builder wizard, SYSTEM_IMPLEMENTATIONS, Genesis-Docs-Timeline.

### Tools / skills that fire

- **Safety & discovery**
  - `obsidian_ensure_backup` → if stale, `obsidian_create_backup` (vault or `Ingest/`).
  - `obsidian_list_notes` on `Ingest/`.

- **Per note (`Ingest/*.md`)**
  - `obsidian_read_note`
  - **Classification, but with strong overrides:**
    - `obsidian_classify_para` still runs, but:
      - The prompt’s “force para-type: Resource, project-id: genesis-mythos” effectively overrides/locks the main fields.
      - Internal `ingest_conf` is now mostly about *path* and *role*, not basic type/project.
  - `frontmatter-enrich`:
    - Ensures:
      - `para-type: resource` (locked)
      - `project-id: genesis-mythos`
      - `highlight_key: Genesis-Mythos-Key`
      - `highlight_perspective: geosynchronous-view` on the timeline (already present, now trusted).
      - Standard `created`, `status`, minimal tags (e.g. `[ingest, genesis-mythos, github-doc]`).
  - `name-enhance`:
    - Proposes cleaner, consistent names like:
      - `terrain3d-integration-guide-YYYY-MM-DD-HHMM.md`
      - `system-implementations-YYYY-MM-DD-HHMM.md`
    - With explicit domain context, it can:
      - Avoid renaming the timeline into something misleading.
      - Distinguish wizard flow vs integration vs high-level system docs.
  - `subfolder-organize`:
    - With fixed `project-id` and para-type, path proposals solidify around:
      - `3-Resources/Genesis-Mythos/1-Maps/...`
      - `3-Resources/Genesis-Mythos/2-Terrain3D/...`
      - `3-Resources/Genesis-Mythos/3-Lore/...`
      - `3-Resources/Genesis-Mythos/4-Combat-Equipment/...`
      - `3-Resources/Genesis-Mythos/5-Politics-Factions/...`
      - `3-Resources/Genesis-Mythos/6-World-Builder-Wizard/...`
    - It still has to *invent* the exact folder names, but the prompt gives the axis and ordering.
  - Distill-ish steps embedded in ingest:
    - `obsidian_distill_note` (or similar core distill step).
    - `distill-highlight-color` (using `Genesis-Mythos-Key`).
    - `highlight-perspective-layer` (ties to `geosynchronous-view`).
    - `next-action-extract` (usually finds few tasks; these are reference docs).
    - `split-link-preserve` only if anything is obviously massive and split-worthy (likely rare here).

### Confidence bands

- **Before loop (raw first pass)**
  - `ingest_conf` and especially `path_conf` are much higher than in minimal/basic runs because:
    - Para-type and project-id are fixed.
    - The prompt gives a clear, finite list of domains/phases.
  - **Typical ranges:**
    - Central docs (SYSTEM_IMPLEMENTATIONS, TERRAIN3D guide, world-builder wizard): **82–88%**.
    - Peripheral/ambiguous notes (README-style, grab-bag docs): **75–83%**.

- **After mid-band refinement loop**
  - For notes starting in **72–84%**, the loop uses the explicit phase vocabulary:
    - Re-checks headings vs the given list:
      - “Terrain3D integration” → 2-Terrain3D integration.
      - “World builder wizard” → 6-World-builder wizard.
    - Shifts paths accordingly (e.g. from a generic `Docs/` folder to its phase folder).
  - Post-loop:
    - Most “on-axis” docs climb into **≥85%**.
    - Only weird/very general files stay in mid-band.

**Result:**

- **Most Genesis-mythos docs are actually moved out of `Ingest/`** into a reasonably opinionated `3-Resources/Genesis-Mythos/<phase>/...` tree.
- `Genesis-Docs-Timeline.md`:
  - Treated as **central backbone**; strongly proposed (and likely moved) to:
    - `3-Resources/Genesis-Mythos/Genesis-Docs-Timeline-YYYY-MM-DD-HHMM.md`  
    - Or a small `Roadmap/` subfolder under `Genesis-Mythos`.
  - Confidence: **88–92%** after loop because the prompt explicitly calls it the chronological backbone.

**Proposal / preview callouts**

- **Fewer proposal callouts** than in minimal/basic runs:
  - Only for edge cases:
    - A too-generic `README.md`.
    - Any doc with mixed concerns that doesn’t clearly match the six domains.
- Callouts look like:
  - “Proposed path: `3-Resources/Genesis-Mythos/6-World-Builder-Wizard/world-builder-wizard-guide-....md` (path_conf: 87%). Set `approved: true` to accept.”

---

## 2) `HIGHLIGHT PERSPECTIVE` — `test-extensive-2`

**Prompt (key effects)**

- Names the **geosynchronous-view** lens in detail.
- Specifies:
  - Analogous colors for **related** systems (maps→terrain, lore→combat).
  - Complementary colors for **tensions** (performance vs visual fidelity).
  - Applying **`data-drift-level` 0–3**.

### Tools / skills that fire

- For each note in `3-Resources/Genesis-Mythos/` (including timeline):

  - `obsidian_read_note`
  - `distill-highlight-color`:
    - Uses `highlight_key: Genesis-Mythos-Key`.
    - Now has lens-specific guidance:
      - Stage 1: identify core concepts vs peripherals for this project.
      - Stage 2: map them to a consistent color palette with analogous/complementary rules from the prompt.
  - `highlight-perspective-layer`:
    - Sets:
      - `highlight_perspective: geosynchronous-view` (if not already).
      - `highlight_angles` / `data-drift-level`:
        - Core engine & map/terrain pipeline: **drift-level 0**.
        - Lore/combat/equipment/politics: **1–2**.
        - UI, non-critical details: **3**.
  - Optionally, `distill-perspective-refine` and `callout-tldr-wrap` if the distillation pipeline is configured to run here too.

### Confidence bands

- This is mainly a **distill/highlight** step, governed by `distill_conf`:

  - Before any internal loop:
    - `distill_conf` for highlight layout: **80–88%** (high, because the prompt gives explicit mapping rules).
  - After optional loop (if any mid-band):
    - Most notes reach **≥85–90%** confidence that:
      - The right concepts are highlighted.
      - Drift levels are internally consistent.

**Quality of highlighting**

- **Analogous usage:**
  - All “pipeline” concepts (2D maps → 3D terrain) share a base hue with small shifts in brightness or saturation.
  - Lore, combat, equipment are clustered in another analogous band.
- **Complementary usage:**
  - Tension callouts (e.g. “Performance vs visual fidelity” sections) show high-contrast colors.
- **Drift levels:**
  - Embedded via `data-drift-level` attributes:
    - 0 = core; 3 = far periphery.
  - Visually, this would show as:
    - Strong, saturated highlights for core pipeline steps.
    - Faded/gradient highlights for background lore or implementation details.

**Proposal / manual gates**

- Because this is non-destructive structurally (no moves), the system:
  - **Does not block** highlights behind approval.
  - May append a short note in one central place (e.g. timeline or a hub) saying:
    - “Geosynchronous-view highlighting applied with drift levels. Review if colors feel off.”

---

## 3) `BATCH-EXPRESS` — `test-extensive-3`

**Prompt (key effects)**

- “Consolidate ALL distilled mythos notes into ONE living roadmap note.”
- Must:
  - Use Genesis-Docs-Timeline as backbone.
  - Run `related-content-pull` across *every* phase.
  - Run `express-mini-outline` with project colors.
  - Do `version-snapshot` first.
  - Append a **call-to-action**.
  - Explicitly encode 2D→3D + lore/combat/politics layers with colors.

### Tools / skills that fire

- **Safety**
  - `obsidian_create_backup` already done earlier; here:
    - `version-snapshot` on the target roadmap note path (once it is decided).

- **Content pull & express**
  - `obsidian_read_note` on:
    - `Genesis-Docs-Timeline`.
    - All other `3-Resources/Genesis-Mythos/*` docs.
  - `related-content-pull`:
    - For each major timeline segment/phase, pulls a list of related notes (by semantics + `project-id: genesis-mythos`).
    - Builds a graph of:
      - Maps/terrain docs.
      - Lore systems.
      - Combat/equipment.
      - Politics/factions.
      - Wizard/rendering docs.
  - `express-mini-outline`:
    - Generates a **roadmap outline** in a new or existing note:
      - Likely `3-Resources/Genesis-Mythos/Genesis-Mythos-Roadmap.md`.
    - Uses project colors (from `Genesis-Mythos-Key`) to color section headers or callouts.
  - `express-view-layer`:
    - Annotates any `Related` sections with connection strength and project colors.

- **Polish**
  - `call-to-action-append`:
    - Appends a CTA like:
      - “Next steps: implement Terrain3D integration MVP; then wire basic combat loop with placeholder stats.”
  - `readability-flag`:
    - If the roadmap wall-of-text is too dense, it may mark `needs-simplify: true` and add a friendly callout.

### Confidence bands

- `express_conf` is the main signal:

  - Before refinement:
    - With a strong backbone (timeline) and uniform project-id:
      - Most phases land ~**82–89%**.
  - After one loop (if needed for some phases):
    - The overall express_conf for the roadmap note hits **≥88–92%**.
    - Any low-confidence micro-structure is confined to subtask ordering, not entire sections.

**Structure and richness of the roadmap note**

Roughly:

- **Frontmatter**
  - `project-id: genesis-mythos`
  - `para-type: resource` (but functionally a roadmap hub)
  - `highlight_perspective: geosynchronous-view`
  - `highlight_key: Genesis-Mythos-Key`

- **Top-level**
  - `# Genesis-Mythos — Geosynchronous Roadmap`
  - TL;DR in a summary callout:
    - “2D Azgaar modular maps → Terrain3D open world; layered lore/combat/equipment/politics systems; wizard-driven authoring pipeline.”

- **Phases (1–6) as headings**

  - **1. Maps (Azgaar modular)**
    - Short description: role of 2D modular maps.
    - Bullet list of key tasks/outcomes.
    - Links to source docs (Azgaar map guide, examples).

  - **2. Terrain3D Integration**
    - Steps for ingesting 2D maps → Terrain3D heightmaps/meshes.
    - Performance vs visual fidelity callout (with complementary colors).
    - Links to `TERRAIN3D_INTEGRATION_GUIDE` and relevant SYSTEM_IMPLEMENTATIONS sections.

  - **3. Lore Support Systems**
  - **4. Combat & Equipment**
  - **5. Politics & Factions**
  - **6. World-Builder Wizard & Rendering**
    - Similar pattern: per-phase overview, key bullet tasks, and **auto-linked references**.

- **Related section**
  - “Related Notes by Phase”
  - For each phase:
    - A small table/list of links with connection strength indicators (from `express-view-layer`).

- **CTA**
  - A callout at the end:
    - “Implement Phase 1–2 MVP first; then layer minimal lore + a basic combat loop. Re-run EXPRESS MODE after each milestone.”

**Proposals / approvals**

- Because this is a new roadmap note created and enriched (plus version-snapshot for future edits):

  - The *creation* itself is high-confidence (it doesn’t overwrite others).
  - No destructive move, so no approval gate for creation.
  - There may be a **proposal-like callout** inside the roadmap note:
    - “Treat this as canonical Genesis-Mythos roadmap? Set `status: active` in frontmatter if approved.”

---

## 4) `roadmap-ingest` — `test-extensive-4`

**Prompt (key effects)**

- Provides explicit phase list:
  - 1–6 phases (maps, terrain, lore, combat/equipment, politics, wizard/rendering).
- Asks for:
  - Standardized phases/subphases/tasks checklist.
  - Auto-links back to source notes.
  - Preservation of `highlight_perspective` and `highlight_angles` in frontmatter.

### Tools / skills that fire

- `obsidian_read_note` on:
  - `Genesis-Docs-Timeline.md`
  - Already-distilled docs in `3-Resources/Genesis-Mythos/` (as needed).
- `roadmap-ingest` skill:
  - Parses:
    - Headings and chronology from the timeline.
    - Cross-links / references to phases.
  - Normalizes into:
    - **Phases** → **Subphases** → **Tasks** tree.
- Possibly `roadmap-checklist` if wired:
  - To write the hierarchical checklist back into either:
    - The same `Genesis-Docs-Timeline.md`, or
    - The dedicated `Genesis-Mythos-Roadmap.md` created in the previous step.
- Frontmatter tweaks:
  - Ensure `highlight_perspective`, `highlight_angles`, `project-id`, etc., remain consistent.

### Confidence bands

- Primary signal for this step is a variant of `express_conf` / `distill_conf` / roadmap-specific confidence:

  - Before loop:
    - With explicit phase names in the prompt, **phase-boundaries** are high-confidence (**85–90%**).
    - Subphases/tasks extracted from prose are mid-high (**78–86%**).
  - After loop:
    - Overall roadmap checklist structure: **≥90%**.
    - Some **individual task granularity** may remain mid-band (ordering or grouping is somewhat subjective).

**Resulting checklist structure**

Likely written as a section like:

- `## Genesis-Mythos — Implementation Checklist`
- Then:

- **Phase 1 — Maps (Azgaar modular)**  
  - Subphase: Map generation pipeline
    - [ ] Choose map templates and biome presets
    - [ ] Define modular region schema
  - Subphase: Export to engine
    - [ ] Define Azgaar → engine format
    - [ ] Validate off-grid regions

- **Phase 2 — Terrain3D Integration**
  - Subphase: Heightmap generation
    - [ ] Derive heightmaps from 2D maps
    - [ ] Validate seams between tiles
  - Subphase: Performance tuning
    - [ ] Baseline performance with default materials
    - [ ] Optimize LOD & streaming

- **… through Phase 6 — Wizard & Rendering**

Each checklist item carries:

- A link or reference like:
  - “Source: [[3-Resources/Genesis-Mythos/TERRAIN3D_INTEGRATION_GUIDE-...]]”
- Optionally a block reference if extracted from a specific section.

**Proposals / manual gates**

- Because roadmap-ingest:
  - Writes *within* timeline/roadmap notes but doesn’t move/rename them.
  - Might:
    - Prepend a short callout:
      - “Roadmap checklist auto-generated. Edit freely; set `approved: true` to mark as canonical.”

---

## 5) Comparison vs minimal and basic runs

### Confidence

- **Minimal run:**
  - Most notes in **mid-band**.
  - A few in high; many proposals; lots left in `Ingest/`.
- **Basic run:**
  - Slight bump; some phases inferred from the short lens phrase.
  - Mid-band still dominant for path decisions.
- **Extensive run:**
  - Explicit project-id, para-type, highlight_key, and phase vocabulary:
    - Push **most core docs and all phase assignments into ≥85%** after loops.
    - Only truly ambiguous odds-and-ends linger in mid-band.

### Highlighting quality

- **Minimal:**
  - Generic highlight coverage; colors may feel arbitrary; no clear sense of drift.
- **Basic:**
  - Some alignment to maps→terrain and lore/combat, but still shallow and inconsistent.
- **Extensive:**
  - Clear, repeatable **color grammar**:
    - Analogous for pipelines and related subsystems.
    - Complementary for trade-offs/tensions.
    - `data-drift-level` giving a meaningful core→periphery gradient.

### Roadmap richness

- **Minimal:**
  - Thin outline, little cross-linking, lots of “proposal” noise.
- **Basic:**
  - Better phases, some cross-links, but:
    - Related-content coverage spotty.
    - Checklist shallow and non-standard across phases.
- **Extensive:**
  - Single, **cohesive living roadmap**:
    - Phases 1–6 explicitly structured.
    - Subphases and tasks extracted and normalized.
    - Cross-links to all relevant docs.
    - CTA for next steps.
    - Color-coded flow consistent with the lens.

### Reusable pattern for future ingests

- **Minimal/basic:**
  - Future ingests don’t have a strong pattern to copy; you mostly created **ad-hoc buckets**.
- **Extensive:**
  - You now have:
    - A **canonical project-id** (`genesis-mythos`).
    - A well-defined **3-Resources/Genesis-Mythos/** subtree with phases.
    - A **roadmap hub note** that defines:
      - Phase names
      - Color usage
      - Checklist style
    - Future ingests can:
      - Reuse `highlight_key`, `project-id`, and phase folders.
      - Slot new docs into the existing roadmap with higher default confidence.

**Is the extra guidance worth it?**

- For a **foundational corpus like Genesis-Mythos**, yes:
  - It materially improves confidence and structure.
  - It produces a reusable pattern instead of a one-off mess.
- The trade-off:
  - You still need to manually tweak some task granularity and path naming.
  - But the amount of cleanup is much smaller than in minimal/basic runs, and later ingests benefit disproportionately from this first, well-guided pass.

## Review Needed
Proposed para-type: project. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.