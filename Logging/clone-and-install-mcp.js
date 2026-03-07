#!/usr/bin/env node
/**
 * Clone cyanheads/obsidian-mcp-server into mcp-server/ and run npm install.
 * Logs every step to mcp-setup-log.md. Safe to re-run (skips clone if already present).
 * Run from vault root: node clone-and-install-mcp.js
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const VAULT_ROOT = process.cwd();
const MCP_DIR = path.join(VAULT_ROOT, 'mcp-server');
const LOG_FILE = path.join(VAULT_ROOT, 'mcp-setup-log.md');
const REPO_URL = 'https://github.com/cyanheads/obsidian-mcp-server.git';

function ts() {
  return new Date().toISOString().replace('T', ' ').slice(0, 19);
}

function appendLog(line) {
  const entry = `- ${ts()} | ${line}\n`;
  // Append before the final "## Entries" content; we append to the end of file
  fs.appendFileSync(LOG_FILE, entry, 'utf8');
  console.log(line);
}

function run(cmd, cwd = VAULT_ROOT) {
  return execSync(cmd, { cwd, encoding: 'utf8', stdio: 'pipe' });
}

function main() {
  appendLog('Action: clone-and-install-mcp.js started | Result: in_progress | Notes: cwd=' + VAULT_ROOT);

  const hasPackageJson = fs.existsSync(path.join(MCP_DIR, 'package.json'));

  if (hasPackageJson) {
    appendLog('Action: skip clone (mcp-server/ already has package.json) | Result: skipped | Notes: running npm install only');
  } else {
    if (!fs.existsSync(MCP_DIR)) {
      fs.mkdirSync(MCP_DIR, { recursive: true });
      appendLog('Action: created mcp-server/ | Result: success');
    }
    const cloneDir = path.join(VAULT_ROOT, 'obsidian-mcp-server-clone');
    try {
      run(`git clone ${REPO_URL} "${cloneDir}"`);
      appendLog('Action: git clone obsidian-mcp-server | Result: success');
      // Move contents into mcp-server (so mcp-server gets package.json, src/, etc.)
      const entries = fs.readdirSync(cloneDir, { withFileTypes: true });
      for (const e of entries) {
        const src = path.join(cloneDir, e.name);
        const dest = path.join(MCP_DIR, e.name);
        fs.renameSync(src, dest);
      }
      fs.rmdirSync(cloneDir);
      appendLog('Action: moved repo contents into mcp-server/ | Result: success');
    } catch (err) {
      appendLog('Action: git clone or move | Result: failure | Notes: ' + (err.message || String(err)).slice(0, 200));
      console.error(err);
      process.exit(1);
    }
  }

  try {
    run('npm install', MCP_DIR);
    appendLog('Action: npm install in mcp-server/ | Result: success');
  } catch (err) {
    appendLog('Action: npm install in mcp-server/ | Result: failure | Notes: ' + (err.message || String(err)).slice(0, 200));
    console.error(err);
    process.exit(1);
  }

  appendLog('Action: clone-and-install-mcp.js finished | Result: success');
}

main();
