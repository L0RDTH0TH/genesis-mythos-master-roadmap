---
created: 2026-03-20
tags: [research, agent-research, raw]
project_id: genesis-mythos-master
linked_phase: "Phase-2-1-5"
source_urls:
  - https://docs.eventsourcingdb.io/best-practices/optimizing-event-replays/
agent-generated: true
---

## Source: https://docs.eventsourcingdb.io/best-practices/optimizing-event-replays/

### Key excerpt (replay-safe side effects: idempotent + isolated)

> "One of the most important considerations during a replay is whether or not it is safe to trigger side effects."

> "Events that are replayed for the purpose of building internal state or read models should not cause external actions such as sending emails, updating third-party systems, or writing to external databases."

> "Replay-safe logic should be idempotent and isolated."

> "Components that are responsible for side effects should be designed to distinguish between live processing and replay, and to avoid duplicating actions."

