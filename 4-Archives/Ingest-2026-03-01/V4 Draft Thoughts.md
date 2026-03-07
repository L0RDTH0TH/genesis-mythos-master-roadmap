---

---
**Protect the file the watcher points at**  
**File guard**
- I do not want this defered
**Add buttons and text fields**  
**UI layer**
- Lets split this from one monolithic file into individual files and remove the Ingest button
- The Ingest button functionality will be migrated to a tool bar entry
**Wait for Cursor completion or failure**  
**Completion detection** – script waits until the Cursor run is “done” (success or failure).
- my first thought is piggy back off Cursor system notifications but there may be a more standard way or just superior
**Popup with completion message**  
**Notification** – show a popup with the outcome (e.g. “Done” / “Failed” / “Timeout”).
- these should be detailed with an error trace

## Review Needed
Proposed para-type: archive. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.