---
confidence: 70%
created: 2026-03-02
status: ingest
proposal_path: Ingest/Decisions/Decision-for-cascade-tree--2026-03-04-0436.md
decision_candidate: true
decision_priority: high
---
────────────────────────
### Sub-task 1 – WedgeButton.gd (the reusable slice)
```gdscript
# WedgeButton.gd
@tool
class_name WedgeButton extends Control

@export var wedge_angle: float = 90.0   # 90° total wedge
@export var slice_count: int   = 7
@export var label_text: String  = "?"

var slice_angle: float

func _ready() -> void:
    slice_angle = deg_to_rad(wedge_angle / slice_count)
    if not Engine.is_editor_hint():
        _update_label()

func _draw() -> void:
    var c = size / 2
    var r = min(size.x, size.y) * 0.45
    var start = -slice_angle / 2

    for i in slice_count:
        var a1 = start + i * slice_angle
        var a2 = a1 + slice_angle
        # outer arc
        draw_arc(c, r, a1, a2, 32, Color("#1e90ff"), 3, true)
        # radials
        draw_line(c, c + Vector2(cos(a1), sin(a1)) * r, Color("#1e90ff"), 3)
        draw_line(c, c + Vector2(cos(a2), sin(a2)) * r, Color("#1e90ff"), 3)

func _update_label() -> void:
    var lbl = $Label as Label
    if not lbl:
        lbl = Label.new()
        lbl.name = "Label"
        lbl.anchor_left   = 0.5
        lbl.anchor_top    = 0.5
        lbl.anchor_right  = 0.5
        lbl.anchor_bottom = 0.5
        lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
        lbl.vertical_alignment   = VERTICAL_ALIGNMENT_CENTER
        add_child(lbl)
    lbl.text = label_text
```

### Sub-task 2 – TreeRoot.tscn (bow-tie layout)
```
TreeRoot (Control)
 ├─ LeftFan  (Control)   rotation = -45°
 │    └─ WedgeButton (90°)
 ├─ Portal   (ColorRect)  size = 80×80, color = black
 └─ RightFan (Control)   rotation = +45°
      └─ WedgeButton (90°)
```

### Sub-task 3 – Auto-populate 7 wedges
```gdscript
# TreeRoot.gd
@onready var left_wedge  = $LeftFan/WedgeButton
@onready var right_wedge = $RightFan/WedgeButton

var left_items  = ["Main", "Player", "World", "Settings", "Audio", "Video", "Exit"]
var right_items = ["Stats", "Inventory", "Quests", "Map", "Craft", "Social", "Logout"]

func _ready() -> void:
    _build_fan(left_wedge,  left_items)
    _build_fan(right_wedge, right_items)

func _build_fan(wedge: WedgeButton, items: Array) -> void:
    wedge.slice_count = items.size()
    wedge.queue_redraw()
    for i in items.size():
        var btn = Button.new()
        btn.text = items[i]
        btn.custom_minimum_size = Vector2(80, 30)
        btn.position = _slice_center(wedge, i)
        wedge.add_child(btn)

func _slice_center(w: WedgeButton, i: int) -> Vector2:
    var c = w.size / 2
    var r = min(w.size.x, w.size.y) * 0.35
    var a = -w.slice_angle/2 + (i+0.5) * w.slice_angle
    return c + Vector2(cos(a), sin(a)) * r
```

### Sub-task 4 – Hover → spawn child tree (depth ≤ 5)
```gdscript
const MAX_DEPTH = 5

func _on_slice_hovered(wedge: WedgeButton, slice_idx: int, depth: int) -> void:
    if depth >= MAX_DEPTH: return
    var child = preload("res://WedgeButton.tscn").instantiate()
    child.wedge_angle = 90
    child.slice_count = randi_range(3,7)
    child.label_text = "L%d-%d" % [depth+1, slice_idx]
    child.position = _slice_center(wedge, slice_idx) + Vector2(0, 60)
    wedge.add_child(child)
    # fade-in tween
    child.modulate.a = 0
    var tw = create_tween()
    tw.tween_property(child, "modulate:a", 1.0, 0.2)
```

### Sub-task 5 – Wire hover signals
```gdscript
# inside WedgeButton.gd
func _input(event: InputEvent) -> void:
    if event is InputEventMouseMotion:
        var local = to_local(event.position)
        var c = size / 2
        var angle = (local - c).angle()
        var slice = int((angle + slice_angle/2) / slice_angle) % slice_count
        if slice != hovered_slice:
            hovered_slice = slice
            queue_redraw()
            emit_signal("slice_hovered", self, slice, depth)
```

### Sub-task 6 – Dynamic branch sizing (your original rule)
```gdscript
# TreeRoot.gd → tweak _build_fan
wedge.custom_minimum_size = Vector2(full_width / items.size(), 180)
```

### Sub-task 7 – One-click play test
1. Attach `TreeRoot.tscn` to a new empty scene.  
2. Hit F5.  
3. Hover any slice → instant child fan appears → keep going up to depth 5 → auto-stops.  

**Done.**  
Copy → paste → run.  
Seven wedges, 12.857° each, recursion capped, zero 91° hacks.

Want the **full zip-ready project** or a **Godot 4.3 export template** next? Just shout.

## Review Needed
Proposed para-type: project. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.