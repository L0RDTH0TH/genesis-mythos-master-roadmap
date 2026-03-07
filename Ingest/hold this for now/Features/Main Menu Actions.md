---
tags: [feature, main-menu, implementation]
status: active
date: 2025-10-30
proposal_path: Ingest/Decisions/Decision-for-main-menu-actions--2026-03-04-0441.md
---
# Main Menu Actions

## Overview

The main menu provides 5 primary options, each triggering specific game actions when selected.

## Menu Structure

```
Main Menu
├─ Player (submenu)
│  ├─ New Character → Archetype selection
│  └─ Edit Character → Character editor (placeholder)
├─ Mods → Mod browser (placeholder)
├─ Settings → Settings menu (placeholder)
├─ DM (submenu)
│  ├─ New World → World creation (placeholder)
│  ├─ Edit World → World editor (placeholder)
│  ├─ Session Preparation → Session prep tools (placeholder)
│  └─ Launch Game → Game launcher (placeholder)
└─ Exit → Quit application ✅ IMPLEMENTED
```

## Implemented Actions

### Exit Button ✅

**Status**: Fully Implemented  
**File**: `scenes/Main.gd`  
**Function**: `_on_wheel_select(item)`

**Behavior**:
- Clicking the Exit segment immediately closes the application
- Uses `get_tree().quit()` for clean shutdown
- Console message: "→ Exiting game..." before quit

**Code**:
```gdscript
"Exit":
    print("  → Exiting game...")
    get_tree().quit()
```

**Testing**:
1. Launch the game
2. Navigate to the Exit segment (bottom of the wheel)
3. Click to select
4. Application should close immediately

## Placeholder Actions

The following menu items are set up with signal handlers but currently only print debug messages:

### Mods
- **Current**: Prints "→ Mods menu would open here"
- **Future**: Load mod browser/manager UI

### Settings
- **Current**: Prints "→ Settings menu would open here"
- **Future**: Open settings panel (audio, graphics, keybindings, etc.)

### Edit Character
- **Current**: Prints "→ Character editor would open here"
- **Future**: Load character sheet editor

### Edit World
- **Current**: Prints "→ World editor would open here"
- **Future**: Load world/campaign editor

### New World
- **Current**: Prints "→ DM action triggered: New World"
- **Future**: Start world creation wizard

### Session Preparation
- **Current**: Prints "→ DM action triggered: Session Preparation"
- **Future**: Load session prep tools (encounters, NPCs, etc.)

### Launch Game
- **Current**: Prints "→ DM action triggered: Launch Game"
- **Future**: Start game session with active world

## Implementation Pattern

All menu actions follow this pattern in `scenes/Main.gd`:

```gdscript
func _on_wheel_select(item):
    print("▶ Selected: ", item.label, " (leaf node)")
    
    match item.label:
        "MenuItem":
            print("  → Action description")
            # Action implementation here
```

### Adding New Actions

1. Ensure the menu item is a **leaf node** (empty children array in JSON)
2. Add a case to the match statement in `_on_wheel_select()`
3. Implement the action logic
4. Update this documentation

## Signal Flow

```
User clicks segment
    ↓
WedgeSegment emits segment_clicked
    ↓
FractalWheel._on_segment_clicked()
    ↓
Checks if leaf node
    ↓
FractalWheel emits on_select signal
    ↓
Main._on_wheel_select(item)
    ↓
Match statement routes to specific action
    ↓
Action executed
```

## Future Enhancements

- [ ] Implement Settings menu
- [ ] Implement Mods browser
- [ ] Connect Edit Character to character sheet system
- [ ] Connect DM tools to world/session management
- [ ] Add confirmation dialog for Exit (optional)
- [ ] Add keyboard shortcuts for common actions
- [ ] Implement "Are you sure?" for destructive actions

## Related Files

- `scenes/Main.gd` - Main menu action handlers
- `resources/test_menu_data.json` - Menu structure definition
- `scripts/gui/FractalWheel.gd` - Menu navigation system
- `scripts/gui/WedgeSegment.gd` - Individual segment component

---

**See Also:**
- [[Archetype Menu System]]
- [[Menu Structure Map]]
- [[Fractal Wheel System]]

## Review Needed
Proposed para-type: resource. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.