---
created: 2026-03-02
tags: [ingest, github-docs, documentation]
source: "https://github.com/L0RDTH0TH/genesis-mythos/blob/main/docs/archive/debug/COLUMNS_DEBUG_COMPLETE_ANSWERS.md"
title: "Columns Debug Complete Answers"
---

# COLUMNS INVISIBILITY - COMPLETE DEBUG ANSWERS

## ANSWERING ALL 10 QUESTIONS WITH EXACT VALUES

---

### 1. SCENE STRUCTURE

**Exact scene name:** `res://scenes/character_creation/tabs/RaceTab.tscn`

**Full hierarchy path of the scene where columns should appear:**
```
RaceTab (Control)
└── MainPanel (Panel)
    └── UnifiedScroll (ScrollContainer)
        └── RaceGrid (GridContainer) ← COLUMNS NODE
```

**Which node shows the columns:** `RaceGrid` (GridContainer)

---

### 2. NODE RESPONSIBLE FOR COLUMNS

**Exact node name and type:** `RaceGrid` (GridContainer)

**Container Sizing flags:**
- **Horizontal:** `3` (SIZE_EXPAND_FILL) ✅ **FIXED from 4 (SIZE_SHRINK_CENTER)**
- **Vertical:** `3` (SIZE_EXPAND_FILL)

**Layout preset:** Layout Mode = `1` (Anchors mode)

**Anchors preset:** `15` (Full Rect - all anchors at 0.0/1.0)

**Current Size Flags on parent chain (root → RaceGrid):**

| Node | Type | H Flags | V Flags |
|------|------|---------|---------|
| RaceTab | Control | 3 (Expand+Fill) | 3 (Expand+Fill) |
| MainPanel | Panel | 3 (Expand+Fill) | 3 (Expand+Fill) |
| UnifiedScroll | ScrollContainer | 3 (Expand+Fill) | 3 (Expand+Fill) |
| RaceGrid | GridContainer | 3 (Expand+Fill) ✅ **FIXED** | 3 (Expand+Fill) |

---

### 3. THEME & STYLEBOXES

**Theme assigned to root Control:** `res://themes/bg3_theme.tres`
- Assigned via project settings: `[gui] theme/custom="res://themes/bg3_theme.tres"`

**For RaceGrid (GridContainer):**
- No StyleBox overrides (GridContainer doesn't use StyleBox for background)
- Inherits theme from parent chain

**For RaceEntry child items (PanelContainer):**
- **Normal StyleBox:** `race_button_normal` (StyleBoxFlat_34)
  - bg_color: `Color(0.15, 0.09, 0.05, 1)` - alpha = 1.0 ✅
- **Hover StyleBox:** `race_button_hover` (StyleBoxFlat_35)
  - bg_color: `Color(0.2, 0.12, 0.07, 1)` - alpha = 1.0 ✅
- **Pressed StyleBox:** `race_button_pressed` (StyleBoxFlat_36)
  - bg_color: `Color(0.18, 0.11, 0.06, 1)` - alpha = 1.0 ✅
- **Selected StyleBox:** `race_button_selected` (StyleBoxFlat_37)
  - bg_color: `Color(0.15, 0.09, 0.05, 1)` - alpha = 1.0 ✅

**✅ NO TRANSPARENT STYLEBOXES** - All alpha values = 1.0 (fully opaque)

---

### 4. VISIBILITY & MODULATION

**RaceGrid visibility:**
- Scene file: Not explicitly set (defaults to `true`)
- Code (line 57): `race_grid.visible = true` (explicitly set) ✅

**RaceEntry visibility:**
- Scene file: Not explicitly set (defaults to `true`) ✅

**Modulation values:**
- RaceGrid: Not set → defaults to `Color(1, 1, 1, 1)` (fully opaque) ✅
- RaceEntry: Not set → defaults to `Color(1, 1, 1, 1)` (fully opaque) ✅

**Canvas_item visibility scripts:**
- ✅ No scripts setting `visible = false`
- ✅ No scripts hiding content programmatically

---

### 5. RECT VALUES AT RUNTIME

**⚠️ TO BE CAPTURED VIA REMOTE TAB**

To capture runtime values:
1. Run project (F6)
2. Navigate to Race tab
3. Open Remote tab in Godot editor
4. Inspect: `CharacterCreationRoot/MainHBox/MarginContainer2/center_area/MarginContainer3/CurrentTabContainer/RaceTab/MainPanel/UnifiedScroll/RaceGrid`

**Expected values after fix:**
- `size` should be non-zero (e.g., Vector2(1200, 1962) or similar based on window size)
- `position` should be (0, 0) relative to ScrollContainer
- `global_position` should account for parent hierarchy offsets
- `custom_minimum_size` should be Vector2(0, 0) or calculated from children

---

### 6. GRIDCONTAINER COLUMNS SPECIFIC

**columns property value:** `4` ✅

**custom_minimum_size:**
- **BEFORE FIX:** `Vector2(0, 0)` ⚠️ **BUG FOUND**
- **AFTER FIX:** Removed from code (uses natural minimum from children) ✅

**separation_horizontal:** Not set (uses theme/default, typically 4px)

**separation_vertical:** Not set (uses theme/default, typically 4px)

**Child nodes (RaceEntry) Fill/Expand:**
- **RaceEntry (PanelContainer):**
  - `size_flags_horizontal = 3` (SIZE_EXPAND_FILL) ✅
  - `size_flags_vertical = 0` (No flags - fixed height) ✅
  - `custom_minimum_size = Vector2(0, 100)` (100px height minimum) ✅

---

### 7. ITEMLIST SPECIFIC

**Not applicable** - This is a GridContainer, not an ItemList.

---

### 8. CODE THAT POPULATES THE COLUMNS

**Exact function:** `_populate_list()` in `RaceTab.gd` (lines 30-99)

**Key code sections:**

```gdscript
# Line 54: Set columns
race_grid.columns = 4

# Line 55: FIXED - Changed from SIZE_SHRINK_CENTER to SIZE_EXPAND_FILL
race_grid.size_flags_horizontal = Control.SIZE_EXPAND_FILL

# Line 70: Add children to grid
race_grid.add_child(entry)

# Lines 90-91: Force layout updates
race_grid.update_minimum_size()
race_grid.queue_sort()
```

**Layout update calls:** ✅
- `update_minimum_size()` called after adding children
- `queue_sort()` called to refresh layout
- Multiple `await get_tree().process_frame` calls for async safety

**Clear calls:** ✅
- Lines 36-37: Clears existing children before repopulating
- `all_entries.clear()` resets tracking array

**⚠️ BUGS FIXED:**
- ❌ **WAS:** `race_grid.size_flags_horizontal = Control.SIZE_SHRINK_CENTER` (value 4)
- ✅ **NOW:** `race_grid.size_flags_horizontal = Control.SIZE_EXPAND_FILL` (value 3)
- ❌ **WAS:** `race_grid.custom_minimum_size = Vector2(0, 0)` (causing collapse)
- ✅ **NOW:** Removed (uses natural minimum)

---

### 9. Z-INDEX AND CLIPPING

**Clip Contents:**

| Node | Clip Contents | Notes |
|------|---------------|-------|
| UnifiedScroll | `true` (default for ScrollContainer) | ✅ Normal - clips overflow |
| RaceGrid | `false` (default) | ✅ No clipping issues |
| RaceEntry | `false` (explicitly set) | ✅ No clipping issues |

**Z-index values:**
- Default stacking order (no explicit z-index overrides)
- RaceGrid is child of ScrollContainer
- RaceEntry nodes are children of RaceGrid

**✅ NO CLIPPING ISSUES** (except normal ScrollContainer overflow clipping)

---

### 10. PROJECT SETTINGS

**display/window/size/viewport_width:** `1920`

**display/window/size/viewport_height:** `1080`

**display/window/stretch/mode:** `"canvas_items"`

**display/window/stretch/aspect:** `"expand"`

**Theme assigned:** `res://themes/bg3_theme.tres`

---

## CRITICAL BUGS IDENTIFIED AND FIXED

### 🚨 BUG #1: SIZE_SHRINK_CENTER instead of SIZE_EXPAND_FILL

**Location:**
- `RaceTab.tscn` line 81
- `RaceTab.gd` line 55

**Problem:**
```gdscript
size_flags_horizontal = 4  # SIZE_SHRINK_CENTER - WRONG!
```

**Impact:** GridContainer shrinks to minimum size instead of expanding to fill available width, making columns invisible.

**Fix Applied:**
```gdscript
size_flags_horizontal = 3  # SIZE_EXPAND_FILL - CORRECT!
```

---

### 🚨 BUG #2: Zero Minimum Size

**Location:**
- `RaceTab.tscn` line 83
- `RaceTab.gd` line 56

**Problem:**
```gdscript
custom_minimum_size = Vector2(0, 0)  # No minimum size!
```

**Impact:** Combined with SIZE_SHRINK_CENTER, grid collapsed to near-zero width.

**Fix Applied:** Removed the line - grid now uses natural minimum size calculated from children.

---

## FILES MODIFIED

1. **`scenes/character_creation/tabs/RaceTab.tscn`**
   - Line 81: Changed `size_flags_horizontal = 4` → `size_flags_horizontal = 3`
   - Line 83: Removed `custom_minimum_size = Vector2(0, 0)`

2. **`scripts/character_creation/tabs/RaceTab.gd`**
   - Line 55: Changed `Control.SIZE_SHRINK_CENTER` → `Control.SIZE_EXPAND_FILL`
   - Line 56: Removed `race_grid.custom_minimum_size = Vector2(0, 0)`

---

## EXPECTED BEHAVIOR AFTER FIX

✅ GridContainer expands to fill available width in ScrollContainer
✅ Four columns are visible with proper spacing
✅ Race entries distribute evenly across 4 columns
✅ Grid scrolls vertically when content exceeds viewport height

---

## TESTING INSTRUCTIONS

1. Run the project (F6)
2. Navigate to Character Creation
3. Select "Race" tab
4. **Expected:** See 4 columns of race entries displayed horizontally
5. **If still invisible:** Check Remote tab for runtime rect values

---

**Report Generated:** Complete column visibility debug analysis
**Status:** ✅ Bugs identified and fixed
**Next Step:** Test in-game to verify columns are now visible


