---
title: "2D Map Maker – Parchment-to-3D Terrain (Godot VTT)"
created: 2026-03-02
aliases: [2d map maker.txt]
tags: [type/reference, source/attachment, godot, vtt]
source: "![[5-Attachments/Other/2d map maker.txt]]"
---

# 2D Map Maker (Parchment to 3D Terrain)

Companion note for ingested text: workflow for a 3D first-person VTT where players sketch fantasy maps on parchment and see them become explorable 3D terrains.

## Summary

- **Stack**: Godot 4.3+, Terrain3D, free parchment assets, ~200 lines GDScript + shader.
- **Flow**: 2D parchment editor (MapEditor) → height/biome layers → 3D terrain; supports FPS camera, minis, fog of war, grid.
- **References**: Open-VTT (Khazlor), itch.io parchment textures. Target: 1–2 hours for prototype.

Store the original `.txt` in `5-Attachments/Other/` for full detail.
