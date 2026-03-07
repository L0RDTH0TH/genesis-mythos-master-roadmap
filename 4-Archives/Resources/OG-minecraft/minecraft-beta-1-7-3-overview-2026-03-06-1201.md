---
title: Minecraft Beta 1.7.3 Overview
created: "2026-03-06 12:01"
tags: ["minecraft","minecraft-beta","ai-output"]
para-type: Resource
status: ingest
ingest-type: ai-output
project-id: OG-minecraft
---
# AI Output Capture

## Source & prompt

_Which model/app and what did you ask? Paste the key parts of your prompt here._

- Source/model: Grok
- Date/time: 2026-03-06 12:01
- Prompt: High-level overview of Minecraft Beta 1.7.3: core survival loop, missing modern systems, world generation quirks, mobs, crafting, and overall "beta feel", with emphasis on mechanics relevant to recreating the experience in a modern engine.

>  

## Full output

**Key Features and Changes**  
- Beta 1.7.3 was a bug-fix release (July 2011), building on 1.7's pistons and shears. Core mechanics were largely stable from earlier Betas: infinite world, basic survival loop (gather, build, survive nights).  
- No hunger (added in 1.8), no experience or enchanting. Focus was on exploration plus the mining/crafting basics rather than RPG progression.  
- The world used chunk-based generation (16×16×128 height limit) with Perlin noise for terrain. Simple biomes (forest, desert, etc.), no modern amplified or highly varied worlds.  
- Quirks included floating islands near cliffs and basic caves (narrow tunnels, no lush/deep dark or large modern cave rooms).  

**Blocks**  
- Roughly ~50 block types: stone, dirt, grass, wood, leaves, basic ores (coal, iron, gold, diamond, lapis), sand and gravel with gravity, plus early utility blocks like workbench and furnace.  
- Interactions were simple: punch to break (with tools speeding it up), place via right-click.  

**Player/Controls**  
- WASD movement with mouse look; space to jump, shift to sneak.  
- Inventory on E, hotbar on 1–9.  
- Health bar only (no hunger), so the survival feel was more about avoiding direct damage than managing long-term resource depletion.  

**Mobs**  
- Passive mobs (cow, pig, sheep, chicken) wandered and fled when hit.  
- Hostile mobs (zombie, skeleton, creeper, spider) detected players at ~16 blocks and used simple pathfinding to chase and attack.  
- Creepers exploded on close approach, creating terrain damage and danger near bases.  

**Day/Night**  
- 20‑minute cycle: ~10 minutes day, ~10 minutes night.  
- Sun and moon visibly moved across the sky; lighting shifted from blue to orange to dark.  
- Hostiles spawned at light level <7, making darkness itself the primary threat.  

**Crafting and Progression**  
- 2×2 inventory grid and 3×3 workbench.  
- Classic progression: punch trees → planks/sticks → wooden tools → stone/iron/diamond tools via mining and smelting.  
- Furnace smelted ores into ingots using coal or other fuels.  

**Tools/Mining/Smelting**  
- Pickaxes, axes, shovels, and swords had tiers (wood, stone, iron, diamond) with increasing speed and durability.  
- Mining revealed ores embedded in stone; smelting transformed raw materials into higher‑tier tool components.  

**Beta Feel**  
- Janky physics and exploits (e.g., falling sand/gravel tricks, simple mob pathing leading to stuck enemies).  
- Sparse world content: no villages, no modern structures, limited biomes.  
- Overall tone: lonely, atmospheric, and more about sandbox experimentation than guided progression.  

## Key insights

- Beta 1.7.3’s scope is much smaller than modern Minecraft, which makes it tractable for a faithful clone that focuses on terrain, basic survival, and simple mob AI rather than late‑game systems.
- The lack of hunger, XP, and complex structures means you can scope the project around the mining–building loop plus a tight day/night danger rhythm.
- World generation, basic block interactions, and simple AI/pathfinding are the largest technical pillars to get right for an authentic “beta” feel.

## TL;DR

_Short summary of why this output matters (or “nothing useful” if so)._

- Minecraft Beta 1.7.3 offers a tightly scoped survival sandbox—simple terrain, blocks, mobs, and progression—making it an ideal target for a faithful clone that captures the feel of early Minecraft without modern system bloat.

## Sources

- Minecraft Wiki — Beta 1.7.3: `https://minecraft.wiki/w/Beta_1.7.3`

## Review Needed
Proposed para-type: project. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.