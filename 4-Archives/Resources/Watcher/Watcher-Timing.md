---
created: 2026-02-27
tags:
  - watcher
  - timing
  - lag
---

# Watcher timing and lag estimation

Timestamps captured by the Watcher flow so you can estimate lag between **trigger** and **execute** (and optional stages in between).

## What is captured today

| Stage | Where | Format | Notes |
|--------|--------|--------|--------|
| **Triggered at** | `3-Resources/Watcher-Signal.md` | Each line starts with `[ISO8601]`, e.g. `[2026-02-27T01:35:59.798Z]` | When the plugin wrote the signal (mobile or desktop). |
| **Seen at (synced to laptop)** | `3-Resources/Watcher-Timing-Log.md` | `[<ISO8601>] requestId: <id> \| event: seen` | When the laptop’s Watcher detected the new signal — so the file had synced and the plugin saw it. |
| **Cursor complete at** | `3-Resources/Watcher-Result.md` | Each result line includes ` \| completed: <ISO8601>` | When the Cursor run finished and the agent appended the result. |

**End-to-end lag (trigger → complete):**  
Match lines by `requestId`, then subtract the Signal line timestamp from the Result line `completed` value. That gives you total time from “user triggered” to “run finished.”

## What is not captured in the vault (yet)

- **Cursor launch at** — When the bridge or script ran `xdg-open` / opened the deeplink. Not written to a file.

To estimate **sync lag** (trigger → seen) or **launch lag** (seen → launch), you’d need one or both of:

- **Seen at:** Plugin (or a wrapper) appending a line with timestamp to a log file when it detects a new signal (e.g. `Watcher-Timing-Log.md` or a dedicated log).
- **Cursor launch at:** The bridge or `cursor-deeplink-auto-archive.sh` (or AutoKey) writing a timestamp when it invokes the deeplink (e.g. to the same log file or a small “last launch” file).

## Optional: logging “launch at”

The plugin already appends **seen at** to `3-Resources/Watcher-Timing-Log.md` when it detects a new signal (event: `seen`). That timestamp = “message had synced to this device and the plugin saw it.”

- **Launch at:** To get the moment the deeplink was opened, add logging in the code that calls `window.open(uri)` (or in the shell script that runs `xdg-open`): append a line to the same file: `[<ISO8601>] requestId: <id> | event: launch`.

Then you can compute: **trigger → seen** (sync + poll interval), **seen → launch** (bridge/script delay), **launch → completed** (Cursor run duration).

## Result line format (reference)

Each result line in `Watcher-Result.md` should look like:

```
requestId: <id> | status: success|failure | message: "..." | trace: "..." | completed: 2026-02-27T12:34:56.789Z
```

The plugin parses `requestId` and `status`; `completed` is for lag estimation and display (e.g. in a popup or Dataview).
