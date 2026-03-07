---
created: 2026-03-02
tags: [ingest, github-docs, documentation]
source: "https://github.com/L0RDTH0TH/genesis-mythos/blob/main/assets/textures/README_PARCHMENT_SELECTION.md"
title: Readme Parchment Selection
proposal_path: Ingest/Decisions/Decision-for-genesis-mythos-assets-textures-parchment--2026-03-04-0442.md
---
# Parchment Texture Selection Guide

## Quick Selection Commands

Once you've chosen your favorites, copy them to the main textures directory:

```bash
# Example: Select Image_005.png as primary background
cp BeerPaper1/Image_005.png parchment_background.png

# Example: Select Image_032.png as stain overlay
cp BeerPaper2/Image_032.png parchment_stain_overlay.png
```

## Recommendations

- **Primary Background**: Choose images with:
  - Good overall beige/brown parchment color
  - Subtle stains (not too dark)
  - Even lighting (no harsh shadows)
  - High resolution (all are ~20-35MB, so they're high-res)

- **Stain Overlay**: Choose images with:
  - Interesting stain patterns
  - Can be slightly darker for contrast
  - Different pattern than primary for variety

## View Images in Godot

1. Open Godot Editor
2. Navigate to `res://assets/textures/BeerPaper1/` or `BeerPaper2/`
3. Click any PNG file to preview in the bottom panel
4. Once selected, copy to `parchment_background.png` in the textures root

The parchment shader will automatically use your selection once it's named correctly.

## Review Needed
Proposed para-type: archive. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.