#!/usr/bin/env bash
# Manual operator backup sweep:
# 1) Run curator snapshot (vault -> private export -> Curator push)
# 2) Push all branches/tags for private export checkout
# 3) Push all branches/tags for public export checkout
#
# Usage:
#   ./scripts/backup_all_githubs.sh ["short summary"]
# Optional env overrides:
#   CURATOR_EXPORT_ROOT=/abs/path
#   PUBLIC_EXPORT_ROOT=/abs/path

set -euo pipefail

VAULT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CURATOR_EXPORT_ROOT="${CURATOR_EXPORT_ROOT:-/home/darth/Documents/gmm-curator-export}"
PUBLIC_EXPORT_ROOT="${PUBLIC_EXPORT_ROOT:-/home/darth/Documents/gmm-roadmap-export}"
SUMMARY="${1:-backup dir now}"

ensure_git_checkout() {
  local path="$1"
  local label="$2"
  if [[ ! -d "$path" ]]; then
    echo "backup_all_githubs: missing ${label} checkout: $path" >&2
    exit 1
  fi
  if ! git -C "$path" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "backup_all_githubs: ${label} is not a git checkout: $path" >&2
    exit 1
  fi
}

resolve_remote() {
  local path="$1"
  if git -C "$path" remote get-url curator >/dev/null 2>&1; then
    echo "curator"
    return
  fi
  if git -C "$path" remote get-url origin >/dev/null 2>&1; then
    echo "origin"
    return
  fi
  echo ""
}

require_auth_ready() {
  local path="$1"
  local remote="$2"
  local label="$3"
  if ! GIT_TERMINAL_PROMPT=0 git -C "$path" ls-remote "$remote" >/dev/null 2>&1; then
    echo "backup_all_githubs: auth/preflight failed for ${label} remote '${remote}' (non-interactive)" >&2
    echo "backup_all_githubs: complete manual git auth in '$path', then retry" >&2
    exit 1
  fi
}

push_all_refs() {
  local path="$1"
  local label="$2"
  local remote
  remote="$(resolve_remote "$path")"
  if [[ -z "$remote" ]]; then
    echo "backup_all_githubs: ${label} has no 'curator' or 'origin' remote" >&2
    exit 1
  fi
  require_auth_ready "$path" "$remote" "$label"
  echo "backup_all_githubs: pushing all branches for ${label} via remote '${remote}'"
  GIT_TERMINAL_PROMPT=0 git -C "$path" push "$remote" --all
  echo "backup_all_githubs: pushing all tags for ${label} via remote '${remote}'"
  GIT_TERMINAL_PROMPT=0 git -C "$path" push "$remote" --tags
}

ensure_git_checkout "$CURATOR_EXPORT_ROOT" "private"
ensure_git_checkout "$PUBLIC_EXPORT_ROOT" "public"

echo "backup_all_githubs: running curator snapshot"
"$VAULT_ROOT/scripts/curator_snapshot.sh" "$SUMMARY"

push_all_refs "$CURATOR_EXPORT_ROOT" "private"
push_all_refs "$PUBLIC_EXPORT_ROOT" "public"

echo "backup_all_githubs: complete"
