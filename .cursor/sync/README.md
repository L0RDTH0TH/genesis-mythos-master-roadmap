# Sync — markdown copies of rules and skills

This folder holds **synced markdown copies** of Cursor rules (`.mdc`) and skills (`SKILL.md`) for visibility and backup. Cursor reads the originals (`.cursor/rules/**/*.mdc` and `.cursor/skills/**/SKILL.md`); these `.md` copies are for reference only.

- **rules/always/** — copies of `.cursor/rules/always/*.mdc`
- **rules/context/** — copies of `.cursor/rules/context/*.mdc`
- **rules/agents/** — copies of `.cursor/rules/agents/*.mdc` (pipeline subagent rules)
- **skills/** — copies of `.cursor/skills/<name>/SKILL.md` as `<name>.md`

**Not mirrored here:** `.cursor/rules/agents/_template.mdc` (scaffold only). **`.cursor/rules/legacy-agents/*.mdc`** are older reference/rollback copies and are not copied to sync; live behavior is **`agents/*.mdc`** plus **`.cursor/agents/*.md`**.

Keep these in sync when you update the source `.mdc` or `SKILL.md` files.
