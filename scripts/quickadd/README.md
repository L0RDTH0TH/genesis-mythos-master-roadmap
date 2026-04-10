# QuickAdd pipeline triggers

These scripts are used by QuickAdd **Macro** choices to log pipeline triggers so Cursor/MCP can run the autonomous ingest, distill, and express pipelines.

## Choices (in `.obsidian/plugins/quickadd/data.json`)

| Choice name   | Script              | Log file              | Trigger line / behavior |
|---------------|---------------------|-----------------------|--------------------------|
| **Ingest Batch** | `ingest-batch.js`   | `Ingest-Log.md`       | Appends `INGEST MODE – safe batch autopilot` + timestamp. |
| **Run Ingest**   | `run-ingest.js`     | `Ingest-Log.md`       | Appends `INGEST MODE – execute now` + timestamp. Fallback: open Cursor manually. |
| **Distill**      | `distill-current.js`| `3-Resources/Distill-Log.md` | Appends DISTILL MODE + current note path. |
| **Express**      | `express-current.js`| `3-Resources/Express-Log.md` | Appends EXPRESS MODE + current note path. |

All four are **Macro** type with a single **UserScript** step. Each script appends a timestamped line to the relevant log and shows a notice. Optional: use Advanced URI to open Cursor with a pre-filled prompt; if URI is unavailable, the notice says to open Cursor manually.

## Mobile toolbar

In Obsidian: **QuickAdd** → configure each choice → enable **“Create command”** (or equivalent). Then add the commands in **Settings → Mobile → Manage toolbar options** for one-tap access.

## Ingest template chooser

Keep the full ingest template/capture chooser as a **separate** QuickAdd command or command-palette entry; do not put template selection on these four toolbar buttons.
