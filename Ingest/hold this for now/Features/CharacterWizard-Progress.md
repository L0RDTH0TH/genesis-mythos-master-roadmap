---
proposal_path: Ingest/Decisions/Decision-for-characterwizard-progress--2026-03-04-0441.md
---
# Character Creation Wizard - Progress Tracker

## Current State

### Completed Steps
1. **Archetype Family** - Working ✓
2. **Archetype** - Working ✓
3. **Class** - Working ✓
4. **Subclass** - Working ✓
5. **Race** - Working ✓
6. **Subrace** - Working ✓
7. **Stats** - Working ✓ (point-buy system)
8. **Equipment** - Working ✓ (weapon & armor selection)
9. **Appearance** - PARTIAL ✓ (only height implemented)
10. **Summary** - Working ✓ (save character)

### Current Issue

**APPEARANCE Step** has a navigation problem:
- Height adjustment works (can adjust +/-)
- But no way to confirm/done and proceed to SUMMARY
- Confirm button is hidden/disabled for APPEARANCE step (line 963-965)
- User gets stuck after adjusting height

### Root Cause

In `_build_appearance_step()` at lines 963-965:
```gdscript
# Confirm button only shown on STATS step
confirm_button.visible = false
confirm_button.disabled = true
```

This explicitly hides the confirm button for the APPEARANCE step, even though the confirm handler at lines 350-355 expects to be called:

```gdscript
WizardStep.APPEARANCE:
    # Persist appearance settings (height, etc.)
    var cdm_a = _cdm()
    if cdm_a != null:
        cdm_a.active_character["height"] = current_height_cm
    current_step = WizardStep.SUMMARY
```

## Next Steps

### Option 1: Enable Confirm Button (Recommended)
Add a condition to show the confirm button on APPEARANCE step:
- Similar to how STATS step works
- User clicks confirm when done with height/appearance
- Proceeds to SUMMARY

### Option 2: Auto-Advance
- Automatically proceed after adjusting height
- Less user control but smoother flow

### Option 3: ESC Navigation
- Add explicit "Done" option to the appearance menu
- Or rely on ESC to proceed (needs investigation)

## Recommended Fix

Enable confirm button on APPEARANCE step by modifying `_build_appearance_step()`:

```gdscript
func _build_appearance_step() -> void:
    # ... existing code ...
    
    # Show confirm button for appearance step
    confirm_button.visible = true
    confirm_button.disabled = false
    confirm_button.text = "Confirm Appearance"
```

This would allow the user to:
1. Adjust height with +/-
2. Click "Confirm" to proceed
3. Save height to character and go to SUMMARY

## Related TODO
Line 950 in CharacterCreator.gd:
```gdscript
# TODO: Add more appearance options here (hair color, eye color, skin tone, etc.)
```


## Update - 2025-10-31

### Fixed
✅ Enabled confirm button on APPEARANCE step
- Added `confirm_button.text = "Confirm Appearance"`
- Set `confirm_button.visible = true` and `confirm_button.disabled = false`
- User can now proceed from APPEARANCE to SUMMARY

### Change Made
Modified `_build_appearance_step()` at lines 963-966 to show the confirm button instead of hiding it.

## Review Needed
Proposed para-type: archive. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.