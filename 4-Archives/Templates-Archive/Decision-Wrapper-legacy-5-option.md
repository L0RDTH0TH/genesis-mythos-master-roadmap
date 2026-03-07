---
approved: false
decision_candidate: true
wrapper_type: ingest-decision
proposal_path: {{proposal_path}}                        # full path where this wrapper itself lives
original_note: [[{{original_filename}}]]
original_path: {{original_path}}                       # full path of the note being decided
decision_priority: {{priority}}
---

# Decision: Where should [[{{original_filename}}]] go?

**Classifier top 5 candidates** (ranked):

1. {{cand1_path}} — {{cand1_conf}}%  
   {{cand1_reason}}

2. {{cand2_path}} — {{cand2_conf}}%  
   {{cand2_reason}}

3. {{cand3_path}} — {{cand3_conf}}%  
   {{cand3_reason}}

4. {{cand4_path}} — {{cand4_conf}}%  
   {{cand4_reason}}

5. {{cand5_path}} — {{cand5_conf}}%  
   {{cand5_reason}}

**Your action — edit ONE line:**

- Quick pick: `approved_option: 1`   ← change the number
- OR custom path: `approved_path: "2-Areas/AI Integration.md"`
- OR reject all: `approved_option: 0`

**Thoughts / corrections / why this location?** (becomes user_guidance)
> 
> 
> 

Run **EAT-QUEUE** after editing.

```dataview
TABLE decision_priority, approved_option, approved_path
FROM "Ingest/Decisions"
WHERE decision_candidate = true AND approved = false
  AND (file.folder = "Ingest/Decisions/Ingest-Decisions" OR file.folder = "Ingest/Decisions/Roadmap-Decisions")
SORT decision_priority DESC
```

