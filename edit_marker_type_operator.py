import bpy

class EditMarkerType(bpy.types.Operator):
    """Edit marker type"""
    bl_idname = "tile_markers.edit_marker_type"
    bl_label = "Edit marker type"
    bl_options = {'INTERNAL'}

    marker_type_index: bpy.props.IntProperty()

    def execute(self, context):
        mt = context.scene.marker_types[self.marker_type_index]
        mt.edit_mode = not mt.edit_mode
        return {'FINISHED'}