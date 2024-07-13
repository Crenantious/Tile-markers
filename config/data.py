import bpy

from . import PropertyDataTypes

__properties = {}


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

def init():
    bpy.types.Scene.tile_markers_config_data = bpy.props.PointerProperty(type = PropertyDataTypes.DataGroup, name = "Config data")
    def data():
        return bpy.context.scene.tile_markers_config_data

    add_property("gpencil_object", lambda: data().gpencil)
    add_property("erase_material", lambda: data().erase_material)

def __getattr__(name):
    if name == "config_data":
        return bpy.context.scene.tile_markers_config_data
    
    if name in __properties:
        property = __properties[name]
        if property.value is None:
            property.set_value()
        return property.value
    
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")