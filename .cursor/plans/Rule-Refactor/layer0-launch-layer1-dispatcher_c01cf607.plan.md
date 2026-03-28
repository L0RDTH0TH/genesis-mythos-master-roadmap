---
name: Layer0-Launch-Layer1-Dispatcher
overview: Change the dispatcher so EAT-QUEUE causes Layer 0 to launch the Queue subagent (Layer 1) via Task instead of running queue logic in Layer 0.
todos: []
isProject: false
---

# Layer 0 must launch Layer 1 via Task (dispatcher fix)

## Problem

When the user says EAT-QUEUE, the **dispatcher** currently tells the agent to "Act as the queue orchestrator" and run Step 0, read queue, parse, dispatch. So **Layer 0 runs queue logic inline** instead of **launching Layer 1** (Queue subagent) via the Task tool. The user wants: Layer 0's only action = call Task to spawn Queue; Queue (Layer 1) then runs in its own context.

## Required change

**File:** `.cursor/rules/always/dispatcher.mdc`

**Replace** the section "## Queue triggers → Queue/Dispatcher subagent" through the end of the "then:" block (lines 20–34) **with** the following.

---

## Queue triggers → spawn Layer 1 (Queue subagent) via Task

When the user instruction contains any of these (case-insensitive):

- **EAT-QUEUE** *(canonical)*
- **Process queue**
- **EAT-CACHE** / **eat cache**
- **PROCESS TASK QUEUE**

then **Layer 0 (this agent) must NOT run queue logic**. Your **only** action is to **launch the Queue/Dispatcher subagent (Layer 1)** by **calling the `Task` tool once**:

1. **Build a hand-off** for the Queue subagent that includes:
  - Vault root (workspace path).
  - Prompt queue path: `.technical/prompt-queue.jsonl`.
  - Task queue path: `3-Resources/Task-Queue.md`.
  - Which to process: prompt queue (EAT-QUEUE / Process queue / EAT-CACHE) or task queue (PROCESS TASK QUEUE) or both if the user asked for both.
  - If EAT-CACHE with pasted payload: include the pasted payload (e.g. `queued_prompts`) in the hand-off.
  - Instruction: "You are the Queue/Dispatcher subagent (Layer 1). Process the queue(s) as specified in .cursor/rules/agents/queue.mdc: Step 0 (wrappers), read, parse/validate/dedup/order, then for each pipeline entry call the Task tool to launch that pipeline's subagent, Watcher-Result, rewrite. Do not run queue logic in the parent context; you run in this context only."
2. **Call the `Task` tool** with **subagent_type: `queue`** (or the type that loads `.cursor/agents/queue.md`), **description**: one sentence (e.g. "Process the prompt queue and/or task queue"), **prompt**: the full hand-off text above. Wait for the Task call to return.
3. **Do not** read `.technical/prompt-queue.jsonl` or `3-Resources/Task-Queue.md` yourself. **Do not** run Step 0, parse, dispatch, or Watcher-Result in this context. If the Task tool is unavailable or the call fails, report that the Queue subagent could not be launched and do not run queue steps inline.

---

## Optional follow-up

- **Sync:** Update `.cursor/sync/rules/always/dispatcher.md` to match (backbone-docs-sync).
- **system-funnels.mdc:** If it describes EAT-QUEUE behavior, align wording so it says Layer 0 launches Queue via Task rather than acting as the queue processor.

