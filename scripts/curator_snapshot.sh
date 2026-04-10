#!/usr/bin/env bash
# Mirror vault -> private export checkout, then commit + push Curator main.
# Usage: from vault root: ./scripts/curator_snapshot.sh [short task summary]
# Optional env override: CURATOR_EXPORT_ROOT=/abs/path/to/private-export

set -euo pipefail
VAULT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
EXPORT_ROOT_DEFAULT="/home/darth/Documents/gmm-curator-export"
EXPORT_ROOT="${CURATOR_EXPORT_ROOT:-$EXPORT_ROOT_DEFAULT}"
cd "$VAULT_ROOT"

auth_fail() {
  local remote="$1"
  echo "curator_snapshot: auth/preflight failed for remote '$remote' (non-interactive)" >&2
  echo "curator_snapshot: run a manual git auth step in '$EXPORT_ROOT' first, then retry" >&2
  exit 1
}

if [[ ! -d "$EXPORT_ROOT" ]]; then
  echo "curator_snapshot: private export checkout missing: $EXPORT_ROOT" >&2
  echo "curator_snapshot: create it first (git clone Curator into that path)" >&2
  exit 1
fi
if [[ "$EXPORT_ROOT" == "$VAULT_ROOT" ]]; then
  echo "curator_snapshot: export root must not equal vault root" >&2
  exit 1
fi
if ! git -C "$EXPORT_ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "curator_snapshot: no git repository at export root: $EXPORT_ROOT" >&2
  exit 1
fi

# Mirror vault into private export checkout.
rsync -a --delete \
  --exclude '.git/' \
  --exclude '.obsidian/workspace*' \
  "$VAULT_ROOT/" "$EXPORT_ROOT/"

cd "$EXPORT_ROOT"

target_branch="main"
if git show-ref --verify --quiet refs/heads/main; then
  target_branch="main"
elif git show-ref --verify --quiet refs/heads/master; then
  target_branch="master"
fi
git switch "$target_branch" >/dev/null 2>&1 || true

SUMMARY="${1:-curator snapshot}"
TS="$(date -Iseconds)"
MSG="auto: ${TS} — Cursor task: ${SUMMARY}"

# Prefer targeted staging: tracked updates + untracked (path-safe)
stage_ok=true
git add -u || stage_ok=false
while IFS= read -r -d '' f; do
  [[ -n "$f" ]] && git add -- "$f" || stage_ok=false
done < <(git ls-files -z --others --exclude-standard 2>/dev/null || true)

if [[ "$stage_ok" != true ]]; then
  echo "curator_snapshot: targeted staging had errors; trying git add -A" >&2
  git add -A
fi

if git diff --cached --quiet; then
  echo "curator_snapshot: nothing to commit after staging"
  exit 0
fi

git commit -m "$MSG"

REMOTE="curator"
if ! git remote get-url "$REMOTE" >/dev/null 2>&1; then
  REMOTE="origin"
  echo "curator_snapshot: remote 'curator' missing; using 'origin'" >&2
fi

# Fail fast on missing credentials; never hang waiting for prompt in automation.
if ! GIT_TERMINAL_PROMPT=0 git ls-remote "$REMOTE" >/dev/null 2>&1; then
  auth_fail "$REMOTE"
fi

if ! GIT_TERMINAL_PROMPT=0 git push -u "$REMOTE" "$target_branch"; then
  echo "curator_snapshot: git push $REMOTE $target_branch failed" >&2
  exit 1
fi

echo "curator_snapshot: pushed to $REMOTE $target_branch"
