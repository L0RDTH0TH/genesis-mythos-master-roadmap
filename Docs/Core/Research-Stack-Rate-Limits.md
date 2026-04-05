---
title: Research Stack Rate Limits
created: 2026-03-15
tags: [second-brain, research, mcp, rate-limits]
para-type: Resource
status: active
---

**TL;DR** — The research-agent-run skill respects **research_result_limit** and avoids burst; it does not enforce numeric rate limits. Use this table for operator awareness and capacity planning.

---

## Rate limits (research pipeline tools)

| Service / tool | Type | Rate / volume limit | Notes |
|----------------|------|----------------------|--------|
| **Semantic Scholar API** | Free, no key | **100 requests / 5 min** (per IP) | ~1 req every 3 s. 429/500 if exceeded. |
| **Semantic Scholar API** | Free, with API key | **~100 requests / s** | Free key from api.semanticscholar.org. |
| **arXiv API** | Free | **~3 requests / s** (de facto); **1,000 results max per query** | Use pagination; avoid burst. |
| **Crossref REST API** | Free (polite pool) | **10 req/s** (single DOI); **3 req/s** (list/query) | Send mailto (or User-Agent) for polite pool. |
| **Firecrawl (self-hosted)** | OSS / self-hosted | **None** | Limited by your server only. |
| **Browser MCP / browser-tools** | Self-hosted OSS | **None** | Limited by local machine and target sites. |
| **mcp_web_fetch** | Built-in | **Not documented** | Depends on Cursor/host. |

---

## Guidance

- **Skill behavior:** The skill caps total discovery calls (e.g. 3–5) and respects **research_result_limit** (default 3–5, up to 5–7 when util-driven). It does not enforce the exact numbers above; operators use this table for capacity planning and to avoid hitting provider limits under heavy use.
- **Optional API key:** For Semantic Scholar, set `SEMANTIC_SCHOLAR_API_KEY` (or the env var required by your Semantic Scholar MCP) for higher rate limit when running many academic queries.
