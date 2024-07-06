import bpy

from bpy_extras import view3d_utils

GPENCIL_NAME = "Draw tile markers"
TILE_SIZE = 2
object = None

# TODO: rename
def setup(materials):
    global object
    if object is None:
        if GPENCIL_NAME in bpy.data.objects:
            object = bpy.data.objects[GPENCIL_NAME]
        else:
            object = create(materials)
    elif object not in bpy.context.scene.objects.values(): # object deleted
        object = create(materials)

    set_gpencil_active()

def is_active():
    global object
    return object is not None and bpy.context.view_layer.objects.active == object and object in bpy.context.scene.objects.values() and bpy.context.object.mode == 'PAINT_GPENCIL'

def create(materials):
    data = bpy.data.grease_pencils.new(GPENCIL_NAME)
    gpencil = bpy.data.objects.new(GPENCIL_NAME, data)

    bpy.context.scene.collection.objects.link(gpencil)
    bpy.context.scene.tool_settings.gpencil_stroke_placement_view3d = 'SURFACE'

    gpencil.data.layers.new("Draw")
    gpencil.data.layers[0].frames.new(0, active=True)

    for material in materials:
        data.materials.append(material)
    
    return gpencil

def set_gpencil_active():
    global object
    bpy.context.view_layer.objects.active = object
    bpy.ops.object.select_all(action='DESELECT')
    object.select_set(True)
    bpy.ops.object.mode_set(mode='PAINT_GPENCIL')

def get_brush(name, blend):
    if name in bpy.data.brushes:
        brush = bpy.data.brushes[name]
    else:
        brush = bpy.data.brushes.new(name, mode='PAINT_GPENCIL')

    brush.use_paint_grease_pencil = True
    brush.blend = blend
    brush.use_pressure_strength = False
    bpy.data.brushes.create_gpencil_data(brush)
    return brush


def get_draw_brush():
    brush = get_brush('Draw tiles', 'ADD')
    bpy.context.scene.tool_settings.gpencil_paint.brush = brush
    return brush


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