# Second Brain — Limitations

Explicit, accepted limitations of the current Second Brain setup and pipelines.

---

## Manual-only steps (accepted)

**Decision: consciously accept as manual-only.**

- **Mobile capture** (Readwise, phone notes, web clips, highlights) and **direct highlight ingest** remain manual steps.
- The planned **Connection Ingest** plugin is not currently implemented.
- This is the **primary remaining manual step** outside of deliberate user review (`#review-needed` items).

Automated ingest (e.g. para-zettel-autopilot) applies to content once it is in the vault; bringing content in from mobile, Readwise, or highlight sources is out of scope until/unless Connection Ingest or equivalent is implemented.

---

## Deep-nested PARA move behavior (verified 2026-02-25)

- **Test path:** 4-level path used for verification: `4-Archives/Test-Project-Archive/Subtheme/2026-02-25-archive-test.md`.
- **Folders created reliably:** Yes, when using **obsidian_ensure_structure** with the optional **folder_path** parameter set to the target parent (e.g. `4-Archives/Test-Project-Archive/Subtheme`). The MCP server creates that path recursively with `os.makedirs(..., exist_ok=True)`. **obsidian_move_note** alone does not create parent directories (Obsidian Local REST API calls `createFolder` once; Obsidian API does not create parent folders recursively).
- **Conflict / already-exists handling:**
  - **Already-exists folders:** Silently skipped (idempotent). Safe to call ensure_structure multiple times.
  - **Target note already exists at new_path:** Move overwrites (PUT then delete). Backup and per-change snapshot before move are the safety net; no separate “target exists” check.
- **Limitations still present:** Paths are used as-is (no case or character normalization). Invalid filesystem characters can cause errors.

**Checklist (deep-nested move):** [x] Verify deep-nested PARA move behavior (3–4 levels); ensure_structure + move_note documented; conflict/already-exists handling documented.

---

## Split linking (2026-02-25)

After `obsidian_split_atomic`, the **split-link-preserve** skill (full-autonomous-ingest, immediately after split) adds minimal traceability:

- **New atomic notes**: YAML `split_from: "[[Original Note Title]]"`; if the note already has `related` frontmatter, the original link is appended to that array (no overwrite).
- **Original note**: A **## Splits** section is appended (or updated if it exists) with "Splits / Extracted" and a bullet list: `- [[New Atomic Note Title]] — brief one-line reason` (e.g. first sentence or heading of the split content).
- **Navigation**: Obsidian backlinks pane is used for reverse navigation; no separate backlink note.
- **Safety**: Edits are idempotent (no duplicate bullets or duplicate `related` entries); snapshot before edit follows pipeline policy.

Enables Dataview queries such as `LIST FROM "" WHERE split_from` and backlink-based "note X split into Y, Z".
