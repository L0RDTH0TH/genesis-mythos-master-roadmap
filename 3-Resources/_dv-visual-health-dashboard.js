const { dv } = input;

if (!dv) {
  dv.paragraph("Error: dv object not passed to view script.");
  return;
}

function isCoreNote(p) {
  const path = p.file.path;
  if (path.startsWith("4-Archives/") || path.startsWith("Backups/") || path.startsWith("Templates/") || path.startsWith("Ingest/")) return false;
  if (path.match(/Log.*\.md$/) || path.match(/Hub\.md$/)) return false;
  return path.startsWith("1-Projects/") || path.startsWith("2-Areas/") || path.startsWith("3-Resources/");
}

const corePages = dv.pages().where(isCoreNote);
if (corePages.length > 1500) {
  dv.paragraph("⚠️ Vault too large for full content scan — consider backfilling frontmatter fields.");
  return;
}
const total = corePages.length;

function hasNextActions(p) {
  const val = p["next-actions"];
  if (!val) return false;
  if (Array.isArray(val)) return val.length > 0;
  return String(val).trim().length > 0;
}

dv.paragraph(`**Core notes scanned:** ${total}`);

// --- Section 1: TL;DR coverage ---
let withTldr = 0;
for (let p of corePages) {
  const content = await dv.io.load(p.file.path);
  if (!content) continue;
  if (content.match(/>\s*\[!summary\]\s*[\s-]*TL;DR/i) || content.match(/##\s*TL;DR/i) || content.match(/>\s*TL;DR/i)) {
    withTldr++;
  }
}
const percentage = total > 0 ? Math.round((withTldr / total) * 100) : 0;
dv.paragraph(`**${percentage}%** of core notes have a TL;DR (${withTldr} / ${total})`);
const status = percentage >= 85 ? "🟢 Good" : percentage >= 60 ? "🟡 Fair" : "🔴 Needs work";
dv.paragraph(`Progress: **${status}**`);

// --- Section 2: Highlightr usage by color (inline CSS + legacy ^{Color}) ---
// Hex-to-color mapping from Highlightr-Color-Key.md Section 2 (inline CSS)
const hexToColor = {
  "#fff3a3a6": "Yellow", "#c1e1c1a6": "Green", "#a3d8ffa6": "Blue", "#ffaaaaa6": "Red",
  "#ffd9a3a6": "Orange", "#e6ccffa6": "Purple", "#ffc1cca6": "Pink", "#a3ffffa6": "Cyan", "#e0e0e0a6": "Grey"
};
function hasLegacyColor(content, colorName) {
  return content && content.match(new RegExp(`\\^\\{${colorName.trim()}\\}`, 'i'));
}
function getInlineHexes(content) {
  if (!content) return [];
  const hexes = [];
  /* Match <mark ... style="background: #HEX"> (allows data-highlight-source="agent" etc.) */
  const re = /<mark\s+(?:[^>]*?\s+)?style="background:\s*(#[0-9A-Fa-f]{8})"/g;
  let m;
  while ((m = re.exec(content)) !== null) hexes.push(m[1].toLowerCase());
  return hexes;
}

const colors = ["Red", "Orange", "Yellow", "Green", "Blue", "Purple", "Cyan", "Pink", "Grey"];
const counts = {};
for (let c of colors) counts[c] = 0;

for (let p of corePages) {
  const content = await dv.io.load(p.file.path);
  if (!content) continue;
  const usedColors = new Set();
  for (let c of colors) {
    if (hasLegacyColor(content, c)) usedColors.add(c);
  }
  const hexes = getInlineHexes(content);
  for (const hex of hexes) {
    if (hexToColor[hex]) usedColors.add(hexToColor[hex]);
  }
  for (const c of usedColors) counts[c] = (counts[c] || 0) + 1;
}

dv.header(3, "Notes using each color (at least once)");
dv.paragraph("*Counts combine inline CSS and legacy `^{Color}` format.*");
const sortedColors = Object.entries(counts).sort((a, b) => b[1] - a[1]);
for (let [color, num] of sortedColors) {
  if (num > 0) {
    dv.paragraph(`**${color}**: ${num} notes`);
  }
}

// --- Section 4: Per-project / per-folder highlight table ---
const groups = {};
for (let p of corePages) {
  const folder = p.file.folder || "";
  const group = folder ? folder.split("/")[0] : (p.file.path ? p.file.path.split("/")[0] : "Other");
  if (!groups[group]) {
    groups[group] = { pages: [], total: 0, colors: {} };
    for (let c of colors) groups[group].colors[c] = 0;
  }
  groups[group].pages.push(p);
  groups[group].total++;
}

const tableColors = ["Red", "Orange", "Yellow", "Green", "Blue", "Purple"];
for (let groupName of Object.keys(groups)) {
  const data = groups[groupName];
  for (let p of data.pages) {
    const content = await dv.io.load(p.file.path);
    if (!content) continue;
    const usedColors = new Set();
    for (let c of tableColors) {
      if (hasLegacyColor(content, c)) usedColors.add(c);
    }
    const hexes = getInlineHexes(content);
    for (const hex of hexes) {
      if (hexToColor[hex] && tableColors.includes(hexToColor[hex])) usedColors.add(hexToColor[hex]);
    }
    for (const c of usedColors) data.colors[c]++;
  }
}

const rows = [];
for (let [groupName, data] of Object.entries(groups)) {
  let alert = "";
  let maxColorPct = 0;
  let dominantColor = "";
  for (let c of tableColors) {
    const pct = data.total > 0 ? (data.colors[c] / data.total) : 0;
    if (pct > maxColorPct) {
      maxColorPct = pct;
      dominantColor = c;
    }
  }
  if (maxColorPct > 0.5) {
    alert = `⚠️ ${dominantColor}-heavy (${Math.round(maxColorPct * 100)}%)`;
  } else if (Object.values(data.colors).every(v => v === 0)) {
    alert = "No highlights";
  }
  rows.push([
    groupName,
    data.total,
    ...tableColors.map(c => data.colors[c]),
    alert
  ]);
}

dv.header(3, "Highlight patterns by folder (top-level PARA)");
dv.table(["Group", "Total Notes", ...tableColors, "Alert"], rows);
dv.paragraph("*Per-folder counts combine inline CSS and legacy `^{Color}`.*");

// --- Graph health score ---
let totalOutlinks = 0;
let withGraphFrontmatter = 0;
for (const p of corePages) {
  const outlinks = p.file.outlinks;
  totalOutlinks += (outlinks && outlinks.length) ? outlinks.length : 0;
  if (p["graph"] != null || (typeof p["graph"] === "object" && Object.keys(p["graph"] || {}).length > 0)) withGraphFrontmatter++;
}
const avgLinkDensity = total > 0 ? (totalOutlinks / total).toFixed(1) : 0;
const graphPct = total > 0 ? Math.round((withGraphFrontmatter / total) * 100) : 0;
dv.header(2, "Graph health");
dv.paragraph(`**Avg outlinks per note:** ${avgLinkDensity}  |  **Notes with graph frontmatter:** ${withGraphFrontmatter} (${graphPct}%)`);

// --- Section 3: Actionable summary (in script so dashboard only needs DQL list) ---
dv.header(2, "Actionable Summary");
const ns = corePages.where(p => p["needs-simplify"] === true).length;
const rc = corePages.where(p => p["resurface-candidate"] === true).length;
const na = corePages.where(p => hasNextActions(p)).length;
dv.paragraph(`**needs-simplify:** ${ns}  |  **resurface-candidate:** ${rc}  |  **next-actions (non-empty):** ${na}`);
