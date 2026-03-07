---
title: Second Brain Automation Recommendations
created: 2026-02-26
tags: [pkm, second-brain, cursor, persona, pipelines, file-types]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[Cursor-Skill-Pipelines-Reference]]", "[[Second-Brain-Config]]"]
---

# Second Brain Automation Recommendations

Recommendations to **finalize** (1) the persona Cursor operates under, (2) the standard pipeline prompts, and (3) how Cursor handles non-markdown file types. Apply these in rules, config, and templates as you implement.

---

## 1. Persona: What Cursor Operates As

**Current state:** Identity is implied in several places — "autonomous Zettelkasten ingest agent" (Templates/AI Prompts), "expert auditor" (audit prompt), PARA + Zettel in para-zettel-autopilot — but there is no single, canonical persona that every pipeline and prompt inherits.

**Recommendation: Define one canonical persona and reference it everywhere.**

### 1.1 Create a persona rule/note

- **Location:** Either:
  - **Option A:** `.cursor/rules/always/second-brain-persona.mdc` (always-applied, short: 1–2 paragraphs).
  - **Option B:** `3-Resources/Second-Brain-Persona.md` (full note) + one always-applied rule that says: "When processing this vault, adopt the identity and principles in [[Second-Brain-Persona]]; read that note at session start or when user says INGEST/DISTILL/ARCHIVE/EXPRESS/ORGANIZE."

- **Content to encode:**

| Element | Recommendation |
|--------|-----------------|
| **Name/role** | e.g. "Second Brain Autopilot" or "PARA-Zettel Conductor" — one short title used in logs and prompts. |
| **Mission** | Capture is the only manual step; everything after (organize, distill, hub, archive, express) runs via Cursor + MCP when the user triggers a pipeline. |
| **Principles** | Backup-first (Option C); ≥85% auto-execute, &lt;85% propose + #review-needed; no shell vault ops (cp/mv/rm); per-note isolation in batches; log every action with backup path. |
| **Scope** | This vault only; PARA + Zettelkasten; MCP from global config; skills/rules from `.cursor/`. |
| **Tone** | Concise, deterministic, no confirmation loops; state confidence and actions taken; use canonical log format. |

- **Where to reference:** In always-ingest-bootstrap, para-zettel-autopilot description, and in each context rule (auto-distill, auto-archive, auto-express, auto-organize): add one line such as "Operate under the persona in [[Second-Brain-Persona]] (or second-brain-persona rule)."

### 1.2 Single source of truth

- Keep **one** place that defines the persona (the .mdc rule or the linked note). Pipelines and prompts then "inherit" by reference instead of redefining the agent in each template.

---

## 2. Standard Pipeline Prompts

**Current state:** Ingest has a canonical block in `3-Resources/2026-02-24-cursor-ingest-prompt-reference.md` and a shorter version in `Templates/AI Prompts.md`. Distill, Archive, Express, and Organize have **trigger phrases** in context rules but no single "paste this to run X" prompt block.

**Recommendation: One canonical launch prompt per pipeline, in one place.**

### 2.1 Where to store them

- **Primary:** `Templates/AI Prompts.md` (or a dedicated `Templates/Pipeline-Prompts.md`).
- **Alternative:** A section in `3-Resources/Cursor-Skill-Pipelines-Reference.md` titled "Canonical launch prompts" with copy-paste blocks.
- Keep the **trigger phrase** and the **full prompt** aligned: the trigger activates the rule; the full prompt is what the user (or a macro) can paste for a full run.

### 2.2 Standard prompts to define

| Pipeline | Canonical trigger (already in rules) | What to add |
|----------|--------------------------------------|-------------|
| **Ingest** | "INGEST MODE – safe batch autopilot" | Already have canonical block in prompt reference; ensure Templates/AI Prompts.md matches it and points to persona + pipeline order. |
| **Distill** | "DISTILL MODE – safe batch autopilot" | Add a **DISTILL** block: persona ref, backup-first, pipeline order (backup → optional auto-layer-select → distill layers → distill-highlight-color → layer-promote → callout-tldr-wrap → readability-flag → log). Confidence ≥85% for destructive steps; batch size ~5; log to Distill-Log.md and Backup-Log.md. |
| **Archive** | "ARCHIVE MODE – safe batch autopilot" | Add an **ARCHIVE** block: persona ref, backup-first, pipeline (backup → classify_para → archive-check → subfolder-organize → resurface-candidate-mark → summary-preserve → move_note → log). Scope: 1-Projects, 2-Areas, 3-Resources only; exclusions (Backups, Logs, Hubs). Log to Archive-Log.md and Backup-Log.md. |
| **Express** | "EXPRESS MODE – safe batch autopilot" | Add an **EXPRESS** block: persona ref, version-snapshot before major appends, pipeline (backup → version-snapshot → related-content-pull → express-mini-outline → call-to-action-append → log). Single-note or very small batch; log to Express-Log.md and Backup-Log.md. |
| **Organize** | "ORGANIZE MODE – safe batch autopilot [on folder]" | Add an **ORGANIZE** block: persona ref, backup-first, pipeline (backup → classify_para → frontmatter-enrich → subfolder-organize → optional rename → move_note → log). Scope folder explicitly if provided; log to Organize-Log.md and Backup-Log.md. |

### 2.3 Prompt block structure (template)

For each pipeline, use a consistent structure so the model and the user know what to expect:

1. **Launch phrase** (one line).
2. **Identity:** "Operate as [persona]. Follow [rule/skill reference]."
3. **Core rules:** Backup first; confidence threshold; no confirmation loops; per-note isolation.
4. **Scope/filter:** Which notes (path, status, or "current note").
5. **Exact tool/skill sequence** (numbered list matching Cursor-Skill-Pipelines-Reference).
6. **Log format** and where to append (which Log.md, Backup-Log.md).
7. **Batch summary** (if batch): Processed N | Auto-executed X | Flagged Z | Failed W.

### 2.4 Sync with rules

- When you add or change a pipeline in Cursor-Skill-Pipelines-Reference or in a context rule, update the corresponding prompt block so the paste-able prompt and the rule stay in sync.

---

## 3. Non-Markdown File Types

**Current state (updated):** Non-MD files (including images embedded in ingested .md notes) now receive full proactive handling. When the user says "Process Ingest" / "INGEST MODE" or when working in Ingest/, the agent follows **ingest-processing** and **non-markdown-handling**:

- **Direct non-.md** → companion .md + #needs-manual-move; user moves original to **5-Attachments/[subtype]/** (PDFs/, Images/, Audio/, Documents/, Other/) manually.
- **Images embedded inside .md** → automatic link normalization to 5-Attachments/Images/ + #needs-attachment-relocation callout; image files remain in place until user drags them (MCP-safe).

MCP does not move binaries (obsidian_move_note only supports .md); shell mv/cp/rm is not used. Full-autonomous-ingest then runs on all Ingest/*.md (including the new companions).

### 3.1 Policy (implemented)

| Approach | Use case | Status |
|---------|----------|--------|
| **Proactive companion** | Non-.md in Ingest/ | Agent creates companion .md per non-markdown-handling; original stays in Ingest/ with #needs-manual-move; user moves to 5-Attachments/[subtype]/; pipeline runs on .md only. |
| **Sidecar .md** | PDF/image/URL that should become a note | Same as above: companion .md with frontmatter and embed/link to target path 5-Attachments/...; asset moved by user. |
| **Convert then ingest** | One-off "Turn this PDF into a note" | Still valid: user can request one-off conversion; standard batch uses proactive companion flow. |

### 3.2 Rules and references

- **ingest-processing.mdc** (context, globs: Ingest/**): lists Ingest (md + non-md), creates companions for non-.md, then runs full-autonomous-ingest on .md.
- **non-markdown-handling.mdc** (context, Ingest/**): file-type matrix, frontmatter template, 5-Attachments/[subtype] paths, MCP SAFETY (no move_note on binaries, no shell ops).
- **mcp-obsidian-integration.mdc**: states non-markdown handling and #needs-manual-move; 5-Attachments/[subtype]/.

### 3.3 Edge cases

- **Untitled or extension-less files in Ingest/:** If the vault or MCP lists them, skip them unless they are treatable as markdown (e.g. no extension but content is markdown — then optional: propose rename to `.md` and process, with #review-needed if unsure).
- **Attachments (images, PDFs) linked from .md:** No change: the note is .md; links to assets are preserved. Pipeline does not "process" the binary; it only processes the note content and frontmatter.
- **Future: OCR or "import PDF" as note:** Document as a separate, optional flow (e.g. "Run only when user asks 'Turn this PDF into an Ingest note'") and keep it outside the default INGEST MODE batch.

---

## 4. Implementation Checklist

- [ ] **Persona:** Create `.cursor/rules/always/second-brain-persona.mdc` (or `3-Resources/Second-Brain-Persona.md` + rule reference). Add one-line reference in always-ingest-bootstrap, para-zettel-autopilot, auto-distill, auto-archive, auto-express, auto-organize.
- [ ] **Pipeline prompts:** Add DISTILL, ARCHIVE, EXPRESS, ORGANIZE blocks to `Templates/AI Prompts.md` (or Pipeline-Prompts.md) using the structure in §2.3. Align with Cursor-Skill-Pipelines-Reference.
- [ ] **Non-markdown:** Add "File scope: .md only; skip non-markdown" to mcp-obsidian-integration or Second-Brain-Config; add `file_scope` / `allowed_extensions` to Second-Brain-Config if desired. In ingest prompt and para-zettel-autopilot, keep or add "Skip non-markdown; process only .md files."
- [ ] **Sync:** After changes, update Cursor-Project-Rules-Summary.md and Cursor-Skill-Pipelines-Reference.md so the docs reflect persona ref, prompt locations, and file-scope policy.

---

*This note is the single recommendations reference for persona, pipeline prompts, and non-markdown handling. Link it from the pipeline reference and from the rules that invoke the pipelines.*
