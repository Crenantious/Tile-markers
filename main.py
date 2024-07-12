import bpy

from .materials import *
from .dynamic_property import *
from .gpencil import *
from . import object_selection

class TileMarkers(bpy.types.Operator):
    """Tile markers"""
    bl_idname = "tile_markers.tile_markers"
    bl_label = "Tile markers"
    bl_options = {'REGISTER', 'UNDO'}
    active_operator = None
    gpencil = None

    def __init__(self):
        self.is_finished = False
        self.validation = TileMarkersValidation()

    def invoke(self, context, event):
        self.validation.validate_area(context)
        self.validation.validate_active_operator()
        self.validation.validate_gpencil()
        if self.validation.error is not None:
            return self.validation.error
        
        context.window_manager.modal_handler_add(self)

        register_property(bpy.types.Object, "is_tile_marker", False)
            
        #if TileMarkers.gpencil is None:
        TileMarkers.gpencil = GPencil()

        TileMarkers.gpencil.set_object_active()
        TileMarkers.active_operator = self

        return {'RUNNING_MODAL'}    

    def modal(self, context, event):
        if self.is_finished:
            return {'FINISHED'}
        
        context.area.tag_redraw()
        
        if self.validation.validate_modal_event(event) is False:
            return {'PASS_THROUGH'}
        
        gp_points_exist, map_locations, tile_markers = object_selection.raycast_gpencil_points(TileMarkers.gpencil)

        if gp_points_exist:
            bpy.ops.gpencil.delete(type='POINTS')
            object_selection.handle_selected_objects(TileMarkers.gpencil, map_locations, tile_markers)
        
        return {'PASS_THROUGH'}

    def finish(self):
        self.is_finished = True

class TileMarkersValidation:
    def __init__(self):
        self.error = None
    
    def validate_area(self, context):
        if context.area.type != 'VIEW_3D':
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            self.__try_set_error('CANCELLED')
    
    def validate_active_operator(self):
        if TileMarkers.active_operator is not None:
            TileMarkers.active_operator.finish()
            TileMarkers.active_operator = None
    
    def validate_gpencil(self):
        gpencil = TileMarkers.gpencil
        if gpencil is not None and gpencil.object_exists() and gpencil.is_object_active() and gpencil.is_mode_correct():
            bpy.ops.object.mode_set(mode='OBJECT')
            self.__try_set_error('FINISHED')
    
    def validate_modal_event(self, event):
        obj = bpy.context.view_layer.objects.active
        return event.type == 'MOUSEMOVE' and obj is not None and obj == TileMarkers.gpencil.object

    def __try_set_error(self, error):
        if self.error is None:
            self.error = {error}