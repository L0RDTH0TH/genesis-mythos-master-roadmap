---
title: Color-Coded Highlighting — Linking Ideas Across Projects
created: 2026-02-28
tags: [pkm, second-brain, highlightr, distill, express, projects]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/README]]"]
---

# Color-Coded Highlighting — Linking Ideas Across Projects

This note describes how the vault uses **semantic, color-coded highlighting** to link and relate ideas **within and across projects**, so you can see at a glance what type of content you’re reading and how it connects to other notes.

## Goal

- **Same meaning → same color** everywhere (e.g. key facts = yellow, actionable items = blue).
- **Related ideas across projects** use **analogous** colors (e.g. blue–green for one theme).
- **Contrasting or conflicting ideas** use **complementary** colors (e.g. orange vs blue for tension).
- **Project identity**: Notes in a project can share a **project-level color grammar** via `highlight_key`, so one project can favor certain colors for its domain (e.g. user-flow project: blue–green for flows, orange for pain points).

## Responsibilities

**Highlightr** plus the **master key** (Highlightr-Color-Key) define semantics. **distill-highlight-color** and **layer-promote** apply colors; **project highlight_key** overrides when set. **Analogous** colors = related ideas; **complementary** = contrast/tension. Skills log coverage_adapted and perspective to pipeline logs.

## Usage example

Set frontmatter **`highlight_perspective: combat`** or trigger **HIGHLIGHT PERSPECTIVE: combat** (e.g. via Commander macro "Queue Highlight: Combat"). The distill-highlight-color skill then applies **lens-focused** highlighting: spans that match the perspective get analogous colors (same theme = same hue family); contrasts still use complementary colors.

## 1. Semantic color key (vault-wide)

The single source of truth is [[3-Resources/Highlightr-Color-Key|Highlightr-Color-Key]]. **Section 1** defines the canonical mapping:

| Color  | Meaning (short) |
|--------|------------------|
| Yellow | Key facts, premises, main points |
| Green  | Definitions, core concepts |
| Blue   | Actionable items, next steps, thesis |
| Red    | Critiques, warnings, questions |
| Orange | Examples, case studies, applications |
| Purple | Quotes, key insights, mental models |
| Pink   | Resurface later, connections, open questions |
| Cyan   | Secondary/supporting details |
| Grey   | Deprecated or low-confidence |

Every pipeline and skill that applies highlights uses this key (or a project override) so **the same concept type has the same color** across the vault. That creates a **visual language**: e.g. blue = “do this,” purple = “insight/quote,” red = “watch out.”

## 2. Project-level overrides (`highlight_key`)

Notes can carry frontmatter **`highlight_key`** (or a project-specific key name) so that:

- **Distill and express skills** use project-specific color choices when present.
- **Same project** → consistent color grammar (e.g. “Project-X: blue–green for user-flow ideas, orange for pain points”).
- **Linking across projects**: When notes from different projects reference the same theme, using the **same semantic color** (or analogous colors) keeps the relation visible even in hub views or backlinks.

**Config**: [[3-Resources/Second-Brain-Config|Second-Brain-Config]] sets `highlight.default_key` to the Highlightr-Color-Key path. Skills read that for the master key and use frontmatter `highlight_key` for project overrides. See Highlightr-Color-Key **“For MCP / pipelines”** and **“Project-Specific Guidelines.”**

## 3. Color theory — how we relate ideas

Skills (especially **distill-highlight-color**, **layer-promote**, **related-content-pull**, **express-mini-outline**) apply simple color theory so **relations are visible**:

- **Analogous colors** (e.g. blue, blue–green, green): use for **related ideas**, continuity, same theme across sections or **across linked project files**. Seeing similar hues signals “same family of ideas.”
- **Complementary colors** (e.g. blue vs orange): use for **contrasts**, tension, opposing ideas (e.g. pain points vs benefits, critique vs claim). Side-by-side colors signal “these are in dialogue.”

So highlighting doesn’t only mark “what kind of content” (semantic key) — it also encodes **how ideas relate** (analogous = related, complementary = contrast), including **across projects** when notes are linked or shown together (e.g. in a hub or Related section).

## 4. Where it’s applied (pipelines and skills)

| Pipeline / moment | Skill / step | Role |
|-------------------|-------------|------|
| **Ingest** (after distill_note) | **distill-highlight-color** | Apply semantic colors + project `highlight_key`; analogous for related ideas, complementary for contrasts. |
| **Distill** (after highlight) | **layer-promote** | Promote bold → highlight → TL;DR; project colors; complementary for conflicting ideas. |
| **Express** (before outline) | **related-content-pull** | Related section with color-theory emphasis (analogous/complementary for links). |
| **Express** (outline) | **express-mini-outline** | Outline/summary with project colors for sections (analogous for related sub-ideas). |
| **Archive** (before move) | **summary-preserve** | Preserve existing Highlightr markup and project color links so archived notes stay relationally clear. |

**Frontmatter**: **frontmatter-enrich** can set `highlight_key` (e.g. for audit notes); **graph**-related frontmatter can be set from project color for graph view. See [[3-Resources/Second-Brain/Skills|Skills]].

## 5. How this “links” ideas across projects

- **Same color across notes** → same meaning type (e.g. all “actionable” in blue). When you jump between notes or projects, the color carries the same semantics.
- **Analogous colors** in linked or co-displayed notes → “same theme / continuity.” Useful when multiple projects touch one theme (e.g. “onboarding” in Project A and Project B both use blue–green).
- **Complementary colors** in one note or across linked notes → “tension or contrast” (e.g. benefit in blue, pain in orange).
- **Project `highlight_key`** → per-project “accent” so a project’s notes feel visually consistent and its main concepts are easy to spot in hubs and MOCs.

So the **link** is both conceptual (semantic key) and **relational** (analogous/complementary and project grammar), without relying only on tags or links.

## 6. Perspective guidelines

When you want highlighting to focus on a **specific lens** (e.g. "combat systems", "performance", "user flow"):

- Set note frontmatter **`highlight_perspective: [lens]`** or trigger **HIGHLIGHT PERSPECTIVE: [lens]** (e.g. via Commander macro "Queue Highlight: Combat"). The distill-highlight-color skill then applies **lens-focused** highlighting: spans that match the perspective get **analogous** colors (same theme = same hue family).
- **When to use a lens**: Use when a note serves multiple angles and you want one pass to emphasize one angle (e.g. technical vs stakeholder). Same note can be re-run later with a different lens for a different view.
- **Relation to analogous colors**: Within the chosen lens, related ideas share analogous hues; contrasts still use complementary colors so tension remains visible.
- **Fallback**: If CSS gradients (`data-drift-level`) render poorly on mobile (e.g. lags or missing styles), use **fallback to emojis** for depth/drift in callouts (e.g. 🔵 core, 🟢 supporting, ⚪ fading). Skills (e.g. highlight-perspective-layer) can detect mobile context or user preference and emit emoji indicators instead of or in addition to data-drift-level. See Skills.md highlighter flow.

## 7. References

- **Master key and format**: [[3-Resources/Highlightr-Color-Key|Highlightr-Color-Key]] (Section 1 semantics, Section 2 storage format, Section 3 agent vs user, Project-Specific Guidelines).
- **Config**: [[3-Resources/Second-Brain-Config|Second-Brain-Config]] → `highlight.default_key`.
- **Skills**: [[3-Resources/Second-Brain/Skills|Skills]] — distill-highlight-color, layer-promote, express-mini-outline, related-content-pull, summary-preserve.
