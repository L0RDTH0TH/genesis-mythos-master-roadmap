---
created: 2026-03-02
tags: [ingest, github-docs, documentation]
source: "https://github.com/L0RDTH0TH/genesis-mythos/blob/main/docs/investigation_world_builder_github_bug.md"
title: "Investigation World Builder Github Bug"
---

# Investigation Report: World Builder Showing godot_wry GitHub Page
**Date:** 2026-01-11  
**Project:** Genesis Mythos  
**Godot Version:** 4.6-beta2  
**Purpose:** Diagnose why World Builder UI fails to load and shows external GitHub repo instead.

---

## Executive Summary

The World Builder UI is configured to load `res://assets/ui_web/templates/world_builder.html` via `WorldBuilderWebController._ready()`, which calls `web_view.load_url()` after the scene loads. However, the WebView node in `WorldBuilderWeb.tscn` has **no URL property set in the scene file itself**. The root cause hypothesis is that the godot_wry WebView addon may have a default URL or fallback behavior that loads when no URL is explicitly set, or there may be a timing issue where the WebView initializes with a default URL before `_ready()` executes. The GitHub URL (`https://github.com/doceazedo/godot_wry`) appears in the addon's demo files but is not directly referenced in the codebase, suggesting it may be a built-in default or demo URL in the godot_wry addon itself.

---

## 1. Reproduction Steps

1. Launch the game from `MainMenuWeb.tscn`
2. Click the "Create World" button (or "World Builder" menu item)
3. Expected: World Builder UI loads with three-column layout (left step tabs, center preview, right parameters)
4. Actual: WebView displays `https://github.com/doceazedo/godot_wry` instead of the local UI

---

## 2. Scene Inspection

### 2.1 WorldBuilderWeb Scene Structure

**File:** `res://ui/world_builder/WorldBuilderWeb.tscn`

```
[gd_scene load_steps=4 format=3 uid="uid://world_builder_web_phase2"]

[node name="WorldBuilderWebRoot" type="Control"]
├── script = "res://scripts/ui/WorldBuilderWebController.gd"
└── [node name="WebView" type="WebView" parent="."]
    ├── layout_mode = 1
    ├── anchors_preset = 15 (FULL_RECT)
    └── [NO url PROPERTY SET]
```

**Key Finding:** The WebView node has **no `url` property** defined in the scene file. This is different from the godot_wry example scene (`addons/godot_wry/examples/example.tscn`), which explicitly sets `url = "res://addons/godot_wry/examples/test.html"`.

### 2.2 Comparison with Example Scene

**File:** `res://addons/godot_wry/examples/example.tscn` (lines 31-38)
```
[node name="WebView" type="WebView" parent="Window"]
full_window_size = false
url = "res://addons/godot_wry/examples/test.html"  # ✅ URL SET IN SCENE
anchors_preset = 15
...
```

**Difference:** The example scene sets `url` directly in the scene file, while `WorldBuilderWeb.tscn` relies entirely on script-based `load_url()` calls.

---

## 3. Script Analysis

### 3.1 WorldBuilderWebController._ready()

**File:** `res://scripts/ui/WorldBuilderWebController.gd` (lines 62-84)

```gdscript
func _ready() -> void:
	"""Initialize the WebView and load the World Builder HTML."""
	MythosLogger.info("WorldBuilderWebController", "_ready() called")
	
	# ... diagnostic logging ...
	
	if not web_view:
		MythosLogger.error("WorldBuilderWebController", "WebView node not found!")
		return
	
	# ... load step definitions and archetype presets ...
	
	# Load the World Builder HTML file (default: fork mode)
	current_mode = MODE_FORK
	var html_url: String = "res://assets/ui_web/templates/world_builder.html"
	web_view.load_url(html_url)
	MythosLogger.info("WorldBuilderWebController", "Loaded World Builder HTML (fork mode)", {"url": html_url, "mode": current_mode})
```

**Analysis:**
- Script correctly calls `web_view.load_url("res://assets/ui_web/templates/world_builder.html")`
- URL is hardcoded and should load the local HTML file
- Logging indicates the call is made

### 3.2 Scene Loading Flow

**File:** `res://core/scenes/world_root.gd` (lines 106-176)

1. User clicks "Create World" button → navigates to `world_root.tscn`
2. `world_root._ready()` calls `_setup_world_builder_ui_async()`
3. Scene loads `WorldBuilderWeb.tscn` via `load("res://ui/world_builder/WorldBuilderWeb.tscn")`
4. Scene is instantiated and added to CanvasLayer
5. `WorldBuilderWebController._ready()` should execute and call `load_url()`

**Potential Issue:** There may be a race condition where the WebView initializes with a default URL before `_ready()` executes, or `load_url()` fails silently and the WebView falls back to a default.

---

## 4. WebView Configuration

### 4.1 File Existence Verification

**Command:** `test -f /home/darth/Final-Approach/assets/ui_web/templates/world_builder.html`
**Result:** ✅ **EXISTS** - The target HTML file exists at the expected path.

### 4.2 godot_wry Addon Structure

**Directory:** `res://addons/godot_wry/`
- Contains compiled binaries for Linux (`libgodot_wry.so`)
- Example scenes in `examples/` directory
- No Rust/C++ source code visible (binary addon)

### 4.3 Default URL Investigation

**Search Results:**
- No direct references to `github.com/doceazedo/godot_wry` in the codebase
- Reference found in `addons/godot_wry/examples/character_creator_ui_demo/ui/src/routes/+layout.svelte` (line 39-40) as a **link in the demo UI**, not a default URL
- No `@export var url` or default URL properties found in visible addon files
- Binary addon (`libgodot_wry.so`) contains strings but analysis was limited

**Finding:** The GitHub URL does not appear to be explicitly set as a default in the project code. It may be:
1. A built-in default in the godot_wry addon binary
2. A fallback URL when file loading fails
3. An error page or demo URL embedded in the addon

---

## 5. Addon Inspection

### 5.1 godot_wry Example Scene

**File:** `res://addons/godot_wry/examples/example.tscn`

```gdscript
[node name="WebView" type="WebView" parent="Window"]
full_window_size = false
url = "res://addons/godot_wry/examples/test.html"  # Explicit URL in scene
```

**Observation:** The example scene sets `url` directly in the scene file properties, suggesting this is the recommended approach.

### 5.2 addons/godot_wry/index.html

**Status:** File exists but is a simple HTML file (not inspected in detail). No indication it's used as a default.

---

## 6. Logs & Errors

**Note:** This investigation was performed in read-only mode. Actual runtime logs were not captured, but based on previous audit reports, the expected log sequence should be:

```
[WorldBuilderWebController] [INFO]: _ready() called
[WorldBuilderWebController] [INFO]: Loaded World Builder HTML (fork mode) {"url":"res://assets/ui_web/templates/world_builder.html"}
```

**Potential Silent Failures:**
- If `load_url()` fails, it may not log an error
- WebView may silently fall back to a default URL
- File loading errors (e.g., path resolution) may not be visible in logs

---

## 7. Hypotheses & Evidence

### Hypothesis 1: WebView Initializes Before _ready() Executes
**Evidence:**
- WebView node has no URL property in scene file
- `_ready()` is called after the node enters the scene tree
- WebView may initialize with a default URL on creation

**Likelihood:** ⭐⭐⭐ (Medium) - Node initialization timing could cause this, but `_ready()` should execute before the WebView becomes visible.

### Hypothesis 2: load_url() Fails Silently / File Not Found
**Evidence:**
- File exists at expected path (verified)
- No error logging visible (but logs weren't captured in this investigation)
- WebView may fall back to a default/demo URL on error

**Likelihood:** ⭐⭐ (Low-Medium) - File exists, but path resolution or file access issues could cause silent failure.

### Hypothesis 3: godot_wry Has Built-in Default/Demo URL
**Evidence:**
- GitHub URL (`github.com/doceazedo/godot_wry`) appears in addon demo files
- No explicit default URL found in project code
- Binary addon may contain embedded default URLs

**Likelihood:** ⭐⭐⭐⭐ (High) - Most likely, as the GitHub URL is specifically the addon author's repository and appears when no URL is set or when file loading fails.

### Hypothesis 4: Scene File Missing URL Property
**Evidence:**
- `WorldBuilderWeb.tscn` WebView node has no `url` property
- Example scene (`example.tscn`) explicitly sets `url` in scene file
- Script-based `load_url()` may not override scene defaults in all cases

**Likelihood:** ⭐⭐⭐⭐ (High) - Strong evidence that setting URL in scene file is the recommended approach, and script-based loading may not work reliably.

---

## 8. Recommended Fixes

### Fix 1: Set URL Property in Scene File (Recommended)

**File:** `res://ui/world_builder/WorldBuilderWeb.tscn`

**Action:** Add `url` property to the WebView node in the scene file:

```
[node name="WebView" type="WebView" parent="."]
layout_mode = 1
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
grow_horizontal = 2
grow_vertical = 2
url = "res://assets/ui_web/templates/world_builder.html"  # ✅ ADD THIS
```

**Rationale:** This matches the pattern used in the godot_wry example scene and ensures the URL is set before the WebView initializes, avoiding timing issues.

### Fix 2: Verify load_url() Timing (If Fix 1 Doesn't Work)

**File:** `res://scripts/ui/WorldBuilderWebController.gd`

**Action:** Ensure `load_url()` is called immediately in `_ready()` before any async operations:

```gdscript
func _ready() -> void:
	if not web_view:
		MythosLogger.error("WorldBuilderWebController", "WebView node not found!")
		return
	
	# Load URL FIRST, before other initialization
	var html_url: String = "res://assets/ui_web/templates/world_builder.html"
	web_view.load_url(html_url)
	MythosLogger.info("WorldBuilderWebController", "Loaded World Builder HTML", {"url": html_url})
	
	# Then load step definitions, etc.
	_load_step_definitions()
	_load_archetype_presets()
	# ...
```

**Rationale:** Ensures URL is set as early as possible in the initialization sequence.

### Fix 3: Add Error Handling for load_url()

**File:** `res://scripts/ui/WorldBuilderWebController.gd`

**Action:** Add error checking and logging:

```gdscript
var html_url: String = "res://assets/ui_web/templates/world_builder.html"
var file_exists = ResourceLoader.exists(html_url)
if not file_exists:
	MythosLogger.error("WorldBuilderWebController", "HTML file not found!", {"url": html_url})
else:
	web_view.load_url(html_url)
	MythosLogger.info("WorldBuilderWebController", "Loaded World Builder HTML", {"url": html_url})
```

**Rationale:** Provides visibility into file loading failures.

### Fix 4: Check WebView URL Property After Load

**Action:** Add diagnostic logging to verify the URL was set:

```gdscript
# After load_url() call
if web_view.has_method("get_url") or "url" in web_view:
	var current_url = web_view.get("url") if web_view.has_method("get") else null
	MythosLogger.debug("WorldBuilderWebController", "WebView URL after load_url", {"current_url": current_url})
```

**Rationale:** Helps diagnose if `load_url()` actually sets the URL property.

### Fix 5: Test with Explicit URL in Scene (Priority)

**Action:** Apply Fix 1 first, as it's the most likely solution based on the example scene pattern.

---

## 9. Additional Notes

- The GitHub URL (`github.com/doceazedo/godot_wry`) is the official repository for the godot_wry addon
- The addon author (doceazedo) may have included this as a default/demo URL in the binary
- Previous audit reports indicate the World Builder UI has been working, suggesting this may be a recent regression or environment-specific issue
- The file `res://assets/ui_web/templates/world_builder.html` exists and should be accessible

---

## Conclusion

The most likely root cause is that the WebView node in `WorldBuilderWeb.tscn` lacks an explicit `url` property in the scene file, causing the godot_wry addon to fall back to a default/demo URL (the GitHub repository). The recommended fix is to add the `url` property directly to the WebView node in the scene file, matching the pattern used in the godot_wry example scene. This ensures the URL is set during scene initialization, before the WebView becomes visible, avoiding any timing issues with script-based `load_url()` calls.

