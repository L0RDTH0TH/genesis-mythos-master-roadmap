---
title: Attachment Subtype Mapping
created: 2026-03-01
tags: [second-brain, ingest, attachments, config]
para-type: Resource
status: active
---

# Attachment Subtype Mapping

Single source of truth for **file extension → 5-Attachments subfolder** when ingesting non-markdown files from Ingest/. Referenced by [non-markdown-handling](.cursor/rules/context/non-markdown-handling.mdc) and ingest pipeline. If this file is missing, the rule falls back to the table in the rule.

## Mapping table

| Extension(s) | Subfolder (under 5-Attachments/) |
| ------------ | --------------------------------- |
| .png, .jpg, .jpeg, .gif, .webp, .svg, .bmp | Images/ |
| .pdf | PDFs/ |
| .docx, .xlsx, .pptx | Documents/ |
| .mp3, .wav, .m4a, .ogg, .flac, .webm, .mp4, .mov, .avi, .mkv | Audio/ |
| .zip, .tar, .gz, .7z | Other/ |
| .txt, .csv, .json, .py, .js, .ts, .md (non-note), .xml, .yaml, .yml | Other/ |

**Unknown extensions** default to **Other/**; the pipeline logs a suggestion to add them here (e.g. for future `.heic` or new types).

## Edge cases

- **.md.txt** or double extensions: treat as text → Other/.
- **Very large files** (e.g. >100MB): optional warning in companion or log; move logic unchanged unless a separate rule is added.

## Customization

Edit this note to add or change rows. Keep one row per subtype; list multiple extensions in the first column. Subfolders must be one of: Images/, PDFs/, Documents/, Audio/, Other/.
