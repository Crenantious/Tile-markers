import bpy
from bpy_extras import view3d_utils
from . import tile_marker
from .config import data

def raycast_gpencil_points(gpencil):
    gp_points_exist = False
    map_locations = set()
    tile_markers = set()

    for layer in gpencil.object.data.layers:
        for frame in layer.frames:
            for stroke in frame.strokes:
                for point in stroke.points:
                    gp_points_exist = True
                    point.select = True
                    result, location, obj_hit = get_object_under_point(gpencil.object, point)
                    if result:
                        if is_map(obj_hit):
                            map_locations.add(location)
                        elif obj_hit.is_tile_marker:
                            tile_markers.add(obj_hit)

    return gp_points_exist, map_locations, tile_markers

# TODO: rename
def get_object_under_point(gpencil, point):
    scene = bpy.context.scene
    region = bpy.context.region
    rv3d = bpy.context.region_data

    screen_point = view3d_utils.location_3d_to_region_2d(region, rv3d, point.co + gpencil.location)
    view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, screen_point)
    ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, screen_point)

    result, location, normal, index, obj, matrix = scene.ray_cast(bpy.context.evaluated_depsgraph_get(), ray_origin,
                                                                  view_vector)

    if result:
        location = get_nearest_tile(location)
    return result, location, obj

def handle_selected_objects(gpencil, map_locations, tile_markers):
    stroke_material = gpencil.object.active_material

    if stroke_material is None:
        return

    if stroke_material == data.config_data.erase_material:
        delete_objects(tile_markers)

    if stroke_material in gpencil.materials:
        tile_marker_material = gpencil.materials[stroke_material]
        tile_marker.create_markers(map_locations, tile_marker_material)

    bpy.context.view_layer.objects.active = gpencil.object
    bpy.ops.object.mode_set(mode='PAINT_GPENCIL')

def get_nearest_tile_vertex(vertex):
    return (int(vertex / data.config_data.tile_size) + 0.5) * data.config_data.tile_size

def get_nearest_tile(pos):
    return get_nearest_tile_vertex(pos.x), get_nearest_tile_vertex(pos.y), get_nearest_tile_vertex(pos.z)

def is_map(obj):
    return obj == bpy.data.objects["Map"]

def delete_objects(objs):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objs:
        obj.select_set(True)
    bpy.ops.object.delete()