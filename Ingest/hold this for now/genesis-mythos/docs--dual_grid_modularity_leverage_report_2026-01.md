---
created: 2026-03-02
tags: [ingest, github-docs, documentation]
source: "https://github.com/L0RDTH0TH/genesis-mythos/blob/main/docs/dual_grid_modularity_leverage_report_2026-01.md"
title: "Dual Grid Modularity Leverage Report 2026 01"
---

# Leveraging Azgaar Genesis Fork Iteration 2 Modularity for Dual Grid & World Building Improvements in Genesis Mythos

**Date:** 2026-01-09  
**Project:** Genesis Mythos – Full First Person 3D Virtual Tabletop RPG  
**Godot Version:** 4.6-beta2  
**Report Type:** Integration Strategy & Technical Analysis

---

## Executive Summary

The Azgaar Genesis fork has undergone significant Iteration 2 improvements that introduce **phase-based modularity**, **surgical regeneration capabilities**, and **intelligent caching** with dependency validation. These architectural enhancements can dramatically improve both the **Stålberg-inspired dual grid system** (Voronoi/Delaunay meshes, state border merging) and the **overall world-building UX** in Genesis Mythos by enabling:

1. **Incremental regeneration** of political/cultural layers without touching terrain
2. **Fast cache restoration** for locked terrain with rapid state/province updates
3. **Live preview feedback** during parameter tweaking without full rebuilds
4. **Targeted phase execution** for specific dual grid operations (e.g., STATE regeneration only)

This report analyzes the Iteration 2 improvements, explains their benefits for dual grid operations and world-building workflows, provides usage examples, and outlines prioritized recommendations for integration.

---

## Iteration 2 Improvements Summary

### Core Architectural Enhancements

#### 1. Phase-Based Modularity (`skipPhases` & `generatePartial`)

**What it is:**
- **16 distinct generation phases** (VORONOI, HEIGHTMAP, GRID_MARKUP, MAP_COORDINATES, TEMPERATURES, PRECIPITATION, PACK_CREATION, RIVERS, BIOMES, PACK_MARKUP, CLUSTER_MERGE, RANK_CELLS, CULTURES, BURGS, STATES, PROVINCES, RELIGIONS, EMBLEMS)
- **`skipPhases` option**: Array of phase names to skip during generation (e.g., `skipPhases: [PHASES.STATES, PHASES.PROVINCES]`)
- **`generatePartial(phasesToRun)` API**: Runs only specified phases, skipping all others automatically

**Key Benefits:**
- **Surgical regeneration**: Regenerate only STATES/PROVINCES without touching VORONOI/HEIGHTMAP
- **Fast iteration**: Lock terrain, tweak political parameters, regenerate in seconds
- **Selective updates**: Update cultures without regenerating burgs/states

**Implementation Location:**
- `src/generator.js`: Main generation loop with phase checks
- `src/partials.js`: `generatePartial()` function and phase dependency validation

#### 2. Dependency Graph & Validation (`PHASE_DEPENDENCIES`)

**What it is:**
- **Explicit dependency graph** defining which phases require which others
- **`validatePhaseDependencies()`**: Pre-execution validation ensuring all dependencies are met (either executed or cached)
- **Hard requirement enforcement**: RANK_CELLS is required for political phases (CULTURES, BURGS, STATES, PROVINCES)

**Key Benefits:**
- **Prevents corruption**: Catches missing dependencies before generation starts
- **Clear error messages**: `DependencyError` with specific phase names and resolution hints
- **Automatic dependency resolution**: Can auto-include required phases if cached

**Example Dependency Chain:**
```
STATES → requires → BURGS → requires → CULTURES → requires → RANK_CELLS → requires → BIOMES, PACK_MARKUP
```

**Implementation Location:**
- `src/partials.js`: `PHASE_DEPENDENCIES` constant and `validatePhaseDependencies()` function

#### 3. Intelligent Caching System

**What it is:**
- **Phase-level caching**: Each phase caches only its relevant data subset (e.g., VORONOI caches grid structure, STATES caches `pack.states` and `pack.cells.state`)
- **FIFO eviction**: `manageCacheSize()` evicts oldest entries when `maxCachedPhases` limit exceeded (default: 8)
- **Efficient deep copy**: `efficientDeepCopyOfRelevantData()` uses `structuredClone()` when available, falls back to JSON round-trip
- **Cache restoration**: `restorePhaseData()` merges cached data back into current state

**Key Benefits:**
- **Memory efficient**: Only stores what's needed per phase (not full map data)
- **Fast restoration**: Restore VORONOI/HEIGHTMAP from cache in milliseconds
- **Bounded growth**: Automatic eviction prevents unbounded memory growth

**Cache Structure:**
```javascript
state.cached = {
  [PHASES.VORONOI]: { grid: { cells: {...}, points: [...], vertices: {...} } },
  [PHASES.HEIGHTMAP]: { grid: { cells: { h: [...] } } },
  [PHASES.STATES]: { pack: { states: [...], cells: { state: [...] } } },
  // ... up to maxCachedPhases entries
}
```

**Implementation Location:**
- `src/partials.js`: `efficientDeepCopyOfRelevantData()`, `restorePhaseData()`, `manageCacheSize()`

#### 4. Phase-Specific RNG Seeds (`getPhaseSeed`)

**What it is:**
- **Deterministic phase seeds**: `getPhaseSeed(mainSeed, phaseName)` generates phase-specific seeds via hash function
- **RNG consistency**: Same main seed + phase name always produces same RNG sequence
- **Isolated randomness**: Each phase has independent RNG, allowing partial regeneration with consistent results

**Key Benefits:**
- **Reproducibility**: Regenerate STATES with same seed → same state boundaries
- **Isolation**: Changing STATE parameters doesn't affect VORONOI (different seeds)
- **Debugging**: Can reproduce specific phase issues with exact seed

**Formula:**
```javascript
phaseSeed = hash(mainSeed + phaseName)  // Returns string seed for RNG
```

**Implementation Location:**
- `src/partials.js`: `getPhaseSeed()` function

#### 5. Deep Merge Utility (`deepMerge`)

**What it is:**
- **Recursive object merging**: Handles nested objects, typed arrays, and plain arrays
- **Typed array preservation**: Uses `.slice()` to preserve typed array types (Uint8Array, Uint16Array, etc.)
- **Index-based array merging**: Merges arrays by index (source overwrites target at same indices)

**Key Benefits:**
- **Safe partial updates**: `generatePartial()` merges partial data without corrupting existing structures
- **Type preservation**: Maintains typed arrays (critical for performance in large maps)
- **Nested structure support**: Handles complex nested objects (grid.cells, pack.features, etc.)

**Implementation Location:**
- `src/partials.js`: `deepMerge()` function

---

## Benefits for Dual Grid System in Genesis Mythos

### Current Dual Grid Implementation

The `DualGridManager.gd` class currently:

1. **Extracts primary grid data** from Azgaar JSON (`grid.points`, `grid.cells`, `pack.cells.state`)
2. **Builds dual grid representation** by identifying border edges between cells with different state IDs
3. **Creates border segments** with midpoint calculations for state boundary visualization
4. **Supports toroidal wrapping** for borders crossing map boundaries

**Current Limitations:**
- **Full regeneration required**: Changing state parameters requires full map regeneration (slow, ~30-60s)
- **No incremental updates**: Cannot update state borders without regenerating terrain
- **Cache not utilized**: No mechanism to preserve terrain while updating politics

### How Iteration 2 Improves Dual Grid Operations

#### 1. Incremental STATE/PROVINCE Regeneration

**Scenario:** User wants to adjust `statesNumber` from 18 to 25 without changing terrain.

**Current Flow (Slow):**
```
User changes statesNumber → Full generation (VORONOI → HEIGHTMAP → ... → STATES) → 45s wait → DualGridManager re-initializes
```

**Iteration 2 Flow (Fast):**
```javascript
// Lock terrain (cache VORONOI, HEIGHTMAP, PACK_CREATION)
// Update statesNumber in options
// Regenerate only STATES phase
generatePartial([PHASES.STATES]);  // ~2-5s
// DualGridManager re-initializes from updated pack.cells.state
```

**Benefits:**
- **10-20x faster**: 2-5s vs 45s for state border updates
- **Terrain preserved**: Heightmap, biomes, rivers unchanged
- **Live feedback**: User sees border changes immediately

#### 2. Local Edits with Fast Cache Restore

**Scenario:** User manually edits state boundaries in DualGridManager, then wants to regenerate provinces to match.

**Iteration 2 Flow:**
```javascript
// User edits state borders via DualGridManager (manual merge/split)
// Export edited pack.cells.state back to Azgaar state
// Regenerate PROVINCES only (depends on STATES)
generatePartial([PHASES.PROVINCES]);  // Uses cached/edited STATES
// DualGridManager updates province borders
```

**Benefits:**
- **Respects user edits**: Manual border changes preserved
- **Fast province recalculation**: Only PROVINCES phase runs (~1-3s)
- **No terrain disruption**: Voronoi, heightmap, biomes untouched

#### 3. Surgical Dual Grid Recalculation

**Scenario:** User wants to recalculate state borders after changing `culturesNumber` (affects state generation).

**Iteration 2 Flow:**
```javascript
// Cache existing VORONOI, HEIGHTMAP, PACK_CREATION, BIOMES
// Update culturesNumber
// Regenerate CULTURES → BURGS → STATES (dependency chain)
generatePartial([PHASES.CULTURES, PHASES.BURGS, PHASES.STATES]);
// DualGridManager re-initializes with new state assignments
```

**Benefits:**
- **Targeted updates**: Only political layers regenerate
- **Dependency awareness**: Automatically includes required phases (BURGS for STATES)
- **Fast iteration**: 5-10s vs 45s for full regeneration

#### 4. Phase-Specific Seed Consistency

**Scenario:** User wants to regenerate STATES with different parameters but keep same Voronoi structure.

**Iteration 2 Flow:**
```javascript
// First generation: Full map with seed "12345"
generateMap({ seed: "12345", statesNumber: 18 });

// Later: Regenerate STATES only with different parameters, same Voronoi
generatePartial([PHASES.STATES], { statesNumber: 25 });  
// Uses cached VORONOI (from seed "12345"), new STATE seed (hash("12345" + "STATES"))
```

**Benefits:**
- **Terrain consistency**: Same Voronoi structure (same seed)
- **Parameter flexibility**: Can change state parameters independently
- **Reproducibility**: Can reproduce exact state layout with same seed

---

## Benefits for World-Building Workflow & UX

### Current World Builder Limitations

The `WorldBuilderWebController.gd` and `world_builder.html` currently:

1. **Full generation on every change**: Parameter tweaks trigger complete regeneration
2. **No phase locking**: Cannot lock terrain while tweaking politics
3. **Slow iteration**: 30-60s wait for each parameter change
4. **No incremental preview**: Must wait for full generation to see results

### How Iteration 2 Improves World-Building UX

#### 1. Targeted Fast Re-Generation

**Workflow:** User adjusts `culturesInput` slider → Only CULTURES/BURGS/STATES regenerate.

**Implementation:**
```javascript
// In world_builder.js (Alpine.js)
async function handleCultureChange(newValue) {
  // Lock terrain phases
  const lockedPhases = [
    PHASES.VORONOI, 
    PHASES.HEIGHTMAP, 
    PHASES.PACK_CREATION, 
    PHASES.BIOMES
  ];
  
  // Update options
  window.AzgaarGenesis.loadOptions({ cultures: newValue });
  
  // Regenerate only political phases
  const result = await window.AzgaarGenesis.generatePartial([
    PHASES.CULTURES,
    PHASES.BURGS,
    PHASES.STATES,
    PHASES.PROVINCES
  ]);
  
  // Update preview (SVG re-render with new state borders)
  updatePreview(result);
}
```

**Benefits:**
- **Instant feedback**: 5-10s vs 45s for culture changes
- **Terrain preserved**: Heightmap, biomes, rivers unchanged
- **Smooth UX**: Slider adjustments feel responsive

#### 2. Live Preview with Incremental Updates

**Workflow:** User tweaks `statesNumber` → Live preview updates state borders in real-time.

**Implementation:**
```javascript
// In world_builder.js
let terrainLocked = false;
let cachedTerrainPhases = [];

function lockTerrain() {
  terrainLocked = true;
  cachedTerrainPhases = [
    PHASES.VORONOI,
    PHASES.HEIGHTMAP,
    PHASES.PACK_CREATION,
    PHASES.BIOMES,
    PHASES.RIVERS
  ];
  // Cache these phases (already generated)
}

async function onStatesNumberChange(newValue) {
  if (terrainLocked) {
    // Fast regeneration: only STATES
    const result = await window.AzgaarGenesis.generatePartial([PHASES.STATES], {
      statesNumber: newValue
    });
    // Update SVG preview with new borders
    updateStateBorders(result.pack.cells.state);
  } else {
    // Full generation (first time)
    await window.AzgaarGenesis.generateMap();
  }
}
```

**Benefits:**
- **Interactive tweaking**: Real-time border updates as slider moves
- **Terrain lock toggle**: User can lock/unlock terrain as needed
- **Fast iteration**: Multiple parameter tweaks in seconds

#### 3. Phase Group Buttons in Alpine UI

**Workflow:** User clicks "Regenerate Politics" button → Only political phases run.

**Implementation:**
```html
<!-- In world_builder.html -->
<div class="phase-controls">
  <button @click="regenerateTerrain()">Regenerate Terrain</button>
  <button @click="regeneratePolitics()">Regenerate Politics</button>
  <button @click="regenerateCultures()">Regenerate Cultures</button>
  <button @click="lockTerrain()">Lock Terrain</button>
</div>
```

```javascript
// In world_builder.js
function regenerateTerrain() {
  return window.AzgaarGenesis.generatePartial([
    PHASES.VORONOI,
    PHASES.HEIGHTMAP,
    PHASES.PACK_CREATION,
    PHASES.BIOMES,
    PHASES.RIVERS
  ]);
}

function regeneratePolitics() {
  return window.AzgaarGenesis.generatePartial([
    PHASES.CULTURES,
    PHASES.BURGS,
    PHASES.STATES,
    PHASES.PROVINCES,
    PHASES.RELIGIONS
  ]);
}
```

**Benefits:**
- **User control**: Explicit phase group selection
- **Fast targeted updates**: Only relevant phases regenerate
- **Clear workflow**: User understands what's being regenerated

#### 4. Export JSON to Terrain3D with Incremental Updates

**Workflow:** User locks terrain, tweaks states → Exports updated JSON to Terrain3D without full heightmap regeneration.

**Implementation:**
```gdscript
# In WorldBuilderWebController.gd
func _handle_partial_generation_complete(data: Dictionary) -> void:
    var map_data: Dictionary = data.get("data", {})
    
    # Check if terrain phases were skipped (incremental update)
    var is_incremental: bool = data.get("incremental", false)
    
    if is_incremental:
        # Only update political/cultural data, preserve terrain
        var dual_grid_manager: DualGridManager = DualGridManager.new()
        dual_grid_manager.initialize_from_azgaar(map_data)
        
        # Update state borders in 3D world (without regenerating terrain)
        _update_state_borders_3d(dual_grid_manager)
    else:
        # Full regeneration: convert heightmap to Terrain3D
        var converter: AzgaarDataConverter = AzgaarDataConverter.new()
        var heightmap_img: Image = converter.convert_to_heightmap(map_data)
        Terrain3DManager.generate_from_heightmap(heightmap_img)
```

**Benefits:**
- **Fast 3D updates**: State border changes reflected in 3D without terrain rebuild
- **Preserved terrain**: Heightmap, biomes, rivers unchanged in Terrain3D
- **Efficient workflow**: Iterate on politics without terrain disruption

---

## Usage Examples & Pseudocode

### Example 1: Incremental STATE Regeneration (GDScript → JS)

**GDScript Side (WorldBuilderWebController.gd):**
```gdscript
func regenerate_states_only(new_states_number: int) -> void:
    """Regenerate only STATES phase without touching terrain."""
    if not web_view:
        return
    
    var script: String = """
        (async function() {
            try {
                // Lock terrain: skip all terrain phases
                const lockedPhases = [
                    window.AzgaarGenesis.PHASES.VORONOI,
                    window.AzgaarGenesis.PHASES.HEIGHTMAP,
                    window.AzgaarGenesis.PHASES.PACK_CREATION,
                    window.AzgaarGenesis.PHASES.BIOMES,
                    window.AzgaarGenesis.PHASES.RIVERS
                ];
                
                // Update options
                window.AzgaarGenesis.loadOptions({
                    statesNumber: %d
                });
                
                // Regenerate only STATES (and dependencies: CULTURES, BURGS)
                const result = await window.AzgaarGenesis.generatePartial([
                    window.AzgaarGenesis.PHASES.CULTURES,
                    window.AzgaarGenesis.PHASES.BURGS,
                    window.AzgaarGenesis.PHASES.STATES
                ]);
                
                // Send updated data to Godot
                if (window.GodotBridge && window.GodotBridge.postMessage) {
                    window.GodotBridge.postMessage('partial_generation_complete', {
                        data: result,
                        incremental: true,
                        phases_run: ['CULTURES', 'BURGS', 'STATES']
                    });
                }
                
                return 'success';
            } catch (error) {
                console.error('[Partial Generation] Error:', error);
                if (window.GodotBridge && window.GodotBridge.postMessage) {
                    window.GodotBridge.postMessage('partial_generation_failed', {
                        error: error.message
                    });
                }
                return 'error: ' + error.message;
            }
        })();
    """ % new_states_number
    
    web_view.execute_js(script)
```

**JavaScript Side (world_builder.js):**
```javascript
// Alpine.js component method
async regenerateStatesOnly(newStatesNumber) {
    this.isGenerating = true;
    this.statusText = 'Regenerating states...';
    
    try {
        // Update options
        window.AzgaarGenesis.loadOptions({
            statesNumber: newStatesNumber
        });
        
        // Regenerate only STATES phase
        const result = await window.AzgaarGenesis.generatePartial([
            window.AzgaarGenesis.PHASES.STATES
        ]);
        
        // Update preview with new state borders
        this.updateStateBorders(result.pack.cells.state);
        
        // Notify Godot
        if (window.GodotBridge) {
            window.GodotBridge.postMessage('partial_generation_complete', {
                data: result,
                incremental: true
            });
        }
        
        this.isGenerating = false;
        this.statusText = 'States regenerated!';
    } catch (error) {
        console.error('State regeneration failed:', error);
        this.isGenerating = false;
        this.statusText = 'Error: ' + error.message;
    }
}
```

### Example 2: Cache Restoration for Fast Terrain Lock

**GDScript Side:**
```gdscript
func lock_terrain_and_regenerate_politics() -> void:
    """Lock terrain phases in cache, then regenerate only politics."""
    var script: String = """
        (async function() {
            try {
                // Ensure terrain phases are cached (from previous full generation)
                const terrainPhases = [
                    window.AzgaarGenesis.PHASES.VORONOI,
                    window.AzgaarGenesis.PHASES.HEIGHTMAP,
                    window.AzgaarGenesis.PHASES.PACK_CREATION,
                    window.AzgaarGenesis.PHASES.BIOMES
                ];
                
                // Check cache availability
                const state = window.AzgaarGenesis.getState();
                const cached = state.cached || {};
                
                const missingPhases = terrainPhases.filter(phase => !cached[phase]);
                if (missingPhases.length > 0) {
                    throw new Error('Terrain phases not cached: ' + missingPhases.join(', '));
                }
                
                // Regenerate only political phases (will use cached terrain)
                const result = await window.AzgaarGenesis.generatePartial([
                    window.AzgaarGenesis.PHASES.CULTURES,
                    window.AzgaarGenesis.PHASES.BURGS,
                    window.AzgaarGenesis.PHASES.STATES,
                    window.AzgaarGenesis.PHASES.PROVINCES
                ]);
                
                // Send to Godot
                if (window.GodotBridge && window.GodotBridge.postMessage) {
                    window.GodotBridge.postMessage('partial_generation_complete', {
                        data: result,
                        incremental: true,
                        cached_phases: terrainPhases
                    });
                }
                
                return 'success';
            } catch (error) {
                console.error('[Terrain Lock] Error:', error);
                return 'error: ' + error.message;
            }
        })();
    """
    
    web_view.execute_js(script)
```

### Example 3: DualGridManager Integration with Partial Updates

**GDScript Side (DualGridManager.gd):**
```gdscript
func update_from_partial_generation(azgaar_data: Dictionary, phases_run: Array) -> void:
    """Update dual grid from partial generation (only relevant phases)."""
    # Check if STATES phase was run
    if "STATES" in phases_run:
        # Re-extract state data only
        var pack_data: Dictionary = azgaar_data.get("pack", {})
        var pack_cells: Dictionary = pack_data.get("cells", {})
        var cell_states: Array = pack_cells.get("state", [])
        
        if not cell_states.is_empty():
            # Update only state borders (preserve existing grid structure)
            primary_grid["cell_states"] = cell_states
            _build_dual_grid(
                cell_states, 
                primary_grid.get("cell_neighbors", []), 
                primary_grid.get("points", [])
            )
            
            MythosLogger.info("DualGridManager", "Updated state borders from partial generation", {
                "phases_run": phases_run,
                "states_count": state_borders.size()
            })
    
    # Check if PROVINCES phase was run
    if "PROVINCES" in phases_run:
        # Update province borders (if implemented)
        # Similar logic for provinces
        pass
```

### Example 4: Phase Group UI Controls

**HTML Side (world_builder.html):**
```html
<div class="phase-control-panel" x-show="!isGenerating">
    <h3>Phase Controls</h3>
    
    <div class="phase-group">
        <label>Terrain:</label>
        <button @click="regenerateTerrain()">Regenerate Terrain</button>
        <button @click="lockTerrain()">Lock Terrain</button>
    </div>
    
    <div class="phase-group">
        <label>Politics:</label>
        <button @click="regeneratePolitics()">Regenerate Politics</button>
        <button @click="regenerateStatesOnly()">States Only</button>
    </div>
    
    <div class="phase-group">
        <label>Culture:</label>
        <button @click="regenerateCultures()">Regenerate Cultures</button>
    </div>
</div>
```

**JavaScript Side (world_builder.js):**
```javascript
// Alpine.js methods
async regenerateTerrain() {
    this.isGenerating = true;
    this.statusText = 'Regenerating terrain...';
    
    try {
        const result = await window.AzgaarGenesis.generatePartial([
            window.AzgaarGenesis.PHASES.VORONOI,
            window.AzgaarGenesis.PHASES.HEIGHTMAP,
            window.AzgaarGenesis.PHASES.PACK_CREATION,
            window.AzgaarGenesis.PHASES.BIOMES,
            window.AzgaarGenesis.PHASES.RIVERS
        ]);
        
        this.updatePreview(result);
        this.isGenerating = false;
    } catch (error) {
        console.error('Terrain regeneration failed:', error);
        this.isGenerating = false;
    }
}

async regeneratePolitics() {
    this.isGenerating = true;
    this.statusText = 'Regenerating politics...';
    
    try {
        const result = await window.AzgaarGenesis.generatePartial([
            window.AzgaarGenesis.PHASES.CULTURES,
            window.AzgaarGenesis.PHASES.BURGS,
            window.AzgaarGenesis.PHASES.STATES,
            window.AzgaarGenesis.PHASES.PROVINCES,
            window.AzgaarGenesis.PHASES.RELIGIONS
        ]);
        
        this.updatePreview(result);
        this.isGenerating = false;
    } catch (error) {
        console.error('Politics regeneration failed:', error);
        this.isGenerating = false;
    }
}
```

---

## Prioritized Recommendations

### Priority 1: Expose Phase Group Buttons in Alpine UI (High Impact, Low Effort)

**What:** Add phase group control buttons to `world_builder.html` (Terrain, Politics, Culture groups).

**Why:** Immediate UX improvement, enables user-driven phase selection.

**Implementation:**
1. Add phase control panel to `world_builder.html`
2. Implement `regenerateTerrain()`, `regeneratePolitics()`, `regenerateCultures()` in `world_builder.js`
3. Wire up IPC messages to `WorldBuilderWebController.gd`

**Estimated Effort:** 2-4 hours

**Impact:** High - Users can lock terrain and iterate on politics quickly

---

### Priority 2: Add Incremental Recalc Hooks in DualGridManager (High Impact, Medium Effort)

**What:** Add `update_from_partial_generation()` method to `DualGridManager.gd` that only updates relevant borders.

**Why:** Enables fast dual grid updates without full re-initialization.

**Implementation:**
1. Add `update_from_partial_generation(azgaar_data: Dictionary, phases_run: Array)` method
2. Check `phases_run` array to determine which borders to update
3. Only rebuild `state_borders` if STATES phase was run
4. Preserve existing grid structure (points, neighbors) if terrain phases skipped

**Estimated Effort:** 4-6 hours

**Impact:** High - 10-20x faster border updates

---

### Priority 3: Implement Terrain Lock Toggle (Medium Impact, Low Effort)

**What:** Add "Lock Terrain" checkbox/toggle in UI that caches terrain phases and skips them in subsequent generations.

**Why:** User-friendly way to preserve terrain while tweaking politics.

**Implementation:**
1. Add `terrainLocked` boolean to Alpine.js component
2. On lock: Cache terrain phases (VORONOI, HEIGHTMAP, PACK_CREATION, BIOMES, RIVERS)
3. On generation: If locked, automatically skip terrain phases
4. Visual indicator in UI (lock icon, disabled terrain sliders)

**Estimated Effort:** 3-5 hours

**Impact:** Medium - Improves UX for iterative world-building

---

### Priority 4: Add Phase-Specific Progress Indicators (Medium Impact, Low Effort)

**What:** Show which phases are running during partial generation (e.g., "Regenerating STATES...").

**Why:** Better user feedback during fast partial generations.

**Implementation:**
1. Modify `generatePartial()` to emit phase start/complete events
2. Update `WorldBuilderWebController.gd` to send phase progress via IPC
3. Display phase name in `world_builder.html` status text

**Estimated Effort:** 2-3 hours

**Impact:** Medium - Better UX feedback

---

### Priority 5: Cache Management UI (Low Impact, Medium Effort)

**What:** Add UI to view/manage cached phases (show cache size, clear cache, set `maxCachedPhases`).

**Why:** Advanced users can optimize memory usage and cache behavior.

**Implementation:**
1. Add cache status display (cached phases, cache size)
2. Add "Clear Cache" button
3. Add `maxCachedPhases` slider in settings

**Estimated Effort:** 4-6 hours

**Impact:** Low - Nice-to-have for power users

---

### Priority 6: Export Partial Updates to Terrain3D (High Impact, High Effort)

**What:** When partial generation completes, update only relevant 3D elements (state borders, burgs) without regenerating terrain.

**Why:** Fast 3D world updates without terrain disruption.

**Implementation:**
1. Modify `WorldBuilderWebController._handle_partial_generation_complete()` to check `phases_run`
2. If terrain phases skipped: Update only political/cultural 3D elements
3. If terrain phases included: Full Terrain3D regeneration
4. Add `_update_state_borders_3d()` method to update border meshes only

**Estimated Effort:** 8-12 hours

**Impact:** High - Enables fast 3D world iteration

---

### Priority 7: Dependency Auto-Resolution (Medium Impact, Medium Effort)

**What:** Automatically include required dependencies when user selects phases (e.g., selecting STATES auto-includes CULTURES, BURGS).

**Why:** Prevents dependency errors, simplifies user workflow.

**Implementation:**
1. Add `resolvePhaseDependencies(phasesToRun)` helper in `world_builder.js`
2. Use `PHASE_DEPENDENCIES` graph to auto-include required phases
3. Show auto-included phases in UI (grayed out, with tooltip)

**Estimated Effort:** 4-6 hours

**Impact:** Medium - Prevents user errors

---

### Priority 8: Phase-Specific Seed Override (Low Impact, Low Effort)

**What:** Allow users to override phase-specific seeds for fine-grained control.

**Why:** Advanced users can tweak individual phase randomness.

**Implementation:**
1. Add `phaseSeeds` option to Azgaar options (e.g., `phaseSeeds: { STATES: "custom_seed" }`)
2. Modify `getPhaseSeed()` to check for override
3. Add UI controls in advanced settings panel

**Estimated Effort:** 3-4 hours

**Impact:** Low - Advanced feature for power users

---

## Remaining Risks & Mitigations

### Risk 1: Cache Size Growth

**Risk:** Unbounded cache growth if `maxCachedPhases` not set or too high.

**Mitigation:**
- ✅ Already implemented: `manageCacheSize()` with FIFO eviction
- ✅ Default `maxCachedPhases: 8` prevents unbounded growth
- ⚠️ **Recommendation:** Add UI warning when cache approaches limit (e.g., "Cache at 7/8 phases")

**Severity:** Low (already mitigated)

---

### Risk 2: Dependency Errors

**Risk:** User selects phases without required dependencies, causing `DependencyError`.

**Mitigation:**
- ✅ Already implemented: `validatePhaseDependencies()` with clear error messages
- ⚠️ **Recommendation:** Implement Priority 7 (Dependency Auto-Resolution) to prevent errors

**Severity:** Medium (mitigated by validation, can be improved with auto-resolution)

---

### Risk 3: Cache Corruption

**Risk:** Cached data becomes invalid if options change (e.g., `mapWidth` changes invalidates VORONOI cache).

**Mitigation:**
- ⚠️ **Recommendation:** Add cache invalidation on option changes (e.g., if `mapWidth` changes, clear VORONOI cache)
- ⚠️ **Recommendation:** Add cache versioning (cache key includes relevant option hash)

**Severity:** Medium (requires implementation)

---

### Risk 4: Performance Degradation with Many Phases

**Risk:** Running many phases in `generatePartial()` may still be slow if dependencies are deep.

**Mitigation:**
- ✅ Already optimized: Each phase only runs if not skipped and dependencies met
- ⚠️ **Recommendation:** Profile phase execution times, optimize slow phases (e.g., RANK_CELLS)

**Severity:** Low (already optimized, can be improved with profiling)

---

### Risk 5: Memory Leaks from Typed Arrays

**Risk:** Typed arrays in cache may not be garbage collected properly.

**Mitigation:**
- ✅ Already handled: `efficientDeepCopyOfRelevantData()` uses `structuredClone()` or safe fallback
- ⚠️ **Recommendation:** Add memory profiling in development mode, monitor cache size

**Severity:** Low (already handled, monitor in production)

---

## Next Steps for Integration

### Phase 1: Foundation (Week 1)

1. **Update Azgaar Fork Bundle**
   - Ensure latest Iteration 2 bundle is in `res://assets/ui_web/js/azgaar/azgaar-genesis.esm.js`
   - Verify `generatePartial()`, `PHASES`, `skipPhases` are available

2. **Add Phase Constants Export**
   - Ensure `PHASES` constant is exported from fork bundle
   - Add `window.AzgaarGenesis.PHASES` global for Alpine.js access

3. **Test Basic Partial Generation**
   - Create test script to verify `generatePartial([PHASES.STATES])` works
   - Verify cache restoration works correctly

**Deliverable:** Working `generatePartial()` API accessible from GDScript/JS

---

### Phase 2: UI Integration (Week 2)

1. **Add Phase Group Buttons** (Priority 1)
   - Implement phase control panel in `world_builder.html`
   - Wire up `regenerateTerrain()`, `regeneratePolitics()` in `world_builder.js`

2. **Add Terrain Lock Toggle** (Priority 3)
   - Implement `terrainLocked` state in Alpine.js
   - Auto-skip terrain phases when locked

3. **Add Phase Progress Indicators** (Priority 4)
   - Show phase name in status text during partial generation

**Deliverable:** User-facing phase controls in World Builder UI

---

### Phase 3: Dual Grid Integration (Week 3)

1. **Add Incremental Recalc Hooks** (Priority 2)
   - Implement `update_from_partial_generation()` in `DualGridManager.gd`
   - Test state border updates from partial generation

2. **Update WorldBuilderWebController**
   - Add `_handle_partial_generation_complete()` IPC handler
   - Pass `phases_run` array to `DualGridManager`

**Deliverable:** Fast dual grid updates from partial generation

---

### Phase 4: Advanced Features (Week 4+)

1. **Export Partial Updates to Terrain3D** (Priority 6)
   - Implement `_update_state_borders_3d()` method
   - Update only relevant 3D elements without terrain regeneration

2. **Dependency Auto-Resolution** (Priority 7)
   - Implement `resolvePhaseDependencies()` helper
   - Auto-include required phases in UI

3. **Cache Management UI** (Priority 5)
   - Add cache status display
   - Add cache controls (clear, set max)

**Deliverable:** Complete integration with advanced features

---

## Conclusion

The Azgaar Genesis Fork Iteration 2 improvements provide a **powerful foundation** for dramatically improving both the dual grid system and world-building UX in Genesis Mythos. By leveraging phase-based modularity, intelligent caching, and surgical regeneration, we can achieve:

- **10-20x faster** state border updates (2-5s vs 45s)
- **Interactive parameter tweaking** with live preview feedback
- **Terrain preservation** during political/cultural iteration
- **Targeted phase execution** for specific dual grid operations

The recommended integration path prioritizes **high-impact, low-effort** features first (phase group buttons, incremental recalc hooks) followed by advanced features (Terrain3D partial updates, dependency auto-resolution). With proper risk mitigation (cache management, dependency validation), this integration will significantly enhance the world-building experience while maintaining system stability and performance.

---

**Report Generated:** 2026-01-09  
**Author:** AI Assistant (Auto)  
**Status:** Ready for Implementation Review

