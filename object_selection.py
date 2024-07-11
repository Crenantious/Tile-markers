import bpy
from bpy_extras import view3d_utils

TILE_SIZE = 2

def get_nearest_tile_vertex(vertex):
    return (int(vertex / TILE_SIZE) + 0.5) * TILE_SIZE


def get_nearest_tile(pos):
    return get_nearest_tile_vertex(pos.x), get_nearest_tile_vertex(pos.y), get_nearest_tile_vertex(pos.z)

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