---
description: "On INGEST MODE / Process Ingest / run ingests, ingest behavior is handled by IngestSubagent (agents/ingest.mdc). This file is a redirect only."
globs: "*"
alwaysApply: true
---

# always-ingest-bootstrap

When the user says **"INGEST MODE"**, **"Process Ingest"**, or **"run ingests"**, ingest processing is handled by the **IngestSubagent** ([agents/ingest.mdc](.cursor/rules/agents/ingest.mdc)). No ingest logic here; routing is via system-funnels and dispatcher to IngestSubagent.
