---
title: obsidian_snapshot MCP Tool Spec
created: 2026-02-25
para-type: Resource
status: draft
tags: [cursor, mcp, obsidian, snapshots]
---

# obsidian_snapshot MCP Tool (spec)

This document describes a future Obsidian MCP tool, `obsidian_snapshot`, that provides a native implementation of the snapshot behavior currently orchestrated by the `.cursor/skills/obsidian-snapshot` skill.

The goal is to support **per-change** and **batch** snapshots with integrity hashes and flattened naming, wired to `SNAPSHOT_DIR` and `BATCH_SNAPSHOT_DIR` from `~/.cursor/mcp.json`.

## Parameters (conceptual schema)

```json
{
  "name": "obsidian_snapshot",
  "params": {
    "note_path": {
      "type": "string",
      "description": "Vault-relative path of the note to snapshot (e.g. '1-Projects/Project-X/note.md'). Required for per-change, optional for batch."
    },
    "type": {
      "type": "string",
      "enum": ["per-change", "batch"],
      "description": "Snapshot mode: 'per-change' for a single note, 'batch' for a summary over multiple notes."
    },
    "description": {
      "type": "string",
      "description": "Human-readable context (e.g. 'INGEST MODE – safe batch autopilot'), included in logs and batch snapshots."
    },
    "batch_details": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "note_path": { "type": "string" },
          "snapshot_path": { "type": "string" },
          "confidence": { "type": "number" }
        },
        "required": ["note_path", "snapshot_path"]
      },
      "description": "For type='batch': list of notes and their per-change snapshots included in this checkpoint."
    },
    "profile": {
      "type": "string",
      "enum": ["default", "lightweight", "aggressive"],
      "description": "Optional performance/safety profile (e.g. 'lightweight' to skip batch files, 'aggressive' for more frequent snapshots)."
    },
    "project_override": {
      "type": "boolean",
      "description": "If true, allow future project-specific overrides (e.g. project-specific retention or directories) based on note frontmatter such as project-id or highlight_key."
    }
  }
}
```

## Behavior (per-change)

Pseudocode (conceptual, not bound to a specific language):

```text
def create_per_change_snapshot(note_path, description, profile):
    vault_root = ENV["OBSIDIAN_VAULT_PATH"]
    snapshot_root = ENV["SNAPSHOT_DIR"]

    assert note_path.startswith(vault_root) or is_vault_relative(note_path)

    content = read_note_from_vault(note_path)
    slug = safe_slug(basename(note_path))                 # e.g. "2026-02-25-report"
    path_hash = short_hash(note_path)                     # e.g. first 8 chars of SHA256
    timestamp = now_utc().strftime("%Y%m%d-%H%M%S")

    snapshot_filename = f"{slug}--{path_hash}--{timestamp}.md.bak"
    snapshot_path = os.path.join(snapshot_root, snapshot_filename)

    snapshot_hash = hash_content(content)                 # e.g. SHA256 hex

    frontmatter = {
        "original_path": note_path,
        "original_title": extract_title(content) or slug,
        "pipeline": infer_pipeline_from_description(description),
        "snapshot_type": "per-change",
        "snapshot_created": now_utc_iso(),
        "snapshot_hash": snapshot_hash,
        "confidence": infer_confidence_from_description(description),
        "flag": "none",
        "immutable": True,
        "para-type": "Archive",
        "status": "frozen"
    }

    snapshot_content = inject_frontmatter(content, frontmatter)

    ensure_directory_exists(snapshot_root)
    write_file(snapshot_path, snapshot_content, overwrite=True)

    return { "snapshot_path": snapshot_path }
```

## Behavior (batch)

```text
def create_batch_snapshot(batch_details, description, profile):
    batch_root = ENV["BATCH_SNAPSHOT_DIR"]

    timestamp = now_utc_iso()
    batch_id = next_batch_id()  # monotonic counter or timestamp-based
    batch_filename = f"{timestamp}-batch-{batch_id}.md"
    batch_path = os.path.join(batch_root, batch_filename)

    ensure_directory_exists(batch_root)

    # Minimal markdown summary
    content = []
    content.append(f"# Batch snapshot {batch_id}")
    content.append("")
    content.append(f"- created: {timestamp}")
    content.append(f"- context: {description}")
    content.append(f"- notes: {len(batch_details)}")
    content.append("")
    content.append("| note | snapshot | confidence |")
    content.append("|------|----------|------------|")
    for item in batch_details:
        content.append(f"| {item.note_path} | {item.snapshot_path} | {item.confidence or ''} |")

    write_file(batch_path, "\\n".join(content), overwrite=True)

    return { "batch_snapshot_path": batch_path }
```

## Integrity and retention

- Each per-change snapshot stores `snapshot_hash` in frontmatter; restore logic should recompute and compare this value before overwriting any original note.
- Retention (e.g. `SNAPSHOT_MAX_DAYS`, `SNAPSHOT_MAX_PER_NOTE`) is enforced at a higher level (e.g. via a `snapshot-sweep` rule), not by this tool directly.

## Relationship to the obsidian-snapshot skill

- Until this MCP tool is implemented in the server, Cursor agents should use:
  - `.cursor/skills/obsidian-snapshot/SKILL.md` to orchestrate equivalent behavior via:
    - `obsidian_read_note`
    - `obsidian_update_note`
    - `obsidian_ensure_structure`
  - `3-Resources/Backup-Log.md` and `3-Resources/Restore Hub.md` for human-facing logs and restore flows.

