import bpy
import bgl
import blf

from .tile_marker import *
from .materials import *
from .dynamic_property import *
from .gpencil import *

TILE_MATERIAL_KEY = "TILE_MATERIAL"


def delete_objects(objs):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objs:
        obj.select_set(True)
    bpy.ops.object.delete()


def is_map(obj):
    return obj == bpy.data.objects["Map"]


class TileMarkers(bpy.types.Operator):
    """Tile markers"""
    bl_idname = "view3d.modal_operator"
    bl_label = "RuneScape tile markers"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self):
        self.dive_stroke_mat = None
        self.dive_tile_mat = None
        self.surge_stroke_mat = None
        self.surge_tile_mat = None
        self.escape_stroke_mat = None
        self.escape_tile_mat = None
        self.erase_stroke_mat = None
        self.erase_tile_mat = None
        self.draw_brush = None
        self.gpencil = None

    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            context.window_manager.modal_handler_add(self)

            register_property(bpy.types.Material, "tile_marker_material")
            register_property(bpy.types.Object, "is_tile_marker", False)

            self.initialise_materials()
            self.draw_brush = get_draw_brush()
            self.gpencil = create_gpencil([self.dive_stroke_mat, self.surge_stroke_mat,
                                   self.escape_stroke_mat, self.erase_stroke_mat])
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}

    def initialise_materials(self):
        self.dive_stroke_mat, self.dive_tile_mat = get_materials("Dive", (1, 1, 0, 1))
        self.surge_stroke_mat, self.surge_tile_mat = get_materials("Surge", (0, 0, 1, 1))
        self.escape_stroke_mat, self.escape_tile_mat = get_materials("Escape", (0, 1, 0, 1))
        self.erase_stroke_mat, self.erase_tile_mat = get_materials("Erase", (0.1, 0.1, 0.1, 1))

    def modal(self, context, event):
        context.area.tag_redraw()
        obj = bpy.context.view_layer.objects.active

        if event.type == 'ESC':
            self.on_esc()

        # TODO: Move to a validation class
        elif event.type == 'MOUSEMOVE' and obj is not None and obj.type == 'GPENCIL' and obj.mode == 'PAINT_GPENCIL':
            gp_points_exist, map_locations, tile_markers = self.raycast_gpencil_points(obj)

            if gp_points_exist:
                bpy.ops.gpencil.delete(type='POINTS')

            self.handle_selected_objects(map_locations, tile_markers)

        return {'PASS_THROUGH'}

    def handle_selected_objects(self, map_locations, tile_markers):
        stroke_material = self.gpencil.active_material
        tile_marker_material = stroke_material.tile_marker_material
        if tile_marker_material is not None:
            if stroke_material == self.erase_stroke_mat:
                delete_objects(tile_markers)
            else:
                create_markers(map_locations, tile_marker_material)

            bpy.context.view_layer.objects.active = self.gpencil
            bpy.ops.object.mode_set(mode='PAINT_GPENCIL')

    def raycast_gpencil_points(self, obj):
        gp_points_exist = False
        map_locations = set()
        tile_markers = set()

        for layer in obj.data.layers:
            for frame in layer.frames:
                for stroke in frame.strokes:
                    for point in stroke.points:
                        gp_points_exist = True
                        point.select = True
                        result, location, obj_hit = get_object_under_point(self.gpencil, point)
                        if result:
                            if is_map(obj_hit):
                                map_locations.add(location)
                            elif obj_hit.is_tile_marker:
                                tile_markers.add(obj_hit)

        return gp_points_exist, map_locations, tile_markers

    @staticmethod
    def on_esc():
        bpy.ops.object.delete()
        return {'CANCELLED'}
