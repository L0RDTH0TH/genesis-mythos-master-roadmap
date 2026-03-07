---
status: reviewed
---
## TL;DR
# Config Reference — Obsidian PARA-Zettel Autopilot MCP

---

# Config Reference — Obsidian PARA-Zettel Autopilot MCP

Quick reference for environment variables and Cursor MCP config. See **INSTALL-CURSOR.md** for full setup and troubleshooting.

---

## Environment variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| **OBSIDIAN_API_KEY** | Yes | — | API key from Obsidian → Settings → Community plugins → Local REST API. |
| **OBSIDIAN_REST_URL** | No | `http://127.0.0.1:27123` | Base URL of the Local REST API (host:port). Change if your plugin uses another port. |
| **OBSIDIAN_VAULT_PATH** | No | — | Absolute path to vault root (folder you open in Obsidian). Enables resolving absolute/workspace paths to vault-relative paths. |
| **BACKUP_DIR** | No* | — | Absolute path to backup directory for Option C safety. Required for destructive tools (move/delete/rename/overwrite/search_replace). Create the directory yourself. |

\* Optional for read-only use; required for destructive tools. Can also be set as top-level `backup_dir` in `~/.cursor/mcp.json` when running **Python** (not when running in Docker — use `BACKUP_DIR` env for Docker).

---

## Export template (shell)

You can source these before running the server or use them as values in Cursor’s MCP `env`:

```bash
export OBSIDIAN_API_KEY="your-api-key-from-obsidian"
export OBSIDIAN_REST_URL="http://127.0.0.1:27123"
export OBSIDIAN_VAULT_PATH="/path/to/your/vault"
export BACKUP_DIR="/path/to/your/backups"
```

Project file **Export-variables.txt** can hold your actual values (do not commit real keys).

---

## Cursor MCP config (`~/.cursor/mcp.json`)

### Why volume mounts in Docker?

Docker containers have an isolated filesystem. Without mounts, paths like `OBSIDIAN_VAULT_PATH` and `BACKUP_DIR` refer to directories *inside* the container, not on your host. The server writes Option C backups to `BACKUP_DIR`—if that isn’t a mount of your host backup folder, backups stay in the container and are lost when the container exits. Mounting the vault and backup dir (same path on host and in container) keeps backups on the host and keeps path resolution correct.

---

### Docker (stdio) — Linux (with `--network host`)

Use this so the container can reach Obsidian on the host (e.g. `127.0.0.1:27123`). **Volume mounts are required**: Docker’s filesystem is isolated from the host, so the vault and backup directories must be mounted for backups to persist on the host and for path resolution to match Obsidian.

```json
{
  "mcpServers": {
    "obsidian-para-zettel-autopilot": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--network", "host",
        "-v", "/path/to/your/vault:/path/to/your/vault",
        "-v", "/path/to/your/backups:/path/to/your/backups",
        "-e", "OBSIDIAN_API_KEY",
        "-e", "OBSIDIAN_REST_URL",
        "-e", "OBSIDIAN_VAULT_PATH",
        "-e", "BACKUP_DIR",
        "obsidian-para-zettel-autopilot-mcp:latest"
      ],
      "env": {
        "OBSIDIAN_API_KEY": "your-api-key",
        "OBSIDIAN_REST_URL": "http://127.0.0.1:27123",
        "OBSIDIAN_VAULT_PATH": "/path/to/your/vault",
        "BACKUP_DIR": "/path/to/your/backups"
      }
    }
  }
}
```

- **Image**: Build with `docker build -t obsidian-para-zettel-autopilot-mcp:latest .` from the project root.
- **Mounts**: Use the same paths in `-v` as in `env` (host path and container path identical) so backups written by the server land on the host and vault paths resolve correctly.
- Use `-i` only (no `-t`); do not use `-t` with stdio.
- Replace `your-api-key`, paths, and port in `env` and in the two `-v` entries to match your setup.

### Docker (stdio) — macOS / Windows

If the API is on the host, use `host.docker.internal` for the URL. **Volume mounts are required** so the container sees your vault and backup dir (e.g. `-v /path/on/host:/path/on/host` with the same paths in `env`).

```json
{
  "mcpServers": {
    "obsidian-para-zettel-autopilot": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-v", "/path/to/your/vault:/path/to/your/vault",
        "-v", "/path/to/your/backups:/path/to/your/backups",
        "-e", "OBSIDIAN_API_KEY",
        "-e", "OBSIDIAN_REST_URL",
        "-e", "OBSIDIAN_VAULT_PATH",
        "-e", "BACKUP_DIR",
        "obsidian-para-zettel-autopilot-mcp:latest"
      ],
      "env": {
        "OBSIDIAN_API_KEY": "your-api-key",
        "OBSIDIAN_REST_URL": "http://host.docker.internal:27123",
        "OBSIDIAN_VAULT_PATH": "/path/to/your/vault",
        "BACKUP_DIR": "/path/to/your/backups"
      }
    }
  }
}
```

### Python (stdio, no Docker)

For local runs the server can read `backup_dir` from `~/.cursor/mcp.json` (top-level key) or use **BACKUP_DIR** env.

```json
{
  "mcpServers": {
    "obsidian-para-zettel-autopilot": {
      "command": "python",
      "args": ["/absolute/path/to/obsidian-para-zettel-autopilot_server.py"],
      "env": {
        "OBSIDIAN_API_KEY": "your-api-key",
        "OBSIDIAN_REST_URL": "http://127.0.0.1:27123",
        "OBSIDIAN_VAULT_PATH": "/path/to/your/vault",
        "BACKUP_DIR": "/path/to/your/backups"
      }
    }
  }
}
```

Optional: add a top-level `backup_dir` in the same JSON file (used when **BACKUP_DIR** is not set):

```json
{
  "backup_dir": "/path/to/your/backups",
  "mcpServers": { ... }
}
```

---

## Rebuild Docker image

After code or dependency changes:

```bash
cd /path/to/PARA-Zettel-Autopilot
docker build -t obsidian-para-zettel-autopilot-mcp:latest .
```

Restart Cursor after changing MCP config or rebuilding the image.

## Review Needed
Proposed para-type: project. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.