---
para-type: Archive
confidence: 70%
created: 2026-03-02
status: ingest
proposal_path: Ingest/Decisions/Decision-for-cascade-breadcrumb--2026-03-04-1021.md
decision_candidate: true
decision_priority: high
---
## TL;DR
────────────────────────

---

────────────────────────
### Sub-task 1 – BreadcrumbBar.tscn (one scene, zero fuss)
```
BreadcrumbBar (HBoxContainer)
 ├─ LeftSpacer (Control)    size_flags_horizontal = EXPAND
 ├─ Crumbs (HBoxContainer)  separation = 12
 └─ RightSpacer (Control)   size_flags_horizontal = EXPAND
```

### Sub-task 2 – CrumbButton.gd (click = time-travel)
```gdscript
# CrumbButton.gd
@tool
class_name CrumbButton extends Button

@export var level: int = 0
@export var title: String = "Root"

signal crumb_clicked(level: int)

func _ready() -> void:
    text = title
    connect("pressed", _on_pressed)

func _on_pressed() -> void:
    emit_signal("crumb_clicked", level)
```

### Sub-task 3 – BreadcrumbManager.gd (the brain)
```gdscript
# BreadcrumbManager.gd → attach to BreadcrumbBar
extends HBoxContainer

@onready var crumbs = $Crumbs
var history: Array[Dictionary] = [
    {title="Root", data=[]}
]

signal navigate_to(level: int)

func _ready() -> void:
    rebuild()

func add_crumb(title: String, data: Array) -> void:
    history.append({title=title, data=data})
    rebuild()

func rebuild() -> void:
    for child in crumbs.get_children():
        child.queue_free()
    for i in history.size():
        var btn = preload("res://CrumbButton.tscn").instantiate()
        btn.title = history[i].title
        btn.level = i
        btn.connect("crumb_clicked", _on_crumb_clicked)
        crumbs.add_child(btn)
        if i < history.size()-1:
            var arrow = Label.new()
            arrow.text = " ▸ "
            arrow.add_theme_color_override("font_color", Color.PURPLE)
            crumbs.add_child(arrow)

func _on_crumb_clicked(level: int) -> void:
    history.resize(level + 1)
    rebuild()
    emit_signal("navigate_to", level)
```

### Sub-task 4 – Wire to TreeRoot
```gdscript
# TreeRoot.gd
@onready var breadcrumb = $UI/BreadcrumbBar

func _ready() -> void:
    breadcrumb.navigate_to.connect(_on_navigate)

func _on_branch_selected(payload: Dictionary) -> void:
    var data = _load_branch_data(payload.text)
    breadcrumb.add_crumb(payload.text, data)
    _repopulate_from(data)

func _on_navigate(level: int) -> void:
    var target = breadcrumb.history[level]
    _repopulate_from(target.data)
```

### Sub-task 5 – Hover preview (peek without clicking)
```gdscript
# CrumbButton.gd → add
func _notification(what: int) -> void:
    if what == NOTIFICATION_MOUSE_ENTER:
        emit_signal("crumb_hovered", level)
    if what == NOTIFICATION_MOUSE_EXIT:
        get_tree().call_group("wedge", "_hide_branches_now")

func _ready() -> void:
    mouse_filter = MOUSE_FILTER_STOP
    connect("crumb_hovered", Callable(get_parent().get_parent(), "_on_crumb_hovered"))
```

```gdscript
# BreadcrumbManager.gd → add
func _on_crumb_hovered(level: int) -> void:
    var data = history[level].data
    get_tree().call_group("preview_wedge", "spawn", data, level)
```

### Sub-task 6 – Preview wedge (yellow ghost fan)
```gdscript
# In any WedgeButton → add group in _ready()
add_to_group("preview_wedge")

func spawn(data: Array, depth: int) -> void:
    _hide_branches_now()
    if depth >= 5: return
    $BranchContainer.spawn(data, depth)
    $BranchContainer.modulate = Color(1, 1, 0, 0.6)  # ghost yellow
```

### Sub-task 7 – One-click sanity test
1. Scene tree:  
   `Main → TreeRoot → UI → BreadcrumbBar`  
2. Play → click Player → New → Archetype  
3. Breadcrumb shows: **Root ▸ Player ▸ New ▸ Archetype**  
4. Hover any crumb → yellow ghost fan appears instantly  
5. Click any crumb → tree rewinds to that exact level

## Review Needed
Proposed para-type: archive. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.