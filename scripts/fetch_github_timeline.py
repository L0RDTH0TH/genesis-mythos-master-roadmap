#!/usr/bin/env python3
"""
Fetch last-commit (last-touched) date for each doc in Ingest/genesis-mythos and
Ingest/Genesis-Azgaar from GitHub API. Output: timeline CSV and optionally update frontmatter.
"""
import json
import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
INGEST = VAULT / "Ingest"
TIMELINE_OUT = VAULT / "Ingest" / "Genesis-Docs-Timeline.md"
API = "https://api.github.com/repos"

def ingest_path_to_repo_path(rel: str, repo_prefix: str) -> tuple[str, str, str]:
    """Convert e.g. genesis-mythos/docs--foo.md -> (owner/repo, branch, docs/foo.md)."""
    rel = rel.replace("\\", "/")
    if repo_prefix == "genesis-mythos":
        owner, repo, branch = "L0RDTH0TH", "genesis-mythos", "main"
    else:
        owner, repo, branch = "L0RDTH0TH", "Genesis-Azgaar", "master"
    # Strip prefix and filename: genesis-mythos/docs--SYSTEM_IMPLEMENTATIONS.md -> docs--SYSTEM_IMPLEMENTATIONS.md
    rest = rel[len(repo_prefix) + 1:] if rel.startswith(repo_prefix + "/") else rel
    # Replace -- with / for repo path
    repo_path = rest.replace("--", "/")
    return f"{owner}/{repo}", branch, repo_path

def fetch_last_commit_date(owner_repo: str, branch: str, path: str) -> str | None:
    url = f"{API}/{owner_repo}/commits?path={urllib.parse.quote(path)}&per_page=1"
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github.v3+json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read().decode())
            if data and isinstance(data, list) and len(data) > 0:
                commit = data[0]
                return commit.get("commit", {}).get("committer", {}).get("date")
    except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError, KeyError) as e:
        print(f"  skip {path}: {e}", file=sys.stderr)
    return None

def main():
    os.chdir(VAULT)
    rows = []
    seen_repo_paths = set()

    for repo_prefix in ("genesis-mythos", "Genesis-Azgaar"):
        root = INGEST / repo_prefix
        if not root.is_dir():
            continue
        for f in root.rglob("*"):
            if not f.is_file():
                continue
            if f.suffix.lower() not in (".md", ".txt"):
                continue
            rel = str(f.relative_to(INGEST))
            owner_repo, branch, repo_path = ingest_path_to_repo_path(rel, repo_prefix)
            key = (owner_repo, repo_path)
            if key in seen_repo_paths:
                continue
            seen_repo_paths.add(key)
            date = fetch_last_commit_date(owner_repo, branch, repo_path)
            if date:
                rows.append((rel, repo_path, owner_repo, date))
            # be nice to GitHub API
            import time
            time.sleep(0.3)

    # Sort by date descending (newest first)
    rows.sort(key=lambda r: r[3], reverse=True)

    # Write timeline note
    lines = [
        "# Genesis docs timeline (last touched in Git)",
        "",
        "Per-file **last commit date** from GitHub. Use for ordering / filtering.",
        "",
        "| Ingest path | Repo path | Repo | Last touched (UTC) |",
        "|-------------|-----------|------|---------------------|",
    ]
    for rel, repo_path, owner_repo, date in rows:
        lines.append(f"| `{rel}` | `{repo_path}` | {owner_repo} | {date} |")
    lines.extend(["", "---", f"*Generated; {len(rows)} files.*"])
    TIMELINE_OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {TIMELINE_OUT} ({len(rows)} rows)")

    # Write JSON for frontmatter updates
    json_out = VAULT / "Ingest" / "Genesis-Docs-Timeline.json"
    out_data = [{"ingest_path": r[0], "repo_path": r[1], "repo": r[2], "source_last_touched_at": r[3]} for r in rows]
    json_out.write_text(json.dumps(out_data, indent=2), encoding="utf-8")
    print(f"Wrote {json_out}")

if __name__ == "__main__":
    main()
