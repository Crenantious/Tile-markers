import bpy
import bmesh

from .config import data

class TileMarker:
    def __init__(self, location, material):
        bpy.ops.mesh.primitive_cube_add(location=location, calc_uvs=False)
        bpy.ops.transform.resize(value=(data.config_data.tile_size / 2, data.config_data.tile_size / 2, 10))

        self.object = bpy.context.object
        self.object.name = "Tile marker"
        self.object.data.materials.append(material)
        self.object.is_tile_marker = True

        self.bool_intersect(data.config_data.map)
        self.delete_excess_verts()

    def bool_intersect(self, floor):
        mod = self.object.modifiers.new('Boolean', type='BOOLEAN')
        mod.object = floor
        mod.operation = 'INTERSECT'
        bpy.ops.object.modifier_apply(modifier=mod.name)

    def delete_excess_verts(self):
        # TODO: Not sure why but removing these causes some extra verticies to be deleted.
        bm = bmesh.new()
        bm.from_mesh(self.object.data)
        verts_to_delete = []

        for vert in bm.verts:
            if vert.co.z * 10 + self.object.location.z < -0.01:  # Under floor
                verts_to_delete.append(vert)
            vert.co += vert.normal * 0.001  # Scale slightly to avoid some clipping (fails for complex geometry)

        bmesh.ops.delete(bm, geom = verts_to_delete, context = 'VERTS')
        bm.to_mesh(self.object.data)
        bm.free()