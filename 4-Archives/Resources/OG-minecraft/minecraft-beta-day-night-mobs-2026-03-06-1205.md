---
title: Minecraft Beta Day/Night Cycle & Mobs
created: "2026-03-06 12:05"
tags: ["minecraft","minecraft-beta","ai-output"]
para-type: Resource
status: active
ingest-type: ai-output
project-id: OG-minecraft
---
# AI Output Capture

## Source & prompt

_Which model/app and what did you ask? Paste the key parts of your prompt here._

- Source/model: Grok
- Date/time: 2026-03-06 12:05
- Prompt: Describe the day/night cycle and mob behaviors in Minecraft Beta 1.7.3, and outline how to implement a similar time-of-day system and basic mob AI (wander, detect, chase, attack) in Godot or Unity.

>  

## Full output

**Day/Night Cycle**  
- Total in‑game day length was ~20 minutes: roughly 10 minutes of daylight followed by 10 minutes of night.  
- The sun rose in the east and set in the west; the moon followed the opposite path. Sky colors transitioned from blue (day) to orange (sunset) to dark with stars (night).  
- Hostile mobs spawned at light levels below 7, which generally meant at night outdoors or in unlit caves.  

**Mobs in Beta**  
- Passive mobs (cows, pigs, sheep, chickens) wandered randomly and fled when attacked. They provided food, wool, and leather.  
- Hostile mobs (zombies, skeletons, creepers, spiders) spawned in dark areas and would:  
  - Randomly wander if they had no target.  
  - Detect players within ~16 blocks line‑of‑sight.  
  - Pathfind toward the player and attempt to attack (melee, arrows, or explosion in the case of creepers).  
- AI was comparatively simple: basic state changes (idle → chase → attack), minimal avoidance or advanced behaviors, and frequent “getting stuck” on terrain.  

**Implementation in Godot**  
- Day/night: add a world time variable and increment it each frame or physics tick, looping every 20 real‑time minutes.  
  - Rotate a directional light to simulate the sun.  
  - Adjust sky and ambient light colors based on time.  
  - Use thresholds to switch mob spawning behavior (enable hostile spawns when time is in the “night” window or when local light is low).  
- Mobs: implement a simple state machine per mob (`IDLE`, `WANDER`, `CHASE`, `ATTACK`).  
  - In `WANDER`, pick random points within a radius and move with collision.  
  - In `CHASE`, move toward the player if within detection range and visible.  
  - In `ATTACK`, play an animation or trigger damage/explosion when close enough.  
- Tutorials like “Basic Mob AI in Godot” and “Simple Enemy AI in Godot” show how to build these state machines and detection behaviors.  

**Implementation in Unity**  
- Day/night: maintain a time variable and rotate a directional light for the sun, optionally a second for the moon; lerp skybox/ambient colors across time.  
- Use `NavMeshAgent` for mob movement:  
  - In idle/wander, pick random NavMesh points.  
  - In chase, set the agent’s destination to the player’s position.  
  - In attack, stop movement and trigger an attack routine.  
- Tutorials such as “Minecraft Tutorial in Unity: Mobs” and generic “Enemy AI in Unity” examples demonstrate:  
  - Basic patrol and chase behavior.  
  - Detection via distance checks and raycasts.  

## Key insights

- The Beta atmosphere depends heavily on a tight 20‑minute day/night loop and a strong contrast between safe daylight and dangerous darkness.
- Mob AI can remain simple—wander, detect, chase, attack—while still feeling authentic to Beta’s sometimes clumsy enemy behavior.
- Time‑of‑day controlled spawning and lighting, combined with straightforward AI state machines, are the core ingredients to capture the Beta tension curve.

## TL;DR

_Short summary of why this output matters (or “nothing useful” if so)._

- Reproducing Beta’s day/night and mob feel means implementing a 20‑minute time loop that drives lighting and hostile spawning, plus simple state‑machine‑driven mobs that wander until they detect and chase the player.

## Sources

- Minecraft Wiki — Mob: `https://minecraft.wiki/w/Mob`  
- Minecraft Wiki — Daylight cycle: `https://minecraft.wiki/w/Daylight_cycle`  
- YouTube — Basic Mob AI for Minecraft Clone: `https://www.youtube.com/watch?v=eBB2U_H5k0g`  
- YouTube — Minecraft Tutorial in Unity: Mobs: `https://www.youtube.com/watch?v=lhgEczq74FM`  
- YouTube — Simple Enemy AI in Godot: `https://www.youtube.com/watch?v=jtQkyIJxnO8`

## Review Needed
Proposed para-type: area. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.