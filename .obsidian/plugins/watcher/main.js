/*
Watcher Plugin v3 — URI Bridge Pivot
Sections: bootstrap, file guard, signals, bridge, modal, completion
*/

const { Plugin, Modal, Notice } = require("obsidian");

// --- Constants ---
const RESOURCES_FOLDER = "3-Resources";
const SIGNAL_FILE = "3-Resources/Watcher-Signal.md";
const RESULT_FILE = "3-Resources/Watcher-Result.md";
const TIMING_LOG_FILE = ".technical/Watcher-Timing-Log.md";
const WATCHED_FILE = "Ingest/watched-file.md";
const QUEUE_FILE = ".technical/prompt-queue.jsonl";
const TASK_QUEUE_FILE = "3-Resources/Task-Queue.md";
const MOBILE_PENDING_FILE = "3-Resources/Mobile-Pending-Actions.md";
const WRAPPER_SYNC_LOG = "3-Resources/Wrapper-Sync-Log.md";
const ERRORS_FILE = "3-Resources/Errors.md";
const DECISIONS_PREFIX = "Ingest/Decisions/";
const COMPLETION_POLL_MS = 15000;
const COMPLETION_TIMEOUT_MS = 15 * 60 * 1000; // 15 min

const MODES = [
  {
    id: "DISTILL",
    preset: "DISTILL MODE – safe batch autopilot",
    placeholder: "Paste context or leave blank for batch…",
  },
  {
    id: "EXPRESS",
    preset: "EXPRESS MODE – safe batch autopilot",
    placeholder: "Paste quotes or context for express…",
  },
  {
    id: "ARCHIVE",
    preset: "ARCHIVE MODE – safe batch autopilot",
    placeholder: "Paste context or leave blank for batch…",
  },
];

// --- WatcherModal (DISTILL, EXPRESS, ARCHIVE only) ---
class WatcherModal extends Modal {
  constructor(app, plugin) {
    super(app);
    this.plugin = plugin;
  }

  onOpen() {
    const { contentEl } = this;
    contentEl.addClass("watcher-modal");
    contentEl.createEl("h2", { text: "Watcher Modes" });

    const scrollContainer = contentEl.createDiv({ cls: "watcher-modal-content" });

    for (const mode of MODES) {
      const section = scrollContainer.createDiv({ cls: "watcher-mode-section" });
      section.createEl("h3", { text: mode.id });

      const textarea = section.createEl("textarea", {
        cls: "watcher-textarea",
        attr: { placeholder: mode.placeholder },
      });

      const btnRow = section.createDiv();
      const pasteBtn = btnRow.createEl("button", { text: "Paste" });
      const sendBtn = btnRow.createEl("button", { text: "Send" });

      pasteBtn.addEventListener("click", () => {
        navigator.clipboard.readText().then((text) => {
          textarea.value = (textarea.value + (textarea.value ? "\n" : "") + text).trim();
        }).catch(() => new Notice("Watcher: Could not read clipboard"));
      });

      sendBtn.addEventListener("click", async () => {
        const context = textarea.value.trim();
        let fullPrompt = context ? `${mode.preset} – ${context}` : mode.preset;
        let sourceFile = "";
        const file = this.app.workspace.getActiveFile();
        if (file && file.extension === "md") {
          try {
            const fileContent = await this.app.vault.cachedRead(file);
            sourceFile = file.path;
            fullPrompt = `${mode.preset}\n\n--- File: ${file.path} ---\n${fileContent}\n\n--- User input ---\n${context || "(none)"}`;
          } catch (_) {}
        }
        const result = await this.plugin.appendToQueue(mode.preset, fullPrompt, sourceFile);
        textarea.value = "";

        const requestId = result?.requestId;
        if (result?.skipped) {
          new Notice("Watcher: Already in queue (duplicate).");
        } else if (requestId) {
          const pending = await this.plugin.getQueuePendingCount();
          new Notice(`Watcher: Added to queue (${requestId}). Pending: ${pending}`);
        } else {
          new Notice("Watcher: Queue write failed.");
        }
      });
    }

    const eatCacheSection = scrollContainer.createDiv({ cls: "watcher-mode-section" });
    eatCacheSection.createEl("h3", { text: "EAT-CACHE" });
    const pendingEl = eatCacheSection.createEl("p", { text: "Pending: …" });
    this.plugin.getQueuePendingCount().then((n) => {
      pendingEl.setText(`Pending: ${n}`);
    });

    const filterRow = eatCacheSection.createDiv();
    filterRow.createEl("label", { text: "Filter: " });
    const filterSelect = filterRow.createEl("select");
    filterSelect.createEl("option", { value: "all", text: "All modes" });
    filterSelect.createEl("option", { value: "distill", text: "Distill only" });
    const btnRow = eatCacheSection.createDiv();
    btnRow.createEl("button", { text: "Copy queue" }).addEventListener("click", () => {
      const filter = filterSelect.value;
      this.plugin.runEatCache({ filter: filter === "distill" ? "distill" : "all" });
      this.close();
    });
    btnRow.createEl("button", { text: "Clear Queue" }).addEventListener("click", async () => {
      await this.plugin.clearQueue(true);
      pendingEl.setText("Pending: 0");
    });
  }

  onClose() {
    this.contentEl.empty();
  }
}

// --- Add Roadmap Item modal (task queue) ---
class AddRoadmapItemModal extends Modal {
  constructor(app, plugin) {
    super(app);
    this.plugin = plugin;
  }

  onOpen() {
    const { contentEl } = this;
    contentEl.addClass("watcher-modal");
    contentEl.createEl("h2", { text: "Add Roadmap Item" });

    const secondaryRow = contentEl.createDiv();
    secondaryRow.createEl("label", { text: "Secondary (file to attach): " });
    const secondaryInput = contentEl.createEl("input", { type: "text", cls: "watcher-input" });
    const file = this.app.workspace.getActiveFile();
    if (file && file.extension === "md") secondaryInput.value = file.path;
    secondaryInput.placeholder = "default: current file";

    const primaryRow = contentEl.createDiv();
    primaryRow.createEl("label", { text: "Primary (roadmap path): " });
    const primaryInput = contentEl.createEl("input", { type: "text", cls: "watcher-input" });
    primaryInput.placeholder = "e.g. 1-Projects/MyProject/Roadmap/Roadmap.md";

    const sectionRow = contentEl.createDiv();
    sectionRow.createEl("label", { text: "Section: " });
    const sectionSelect = contentEl.createEl("select", { cls: "watcher-select" });
    sectionSelect.createEl("option", { value: "", text: "(load sections after primary path)" });

    primaryInput.addEventListener("blur", async () => {
      const path = primaryInput.value.trim();
      sectionSelect.innerHTML = "";
      sectionSelect.createEl("option", { value: "", text: "(select section)" });
      if (!path) return;
      try {
        const f = this.app.vault.getAbstractFileByPath(path);
        if (!f) return;
        const content = await this.app.vault.read(f);
        const headings = content.match(/^#{1,6}\s+.+$/gm) || [];
        headings.forEach((h) => {
          const text = h.replace(/^#+\s+/, "").trim();
          sectionSelect.createEl("option", { value: text, text: text });
        });
      } catch (_) {}
    });

    const insertRow = contentEl.createDiv();
    insertRow.createEl("label", { text: "Insert: " });
    const insertSection = contentEl.createDiv();
    ["section-end", "after-task", "sub-task"].forEach((val) => {
      const label = contentEl.createEl("label");
      const radio = contentEl.createEl("input", { type: "radio", name: "insertType", value: val });
      if (val === "section-end") radio.checked = true;
      label.appendChild(radio);
      label.appendText(val === "section-end" ? " Append to section end " : val === "after-task" ? " After this task " : " As sub-task ");
      insertSection.appendChild(label);
    });

    const btnRow = contentEl.createDiv();
    const confirmBtn = btnRow.createEl("button", { text: "Queue" });
    confirmBtn.addEventListener("click", async () => {
      const primaryPath = primaryInput.value.trim();
      const secondaryPath = secondaryInput.value.trim() || (file && file.path ? file.path : "");
      const section = sectionSelect.value || "";
      const insertType = contentEl.querySelector('input[name="insertType"]:checked')?.value || "section-end";
      if (!primaryPath) {
        new Notice("Watcher: Primary roadmap path required.");
        return;
      }
      const requestId = (Date.now() + Math.random() * 1e9).toString(36);
      const entry = {
        mode: "ADD-ROADMAP-ITEM",
        primaryPath,
        secondaryPath: secondaryPath || (file && file.path ? file.path : ""),
        section,
        insertType,
        requestId,
        timestamp: new Date().toISOString(),
      };
      await this.plugin.appendToTaskQueue(entry);
      new Notice("Add Roadmap Item queued. Run EAT-QUEUE to process.");
      this.close();
    });
  }

  onClose() {
    this.contentEl.empty();
  }
}

// --- Task Complete modal (toggle + queue) ---
class TaskCompleteModal extends Modal {
  constructor(app, plugin) {
    super(app);
    this.plugin = plugin;
  }

  onOpen() {
    const { contentEl } = this;
    contentEl.addClass("watcher-modal");
    contentEl.createEl("h2", { text: "Task Complete" });

    const stateRow = contentEl.createDiv();
    stateRow.createEl("label", { text: "Desired state: " });
    const completeRadio = contentEl.createEl("input", { type: "radio", name: "taskState", value: "complete", id: "tc-complete" });
    const incompleteRadio = contentEl.createEl("input", { type: "radio", name: "taskState", value: "incomplete", id: "tc-incomplete" });
    completeRadio.checked = true;
    const labelComplete = contentEl.createEl("label", { attr: { for: "tc-complete" } });
    labelComplete.appendText(" Complete ");
    const labelIncomplete = contentEl.createEl("label", { attr: { for: "tc-incomplete" } });
    labelIncomplete.appendText(" Incomplete ");
    stateRow.appendChild(completeRadio);
    stateRow.appendChild(labelComplete);
    stateRow.appendChild(incompleteRadio);
    stateRow.appendChild(labelIncomplete);

    const btnRow = contentEl.createDiv();
    const confirmBtn = btnRow.createEl("button", { text: "Queue" });
    confirmBtn.addEventListener("click", async () => {
      const file = this.app.workspace.getActiveFile();
      if (!file || file.extension !== "md") {
        new Notice("Watcher: Open a markdown note with a task.");
        return;
      }
      let taskLocator = "cursor";
      const leaf = this.app.workspace.activeLeaf;
      if (leaf && leaf.view && leaf.view.editor) {
        const line = leaf.view.editor.getCursor().line;
        taskLocator = String(line);
      }
      const desiredState = contentEl.querySelector('input[name="taskState"]:checked')?.value || "complete";
      const requestId = (Date.now() + Math.random() * 1e9).toString(36);
      const entry = {
        mode: "TASK-COMPLETE",
        filePath: file.path,
        taskLocator,
        desiredState,
        requestId,
        timestamp: new Date().toISOString(),
      };
      await this.plugin.appendToTaskQueue(entry);
      await this.plugin.appendToMobilePending("Task Complete queued (pending EAT-QUEUE).");
      new Notice("Task Complete queued (pending until EAT-QUEUE).");
      this.close();
    });
  }

  onClose() {
    this.contentEl.empty();
  }
}

// --- Completion popup (Modal with detailed trace) ---
class CompletionPopupModal extends Modal {
  constructor(app, title, message, trace, status) {
    super(app);
    this.titleText = title;
    this.messageText = message;
    this.traceText = trace || "";
    this.status = status;
  }

  onOpen() {
    const { contentEl } = this;
    contentEl.addClass("watcher-completion-popup");
    contentEl.createEl("h2", { text: this.titleText });
    contentEl.createEl("p", { text: this.messageText });
    if (this.traceText) {
      const pre = contentEl.createDiv({ cls: "watcher-trace" });
      pre.setText(this.traceText);
    }
  }

  onClose() {
    this.contentEl.empty();
  }
}

// --- Main plugin ---
module.exports = class WatcherPlugin extends Plugin {
  constructor(...args) {
    super(...args);
    this.signalFilePath = SIGNAL_FILE;
    this.resultFilePath = RESULT_FILE;
    this.watchedFilePath = WATCHED_FILE;
    this.lastRequestId = "";
    this.cursorBridgeEnabled = false;
    this.hasShownBridgeNotice = false;
    this._pollInterval = null;
  }

  async onload() {
    console.log("[Watcher] Plugin loaded – wiring active");
    // Enable Cursor deeplink/clipboard bridge by default so mobile triggers
    // can hand prompts directly to Cursor.
    this.cursorBridgeEnabled = true;
    await this.ensureFileGuard();
    console.log("[Watcher] File guard initialized");

    this.addCommand({
      id: "open-watcher-modal",
      name: "Prompt Modal",
      callback: () => {
        console.log("[Watcher] Trigger: Open Prompt Modal");
        new WatcherModal(this.app, this).open();
      },
    });

    this.addCommand({
      id: "trigger-ingest",
      name: "Ingest",
      icon: "forward",
      callback: async () => {
        console.log("[Watcher] Trigger: Ingest mode fired (one-tap)");
        const fullPrompt = "INGEST MODE – process captures";
        const result = await this.appendToQueue("INGEST MODE", fullPrompt, "");
        const requestId = result?.requestId;
        if (result?.skipped) {
          new Notice("Watcher: Already in queue (duplicate).");
        } else if (requestId) {
          const pending = await this.getQueuePendingCount();
          new Notice(`Watcher: Added to queue (${requestId}). Pending: ${pending}`);
        } else {
          new Notice("Watcher: Queue write failed.");
        }
      },
    });

    this.addCommand({
      id: "trigger-distill",
      name: "Distill",
      icon: "barrel",
      callback: async () => {
        console.log("[Watcher] Trigger: Distill mode fired (one-tap)");
        let fullPrompt = "DISTILL MODE – safe batch autopilot";
        let sourceFile = "";
        const file = this.app.workspace.getActiveFile();
        if (file && file.extension === "md") {
          try {
            const fileContent = await this.app.vault.cachedRead(file);
            sourceFile = file.path;
            fullPrompt = `DISTILL MODE – safe batch autopilot\n\n--- File: ${file.path} ---\n${fileContent}\n\n--- User input ---\n(none)`;
          } catch (_) {}
        }
        const result = await this.appendToQueue("DISTILL MODE", fullPrompt, sourceFile);
        const requestId = result?.requestId;
        if (result?.skipped) {
          new Notice("Watcher: Distill already in queue (duplicate).");
        } else if (requestId) {
          const pending = await this.getQueuePendingCount();
          new Notice(`Watcher: Added to queue (${requestId}). Pending: ${pending}`);
        } else {
          new Notice("Watcher: Queue write failed.");
        }
      },
    });

    this.addCommand({
      id: "trigger-express",
      name: "Express",
      icon: "music-4",
      callback: async () => {
        console.log("[Watcher] Trigger: Express mode fired (one-tap)");
        let fullPrompt = "EXPRESS MODE – safe batch autopilot";
        let sourceFile = "";
        const file = this.app.workspace.getActiveFile();
        if (file && file.extension === "md") {
          try {
            const fileContent = await this.app.vault.cachedRead(file);
            sourceFile = file.path;
            fullPrompt = `EXPRESS MODE – safe batch autopilot\n\n--- File: ${file.path} ---\n${fileContent}\n\n--- User input ---\n(none)`;
          } catch (_) {}
        }
        const result = await this.appendToQueue("EXPRESS MODE", fullPrompt, sourceFile);
        const requestId = result?.requestId;
        if (result?.skipped) {
          new Notice("Watcher: Already in queue (duplicate).");
        } else if (requestId) {
          const pending = await this.getQueuePendingCount();
          new Notice(`Watcher: Added to queue (${requestId}). Pending: ${pending}`);
        } else {
          new Notice("Watcher: Queue write failed.");
        }
      },
    });

    this.addCommand({
      id: "trigger-organize",
      name: "Organize",
      icon: "arrow-up-down",
      callback: async () => {
        console.log("[Watcher] Trigger: Organize mode fired (one-tap)");
        let fullPrompt = "ORGANIZE MODE – safe batch autopilot";
        let sourceFile = "";
        const file = this.app.workspace.getActiveFile();
        if (file && file.extension === "md") {
          try {
            const fileContent = await this.app.vault.cachedRead(file);
            sourceFile = file.path;
            fullPrompt = `ORGANIZE MODE – safe batch autopilot\n\n--- File: ${file.path} ---\n${fileContent}\n\n--- User input ---\n(none)`;
          } catch (_) {}
        }
        const result = await this.appendToQueue("ORGANIZE MODE", fullPrompt, sourceFile);
        const requestId = result?.requestId;
        if (result?.skipped) {
          new Notice("Watcher: Already in queue (duplicate).");
        } else if (requestId) {
          const pending = await this.getQueuePendingCount();
          new Notice(`Watcher: Added to queue (${requestId}). Pending: ${pending}`);
        } else {
          new Notice("Watcher: Queue write failed.");
        }
      },
    });

    this.addCommand({
      id: "trigger-archive",
      name: "Archive",
      icon: "database-backup",
      callback: async () => {
        console.log("[Watcher] Trigger: Archive mode fired (one-tap)");
        let fullPrompt = "ARCHIVE MODE – safe batch autopilot";
        let sourceFile = "";
        const file = this.app.workspace.getActiveFile();
        if (file && file.extension === "md") {
          try {
            const fileContent = await this.app.vault.cachedRead(file);
            sourceFile = file.path;
            fullPrompt = `ARCHIVE MODE – safe batch autopilot\n\n--- File: ${file.path} ---\n${fileContent}\n\n--- User input ---\n(none)`;
          } catch (_) {}
        }
        const result = await this.appendToQueue("ARCHIVE MODE", fullPrompt, sourceFile);
        const requestId = result?.requestId;
        if (result?.skipped) {
          new Notice("Watcher: Already in queue (duplicate).");
        } else if (requestId) {
          const pending = await this.getQueuePendingCount();
          new Notice(`Watcher: Added to queue (${requestId}). Pending: ${pending}`);
        } else {
          new Notice("Watcher: Queue write failed.");
        }
      },
    });

    this.addCommand({
      id: "eat-cache",
      name: "EAT-CACHE (copy queue to clipboard)",
      callback: () => this.runEatCache(),
    });

    this.addCommand({
      id: "clear-queue",
      name: "Clear queue",
      icon: "trash-2",
      callback: () => this.clearQueue(false),
    });

    this.addCommand({
      id: "trigger-task-roadmap",
      name: "TASK-ROADMAP",
      icon: "list-checks",
      callback: async () => {
        const file = this.app.workspace.getActiveFile();
        const filePath = file && file.extension === "md" ? file.path : "";
        const requestId = (Date.now() + Math.random() * 1e9).toString(36);
        await this.appendToTaskQueue({
          mode: "TASK-ROADMAP",
          filePath: filePath || "Ingest/",
          requestId,
          timestamp: new Date().toISOString(),
        });
        new Notice("TASK-ROADMAP queued. Run EAT-QUEUE to process.");
      },
    });

    this.addCommand({
      id: "trigger-task-complete",
      name: "Task Complete",
      icon: "check-circle",
      callback: () => new TaskCompleteModal(this.app, this).open(),
    });

    this.addCommand({
      id: "open-add-roadmap-item-modal",
      name: "Add Roadmap Item",
      icon: "link",
      callback: () => new AddRoadmapItemModal(this.app, this).open(),
    });

    this.addRibbonIcon("eye", "Watcher Modal", () => {
      console.log("[Watcher] Ribbon trigger: Open modal");
      new WatcherModal(this.app, this).open();
    });

    this.registerEvent(this.app.vault.on("modify", (file) => this.onFileModify(file)));

    // Queue-only flow: no signal polling (mobile triggers append to queue only)
  }

  onunload() {
    if (this._pollInterval) clearInterval(this._pollInterval);
  }

  // --- File guard ---
  async ensureFileGuard() {
    const vault = this.app.vault;
    let folder = vault.getAbstractFileByPath(RESOURCES_FOLDER);
    if (!folder) {
      try {
        folder = await vault.createFolder(RESOURCES_FOLDER);
      } catch (e) {
        console.warn("[Watcher] Could not create 3-Resources", e);
        return;
      }
    }

    let watched = vault.getAbstractFileByPath(this.watchedFilePath);
    if (!watched) {
      const placeholder = "---\nwatcher-protected: true\n---\n\n# Watched file\n";
      try {
        await vault.create(this.watchedFilePath, placeholder);
      } catch (e) {
        console.warn("[Watcher] Could not create watched file", e);
      }
    }
    // Ensure .technical folder exists (required on mobile where adapter.write may not create parents)
    const technicalDir = ".technical";
    let technicalFolder = vault.getAbstractFileByPath(technicalDir);
    if (!technicalFolder) {
      try {
        await vault.createFolder(technicalDir);
        console.log("[Watcher] .technical folder created");
      } catch (e) {
        console.warn("[Watcher] Could not create .technical folder", e);
      }
    }
    // Ensure queue file exists (empty) for queue-only flow
    let queueFile = vault.getAbstractFileByPath(QUEUE_FILE);
    if (!queueFile) {
      try {
        await vault.adapter.write(QUEUE_FILE, "");
        console.log("[Watcher] Queue file created");
      } catch (e) {
        console.warn("[Watcher] Could not create queue file", e);
      }
    }
    // Ensure task queue file exists for roadmap/task queue
    let taskQueueFile = vault.getAbstractFileByPath(TASK_QUEUE_FILE);
    if (!taskQueueFile) {
      try {
        const header = "---\ntitle: Task Queue\n---\n\n# Task Queue\n\n";
        await vault.adapter.write(TASK_QUEUE_FILE, header);
        console.log("[Watcher] Task queue file created");
      } catch (e) {
        console.warn("[Watcher] Could not create task queue file", e);
      }
    }
    console.log("[Watcher] Watched file ensured / protected");
  }

  // --- Decision Wrapper sync (checkbox → frontmatter) ---
  isDecisionWrapperPath(path) {
    if (!path || typeof path !== "string" || !path.endsWith(".md")) return false;
    const normalized = path.replace(/\\/g, "/");
    return normalized.startsWith(DECISIONS_PREFIX) && normalized.length > DECISIONS_PREFIX.length;
  }

  parseFrontmatter(content) {
    const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
    if (!match) return {};
    try {
      const lines = match[1].split(/\r?\n/);
      const out = {};
      for (const line of lines) {
        const colon = line.indexOf(":");
        if (colon === -1) continue;
        const key = line.slice(0, colon).trim();
        let val = line.slice(colon + 1).trim();
        if (val.startsWith('"') && val.endsWith('"')) val = val.slice(1, -1).replace(/\\"/g, '"');
        if (val === "true") out[key] = true;
        else if (val === "false") out[key] = false;
        else out[key] = val;
      }
      return out;
    } catch (_) {
      return {};
    }
  }

  extractPathFromOptionLine(line) {
    const optionMatch = line.match(/\b([A-G])\b[.):]?\s*(.*)/i);
    if (!optionMatch) return "";
    let rest = optionMatch[2].trim();
    rest = rest.replace(/^[\s*_]*|[\s*_]*$/g, "");
    const dash = rest.search(/\s+[—–-]\s+|\s+%\s+/);
    const pathPart = dash >= 0 ? rest.slice(0, dash).trim() : rest.trim();
    return pathPart.replace(/^[`'"]|[`'"]$/g, "").trim();
  }

  parseBodyForCheckedOption(body) {
    const lines = body.split(/\r?\n/);
    const checkedBoxRegex = /\[\s*x\s*\]/i;
    const letterRegex = /\b([A-G])\b[.):]?\s*/i;
    const checked = [];
    for (const line of lines) {
      if (!checkedBoxRegex.test(line)) continue;
      const letterM = line.match(letterRegex);
      if (!letterM) continue;
      const letter = letterM[1].toUpperCase();
      const path = this.extractPathFromOptionLine(line);
      checked.push({ letter, path });
    }
    if (checked.length === 0) return "none";
    if (checked.length > 1) return "conflict";
    return checked[0];
  }

  async appendToWrapperSyncLog(line) {
    try {
      const vault = this.app.vault;
      let folder = vault.getAbstractFileByPath(RESOURCES_FOLDER);
      if (!folder) await vault.createFolder(RESOURCES_FOLDER);
      let existing = "";
      try {
        const f = vault.getAbstractFileByPath(WRAPPER_SYNC_LOG);
        if (f) existing = await vault.read(f);
      } catch (_) {}
      const newContent = (existing.trimEnd() ? existing.trimEnd() + "\n" : "") + line.trim();
      await vault.adapter.write(WRAPPER_SYNC_LOG, newContent);
    } catch (e) {
      console.warn("[Watcher] Wrapper-Sync-Log append failed", e);
    }
  }

  async appendToErrors(line) {
    try {
      const vault = this.app.vault;
      let folder = vault.getAbstractFileByPath(RESOURCES_FOLDER);
      if (!folder) await vault.createFolder(RESOURCES_FOLDER);
      let existing = "";
      try {
        const f = vault.getAbstractFileByPath(ERRORS_FILE);
        if (f) existing = await vault.read(f);
      } catch (_) {}
      const newContent = (existing.trimEnd() ? existing.trimEnd() + "\n" : "") + line.trim();
      await vault.adapter.write(ERRORS_FILE, newContent);
    } catch (e) {
      console.warn("[Watcher] Errors append failed", e);
    }
  }

  onFileModify(file) {
    if (!file || !this.isDecisionWrapperPath(file.path)) return;
    this.app.vault.cachedRead(file).then((content) => {
      this.syncDecisionWrapper(file.path, content).catch((e) => {
        console.warn("[Watcher] syncDecisionWrapper error", e);
      });
    }).catch(() => {});
  }

  async syncDecisionWrapper(path, content) {
    const front = this.parseFrontmatter(content);
    if (front.approved !== true) return;
    const fmEnd = content.match(/^---\r?\n[\s\S]*?\r?\n---/);
    const body = fmEnd ? content.slice(fmEnd[0].length).replace(/^\r?\n+/, "") : content;
    const parsed = this.parseBodyForCheckedOption(body);
    const ts = new Date().toISOString().replace("T", " ").slice(0, 19);

    if (parsed === "conflict") {
      const logLine = `- ${ts}: Watcher conflict | wrapper: ${path} | reason: multiple checkboxes detected — no frontmatter written`;
      await this.appendToWrapperSyncLog(logLine);
      await this.appendToErrors(`### ${ts} — Multiple options checked\n| pipeline | severity | approval | timestamp | error_type |\n|----------|----------|----------|------------|------------|\n| wrapper-sync | medium | pending | ${ts} | conflict |\n\nMultiple options checked in wrapper ${path}. No frontmatter written.\n`);
      return;
    }
    if (parsed === "none") {
      const logLine = `- ${ts}: Watcher conflict | wrapper: ${path} | reason: no A–G checked but approved: true — no frontmatter written`;
      await this.appendToWrapperSyncLog(logLine);
      await this.appendToErrors(`### ${ts} — No option checked\n| pipeline | severity | approval | timestamp | error_type |\n|----------|----------|----------|------------|------------|\n| wrapper-sync | low | pending | ${ts} | no-option |\n\nNo A–G checked but approved: true in wrapper ${path}. Set re-wrap: true manually for re-wrap.\n`);
      return;
    }

    const { letter, path: extractedPath } = parsed;
    const approvedOption = letter;
    const approvedPath = (extractedPath || "").trim();
    const currentOption = (front.approved_option !== undefined && front.approved_option !== null) ? String(front.approved_option).replace(/^["']|["']$/g, "").toUpperCase() : "";
    const currentPath = (front.approved_path !== undefined && front.approved_path !== null) ? String(front.approved_path).trim() : "";

    if (currentOption === approvedOption && currentPath === approvedPath) {
      const logLine = `- ${ts}: Watcher skip | wrapper: ${path} | reason: frontmatter already matches parsed values`;
      await this.appendToWrapperSyncLog(logLine);
      return;
    }

    const fmMatch = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
    let newFmBlock = fmMatch ? fmMatch[1] : "";
    const pathEscaped = approvedPath.includes(":") || approvedPath.includes('"') ? `"${approvedPath.replace(/"/g, '\\"')}"` : approvedPath;
    const setLine = (key, val) => {
      const keyRegex = new RegExp(`^(${key}\\s*:\\s*).*`, "m");
      const line = `${key}: ${val}`;
      if (keyRegex.test(newFmBlock)) newFmBlock = newFmBlock.replace(keyRegex, line);
      else newFmBlock = newFmBlock.trimEnd() + (newFmBlock.trimEnd() ? "\n" : "") + line;
    };
    setLine("approved_option", approvedOption);
    setLine("approved_path", pathEscaped);
    const newContent = "---\n" + newFmBlock + "\n---\n" + body;
    await this.app.vault.adapter.write(path, newContent);
    const prevMatch = (currentOption && currentPath) ? "no" : "yes";
    const logLine = `- ${ts}: Watcher sync | wrapper: ${path} | action: set approved_option: ${approvedOption} | approved_path: ${approvedPath} | previous values matched: ${prevMatch}`;
    await this.appendToWrapperSyncLog(logLine);
  }

  // --- Signals ---
  async writeSignal(mode, fullPrompt) {
    const promptPreview = (fullPrompt || "").slice(0, 100);
    console.log(`[Watcher] writeSignal called – mode: ${mode}, prompt: ${promptPreview}${fullPrompt && fullPrompt.length > 100 ? "..." : ""}`);
    const requestId = (Date.now() + Math.random() * 1e9).toString(36);
    console.log(`[Watcher] Generated requestId: ${requestId}`);
    const escaped = (fullPrompt || "").replace(/"/g, '\\"');
    const line = `[${new Date().toISOString()}] requestId: ${requestId} | mode: ${mode} | prompt: "${escaped}"\n`;

    const vault = this.app.vault;
    let folder = vault.getAbstractFileByPath(RESOURCES_FOLDER);
    if (!folder) await vault.createFolder(RESOURCES_FOLDER);

    let existing = "";
    try {
      const f = vault.getAbstractFileByPath(this.signalFilePath);
      if (f) existing = await vault.read(f);
    } catch (_) {}
    if (!existing.trim()) existing = "# Watcher Signals\n";
    const newContent = existing.trimEnd() + "\n" + line.trim();
    await vault.adapter.write(this.signalFilePath, newContent);
    console.log("[Watcher] Signal appended successfully");
    return { requestId, fullPrompt };
  }

  async getQueuePendingCount() {
    let raw = "";
    try {
      const f = this.app.vault.getAbstractFileByPath(QUEUE_FILE);
      if (!f) return 0;
      raw = await this.app.vault.read(f);
    } catch (_) {
      return 0;
    }
    const lines = raw.split("\n").filter((l) => l.trim());
    let count = 0;
    for (const line of lines) {
      try {
        JSON.parse(line);
        count++;
      } catch (_) {}
    }
    return count;
  }

  async appendToQueue(mode, fullPrompt, sourceFile) {
    const requestId = (Date.now() + Math.random() * 1e9).toString(36);
    const modeNorm = (mode || "").replace(/\s+–\s+safe batch autopilot$/i, "").trim() || mode;
    const entry = {
      id: requestId,
      timestamp: new Date().toISOString(),
      mode: modeNorm,
      prompt: fullPrompt,
      source_file: sourceFile || "",
    };
    const line = JSON.stringify(entry) + "\n";

    const vault = this.app.vault;
    let folder = vault.getAbstractFileByPath(RESOURCES_FOLDER);
    if (!folder) await vault.createFolder(RESOURCES_FOLDER);

    let existing = "";
    try {
      const f = vault.getAbstractFileByPath(QUEUE_FILE);
      if (f) existing = await vault.read(f);
    } catch (_) {}
    // Dedup: same (prompt, source_file); if INGEST with empty source_file already in queue, skip adding another
    const existingEntries = existing.split("\n").filter((l) => l.trim());
    const modeNormForDedup = (mode || "").replace(/\s+–\s+safe batch autopilot$/i, "").trim() || mode;
    const isIngestBatch = modeNormForDedup === "INGEST MODE" && !(sourceFile || "").trim();
    for (const raw of existingEntries) {
      try {
        const o = JSON.parse(raw);
        const sameContent = (o.prompt === entry.prompt) && ((o.source_file || "") === (entry.source_file || ""));
        if (sameContent) return { requestId, skipped: true };
        if (isIngestBatch && (o.mode === "INGEST MODE" || (o.mode && o.mode.replace(/\s+–\s+safe batch autopilot$/i, "").trim() === "INGEST MODE")) && !(o.source_file || "").trim())
          return { requestId, skipped: true };
      } catch (_) {}
    }
    const newContent = (existing.trimEnd() ? existing.trimEnd() + "\n" : "") + line.trim();
    try {
      await vault.adapter.write(QUEUE_FILE, newContent);
    } catch (e) {
      console.warn("[Watcher] Queue write failed, retrying...", e);
      // On mobile, parent folder may not exist; ensure .technical exists then retry
      try {
        const technicalDir = ".technical";
        if (!vault.getAbstractFileByPath(technicalDir)) {
          await vault.createFolder(technicalDir);
          console.log("[Watcher] .technical folder created (appendToQueue fallback)");
        }
      } catch (_) {}
      await new Promise((r) => setTimeout(r, 500));
      try {
        await vault.adapter.write(QUEUE_FILE, newContent);
      } catch (e2) {
        new Notice("Watcher: Could not write to queue. Try again.");
        console.error("[Watcher] Queue write failed after retry", e2);
        return { requestId: null };
      }
    }
    console.log("[Watcher] Appended to queue – requestId:", requestId);
    return { requestId };
  }

  async appendToTaskQueue(entry) {
    const vault = this.app.vault;
    let folder = vault.getAbstractFileByPath(RESOURCES_FOLDER);
    if (!folder) await vault.createFolder(RESOURCES_FOLDER);

    let existing = "";
    try {
      const f = vault.getAbstractFileByPath(TASK_QUEUE_FILE);
      if (f) existing = await vault.read(f);
    } catch (_) {}
    const line = JSON.stringify(entry) + "\n";
    const newContent = existing.trimEnd() + (existing.trimEnd() ? "\n" : "") + line;
    try {
      await vault.adapter.write(TASK_QUEUE_FILE, newContent);
      console.log("[Watcher] Appended to task queue – mode:", entry.mode, "requestId:", entry.requestId);
      return { requestId: entry.requestId };
    } catch (e) {
      console.warn("[Watcher] Task queue write failed", e);
      new Notice("Watcher: Could not write to task queue.");
      return { requestId: null };
    }
  }

  async appendToMobilePending(text) {
    const vault = this.app.vault;
    let folder = vault.getAbstractFileByPath(RESOURCES_FOLDER);
    if (!folder) await vault.createFolder(RESOURCES_FOLDER);
    let existing = "";
    try {
      const f = vault.getAbstractFileByPath(MOBILE_PENDING_FILE);
      if (f) existing = await vault.read(f);
    } catch (_) {}
    const line = `- [${new Date().toISOString()}] ${text}\n`;
    const newContent = existing.trimEnd() + (existing.trimEnd() ? "\n" : "") + line;
    try {
      await vault.adapter.write(MOBILE_PENDING_FILE, newContent);
    } catch (e) {
      console.warn("[Watcher] Mobile pending write failed", e);
    }
  }

  formatQueueForEatCache(entries, opts = {}) {
    const vaultRoot = opts.vaultRoot != null ? opts.vaultRoot : "(open this vault in Cursor as workspace)";
    const summary = entries.length === 1 ? "1 pending prompt" : `${entries.length} pending prompts`;
    const modesBreakdown = entries.reduce((acc, e) => {
      acc[e.mode] = (acc[e.mode] || 0) + 1;
      return acc;
    }, {});
    const sourceCounts = entries.reduce((acc, e) => {
      const p = e.source_file || "(none)";
      acc[p] = (acc[p] || 0) + 1;
      return acc;
    }, {});
    const topSourceFiles = Object.entries(sourceCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([path]) => path);

    const constraints = `  - Never delete core notes (Watcher-Signal, Watcher-Result, queue file, Backups).
  - Prefer appends over overwrites (e.g. Watcher-Result, logs).
  - Preserve YAML frontmatter in existing notes when editing.
  - Log changes verbosely; append to 3-Resources/processed-results.log or provide block for manual append.`;

    const instructions = `  - Cross-reference all queued prompts for duplicates (e.g., same requestId or similar content).
  - If multiple prompts reference the same source_file, group and execute them in optimal order (e.g., distill first, then express/archive if applicable) to minimize mutilation/overwrites of core data in the vault.
  - Build a step-by-step plan to process the queue: For each unique/grouped entry, apply the mode (distill/express/archive), incorporate file content/user input from the prompt, and output results in a format appendable to Watcher-Result.md (e.g., requestId: <id> | status: success | message: "<processed output>" | completed: <ISO8601>).
  - Optimize for efficiency: Deduplicate, batch similar operations, avoid redundant file reads/writes.
  - After planning, execute the plan and provide final outputs/log for manual append to vault (or to 3-Resources/processed-results.log).`;

    const promptLines = entries
      .map((e) => {
        const promptEscaped = (e.prompt || "")
          .replace(/\\/g, "\\\\")
          .replace(/"/g, '\\"')
          .replace(/\n/g, "\\n");
        const sf = (e.source_file || "").replace(/"/g, '\\"');
        return `  - id: ${e.id}\n    timestamp: "${e.timestamp}"\n    mode: ${e.mode}\n    prompt: "${promptEscaped}"\n    source_file: "${sf}"`;
      })
      .join("\n");

    const modesYaml = Object.entries(modesBreakdown)
      .map(([k, v]) => `  ${k}: ${v}`)
      .join("\n");
    const topFilesYaml = topSourceFiles.map((p) => `  - "${p.replace(/"/g, '\\"')}"`).join("\n");

    return `---
mode: EAT-CACHE
vault_root: ${vaultRoot}
pending_count: ${entries.length}
queue_summary: ${summary}
modes_breakdown:
${modesYaml}
top_source_files:
${topFilesYaml}
constraints: |
${constraints.split("\n").map((l) => "  " + l).join("\n")}
instructions: |
${instructions.split("\n").map((l) => "  " + l).join("\n")}
queued_prompts:
${promptLines}
---
`;
  }

  async runEatCache(opts = {}) {
    const vault = this.app.vault;
    let raw = "";
    try {
      const f = vault.getAbstractFileByPath(QUEUE_FILE);
      if (!f) {
        new Notice("Watcher: Queue is empty (no file).");
        return;
      }
      raw = await vault.read(f);
    } catch (e) {
      new Notice("Watcher: Could not read queue.");
      console.warn("[Watcher] EAT-CACHE read error", e);
      return;
    }

    const lines = raw.split("\n").filter((l) => l.trim());
    const entries = [];
    for (const line of lines) {
      try {
        entries.push(JSON.parse(line));
      } catch (_) {}
    }

    if (entries.length === 0) {
      new Notice("Watcher: Queue is empty or malformed.");
      return;
    }

    new Notice(`Pending: ${entries.length}`);

    const seen = new Set();
    const deduped = entries.filter((e) => {
      const key = (e.id || "") + "|" + (e.prompt || "") + "|" + (e.source_file || "");
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });

    let filtered = deduped;
    if (opts.filter === "distill") {
      filtered = deduped.filter((e) => /distill/i.test(e.mode || ""));
    } else if (opts.filter && opts.filter !== "all") {
      filtered = deduped.filter((e) => (e.source_file || "") === opts.filter);
    }

    if (filtered.length === 0) {
      new Notice("Watcher: No entries after filter.");
      return;
    }

    const vaultRoot = this.app.vault.adapter?.basePath ?? "(open this vault in Cursor as workspace)";
    const payload = this.formatQueueForEatCache(filtered, { vaultRoot });
    try {
      await navigator.clipboard.writeText(payload);
      new Notice(`Queue copied to clipboard (${filtered.length} entries). Paste into Cursor plan mode.`);
      console.log("[Watcher] EAT-CACHE: copied", filtered.length, "entries to clipboard");
    } catch (e) {
      new Notice("Watcher: Could not copy to clipboard.");
      console.warn("[Watcher] EAT-CACHE clipboard error", e);
    }
  }

  async clearQueue(archiveFirst = false) {
    const vault = this.app.vault;
    let raw = "";
    try {
      const f = vault.getAbstractFileByPath(QUEUE_FILE);
      if (!f) {
        new Notice("Watcher: Queue is already empty.");
        return;
      }
      raw = await vault.read(f);
    } catch (_) {
      new Notice("Watcher: Could not read queue.");
      return;
    }

    if (archiveFirst && raw.trim()) {
      const ts = new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19);
      const archivePath = ".technical/prompt-queue.done." + ts + ".jsonl";
      try {
        await vault.adapter.write(archivePath, raw.trimEnd() ? raw.trimEnd() + "\n" : "");
      } catch (_) {}
    }

    try {
      await vault.adapter.write(QUEUE_FILE, "");
      new Notice("Watcher: Queue cleared.");
      console.log("[Watcher] Queue cleared.");
    } catch (e) {
      new Notice("Watcher: Could not clear queue.");
      console.warn("[Watcher] Clear queue error", e);
    }
  }

  async appendTimingEvent(event, requestId) {
    try {
      const vault = this.app.vault;
      let folder = vault.getAbstractFileByPath(RESOURCES_FOLDER);
      if (!folder) await vault.createFolder(RESOURCES_FOLDER);
      let existing = "";
      try {
        const f = vault.getAbstractFileByPath(TIMING_LOG_FILE);
        if (f) existing = await vault.read(f);
      } catch (_) {}
      const line = `[${new Date().toISOString()}] requestId: ${requestId} | event: ${event}\n`;
      const newContent = existing.trimEnd() + (existing ? "\n" : "") + line.trim();
      await vault.adapter.write(TIMING_LOG_FILE, newContent);
    } catch (e) {
      console.warn("[Watcher] Could not append timing log:", e.message);
    }
  }

  checkForSignals() {
    (async () => {
      try {
        const f = this.app.vault.getAbstractFileByPath(this.signalFilePath);
        if (!f) return;
        const content = await this.app.vault.read(f);
        const lines = content.split("\n").filter((l) => l.includes("requestId:"));
        const last = lines[lines.length - 1];
        if (!last) return;
        const m = last.match(/requestId:\s*(\w+)/);
        if (!m) return;
        const id = m[1];
        if (id && id !== this.lastRequestId) {
          this.lastRequestId = id;
          console.log("[Watcher] New signal detected via polling:", last);
          new Notice("Watcher: New signal detected!");
          await this.appendTimingEvent("seen", id);

          // When running on a device with the Cursor bridge enabled (typically desktop),
          // automatically hand the latest signal off to Cursor and start completion polling.
          const promptMatch = last.match(/prompt:\s*"(.*)"$/);
          const rawPromptEscaped = promptMatch ? promptMatch[1] : "";
          const fullPrompt = rawPromptEscaped.replace(/\\"/g, '"');
          if (this.cursorBridgeEnabled && fullPrompt) {
            console.log("[Watcher] Bridge enabled – attempting dispatch from signal poll");
            const success = await this.attemptCursorBridge(id, fullPrompt);
            if (success) {
              console.log("[Watcher] Dispatch success – starting completion polling (signal poll)");
              this.startCompletionWait(id, COMPLETION_TIMEOUT_MS, (status, message, trace) => {
                this.showCompletionPopup(status, message, trace);
              });
            } else {
              console.warn("[Watcher] Dispatch failed – no polling (signal poll)");
            }
          }
        }
      } catch (_) {}
    })();
  }

  // --- Bridge: URI → clipboard → request file ---
  async attemptCursorBridge(requestId, fullPrompt) {
    if (!this.cursorBridgeEnabled) return false;
    if (!this.hasShownBridgeNotice) {
      new Notice("Cursor bridge ACTIVE");
      this.hasShownBridgeNotice = true;
      console.log("[Watcher] Bridge first use – notice shown");
    }

    console.log("[Watcher] Bridge attempt started – requestId:", requestId);

    // Official Cursor prompt deeplink per https://cursor.com/docs/integrations/deeplinks
    // Also try the legacy deeplink scheme used by earlier Cursor builds.
    // Regardless of URI behavior, also fall back to clipboard + request file so the
    // prompt is always available somewhere.
    const encodedPrompt = encodeURIComponent(fullPrompt);
    const deeplinks = [
      `cursor://anysphere.cursor-deeplink/prompt?text=${encodedPrompt}`, // current official
      `cursor://default?prompt=${encodedPrompt}`, // legacy
    ];

    let uriOpened = false;
    for (const uri of deeplinks) {
      try {
        console.log(
          "[Watcher] Trying URI:",
          uri.slice(0, 80) + (uri.length > 80 ? "..." : "")
        );
        window.open(uri, "_blank");
        uriOpened = true;
      } catch (e) {
        console.warn("[Watcher] URI failed:", e.message);
      }
    }

    // Clipboard fallback
    try {
      await navigator.clipboard.writeText(fullPrompt);
      console.log("[Watcher] Clipboard fallback: prompt copied");
      new Notice("Watcher: Prompt copied to clipboard");
    } catch (e) {
      console.warn("[Watcher] Clipboard failed:", e.message);
    }

    // Request file fallback (always try so Cursor can read it from the vault)
    try {
      const path = "3-Resources/Watcher-Request.md";
      const content = `# Watcher request ${requestId}\n\n${fullPrompt}\n`;
      await this.app.vault.adapter.write(path, content);
      console.log("[Watcher] Request file created as fallback");
      new Notice("Watcher: Prompt written to 3-Resources/Watcher-Request.md");
    } catch (e) {
      console.error("[Watcher] Request file write failed:", e);
    }

    if (uriOpened) {
      console.log("[Watcher] At least one Cursor URI attempted");
      return true;
    }

    // Even if URIs failed, clipboard and/or request file give you the prompt.
    // Return true so callers will still start completion polling.
    return true;
  }

  // --- Completion detection (file-based polling) ---
  startCompletionWait(requestId, timeoutMs, callback) {
    console.log(`[Watcher] Starting completion wait – requestId: ${requestId}, timeout 15min`);
    const start = Date.now();
    if (this._pollInterval) clearInterval(this._pollInterval);

    const poll = async () => {
      const elapsed = Math.round((Date.now() - start) / 1000);
      console.log(`[Watcher] Polling result file for ${requestId}... (${elapsed}s elapsed)`);

      if (Date.now() - start > timeoutMs) {
        clearInterval(this._pollInterval);
        this._pollInterval = null;
        console.log("[Watcher] Timeout reached – no completion signal");
        callback("timeout", `No result file after ${Math.round(timeoutMs / 60000)} min`, `requestId: ${requestId}`);
        return;
      }

      try {
        const f = this.app.vault.getAbstractFileByPath(this.resultFilePath);
        if (!f) return;
        const content = await this.app.vault.read(f);
        const line = content.split("\n").find((l) => l.includes(`requestId: ${requestId}`) && (l.includes("status: success") || l.includes("status: failure")));
        if (!line) return;

        clearInterval(this._pollInterval);
        this._pollInterval = null;

        const statusMatch = line.match(/status:\s*(success|failure)/);
        const status = statusMatch ? statusMatch[1] : "failure";
        console.log("[Watcher] Completion detected:", status);
        const msgM = line.match(/message:\s*"((?:[^"\\]|\\.)*)"/);
        const traceM = line.match(/trace:\s*"((?:[^"\\]|\\.)*)"/);
        const message = msgM ? msgM[1].replace(/\\"/g, '"') : (status === "success" ? "Cursor run completed successfully." : "Run finished with failure.");
        const trace = traceM ? traceM[1].replace(/\\"/g, '"') : "";
        callback(status, message, trace);
      } catch (_) {}
    };

    this._pollInterval = setInterval(poll, COMPLETION_POLL_MS);
    poll();
  }

  showCompletionPopup(status, message, trace) {
    const tracePreview = trace ? trace.slice(0, 200) + (trace.length > 200 ? "..." : "") : "none";
    console.log(`[Watcher] Showing completion popup – status: ${status}, trace: ${tracePreview}`);
    const title = status === "success" ? "Done" : status === "failure" ? "Failed" : "Timeout";
    new CompletionPopupModal(this.app, title, message, trace, status).open();
  }
};
