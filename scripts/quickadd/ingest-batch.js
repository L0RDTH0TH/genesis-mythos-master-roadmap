// QuickAdd macro: append "INGEST MODE – safe batch autopilot" to Ingest-Log.md
// Use from toolbar: Ingest Batch — then open Cursor to run pipeline.
"use strict";
module.exports = async (params) => {
  const { app } = params;
  const path = "Ingest-Log.md";
  const now = new Date();
  const ts = now.toISOString().replace("T", " ").slice(0, 19) + "Z";
  const line = `\n${ts} | INGEST MODE – safe batch autopilot\n`;
  try {
    const file = app.vault.getAbstractFileByPath(path);
    const content = file ? await app.vault.read(file) : "";
    await (file ? app.vault.modify(file, content + line) : app.vault.create(path, line.trimStart()));
    new Notice("Batch trigger added – open Cursor to run.");
  } catch (e) {
    new Notice("Failed to append to Ingest-Log: " + e.message);
  }
};
