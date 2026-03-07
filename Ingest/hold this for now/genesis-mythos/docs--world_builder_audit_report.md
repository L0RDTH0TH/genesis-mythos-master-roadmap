---
created: 2026-03-02
tags: [ingest, github-docs, documentation]
source: "https://github.com/L0RDTH0TH/genesis-mythos/blob/main/docs/world_builder_audit_report.md"
title: "World Builder Audit Report"
---

# Audit Report: Azgaar Fork, Dual Grid Integration, and UI/UX Setup
**Date:** 2026-01-11  
**Project:** Genesis Mythos  
**Godot Version:** 4.6-beta2  
**Purpose:** Comprehensive audit of Azgaar integration, dual grid system, and UI/UX setup, with UX planning and tool integration recommendations

---

## 1. Audit of Azgaar Fork

### 1.1 Summary of Integration Status

The Azgaar Fantasy Map Generator (FMG) is integrated via a **clean modular fork architecture** using embedded WebView (godot_wry). The integration follows a **fork mode** where the Azgaar Genesis fork is loaded as a JavaScript ES module within the World Builder HTML page, enabling direct API access without iframe communication overhead.

**Integration Mode:** Fork (embedded ES module)  
**Status:** ✅ Functional but requires initialization hook for border system  
**Architecture:** WebView → HTML/JS → Azgaar Genesis Fork (ES module)

### 1.2 Key Files and Modifications

#### Core Integration Files

1. **`assets/ui_web/js/azgaar/azgaar-genesis.esm.js`**
   - Modular ES module bundle for Azgaar Genesis fork
   - Provides: `initGenerator()`, `loadOptions()`, `generateMap()`, `getMapData()`, `renderPreview()`, `renderPreviewSVG()`
   - Status: ✅ Loaded and functional

2. **`assets/ui_web/templates/world_builder.html`**
   - Main HTML template hosting the Azgaar fork
   - Fork is initialized via JavaScript after Alpine.js ready
   - Contains iframe wrapper structure (legacy, may be deprecated)
   - Status: ✅ Functional, fork loads correctly

3. **`assets/ui_web/js/world_builder.js`**
   - Alpine.js data and IPC handlers
   - Fork initialization logic: `window.AzgaarGenesis.initGenerator()`
   - Generation handler: `handleGenerateMap()` function
   - Status: ✅ Functional, IPC communication working

4. **`scripts/ui/WorldBuilderWebController.gd`**
   - GDScript controller for World Builder WebView
   - Handles IPC messages: `map_generated`, `map_generation_failed`
   - Map generation trigger: `_trigger_fork_generation()`
   - Status: ✅ Functional, but missing StateBorderManager initialization hook

#### Key Integration Points

- **Fork Initialization:** JavaScript calls `AzgaarGenesis.initGenerator(Delaunator)` after Alpine.js ready
- **Map Generation:** User triggers generation → JavaScript calls `AzgaarGenesis.generateMap()` → Returns data → Sends to Godot via IPC `map_generated`
- **Data Extraction:** Godot receives JSON via `_handle_map_generated()` handler
- **Preview Rendering:** Fork provides SVG preview via `renderPreviewSVG()` or canvas via `renderPreview()`

### 1.3 Issues and Gaps

1. **Missing Border System Initialization Hook** ❌ **CRITICAL**
   - **Issue:** `StateBorderManager.initialize(azgaar_data)` is never called when map generation completes
   - **Location:** `scripts/ui/WorldBuilderWebController.gd` → `_handle_map_generated()`
   - **Impact:** Borders never computed, even though infrastructure exists
   - **Fix Required:** Add initialization call after map data received

2. **WebView URL Bug** ⚠️ **KNOWN ISSUE**
   - **Issue:** World Builder WebView shows GitHub page instead of local UI (documented in `docs/investigation_world_builder_github_bug.md`)
   - **Status:** Partially fixed (URL property added to scene), but may still occur
   - **Impact:** Blocks testing, but doesn't affect functionality when working

3. **Config File Missing** ⚠️ **MINOR**
   - **Issue:** `data/config/state_border_config.json` referenced but not created
   - **Impact:** Defaults used, but configuration-driven behavior unavailable

---

## 2. Audit of Dual Grid Integration

### 2.1 Status per Phase

#### Phase 1: Dual Grid Foundation ✅ **COMPLETE**

**Implementation:** `scripts/procedural/DualGridManager.gd` (360 lines)

- ✅ Configuration loading (`load_config()`)
- ✅ Azgaar data extraction (`initialize_from_azgaar()`)
- ✅ Primary grid storage (points, cells, neighbors, states)
- ✅ Dual grid construction (`_build_dual_grid()`)
- ✅ Border edge detection and deduplication
- ✅ State borders dictionary (`state_borders: Dictionary`)
- ✅ Border edge retrieval (`get_border_edges_for_state()`)

**Tests:** `tests/procedural/DualGridManagerTest.gd` (434 lines, 8 tests, all passing)

**Code Quality:** Excellent - typed GDScript, error handling, docstrings, no linter errors

#### Phase 2: Map-Edge Wrapping ✅ **COMPLETE**

**Implementation:** `scripts/procedural/DualGridManager.gd` (continued)

- ✅ `enable_wrapping` toggle (`@export var enable_wrapping: bool = true`)
- ✅ Map dimensions storage (`map_width`, `map_height`)
- ✅ Edge cell detection (`is_edge_cell()`)
- ✅ Toroidal wrapping (`get_wrapped_neighbor()`)
- ✅ Wrapped border path generation (`get_wrapped_border_path()`)
- ✅ Chain-following algorithm with visited set (prevents infinite loops)

**Tests:** Included in DualGridManagerTest.gd (3 wrapping-specific tests)

**Code Quality:** Robust, handles edge cases, safety limits in place

#### Phase 3: Dynamic Border Merging ⚠️ **PARTIAL**

**Implementation:** `scripts/managers/StateBorderManager.gd` (153 lines)

**Complete:**
- ✅ Signal declaration (`borders_updated(state_id: int, new_path: Array[Vector2])`)
- ✅ DualGridManager integration (RefCounted instantiation)
- ✅ Border cache (`border_cache: Dictionary`)
- ✅ Initialization method (`initialize(azgaar_data)`)
- ✅ State change handler (`on_state_changed()`) - emits signal with wrapped path

**Stubbed:**
- ⚠️ `merge_states(state_id_a, state_id_b)` - TODO comments, cache clearing only, no cell reassignment
- ⚠️ `add_burg_or_land(position, new_state_id)` - Complete placeholder, no-op

**Tests:** `tests/managers/StateBorderManagerTest.gd` (229 lines, 4 tests, all passing)

#### Phase 4: GUI Visualization ⚠️ **PARTIAL**

**Infrastructure Complete:**
- ✅ SVG overlay layers (`#state-borders-svg`, `#state-borders-svg-canvas`)
- ✅ Alpine.js toggle (`showBorders: true`)
- ✅ UI checkbox control for border visibility
- ✅ CSS styling (fantasy-themed gold borders)
- ✅ JavaScript handler (`handleBorderUpdate(stateId, path)`)
- ✅ IPC message listener (`border_update` / `borders_updated`)
- ✅ GDScript IPC bridge (`_on_borders_updated()` in WorldBuilderWebController)

**Integration Gap:**
- ❌ `StateBorderManager.initialize()` never called → borders never computed → no SVG paths rendered

**Phase 5: Performance Optimization** ❌ **NOT STARTED**

- No profiling or benchmarking
- No incremental recalculation
- No cache optimization

### 2.2 Key Files and Code Quality

| File | Lines | Status | Quality |
|------|-------|--------|---------|
| `scripts/procedural/DualGridManager.gd` | 360 | ✅ Complete | Excellent (typed, documented, tested) |
| `scripts/managers/StateBorderManager.gd` | 153 | ⚠️ Partial | Good (stubs marked, well-structured) |
| `scripts/ui/WorldBuilderWebController.gd` | 2145 | ⚠️ Partial | Good (IPC exists, init missing) |
| `tests/procedural/DualGridManagerTest.gd` | 434 | ✅ Complete | Excellent (8 tests, comprehensive) |
| `tests/managers/StateBorderManagerTest.gd` | 229 | ✅ Complete | Good (4 tests, coordinator focus) |

### 2.3 Integration with Azgaar

**Current State:**
- DualGridManager can extract data from Azgaar JSON structure
- StateBorderManager has initialization method ready
- IPC bridge exists for sending border updates to WebView
- JavaScript handlers ready to render SVG paths

**Critical Gap:**
- `StateBorderManager.initialize(azgaar_data)` is **never called** when `_handle_map_generated()` receives map data
- Location: `scripts/ui/WorldBuilderWebController.gd` line ~1550
- Required: Add initialization call, then trigger border path generation for all states

### 2.4 Testing Status

**Unit Tests:**
- ✅ DualGridManagerTest.gd: 8 tests, all passing
- ✅ StateBorderManagerTest.gd: 4 tests, all passing

**Integration Tests:**
- ❌ Missing: No end-to-end test for Azgaar → DualGrid → StateBorder → WebView → SVG

**Manual Testing:**
- ⚠️ Blocked: Cannot test visualization without initialization fix

---

## 3. Audit of Current UI/UX Setup

### 3.1 Wizard Flow Description

The World Builder uses an **8-step wizard flow** with a three-column layout:

**Layout Structure:**
- **Left Panel:** Numbered tab bar (BG3-style) with 8 steps
- **Center Panel:** Map preview (SVG/canvas) with overlay controls
- **Right Panel:** Step-specific parameters (curated parameter tree)

**Step Definitions:** Loaded from `data/config/azgaar_step_parameters.json`

**Steps (from config):**
1. **Terrain & Heightmap** - Template, cell density, height parameters
2. **Societies & Politics** - States, cultures, religions, manors
3. **Settlements & Scale** - Burgs, population, settlement parameters
4. **Climate & Environment** - Precipitation, temperature, biome settings
5. **States & Provinces** - State/culture growth, expansion, size variety
6. **Environment** - Additional climate/biome refinements
7. **Rivers & Water** - River generation, water parameters
8. **Finalize** - Seed, generation trigger, preview controls

**Current Flow:**
1. User selects archetype (High Fantasy, Dark Fantasy, etc.) → Loads preset parameters
2. User navigates steps via left tabs → Right panel shows curated parameters for that step
3. User adjusts parameters → Changes stored in Alpine.js state
4. User clicks "Generate" (final step or trigger) → JavaScript calls `handleGenerateMap()`
5. Fork generates map → Sends JSON to Godot via IPC
6. Godot receives data → Saves to file, renders preview (SVG/canvas)
7. Preview displayed in center panel → User can toggle SVG/canvas mode

### 3.2 WebView/HTML/JS Implementation

**Technology Stack:**
- **WebView:** godot_wry (embedded browser)
- **HTML:** `assets/ui_web/templates/world_builder.html`
- **CSS:** `assets/ui_web/css/world_builder.css` (fantasy-themed, responsive)
- **JavaScript:** `assets/ui_web/js/world_builder.js` (Alpine.js data + IPC handlers)
- **Framework:** Alpine.js for reactivity

**Architecture:**
- Alpine.js `x-data` provides reactive state
- IPC bridge (`GodotBridge.postMessage()`) for Godot → JS communication
- WebView `ipc_message` signal for JS → Godot communication
- Fork embedded as ES module (no iframe overhead)

**Current Interactivity:**
- ✅ Step navigation (left tabs)
- ✅ Parameter editing (right panel, various input types)
- ✅ Archetype selection (dropdown)
- ✅ Preview mode toggle (SVG ↔ Canvas)
- ✅ Border visibility toggle (checkbox, but borders not visible due to init gap)
- ✅ Generate button (triggers map generation)

### 3.3 Current Interactivity

**Working:**
- Step navigation
- Parameter input (sliders, spinboxes, dropdowns)
- Archetype preset loading
- Map generation trigger
- Preview display (SVG/canvas)
- Preview mode toggle
- Border visibility toggle (UI exists, but no borders to show)

**Missing/Incomplete:**
- ❌ Border visualization (blocked by initialization gap)
- ❌ Interactive map manipulation (no brushes, no state editing)
- ❌ Capital placement tools
- ❌ State merging UI
- ❌ Era/time progression controls
- ❌ Influence/culture spread tools

### 3.4 Pain Points

1. **Grey Placeholder Screen**
   - **Issue:** Center panel shows "Azgaar Genesis Fork - Ready" message until generation
   - **Impact:** No visual feedback until generation completes
   - **Recommendation:** Show loading state, progress bar, or sample preview

2. **Lack of Immediate Feedback**
   - **Issue:** Parameter changes don't show preview updates until full regeneration
   - **Impact:** User must regenerate entire map to see changes
   - **Recommendation:** Live preview updates (debounced) or "Apply" button per step

3. **No Post-Generation Editing**
   - **Issue:** Once map is generated, user cannot modify states/borders/capitals
   - **Impact:** User must regenerate with new parameters if unsatisfied
   - **Recommendation:** Post-generation editing tools (brushes, merge buttons, etc.)

4. **Border System Not Visible**
   - **Issue:** Borders never appear due to initialization gap
   - **Impact:** Cannot test or demonstrate border system
   - **Recommendation:** Fix initialization hook (P0 priority)

5. **No State/Culture Visualization**
   - **Issue:** States and cultures exist in data but not visually represented
   - **Impact:** User cannot see political/cultural boundaries
   - **Recommendation:** Color-coded state regions, border lines, culture overlay

---

## 4. Fleshing Out User Experience with Available Tools

### 4.1 Potential Tools Overview

Based on the dual grid system architecture and Townscaper-inspired emergence philosophy, the following tools can enhance the World Builder UX:

#### 4.1.1 State Merging Tools

**Merge Button/Tool:**
- **Description:** Click two states to merge them (state_b merges into state_a)
- **Visual:** Button in toolbar, or click state_a then state_b to merge
- **Feedback:** Borders update in real-time, merged state adopts state_a's color/culture
- **Implementation:** Calls `StateBorderManager.merge_states(state_id_a, state_id_b)`

**Split State Tool:**
- **Description:** Select a state, draw a line to split it into two states
- **Visual:** Brush tool that draws split line, preview shows split before confirmation
- **Feedback:** New state created, borders recalculated
- **Implementation:** Requires splitting logic (not yet implemented)

#### 4.1.2 Influence/Culture Spread Tools

**Influence Brush (Townscaper-inspired):**
- **Description:** Paint brush that expands a state's influence/culture into adjacent cells
- **Visual:** Brush cursor (circle/radius), paint preview overlay, real-time border updates
- **Feedback:** Borders expand as user paints, state grows organically
- **Implementation:** Calls `StateBorderManager.add_burg_or_land()` for each painted cell
- **UX Inspiration:** Townscaper's organic growth, where painting creates natural boundaries

**Culture Overlay Brush:**
- **Description:** Toggle overlay showing culture spread, brush to modify culture assignments
- **Visual:** Color-coded culture regions, brush modifies culture without changing state borders
- **Feedback:** Culture colors update, borders remain unchanged
- **Implementation:** Requires culture modification logic (future enhancement)

#### 4.1.3 Capital Placement Tools

**Capital Placement Tool:**
- **Description:** Click on a state to place/relocate its capital (burg)
- **Visual:** Capital marker (crown icon, star), click to place, drag to relocate
- **Feedback:** Capital marker moves, state re-centers around new capital (if implemented)
- **Implementation:** Requires capital placement logic (future enhancement)

**Auto-Capital Tool:**
- **Description:** Automatically place capitals at state centers of mass
- **Visual:** Button triggers auto-placement, markers appear
- **Feedback:** All capitals placed, user can manually adjust
- **Implementation:** Calculate state centroids, place capitals

#### 4.1.4 Era/Time Progression Tools

**Era Slider:**
- **Description:** Slider to progress through time eras (Ancient, Medieval, Renaissance, etc.)
- **Visual:** Horizontal slider, era label, preview of era-appropriate states/cultures
- **Feedback:** States expand/contract, cultures evolve, borders shift
- **Implementation:** Requires era-based state evolution (future enhancement)

**Time Step Controls:**
- **Description:** Play/Pause/Step buttons for time progression
- **Visual:** Media player-style controls, timeline with markers
- **Feedback:** States grow/shrink over time, borders update frame-by-frame
- **Implementation:** Requires state growth simulation (future enhancement)

#### 4.1.5 Border Refinement Tools

**Border Smoothing Brush:**
- **Description:** Brush to smooth jagged borders (relaxation algorithm)
- **Visual:** Brush cursor, preview of smoothed border before applying
- **Feedback:** Borders become smoother, more natural-looking
- **Implementation:** Requires border relaxation logic (future enhancement)

**Border Manual Edit Tool:**
- **Description:** Click and drag border vertices to manually adjust borders
- **Visual:** Vertex handles on borders, drag to adjust, snap to grid option
- **Feedback:** Border updates in real-time, state areas recalculate
- **Implementation:** Requires vertex editing logic (future enhancement)

#### 4.1.6 State Creation Tools

**New State Brush:**
- **Description:** Paint brush to create new states from neutral/unclaimed land
- **Visual:** Brush cursor, paint creates new state with unique ID
- **Feedback:** New state appears with default color/culture, borders calculated
- **Implementation:** Calls `StateBorderManager.add_burg_or_land()` with new_state_id

**State Deletion Tool:**
- **Description:** Click state to delete it (cells become neutral/unclaimed)
- **Visual:** Delete button or right-click menu, confirmation dialog
- **Feedback:** State removed, borders updated for neighboring states
- **Implementation:** Requires state deletion logic (future enhancement)

### 4.2 How Each Tool Enhances UX (Townscaper-Inspired Emergence)

**Townscaper Philosophy:**
- **Organic Growth:** Tools enable emergent, intuitive world-building
- **Immediate Feedback:** Visual updates happen in real-time as user interacts
- **No Mode Switching:** Tools work directly on the map, no separate editing mode
- **Playful Exploration:** User can experiment freely, undo/redo available

**Tool Benefits:**

1. **Merge Button** → Enables political consolidation, creates larger empires
2. **Influence Brush** → Organic state expansion, intuitive territory painting
3. **Capital Placement** → Strategic positioning, visual state centers
4. **Era Slider** → Historical progression, dynamic border evolution
5. **Border Smoothing** → Aesthetic refinement, natural-looking boundaries
6. **New State Brush** → Creative freedom, user-guided world-building

### 4.3 Visual/Inspirational Ideas

**Visual Design:**
- **Tool Palette:** Left sidebar or floating toolbar with icon buttons (merge, brush, capital, etc.)
- **Brush Cursor:** Circle with radius indicator, color-coded by tool type
- **State Colors:** Distinct colors per state (generated or user-assigned), semi-transparent fill
- **Border Lines:** Gold/glowing lines (current CSS styling), thicker on hover
- **Capital Markers:** Crown/star icons, glow effect, tooltip with state name
- **Influence Overlay:** Gradient fill showing state influence strength, fades at borders
- **Culture Overlay:** Color-coded regions, toggleable via checkbox
- **Era Timeline:** Horizontal bar with era labels, draggable slider, play/pause buttons

**Interaction Patterns:**
- **Click to Select:** Click state to select (highlight, show borders, show info panel)
- **Click to Merge:** Select state_a, click state_b to merge
- **Paint to Expand:** Click and drag to paint influence, real-time border updates
- **Drag to Place:** Drag capital marker to relocate, snap to valid positions
- **Slider to Progress:** Drag era slider to see time progression, states evolve
- **Hover for Info:** Hover state to show tooltip (name, culture, population, etc.)

**Feedback Mechanisms:**
- **Real-time Updates:** Borders redraw as user interacts (incremental recalculation)
- **Preview Mode:** Show preview of changes before applying (e.g., split line preview)
- **Undo/Redo:** Stack of actions, Ctrl+Z / Ctrl+Y to undo/redo
- **Confirmation Dialogs:** For destructive actions (delete state, merge large states)
- **Progress Indicators:** Show recalculation progress for large operations

---

## 5. Decisions and Recommendations

### 5.1 How to Use the Tools (Workflows, Triggers)

#### 5.1.1 Workflow Patterns

**Pattern 1: Pre-Generation Editing (Step 8)**
- User adjusts parameters in wizard steps 1-7
- Step 8: Preview + Post-Generation Tools
- User generates map → Tools become available for refinement
- User can merge states, place capitals, adjust borders
- User can regenerate if unsatisfied, or proceed to 3D bake

**Pattern 2: Post-Generation Editing Mode**
- After generation, enter "Edit Mode" (button/toggle)
- Tools appear in toolbar (merge, brush, capital, etc.)
- User edits states/borders → Real-time updates
- Exit edit mode → Return to preview/parameter view

**Pattern 3: Interactive Generation**
- User triggers generation → Preview appears
- Tools available immediately (no separate mode)
- User can edit while preview is visible
- Changes trigger incremental border recalculation

#### 5.1.2 Tool Triggers

**Merge Tool:**
- **Trigger:** Click "Merge States" button → Enter merge mode → Click state_a → Click state_b
- **Alternative:** Select state_a → Ctrl+Click state_b → Merge dialog appears
- **Workflow:** `User Action → StateBorderManager.merge_states() → DualGridManager recalc → Signal emitted → SVG update`

**Influence Brush:**
- **Trigger:** Select brush tool → Set radius (slider) → Click and drag on map
- **Workflow:** `Mouse Move → Detect cells under brush → StateBorderManager.add_burg_or_land() → Incremental recalc → Signal emitted → SVG update`

**Capital Placement:**
- **Trigger:** Click "Place Capital" button → Click state → Click position on state
- **Workflow:** `Click State → Show placement cursor → Click Position → Update capital location → Visual update`

**Era Slider:**
- **Trigger:** Drag slider → State evolution simulation runs
- **Workflow:** `Slider Value → Calculate era state → StateBorderManager.on_state_changed() → Border updates → Signal emitted → SVG update`

### 5.2 Integration with Dual Grid

#### 5.2.1 Incremental Recalculation Strategy

**Current State:**
- `StateBorderManager.on_state_changed()` recalculates entire border path
- No incremental optimization

**Recommended Approach:**
1. **Region-Based Updates:** Only recalc borders for affected regions (cells changed)
2. **Dirty Flag System:** Mark states as "dirty" when cells change, batch recalc
3. **Cache Invalidation:** Clear cache for affected states only
4. **Async Processing:** Use `call_deferred()` for heavy recalculations

**Integration Points:**
- `merge_states()` → Mark both states dirty → Recalc merged state + neighbors
- `add_burg_or_land()` → Mark affected state dirty → Recalc state borders
- `on_state_changed()` → Use dirty flags → Incremental recalc → Emit signal

#### 5.2.2 Signal Emission Strategy

**Current State:**
- Signal emitted per state change
- No batching

**Recommended Approach:**
- **Batch Updates:** Collect multiple state changes → Emit once per frame
- **Debouncing:** For rapid changes (brush painting), debounce signal emission
- **Priority System:** Critical updates (merge) emit immediately, cosmetic updates (smoothing) batch

**Implementation:**
```gdscript
# Pseudocode
var pending_updates: Dictionary = {}  # state_id -> path
func queue_border_update(state_id: int, path: Array[Vector2]):
    pending_updates[state_id] = path
    if not update_timer.is_connected(_flush_updates):
        update_timer.timeout.connect(_flush_updates)
        update_timer.start(0.1)  # 100ms debounce

func _flush_updates():
    for state_id in pending_updates:
        borders_updated.emit(state_id, pending_updates[state_id])
    pending_updates.clear()
```

### 5.3 Which Tools to Expose (Priorities, Simple vs Advanced)

#### Priority 1: Essential Tools (MVP)

1. **Border Visibility Toggle** ✅ **ALREADY IMPLEMENTED**
   - Simple checkbox, no additional work needed (once init fixed)

2. **State Merge Button**
   - **Complexity:** Medium (merge logic needs implementation)
   - **Value:** High (enables political consolidation)
   - **UI:** Button in toolbar, click two states to merge
   - **Estimated Effort:** 4-6 hours (implement merge_states())

3. **Influence Brush (Basic)**
   - **Complexity:** High (requires brush interaction, incremental recalc)
   - **Value:** Very High (core Townscaper-inspired UX)
   - **UI:** Brush tool with radius slider, paint to expand states
   - **Estimated Effort:** 8-12 hours (implement add_burg_or_land() + brush UI)

#### Priority 2: Enhancement Tools (Post-MVP)

4. **Capital Placement Tool**
   - **Complexity:** Medium (requires capital data structure)
   - **Value:** Medium (strategic positioning)
   - **UI:** Click state → Click position to place capital
   - **Estimated Effort:** 4-6 hours

5. **State Selection/Info Panel**
   - **Complexity:** Low (UI only, data exists)
   - **Value:** Medium (user feedback)
   - **UI:** Click state → Show info panel (name, culture, population, etc.)
   - **Estimated Effort:** 2-3 hours

#### Priority 3: Advanced Tools (Future)

6. **Era Slider**
   - **Complexity:** Very High (requires state evolution simulation)
   - **Value:** High (dynamic progression)
   - **Estimated Effort:** 16-24 hours

7. **Border Smoothing Brush**
   - **Complexity:** High (requires relaxation algorithm)
   - **Value:** Medium (aesthetic refinement)
   - **Estimated Effort:** 8-12 hours

8. **Split State Tool**
   - **Complexity:** Very High (requires state splitting logic)
   - **Value:** Medium (advanced editing)
   - **Estimated Effort:** 12-16 hours

#### Recommendation: Start with Priority 1 (MVP)

**MVP Toolset:**
- Border visibility toggle (done, needs init fix)
- State merge button (implement merge_states())
- Basic influence brush (implement add_burg_or_land() + brush UI)

**Rationale:**
- Provides core editing capabilities
- Demonstrates dual grid system effectively
- Enables Townscaper-inspired emergence
- Manageable scope (12-18 hours total)

### 5.4 When to Expose Them (Mapping to Wizard Steps 1-8)

#### Step 8: Finalize & Edit (Recommended Location)

**Current Step 8:** Finalize - Seed, generation trigger, preview controls

**Proposed Enhancement:**
- **Pre-Generation:** Seed input, generate button, preview controls
- **Post-Generation:** Tools become available after map generates
- **Layout:** 
  - Left: Step 8 parameters (seed, etc.)
  - Center: Map preview with tools overlay
  - Right: Tool palette (merge, brush, capital, etc.)

**Rationale:**
- Natural flow: User generates → Tools appear for refinement
- No disruption to parameter flow (steps 1-7 remain parameter-focused)
- Clear separation: Parameter editing (steps 1-7) vs. Visual editing (step 8)

#### Alternative: Separate "Edit Mode" Toggle

**Location:** Top bar or center panel control

**Flow:**
1. User generates map (step 8 or generate button)
2. Preview appears
3. "Enter Edit Mode" button/toggle appears
4. User clicks → Tools appear, edit mode active
5. User edits → Real-time updates
6. "Exit Edit Mode" → Return to preview/parameter view

**Rationale:**
- Clear mode separation
- Tools don't clutter parameter UI
- User can switch between edit and parameter views

#### Recommendation: Hybrid Approach

**Step 8 Enhancement:**
- Pre-generation: Parameter controls (seed, generate button)
- Post-generation: Tools appear below preview (toolbar or floating palette)
- No separate mode toggle (tools always available post-generation)

**Benefits:**
- Simple UX (no mode switching)
- Tools appear contextually (only after generation)
- Natural workflow (generate → refine → proceed)

---

## 6. Next Steps and Estimated Effort

### 6.1 Immediate Fixes (P0 - Critical)

#### Fix 1: Connect StateBorderManager Initialization

**Location:** `scripts/ui/WorldBuilderWebController.gd` → `_handle_map_generated()`

**Action:**
1. Add `state_border_manager.initialize(map_data)` call after map data received
2. Trigger border path generation for all states
3. Emit `borders_updated` signals for all states
4. Test: Verify borders appear in preview

**Estimated Effort:** 1-2 hours

**Code Snippet (Pseudocode):**
```gdscript
func _handle_map_generated(data: Dictionary) -> void:
    var map_data: Dictionary = data.get("data", {})
    # ... existing code ...
    
    # Initialize border system
    if state_border_manager != null:
        state_border_manager.initialize(map_data)
        
        # Generate borders for all states
        var state_ids = state_border_manager.dual_grid_manager.state_borders.keys()
        for state_id in state_ids:
            var path = state_border_manager.dual_grid_manager.get_wrapped_border_path(state_id)
            state_border_manager.borders_updated.emit(state_id, path)
```

#### Fix 2: Create Config File

**Location:** `data/config/state_border_config.json`

**Action:** Create JSON file with default settings

**Estimated Effort:** 30 minutes

**Content (Example):**
```json
{
  "wrapping": {
    "enabled": true,
    "default": true
  },
  "border": {
    "threshold": 5.0,
    "smoothing": false
  },
  "performance": {
    "incremental_recalc": false,
    "cache_enabled": true
  }
}
```

### 6.2 Implementation Plan

#### Phase 3 Completion (MVP Tools)

**Step 1: Implement Merge Logic** (4-6 hours)
- Complete `StateBorderManager.merge_states()`
- Cell reassignment in `primary_grid.cell_states`
- Dual grid border rebuild for affected regions
- Test with multiple state merges

**Step 2: Implement Add Burg/Land Logic** (6-8 hours)
- Complete `StateBorderManager.add_burg_or_land()`
- Cell detection (nearest cell to position)
- State assignment (auto-detect or user-specified)
- Border expansion/recalculation
- Test with brush interaction

**Step 3: Add Merge Button UI** (2-3 hours)
- Add button to toolbar (HTML/JS)
- Click handlers (select state_a, click state_b)
- IPC communication (Godot → JS → Godot)
- Visual feedback (state highlighting)

**Step 4: Add Influence Brush UI** (4-6 hours)
- Brush tool (HTML/JS canvas interaction)
- Radius slider
- Mouse tracking (click, drag, release)
- Cell detection under brush
- IPC communication for each painted cell

**Step 5: Integration Testing** (2-3 hours)
- End-to-end test: Generate → Merge → Brush → Verify borders
- Performance testing (large maps, many states)
- UI/UX polish (visual feedback, error handling)

**Total Phase 3 Completion:** 18-26 hours

#### Phase 5: Performance Optimization (Future)

**Step 1: Profiling** (2-4 hours)
- Benchmark border generation for various map sizes
- Identify bottlenecks (dual grid construction, path generation)

**Step 2: Incremental Recalculation** (8-12 hours)
- Region-based border updates
- Dirty flag system
- Cache invalidation strategy

**Step 3: Batch Signal Emission** (2-4 hours)
- Debouncing for rapid changes
- Priority system (critical vs. cosmetic)

**Total Phase 5:** 12-20 hours

### 6.3 Total Estimated Effort

| Task | Effort (Hours) | Priority |
|------|----------------|----------|
| Fix initialization hook | 1-2 | P0 |
| Create config file | 0.5 | P1 |
| Implement merge_states() | 4-6 | P2 |
| Implement add_burg_or_land() | 6-8 | P2 |
| Add merge button UI | 2-3 | P2 |
| Add influence brush UI | 4-6 | P2 |
| Integration testing | 2-3 | P2 |
| **MVP Total** | **20-30** | - |
| Performance profiling | 2-4 | P3 |
| Incremental recalculation | 8-12 | P3 |
| Batch signal emission | 2-4 | P3 |
| **Phase 5 Total** | **12-20** | - |
| **Grand Total** | **32-50** | - |

### 6.4 Recommended Sequencing

**Week 1: Unblock Visualization**
1. Fix initialization hook (1-2 hours)
2. Create config file (0.5 hours)
3. Test end-to-end border visualization (1 hour)
4. **Result:** Borders visible, system demonstrable

**Week 2-3: MVP Tools**
5. Implement merge_states() (4-6 hours)
6. Add merge button UI (2-3 hours)
7. Implement add_burg_or_land() (6-8 hours)
8. Add influence brush UI (4-6 hours)
9. Integration testing (2-3 hours)
10. **Result:** Core editing tools functional

**Week 4+: Enhancements**
11. Performance optimization (Phase 5)
12. Additional tools (capital placement, era slider, etc.)
13. UI/UX polish

---

## 7. Conclusion

The World Builder has a **solid foundation** with Azgaar fork integration, dual grid system, and GUI infrastructure. The **critical gap** (StateBorderManager initialization) blocks visualization, but once fixed, borders will appear correctly. The system is **well-architected** and ready for tool implementation.

**Recommended Path Forward:**
1. **Immediate:** Fix initialization hook (1-2 hours) → Borders visible
2. **Short-term:** Implement MVP tools (20-30 hours) → Core editing capabilities
3. **Long-term:** Performance optimization + advanced tools (12-20+ hours) → Full feature set

**Key Success Factors:**
- Incremental approach (fix init → add tools → optimize)
- User testing (gather feedback on tool UX)
- Performance monitoring (ensure real-time updates stay responsive)
- Clear documentation (tool usage, integration points)

The system is **ready for completion** and will provide a **Townscaper-inspired emergence experience** for user-guided world-building.

