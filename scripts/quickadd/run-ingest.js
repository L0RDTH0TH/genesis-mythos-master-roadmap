// QuickAdd macro: append "INGEST MODE – execute now" to Ingest-Log.md
// Fallback if Advanced URI not used: open Cursor manually to run pipeline.
"use strict";
module.exports = async (params) => {
  const { app } = params;
  const path = "Ingest-Log.md";
  const now = new Date();
  const ts = now.toISOString().replace("T", " ").slice(0, 19) + "Z";
  const line = `\n${ts} | INGEST MODE – execute now\n`;
  try {
    const file = app.vault.getAbstractFileByPath(path);
    const content = file ? await app.vault.read(file) : "";
    await (file ? app.vault.modify(file, content + line) : app.vault.create(path, line.trimStart()));
    new Notice("Trigger logged. Open Cursor manually to run pipeline.");
  } catch (e) {
    new Notice("Failed to append to Ingest-Log: " + e.message);
  }
};
