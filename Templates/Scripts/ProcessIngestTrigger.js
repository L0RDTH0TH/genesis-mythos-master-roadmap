// QuickAdd User Script: Append "Process Ingest" trigger line to Ingest-Log.md
// Use with a QuickAdd Macro (add command: User Script → this file) or run from Macro choice.
// Then say in Cursor: "INGEST MODE – safe batch autopilot" or "Process Ingest/ with autopilot."
module.exports = async (params) => {
  const { app } = params;
  const now = window.moment ? window.moment().format("YYYY-MM-DD HH:mm") : new Date().toISOString().slice(0, 16).replace("T", " ");
  const line = `---\nTrigger: Process Ingest – ${now}\nSay in Cursor: "INGEST MODE – safe batch autopilot" or "Process Ingest/ with autopilot."\n`;
  const logPath = "Ingest-Log.md";
  try {
    const file = app.vault.getAbstractFileByPath(logPath);
    if (file) {
      const content = await app.vault.read(file) + line;
      await app.vault.modify(file, content);
    } else {
      await app.vault.create(logPath, "## Ingest log\n" + line);
    }
    try {
      if (typeof Notice !== "undefined") new Notice("Appended Process Ingest trigger to Ingest-Log.md");
    } catch (_) {}
  } catch (e) {
    console.error("ProcessIngestTrigger:", e);
    throw e;
  }
};
