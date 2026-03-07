---
tags: [bug, fixed, ui, navigation]
status: resolved
date: 2025-10-30
severity: minor
project: Mythos Gen
component: fractal-wheel
proposal_path: Ingest/Decisions/Decision-for-label-ghosting-fix--2026-03-04-0441.md
---
# Label Ghosting Fix

## Problem Description

When pressing **ESC** to navigate back through menus in the Fractal Wheel, text from the previous submenu remained visible during the fade transition, creating a "ghosting" effect.

**Symptoms**:
- ✅ Forward navigation worked perfectly
- ❌ Backward navigation showed old text briefly during fade-in
- Visual inconsistency between navigation directions

## Root Cause

The bug was caused by a **timing issue** in the animation sequence:

1. `navigate_back()` would call `build_torus()` during the tween callback
2. `build_torus()` used `queue_free()` to remove old labels
3. `queue_free()` marks nodes for deletion at frame end (not immediate)
4. Fade-in animation started before labels were actually deleted
5. Old labels briefly visible during alpha 0.0 → 1.0 transition

### Why Forward Worked But Backward Didn't

- **Forward**: Labels scale down (0.8) making ghosting less noticeable
- **Backward**: Labels scale up (1.2) making ghosting MORE noticeable
- Timing window was longer during reverse animation

## Solution

Created a new `_clear_all_labels()` function that:
- Uses `free()` instead of `queue_free()` for instant deletion
- Gets called **before** animation starts in both directions
- Ensures labels are gone before any fade effects begin

### Code Changes

**Modified**: `scripts/gui/FractalWheel.gd`

1. Added `_clear_all_labels()` helper function (uses `free()` not `queue_free()`)
2. Called `_clear_all_labels()` at start of `zoom_to_child()`
3. Called `_clear_all_labels()` at start of `navigate_back()`
4. Removed redundant clearing from `build_torus()`

## Result

Both forward and backward navigation now have clean transitions with no text ghosting.

## Testing

- ✅ Project loads without errors
- ✅ Forward navigation works (unchanged behavior)
- ✅ Backward navigation now matches forward (no ghosting)

## Related Components

- [[Fractal Wheel]] - Main navigation component
- [[WedgeSegment]] - Individual menu segments
- [[Menu Navigation]] - Overall navigation system

## Links

- Full technical details: `/LABEL_GHOSTING_FIX.md` in project root
- Related: [[Submenu Navigation Fix]] (previous fix)

## Review Needed
Proposed para-type: project. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.