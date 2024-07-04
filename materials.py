import bpy


def get_materials(name, colour):
    stroke_mat = get_stroke_material(name, colour)
    tile_marker_mat = get_tile_marker_material(name, colour)
    stroke_mat.tile_marker_material = tile_marker_mat
    return stroke_mat, tile_marker_mat


def get_stroke_material(name, colour):
    name += " stroke"
    if name in bpy.data.materials:
        material = bpy.data.materials[name]
    else:
        material = bpy.data.materials.new(name)
        
    bpy.data.materials.create_gpencil_data(material)
    material.grease_pencil.color = colour
    return material


def get_tile_marker_material(name, colour):
    name += " tile"
    if name in bpy.data.materials:
        material = bpy.data.materials[name]
    else:
        material = bpy.data.materials.new(name)
        
    material.use_nodes = True
    principled = material.node_tree.nodes['Principled BSDF']
    principled.inputs['Base Color'].default_value = colour
    return material
