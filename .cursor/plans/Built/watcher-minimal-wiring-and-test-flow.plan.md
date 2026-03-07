# Watcher minimal wiring, test flow, and recommended improvements

**Overview:** Enhance the Watcher plugin for reliability, debuggability, mobile usability, and cross-device testing — while staying minimal and aligned with the launch goal: simple send/receive signals + basic console visibility. Improvements are grouped into **high** (fix before serious mobile ↔ laptop testing), **medium** (nice-to-have before wider testing), and **low/future** (post-launch polish).

**Scope:** All code changes in [.obsidian/plugins/watcher/main.js](.obsidian/plugins/watcher/main.js). Optional user-facing doc: `3-Resources/Watcher-Plugin-Usage.md`. No changes to `manifest.json`, `styles.css`, or Cursor rules (only reference them in the usage note).

---

## High-priority (do before serious mobile ↔ laptop testing)

### 1. Fix Cursor deep link scheme

**Current (wrong):** `cursor://default?prompt=...`

**Correct (per [Cursor deeplinks docs](https://cursor.com/docs/integrations/deeplinks)):**

```js
// Official Cursor prompt deeplink per https://cursor.com/docs/integrations/deeplinks
// Fallback to clipboard + request file if this fails on your Cursor version
const encodedPrompt = encodeURIComponent(fullPrompt);
const uri = `cursor://anysphere.cursor-deeplink/prompt?text=${encodedPrompt}`;
```

**Change in `attemptCursorBridge()`:** Replace the existing URI construction with the above and keep the existing `console.log('[Watcher] Trying URI:', uri)` (or use the shared `log()` helper below). This is the single most likely reason the bridge would silently fail today.

### 2. Configurable polling intervals

Avoid hard-coded 10s / 15s so tuning during testing is easy (e.g. 3s for fast sync checks).

- At top of plugin class (or in constructor): add instance properties:
  - `this.signalPollIntervalMs = 10000;`
  - `this.completionPollIntervalMs = 15000;`
  - `this.completionTimeoutMs = 15 * 60 * 1000; // 15 min`
- Use `this.signalPollIntervalMs` in `registerInterval(window.setInterval(() => this.checkForSignals(), this.signalPollIntervalMs))`.
- Use `this.completionPollIntervalMs` and `this.completionTimeoutMs` in `startCompletionWait()` (replace `COMPLETION_POLL_MS` and `COMPLETION_TIMEOUT_MS` usages there). Keep the module-level constants for backward compatibility or remove them and use only instance props.

### 3. Robust requestId-to-result matching

- **Stricter format in docs:** In `Watcher-Plugin-Usage.md` and any inline comments, document the expected result line format clearly, e.g.  
  `requestId:abc123-4567 | status:success | message:"Processing complete" | trace:"..."`
- **In `startCompletionWait()` poll callback:**  
  - Only treat a line as a match if it contains the exact `requestId` value and either `status:success` or `status:failure` (current logic is fine; avoid matching partial or junk lines).  
  - Log exactly what happened each tick: either `[Watcher] Polling result file for <requestId>... (Xs elapsed) – no match yet` or `[Watcher] Match found: <the matched line>` (or a safe truncation) then `[Watcher] Completion detected: success|failure`.  
  This avoids false positives from manual junk in the result file and makes debugging trivial.

### 4. Ensure writeSignal is awaited everywhere

- **Modal Send button:** Change to `async () => { await this.plugin.writeSignal(...); ... }` and await before showing Notice and before bridge/polling. Clear the textarea only after successful write.
- **Trigger Ingest command:** Use `await this.writeSignal("INGEST MODE", fullPrompt)` and only then log "Ingest signal written" and proceed to bridge/polling.
- **writeSignal:** Make it `async` and await the vault read/create + append write; return `{ requestId, fullPrompt }` after the write completes. Add try/catch; on failure log and rethrow (or return a failure indicator) so callers don’t assume success.

If not awaited, logs can appear out of order and the Notice may show before the write completes → confusing on slow sync/mobile.

### 5. [Watcher] prefix on ALL console output

Every log must start with `[Watcher]` so DevTools filtering is trivial (search `[Watcher]`).

- Add two helpers on the plugin class:
  - `log(msg)` → `console.log('[Watcher] ' + msg)`
  - `warn(msg)` → `console.warn('[Watcher] ' + msg)`
- Use them everywhere: onload, file guard, writeSignal entry/exit, polling ticks, bridge attempts (URI try, clipboard fallback, request file), completion found/timeout, showCompletionPopup. Replace any ad-hoc `console.log`/`console.warn` in the plugin with these helpers.

---

## Medium-priority (greatly improve test experience)

### 6. Central place for bridge toggle and log level

- **Option A (minimal):** At top of file, add constants:
  - `// Set to true on laptop when Cursor is installed and you want to test hand-off`
  - `const BRIDGE_ENABLED = false;`
  - `const DEBUG_LOGS = true;`  
  Use `BRIDGE_ENABLED` instead of `this.cursorBridgeEnabled` (or set `this.cursorBridgeEnabled = BRIDGE_ENABLED` in constructor). In `log()`/`warn()`, only call `console.log`/`console.warn` when `DEBUG_LOGS` is true (or keep always-on for now and add the gate later).
- **Option B (later):** Use Obsidian `PluginSettingTab` for bridge enabled + debug logs; for this plan, Option A is enough.

### 7. Mobile discoverability and one-tap feel

- **Ribbon:** Rename tooltip to something like "Watcher: Quick Prompt / Ingest" (more descriptive).
- **Toolbar:** If the manifest or Obsidian API allows a hint for command order, ensure "Watcher: Trigger Ingest" is high in the toolbar list for mobile; otherwise document in usage note that users should add it to the mobile toolbar.
- **Modal:** On open, auto-focus the first textarea (e.g. get a ref to the first `watcher-textarea` and call `textareaEl.focus()` after the DOM is ready) — improves mobile typing speed.

### 8. Last requestId status in UI

After a successful `writeSignal`, show a short-lived Notice or a small footer in the modal:
- Example: `Last sent: INGEST MODE • ${requestId.slice(0,8)}...`
- Helps user correlate a mobile trigger with the laptop result file when checking `Watcher-Result.md`.

### 9. Document expected log patterns in Watcher-Plugin-Usage.md

Add a table so the console becomes a verifiable checklist:

| What happened               | Expected console lines (filter by [Watcher]) |
|-----------------------------|----------------------------------------------|
| Plugin loads                | [Watcher] Plugin loaded – wiring active      |
| Trigger Ingest clicked      | [Watcher] Trigger: Ingest mode fired … Signal appended successfully |
| Signal detected (polling)   | [Watcher] New signal detected via polling: … |
| Bridge attempt              | [Watcher] Trying URI: cursor://anysphere...   |
| Completion found             | [Watcher] Completion detected: success       |
| Timeout                     | [Watcher] Timeout reached – no completion signal |

Include the exact result-line format and a short "Test mobile → laptop" flow that references this table.

---

## Low-priority / future polish

### 10. Error handling and retry for vault write

Vault writes can fail (sync conflict, permission). In `writeSignal`, wrap the write in try/catch and retry once after a short delay (e.g. 1s).

### 11. Debounce / throttle polling (or use file watcher)

If sync is very frequent, 10s polling can feel laggy. Consider:
- `this.registerEvent(this.app.vault.on('modify', file => { if (file.path === SIGNAL_FILE) this.checkForSignals(); }))` for signal detection, and optionally similar for result file, to react immediately when files change instead of fixed interval.

### 12. Signal file rotation / cleanup

Append-forever grows the file. Later: keep only the last N lines (e.g. 50) or archive old entries to a separate file.

### 13. Timeout user confirmation

On timeout popup: add a button like "Mark as done anyway" that writes a synthetic success line to the result file for the current requestId — helps when Cursor hung but the user knows the run finished.

---

## Implementation summary (main.js)

- **Bootstrap:** `log('Plugin loaded – wiring active')`, then ensure file guard, then `log('File guard initialized')`. Use `log`/`warn` everywhere.
- **Constants / instance:** Add `BRIDGE_ENABLED`, `DEBUG_LOGS` (optional), and `signalPollIntervalMs`, `completionPollIntervalMs`, `completionTimeoutMs` on the plugin instance (or constants).
- **Commands:** "Watcher: Open Prompt Modal", "Watcher: Trigger Ingest"; ribbon "Watcher: Quick Prompt / Ingest". All callbacks log and (where applicable) await `writeSignal`.
- **writeSignal:** Async; full logging (entry, requestId, success/failure); awaited in Trigger Ingest and in modal Send handler.
- **Bridge:** Use `cursor://anysphere.cursor-deeplink/prompt?text=${encodeURIComponent(fullPrompt)}` with the doc comment; log every step; clipboard and request-file fallbacks unchanged.
- **Completion wait:** Use configurable intervals; log each poll ("no match yet" or "match found" + line); log timeout and completion detected.
- **Modal:** Await `writeSignal` in Send; optional auto-focus first textarea; optional "Last sent: mode • requestId..." in Notice or footer.
- **Result matching:** Stricter parsing and explicit log of matched line (or "no match yet").

---

## User-facing doc (Watcher-Plugin-Usage.md)

- Quick setup: plugin files, enable plugin, add "Watcher: Trigger Ingest" to toolbar (especially for mobile).
- **Expected log patterns** table (see item 9).
- Exact Watcher-Result line format and how to simulate a result for testing.
- Step-by-step: "Test minimal wiring" (same device) and "Test mobile → laptop" (signal from mobile, Cursor on laptop, result sync back, popup where completion wait is running).
- Note: Test the official Cursor URI first on laptop; if it doesn’t open, fallback to clipboard/request file.

---

## Files to touch

| File | Action |
|------|--------|
| [.obsidian/plugins/watcher/main.js](.obsidian/plugins/watcher/main.js) | All code changes above (high + medium items; low items optional later). |
| 3-Resources/Watcher-Plugin-Usage.md | Create: setup, log-pattern table, result format, mobile–laptop test flow. |

No changes: `manifest.json`, `styles.css`, Cursor rules (only referenced in usage note).
