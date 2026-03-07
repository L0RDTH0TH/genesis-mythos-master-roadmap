---
created: 2026-02-26
tags:
  - watcher
  - second-brain
  - setup
---

# Watcher Plugin — Usage & Test Guide

Quick setup, console verification, and mobile–laptop test flow for the Watcher plugin. **Queue-only flow**: all mobile triggers append to `3-Resources/prompt-queue.jsonl`; Cursor is run manually and the single entry prompt is **EAT-QUEUE**.

## Queue-only flow (current)

- **Mobile / Obsidian**: Ingest, Organize, Distill, Express, Archive (one-tap or Prompt Modal Send) **only** append to `3-Resources/prompt-queue.jsonl` and show "Added to queue (requestId). Pending: N". No signal file write and no Cursor bridge for these triggers.
- **Cursor**: Open the vault in Cursor and run **EAT-QUEUE** (or "Process queue", or paste the EAT-CACHE payload). The agent reads the queue, skips entries marked `queue_failed`, dedupes and sorts by pipeline order, dispatches each entry to the right pipeline (INGEST, DISTILL, EXPRESS, ARCHIVE, ORGANIZE), appends one line per request to `3-Resources/Watcher-Result.md`, and **clears only passed entries** — failed/skipped entries are written back with `queue_failed: true` and are skipped on the next EAT-QUEUE run.
- **Optional**: In Obsidian, **"EAT-CACHE (copy queue to clipboard)"** copies the queue as YAML so you can paste into Cursor; **"Clear queue"** wipes the whole queue manually.

## Quick setup

1. **Plugin files**: Ensure `manifest.json`, `main.js`, and `styles.css` are in `.obsidian/plugins/watcher/`.
2. **Enable**: Obsidian → Settings → Community plugins → enable **Watcher**.
3. **Toolbar (optional)**: Add Watcher commands (Ingest, Organize, Distill, Express, Archive, Prompt Modal) to the mobile toolbar for one-tap.

---

## Opening the console and expected log lines

- **Desktop**: Reload Obsidian, then press **Ctrl+Shift+I** (or Cmd+Option+I on Mac) → **Console** tab.
- **Filter**: In the console filter box, type `[Watcher]` to see only plugin logs.

| What happened | Expected console lines (filter by `[Watcher]`) |
|----------------|---------------------------------------------|
| Plugin loads | `[Watcher] Plugin loaded – wiring active` → `[Watcher] File guard initialized` → `[Watcher] Watched file ensured / protected` (no polling; queue-only flow) |
| Trigger Ingest clicked | `[Watcher] Trigger: Ingest mode fired (one-tap)` → `[Watcher] Appended to queue – requestId:` |
| Trigger Distill/Express/Organize/Archive | Same: append to queue, then Notice "Added to queue (...). Pending: N" |
| Ribbon / Open Modal | `[Watcher] Ribbon trigger: Open modal` or `[Watcher] Trigger: Open Prompt Modal` |
| Modal Send | Append to queue only; Notice "Added to queue (...). Pending: N" |

---

## Test minimal wiring (same device)

1. Reload Obsidian (or restart).
2. Open DevTools → **Console** (Ctrl+Shift+I).
3. **Trigger Ingest**: Command palette → **"Watcher: Ingest"**.  
   Expect: `[Watcher] Trigger: Ingest mode fired...` → `[Watcher] Appended to queue – requestId:` and Notice "Added to queue (requestId). Pending: N".
4. **Modal**: Click ribbon or run **"Watcher: Prompt Modal"** → pick a mode, click Send. Expect append to queue and Notice "Added to queue (...). Pending: N".
5. **EAT-QUEUE**: Open the vault in Cursor and say **EAT-QUEUE**. The agent reads `3-Resources/prompt-queue.jsonl`, processes each entry by mode, appends to Watcher-Result, and clears only passed entries (failed/skipped get `queue_failed: true` and stay for visibility; next EAT-QUEUE skips them).
6. **Clear queue (optional)**: In Obsidian, run **"Watcher: Clear queue"** to wipe the queue file manually.

---

## Watcher-Result line format (manual simulation)

Append **exactly one line** to `3-Resources/Watcher-Result.md`:

```
requestId: <your-requestId> | status: success | message: "done" | trace: "ok" | completed: <ISO8601>
```

- **requestId**: Use the value from the Trigger Ingest or modal Send (e.g. from the Notice or from `Watcher-Signal.md` last line).
- **status**: `success` or `failure`.
- **message**: Short summary in double quotes; escape any internal `"` as `\"`.
- **trace**: For failures use full error or log excerpt; for success can be `"ok"` or `""`. Escape internal `"` as `\"`.
- **completed**: ISO 8601 timestamp when the run finished (e.g. `2026-02-27T12:34:56.789Z`). Used for lag estimation: compare with the timestamp on the matching line in `Watcher-Signal.md` (triggered at). See [[Watcher-Timing]].

Example:

```
requestId: m5x2k8abc123 | status: success | message: "Ingest completed" | trace: "" | completed: 2026-02-27T12:35:02.100Z
```

---

## Test mobile → laptop flow

- **Mobile**: In Obsidian (mobile app), run **"Watcher: Ingest"** (or Distill, Express, Organize, Archive, or open the modal and Send). Each action appends to `3-Resources/prompt-queue.jsonl`; your vault syncs (Obsidian Sync / cloud / git).
- **Laptop**: Open the same vault in Cursor and run **EAT-QUEUE**. The agent reads the queue, processes each entry by mode, appends one line per request to Watcher-Result, and clears only passed entries (failed/skipped get `queue_failed: true`). See `.cursor/rules/always/watcher-result-append.mdc` for the result format.
- **Sync back**: After sync, on mobile or laptop Obsidian, the queue file and Watcher-Result are updated. No completion popup in the queue-only flow; check Watcher-Result.md for outcomes.
 
## Optional desktop deeplink helper (ydotool)

On Linux desktops you can also trigger Cursor directly via a shell command that opens a Cursor deeplink and auto-confirms the \"Run with AI\" dialog using `ydotool`:

- **Helper script**: `~/bin/cursor-deeplink-auto-archive.sh`  
  - Usage: `cursor-deeplink-auto-archive.sh [-d seconds] "cursor://anysphere.cursor-deeplink/prompt?text=..."`  
  - Environment: set `CURSOR_DEEPLINK_DELAY` to control the default delay before pressing Enter (fallback is 3s).
  - Requirements: `xdg-open`, `ydotool`, and the `ydotoold` daemon running with permission to send key events.
- **Example deeplinks** (URL-encoded prompt text):
  - Ingest: `cursor://anysphere.cursor-deeplink/prompt?text=INGEST+MODE+%E2%80%93+process+captures`
  - Distill: `cursor://anysphere.cursor-deeplink/prompt?text=DISTILL+MODE+%E2%80%93+safe+batch+autopilot`
  - Express: `cursor://anysphere.cursor-deeplink/prompt?text=EXPRESS+MODE+%E2%80%93+safe+batch+autopilot`
  - Organize: `cursor://anysphere.cursor-deeplink/prompt?text=ORGANIZE+MODE+%E2%80%93+safe+batch+autopilot`
  - Archive: `cursor://anysphere.cursor-deeplink/prompt?text=ARCHIVE+MODE+%E2%80%93+safe+batch+autopilot`

You can wire these into an external-commands plugin (e.g. Shell commands) so that each autopilot mode has a corresponding Obsidian command on desktop. Mobile uses the Watcher commands, which append to `prompt-queue.jsonl` and do not depend on `ydotool`.

**Summary (queue-only flow):**

- **Queue path**: Mobile triggers → append to `3-Resources/prompt-queue.jsonl` → sync → laptop runs **EAT-QUEUE** in Cursor to process the queue.
- **Result path**: Cursor runs EAT-QUEUE → process each entry by mode → append to `Watcher-Result.md` → clear passed entries only (failed/skipped get `queue_failed: true` and stay in queue, skipped on next run).
