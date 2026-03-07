---
created: 2026-03-02
status: ingest
proposal_path: Ingest/Decisions/Decision-for-cascade-portal--2026-03-04-0436.md
decision_candidate: true
decision_priority: high
---
### Sub-task 1 – PortalRoot.tscn (basic elliptical frame)
```
PortalRoot (Control)
 ├─ ViewportContainer (ViewportContainer)  stretch = true
 │    └─ PortalViewport (SubViewport)      size = Vector2i(800, 600), transparent_bg = true
 └─ Outline (ColorRect)                   color = Color.TRANSPARENT
```

```gdscript
# PortalRoot.gd
@export var aspect: float = 1.6  # ~50% horizontal, 100% vertical ratio

func _ready() -> void:
    size = get_viewport_rect().size * Vector2(0.5, 1.0) / aspect
    anchor_left = 0.5
    anchor_top = 0.5
    anchor_right = 0.5
    anchor_bottom = 0.5
    pivot_offset = size / 2
    $Outline.size = size
    $Outline.pivot_offset = size / 2
    $ViewportContainer.size = size
```

### Sub-task 2 – Green outline (_draw green ellipse)
```gdscript
# PortalRoot.gd → add
func _draw() -> void:
    var c = size / 2
    var rx = size.x / 2
    var ry = size.y / 2
    draw_ellipse(c, rx, ry, 64, Color.GREEN, 4.0)

func draw_ellipse(center: Vector2, rx: float, ry: float, segments: int, color: Color, width: float) -> void:
    var points: PackedVector2Array = []
    for i in segments + 1:
        var a = i * TAU / segments
        points.append(center + Vector2(cos(a) * rx, sin(a) * ry))
    draw_polyline(points, color, width, true)
```

### Sub-task 3 – Clip shader (discard outside oval)
```gdscript
# Create new ShaderMaterial → assign to $ViewportContainer.material
# Shader code (portal_clip.shader)
shader_type canvas_item;

uniform float aspect = 1.6;

void fragment() {
    vec2 uv = UV - 0.5;
    uv.x *= aspect;
    if (length(uv) > 0.5) discard;
    COLOR = texture(TEXTURE, UV);
}
```

```gdscript
# PortalRoot.gd → _ready()
var mat = ShaderMaterial.new()
mat.shader = preload("res://portal_clip.shader")
$ViewportContainer.material = mat
mat.set_shader_parameter("aspect", aspect)
```

### Sub-task 4 – Dynamic content signals
```gdscript
# PortalRoot.gd
signal update_content(mode: String, data: Variant)  # e.g., "2d_text", "Hello"

func clear_content() -> void:
    for child in $ViewportContainer/PortalViewport.get_children():
        child.queue_free()

func load_2d(data: String) -> void:
    var lbl = RichTextLabel.new()
    lbl.text = data
    lbl.fit_content = true
    lbl.size = $ViewportContainer/PortalViewport.size
    $ViewportContainer/PortalViewport.add_child(lbl)

func load_3d(scene_path: String) -> void:
    var scene = load(scene_path).instantiate()
    $ViewportContainer/PortalViewport.add_child(scene)
    # Auto-cam if needed
    var cam = Camera3D.new()
    cam.translate(Vector3(0, 0, 5))
    scene.add_child(cam)
    $ViewportContainer/PortalViewport.world_3d.camera = cam
```

### Sub-task 5 – Hover → preview update
```gdscript
# TreeRoot.gd → connect from WedgeButton
func _on_branch_hovered(branch: WedgeButton, depth: int) -> void:
    var preview_data = _get_preview_data(branch.label_text)
    $PortalRoot.update_content(preview_data.mode, preview_data.content)

# Example _get_preview_data()
func _get_preview_data(title: String) -> Dictionary:
    match title:
        "Player": return {mode="2d_text", content="Strength: 10\nAgility: 8"}
        "World":  return {mode="3d_scene", content="res://city_preview.tscn"}
    return {mode="2d_text", content="Loading..."}
```

### Sub-task 6 – Click → full update + input handling
```gdscript
# PortalRoot.gd → add rotation/zoom
var rotate_speed := 1.0
var zoom_speed := 0.1

func _input(event: InputEvent) -> void:
    if event is InputEventMouseMotion and Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
        var current = $ViewportContainer/PortalViewport.get_child(0)
        if current is Node3D:
            current.rotation.y += event.relative.x * rotate_speed * get_process_delta_time()
            current.rotation.x += event.relative.y * rotate_speed * get_process_delta_time()
    elif event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_WHEEL_UP:
        var cam = $ViewportContainer/PortalViewport.find_child("Camera3D")
        if cam: cam.translate(Vector3(0,0,-zoom_speed))
    elif event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
        var cam = $ViewportContainer/PortalViewport.find_child("Camera3D")
        if cam: cam.translate(Vector3(0,0,zoom_speed))
```

### Sub-task 7 – VTTRPG tie-in (archetype/city preview)
```gdscript
# TreeRoot.gd → expand _get_preview_data()
match title:
    "New Character > Archetype":
        return {mode="3d_scene", content="res://archetype_model.tscn"}
    "World > City":
        return {mode="3d_scene", content=_generate_city_preview()}

func _generate_city_preview() -> String:
    # Stub: procedural city
    var scene = PackedScene.new()
    var root = Node3D.new()
    var mesh = MeshInstance3D.new()
    mesh.mesh = BoxMesh.new()
    root.add_child(mesh)
    scene.pack(root)
    return scene.resource_path  # Save temp or preload
```

## Review Needed
Proposed para-type: resource. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.