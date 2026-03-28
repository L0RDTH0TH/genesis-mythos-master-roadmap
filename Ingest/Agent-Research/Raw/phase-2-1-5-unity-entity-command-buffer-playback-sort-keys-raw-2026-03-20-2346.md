---
created: 2026-03-20
tags: [research, agent-research, raw]
project_id: genesis-mythos-master
linked_phase: "Phase-2-1-5"
source_urls:
  - https://docs.unity3d.com/Packages/com.unity.entities@1.0/manual/systems-entity-command-buffer-playback.html
agent-generated: true
---

## Source: https://docs.unity3d.com/Packages/com.unity.entities@1.0/manual/systems-entity-command-buffer-playback.html

### Key excerpt (deterministic playback via sort keys)

> "If you split the recording of commands in an entity command buffer (ECB) across multiple threads [in a parallel job] it means that the order of the commands is non-deterministic because they depend on job scheduling."

> "Deterministic isn't always essential, but code which produces deterministic results is easier to debug."

> "You can't avoid the non-deterministic order of recording [in parallel jobs], but you can make the playback order of the commands deterministic in the following way:"

> "1. Use the sort keys to sort the commands on playback, before Unity performs the commands."

> "2. Record an int sort key passed as the first argument to each ECB method."

> "If the recorded sort keys are independent from the scheduling, then the sorting makes the playback order deterministic."

> "Also, Unity always plays back commands with larger sort keys after commands with smaller sort keys."

### Sort key selection (stable association per chunk)

> "In a parallel job, the sort key you need for each entity is a number that has a fixed and unique association with that chunk in the job's query."

> "You can use the`ChunkIndexInQuery` value in a parallel job as an index."

Example comment (verbatim):

> "The `ChunkIndexInQuery` is unique for each chunk in the query and will be consistent regardless of scheduling. This will result in deterministic playback of the ECB."

