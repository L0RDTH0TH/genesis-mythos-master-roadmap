#!/usr/bin/env bash
# Preflight: snapshot godot PQ → dry-run append_entries with heredoc (no PQ writes).
# Usage: from vault root: ./scripts/eat_queue_core/examples/preflight_godot_append_dryrun.sh
set -euo pipefail
cd "$(dirname "$0")/../../.."
export PYTHONPATH=.
SNAP="$(mktemp /tmp/godot-pq-snapshot-XXXXXX.json)"
cleanup() { rm -f "$SNAP"; }
trap cleanup EXIT
python3 -m scripts.eat_queue_core.harness snapshot --vault-root . --lane godot >"$SNAP"
python3 -m scripts.eat_queue_core.harness append_entries \
  --vault-root . \
  --lane godot \
  --dry-run \
  --require-snapshot-json "$SNAP" <<'EOF'
{"id":"preflight-dryrun-1","mode":"HANDOFF_AUDIT_REPAIR","params":{"origin_request_id":"preflight-o","user_guidance":"harness preflight sample"}}
EOF
echo "preflight_godot_append_dryrun: ok"
