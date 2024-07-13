import bpy

from . import tile_marker_type
from . import tile_marker_types
from . import erase_material as em

__properties = {}

def init():
    bpy.types.Scene.gpencil = bpy.props.PointerProperty(type = bpy.types.Object, name = "gpencil")
    bpy.types.Scene.erase_material = bpy.props.PointerProperty(type = em.EraseMaterial, name = "erase_material")
    bpy.types.Scene.marker_types = bpy.props.CollectionProperty(type = tile_marker_type.TileMarkerType)
    bpy.types.Scene.marker_types_index = bpy.props.IntProperty(name = "Index for marker_types", default = 0)

    class Property:
        def __init__(self, name, getter):
            self.value = None
            self.name = name
            self.getter = getter
        
        def set_value(self):
            self.value = self.getter()

    def add_property(name, getter):
        global __properties
        __properties[name] = Property(name, getter)
        
    add_property("gpencil_object", lambda: bpy.context.scene.gpencil)
    add_property("erase_material", lambda: bpy.context.scene.erase_material)
    add_property("marker_types", lambda: tile_marker_types.TileMarkerTypes())
    add_property("gpencil_object", lambda: bpy.context.scene.gpencil)

def __getattr__(name):
    if name in __properties:
        property = __properties[name]
        if property.value is None:
            property.set_value()
        return property.value
    
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")