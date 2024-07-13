import bpy

def is_gpencil_material(self, object):
    return object.is_grease_pencil

class EraseMaterial(bpy.types.PropertyGroup):
    material: bpy.props.PointerProperty(type=bpy.types.Material, name="GPencil material", poll = is_gpencil_material)