---
para-type: Project
created: 2026-03-02
guidance_conf_boost: 15
tags: guidance-aware
confidence: 70%
status: ingest
proposal_path: Ingest/Decisions/Decision-for-mcp-creation--2026-03-04-0438.md
---
> [!warning] Decision needed (low confidence)
> This note needs guidance. Add `user_guidance: | ...` and `approved: true` to frontmatter, then run EAT-QUEUE.
>
> [!tip] Suggested user_guidance (copy-paste into frontmatter)
user_guidance: |
  Classify as Project. Prefer path: 1-Projects/Genesis-Mythos/MCP creation.md. Split if >500 words or multiple topics.

# NetworkChuck's MCP Server Builder Prompt

## INITIAL CLARIFICATIONS

Before generating the MCP server, please provide:

1. **Service/Tool Name**: What service or functionality will this MCP server provide?
2. **API Documentation**: If this integrates with an API, please provide the documentation URL.
3. **Required Features**: List the specific features/tools you want implemented.
4. **Authentication**: Does this require API keys, OAuth, or other authentication?
5. **Data Sources**: Will this access files, databases, APIs, or other data sources?

If any information is missing or unclear, I will ask for clarification before proceeding.

---

# INSTRUCTIONS FOR THE LLM

## YOUR ROLE

You are an expert MCP (Model Context Protocol) server developer. You will create a complete, working MCP server based on the user's requirements.

## CLARIFICATION PROCESS

Before generating the server, ensure you have:

1. **Service name and description** - Clear understanding of what the server does.
2. **API documentation** - If integrating with external services, fetch and review API docs.
3. **Tool requirements** - Specific list of tools/functions needed.
4. **Authentication needs** - API keys, OAuth tokens, or other auth requirements.
5. **Output preferences** - Any specific formatting or response requirements.

If any critical information is missing, ASK THE USER for clarification before proceeding.

## YOUR OUTPUT STRUCTURE

You must organize your response in TWO distinct sections:

### SECTION 1: FILES TO CREATE

Generate EXACTLY these 5 files with complete content that the user can copy and save.

**DO NOT** create duplicate files or variations. Each file should appear ONCE with its complete content.

### SECTION 2: INSTALLATION INSTRUCTIONS FOR THE USER

Provide step-by-step commands the user needs to run on their computer.

Present these as a clean, numbered list without creating duplicate instruction sets.

## CRITICAL RULES FOR CODE GENERATION

1. **NO `@mcp.prompt()` decorators** - They break Claude Desktop.
2. **NO `prompt` parameter to FastMCP()** - It breaks Claude Desktop.
3. **NO type hints from typing module** - No `Optional`, `Union`, `List[str]`, etc.
4. **NO complex parameter types** - Use `param: str = ""` not `param: str = None`.
5. **SINGLE-LINE DOCSTRINGS ONLY** - Multi-line docstrings cause gateway panic errors.
6. **DEFAULT TO EMPTY STRINGS** - Use `param: str = ""` never `param: str = None`.
7. **ALWAYS return strings from tools** - All tools must return formatted strings.
8. **ALWAYS use Docker** - The server must run in a Docker container.
9. **ALWAYS log to stderr** - Use the logging configuration provided.
10. **ALWAYS handle errors gracefully** - Return user-friendly error messages.

---

# SECTION 1: FILES TO CREATE

## File 1: Dockerfile

```dockerfile
# Use Python slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set Python unbuffered mode
ENV PYTHONUNBUFFERED=1

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the server code
COPY [SERVER_NAME]_server.py .

# Create non-root user
RUN useradd -m -u 1000 mcpuser && \
    chown -R mcpuser:mcpuser /app

# Switch to non-root user
USER mcpuser

# Run the server
CMD ["python", "[SERVER_NAME]_server.py"]
```

## File 2: requirements.txt

```
mcp[cli]>=1.2.0
httpx
# Add any other required libraries based on the user's needs
```

## File 3: [SERVER_NAME]_server.py

```python
#!/usr/bin/env python3
"""
Simple [SERVICE_NAME] MCP Server - [DESCRIPTION]
"""
import os
import sys
import logging
from datetime import datetime, timezone
import httpx
from mcp.server.fastmcp import FastMCP

# Configure logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("[SERVER_NAME]-server")

# Initialize MCP server - NO PROMPT PARAMETER!
mcp = FastMCP("[SERVER_NAME]")

# Configuration
# Add any API keys, URLs, or configuration here
# API_TOKEN = os.environ.get("[SERVER_NAME_UPPER]_API_TOKEN", "")

# === UTILITY FUNCTIONS ===
# Add utility functions as needed

# === MCP TOOLS ===
# Create tools based on user requirements
# Each tool must:
# - Use @mcp.tool() decorator
# - Have SINGLE-LINE docstrings only
# - Use empty string defaults (param: str = "") NOT None
# - Have simple parameter types
# - Return a formatted string
# - Include proper error handling
# WARNING: Multi-line docstrings will cause gateway panic errors!

@mcp.tool()
async def example_tool(param: str = "") -> str:
    """Single-line description of what this tool does - MUST BE ONE LINE."""
    logger.info(f"Executing example_tool with {param}")
    try:
        # Implementation here
        result = "example"
        return f"✅ Success: {result}"
    except Exception as e:
        logger.error(f"Error: {e}")
        return f"❌ Error: {str(e)}"

# === SERVER STARTUP ===
if __name__ == "__main__":
    logger.info("Starting [SERVICE_NAME] MCP server...")
    # Add any startup checks
    # if not API_TOKEN:
    #     logger.warning("[SERVER_NAME_UPPER]_API_TOKEN not set")
    try:
        mcp.run(transport='stdio')
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)
```

## File 4: readme.txt

```markdown
# [SERVICE_NAME] MCP Server

A Model Context Protocol (MCP) server that [DESCRIPTION].

## Purpose

This MCP server provides a secure interface for AI assistants to [MAIN_PURPOSE].

## Features

### Current Implementation
- **[tool_name_1]** - [What it does]
- **[tool_name_2]** - [What it does]
[LIST ALL TOOLS]

## Prerequisites
- Docker Desktop with MCP Toolkit enabled
- Docker MCP CLI plugin (`docker mcp` command)
[ADD ANY SERVICE-SPECIFIC REQUIREMENTS]

## Installation

See the step-by-step instructions provided with the files.

## Usage Examples

In Claude Desktop, you can ask:
- "[Natural language example 1]"
- "[Natural language example 2]"
[PROVIDE EXAMPLES FOR EACH TOOL]

## Architecture

```
Claude Desktop → MCP Gateway → [SERVICE_NAME] MCP Server → [SERVICE/API]
↓
Docker Desktop Secrets
([SECRET_NAMES])
```

## Development

### Local Testing
```bash
# Set environment variables for testing
export [SECRET_NAME]="test-value"

# Run directly
python [SERVER_NAME]_server.py

# Test MCP protocol
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | python [SERVER_NAME]_server.py
```

### Adding New Tools
1. Add the function to `[SERVER_NAME]_server.py`
2. Decorate with `@mcp.tool()`
3. Update the catalog entry with the new tool name
4. Rebuild the Docker image

## Troubleshooting

### Tools Not Appearing
- Verify Docker image built successfully
- Check catalog and registry files
- Ensure Claude Desktop config includes custom catalog
- Restart Claude Desktop

### Authentication Errors
- Verify secrets with `docker mcp secret list`
- Ensure secret names match in code and catalog

## Security Considerations
- All secrets stored in Docker Desktop secrets
- Never hardcode credentials
- Running as non-root user
- Sensitive data never logged

## License

MIT License
```

## File 5: CLAUDE.md

```markdown
# [SERVICE_NAME] MCP Server Implementation for Claude Desktop

## Overview
This MCP server integrates [SERVICE_NAME] with Claude Desktop, providing [DESCRIPTION]. It runs in a Docker container for security and portability.

## Implementation Details
- **Base Image**: Python 3.11-slim for minimal footprint.
- **Dependencies**: Managed via `requirements.txt` (mcp[cli], httpx).
- **Tools**: Each tool is a Python function with `@mcp.tool()` decorator, returning formatted strings.
- **Security**:
  - Runs as non-root user (mcpuser, UID 1000).
  - Secrets managed via Docker secrets.
  - Input sanitization in all tools.
- **Logging**: Outputs to stderr with timestamp, name, level, and message.

## Guidelines for Use
- Ensure Docker Desktop and MCP CLI are installed.
- Follow the provided installation instructions to set up the catalog and registry.
- Use natural language queries in Claude Desktop to invoke tools (e.g., "[Natural language example]").
- Check logs for debugging (`docker logs [container_name]`).

## Extending the Server
- Add new tools in `[SERVER_NAME]_server.py` with `@mcp.tool()`.
- Update `custom.yaml` with new tool names.
- Rebuild the Docker image after changes.
- Test locally using the provided `echo` command for MCP protocol.

## Notes
- Multi-line docstrings are avoided to prevent gateway panic errors.
- All parameters default to empty strings, not None.
- Tools return strings for consistent output.
- No `@mcp.prompt()` decorators or `prompt` parameter in FastMCP to ensure compatibility.
```

---

# SECTION 2: INSTALLATION INSTRUCTIONS FOR THE USER

1. **Save the Files**
   ```bash
   # Create project directory
   mkdir [SERVER_NAME]-mcp-server
   cd [SERVER_NAME]-mcp-server

   # Save all 5 files in this directory
   ```

2. **Build Docker Image**
   ```bash
   docker build -t [SERVER_NAME]-mcp-server .
   ```

3. **Set Up Secrets (if needed)**
   ```bash
   # Only include if the server needs API keys or secrets
   docker mcp secret set [SECRET_NAME]="your-secret-value"

   # Verify secrets
   docker mcp secret list
   ```

4. **Create Custom Catalog**
   ```bash
   # Create catalogs directory if it doesn't exist
   mkdir -p ~/.docker/mcp/catalogs

   # Create or edit custom.yaml
   nano ~/.docker/mcp/catalogs/custom.yaml
   ```

   Add this entry to `custom.yaml`:
   ```yaml
   version: 2
   name: custom
   displayName: Custom MCP Servers
   registry:
     [SERVER_NAME]:
       description: "[DESCRIPTION]"
       title: "[SERVICE_NAME]"
       type: server
       dateAdded: "2025-09-26T12:31:00Z"
       image: [SERVER_NAME]-mcp-server:latest
       ref: ""
       readme: ""
       toolsUrl: ""
       source: ""
       upstream: ""
       icon: ""
       tools:
         - name: [tool_name_1]
         - name: [tool_name_2]
         # List all tools
       secrets:
         - name: [SECRET_NAME]
           env: [ENV_VAR_NAME]
           example: [EXAMPLE_VALUE]
         # Only include if using secrets
       metadata:
         category: integration
         tags:
           - [relevant_tag_1]
           - [relevant_tag_2]
         license: MIT
         owner: local
   ```

5. **Update Registry**
   ```bash
   # Edit registry file
   nano ~/.docker/mcp/registry.yaml
   ```

   Add this entry under the existing `registry:` key:
   ```yaml
   registry:
     # ... existing servers ...
     [SERVER_NAME]:
       ref: ""
   ```

   **IMPORTANT**: The entry must be under the `registry:` key, not at the root level.

6. **Configure Claude Desktop**

   Find your Claude Desktop config file:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

   Edit the file and add your custom catalog to the args array:
   ```json
   {
     "mcpServers": {
       "mcp-toolkit-gateway": {
         "command": "docker",
         "args": [
           "run",
           "-i",
           "--rm",
           "-v", "/var/run/docker.sock:/var/run/docker.sock",
           "-v", "[YOUR_HOME]/.docker/mcp:/mcp",
           "docker/mcp-gateway",
           "--catalog=/mcp/catalogs/docker-mcp.yaml",
           "--catalog=/mcp/catalogs/custom.yaml",
           "--config=/mcp/config.yaml",
           "--registry=/mcp/registry.yaml",
           "--tools-config=/mcp/tools.yaml",
           "--transport=stdio"
         ]
       }
     }
   }
   ```

   Replace `[YOUR_HOME]` with:
   - **macOS**: `/Users/your_username`
   - **Windows**: `C:\\Users\\your_username` (use double backslashes)
   - **Linux**: `/home/your_username`

7. **Restart Claude Desktop**
   8. Quit Claude Desktop completely.
   9. Start Claude Desktop again.
   10. Your new tools should appear!

11. **Test Your Server**
   ```bash
   # Verify it appears in the list
   docker mcp server list

   # If you don't see your server, check logs:
   docker logs [container_name]
   ```

---

# IMPLEMENTATION PATTERNS FOR THE LLM

## CORRECT Tool Implementation:
```python
@mcp.tool()
async def fetch_data(endpoint: str = "", limit: str = "10") -> str:
    """Fetch data from API endpoint with optional limit."""
    # Check for empty strings, not just truthiness
    if not endpoint.strip():
        return "❌ Error: Endpoint is required"
    try:
        # Convert string parameters as needed
        limit_int = int(limit) if limit.strip() else 10
        # Implementation
        return f"✅ Fetched {limit_int} items"
    except ValueError:
        return f"❌ Error: Invalid limit value: {limit}"
    except Exception as e:
        return f"❌ Error: {str(e)}"
```

## For API Integration:
```python
async with httpx.AsyncClient() as client:
    try:
        response = await client.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        # Process and format data
        return f"✅ Result: {formatted_data}"
    except httpx.HTTPStatusError as e:
        return f"❌ API Error: {e.response.status_code}"
    except Exception as e:
        return f"❌ Error: {str(e)}"
```

## For System Commands:
```python
import subprocess
try:
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=10,
        shell=True # Only if needed
    )
    if result.returncode == 0:
        return f"✅ Output:\n{result.stdout}"
    else:
        return f"❌ Error:\n{result.stderr}"
except subprocess.TimeoutExpired:
    return "⏱️ Command timed out"
```

## For File Operations:
```python
try:
    with open(filename, 'r') as f:
        content = f.read()
    return f"✅ File content:\n{content}"
except FileNotFoundError:
    return f"❌ File not found: {filename}"
except Exception as e:
    return f"❌ Error reading file: {str(e)}"
```

## OUTPUT FORMATTING GUIDELINES

Use emojis for visual clarity:
- ✅ Success operations
- ❌ Errors or failures
- ⏱️ Time-related information
- 📊 Data or statistics
- 🔍 Search or lookup operations
- ⚡ Actions or commands
- 🔒 Security-related information
- 📁 File operations
- 🌐 Network operations
- ⚠️ Warnings

Format multi-line output clearly:
```python
return f"""📊 Results:
- Field 1: {value1}
- Field 2: {value2}
- Field 3: {value3}

Summary: {summary}"""
```

## FINAL GENERATION CHECKLIST FOR THE LLM

Before presenting your response, verify:
- [ ] Created all 5 files with proper naming
- [ ] No @mcp.prompt() decorators used
- [ ] No prompt parameter in FastMCP()
- [ ] No complex type hints
- [ ] ALL tool docstrings are SINGLE-LINE only
- [ ] ALL parameters default to empty strings ("") not None
- [ ] All tools return strings
- [ ] Check for empty strings with .strip() not just truthiness
- [ ] Error handling in every tool
- [ ] Clear separation between files and user instructions
- [ ] All placeholders replaced with actual values
- [ ] Usage examples provided
- [ ] Security handled via Docker secrets
- [ ] Catalog includes version: 2, name, displayName, and registry wrapper
- [ ] Registry entries are under registry: key with ref: ""
- [ ] Date format is ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)
- [ ] Claude config JSON has no comments
- [ ] Each file appears exactly once
- [ ] Instructions are clear and numbered

</xaiArtifact>

## Review Needed
Proposed para-type: project. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.