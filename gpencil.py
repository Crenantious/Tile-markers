import bpy

from .tile_marker_types import marker_types

GPENCIL_NAME = "Draw tile markers"

__gpencil = None

def __getattr__(name):
    if name == 'gpencil':
        global __gpencil
        if __gpencil is None:
            __gpencil = GPencil()
        return __gpencil
    
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

class GPencil:
    def __init__(self):
        bpy.types.Scene.gpencil = bpy.props.PointerProperty(type = bpy.types.Object, name = "gpencil")
        self.object = bpy.context.scene.gpencil

        self.brush = self.setup_brush()
        self.set_materials()
        self.erase_material = None

    def create(self):
        self.object, self.data = self.__create()
        bpy.context.scene.gpencil = self.object

    def __create(self):
        data = bpy.data.grease_pencils.new(GPENCIL_NAME)
        gpencil = bpy.data.objects.new(GPENCIL_NAME, data)

        bpy.context.scene.collection.objects.link(gpencil)
        bpy.context.scene.tool_settings.gpencil_stroke_placement_view3d = 'SURFACE'

        gpencil.data.layers.new("Draw")
        gpencil.data.layers[0].frames.new(0, active=True)
        
        return gpencil, data

    def setup_brush(self):
        brush = self.get_brush('Draw tiles', 'ADD')
        bpy.context.scene.tool_settings.gpencil_paint.brush = brush
        return brush
    
    def get_brush(self, name, blend):
        if name in bpy.data.brushes:
            brush = bpy.data.brushes[name]
        else:
            brush = bpy.data.brushes.new(name, mode='PAINT_GPENCIL')

        brush.use_paint_grease_pencil = True
        brush.blend = blend
        brush.use_pressure_strength = False
        bpy.data.brushes.create_gpencil_data(brush)
        return brush
    
    def set_materials(self):
        #self.object.material_slots.clear()
        self.materials = {}

        for marker_type in marker_types.types:
            stroke, marker = marker_type.stroke_material, marker_type.marker_material
            if stroke is None or marker is None:
                continue # Notify user of error

            self.materials[stroke] = marker
            self.data.materials.append(marker)

    def set_object_active(self):
        bpy.context.view_layer.objects.active = self.object
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        self.object.select_set(True)
        bpy.ops.object.mode_set(mode='PAINT_GPENCIL')

    def does_object_exist(self):
        return self.object in bpy.context.scene.objects.values()
    
    def is_object_active(self):
        return bpy.context.view_layer.objects.active == self.object
    
    def is_mode_correct(self):
        return bpy.context.object.mode == 'PAINT_GPENCIL'