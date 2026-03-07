---
proposal_path: Ingest/Decisions/Decision-for-menu-structure-map--2026-03-04-0441.md
---
# Menu Structure Map

## Overview
This document describes the complete hierarchical menu structure for the Mythos Gen fractal wheel GUI system.

## Color Coding Scheme
- **Red (#ff0000)** - Player options
- **Orange (#ff8800)** - Modifications
- **Green (#00ff00)** - Settings
- **Purple (#8800ff)** - Dungeon Master options
- **Blue (#0000ff)** - Exit

## Menu Hierarchy

### Main Menu (Root Level)
The main menu displays 5 segments arranged radially:

| Segment | Label | Color | Position | Type | Children |
|---------|-------|-------|----------|------|----------|
| 0 | Player | Red | Top Middle | Navigation | 2 |
| 1 | Mods | Orange | Top Right | Action (Leaf) | 0 |
| 2 | Settings | Green | Right Middle | Action (Leaf) | 0 |
| 3 | DM | Purple | Left Middle | Navigation | 4 |
| 4 | Exit | Blue | Bottom Middle | Action (Leaf) | 0 |

### Player Submenu
Accessed by clicking **Player** on the main menu.

| Segment | Label | Color | Type | Children |
|---------|-------|-------|------|----------|
| 0 | New Character | Light Red (#ff6666) | Navigation | 4 |
| 1 | Edit Character | Light Red (#ff6666) | Action (Leaf) | 0 |

### New Character Submenu (Archetypes)
Accessed by clicking **New Character** in the Player submenu.

| Segment | Label | Color | Type | Description |
|---------|-------|-------|------|-------------|
| 0 | Identity and Self | Lighter Red (#ff8888) | Action (Leaf) | Character archetype selection |
| 1 | Transformation and Balance | Lighter Red (#ffaaaa) | Action (Leaf) | Character archetype selection |
| 2 | Guidance and Authority | Lighter Red (#ffcccc) | Action (Leaf) | Character archetype selection |
| 3 | Rebellion and Change | Lightest Red (#ffeeee) | Action (Leaf) | Character archetype selection |

### DM Submenu
Accessed by clicking **DM** on the main menu.

| Segment | Label | Color | Type | Description |
|---------|-------|-------|------|-------------|
| 0 | New World | Light Purple (#aa66ff) | Action (Leaf) | Create a new world |
| 1 | Edit World | Light Purple (#aa66ff) | Action (Leaf) | Modify existing world |
| 2 | Session Preparation | Light Purple (#aa66ff) | Action (Leaf) | Prepare for game session |
| 3 | Launch Game | Light Purple (#aa66ff) | Action (Leaf) | Start the game |

## Navigation Behavior

### Navigation Nodes vs. Action Nodes

**Navigation Nodes** (have children):
- Player
- New Character
- DM

**Action Nodes** (leaf nodes, no children):
- Mods
- Settings
- Exit
- Edit Character
- Identity and Self
- Transformation and Balance
- Guidance and Authority
- Rebellion and Change
- New World
- Edit World
- Session Preparation
- Launch Game

### User Interaction

1. **Clicking a Navigation Node**: Zooms into that node's children with an animated transition (0.3s duration)
2. **Clicking an Action Node**: Emits the `on_select` signal with the node data for action handling
3. **Pressing ESC**: Navigates back to the parent menu level

### Implementation Details

- **Data Source**: `resources/test_menu_data.json`
- **Main Controller**: `scripts/gui/FractalWheel.gd`
- **Segment Rendering**: `scripts/gui/WedgeSegment.gd`
- **Data Structure**: `scripts/gui/MenuNode.gd`

## Technical Notes

### Zoom Animation
The fractal zoom uses a tween animation system:
1. Fade out current menu (0.15s)
2. Scale down to 80%
3. Build new menu at midpoint
4. Scale up from 120%
5. Fade in new menu (0.15s)

### Data Loading
All menu data is loaded from JSON at startup via `MenuNode.load_from_json()`. The structure supports unlimited nesting depth.

### Future Expansion
- **Mods**: Will contain modification/plugin management options
- **Settings**: Will contain application configuration options
- Both are currently placeholder leaf nodes that can be expanded later

## Testing Status

✅ JSON parsing works correctly  
✅ Menu hierarchy loads with all children  
✅ Segments receive correct MenuNode data  
✅ Navigation logic correctly identifies leaf vs. navigation nodes  
✅ build_torus() correctly creates submenus  
⚠️  Tween animations need GUI testing (don't work in headless mode)

## See Also

- [[Fractal Wheel Architecture]]
- [[MenuNode Data Structure]]
- [[Session Preparation Flow]]

## Review Needed
Proposed para-type: resource. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.