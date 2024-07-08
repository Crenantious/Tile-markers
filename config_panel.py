import bpy
import bpy.utils.previews

icons = None
property_group = None

class ConfigPanel(bpy.types.Panel):
    bl_label = "Tile markers"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        layout.label(icon_value=icons["test_icon"].icon_id)
        layout.prop(context.scene.property_group, 'material')

class ConfigPropertyGroup(bpy.types.PropertyGroup):
    material: bpy.props.PointerProperty(type=bpy.types.Material, name="Material")


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