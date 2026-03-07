# PARA-Zettel Autopilot — Second Brain Vault

A clean **PARA** (Projects, Areas, Resources, Archives) + **Zettelkasten-style** atomic notes vault for Obsidian, with optional Cursor/MCP autopilot for ingest processing.

## Quick setup

1. **Open in Obsidian**  
   Use this folder as an Obsidian vault (File → Open folder as vault).

2. **Core structure**  
   - `1-Projects/` — time-bound goals (starts with one example note; use templates to populate)  
   - `2-Areas/` — ongoing responsibilities (starts with one example note)  
   - `3-Resources/` — reference and atomic notes  
   - `4-Archives/` — inactive items (starts with one example note)  
   - `Ingest/` — raw captures (process into PARA or leave for review)  
   - `Templates/` — note templates  
   - `Daily Notes/` — daily note output (if using Periodic Notes)  

   **PARA folders start empty or with a single example note—use the templates in `Templates/` to create new projects, areas, and resources.**

3. **Hubs & dashboard**  
   - **[[PARA-Dashboard]]** — vault home; Dataview-based overview of Projects, Areas, Resources, Archives  
   - **[[Projects Hub]]**, **[[Areas Hub]]**, **[[Resources Hub]]** — MOC-style index notes

4. **Plugins**  
   - **Dataview** — used in the dashboard and hubs  
   - **Templater** (optional) — for ingest templates  
   - **Obsidian Local REST API** (optional) — for MCP/Cursor integration; after install, set your API key in the plugin settings (no `data.json` is shipped).

## MCP / Cursor rules rebuild

If you use this vault with **Cursor** and **obsidian-mcp-server** (or para-zettel-autopilot MCP):

- Rules and prompts are **not** included in this template (no `.cursor/` folder).
- To restore Cursor behaviour: add a `.cursor/rules/` (or equivalent) folder and repopulate from your own backup or from your MCP server documentation.
- Ingest autopilot: follow the multi-shot flow (create_backup → classify_para → split_atomic → distill → append_to_hub → move_note → log_action) as in your MCP server documentation.

## Optional: zip for distribution

From the vault root:

```bash
zip -r para-zettel-autopilot-clean-v1.zip . -x "*.zip" -x ".git/*" -x ".cursor/*" -x ".trash/*"
```

---

*Built with PARA (Tiago Forte) and atomic/Zettelkasten-style notes. Ingest pipeline compatible with Cursor + Obsidian Local REST API.*
