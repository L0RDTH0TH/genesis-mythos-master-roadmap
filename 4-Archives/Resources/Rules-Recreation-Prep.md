---
title: Rules Recreation — Phase 1 Prep
created: 2026-02-25
tags: [cursor, rules, second-brain, recreation]
para-type: Resource
status: active
links: [[Cursor-Project-Rules-Summary]], [[Resources Hub]]
---

# Rules Recreation — Phase 1 Prep

Checklist and scope for Rule Recreation Road Map Phase 1. Use this when setting up the test vault and validating baseline context.

---

## 1. Test Vault Clone

- **Goal**: Clone current vault to a safe path (e.g. `~/Documents/Second-Brain-Rules-Recreation`) for testing recreated rules.
- **Include in clone**:
  - Full vault structure: `Ingest/`, `1-Projects/`, `2-Areas/`, `3-Resources/`, `4-Archives/`, hubs, `Templates/`.
  - **`.cursor/skills/`** — Copy the 14 skills from the main vault so Phase 2 can test skill invocation in a sample pipeline. If the main vault already has `.cursor/skills/` with all 14 skill directories, ensure the clone gets a full copy.
- **Exclude**: Personal data if desired (e.g. sensitive notes); document exclusions in Rules-Recreation-Log.md.
- **Output**: Clean test vault with PARA folders, hubs, and `.cursor/skills/` (14 skills present).

---

## 2. Backup Scope (before any recreation work)

Run **obsidian_create_backup** (or equivalent) on the following before changing rules or structure:

| Item | Path / scope |
|------|----------------|
| Current `.cursor/` | Entire `.cursor/` directory (rules, skills, plans) if it exists |
| Rules summary | `3-Resources/Cursor-Project-Rules-Summary.md` |
| Second Brain summary | `3-Resources/Second Brain Summary.md` |
| Highlightr key | `3-Resources/Highlightr-Color-Key.md` |
| Skills | Each `.cursor/skills/<name>/SKILL.md` (e.g. distill-highlight-color, subfolder-organize, …) |

**Improvement**: Add an "always-backup-first" rule snippet in recreated rules so this scope is enforced globally for destructive or rule-changing work.

**Output**: Backup paths logged in `Rules-Recreation-Log.md`.

---

## 3. Validate Context (gap table)

- Cross-reference **Cursor-Project-Rules-Summary.md** with skills in `.cursor/skills/` and (if provided) any pasted-text or recovered rule snippets.
- **Pasted-text**: Optional. If `pasted-text.txt` (or similar) is not provided, leave "Pasted-Text Addition" column as N/A in the gap table; validation still runs on Summary vs. Skills vs. Gaps.
- **Output**: Fill **Rules-Recreation-Gap-Table.md** with columns: Rule Section | Summary Coverage | Skills Integration | Gaps.

---

## 4. Confidence threshold (project standard)

- **Use 85% everywhere** for auto-execute vs. propose. Summary, ingest prompt, and all recreated rules must use **≥85%** for auto-actions and **<85%** for propose-only / #review-needed.
- Do not introduce 90% in rules or prompts unless the summary and ingest prompt are updated together; keep a single threshold to avoid mixed behavior in the same pipeline.

---

*When Phase 1 is complete: test vault exists, backup log updated, gap table filled. Proceed to Phase 2 (core always-applied rules).*

---

## 5. Phase 2 exit checkpoint (validation before Phase 3)

Before moving to Phase 3 (context-specific rules), run a **sample pipeline test** in the test vault:

1. **Run one sample ingest**: Process one note in `Ingest/` using the full ingest pipeline (create_backup → classify_para → … → log_action).
2. **Confirm skills invocation**: Verify that at least **two skills** from the pipeline are invoked and logged (e.g. **frontmatter-enrich**, **next-action-extract**). Check that the agent follows the rule and skill sequence (e.g. from [[3-Resources/Cursor-Skill-Pipelines-Reference]]).
3. **Log result**: In Rules-Recreation-Log.md, note: "Phase 2 exit: sample pipeline run on [date]; skills invoked: [list]; pass/fail."

This ensures rules and skills are wired correctly before adding context-specific rules in Phase 3.
