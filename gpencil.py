import bpy

from .tile_marker_types import marker_types

GPENCIL_NAME = "Draw tile markers"

class GPencil:
    def __init__(self, existing_gpencil_object = None):
        if existing_gpencil_object is None:
            self.object = __create()
        else:
            self.object = existing_gpencil_object
            
        self.brush = self.setup_brush()
        self.set_materials()
        self.erase_material = None

    def set_materials(self):
        self.object.data.materials.clear()
        self.materials = {}

        for marker_type in marker_types.types:
            self.materials[marker_type.stroke_material] = marker_type.marker_material
            self.object.data.materials.append(marker_type.marker_material)

    def set_object_active(self):
        bpy.context.view_layer.objects.active = self.object
        bpy.ops.object.select_all(action='DESELECT')
        self.object.select_set(True)
        bpy.ops.object.mode_set(mode='PAINT_GPENCIL')

    def setup_brush(self):
        brush = get_brush('Draw tiles', 'ADD')
        bpy.context.scene.tool_settings.gpencil_paint.brush = brush
        return brush
    
    def object_exists(self):
        return object in bpy.context.scene.objects.values()
    
    def is_object_active():
        return bpy.context.view_layer.objects.active == object
    
    def is_mode_correct():
        return bpy.context.object.mode == 'PAINT_GPENCIL'

def __create():
    data = bpy.data.grease_pencils.new(GPENCIL_NAME)
    gpencil = bpy.data.objects.new(GPENCIL_NAME, data)

    bpy.context.scene.collection.objects.link(gpencil)
    bpy.context.scene.tool_settings.gpencil_stroke_placement_view3d = 'SURFACE'

    gpencil.data.layers.new("Draw")
    gpencil.data.layers[0].frames.new(0, active=True)
    
    return gpencil

def get_brush(name, blend):
    if name in bpy.data.brushes:
        brush = bpy.data.brushes[name]
    else:
        brush = bpy.data.brushes.new(name, mode='PAINT_GPENCIL')

    brush.use_paint_grease_pencil = True
    brush.blend = blend
    brush.use_pressure_strength = False
    bpy.data.brushes.create_gpencil_data(brush)
    return brush

def get_existing_object():
    if GPENCIL_NAME in bpy.data.objects:
        return bpy.data.objects[GPENCIL_NAME]
    return None