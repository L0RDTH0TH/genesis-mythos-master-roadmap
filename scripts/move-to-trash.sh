#!/usr/bin/env bash
# Move vault paths into .trash/<timestamp>/ and append TRASH-MANIFEST.log.
# Usage (from vault root): ./scripts/move-to-trash.sh <relative-or-absolute-path> [...]
# Does not use rm. Refuses paths outside vault root.

set -euo pipefail
VAULT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TRASH_ROOT="${VAULT_ROOT}/.trash"
STAMP="$(date +%Y%m%d-%H%M%S)"
BUCKET="${TRASH_ROOT}/${STAMP}"
MANIFEST="${TRASH_ROOT}/TRASH-MANIFEST.log"
ISO="$(date -Iseconds)"

if [[ $# -lt 1 ]]; then
  echo "usage: $0 <path> [path ...]" >&2
  exit 1
fi

mkdir -p "$BUCKET"

vault_resolve() {
  local p="$1"
  if [[ "$p" = /* ]]; then
    echo "$p"
  else
    echo "${VAULT_ROOT}/${p}"
  fi
}

for rel in "$@"; do
  src="$(vault_resolve "$rel")"
  src="$(cd "$(dirname "$src")" && pwd)/$(basename "$src")"
  case "$src" in
    "${VAULT_ROOT}"|"${VAULT_ROOT}/")
      echo "move-to-trash: refusing vault root: $src" >&2
      exit 2
      ;;
  esac
  if [[ "${src}" != "${VAULT_ROOT}"* ]]; then
    echo "move-to-trash: path outside vault: $src" >&2
    exit 3
  fi
  if [[ ! -e "$src" ]]; then
    echo "move-to-trash: not found: $src" >&2
    exit 4
  fi
  rel_under="${src#"${VAULT_ROOT}/"}"
  dest_parent="${BUCKET}/$(dirname "$rel_under")"
  mkdir -p "$dest_parent"
  dest="${BUCKET}/${rel_under}"
  mv "$src" "$dest"
  echo "${ISO} | ${rel_under} -> .trash/${STAMP}/${rel_under}" >> "$MANIFEST"
  echo "moved: ${rel_under} -> .trash/${STAMP}/${rel_under}"
done
