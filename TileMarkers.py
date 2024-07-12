import bpy

from .materials import *
from . import gpencil as gp
from . import object_selection
from .validation import *
from .validators import *

class TileMarkers(bpy.types.Operator):
    """Tile markers"""
    bl_idname = "tile_markers.tile_markers"
    bl_label = "Tile markers"
    bl_options = {'REGISTER', 'UNDO'}

    invoke_validators = Validators()
    invoke_validators.add(Validator(validate_area))
    invoke_validators.add(Validator(validate_active_operator))
    invoke_validators.add(Validator(validate_gpencil))

    modal_validators = Validators()
    modal_validators.add(Validator(validate_modal_event))

    def __init__(self):
        self.is_finished = False

    def invoke(self, context, event):
        TileMarkers.invoke_validators.validators[0].set_args(context)
        errors = TileMarkers.invoke_validators.validate()
        if len(errors) > 0:
            return errors
        
        context.window_manager.modal_handler_add(self)

        gp.gpencil.set_object_active()
        TileMarkers.active_operator = self

        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        TileMarkers.modal_validators.validators[0].set_args(self, event)
        errors = TileMarkers.modal_validators.validate()
        if len(errors) > 0:
            return errors
        
        context.area.tag_redraw()
        
        gp_points_exist, map_locations, tile_markers = object_selection.raycast_gpencil_points(gp.gpencil)

        if gp_points_exist:
            bpy.ops.gpencil.delete(type='POINTS')
            object_selection.handle_selected_objects(gp.gpencil, map_locations, tile_markers)
        
        return {'PASS_THROUGH'}

    def finish(self):
        self.is_finished = True