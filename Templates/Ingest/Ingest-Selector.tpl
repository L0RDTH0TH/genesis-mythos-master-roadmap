<%*
// Paths: flat Templates/ (use "Templates/Ingest/Stray-Thoughts.md" etc. if you use that subfolder)
const templates = {
  "Stray Thoughts": "Templates/Ingest/By-Type/Stray-Thoughts.md",
  "AI Output": "Templates/Ingest/By-Type/AI-Output.md",
  "Link Note": "Templates/Ingest/By-Type/Link-Note.md",
};

const displayNames = Object.keys(templates);
const paths = Object.values(templates);

const selectedPath = await tp.system.suggester(displayNames, paths, false, "Select ingest type…");
%>

<%*
if (selectedPath) {
  tR += await tp.file.include(selectedPath);
} else {
  const created = tp.date.now("YYYY-MM-DD HH:mm");
  const title = tp.file.title;
  tR += `---
title: "${title}"
created: "${created}"
tags: [ingest, raw-capture, no-template]
para-type: Ingest
status: ingest
ingest-type: raw-capture
---

# No template selected

Paste your raw capture here.
`;
}
%>
