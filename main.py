import bpy

from .tile_marker import *
from .materials import *
from .dynamic_property import *
from . import gpencil

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
    bl_idname = "tile_markers.tile_markers"
    bl_label = "Tile markers"
    bl_options = {'REGISTER', 'UNDO'}
    active_operator = None

    def __init__(self):
        self.is_finished = False
        self.dive_stroke_mat = None
        self.dive_tile_mat = None
        self.surge_stroke_mat = None
        self.surge_tile_mat = None
        self.escape_stroke_mat = None
        self.escape_tile_mat = None
        self.erase_stroke_mat = None
        self.erase_tile_mat = None
        self.draw_brush = None

    def invoke(self, context, event):
        if TileMarkers.active_operator is not None:
            TileMarkers.active_operator.finish()
            
        if gpencil.is_active():
            bpy.ops.object.mode_set(mode='OBJECT')
            TileMarkers.active_operator = None
            return {'FINISHED'}
            
        if context.area.type != 'VIEW_3D':
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}
        
        context.window_manager.modal_handler_add(self)

        register_property(bpy.types.Material, "tile_marker_material")
        register_property(bpy.types.Object, "is_tile_marker", False)

        self.initialise_materials()
        self.draw_brush = gpencil.get_draw_brush()
            
        gpencil.setup([self.dive_stroke_mat, self.surge_stroke_mat,
                       self.escape_stroke_mat, self.erase_stroke_mat])

        TileMarkers.active_operator = self

        return {'RUNNING_MODAL'}

    def initialise_materials(self):
        self.dive_stroke_mat, self.dive_tile_mat = get_materials("Dive", (1, 1, 0, 1))
        self.surge_stroke_mat, self.surge_tile_mat = get_materials("Surge", (0, 0, 1, 1))
        self.escape_stroke_mat, self.escape_tile_mat = get_materials("Escape", (0, 1, 0, 1))
        self.erase_stroke_mat, self.erase_tile_mat = get_materials("Erase", (0.1, 0.1, 0.1, 1))

    def modal(self, context, event):
        if self.is_finished:
            return {'FINISHED'}
        
        context.area.tag_redraw()
        obj = bpy.context.view_layer.objects.active

        # TODO: Move to a validation class
        if event.type == 'MOUSEMOVE' and obj is not None and obj == gpencil.object:
            gp_points_exist, map_locations, tile_markers = self.raycast_gpencil_points(obj)

            if gp_points_exist:
                bpy.ops.gpencil.delete(type='POINTS')
                self.handle_selected_objects(map_locations, tile_markers)

        return {'PASS_THROUGH'}

    def handle_selected_objects(self, map_locations, tile_markers):
        stroke_material = gpencil.object.active_material
        tile_marker_material = stroke_material.tile_marker_material
        if tile_marker_material is not None:
            if stroke_material == self.erase_stroke_mat:
                delete_objects(tile_markers)
            else:
                create_markers(map_locations, tile_marker_material)

            bpy.context.view_layer.objects.active = gpencil.object
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
                        result, location, obj_hit = gpencil.get_object_under_point(gpencil.object, point)
                        if result:
                            if is_map(obj_hit):
                                map_locations.add(location)
                            elif obj_hit.is_tile_marker:
                                tile_markers.add(obj_hit)

        return gp_points_exist, map_locations, tile_markers

    def finish(self):
        self.is_finished = True
