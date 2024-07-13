import bpy
from . import tile_marker_type
from . import tile_marker_types
from . import erase_material as em

__data = None

def __getattr__(name):
    if name == 'data':
        global __data
        if __data is None:
            __data = ConfigData()
        return __data
    
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

class ConfigData:
    @staticmethod
    def init():
        bpy.types.Scene.gpencil = bpy.props.PointerProperty(type = bpy.types.Object, name = "gpencil")
        bpy.types.Scene.erase_material = bpy.props.PointerProperty(type = em.EraseMaterial, name = "erase_material")
        bpy.types.Scene.marker_types = bpy.props.CollectionProperty(type = tile_marker_type.TileMarkerType)
        bpy.types.Scene.marker_types_index = bpy.props.IntProperty(name = "Index for marker_types", default = 0)

    def __init__(self):
        self.gpencil_object = bpy.context.scene.gpencil
        self.erase_material = bpy.context.scene.erase_material
        self.marker_types = tile_marker_types.TileMarkerTypes()