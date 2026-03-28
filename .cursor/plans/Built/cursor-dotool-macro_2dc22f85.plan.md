---
name: cursor-dotool-macro
overview: Finalize a dotool-based macro on Linux that uses a calibrated screen position to focus the Cursor text input, paste from the clipboard, and press Enter repeatedly.
todos: []
isProject: false
---

## Goal

Create a reliable dotool-based macro workflow that:

- Uses a one-time calibration script to record the Cursor text field coordinates
- Uses a main macro script that moves the mouse to those coordinates, clicks to focus, pastes the clipboard, presses Enter, and optionally repeats with delays
- Is easy to tweak (delays, repeat count) and bind to a desktop hotkey

## Steps

- **Review draft scripts**
  - Reuse your existing concept: a calibration script that stores `X` and `Y` in a config file and a main script that sources that config.
  - Ensure we assume dotool is already installed and working (as in your draft).
- **Design calibration script behavior**
  - Keep it simple: you manually position the mouse over the Cursor input, then press Enter in the terminal to capture.
  - For now, avoid dependencies like `slop` or `xdotool`; instead, call dotool’s `getmouselocation` equivalent if available or rely on a very small helper, and if not available, keep your manual X/Y input as a fallback.
  - Write the resulting coordinates into a small config file under your home directory (e.g. `~/.cursor-macro-pos` with `X=...` and `Y=...`).
- **Define the main macro script**
  - Read `X` and `Y` from the config file and validate they exist.
  - Optionally accept a `REPEATS` argument (default N) to control how many times to run.
  - For each iteration:
    - Move mouse to `X Y` and left-click to focus the Cursor field.
    - Send `Ctrl+Shift+V` via dotool to paste from the clipboard.
    - Wait a short paste delay.
    - Send `Return` key via dotool to submit.
    - Wait a longer delay to let Cursor respond before the next iteration.
  - Print clear messages in the terminal describing what it’s doing and how to abort.
- **Tuning and robustness**
  - Expose key knobs as top-of-file variables: paste delay, post-Enter delay, default repeats.
  - Document that moving/resizing the Cursor window requires re-running calibration.
  - Optionally add a quick pre-flight check that dotool is available and that the config file exists.
- **Shortcut / integration notes**
  - Describe how to bind the main script to a global shortcut in common environments (e.g. GNOME/KDE custom keyboard shortcuts) while keeping the script itself desktop-agnostic.
  - Suggest a workflow: calibrate occasionally, then trigger the macro from a hotkey whenever you want to queue N copies of the current clipboard into Cursor.

## Todos

- v
- **macro-script**: Implement the main dotool macro that reads calibration, focuses the field, pastes, and presses Enter repeatedly with tunable delays.
- **usage-docs**: Add minimal inline comments and usage examples (calibrate once, then run macro with optional repeat count and/or bind to desktop hotkey).

