---
created: 2026-02-27
tags:
  - watcher
  - cursor
  - extension
  - feasibility
  - second-brain
---

# Watcher → Cursor Signal Extension: Feasibility Evaluation

Evaluation of the approach: **a Cursor/VS Code extension that watches a signal file and triggers a new chat with the prompt** (so Cursor reacts to Watcher emissions without manual paste).

## Summary

| Aspect | Verdict | Notes |
|--------|--------|--------|
| **File watching** | ✅ Feasible | `createFileSystemWatcher` works; watch `Watcher-Signal.md` or a dedicated `signal.json` in workspace. |
| **Opening chat** | ⚠️ Likely | `workbench.action.chat.open` (or Cursor equivalent) may exist; needs verification in Cursor. |
| **Pasting prompt** | ⚠️ Fragile | Clipboard + paste depends on focus landing in chat input; timing and focus can be flaky. |
| **Auto-submit** | ❌ Blocked | **`workbench.action.chat.submit` is missing in Cursor** (reported in forum as of 2025); only `workbench.action.chat.stopListeningAndSubmit` exists (voice-specific). |
| **Output capture** | ❌ Brittle | Select-all + copy in chat panel is timing-dependent and may capture wrong content; no stable API for "chat response text". |

**Overall:** The idea is **partially feasible**. File watching + opening chat + pasting can likely be done; **automatic submit is the main blocker** unless Cursor adds a submit command or the extension finds a workaround (e.g. simulated Enter in chat input, if exposed).

---

## What Works

### 1. File system watcher

- **API:** `vscode.workspace.createFileSystemWatcher(glob)` — standard VS Code; works in Cursor.
- **Scope:** Only files under workspace (or open folders). Your signal file must live in the vault (e.g. `3-Resources/Watcher-Signal.md` or `signal.json` in project root).
- **Events:** `onDidChange`, `onDidCreate`, `onDidDelete`. For Watcher, **onDidChange** is the right one (Obsidian appends a new line to `Watcher-Signal.md`).
- **Parsing:** Either watch `3-Resources/Watcher-Signal.md` and parse the **last line** (`[timestamp] requestId: ... | mode: ... | prompt: "..."`) or have Watcher also write a small `signal.json` with `{ "instruction": "..." }` for simpler parsing. The former avoids changing the Watcher plugin.

### 2. Opening the chat panel

- **VS Code:** Commands like `workbench.action.chat.open` (or similar) exist in VS Code’s Copilot/Chat UX. Cursor is a fork; its command IDs might differ.
- **Action:** On signal file change, call `vscode.commands.executeCommand('workbench.action.chat.open')` (or the Cursor equivalent). Worth testing in Cursor’s command palette / keybindings to see what “Open AI Chat” is bound to.

### 3. Putting the prompt into the chat input

- **Approach:** `vscode.env.clipboard.writeText(signal.instruction)` then trigger paste (e.g. `editor.action.clipboardPasteAction` or a chat-specific paste command).
- **Risk:** Paste goes to the **currently focused** widget. If the chat panel opens asynchronously, focus might still be in the editor; then paste would go to the wrong place. A short delay (e.g. 300–500 ms) after opening chat might be needed; still heuristic.

---

## What’s Blocked or Brittle

### 1. Auto-submit (submit after pasting)

- **Issue:** In Cursor, **`workbench.action.chat.submit` is not available** (see [forum post](https://forum.cursor.com/t/missing-workbench-action-chat-submit-command/118037)). Only `workbench.action.chat.stopListeningAndSubmit` appears, and it’s for voice chat.
- **Impact:** The extension can open chat and paste the prompt, but **cannot reliably submit** via a known command. User would still have to press Enter (or click Send).
- **Workarounds (uncertain):**
  - Simulate keypress (e.g. Enter) in the chat input. This would require the chat input to be focusable and the extension to send keys to it; possible only if Cursor exposes an API or if a generic “type key in focused element” exists (not standard in VS Code extension API for the chat widget).
  - Request Cursor to add `workbench.action.chat.submit` (or equivalent) so extensions/keybindings can submit chat.

### 2. Capturing chat output

- The suggested approach (after a delay: select all → copy → write to file) is **fragile**: the “editor” at that moment might be the chat response area, or something else; selection and timing are unreliable.
- There is **no public VS Code/Cursor API** that returns “the last assistant message in the chat” as a string. So automated, reliable “write result to Watcher” in the extension is not feasible without such an API.

---

## Alignment with Your Current Setup

- **Watcher** already writes to `3-Resources/Watcher-Signal.md` with line-based format:  
  `[ISO8601] requestId: <id> | mode: <mode> | prompt: "<text>"`
- **Agent** (and rules) already read the **last line** of that file to get `requestId` and prompt when the user triggers “INGEST MODE” etc. from the Watcher.
- **Watcher-Result:** The agent appends to `3-Resources/Watcher-Result.md` when done; no need for the extension to capture chat output if the agent continues to do that.

So the **only** thing the extension would add is: **when `Watcher-Signal.md` changes, open Cursor chat and paste the prompt** (and ideally submit). Given the missing submit command, the extension still reduces friction (open + paste) but does not achieve full “hands-off” automation.

---

## Recommended Directions

1. **Minimal extension (no submit)**  
   Watch `3-Resources/Watcher-Signal.md` (or `**/signal.json`). On change: parse last line (or JSON), open chat, write prompt to clipboard, run “open chat” command, then trigger paste after a short delay. Document that the user must press Enter to submit. Still useful for “one keypress instead of copy-paste from file”.

2. **Verify Cursor command IDs**  
   In Cursor: Open Keyboard Shortcuts, search for “chat” and “submit”. Note the exact command IDs for “Open Chat” and (if any) “Submit” or “Send”. If a submit command exists under another ID, the extension can use it.

3. **Feature request to Cursor**  
   Ask Cursor to expose a command equivalent to `workbench.action.chat.submit` so that extensions (and keybindings) can submit the chat programmatically.

4. **Alternative: MCP or polling in agent**  
   Keep the current flow: user (or a cron/scheduler) opens Cursor and runs a single prompt (e.g. “Process Watcher signal” or “INGEST MODE”). The agent then reads `Watcher-Signal.md` and processes it. No extension needed; automation is “trigger Cursor with a fixed prompt” (e.g. from Watcher’s bridge or a shell script) and the agent does the rest. This is already supported by your rules and Watcher-Result contract.

5. **If you still build the extension**  
   - Use `createFileSystemWatcher('**/Watcher-Signal.md')` and parse the last line to get `requestId` and `prompt`.  
   - Contribute a command (e.g. “Watcher: Process latest signal”) so the user can also trigger it from the palette.  
   - Don’t rely on output capture; keep using agent-appended `Watcher-Result.md` for completion and popups.

---

## Conclusion

- **Feasible:** File watching, opening chat, and pasting the Watcher prompt into Cursor (with minor focus/timing caveats).
- **Not feasible today:** Fully automatic submit and reliable capture of chat output, due to missing Cursor command and no chat-response API.
- **Practical use:** An extension that “open chat + paste prompt” is viable and reduces friction; full automation (submit + optional capture) depends on Cursor adding a submit command and, for capture, a chat API.
