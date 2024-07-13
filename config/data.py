import bpy

from . import tile_marker_type
from . import tile_marker_types
from . import erase_material as em

def init():
    bpy.types.Scene.gpencil = bpy.props.PointerProperty(type = bpy.types.Object, name = "gpencil")
    bpy.types.Scene.erase_material = bpy.props.PointerProperty(type = em.EraseMaterial, name = "erase_material")
    bpy.types.Scene.marker_types = bpy.props.CollectionProperty(type = tile_marker_type.TileMarkerType)
    bpy.types.Scene.marker_types_index = bpy.props.IntProperty(name = "Index for marker_types", default = 0)

class Data:
    def __init__(self):
        self.gpencil_object = None
        self.erase_material = None
        self.marker_types = None

__data = Data()
__gpencil_object = None
__erase_material = None
__marker_types = None

def __getattr__(name):
    def gpencil_object():
        return bpy.context.scene.gpencil

    def erase_material():
        return bpy.context.scene.erase_material

    def marker_types():
        return tile_marker_types.TileMarkerTypes()
    
    var_map = {'gpencil_object': gpencil_object, 'erase_material': erase_material, 'marker_types': marker_types}
    if name in var_map:
        if getattr(__data, name) is None:
            setattr(__data, name, var_map[name]())
        return getattr(__data, name)
    
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")