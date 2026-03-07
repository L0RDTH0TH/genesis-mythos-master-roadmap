---
name: CHECK_WRAPPERS plan tighten-ups
overview: Tighten the CHECK_WRAPPERS / stale-wrapper implementation plan with explicit idempotency (tag + section check), documented vault search (obsidian_global_search / list_notes), consistent CHECK_WRAPPERS-prefixed Ingest-Log lines, a hidden comment in the Decision-Wrapper template for insertion point, and a Vault-Layout.md one-liner for orphan behavior discoverability.
todos: []
isProject: false
---

# CHECK_WRAPPERS plan tighten-ups

Minor improvements to the existing CHECK_WRAPPERS / stale-wrapper / orphan design: idempotency guard, vault search spec, logging format, template insertion anchor, and Vault-Layout discoverability.

---

## 1. Idempotency guard (explicit, tag-based)

**Requirement:** Before writing the `## Wrapper state` block (or equivalent reserved block), the agent must **skip appending** if any of the following is true:

- Frontmatter contains tag `**#orphan`** or `**#true-orphan`** (or `tags` array includes `orphan` / `true-orphan`).
- The note body already contains the **section header** used for the block (e.g. `## Wrapper state` or the exact callout title used for the internal note).

**Where to document:** In [.cursor/rules/context/auto-eat-queue.mdc](.cursor/rules/context/auto-eat-queue.mdc), in the "Internal note placement and idempotency" subsection (or equivalent). State explicitly:

- "Before inserting the Wrapper state block, check: (1) frontmatter does not already contain `#orphan` or `#true-orphan`; (2) body does not already contain the section header `## Wrapper state` (or the reserved callout title). If either check fails, do not append; prevents duplicate notes on repeated EAT-QUEUE runs."

No code change beyond the rule text; behavior is agent-follows-rule.

---

## 2. Vault search implementation note

**Requirement:** The rule must document the **exact** way the companion is searched for, so it is not "magic" for future readers.

**Spec to add in the rule:**

- **Primary:** Use `**obsidian_global_search`** with a query that matches the original note (e.g. filename or title). If the MCP returns path(s), filter to the vault and exclude the wrapper path; treat a single path match as "found at P"; multiple candidates can be listed in the trace.
- **Fallback:** If global search is unavailable or returns nothing, use `**obsidian_list_notes`** (or equivalent list) and filter by **basename** of `original_path` (and optionally by note title derived from the wrapper). Document: "Companion search: `obsidian_global_search` with query derived from original_path basename (and optionally title); fallback: list_notes + basename filter."
- **Result:** If found at path P and P equals resolved `target_path` → original at target (archive wrapper). If found at P ≠ target_path → Orphan; if not found → True Orphan.

**Where:** In the same rule file, in the "Stale wrapper" / "Orphan" execution semantics, add a short **"Vault search implementation"** bullet or subsubsection that states the exact call(s) and fallback so implementors and readers know what to run.

---

## 3. Logging phrases (consistent, greppable)

**Requirement:** All CHECK_WRAPPERS-related Ingest-Log lines must:

- Follow the existing **Ingest-Log format**: `timestamp | Excerpt | PARA | Changes | Confidence | Proposed MV | Flag`
- Be **prefixed with** `CHECK_WRAPPERS:`  so they are greppable (e.g. `grep "CHECK_WRAPPERS:" 3-Resources/Ingest-Log.md`).

**Examples to document in the rule (or in Logs.md):**

- Apply / retry: `CHECK_WRAPPERS: <timestamp> | <excerpt e.g. "Retry apply (stale; original still in Ingest): <original_path>" | Resource | <changes> | <conf>% | <proposed_mv or target_path> |` 
- Stale archived: `CHECK_WRAPPERS: <timestamp> | Stale wrapper archived; original at target | ... | ... | ... | 4-Archives/Ingest-Decisions/<basename>.md |` 
- Orphan: `CHECK_WRAPPERS: <timestamp> | Orphan; companion at P, expected at target_path | ... | ... | | | #orphan`
- True Orphan: `CHECK_WRAPPERS: <timestamp> | True Orphan; companion not found in vault | ... | ... | | | #true-orphan`

Exact field values (PARA, Confidence, etc.) can follow existing Ingest-Log conventions; the rule and Logs.md should state that CHECK_WRAPPERS lines use this format and prefix.

---

## 4. Template: reserved slot + hidden comment

**Requirement:** In [Templates/Decision-Wrapper.md](Templates/Decision-Wrapper.md), after the reserved **Wrapper state** slot (the block above "**Thoughts / corrections / why this location?**" and below "**Your action — check ONE box above…**"), add a **hidden HTML comment** that marks the exact insertion point so the agent can find it even if the user edits the template.

**Example:**

```markdown
**Wrapper state** *(do not edit manually; set by EAT-QUEUE when wrapper is orphaned or not archived)*
<!-- CHECK_WRAPPERS: insert Wrapper state block above this line -->
```

So the agent inserts the `## Wrapper state` (or callout) content **above** that comment. The comment text should be unique and greppable (e.g. `CHECK_WRAPPERS: insert` or `insert Wrapper state block above this line`).

---

## 5. Sync section: Vault-Layout.md one-liner

**Requirement:** Add a **one-liner** in [3-Resources/Second-Brain/Vault-Layout.md](3-Resources/Second-Brain/Vault-Layout.md) so that **orphan/stale wrapper behavior** is discoverable from the layout doc.

**Placement:** Under or next to the existing mention of **Ingest/Decisions** (e.g. in the table row for **Ingest** or in the exclusions bullet that references Decision Wrappers). Current text already says processed wrappers move to `4-Archives/Ingest-Decisions/` and step 0 scans `Ingest/Decisions/`.

**Suggested one-liner to add:**

- In the **Ingest** row of the folder table (Responsibilities column), append or fold in: "Stale wrappers (processed but still in Decisions): EAT-QUEUE tries ingest if original still in Ingest; else archives wrapper only when original is at target; otherwise tags Orphan/True Orphan and adds internal note (no archive)."
- Or as a short bullet under the exclusions / Decision Wrappers bullet: "Orphan behavior: wrappers with processed but missing/wrong-location original get #orphan or #true-orphan and an internal note; wrapper is not archived until original is at target."

Choose one place so the layout doc has a single, discoverable sentence; the plan does not mandate which.

---

## 6. Files to touch (summary)


| File                                                                                 | Change                                                                                                                                                                                                 |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [.cursor/rules/context/auto-eat-queue.mdc](.cursor/rules/context/auto-eat-queue.mdc) | Add explicit idempotency check (tags + section header); add "Vault search implementation" with obsidian_global_search + list_notes fallback; add Ingest-Log format and CHECK_WRAPPERS prefix examples. |
| [Templates/Decision-Wrapper.md](Templates/Decision-Wrapper.md)                       | Add hidden comment after reserved Wrapper state slot: `<!-- CHECK_WRAPPERS: insert Wrapper state block above this line -->`.                                                                           |
| [3-Resources/Second-Brain/Vault-Layout.md](3-Resources/Second-Brain/Vault-Layout.md) | Add one-liner near Ingest/Decisions (table or exclusions) describing orphan/stale wrapper behavior.                                                                                                    |
| .cursor/sync/rules/context/auto-eat-queue.md                                         | Mirror rule changes.                                                                                                                                                                                   |
| 3-Resources/Second-Brain/Logs.md (if present)                                        | Add CHECK_WRAPPERS line format and prefix to Ingest-Log conventions.                                                                                                                                   |


---

## 7. No change to flow

The **control flow** (try-ingest when both in Ingest; archive only when at target; vault search → Orphan vs True Orphan; three tags) is unchanged. This plan only tightens idempotency, search spec, logging, template anchor, and layout discoverability.