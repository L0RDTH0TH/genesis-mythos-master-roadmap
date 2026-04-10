#!/bin/bash
# Cursor macro calibration - run once to save the prompt field coordinates

CONFIG_FILE="$HOME/.cursor-macro-pos"

echo "=== Cursor Macro Calibration ==="
echo ""
echo "1. Make sure Cursor is open and visible."
echo "2. Move your mouse to the EXACT CENTER of the text input field"
echo "   (chat box, Composer input, or wherever you type prompts)."
echo ""
echo "When the mouse is perfectly positioned, press ENTER in this terminal."

read -r dummy

echo ""
echo "Since dotool cannot query mouse position, please enter the coordinates manually."
echo "(Quick tip: most people use 'slop' once, or a screenshot + ruler, or their DE's debug overlay.)"
echo ""

read -rp "Enter X coordinate (pixels): " X
read -rp "Enter Y coordinate (pixels): " Y

# Basic validation
if ! [[ "$X" =~ ^[0-9]+$ ]] || ! [[ "$Y" =~ ^[0-9]+$ ]]; then
  echo "Error: Coordinates must be numbers. Aborting."
  exit 1
fi

cat > "$CONFIG_FILE" << EOF
# Cursor macro saved position - generated $(date)
X=$X
Y=$Y
EOF

echo ""
echo "✅ Saved! Position: $X, $Y"
echo "Config file: $CONFIG_FILE"
echo "You can now run the main macro."
echo "(Re-run this script if you move or resize the Cursor window.)"
