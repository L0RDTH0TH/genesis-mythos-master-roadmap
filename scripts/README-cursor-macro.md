# Cursor queue macro (dotool)

Coordinate-based macro that moves the mouse to the Cursor prompt field, pastes from the clipboard, and presses Enter — repeatable N times. Uses **dotool** (Wayland/X11). Config is stored in `~/.cursor-macro-pos` (outside the repo).

## Requirements

- **dotool** installed and in PATH; **dotoold** running; user in `input` group if required by your setup.

## One-time setup

1. **Calibrate** (run once, or after moving/resizing the Cursor window):
   ```bash
   ./scripts/calibrate-cursor.sh
   ```
   Position the mouse over the center of the Cursor text input (chat or Composer), press Enter in the terminal, then enter X and Y when prompted (e.g. from `slop -f '%x %y'`, or your DE’s coordinate tool).

2. **Run the macro** from the repo:
   ```bash
   ./scripts/cursor-queue-prompts.sh          # default repeats (5)
   ./scripts/cursor-queue-prompts.sh 12        # 12 times
   ```

## Bind to a hotkey

Use the **full path** to the macro script so it works from any working directory.

- **GNOME**: Settings → Keyboard → Keyboard Shortcuts → Custom Shortcuts → Add  
  Command: `/home/YOUR_USERNAME/Documents/Second-Brain/scripts/cursor-queue-prompts.sh 8`  
  Shortcut: e.g. `Ctrl+Alt+Q`
- **KDE**: System Settings → Shortcuts → Custom Shortcuts → New → Global Shortcut → Command/URL
- **Hyprland / Sway / i3**: e.g. `bind = SUPER+SHIFT+Q, exec, /home/YOUR_USERNAME/Documents/Second-Brain/scripts/cursor-queue-prompts.sh 5`

## Workflow

1. Calibrate once (or after changing Cursor window position/size).
2. Copy your prompt to the clipboard.
3. Trigger the macro (hotkey or terminal); it will click the saved position, paste (Ctrl+Shift+V), press Enter, then repeat after delays.
4. Adjust `PASTE_DELAY`, `ENTER_DELAY`, and `DEFAULT_REPEATS` at the top of `cursor-queue-prompts.sh` if needed.

## Files

| File | Purpose |
|------|--------|
| `scripts/calibrate-cursor.sh` | Save X,Y to `~/.cursor-macro-pos` |
| `scripts/cursor-queue-prompts.sh` | Main macro: move → click → paste → Enter × N |

Config file `~/.cursor-macro-pos` is in your home directory and is not version-controlled.
