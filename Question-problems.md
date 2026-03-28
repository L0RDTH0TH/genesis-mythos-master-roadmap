For RESUME-ROADMAP, how should we set `max_depth` (maximum roadmap tree depth for this run)?

**A.** I’ll specify max_depth explicitly (e.g. 3, 4, 5)  
**B.** default — derive from phase/config defaults  
**C.** AI reasoning — choose a depth cap for this project and explain briefly


# SHOULD BE
**C.** AI reasoning - choose a depth cap for each phase per iteration

Does **NOT** need to be specific but general you evaluate the necessary depth based on current state



For a multi-phase mythos project, a `max_depth` of around 4 for this run balances richness with manageability: deep enough for subphases and key task clusters, but shallow enough that later deepen runs can refine without the tree exploding. Deeper than 5 on a first resume step tends to create fragile, over-detailed branches that are hard to maintain.

For RESUME-ROADMAP, how should we set `branch_factor` (children per node during deepen)?

**A.** I’ll specify branch_factor explicitly (e.g. 3, 4, 6)  
**B.** default — use config defaults (e.g. 4 for deeper phases)  
**C.** AI reasoning — pick a branching factor for this project and explain briefly


# SHOULD BE
**C.** AI reasoning - evaluate if a new branch is superior to continuing branches



A branch_factor of **4** suits this roadmap: it gives enough parallel sub-branches (e.g. lore, mechanics, tooling, publishing) to capture the mythos’ dimensions without fragmenting focus into too many thin strands; going much higher tends to create noisy, shallow nodes that are harder to prioritize.

For RESUME-ROADMAP, how should we set `profile` (which prompt_defaults.roadmap profile to use)?

**A.** I’ll specify the profile explicitly (e.g. default, deep-technical, narrative-heavy)  
**B.** default — use the standard roadmap profile from Config  
**C.** AI reasoning — choose a profile for this project and explain briefly


# SHOULD BE
This should not be here we tried to move it you failed.






Yes. That design can cause exactly the breakage you’re describing.

**What goes wrong**

1. **A = “specify profile name” but name isn’t in Config**  
   The crafter sets `params.profile: "some-name"`. At run time the pipeline only merges from **existing** `prompt_defaults.profiles` (or roadmap block). If `"some-name"` isn’t there, nothing is merged for that key, so the run falls back to base defaults. The user’s choice is effectively ignored and they’re forced into default behavior — **breakage**.

2. **Overwriting earlier crafting steps**  
   If the pipeline does “base defaults → then apply profile,” a profile that *does* exist can override params the user already set in the crafter (e.g. token_cap, branch_factor). So a later “use this profile” step can overwrite earlier custom choices. If the profile doesn’t exist, the user still loses their “use this profile” intent and gets defaults — again overwriting the idea of a custom run.

3. **Future config selections don’t “root”**  
   The crafter never writes new entries into Config. So any one-off or new profile name the user types in when they choose A never becomes a real profile. It doesn’t persist or “root” anywhere; only names that already exist in Config do anything. That forces users to edit Config to make custom profiles real, and makes “specify profile name” fragile for anything that isn’t already defined.

So: **yes** — as specified, this can force users onto defaults, overwrite the intent of earlier steps, and prevent new profile names from taking effect until someone edits Config. Fixing that would mean either validating the profile name against Config and failing/warning when it’s missing, or allowing the crafter to create/update a profile in Config when the user chooses A and specifies a name (so the choice can root and re-use).