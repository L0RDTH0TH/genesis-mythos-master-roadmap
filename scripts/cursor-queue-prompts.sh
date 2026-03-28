#!/bin/bash
# Cursor macro — Ctrl+V → Enter → wait → repeat (testing / queue simulation).
#
# --- Two ways to run ---
# 1) From terminal: run the script, use the countdown to click Cursor's input.
#    Override wait:  START_DELAY=0 ./scripts/cursor-queue-prompts.sh
# 2) Global hotkey (no terminal focus): bind a shortcut to this script's full path.
#    Example (GNOME): Settings → Keyboard → Custom Shortcut
#      Command: /home/USER/Documents/Second-Brain/scripts/cursor-queue-prompts.sh 1
#    Focus the chat/composer first, press the hotkey; set START_DELAY=0 in the command
#    if the hotkey should paste immediately: env START_DELAY=0 /path/to/script.sh 1
#
# Requires: dotool + dotoold; clipboard holds the text to send.

# ====================== TUNABLE SETTINGS (edit these) ======================
: "${START_DELAY:=5}" # seconds before first paste (time to focus Cursor). Env overrides.
INTERVAL_SECONDS=2    # seconds between cycles (after Enter, before next paste)
PASTE_SETTLE=0.5     # brief pause after paste before Enter
# Paste: use keydown/keyup — chord "ctrl+v" often resolves to plain "v" on some dotool builds
# (there is no bare "ctrl" key; see dotool --list-keys → leftctrl).
# Plain-text paste (Ctrl+Shift+V): set PASTE_PLAIN_TEXT=1
: "${PASTE_PLAIN_TEXT:=0}"
: "${SUBMIT_KEY:=enter}"   # Linux key name; avoid "Return" (often rejected per layout)
# After keydown modifier(s), wait before `key v` so the WM sees Ctrl before V (avoids rare plain "v").
: "${MODIFIER_SETTLE:=0.06}"
# Optional pause after `key v` before keyup (release ordering); 0 to disable
: "${AFTER_V_SETTLE:=0.03}"
DEFAULT_REPEATS=15    # iterations if no argument
# ===========================================================================

if ! command -v dotool >/dev/null 2>&1; then
  echo "Error: dotool not found. Install it and ensure dotoold is running."
  exit 1
fi

# Send Ctrl+V (or Ctrl+Shift+V) via explicit modifier keys; one dotool session per paste.
# Shell `sleep` between writes spaces events so Ctrl is latched before V (see MODIFIER_SETTLE).
dotool_paste() {
  if [ "$PASTE_PLAIN_TEXT" = 1 ]; then
    {
      echo keydown leftctrl
      echo keydown leftshift
      sleep "$MODIFIER_SETTLE"
      echo key v
      sleep "$AFTER_V_SETTLE"
      echo keyup leftshift
      echo keyup leftctrl
    } | dotool
  else
    {
      echo keydown leftctrl
      sleep "$MODIFIER_SETTLE"
      echo key v
      sleep "$AFTER_V_SETTLE"
      echo keyup leftctrl
    } | dotool
  fi
}

REPEATS=${1:-$DEFAULT_REPEATS}

echo "=== Cursor paste macro ==="
echo "Cycles: $REPEATS | gap between cycles: ${INTERVAL_SECONDS}s"
if [ "${START_DELAY}" -gt 0 ] 2>/dev/null; then
  echo "First paste in ${START_DELAY}s — switch to Cursor and click the input now."
  echo "Clipboard should hold your text. Ctrl+C to abort."
  echo ""
  left=$START_DELAY
  while [ "$left" -gt 0 ]; do
    printf '\r  Starting in %2d s ' "$left"
    sleep 1
    left=$((left - 1))
  done
  printf '\r  Go!                    \n'
else
  echo "START_DELAY=0 — pasting immediately."
  echo "Clipboard should hold your text. Ctrl+C to abort."
  echo ""
fi

for ((i=1; i<=REPEATS; i++)); do
  echo "→ $i/$REPEATS : paste → Enter → sleep ${INTERVAL_SECONDS}s"

  dotool_paste
  sleep "$PASTE_SETTLE"
  echo "key ${SUBMIT_KEY}" | dotool

  if [ "$i" -lt "$REPEATS" ]; then
    sleep "$INTERVAL_SECONDS"
  fi
done

echo "✅ Finished ($REPEATS cycles)."
