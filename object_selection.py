import bpy
from bpy_extras import view3d_utils
from . import tile_marker

TILE_SIZE = 2

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
    tile_marker_material = stroke_material.tile_marker_material
    if tile_marker_material is not None:
        if stroke_material == gpencil.erase_material:
            delete_objects(tile_markers)
        else:
            tile_marker.create_markers(map_locations, tile_marker_material)

        bpy.context.view_layer.objects.active = gpencil.object
        bpy.ops.object.mode_set(mode='PAINT_GPENCIL')

def get_nearest_tile_vertex(vertex):
    return (int(vertex / TILE_SIZE) + 0.5) * TILE_SIZE


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