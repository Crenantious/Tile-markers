import bpy

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
        context.scene.marker_types.add()
        context.scene.marker_types_index = len(context.scene.marker_types) - 1
        return {'FINISHED'}

class RemoveMarkerType(bpy.types.Operator):
    """Remove marker type"""
    bl_idname = "tile_markers.remove_marker_type"
    bl_label = "Remove marker type"
    bl_options = {'INTERNAL', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return is_index_in_range(context)

    def execute(self, context):
        context.scene.marker_types.remove(context.scene.marker_types_index)
        clamp_index(context)
        return {'FINISHED'}
    
class MoveMarkerTypeUp(bpy.types.Operator):
    """Move marker type up"""
    bl_idname = "tile_markers.move_marker_type_up"
    bl_label = "Move marker type up"
    bl_options = {'INTERNAL', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.scene.marker_types_index > 0

    def execute(self, context):
        index = context.scene.marker_types_index

        context.scene.marker_types.move(index, index - 1)
        context.scene.marker_types_index -= 1
        return {'FINISHED'}

class MoveMarkerTypeDown(bpy.types.Operator):
    """Move marker type down"""
    bl_idname = "tile_markers.move_marker_type_down"
    bl_label = "Move marker type down"
    bl_options = {'INTERNAL', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.scene.marker_types_index < len(context.scene.marker_types) - 1
    
    def execute(self, context):
        index = context.scene.marker_types_index
        
        context.scene.marker_types.move(index, index + 1)
        context.scene.marker_types_index += 1
        return {'FINISHED'}

def clamp_index(context):
    index, length = context.scene.marker_types_index, len(context.scene.marker_types)
    context.scene.marker_types_index = max(0, min(index, length - 1))

def is_index_in_range(context):
    index, length = context.scene.marker_types_index, len(context.scene.marker_types)
    return index >=0 and index < length