### What We Want to Keep and Add for the Virginal State Test Vault

To simulate a "fresh install" as if a new user just bought the software (launch readiness testing), we'll build a minimal, self-contained vault that bootstraps itself with the core automations. This means **no pre-existing manual data entries** (e.g., no user-captured notes), but include all structural, configurational, and instructional elements needed for seamless onboarding. The vault should feel "plug-and-play": a new user opens it, follows minimal manual steps (documented in .md files), and the system is ready to ingest their first captures.

**Keep (from existing setup, but minimized):**
- **Core file structure**: PARA folders (1-Projects/, 2-Areas/, 3-Resources/, 4-Archives/), Ingest/, Backups/ (with subdirs Per-Change/ and Batch/), Versions/.
- **Cursor integration**: `.cursor/rules/` (always/ and context/ subdirs with .mdc files like mcp-obsidian-integration.mdc, ingest-processing.mdc, etc.), `.cursor/skills/` (with SKILL.md files for frontmatter-enrich, subfolder-organize, etc.).
- **MCP config**: mcp.json (or equivalent) in a documented location (e.g., root or .obsidian/), with defaults for vault path, backup dir, serverIdentifier, etc.
- **Plugin configs**: Pre-configured .obsidian/ folder with essentials (see below).
- **Documentation .md files**: Key reports like Second-Brain-Automations-Setup-Report.md, Cursor-Skill-Pipelines-Reference.md, Automation-Flows-MCP-Improvements.md — placed in 3-Resources/ for easy access.
- **Safety defaults**: Ensure ensure_backup max_age_minutes: 1440, dry_run: true enforcement, health_check periodic calls.

**Add (for onboarding focus):**
- **Onboarding-specific files**: 
  - `0-Onboarding/Welcome-to-Second-Brain.md` (main guide: quick-start steps, trigger phrases, how to capture first note).
  - `0-Onboarding/Install-Steps.md` (manual steps: install Obsidian plugins, start MCP server, open in Cursor).
  - `0-Onboarding/Basic-Examples.md` (seed templates: empty Project/Area/Resources notes with frontmatter examples).
- **Basic seed content**: Minimal, automation-friendly examples to demonstrate pipelines without manual data:
  - One empty Project note in 1-Projects/ (e.g., "Project-Template.md" with frontmatter like project-id, highlight_key).
  - One empty Area note in 2-Areas/ (e.g., "Area-Template.md").
  - One Resource hub in 3-Resources/ (e.g., "Resources-Hub.md" with Dataview query placeholders).
- **Param settings**: Defaults in mcp.json or a new `3-Resources/Config-Defaults.md` (e.g., confidence bands: low <72%, mid 72–84%, high ≥85%; Highlightr color schemes: analogous/complementary mappings).
- **MCP tools docs**: All tools (e.g., obsidian_subfolder_organize, calibrate_confidence) documented in .md files within `.cursor/skills/` or 3-Resources/, with usage examples.
- **Test seeds for ingest**: A few placeholder files in Ingest/ (e.g., "Test-Capture-1.md" with simple text) to trigger pipelines immediately.

This keeps the vault "virginal" (no real user data) but ready for testing/launch: automations dominate from the start.

### How We Will Structure/Use the Resources

Resources will be structured to prioritize **seamless onboarding** and alignment with the Master Goal (autonomous post-capture processing). We'll use a dedicated `0-Onboarding/` folder at the root (outside PARA to avoid automation interference) as the entry point. This folder acts as a "wizard": guiding the user through setup, then self-archiving once complete.

- **Structure**:
  - `0-Onboarding/`:
    - Welcome-to-Second-Brain.md (overview of Master Goal, benefits, quick-start).
    - Install-Steps.md (numbered manual steps with screenshots/placeholders).
    - Basic-Examples.md (copy-paste templates for Project/Area/Resources).
    - Troubleshooting.md (common issues: MCP connection, Cursor rules not loading).
  - `3-Resources/` (PARA-aligned docs):
    - System reports (e.g., Second-Brain-Automations-Setup-Report.md).
    - Config-Defaults.md (editable params like confidence thresholds, color schemes).
    - MCP-Tools-Reference.md (all MCP tools in table format with params/examples).
  - PARA folders: Minimal seeds (templates) to bootstrap automations.
  - `.obsidian/`: Pre-baked configs for plugins (JSON files).
  - `.cursor/`: Rules and skills as .md (with inline docs for manual tweaks).

- **Usage**:
  - **Onboarding flow**: User opens vault → reads Welcome.md → follows Install-Steps.md (manual: install plugins, start MCP) → drops first capture in Ingest/ → triggers "Process Ingest" → watches autonomous magic (classification, move, distill). Basic seeds demonstrate Highlightr colors, frontmatter, hubs.
  - **Resources as self-sustaining**: Use Dataview in hubs for dynamic lists (e.g., #review-needed). Params in Config-Defaults.md allow user tweaks without code (e.g., change mid-band to 70–80%).
  - **Testing/launch focus**: In virginal state, resources ensure pipelines run on seeds first (e.g., bootstrap detects template Project → auto-enriches). This tests autonomy without user data, proving "out-of-box" readiness.

Resources emphasize **visual clarity** (callouts, tables) and **relational ties** (links to Master Goal, color examples), making the system intuitive for new users.

### This Is the Structure of the Onboarding

The onboarding is a **phased, guided experience** designed to get a new user from "open vault" to "first autonomous ingest" in <15 minutes, with minimal friction. It's linear but skippable for advanced users. Structure: Folder-based wizard + automated self-cleanup.

1. **Discovery Phase** (Immediate on open):
   - Vault opens to `0-Onboarding/Welcome-to-Second-Brain.md` (pinned or via Obsidian startup setting).
   - Content: High-level Master Goal recap, "Why this system?" (autonomy benefits), video/gif placeholders for demo.

2. **Setup Phase** (Manual steps, documented):
   - Link to Install-Steps.md: Numbered list:
     1. Install Obsidian plugins (e.g., Dataview, Highlightr, MCP integration if plugin-based).
     2. Configure .obsidian/ (copy-paste JSON snippets if needed).
     3. Start MCP server (command-line instructions, e.g., `node obsidian-para-zettel-autopilot`).
     4. Open vault in Cursor (setup .cursor/ if not auto-detected).
     5. Test health_check via chat ("Run health check").
   - Interactive: Each step ends with "Verify: [expected output]" (e.g., MCP-Health note created).

3. **Learning Phase** (Hands-on with seeds):
   - Link to Basic-Examples.md: Copy templates to PARA folders → trigger "ORGANIZE MODE" to see auto-enrichment.
   - Quick tutorial: "Drop a test note in Ingest/ → say 'Process Ingest' → observe logs."

4. **Activation Phase** (Go live):
   - Final step: Trigger "Onboarding complete" → automation archives 0-Onboarding/ to 4-Archives/ (using autonomous-archive pipeline).
   - Post-onboarding: Redirect to Resources-Hub.md for ongoing tips.

This structure ensures seamless flow: educational, verifiable, and automates cleanup to keep vault clean.

### Phased Implementation Plan

To align with the Master Goal (autonomous Second Brain), we'll implement the virginal state vault in phases/subphases. This mirrors the MCP migration plan: start with foundations, add automations, then onboarding polish. Each phase ends with a validation step (e.g., run health_check, simulate ingest).

#### Phase 1: Core Structure and Config (Foundations – 1–2 hours)
- **Subphase 1.1: Folder Skeleton**
  - Create root folders: 0-Onboarding/, 1-Projects/, 2-Areas/, 3-Resources/, 4-Archives/, Ingest/, Backups/ (Per-Change/, Batch/), Versions/.
- **Subphase 1.2: .obsidian/ Config**
  - Pre-configure plugins: Enable Dataview, Highlightr; set color schemes (analogous/complementary in JSON).
  - Add startup: Open Welcome.md on load.
- **Subphase 1.3: MCP and Params**
  - Place mcp.json at root with defaults (vault path, backup dir, max_age_minutes: 1440).
  - Create Config-Defaults.md in 3-Resources/ with editable params (confidence bands, highlight_key examples).
- **Validation**: Open in Obsidian → confirm folders; run manual health_check → log to MCP-Health note.

#### Phase 2: Rules, Skills, and Docs (Automations – 2–3 hours)
- **Subphase 2.1: .cursor/ Integration**
  - Add rules/ (always/ mcp-obsidian-integration.mdc, etc.) and skills/ (SKILL.md with docs).
- **Subphase 2.2: System Reports**
  - Place reports in 3-Resources/: Second-Brain-Automations-Setup-Report.md, etc., with links to Master Goal.
- **Subphase 2.3: MCP Tools Docs**
  - Create MCP-Tools-Reference.md: Table of tools (e.g., | Tool | Params | Example |) for calibrate_confidence, etc.
- **Validation**: Open in Cursor → trigger "Run health check" → confirm dry_run enforcement in logs.

#### Phase 3: Seed Content and Onboarding (User-Facing – 1–2 hours)
- **Subphase 3.1: Basic Seeds**
  - Add templates: Project-Template.md (frontmatter), Area-Template.md, Resources-Hub.md (Dataview).
- **Subphase 3.2: Onboarding Files**
  - Populate 0-Onboarding/: Welcome.md (Master Goal), Install-Steps.md (manuals), Basic-Examples.md, Troubleshooting.md.
- **Subphase 3.3: Self-Cleanup**
  - Document "Onboarding complete" trigger → archives folder via pipeline.
- **Validation**: Simulate new user: Follow Install-Steps → drop seed in Ingest/ → "Process Ingest" → check autonomous flow, Highlightr colors, logs.

#### Phase 4: Testing and Polish (Launch Readiness – 1 hour)
- **Subphase 4.1: Full Pipeline Test**
  - Run all triggers (INGEST, DISTILL, etc.) on seeds.
- **Subphase 4.2: Edge Cases**
  - Test mid-band refinement, dry_run fallbacks, task rerouting.
- **Subphase 4.3: Documentation Pass**
  - Ensure all .md files have callouts for key steps, links to resources.
- **Validation**: Compare to Master Goal: Measure time to first ingest (<15 min); count #review-needed (should be zero on seeds).

This plan ensures progressive build: safe, testable, and fully aligned to autonomy. After completion, zip the vault as "Second-Brain-Starter-Kit.zip" for distribution/testing.


# Notes
- we should include mobile toolbar configs