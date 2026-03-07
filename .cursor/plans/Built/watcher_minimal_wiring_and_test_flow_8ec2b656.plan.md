---
name: Watcher minimal wiring and test flow
overview: Enhance the existing Watcher plugin with consistent "Watcher:" command names, heavy console logging at every step, async writeSignal for correct ordering, and document the user-facing trigger + mobile-to-laptop test flow without changing file guard, CSS, or Cursor rules.
todos: []
isProject: false
---

# Watcher minimal wiring and mobile–laptop test flow

## Current state

- **Plugin**: [.obsidian/plugins/watcher/main.js](.obsidian/plugins/watcher/main.js) (v3) — file guard, signal write, bridge (URI → clipboard → request file), 10s cross-device polling, completion wait with single `_pollInterval`.
- **Gaps**: No console logs; command names are "Open Prompt Modal" / "Trigger Ingest" (no "Watcher:" prefix); `writeSignal` returns immediately while the file write is async (so "signal written" ordering is unclear); completion polling and bridge have minimal visibility.
- **Out of scope**: [.obsidian/plugins/watcher/manifest.json](.obsidian/plugins/watcher/manifest.json), [.obsidian/plugins/watcher/styles.css](.obsidian/plugins/watcher/styles.css), and all Cursor rules stay as-is.

## 1. Enhance main.js only

### 1.1 Bootstrap and file guard

- In `onload()`: log `[Watcher] Plugin loaded – wiring active` at start.
- After `await this.ensureFileGuard()`: log `[Watcher] File guard initialized`.
- In `ensureFileGuard()`: after ensuring folder and watched file, log `[Watcher] Watched file ensured / protected` (and keep existing `console.warn` on errors).

### 1.2 Commands and ribbon (triggerability + naming)

- **Command ids/names** (for discoverability, especially mobile):
  - `open-watcher-modal` / **"Watcher: Open Prompt Modal"** — callback: log `[Watcher] Trigger: Open Prompt Modal`, then open `WatcherModal`.
  - `trigger-ingest` / **"Watcher: Trigger Ingest"** — callback: log `[Watcher] Trigger: Ingest mode fired (one-tap)`, then run ingest flow below.
- **Ribbon**: Keep eye icon; tooltip e.g. "Watcher Modal". On click: log `[Watcher] Ribbon trigger: Open modal`, then open modal.
- After registering the 10s interval: log `[Watcher] Polling interval started (10s)`.

### 1.3 writeSignal (async + logging)

- Make **writeSignal async**: perform the vault read/create folder + append write inside the function and **await** the write; return `{ requestId, fullPrompt }` after the write completes.
- Logging:
  - On entry: `[Watcher] writeSignal called – mode: ..., prompt: <first 100 chars>...`
  - After generating `requestId`: `[Watcher] Generated requestId: ...`
  - After successful write: `[Watcher] Signal appended successfully`
- **Call sites**: In the **Trigger Ingest** command, use `await this.writeSignal("INGEST MODE", fullPrompt)` and then log `[Watcher] Ingest signal written – requestId: ${requestId}`. In **WatcherModal** Send button, use `await this.plugin.writeSignal(...)` and keep the existing Notice; optionally log there too.

### 1.4 Trigger Ingest flow (branch logging)

After `await this.writeSignal(...)`:

- If `this.cursorBridgeEnabled`: log `[Watcher] Bridge enabled – attempting dispatch`; then `const success = await this.attemptCursorBridge(...)`; if success log `[Watcher] Dispatch success – starting completion polling`, else `[Watcher] Dispatch failed – no polling`; if success call `this.startCompletionWait(...)`.
- Else: log `[Watcher] Bridge disabled – signal only`.

(Keep existing Notice for "signal sent".)

### 1.5 checkForSignals

- When a new signal is detected (id !== this.lastRequestId): log `[Watcher] New signal detected via polling:`, and the last line or requestId (for debugging). Keep existing Notice.

### 1.6 attemptCursorBridge (step-by-step logs)

- If bridge disabled: return false (no new logs).
- On first use: keep or adjust Notice (e.g. "Cursor bridge ACTIVE"); log `[Watcher] Bridge first use – notice shown`.
- Log `[Watcher] Bridge attempt started – requestId:`, requestId.
- **URI**: Log `[Watcher] Trying URI:`, `<uri>` (optionally truncated if very long). On `window.open` success: log `[Watcher] URI opened – assuming success`; on catch: log `[Watcher] URI failed:`, err.message.
- **Clipboard fallback**: On success log `[Watcher] Clipboard fallback: prompt copied`; on catch log `[Watcher] Clipboard failed:`, err.message.
- **Request file fallback**: On success log `[Watcher] Request file created as fallback`; on final failure log `[Watcher] All bridge methods failed:`, err.

**URI format**: Current code uses `cursor://default?prompt=...`. The user snippet used `cursor://anysphere.cursor-deeplink/prompt?text=...`. Keep the current URI unless you have Cursor docs indicating otherwise; add a short code comment that the scheme can be switched for Cursor compatibility if needed.

### 1.7 startCompletionWait (polling visibility)

- At start: log `[Watcher] Starting completion wait – requestId: ${requestId}, timeout 15min`.
- Inside the poll callback (every 15s): log `[Watcher] Polling result file for ${requestId}... (${Math.round((Date.now() - start)/1000)}s elapsed)`.
- When a matching result line is found: clear interval, then log `[Watcher] Completion detected:`, status; then call callback (which shows popup).
- On timeout: log `[Watcher] Timeout reached – no completion signal`; then call callback with timeout.

### 1.8 showCompletionPopup

- At start: log `[Watcher] Showing completion popup – status: ..., trace: <first 200 chars>...` (or "none" if no trace). Then open the existing CompletionPopupModal / Notice as today.

### 1.9 Modal Send button (await writeSignal)

- In `WatcherModal`, the Send button handler must **await** `this.plugin.writeSignal(mode.preset, fullPrompt)` so the signal is written before the Notice and before any bridge/polling. Add `async` to the click handler and `await` the writeSignal call.

## 2. User-facing exposure and mobile–laptop test flow

**Goal**: Expose the user side clearly and give repeatable steps to confirm communication from mobile to laptop (and back via result).

### 2.1 What the user sees (no code change)

- **Quick setup**: Ensure `manifest.json`, `main.js`, `styles.css` are in `.obsidian/plugins/watcher/`; enable the plugin in Obsidian (Community plugins). Add commands to toolbar if desired, especially **"Watcher: Trigger Ingest"** for one-tap on mobile.
- **Bridge**: `cursorBridgeEnabled` remains `false` by default; set to `true` in code only when testing the Cursor hand-off (e.g. on laptop).

### 2.2 Testing minimal wiring (same device)

1. Reload Obsidian (or restart).
2. Open DevTools (Ctrl+Shift+I) → Console.
3. **Trigger Ingest**: Command palette → "Watcher: Trigger Ingest". Expect console: `[Watcher] Trigger: Ingest mode fired...` → `writeSignal...` → `Generated requestId:` → `Signal appended successfully` → `Ingest signal written – requestId: ...` → `Bridge disabled – signal only`.
4. **Modal**: Ribbon or "Watcher: Open Prompt Modal" → send a mode. Expect logs for writeSignal and (if bridge enabled) bridge + polling.
5. **Bridge test**: Set `cursorBridgeEnabled = true`, reload, trigger again. Expect URI log and Cursor opening if the app is installed.
6. **Completion simulation**: Manually append to `3-Resources/Watcher-Result.md` one line:
  - `requestId: <requestId-from-step-3> | status: success | message: "done" | trace: "ok"`
  - With bridge enabled and completion wait running, polling should detect it and show the popup (and log "Completion detected: success").

### 2.3 Mobile → laptop flow (test communication)

- **Mobile**: In Obsidian (mobile app), run **"Watcher: Trigger Ingest"** (or open modal and send). Signal is written to `3-Resources/Watcher-Signal.md`; vault syncs (Obsidian Sync / cloud/git).
- **Laptop**: Open the same vault in Obsidian; optionally open `Watcher-Signal.md` and copy the last line’s prompt, or use Cursor there with that prompt. Run the Cursor pipeline (e.g. INGEST MODE). When done, Cursor (or the user) appends to `3-Resources/Watcher-Result.md` per [watcher-result-append.mdc](.cursor/rules/always/watcher-result-append.mdc).
- **Sync back**: After sync, on mobile (or laptop) Obsidian, the 10s polling will see the new result line and can show the completion popup (if completion wait was started on that device—e.g. if bridge was used on laptop after reading the signal). So:
  - **Signal path**: Mobile triggers → signal file written → sync → laptop sees signal (and can run Cursor).
  - **Result path**: Laptop runs Cursor → result appended → sync → any device with Obsidian and polling sees result; completion popup appears only where `startCompletionWait` was running (typically laptop if bridge is used there).

Document this in a short **user-facing note** (e.g. `3-Resources/Watcher-Plugin-Usage.md`) with:

- Quick setup recap (files, enable plugin, toolbar).
- How to open Console and what log lines to expect for trigger / signal / bridge / polling / completion.
- Step-by-step "Test minimal wiring" and "Test mobile → laptop" as above.
- Exact Watcher-Result line format for manual simulation (requestId, status, message, trace with escaped quotes).

## 3. Optional later tweaks (not in this plan)

- **Debug flag**: Add a plugin setting or constant to turn off or reduce console logs after testing.
- **URI scheme**: If Cursor does not open with `cursor://default?prompt=...`, try `cursor://anysphere.cursor-deeplink/prompt?text=...` and document in the usage note.

## 4. Files to touch


| File                                                                   | Action                                                                                                      |
| ---------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| [.obsidian/plugins/watcher/main.js](.obsidian/plugins/watcher/main.js) | All code changes: logging, async writeSignal, command names, modal await.                                   |
| `3-Resources/Watcher-Plugin-Usage.md`                                  | Create (optional but recommended): setup recap, console test steps, mobile–laptop flow, result line format. |


No changes: `manifest.json`, `styles.css`, any Cursor rules or pipeline docs (only reference them in the usage note).

## 5. Summary

- **Plugin**: Add pervasive `[Watcher]` console logs; rename commands to "Watcher: ..."; make `writeSignal` async and await it in Trigger Ingest and modal; add branch logs for bridge on/off and completion polling/timeout; keep bridge off by default.
- **User side**: Expose "Watcher: Trigger Ingest" and "Watcher: Open Prompt Modal" plus ribbon; document setup, Console-based verification, and mobile → laptop test flow in one short usage note so you can confirm communication end-to-end.

