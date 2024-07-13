import bpy

def is_gpencil_material(self, object):
    return object.is_grease_pencil

def is_marker_material(self, object):
    return object.is_grease_pencil is False

# TODO: consider validating the names are unique
class TileMarkerType(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name", default="name")
    gpencil_material: bpy.props.PointerProperty(type=bpy.types.Material, name="GPencil material", poll = is_gpencil_material)
    marker_material: bpy.props.PointerProperty(type=bpy.types.Material, name="Marker material", poll = is_marker_material)