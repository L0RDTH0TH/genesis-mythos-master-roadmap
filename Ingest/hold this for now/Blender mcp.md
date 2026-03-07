---
para-type: Resource
confidence: 70%
created: 2026-03-02
status: ingest
decision_candidate: true
decision_priority: high
proposal_path: Ingest/Decisions/Decision-for-blender-mcp--2026-03-04-0424.md
---
### Step-by-Step Setup (Works on Windows/macOS/Linux)

#### 1. Install Blender MCP Addon (inside Blender)
   - Download the latest release from GitHub: https://github.com/mehmetakar/BlenderMCP/releases
   - Open Blender → Edit → Preferences → Add-ons → Install → select the `.zip`
   - Enable **Blender MCP** (search for it)
   - Press **N** in the 3D viewport → MCP tab appears on the sidebar
   - Click **Start Server** (light turns green = success)<grok:render card_id="b6f0e4" card_type="citation_card" type="render_inline_citation">
<argument name="citation_id">23</argument>
</grok:render><grok:render card_id="98a577" card_type="citation_card" type="render_inline_citation">
<argument name="citation_id">34</argument>
</grok:render>

   **Bonus features** you get for free:
   - Viewport screenshots
   - Poly Haven / Hyper3D asset search
   - Sketchfab upload
   - Material editing
   - Arbitrary Python execution

#### 2. Install `uv` (Python tool runner – required for MCP server)
   ```bash
   # Windows (PowerShell)
   iwr https://astral.sh/uv/install.ps1 | iex

   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
   Restart terminal.<grok:render card_id="e6c0b0" card_type="citation_card" type="render_inline_citation">
<argument name="citation_id">1</argument>
</grok:render>

#### 3. Connect Cursor to Blender MCP
   - Open Cursor → Settings (⌘,) → Features → MCP
   - Add new server:
     ```json
     {
       "mcpServers": {
         "blender": {
           "command": "uvx",
           "args": ["blender-mcp"]
         }
       }
     }
     ```
   - On Windows: use full path if needed (see forum fix).<grok:render card_id="e13302" card_type="citation_card" type="render_inline_citation">
<argument name="citation_id">1</argument>
</grok:render>
   - Save → Restart Cursor
   - Cursor now shows **Blender** tools in Agent mode!

#### 4. Test It!
   - Open Cursor Agent (⌘ L)
   - Type: *"In Blender, create a red cube at origin, then a sphere on top, apply smooth shading"*
   - Watch Blender update live (keep Blender window visible)
   - Or: *"Import a tree from Poly Haven and place it at (5,0,0)"*

### Pro Tips for Insane Workflows (2025 Edition)
- **Use GPT-5 High / Codex** in Cursor for complex prompts – it understands Blender API deeply.<grok:render card_id="73ee82" card_type="citation_card" type="render_inline_citation">
<argument name="citation_id">45</argument>
</grok:render>
- Combine with **Trae Editor** or **Windsurf** for even faster loops.
- For local/no-API: point MCP at Ollama (Llama 3.2-Vision or DeepSeek-Coder).<grok:render card_id="546cda" card_type="citation_card" type="render_inline_citation">
<argument name="citation_id">34</argument>
</grok:render>
- Security: MCP runs arbitrary Python – only use trusted prompts.
- Alternative quick-start: Use the curated MCP list in Cursor → "Add from marketplace" → search "Blender".<grok:render card_id="ae82f8" card_type="citation_card" type="render_inline_citation">
<argument name="citation_id">11</argument>
</grok:render>

### Results People Are Getting
- Full airplanes built piece-by-piece with natural language.<grok:render card_id="d4082c" card_type="citation_card" type="render_inline_citation">
<argument name="citation_id">18</argument>
</grok:render>
- Low-poly ninjas + Unity export in minutes.<grok:render card_id="78fa60" card_type="citation_card" type="render_inline_citation">
<argument name="citation_id">24</argument>
</grok:render>
- Agentic systems that run inside Blender itself.<grok:render card_id="61fc67" card_type="citation_card" type="render_inline_citation">
<argument name="citation_id">49</argument>
</grok:render>

This is legitimately "Cursor for 3D" – no more manual modeling for concepts. Set it up once and you'll never open Blender the old way again.<grok:render card_id="c6acbb" card_type="citation_card" type="render_inline_citation">
<argument name="citation_id">20</argument>
</grok:render><grok:render card_id="17c957" card_type="citation_card" type="render_inline_citation">
<argument name="citation_id">50</argument>
</grok:render>

If you hit any snags (e.g., Windows path issues), drop a screenshot – happy to debug! 🚀

## Review Needed
Proposed para-type: resource. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.