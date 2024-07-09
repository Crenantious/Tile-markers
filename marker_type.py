import bpy

# TODO: consider validating the names are unique
class MarkerType(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name", default="name")
    stroke_material: bpy.props.PointerProperty(type=bpy.types.Material, name="Stroke material")
    marker_material: bpy.props.PointerProperty(type=bpy.types.Material, name="Marker material")