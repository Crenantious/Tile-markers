import bpy
import bpy.utils.previews
from . import edit_marker_type_operator as emt

class TileMarkerTypesPanel(bpy.types.Panel):
    bl_label = "Tile marker types"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_idname = "VIEW3D_PT_tile_marker_types"
    is_list_setup = False # For testing only
    bl_order = 1

    def __init__(self):
        if TileMarkerTypesPanel.is_list_setup is False:
            TileMarkerTypesPanel.is_list_setup = True
            #bpy.context.scene.marker_types.add()

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.template_list("Material_UI_LIST", "", context.scene, "marker_types", context.scene, "marker_types_index")
        column = row.column()
        column.label(icon='ADD') # Make an operator
        column.label(icon='REMOVE') # Make an operator
        column.label(icon='TRIA_UP') # Make an operator
        column.label(icon='TRIA_DOWN') # Make an operator

class Material_UI_LIST(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(text=item.name)

class EditTileMarkerTypePanel(bpy.types.Panel):
    bl_label = "Edit tile marker type"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_idname = "VIEW3D_PT_edit_tile_marker_type"
    bl_order = 0

    def draw(self, context):
        if context.scene.marker_types_index >= len(context.scene.marker_types):
            return
        
        layout = self.layout
        item = context.scene.marker_types[context.scene.marker_types_index]
        layout.prop(item, 'name')
        layout.prop(item, 'stroke_material')
        layout.prop(item, 'marker_material')