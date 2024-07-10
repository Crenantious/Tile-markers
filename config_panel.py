import bpy
from . import marker_type_list_operators as list_operators
from .tile_marker_types import marker_types

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

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.template_list("Material_UI_LIST", "", bpy.context.scene, "marker_types", bpy.context.scene, "marker_types_index")
        column = row.column()
        column.operator(list_operators.AddMarkerType.bl_idname, text="", icon='ADD')
        column.operator(list_operators.RemoveMarkerType.bl_idname, text="", icon='REMOVE')
        column.operator(list_operators.MoveMarkerTypeUp.bl_idname, text="", icon='TRIA_UP')
        column.operator(list_operators.MoveMarkerTypeDown.bl_idname, text="", icon='TRIA_DOWN')

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
        layout = self.layout
        item = marker_types.get_active_item()
        
        if item is None:
            return
        
        layout.prop(item, 'name')
        layout.prop(item, 'stroke_material')
        layout.prop(item, 'marker_material')