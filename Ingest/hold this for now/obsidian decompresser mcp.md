---
proposal_path: Ingest/Decisions/Decision-for-obsidian-decompresser-mcp--2026-03-04-0440.md
---
## TL;DR
NetworkChuck's MCP Server Builder Prompt

---

NetworkChuck's MCP Server Builder Prompt

## INITIAL CLARIFICATIONS

Before generating the MCP server, please provide:

### 1. Service/Tool Name
The MCP server will integrate with the *Smart Composer* Obsidian plugin to decompose an Obsidian vault (used as a PRD) into individual AI prompts for the *Windsurf* coding agent. It will leverage Obsidian’s structure to break the vault into logical chunks, cross-reference related content, and tag chunks with relevant metadata (e.g., linking "Character Customization" and "Character Customization System").

### 2. API Documentation
- **Obsidian Local REST API** (coddingtonbear): [https://github.com/coddingtonbear/obsidian-local-rest-api](https://github.com/coddingtonbear/obsidian-local-rest-api)  
  - Interactive Docs: [https://coddingtonbear.github.io/obsidian-local-rest-api/](https://coddingtonbear.github.io/obsidian-local-rest-api/)  
- **Obsidian Local REST API** (j-shelfwood, Laravel-based): [https://github.com/j-shelfwood/obsidian-local-rest-api](https://github.com/j-shelfwood/obsidian-local-rest-api)  
- **Obsidian Local REST API MCP** (AI-Native): [https://github.com/j-shelfwood/obsidian-local-rest-api-mcp](https://github.com/j-shelfwood/obsidian-local-rest-api-mcp)  
- **Smart Composer MCP Support**: [https://github.com/glowingjade/obsidian-smart-composer](https://github.com/glowingjade/obsidian-smart-composer) (MCP section for local tool integrations).

### 3. Required Features
- **Vault Parsing**: Automatically parse an Obsidian vault into logical chunks for AI prompts.  
- **Metadata Tagging**: Tag chunks with metadata (e.g., linking related files like "Character Customization" and "Character Customization System").  
- **Cross-Referencing**: Link related vault content for comprehensive prompts.  
- **Task Grouping by Relevancy**: Group tasks into 3 levels:  
  - Level 1: High priority (immediate action).  
  - Level 2: Medium priority (address soon).  
  - Level 3: Low priority (deferrable).  
- **Sub-Task Breakdown**: Break each task into 3 sub-tasks, with an option to manually expand sub-tasks later for added granularity.  
- **Smart Composer Integration**: Integrate with *Smart Composer* for *Windsurf* prompt generation.  
- **Prompt Optimization**: Create clear, context-rich prompts for the AI coding agent.  
- **Index File Support**: Use an index file to track metadata links and relationships.  
- **Error Handling**: Handle invalid vault structures or missing metadata.

### 4. Authentication
- **API Keys**: Required for Obsidian Local REST API (see [coddingtonbear’s documentation](https://github.com/coddingtonbear/obsidian-local-rest-api)).  
- **No OAuth**: Not required, but authentication may vary by implementation (e.g., Laravel-based or AI-Native).  
- **Local Tool Access**: *Smart Composer* and *Windsurf* may require local configuration or API tokens per their documentation.

### 5. Data Sources
- **Obsidian Vault**: Primary source with markdown files structured as a PRD.  
- **Index File**: Tracks metadata links and relationships within the vault.  
- **Obsidian Local REST API**: Used for programmatic vault content extraction and processing.

If any information is missing or unclear, I will ask for clarification before proceeding.

---

## Review Needed
Proposed para-type: resource. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.