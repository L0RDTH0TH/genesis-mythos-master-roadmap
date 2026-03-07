# Ingest run trace — Batch 4 (2026-03-03)

Step-by-step trace of the run that processed 5 notes and applied the **decision-candidate (user loop)** steps. Use this to verify where each result lives in the vault.

---

## 1. Backup

| Step | Tool | Input | Result |
|------|------|--------|--------|
| 1.1 | `obsidian_create_backup` | paths: DM Free Camera, DND subclasses, Dm, Eberron Rising..., Feature request template | success; backups under `/home/darth/Documents/Second-Brain-oops-Backups/` timestamp **20260303-045649** |

**Where to verify:** External backup folder (Second-Brain-oops-Backups). Files like `20260303-045649-DM Free Camera.md` etc.

---

## 2. Classify (primary confidence)

| Note | Tool | Result |
|------|------|--------|
| DM Free Camera | `obsidian_classify_para` | Area, 70% |
| DND subclasses | `obsidian_classify_para` | Archive, 70% |
| Dm | `obsidian_classify_para` | Archive, 70% |
| Eberron Rising from the Last War (ERftLW) | `obsidian_classify_para` | Archive, 70% |
| Feature request template | `obsidian_classify_para` | Resource, 70% |

70% → **mid-band (68–84%)** → refinement loop ran.

---

## 3. Mid-band loop (path candidates)

| Note | Tool | selected_path | post_loop_conf |
|------|------|----------------|----------------|
| DM Free Camera | `obsidian_subfolder_organize` | 2-Areas/DM Free Camera.md | 75% |
| DND subclasses | `obsidian_subfolder_organize` | 4-Archives/Genesis/DND subclasses.md | 75% |
| Dm | `obsidian_subfolder_organize` | 4-Archives/Genesis/Dm.md | 75% |
| Eberron Rising... | `obsidian_subfolder_organize` | 4-Archives/Genesis/Eberron Rising from the Last War (ERftLW).md | 75% |
| Feature request template | `obsidian_subfolder_organize` | 3-Resources/Feature request template.md | 75% |

75% < 85% → **no move**; decision-candidate steps applied instead.

---

## 4. Frontmatter (per note)

For each note the agent called `obsidian_manage_frontmatter` for: `para-type`, `confidence`, `created`, `status`, `decision_candidate`, `guidance_conf_boost`, `decision_priority`.

**Where to verify:** Open each note in Obsidian (or raw .md); look at the **YAML block at the top** (between `---`).

| Note | Path in vault | Expected frontmatter (decision-related) |
|------|----------------|------------------------------------------|
| DM Free Camera | `Ingest/DM Free Camera.md` | `decision_candidate: true`, `guidance_conf_boost: 15`, `decision_priority: medium` |
| DND subclasses | `Ingest/DND subclasses.md` | same |
| Dm | `Ingest/Dm.md` | same |
| Eberron Rising from the Last War (ERftLW) | `Ingest/Eberron Rising from the Last War (ERftLW).md` | same |
| Feature request template | `Ingest/Feature request template.md` | same |

---

## 5. Tag #guidance-aware

| Step | Tool | Input | Result |
|------|------|--------|--------|
| 5.1–5.5 | `obsidian_manage_tags` | add_tags: "guidance-aware" for each of the 5 notes | Tags updated |

**Where to verify:** In each note, frontmatter should contain `tags: guidance-aware` (or Obsidian may show it as `#guidance-aware` in the tag pane / all tags).

---

## 6. Callout (Decision needed + Suggested user_guidance)

For each note the agent called `obsidian_search_replace` to insert a block **immediately after the closing `---`** of the frontmatter:

- `> [!warning] Decision needed (low confidence)`  
- `> This note needs guidance. Add user_guidance and approved: true...`  
- `> [!tip] Suggested user_guidance (copy-paste into frontmatter)`  
- `> user_guidance: |`  
- `>   Classify as [type]. Prefer path: [proposed path]. Split if >500 words...`

**Where to verify:** Open each note in **reading/preview mode** or **edit mode**. The first content after the frontmatter should be the **warning callout** (yellow/orange “Decision needed”) and below it the **tip callout** (suggested user_guidance). In **edit mode** you see the raw `> [!warning]` and `> [!tip]` blocks.

| Note | Location in file |
|------|-------------------|
| DM Free Camera | Lines 11–16 (after `---`) |
| DND subclasses | Lines 12–17 |
| Dm | Lines 12–17 |
| Eberron Rising... | Lines 12–17 |
| Feature request template | Lines 16–21 |

---

## 7. Log entries

| Step | Tool | Where |
|------|------|--------|
| 7.1–7.5 | `obsidian_log_action` | Each note → one line appended to `3-Resources/Ingest-Log.md` |
| 7.6 | Text append | Run summary appended to same file |

**Where to verify:** Open **`3-Resources/Ingest-Log.md`**, scroll to the bottom. You should see:

- Five log lines with timestamp `2026-03-03 04:58:3x`, mentioning **decision_candidate**, **#guidance-aware**, **callout**, **low_conf_trigger: mid-band-failure**, and backup **20260303-045649**.
- A run summary paragraph for batch 4 listing the 5 notes and “Decision-candidate steps applied”.

---

## 8. Quick checklist (where to look)

| Result | Where to look |
|--------|----------------|
| Backups | `Second-Brain-oops-Backups` (outside vault), files `20260303-045649-*.md` |
| Frontmatter (decision_candidate, etc.) | Top of each note in `Ingest/`: DM Free Camera, DND subclasses, Dm, Eberron Rising..., Feature request template |
| Tag #guidance-aware | Same notes: frontmatter `tags: guidance-aware` or tag pane in Obsidian |
| Decision callout | Same notes: first block after frontmatter (warning + tip) |
| Log + low_conf_trigger | `3-Resources/Ingest-Log.md` (last 5 data lines + batch 4 summary) |

---

## 9. Note on “results not obviously present”

- **Callouts:** Visible in **preview/reading view** as colored callout boxes. In **edit view** they are the lines starting with `> [!warning]` and `> [!tip]`.
- **Tags:** In Obsidian, check the **tag pane** (e.g. #guidance-aware) or the **frontmatter** line `tags: guidance-aware`.
- **Frontmatter:** Easiest in **edit mode** (first ~15 lines). In preview, some themes only show title; open in edit to see full YAML.
- **Log:** `Ingest-Log.md` is a long file; search for **“mid-band-failure”** or **“045649”** or **“batch 4”** to jump to this run.

If you were looking at **other Ingest notes** (e.g. from an earlier batch like AI Integration, Cascade Implementation), those were processed **before** the decision-candidate rule was enforced; they have proposed paths in the log but do **not** have the callout or decision_candidate frontmatter unless we backfill them.

---

## 10. Gap found and fixed

**DM Free Camera** was missing `guidance_conf_boost: 15` and `decision_priority: medium` in frontmatter (likely lost when the callout was inserted). Those two keys were re-applied after this trace so all 5 notes are consistent.
