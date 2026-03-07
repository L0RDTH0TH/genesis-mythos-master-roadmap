#!/usr/bin/env python3
"""Build Genesis docs timeline from local git (Azgaar) + repo-level date (genesis-mythos)."""
import subprocess
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
INGEST = VAULT / "Ingest"
AZGAAR_CLONE = Path("/tmp/GM")
GM_REPO_DATE = "2026-01-12T20:18:21Z"  # from API: latest commit on main

def repo_path_from_ingest(rel: str, prefix: str) -> str:
    """Ingest path segment -> repo path (-- to /)."""
    if rel.startswith(prefix + "/"):
        rel = rel[len(prefix) + 1:]
    return rel.replace("--", "/")

def main():
    rows = []

    # Genesis-Azgaar: per-file from local clone
    for f in (INGEST / "Genesis-Azgaar").rglob("*"):
        if not f.is_file() or f.suffix.lower() not in (".md", ".txt"):
            continue
        rel = str(f.relative_to(INGEST))
        repo_path = repo_path_from_ingest(rel, "Genesis-Azgaar")
        r = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", repo_path],
            cwd=AZGAAR_CLONE,
            capture_output=True,
            text=True,
        )
        if r.returncode == 0 and r.stdout.strip():
            rows.append((rel, repo_path, "L0RDTH0TH/Genesis-Azgaar", r.stdout.strip()))

    # Genesis-mythos: repo-level date for every ingest file
    gm_root = INGEST / "genesis-mythos"
    if gm_root.exists():
        for f in gm_root.rglob("*"):
            if not f.is_file() or f.suffix.lower() not in (".md", ".txt"):
                continue
            rel = str(f.relative_to(INGEST))
            repo_path = repo_path_from_ingest(rel, "genesis-mythos")
            rows.append((rel, repo_path, "L0RDTH0TH/genesis-mythos", GM_REPO_DATE))

    # Sort by date descending
    rows.sort(key=lambda r: r[3], reverse=True)

    # Markdown
    out_md = INGEST / "Genesis-Docs-Timeline.md"
    lines = [
        "# Genesis docs timeline (last touched in Git)",
        "",
        "Per-file **last commit date** where available. Genesis-mythos uses repo-level latest commit (per-file would require clone or API token).",
        "",
        "| Ingest path | Repo path | Repo | Last touched (UTC) |",
        "|-------------|-----------|------|---------------------|",
    ]
    for rel, repo_path, repo, date in rows:
        lines.append(f"| `{rel}` | `{repo_path}` | {repo} | {date} |")
    lines.extend(["", "---", f"*Generated; {len(rows)} files.*"])
    out_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out_md} ({len(rows)} rows)")

    # JSON for frontmatter
    out_json = INGEST / "Genesis-Docs-Timeline.json"
    data = [{"ingest_path": r[0], "repo_path": r[1], "repo": r[2], "source_last_touched_at": r[3]} for r in rows]
    out_json.write_text(__import__("json").dumps(data, indent=2), encoding="utf-8")
    print(f"Wrote {out_json}")

if __name__ == "__main__":
    main()
