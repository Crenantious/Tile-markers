import bpy

# TODO: put into config/preferences
TILE_SIZE = 2

class TileMarker:
    def __init__(self, location, material):
        bpy.ops.mesh.primitive_cube_add(location=location)
        bpy.ops.transform.resize(value=(TILE_SIZE / 2, TILE_SIZE / 2, 10))

        self.object = bpy.context.object
        self.object.data.materials.clear()
        self.object.data.materials.append(material)
        self.object.is_tile_marker = True

        self.bool_intersect(bpy.data.objects["Map"])

    def bool_intersect(self, floor):
        self.object.modifiers.clear()
        mod = self.object.modifiers.new('Boolean', type='BOOLEAN')
        mod.object = floor
        mod.operation = 'INTERSECT'
        bpy.ops.object.modifier_apply(modifier=mod.name)

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        for vert in self.object.data.vertices:
            if vert.co[2] * 10 + self.object.location[2] < -0.01:  # Under floor
                vert.select = True
            vert.co += vert.normal * 0.001  # Scale slightly to avoid some clipping (fails for complex geometry)

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.delete(type='VERT')
        bpy.ops.object.mode_set(mode='OBJECT')

def create_markers(locations, material):
    for location in locations:
        TileMarker(location, material)