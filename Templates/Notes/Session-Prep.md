<%*
// Session-Prep: lightweight startup check for autonomous Second Brain.
// Runs on Obsidian load (Templater startup template).
// - Reminds to run INGEST MODE if there are files in Ingest.
const ingestPath = "Ingest";
const ingestFolder = app.vault.getAbstractFileByPath(ingestPath);
const now = tp.date.now("YYYY-MM-DD HH:mm");
if (typeof app === "undefined") return;
let message = "";
if (ingestFolder && ingestFolder.children) {
  const mdFiles = ingestFolder.children.filter(f => f.extension === "md");
  if (mdFiles.length > 0) {
    message = `\n[Session ${now}] Ingest has ${mdFiles.length} note(s). Say in Cursor: **INGEST MODE – safe batch autopilot** or **Process Ingest/ with autopilot.**\n`;
  }
}
if (message) {
  const logPath = "Ingest-Log.md";
  const logFile = app.vault.getAbstractFileByPath(logPath);
  let content = message;
  if (logFile) {
    try {
      content = await app.vault.read(logFile) + message;
      await app.vault.modify(logFile, content);
    } catch (e) {
      console.warn("Session-Prep: could not append to Ingest-Log", e);
    }
  } else {
    await app.vault.create(logPath, "## Session log\n" + message);
  }
}
%>
