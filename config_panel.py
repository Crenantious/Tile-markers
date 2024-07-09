import bpy
import bpy.utils.previews
from . import edit_marker_type_operator as emt

icons = None
property_group = None

class ConfigPanel(bpy.types.Panel):
    bl_label = "Tile markers 1"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_idname = "A_PT_aaaaaaaaa"
    is_list_setup = False

    def __init__(self):
        if ConfigPanel.is_list_setup is False:
            ConfigPanel.is_list_setup = True
            #bpy.context.scene.demo_list.add()

    def draw(self, context):
        layout = self.layout
        #layout.popover(MaterialMenu.bl_idname, text="1")
        #layout.menu(MaterialMenu.bl_idname, text="2")
        #layout.menu_contents(MaterialMenu.bl_idname)
        #layout.label(icon_value=icons["test_icon"].icon_id)
        #layout.prop_with_menu(context.scene.property_group, 'material', menu=MaterialMenu.bl_idname)
        row = layout.row()
        row.template_list("Material_UI_LIST", "", context.scene, "demo_list", context.scene, "list_index")
        column = row.column()
        column.label(icon='ADD') # Make an operator
        column.label(icon='REMOVE') # Make an operator
        column.label(icon='TRIA_UP') # Make an operator
        column.label(icon='TRIA_DOWN') # Make an operator

class Material_UI_LIST(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        column = layout.column()
        rowOne = column.row()
        rowTwo = column.row()

        rowOne.label(text=item.name)
        op = rowOne.operator(emt.EditMarkerType.bl_idname, text="", icon='TRIA_DOWN')
        op.marker_type_index = index

        if item.edit_mode:
            box = rowTwo.split(factor=0.02)
            box.label()
            box = box.box()
            box.prop(item, 'material')

class MaterialPanel(bpy.types.Panel):
    bl_label = "Tile markers 2"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_idname = "D_PT_dddd"
    is_popover = True

    def draw(self, context):
        layout = self.layout
        layout.label(text='Stroke')
        layout.label(text='Marker')
        layout.prop(context.scene.property_group, 'material')

class MaterialMenu(bpy.types.Menu):
    bl_label = "Tile markers 3"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_idname = "D_MT_ddddaaaaa"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'EXEC_REGION_WIN'
        layout.label(text='Stroke')
        layout.label(text='Marker')
        layout.prop(context.scene.property_group, 'material')

# def do_update( self, context ):
#     if context.active_object:
#         context.active_object.location.x = self.someValue
#     print( 'update', self.someValue )

# def register():
#     bpy.types.Scene.someValue = bpy.props.FloatProperty(name = "Float", 
#         description = "Enter a float", min = -100, max = 100, update=do_update )
#     bpy.utils.register_class(SomePanel)

# def unregister():
#     bpy.utils.unregister_class(SomePanel)
#     del bpy.types.Scene.someValue