import bpy

class MarkerType(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name", default="name")
    stroke_material: bpy.props.PointerProperty(type=bpy.types.Material, name="Stroke material")
    marker_material: bpy.props.PointerProperty(type=bpy.types.Material, name="Marker material")
    edit_mode: bpy.props.BoolProperty(name="Edit mode")
