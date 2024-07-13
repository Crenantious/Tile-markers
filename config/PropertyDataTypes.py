import bpy

def is_gpencil_material(self, object):
    return object.is_grease_pencil

def is_marker_material(self, object):
    return object.is_grease_pencil is False

# TODO: consider validating the names are unique
class TileMarkerType(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name", default="name")
    gpencil_material: bpy.props.PointerProperty(type=bpy.types.Material, name="GPencil material", poll = is_gpencil_material,
                                                description = "The gpencil material used to indicate where to create tile markers with the corresponding 'marker material' below")
    marker_material: bpy.props.PointerProperty(type=bpy.types.Material, name="Marker material", poll = is_marker_material,
                                               description = "The material added to the tile marker that was created using the above 'gpencil material'")

class DataGroup(bpy.types.PropertyGroup):
    gpencil: bpy.props.PointerProperty(type = bpy.types.Object, name = "gpencil")
    erase_material: bpy.props.PointerProperty(type = bpy.types.Material, name="GPencil erase material", poll = is_gpencil_material,
                                              description = "The gpencil material that is used to erase tiles")
    marker_types: bpy.props.CollectionProperty(type = TileMarkerType)
    marker_types_index: bpy.props.IntProperty(name = "Index for marker_types", default = 0)
    tile_size: bpy.props.FloatProperty(name = "Tile width and height", default = 0)
    map: bpy.props.PointerProperty(type = bpy.types.Object, name = "map", description = "The object to generae tile markers from.")