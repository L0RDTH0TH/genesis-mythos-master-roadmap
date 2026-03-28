<%*
const templates = {
  "Stray Thoughts": "[[Templates/Ingest/By-Type/Stray-Thoughts]]",
  "AI Output": "[[Templates/Ingest/By-Type/AI-Output]]",
  "Link Note": "[[Templates/Ingest/By-Type/Link-Note]]",
};

const displayNames = Object.keys(templates);
const linkValues = Object.values(templates);

const selectedLink = await tp.system.suggester(
  displayNames,
  linkValues,
  false,
  "Select ingest type for this note… (Esc to cancel)"
);

if (selectedLink) {
  // Capture and append the returned content so it appears in the note
  tR += await tp.file.include(selectedLink);
} else {
  const created = tp.date.now("YYYY-MM-DD HH:mm");
  tR += `---
created: ${created}
tags: [ingest, raw-capture, no-template]
para-type: Ingest
status: ingest
---

# No template selected

Paste your raw capture here. You can refactor or re-template this later.
`;
}
%>
