  
Here’s a concise summary of how to phrase prompts so they work with your automations:

---

## Summary: Rules for Crafting Prompts for Automations

### 1. **Use the right trigger phrases**

Triggers are **case-insensitive** and often work with **partial match**. Use one of these to start a pipeline:

| Goal | Trigger phrases | Pipeline |
|------|------------------|----------|
| **Ingest** | **"INGEST MODE"**, **"Process Ingest"**, **"run ingests"** | full-autonomous-ingest |
| **Distill** | **"DISTILL MODE – safe batch autopilot"**, "distill this note", "refine this note" | autonomous-distill |
| **Archive** | **"ARCHIVE MODE – safe batch autopilot"**, "archive this note", "send to Archives" | autonomous-archive |
| **Express** | **"EXPRESS MODE – safe batch autopilot"**, "express this note", "generate outline" | autonomous-express |
| **Organize** | **"ORGANIZE MODE – safe batch autopilot [on folder]"**, "re-organize", "classify and move" | autonomous-organize |
| **Resurface** | "Resurface", "show resurface candidates" | — |

Canonical mode triggers (e.g. **"INGEST MODE – safe batch autopilot"**) are the most reliable; the full blocks live in `Templates/AI Prompts.md` and in the pipelines reference.

---

### 2. **Prompt → MCP action (ad‑hoc vault actions)**

For one-off actions (no full pipeline), phrase your intent so the agent maps it to MCP tools:

- **Read note** → `obsidian_read_note`
- **Move** → classify first, then propose path (or run organize pipeline)
- **Search** → `obsidian_global_search`
- **List folder** → `obsidian_list_notes`
- **Update/append** → `obsidian_update_note` / `obsidian_search_replace`
- **Frontmatter/tags** → `obsidian_manage_frontmatter` / `obsidian_manage_tags`

So prompts like “read this note”, “search for X”, “list notes in Ingest”, “update the tags on this note” will route to the right tools.

---

### 3. **What a full pipeline prompt should include**

If you write or paste a **full** launch prompt (e.g. in `Templates/AI Prompts.md` or a macro), it should follow this structure:

1. **Launch phrase** — One clear line (e.g. "INGEST MODE – safe batch autopilot").
2. **Identity** — Operate as [persona]; follow [rule/skill reference].
3. **Core rules** — Backup first; confidence ≥85% for auto-execute; no confirmation loops; per-note isolation.
4. **Scope/filter** — Which notes (e.g. directory `"Ingest"`, current note, or a folder path for Organize).
5. **Exact tool/skill sequence** — Numbered list matching `Cursor-Skill-Pipelines-Reference.md`.
6. **Log format** — Where to append (e.g. Ingest-Log.md, Backup-Log.md) and what to include (e.g. backup path in `changes`).
7. **Batch summary** (if batch) — Processed N | Auto-executed X | Flagged Z | Failed W.

Keeping this structure (and the trigger phrase) aligned with the rules and pipelines reference keeps behavior consistent.

---

### 4. **Scope and context**

- **Ingest**: Uses `obsidian_list_notes` with `directory: "Ingest"`; typically all `.md` in Ingest/ (or state if you filter by tag/status).
- **Distill / Archive / Express**: Apply to notes under `1-Projects/**`, `2-Areas/**`, `3-Resources/**`; they exclude `4-Archives/**`, `Backups/**`, `Templates/**`, and `*Hub.md` / Log files.
- **Organize**: Can be scoped to a folder, e.g. **"ORGANIZE MODE – safe batch autopilot on 1-Projects/Test-Project"**.
- **Express**: Usually single-note or very small batch.

Being explicit about scope in the prompt (“on 3-Resources”, “current note”, “all of Ingest”) avoids wrong pipeline or wrong set of notes.

---

### 5. **Safety and behavior (don’t contradict in prompts)**

- **No “wait for ok”** — At ≥85% confidence the agent auto-executes; at &lt;85% it proposes and flags `#review-needed` only. Prompts should not ask for step-by-step confirmation.
- **Backup first** — Every pipeline starts with `obsidian_create_backup`; prompts should not tell the agent to skip backup.
- **No shell vault ops** — Never ask for `cp`/`mv`/`rm` on the vault; all moves/edits go through MCP and skills.

---

### 6. **Where to look for canonical prompts**

- **Trigger ↔ pipeline mapping**: `3-Resources/Cursor-Skill-Pipelines-Reference.md` (trigger table and pipeline flows).
- **Ingest**: `Templates/AI Prompts.md` (and `3-Resources/2026-02-24-cursor-ingest-prompt-reference.md`).
- **Prompt design template**: `3-Resources/Second-Brain-Automation-Recommendations.md` (§2.3 Prompt block structure).

In short: use the **trigger phrases** for the pipeline you want; for ad‑hoc vault actions use **plain intent** (read, search, list, update, move); and for **full launch prompts** use the **seven-part structure** and keep triggers and scope aligned with the pipelines reference.




# A few things for our second brain automations.

We need to finalize the persona Cursor will operate under, we will need to finalize the standard pipeline prompts, and define how Cursor will handle none markdown file types.

Help me craft the rough draft.

Use this to help craft the persona as what the automatons help me do is capture my insights discern where they are connected and assist in mapping how to apply them.