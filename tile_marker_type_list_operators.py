import bpy
from .tile_marker_types import marker_types

class AddMarkerType(bpy.types.Operator):
    """Add marker type"""
    bl_idname = "tile_markers.add_marker_type"
    bl_label = "Add marker type"
    bl_options = {'INTERNAL', 'UNDO'}

    @classmethod
    def poll(cls, context):
        # TODO: think about a limit
        return True
    
    def execute(self, context):
        marker_types.add()
        marker_types.index.set_to_end()
        return {'FINISHED'}

class RemoveMarkerType(bpy.types.Operator):
    """Remove marker type"""
    bl_idname = "tile_markers.remove_marker_type"
    bl_label = "Remove marker type"
    bl_options = {'INTERNAL', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return marker_types.get_active_item() is not None

    def execute(self, context):
        marker_types.remove_current()
        return {'FINISHED'}
    
class MoveMarkerTypeUp(bpy.types.Operator):
    """Move marker type up"""
    bl_idname = "tile_markers.move_marker_type_up"
    bl_label = "Move marker type up"
    bl_options = {'INTERNAL', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return marker_types.index.value > 0

    def execute(self, context):
        marker_types.move_up()
        return {'FINISHED'}

class MoveMarkerTypeDown(bpy.types.Operator):
    """Move marker type down"""
    bl_idname = "tile_markers.move_marker_type_down"
    bl_label = "Move marker type down"
    bl_options = {'INTERNAL', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return marker_types.index.value < marker_types.index.max

    def execute(self, context):
        marker_types.move_down()
        return {'FINISHED'}