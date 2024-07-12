import bpy

from .materials import *
from .dynamic_property import *
from . import gpencil as gp
from . import object_selection
from .validation import *

class TileMarkers(bpy.types.Operator):
    """Tile markers"""
    bl_idname = "tile_markers.tile_markers"
    bl_label = "Tile markers"
    bl_options = {'REGISTER', 'UNDO'}
    active_operator = None

    validators = Validators()
    validators.add(Validator(validate_area))
    validators.add(Validator(validate_active_operator))
    validators.add(Validator(validate_gpencil))

    def __init__(self):
        self.is_finished = False

    def invoke(self, context, event):
        TileMarkers.validators.validators[0].set_args(context)
        result = TileMarkers.validators.validate()
        if result is not None:
            return result
        
        context.window_manager.modal_handler_add(self)

        register_property(bpy.types.Object, "is_tile_marker", False)
            
        gp.gpencil

        gp.gpencil.set_object_active()
        TileMarkers.active_operator = self

        return {'RUNNING_MODAL'}    

    def modal(self, context, event):
        if self.is_finished:
            return {'FINISHED'}
        
        context.area.tag_redraw()
        
        if self.validators.validate_modal_event(event) is False:
            return {'PASS_THROUGH'}
        
        gp_points_exist, map_locations, tile_markers = object_selection.raycast_gpencil_points(gp.gpencil)

        if gp_points_exist:
            bpy.ops.gpencil.delete(type='POINTS')
            object_selection.handle_selected_objects(gp.gpencil, map_locations, tile_markers)
        
        return {'PASS_THROUGH'}

    def finish(self):
        self.is_finished = True