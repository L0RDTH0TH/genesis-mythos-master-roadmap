# Rule: Executing Tasks from a Markdown Task List

## Goal

To guide an AI assistant in **sequentially executing tasks** from a Markdown checklist (e.g. `tasks-[feature-name].md`) inside Cursor, updating the file as it goes. The assistant should:

- Work **one unchecked task at a time**
- **Plan briefly** before coding
- **Implement and run checks** (tests / lint) when possible
- **Mark tasks as complete** (`[x]`) and save the file
- Avoid skipping ahead unless explicitly instructed

This rule is designed for Cursor’s Agent/Composer and works best with task lists generated via `@ai-dev-tasks/generate-tasks.md`.

## Inputs

- A Markdown task file, usually named like `tasks-[feature-name].md`, containing:
  - A `## Relevant Files` section
  - A `## Tasks` section with `- [ ]` and `- [x]` items, optionally with nested sub-tasks
- Optional: A PRD file (e.g., `prd-[feature-name].md`) for additional context.

## High-Level Process

1. **Load Context**
   - Read the `tasks-[feature-name].md` file.
   - Skim `## Relevant Files` to understand where changes are likely to happen.
   - Optionally skim the PRD if referenced.

2. **Select Next Task**
   - Find the **first unchecked sub-task** (`- [ ]`) under `## Tasks`, in order.
   - Prefer the **lowest-level unchecked sub-task** (e.g., `1.1`, `1.2`, etc.) before marking a parent task like `1.0` complete.
   - If no unchecked tasks remain, stop and report that all tasks are complete.

3. **Plan Before Coding (Mini Plan)**
   - For the selected task, write a **short plan** (3–7 bullet points) covering:
     - Files to inspect or modify
     - New functions/components to create or update
     - Tests or validation to run
   - Keep this plan in the chat; do **not** modify the task file during planning.

4. **Implement the Task**
   - Follow the plan step-by-step:
     - Read relevant files
     - Implement code changes
     - Add/adjust tests when appropriate
   - Stay scoped to the current task. If you discover missing prerequisites or ambiguous requirements:
     - Either expand the current task scope slightly, or
     - Propose adding a new sub-task in the task list, and wait for user confirmation.

5. **Run Checks**
   - When feasible, run:
     - **Tests** (e.g., `npm test`, `pnpm test`, `npx jest`, framework-specific commands), and/or
     - **Linters/formatters** (e.g., `npm run lint`, `eslint`, `prettier`, `go test`, `pytest`, etc.).
   - If checks fail:
     - Fix issues that clearly relate to your changes.
     - If failures are pre-existing or unrelated, call them out explicitly in the chat and do **not** attempt large refactors unless asked.

6. **Update the Task File**
   - Once the task is reasonably complete and checks pass (or you have documented any blockers):
     - Change the relevant line in the task file from `- [ ]` to `- [x]`.
     - If you added or changed tests, optionally add a short note under the task describing what was covered (one short sentence).
   - Only mark **parent tasks** (e.g., `1.0`) as complete once all of their child tasks (e.g., `1.1`, `1.2`, etc.) are checked off, unless the structure clearly indicates otherwise.

7. **Report Progress and Loop**
   - In the chat, briefly summarize:
     - What task you completed (e.g., `1.2 Add validation to signup form`)
     - Key files touched
     - Test/lint status
   - Then **select the next unchecked task** and repeat from step 3, unless:
     - The user has asked you to stop after one task, or
     - You hit a blocker that needs user input (missing requirements, permissions, secrets, etc.).

## Detailed Behavior

### Choosing Tasks

- **Preferred order**:
  1. The earliest incomplete sub-task under the earliest incomplete parent.
  2. If a parent has no explicit sub-tasks, treat it as a single unit of work.
- **Do not** reorder tasks unless the user explicitly allows it (e.g., "You can reorder for efficiency").
- If a later task is clearly a prerequisite for an earlier one (rare), you may:
  - Propose reordering in the chat, and
  - Wait for confirmation before continuing.

### Editing the Task File

- Preserve the existing structure, indentation, and headings.
- Only change:
  - Checkboxes (`[ ]` → `[x]`), and
  - Very short notes under the task (if helpful), such as:
    - "Implemented in `SignupForm.tsx` and added Jest tests"
- Do **not** rewrite the task descriptions wholesale unless the user requests it.

### Handling Blockers

If you cannot complete a task due to missing information, environment issues, or external dependencies:

1. Do **not** mark the task as complete.
2. Add a short note under the task in the task file, e.g.:
   - "_Blocked: missing API key for external service_"
3. In the chat, clearly state:
   - What you attempted
   - Why you are blocked
   - What you need from the user

### Scope Discipline

- Stay tightly focused on the **current task**.
- If you notice unrelated bugs or refactors:
  - Mention them briefly in the chat or suggest adding new tasks to the list.
  - Do not silently refactor large areas unrelated to the active task.

## Example Usage in Cursor

Typical usage pattern in Cursor Agent/Composer:

1. Generate PRD:

   - `@ai-dev-tasks/create-prd.md Build a simple habit tracker app with React, localStorage, dark mode, and basic stats.`

2. Generate tasks:

   - `@ai-dev-tasks/generate-tasks.md Now use @prd-habit-tracker.md to create the task list.`

3. Execute tasks:

   - `Follow @ai-dev-tasks/execute-tasks.md to work through @tasks-habit-tracker.md. Start with the first unchecked sub-task, plan briefly, then implement, test, and mark it [x]. Continue to the next unchecked task until you need input or hit an error.`

## Final Instructions for the AI

When invoked with this file:

1. **Do not** invent a new task file—always operate on the referenced one.
2. **Always**:
   - Read the current task file
   - Pick the next unchecked task
   - Plan briefly
   - Implement changes
   - Run checks when feasible
   - Update the task file (`[ ]` → `[x]`)
3. Stop and ask the user if:
   - You are blocked
   - Requirements are ambiguous
   - You believe the remaining tasks should be re-scoped or reordered.

