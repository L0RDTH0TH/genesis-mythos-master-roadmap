// QuickAdd macro: append DISTILL MODE trigger for current note to Distill-Log.md
// Then open Cursor and run: DISTILL MODE – safe batch autopilot (or use Advanced URI).
"use strict";
module.exports = async (params) => {
  const { app } = params;
  const path = "3-Resources/Distill-Log.md";
  const active = app.workspace.getActiveFile();
  const noteRef = active ? active.path : "(no active note)";
  const now = new Date();
  const ts = now.toISOString().replace("T", " ").slice(0, 19) + "Z";
  const line = `\n${ts} | DISTILL MODE – safe batch autopilot | Note: ${noteRef}\n`;
  try {
    const file = app.vault.getAbstractFileByPath(path);
    const content = file ? await app.vault.read(file) : "";
    await (file ? app.vault.modify(file, content + line) : app.vault.create(path, line.trimStart()));
    new Notice("Distill trigger logged. Open Cursor to run pipeline.");
  } catch (e) {
    new Notice("Failed to append to Distill-Log: " + e.message);
  }
};
