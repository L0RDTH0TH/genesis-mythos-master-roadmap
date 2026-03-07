---
title: Obsidian MCP Server Integration Plan
created: 2026-02-24
para-type: resource
tags: [mcp, obsidian, reference]
---
### Integration Plan for cyanheads/obsidian-mcp-server into Obsidian Vault

This plan focuses on setting up the cyanheads/obsidian-mcp-server to enable AI agents (like Cursor) to interact with your Obsidian vault via the Local REST API plugin. This will allow reliable operations such as reading, writing, searching, and moving notes (e.g., automating ingest processing to PARA folders without root-dumping files). The setup assumes you have Node.js (v18+) and npm installed; if not, add that as a preliminary manual step.

The plan is divided into two sections as requested:  
- **Cursor Half**: Automated or semi-automated tasks that Cursor (the AI coding IDE) can handle via prompts. These involve code generation, file creation, repo pulling, and config scripting to minimize manual effort. Provide these as ready-to-paste prompts for Cursor.  
- **User Half**: Manual tasks you must complete yourself, as they involve UI interactions, security-sensitive steps, or runtime execution.

#### Cursor Half: Automated Tasks (Handled via Cursor Prompts)
Use Cursor to automate cloning, config generation, script creation, and initial testing setups. Paste each sub-prompt directly into Cursor's Composer or chat mode (prepend your PARA-Zettel-Autopilot persona if desired for consistency). These steps assume your vault is open in Cursor as a project.

1. **Pull/Cloning the Repo Automatically**  
   Prompt:  
   ```
   Clone the GitHub repo https://github.com/cyanheads/obsidian-mcp-server into 4-Archives in my vault, in a folder named mcp-server (i.e. 4-Archives/mcp-server). Use Node.js code to automate the git clone (generate a script like clone-repo.js that runs 'git clone' via child_process). Then, run npm install in the cloned folder via the script. Output the script and suggest running it in terminal (do not execute directly for safety). Log actions to Ingest-Log.md with confidence 100%.
   ```  
   Expected: Cursor generates a Node.js script you can run once (e.g., via code_execution tool if needed, but manually for now). This pulls the server code without manual git commands.

2. **Generate .env Config File**  
   Prompt:  
   ```
   Create a .env file in 4-Archives/mcp-server based on cyanheads repo requirements. Include placeholders for OBSIDIAN_API_KEY (leave blank), OBSIDIAN_BASE_URL="http://127.0.0.1:27123", OBSIDIAN_VERIFY_SSL="false", OBSIDIAN_ENABLE_CACHE="true", and OBSIDIAN_CACHE_REFRESH_INTERVAL_MIN=10. Add comments explaining each var. Do not hardcode sensitive keys. Save it directly if the folder is open; otherwise, output the file content for copy-paste.
   ```  
   Expected: Cursor creates or outputs the .env file automatically, ready for you to fill in the API key later.

3. **Generate Docker Setup Script**  
   Prompt:  
   ```
   The repo includes a Dockerfile. Generate a build-and-run script (e.g., setup-docker.sh) that: 1) Builds the Docker image as 'obsidian-mcp-server', 2) Runs it with --env-file .env and ports mapped (e.g., 3010:3010 for HTTP), 3) Mounts the vault root for any needed access (but warn about security). Make it cross-platform (bash or PowerShell). Output the script content and suggest placing it in 4-Archives/mcp-server/.
   ```  
   Expected: Cursor outputs a ready script for automated building/running the server in Docker, handling config pull from .env.

4. **Generate MCP Client Config for Cursor Integration**  
   Prompt:  
   ```
   Create a JSON config file (e.g., mcp-client-config.json) for integrating the MCP server with AI tools like Cursor. Use the example from cyanheads: Include "mcpServers" with "obsidian-mcp-server" entry, command: "npx", args: ["obsidian-mcp-server"], and env placeholders for API key/URL. Add notes on how to load this in Cursor prompts (e.g., via function calling simulation). Save or output for placement in vault root.
   ```  
   Expected: Cursor generates the config JSON, which you can reference in future Cursor prompts to simulate/call MCP tools.

5. **Generate Test Prompts for MCP Tools**  
   Prompt:  
   ```
   Create a new rule file in .cursor/rules/ called auto-mcp-integration.mdc. Define prompts for testing MCP tools: e.g., "Test read_note on Ingest/example.md", "Test move_note from Ingest/ to 1-Projects/ based on para-type". Make it alwaysApply: true, globs: *.md. Include logging to Ingest-Log.md. Output the full file content.
   ```  
   Expected: Cursor automatically creates a rule file that enables automated testing/integration of MCP tools in your workflow, pulling configs as needed.

#### User Half: Manual Tasks
These steps require your direct intervention for security, UI access, or verification. Complete them in sequence after the Cursor half where applicable.

1. **Install and Configure Obsidian Local REST API Plugin**  
   - Open Obsidian → Settings → Community Plugins → Browse → Search for "Local REST API" → Install and Enable.  
   - In plugin settings: Generate/configure an API key (copy it securely).  
   - Enable "Non-encrypted (HTTP) Server" for simpler setup (uses port 27123); or use HTTPS (27124) and note the self-signed cert warning.  
   - Restart Obsidian to activate the API server.

2. **Fill in Sensitive Configs**  
   - After Cursor generates .env and mcp-client-config.json, manually edit them: Paste your OBSIDIAN_API_KEY from the plugin. Verify other vars (e.g., BASE_URL matches your port).  
   - Do not commit these to Git (add .env to .gitignore if needed).

3. **Run npm Install and Build (If Not Docker)**  
   - Navigate to the MCP server folder in terminal: `cd vault-root/4-Archives/mcp-server`.  
   - Run `npm install` to pull dependencies.  
   - If using local run: `npm run build` to compile TypeScript.

4. **Run the Server**  
   - For local stdio: `npx obsidian-mcp-server` (or `node dist/index.js`).  
   - For HTTP: `npm run start:http` (default port 3010).  
   - For Docker: Run the script generated by Cursor (e.g., `./setup-docker.sh`). Ensure Docker is installed/running.  
   - Verify: Check console for startup logs; test connectivity (e.g., curl http://localhost:3010 if HTTP).

5. **Integrate and Test in Cursor**  
   - Open Cursor with your vault as project.  
   - Use a test prompt like: "Using obsidian-mcp-server, read a note from Ingest/ and propose a move to PARA folder." (Reference the generated mcp-client-config.json if needed for env).  
   - Manually append any test logs to Ingest-Log.md and review for issues (e.g., SSL errors → set VERIFY_SSL=false).  
   - If integration fails, debug by checking server logs or restarting Obsidian/plugin.

Once complete, your setup should allow Cursor prompts to invoke MCP tools (e.g., move_note) autonomously, closing the automation loop for ingest processing. Test in a vault copy first. If issues arise (e.g., cache mismatches), disable cache in .env.




Here’s a concrete **how** for the Advanced Exclude route:

---

# 1. Install BRAT (if you don’t have it)

1. Open **Settings** (gear) → **Community plugins** → **Browse**.
2. Search for **BRAT** (full name: **Obsidian42 - BRAT**).
3. **Install**, then **Enable**.
4. Leave Community plugins **on** (toggle at top).

---

## 2. Install Advanced Exclude via BRAT

1. In Obsidian, go to **Settings** → **Community plugins** and find **BRAT** in the list.
2. Open **BRAT** settings.
3. Click **“Add a beta plugin”**.
4. Paste this repo URL and confirm:
   ```text
   https://github.com/mnaoumov/obsidian-advanced-exclude
   ```
5. Wait until the plugin appears in the list, then **enable** it (toggle on).

**Alternative:** Open this link in your browser (with Obsidian running and the vault open); it should trigger the BRAT “Add plugin” flow:

```text
obsidian://brat?plugin=https://github.com/mnaoumov/obsidian-advanced-exclude
```

(Some setups use a redirector; if the link doesn’t open Obsidian, use the “Add a beta plugin” + URL method above.)

---

## 3. Create `.obsidianignore` in the vault root

1. In your **Second-Brain** vault root, create a file named **`.obsidianignore`** (no extension).
2. Put one of these lines in it (one line is enough):

   ```text
   mcp-server/
   ```

   or, to match that folder name anywhere in the vault:

   ```text
   **/mcp-server/**
   ```

3. Save the file.

---

## 4. Reload so Obsidian picks it up

- **Settings** → **Advanced** → **Reload app without saving**,  
  or close and reopen the vault.

After that, `mcp-server/` is treated as non-existent for indexing (search, graph, backlinks, etc.). To change what’s ignored later, edit `.obsidianignore` (gitignore-style patterns).

## Why resource?
Assigned based on content/frontmatter (confidence ~85%).

## Review Needed
Proposed para-type: resource. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.