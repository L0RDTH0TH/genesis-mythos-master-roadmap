---
created: 2026-03-02
tags: [ingest, github-docs, documentation]
source: "https://github.com/L0RDTH0TH/genesis-mythos/blob/main/audit/current_state_report.md"
title: "Current State Report"
---

# Codebase Investigation Report - December 27, 2025

**Project:** Genesis Mythos - Full First Person 3D Virtual Tabletop RPG  
**Godot Version:** 4.3.stable (project.godot shows 4.3, rules specify 4.5.1 - **VERSION MISMATCH**)  
**Investigation Date:** 2025-12-27  
**Purpose:** Current state analysis for prompt refinement and future implementation planning

---

## Executive Summary

The codebase has undergone a significant pivot from native Godot UI to **JavaScript/Alpine.js-based UI** delivered via `godot_wry` WebView nodes. Key systems (World Builder, Main Menu, Progress Dialog) now use HTML/CSS/JS with Alpine.js for reactivity, while maintaining bidirectional IPC communication with GDScript controllers.

**Current Status:**
- ✅ **Hybrid UI Architecture:** Native Godot UI (character creation, overlays) + WebView-based UI (world builder, main menu)
- ✅ **Azgaar Integration:** Fully implemented but currently **DISABLED** via `DEBUG_DISABLE_AZGAAR` flag
- ⚠️ **Version Mismatch:** Project uses Godot 4.3.stable but rules specify 4.5.1
- ⚠️ **Performance:** Documented performance issues (~5 FPS) with detailed audits available
- ✅ **Code Compliance:** Strong adherence to naming conventions, script headers, typed GDScript

---

## 1. Folder Structure

### 1.1 Compliance with Rules

The folder structure largely matches the rules specification from Section 2, with some additions and deviations:

| Path | Status | Notes |
|------|--------|-------|
| `res://assets/` | ✅ Compliant | Contains fonts, icons, models, textures, sounds, ui subfolders |
| `res://core/` | ✅ Compliant | Core engine systems (singletons, streaming, sim, procedural, utils, world_generation) |
| `res://data/` | ✅ Compliant | All JSON configs present, including `races.json`, `classes.json`, `archetypes/` |
| `res://scenes/` | ✅ Compliant | Core, ui, character_creation, tabletop, tools structure |
| `res://scripts/` | ✅ Compliant | Organized by feature (ui, character_creation, managers, etc.) |
| `res://themes/` | ✅ Compliant | `bg3_theme.tres` exists (2 theme files found) |
| `res://addons/` | ✅ Allowed | Terrain3D, GUT, ProceduralWorldMap, godot_wry explicitly supported |
| `res://tools/azgaar/` | ✅ Allowed | Full Azgaar bundle (338 SVG files, JS modules, heightmaps) |
| `res://web_ui/` | ⚠️ **NEW** | Not in original rules but required for WebView UI (main_menu, world_builder, overlays) |
| `res://audit/` | ✅ Allowed | Explicitly allowed per rules, contains 109 markdown audit files |
| `res://demo/` | ✅ Allowed | Demo scenes and tests |
| `res://tests/` | ✅ Allowed | Unit/integration tests with GUT |
| `res://godot/` | ⚠️ **UNUSUAL** | Contains 1352 files (md5, ctex, cfg) - appears to be cache/import artifacts |

### 1.2 Key Additions (Not in Original Rules)

- **`res://web_ui/`** - JavaScript/HTML/CSS files for WebView-based UIs
  - `web_ui/main_menu/` - Main menu HTML/CSS/JS
  - `web_ui/world_builder/` - World Builder UI with Alpine.js
  - `web_ui/overlays/progress_dialog/` - Progress dialog WebView
  - `web_ui/shared/` - Shared bridge.js and Alpine.min.js

- **`res://tools/azgaar/`** - Full Azgaar Fantasy Map Generator bundle
  - Complete HTML/JS/CSS bundle (703 files)
  - Heightmaps, textures, modules, libs
  - Served via `AzgaarServer` (embedded HTTP server) or file:// URLs

---

## 2. Key Systems Analysis

### 2.1 World Building System

**Status:** ✅ **FULLY IMPLEMENTED** (currently disabled via diagnostic flag)

**Architecture:**
```
WorldBuilderWeb.tscn (Control root)
└── WebView (godot_wry)
    └── Loads: res://web_ui/world_builder/index.html
    
WorldBuilderWebController.gd
├── Manages WebView IPC communication
├── Loads step definitions from JSON (azgaar_step_parameters.json)
├── Handles archetype presets
└── Coordinates with WorldBuilderAzgaar.gd for generation
```

**Key Files:**
- `res://scripts/ui/WorldBuilderWebController.gd` - WebView controller
- `res://scripts/ui/WorldBuilderAzgaar.gd` - Azgaar WebView integration (disabled)
- `res://scripts/managers/AzgaarIntegrator.gd` - Asset copying and URL management
- `res://scripts/managers/AzgaarServer.gd` - Embedded HTTP server for Azgaar files
- `res://web_ui/world_builder/index.html` - Alpine.js-based UI
- `res://data/config/azgaar_step_parameters.json` - 8-step parameter definitions

**Current Status:**
- ⚠️ **Azgaar WebView DISABLED:** `DEBUG_DISABLE_AZGAAR = true` in both `WorldBuilderAzgaar.gd` and `AzgaarServer.gd`
- ✅ **WebView UI ACTIVE:** World Builder UI loads and displays via `WorldBuilderWebController`
- ✅ **Parameter System:** Full 8-step wizard with Alpine.js reactivity
- ✅ **Data-Driven:** All parameters loaded from JSON configs

**Communication Flow:**
1. GDScript → JS: `web_view.execute_js()` / `web_view.eval()` sends step definitions, archetypes, params
2. JS → GDScript: `window.ipc.postMessage()` → `ipc_message` signal → `_on_ipc_message()`
3. Bridge: `web_ui/shared/bridge.js` provides `GodotBridge.postMessage()` wrapper

### 2.2 Procedural Generation System

**Status:** ✅ **IMPLEMENTED**

**Components:**
- `res://core/world_generation/MapGenerator.gd` - 2D map generation
- `res://core/world_generation/MapRenderer.gd` - Map rendering
- `res://core/world_generation/MapEditor.gd` - Map editing tools
- `res://core/world_generation/Terrain3DManager.gd` - Terrain3D integration
- `res://core/world_generation/WorldGenerator.gd` - High-level world generation orchestrator

**Addons:**
- `res://addons/terrain_3d/` - Terrain3D addon (128 files, stable)
- `res://addons/procedural_world_map/` - ProceduralWorldMap addon (18 files, explicitly supported)

**Integration:**
- Azgaar generates 2D heightmaps → exported to Image → Terrain3D imports
- `WorldBuilderAzgaar.gd` has `export_heightmap()` method (currently disabled)

### 2.3 UI Implementation

**Status:** ✅ **HYBRID ARCHITECTURE** (Native + WebView)

**Native Godot UI:**
- Character Creation (`res://scenes/character_creation/`) - Full native UI with SubViewport 3D preview
- Performance Monitor (`res://scenes/ui/overlays/PerformanceMonitor.tscn`) - Native overlay
- Loading Overlay (`res://scenes/ui/LoadingOverlay.tscn`) - Native overlay
- Debug Overlay (`res://scenes/ui/DebugOverlay.tscn`) - Native overlay

**WebView-Based UI (godot_wry):**
- Main Menu (`res://web_ui/main_menu/`) - HTML/CSS/JS with vanilla JavaScript
- World Builder (`res://web_ui/world_builder/`) - HTML/CSS with Alpine.js
- Progress Dialog (`res://web_ui/overlays/progress_dialog/`) - HTML/CSS/JS

**WebView Integration Pattern:**
```gdscript
# Controller script pattern (all WebView controllers follow this)
@onready var web_view: WebView = $WebView

func _ready() -> void:
    web_view.load_url("res://web_ui/[path]/index.html")
    web_view.ipc_message.connect(_on_ipc_message)
    
func _on_ipc_message(message: String) -> void:
    var json = JSON.new()
    json.parse(message)
    var data = json.data
    # Handle message...
```

**JavaScript Bridge Pattern:**
```javascript
// All WebView UIs use GodotBridge from bridge.js
GodotBridge.postMessage('message_type', { data: ... });

// Alpine.js components (World Builder)
Alpine.data('worldBuilder', () => ({
    currentStep: 0,
    params: {},
    // ... reactive state
}));
```

### 2.4 Character Creation System

**Status:** ✅ **IMPLEMENTED** (Native UI)

**Structure:**
- `res://scenes/character_creation/CharacterCreationRoot.tscn` - Main scene
- `res://scripts/character_creation/CharacterCreationRoot.gd` - Controller
- `res://scenes/character_creation/tabs/` - 6 tab scenes (Race, Class, Background, Ability Scores, Appearance, Name/Confirm)
- `res://scripts/character_creation/tabs/` - Tab controllers (all extend `BaseTab.gd`)
- `res://scripts/character_creation/CharacterPreview3D.gd` - 3D preview management

**Features:**
- ✅ Wizard-style flow (6 steps)
- ✅ 3D character preview (SubViewport + Node3D)
- ✅ Data-driven (loads from `races.json`, `classes.json`, `backgrounds.json`)
- ✅ Uses `UIConstants.gd` for sizing
- ✅ Theme applied (`bg3_theme.tres`)

**Data Files:**
- ✅ `data/races.json` - Exists
- ✅ `data/classes.json` - Exists
- ✅ `data/backgrounds.json` - Exists
- ✅ `data/abilities.json` - Exists
- ✅ `data/archetypes/` - 13 archetype JSON files

### 2.5 First-Person Controller

**Status:** ⚠️ **PARTIAL** (Demo only, not integrated)

**Current State:**
- `res://demo/src/Player.gd` - Demo character controller (CharacterBody3D)
  - Supports first-person toggle (V key)
  - Basic movement (WASD, QE for up/down)
  - Camera-relative movement
  - NOT integrated into main game flow

**Missing:**
- ❌ No integrated first-person controller in main scenes
- ❌ `CreativeFlyCamera` exists (`res://core/utils/creative_fly_camera.gd`) but is fly camera, not FPS
- ❌ No ground collision-based FPS controller

**Per Rules Section 10:**
> **🔄 In Progress:** First-person character controller integration

---

## 3. Code Compliance Audit

### 3.1 Script Headers

**Status:** ✅ **EXCELLENT COMPLIANCE**

All 30 GDScript files checked have proper headers:
```gdscript
# ╔═══════════════════════════════════════════════════════════
# ║ ScriptName.gd
# ║ Desc: Brief one-line description
# ║ Author: Lordthoth
# ╚═══════════════════════════════════════════════════════════
```

**Files Verified:** 30/30 scripts use exact header format

### 3.2 Naming Conventions

**Status:** ✅ **COMPLIANT**

- ✅ Variables/functions: `snake_case` (e.g., `current_step`, `_on_ipc_message`)
- ✅ Classes/Resources: `PascalCase` (e.g., `WorldBuilderWebController`, `UIConstants`)
- ✅ Constants: `ALL_CAPS` (e.g., `DEBUG_DISABLE_AZGAAR`, `BUTTON_HEIGHT_MEDIUM`)
- ✅ File names match class names: `WorldBuilderWebController.gd` → `class_name WorldBuilderWebController`

### 3.3 Typed GDScript

**Status:** ✅ **STRONG TYPING**

Examples from key files:
```gdscript
@onready var web_view: WebView = $WebView  # Typed
var current_step: int = 0  # Typed
var current_params: Dictionary = {}  # Typed
func _on_ipc_message(message: String) -> void:  # Typed params and return
```

**Compliance:** ~95% of code uses explicit typing

### 3.4 Magic Numbers

**Status:** ⚠️ **MOSTLY COMPLIANT** (some magic numbers remain)

**Good Examples:**
- `UIConstants.gd` provides semantic constants (`BUTTON_HEIGHT_MEDIUM = 80`)
- World Builder UI uses `UIConstants` for sizing
- Character Creation uses `UIConstants` for button heights

**Issues Found:**
- Some hard-coded values in UI controllers (e.g., `viewport_size.x * 0.6` in CharacterCreationRoot.gd line 63)
- Timer wait times sometimes hard-coded (e.g., `await get_tree().create_timer(1.5).timeout`)
- Magic numbers in performance monitoring code (acceptable for diagnostics)

**Recommendation:** Migrate remaining magic numbers to `UIConstants` or add as named constants.

### 3.5 Theme Usage

**Status:** ✅ **COMPLIANT**

- ✅ `bg3_theme.tres` exists at `res://themes/bg3_theme.tres`
- ✅ All native UI scenes reference the theme
- ✅ WebView UIs use CSS for styling (appropriate for HTML/CSS/JS architecture)
- ✅ Theme constants used via `theme_override_constants`

### 3.6 UI Responsiveness (Native UI Only)

**Status:** ⚠️ **PARTIAL COMPLIANCE**

**Good Examples:**
- WebView UIs are inherently responsive (HTML/CSS with percentage-based layouts)
- Character Creation uses `HSplitContainer` with `UIConstants` for sizing
- Anchors and size flags used appropriately in many scenes

**Areas Needing Review:**
- Some scenes may have hard-coded panel widths (audit needed for all native UI scenes)
- Window resize handling may be incomplete in some controllers
- Performance Monitor overlay has fixed positioning (acceptable for overlays)

**Note:** WebView-based UIs handle responsiveness via CSS, which is appropriate and compliant.

---

## 4. Performance Notes

### 4.1 Documented Performance Issues

**Status:** ⚠️ **PERFORMANCE ISSUES DOCUMENTED** (multiple audits available)

**Key Findings from Audits:**
1. **PerformanceMonitor._process()** - 12+ `Performance.get_monitor()` calls + 5+ `RenderingServer.get_rendering_info()` calls per frame (DETAILED mode: 20-50ms per frame)
2. **GraphControl._draw()** - Complex polygon calculations every frame
3. **WaterfallControl._draw()** - Drawing 480+ rectangles per frame
4. **Multiple _process() loops** - 8+ nodes with active `_process()` methods
5. **WorldBuilderUI._process()** - Always running even when idle (diagnostic code should be removed)

**Audit Files:**
- `audit/full_line_by_line_audit_2025-12-25.md` - Comprehensive performance audit
- `audit/GUI_performance_audit.md` - GUI-specific performance issues
- `audit/idle_fps_investigation.md` - Idle FPS investigation

**Current Status:**
- ⚠️ ~5 FPS reported in World Builder UI (even with Azgaar disabled)
- ✅ Performance monitoring systems exist and are functional
- ⚠️ Diagnostic code still present in production code (should be removed)

### 4.2 Engine Limitations

**Godot Version:**
- ⚠️ **VERSION MISMATCH:** `project.godot` shows `godot_version="4.3.stable"` but rules specify 4.5.1
- Need to verify if this is intentional or oversight

**WebView Performance:**
- `godot_wry` WebView may have performance overhead compared to native UI
- HTML/CSS rendering adds layer of abstraction
- IPC communication adds minimal overhead (JSON parsing)

### 4.3 Optimization Opportunities

**Recommended Actions:**
1. Remove diagnostic code from production (timing, frame counting in `_process()`)
2. Throttle PerformanceMonitor updates (memory/object counts every 10 frames, rendering info every 2-3 frames)
3. Reduce WaterfallControl redraw frequency
4. Disable `_process()` when not needed (only enable during generation)
5. Cache node references to avoid repeated `get_node()` calls

---

## 5. Azgaar Integration Details

### 5.1 Current Implementation

**Status:** ✅ **FULLY IMPLEMENTED** (currently disabled via `DEBUG_DISABLE_AZGAAR`)

**Architecture:**
```
AzgaarIntegrator (singleton)
├── Copies Azgaar bundle from res://tools/azgaar/ to user://azgaar/
└── Provides URL methods (get_azgaar_url(), get_azgaar_http_url())

AzgaarServer (singleton)
├── Embedded HTTP server (TCPServer on port 8080+)
├── Serves files from user://azgaar/
└── Provides MIME type handling

WorldBuilderAzgaar.gd
├── Manages WebView node (godot_wry)
├── Injects JavaScript bridge for communication
├── Executes JS via execute_js() / eval()
├── Handles parameter syncing via _sync_parameters_to_azgaar()
└── Exports heightmaps via export_heightmap()
```

### 5.2 Parameter Handling

**Method:** ✅ **Direct JavaScript Injection** (not file-based)

**Flow:**
1. User adjusts parameters in Alpine.js UI
2. `world_builder.js` calls `GodotBridge.postMessage('update_param', {...})`
3. `WorldBuilderWebController._handle_update_param()` stores in `current_params`
4. On generate, `WorldBuilderAzgaar._sync_parameters_to_azgaar()` executes JS:
   ```javascript
   azgaar.options.paramKey = value;
   ```
5. Azgaar generates map with injected parameters

**Parameter Sources:**
- `data/config/azgaar_step_parameters.json` - Step definitions with UI types, min/max, defaults
- `WorldBuilderWebController.ARCHETYPES` - Hard-coded archetype presets (High Fantasy, Low Fantasy, etc.)
- User input via Alpine.js UI

**Clamping:**
- `UIConstants.get_clamped_points()` - Hardware-based clamping for `pointsInput` parameter
  - Low-end hardware: max 500,000 points
  - High-end hardware: max 2,000,000 points

### 5.3 JavaScript Interaction

**Methods Used:**
- `web_view.execute_js(code: String) -> Variant` - Primary method (returns value)
- `web_view.eval(code: String)` - Fallback (void return)
- `web_view.post_message(message: String)` - Bidirectional IPC (not currently used for Azgaar)

**Bridge Injection:**
- `WorldBuilderAzgaar._inject_azgaar_bridge()` - Injects bridge script after page load
- Bridge hooks into `azgaar.generate()` to send completion events
- Listens for `mapGenerated` events

**Current Limitations:**
- ⚠️ Azgaar WebView currently disabled (`DEBUG_DISABLE_AZGAAR = true`)
- ⚠️ Heightmap export not tested (method exists but disabled)
- ⚠️ Parameter syncing not tested with actual Azgaar instance

### 5.4 Options.json vs Direct JS

**Previous Approach (Deprecated):**
- Writing `options.json` to `user://azgaar/options.json`
- Loading Azgaar with `?json=user://azgaar/options.json#` URL parameter
- Reloading page to apply options

**Current Approach (Active):**
- Direct JavaScript injection: `azgaar.options.paramKey = value`
- No file I/O overhead
- Real-time parameter updates (no page reload)
- More reliable (no file path issues)

**Recommendation:** Current approach is superior. No migration to `options.json` needed.

---

## 6. Gaps and Recommendations

### 6.1 Critical Gaps

| Gap | Severity | Impact | Recommendation |
|-----|----------|--------|----------------|
| **Godot Version Mismatch** | 🔴 High | May cause compatibility issues | Verify if 4.3 is intentional or migrate to 4.5.1 |
| **Azgaar Disabled** | 🟡 Medium | World generation not functional | Re-enable `DEBUG_DISABLE_AZGAAR = false` after testing |
| **First-Person Controller** | 🟡 Medium | Core feature incomplete | Integrate demo Player.gd or create new FPS controller |
| **Performance Issues** | 🟡 Medium | Poor UX (~5 FPS) | Implement optimizations from audit reports |
| **Diagnostic Code in Production** | 🟢 Low | Minor overhead | Remove timing/frame counting from `_process()` methods |

### 6.2 Code Quality Gaps

| Area | Issue | Recommendation |
|------|-------|----------------|
| **Magic Numbers** | Some hard-coded values remain | Migrate to `UIConstants` or named constants |
| **UI Responsiveness** | Some native UI scenes need audit | Review all native UI scenes for anchor/size flag compliance |
| **Error Handling** | Limited error handling in WebView IPC | Add try-catch in JS, error signals in GDScript |

### 6.3 Feature Gaps (Per Rules Section 10)

**In Progress:**
- ✅ **UI Polish** - WebView UI is polished, native UI needs consistency review
- ⚠️ **First-Person Controller** - Demo exists but not integrated

**Planned/Future:**
- ❌ **Tabletop Overlay System** - Dice, tokens, fog of war not implemented
- ❌ **Multiplayer Networking** - `NetworkManager.gd` singleton not found
- ❌ **Expanded Sound Integration** - Basic structure exists but not expanded

### 6.4 Recommendations for Future Prompts

**For World Building:**
- Specify that Azgaar is currently disabled and needs re-enabling
- Use `WorldBuilderWebController` pattern for WebView IPC
- Reference `azgaar_step_parameters.json` for parameter definitions
- Use Alpine.js for reactive UI state

**For UI Development:**
- **Native UI:** Use `UIConstants`, anchors, size flags, theme
- **WebView UI:** Use HTML/CSS/JS with Alpine.js, `GodotBridge` for IPC
- Specify which UI approach (native vs WebView) for new features

**For Azgaar Integration:**
- Parameters are synced via direct JS injection (not `options.json`)
- Use `UIConstants.get_clamped_points()` for hardware-aware clamping
- Bridge script must be injected after Azgaar page loads
- Test with `DEBUG_DISABLE_AZGAAR = false`

**For Performance:**
- Reference audit files for known bottlenecks
- Avoid per-frame operations when possible
- Throttle expensive calls (RenderingServer, Performance.get_monitor)
- Remove diagnostic code before production

**For Code Compliance:**
- Always use exact script header format
- Use `UIConstants` for sizing (no magic numbers >10)
- Apply `bg3_theme.tres` to native UI
- Use typed GDScript everywhere

---

## 7. Summary

### 7.1 Implementation Status (Per Rules Section 10)

**✅ Implemented:**
- Procedural world generation (MapGenerator, MapRenderer, MapEditor, Terrain3D integration)
- Terrain3D integration and streaming
- 8-step World Builder UI wizard with Azgaar integration (UI complete, Azgaar disabled)
- Azgaar WebView integration using godot_wry (implemented, disabled)
- Core singletons (Eryndor, Logger, WorldStreamer, EntitySim, FactionEconomy)
- CreativeFlyCamera for 3D exploration
- Basic save/load foundations
- GUT setup for unit/integration testing
- **Character Creation System** (6-step wizard with 3D preview)
- **Hybrid UI Architecture** (Native + WebView via godot_wry)

**🔄 In Progress:**
- First-person character controller integration (demo exists, not integrated)
- UI polish and theme consistency (WebView UI polished, native UI needs review)

**📋 Planned / Future:**
- Full character creation system + data files (**✅ Data files exist, system is functional**)
- Tabletop overlay system (dice, tokens, fog of war)
- Multiplayer networking (NetworkManager.gd singleton)
- Expanded sound integration

### 7.2 Architecture Summary

**UI Architecture:**
- **Hybrid Approach:** Native Godot UI (character creation, overlays) + WebView-based UI (main menu, world builder) via `godot_wry`
- **Communication:** Bidirectional IPC via `ipc_message` signal and `GodotBridge.postMessage()`
- **State Management:** Alpine.js for WebView UIs, GDScript signals for native UI

**World Generation:**
- **2D Generation:** Azgaar Fantasy Map Generator (disabled but implemented)
- **3D Integration:** Terrain3D addon for heightmap → 3D terrain conversion
- **Data Flow:** Azgaar → heightmap Image → Terrain3D → procedural world

**Code Quality:**
- **Strong Compliance:** Headers, naming, typing all excellent
- **Minor Issues:** Some magic numbers, diagnostic code in production
- **Performance:** Documented issues with multiple optimization paths identified

### 7.3 Key Takeaways for Prompt Refinement

1. **UI Approach:** Always specify native vs WebView (use WebView for complex reactive UIs, native for simple overlays)
2. **Azgaar Status:** Currently disabled - reference `DEBUG_DISABLE_AZGAAR` flag
3. **Parameter Handling:** Use direct JS injection, not `options.json`
4. **Compliance:** Strong adherence to rules - reference existing code for patterns
5. **Performance:** Be aware of documented bottlenecks (PerformanceMonitor, _process() loops)
6. **Version:** Confirm Godot version (4.3 vs 4.5.1 mismatch needs resolution)

---

## 8. Appendix: File Inventory

### 8.1 Key Script Files

| Path | Lines | Purpose | Status |
|------|-------|---------|--------|
| `scripts/ui/WorldBuilderWebController.gd` | 408 | WebView controller for World Builder | ✅ Active |
| `scripts/ui/WorldBuilderAzgaar.gd` | 401 | Azgaar WebView integration | ⚠️ Disabled |
| `scripts/managers/AzgaarIntegrator.gd` | 138 | Azgaar asset management | ✅ Active |
| `scripts/managers/AzgaarServer.gd` | 295 | Embedded HTTP server | ⚠️ Disabled |
| `scripts/ui/MainMenuWebController.gd` | 116 | Main menu WebView controller | ✅ Active |
| `scripts/ui/UIConstants.gd` | 111 | UI sizing constants | ✅ Active |
| `scripts/character_creation/CharacterCreationRoot.gd` | 312 | Character creation controller | ✅ Active |

### 8.2 Key Data Files

| Path | Purpose | Status |
|------|---------|--------|
| `data/config/azgaar_step_parameters.json` | 8-step parameter definitions | ✅ Active |
| `data/races.json` | Race definitions | ✅ Exists |
| `data/classes.json` | Class definitions | ✅ Exists |
| `data/backgrounds.json` | Background definitions | ✅ Exists |
| `data/archetypes/` | 13 archetype JSON files | ✅ Exists |

### 8.3 WebView UI Files

| Path | Purpose | Status |
|------|---------|--------|
| `web_ui/world_builder/index.html` | World Builder UI (Alpine.js) | ✅ Active |
| `web_ui/world_builder/world_builder.js` | Alpine.js data component | ✅ Active |
| `web_ui/main_menu/index.html` | Main menu UI | ✅ Active |
| `web_ui/shared/bridge.js` | IPC bridge library | ✅ Active |

---

**Report Generated:** 2025-12-27  
**Investigation Method:** Static code analysis, file system traversal, key file review  
**Confidence Level:** High (comprehensive file review, multiple audits referenced)


