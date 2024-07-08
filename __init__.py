import bpy

from .main import TileMarkers
from .dynamic_property import *
from . import config_panel

bl_info = {
    "name": "Tile marker",
    "author": "Crenantious",
    "version": (1, 0),
    "blender": (3, 2, 0),
    "location": "View3D > Add > Mesh > Tile markers",
    "description": "Generates tile markers on an object based on the generated grease pencil.",
    "warning": "",
    "doc_url": "",
}


addon_keymaps = []

def register():
    load_icons()
    bpy.utils.register_class(config_panel.ConfigPropertyGroup)
    bpy.types.Scene.property_group = bpy.props.PointerProperty(type=config_panel.ConfigPropertyGroup)

    bpy.utils.register_class(TileMarkers)
    bpy.utils.register_class(config_panel.ConfigPanel)
    
    bpy.types.VIEW3D_MT_object.append(menu_func)
    register_keymaps()

def load_icons():
    config_panel.icons = bpy.utils.previews.new()
    config_panel.icons.load("test_icon", "Icon.png", 'IMAGE')

def register_keymaps():
    keymaps = bpy.context.window_manager.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
    items = keymaps.keymap_items.new(TileMarkers.bl_idname, 'F9', 'PRESS', ctrl=True, shift=True)
    items.active = True
    addon_keymaps.append((keymaps, items))


def unregister():
    if config_panel.icons is not None:
        bpy.utils.previews.remove(config_panel.icons)

    bpy.utils.unregister_class(TileMarkers)
    bpy.utils.unregister_class(config_panel.OptionsPanel)
    bpy.utils.unregister_class(config_panel.OptionsPropertyGroup)
    try:
        del bpy.types.Scene.property_group
    except:
        pass
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    unregister_keymaps()


def unregister_keymaps():
    for keymaps, items in addon_keymaps:
        keymaps.keymap_items.remove(items)
    addon_keymaps.clear()


def menu_func(self, context):
    self.layout.operator(TileMarkers.bl_idname, text="Add tile markers", icon='PLUGIN')