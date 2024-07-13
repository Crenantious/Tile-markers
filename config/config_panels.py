import bpy

from .. import tile_marker_type_list_operators as list_operators
from . import data

class PanelInfo:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Create"
    bl_options = {"DEFAULT_CLOSED"}

class ConfigPanel(PanelInfo, bpy.types.Panel):
    bl_label = "Tile markers"
    bl_idname = "VIEW3D_PT_tm_config"

    def draw(self, context):
        self.layout.prop_with_label("Tile size", data.config_data, 'tile_size')

class MaterialsPanel(PanelInfo, bpy.types.Panel):
    bl_label = "Materials"
    bl_idname = "VIEW3D_PT_tm_config_materials"
    bl_parent_id = ConfigPanel.bl_idname
    bl_order = 0

    def draw(self, context):
        column = self.layout.column()

        column.prop_with_label("Erase material", data.config_data, 'erase_material')
        column.separator()
        column.label(text = "Marker types")

        row = column.row()
        row.template_list("Material_UI_LIST", "", data.config_data, "marker_types", data.config_data, "marker_types_index")

        column = row.column()
        column.operator(list_operators.AddMarkerType.bl_idname, text="", icon='ADD')
        column.operator(list_operators.RemoveMarkerType.bl_idname, text="", icon='REMOVE')
        column.operator(list_operators.MoveMarkerTypeUp.bl_idname, text="", icon='TRIA_UP')
        column.operator(list_operators.MoveMarkerTypeDown.bl_idname, text="", icon='TRIA_DOWN')

class Material_UI_LIST(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(text=item.name)

class EditTileMarkerTypePanel(PanelInfo, bpy.types.Panel):
    bl_label = "Edit marker type"
    bl_idname = "VIEW3D_PT_edit_tile_marker_type"
    bl_parent_id = MaterialsPanel.bl_idname
    bl_order = 1

    def draw(self, context):
        layout = self.layout
        item = data.marker_types.get_active_item()
        
        if item is None:
            return
        
        layout.prop(item, 'name')
        layout.prop(item, 'gpencil_material')
        layout.prop(item, 'marker_material')

def prop_with_label(layout, name, prop, prop_name):
    row = layout.row()
    row.alignment = 'LEFT'
    row.label(text = name)
    row.prop(prop, prop_name, text = "")

bpy.types.UILayout.prop_with_label = prop_with_label