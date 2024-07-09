import bpy

from .main import TileMarkers
from .dynamic_property import *
from . import config_panel
from . import marker_type
from . import edit_marker_type_operator as emt

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

    bpy.utils.register_class(marker_type.MarkerType)
    bpy.types.Scene.property_group = bpy.props.PointerProperty(type=marker_type.MarkerType)

    bpy.types.Scene.demo_list = bpy.props.CollectionProperty(type = marker_type.MarkerType)
    bpy.types.Scene.list_index = bpy.props.IntProperty(name = "Index for demo_list", default = 0)

    bpy.utils.register_class(TileMarkers)
    bpy.utils.register_class(config_panel.MaterialPanel)
    bpy.utils.register_class(config_panel.Material_UI_LIST)
    bpy.utils.register_class(config_panel.MaterialMenu)
    bpy.utils.register_class(emt.EditMarkerType)
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
    bpy.utils.unregister_class(config_panel.ConfigPanel)
    bpy.utils.unregister_class(emt.EditMarkerType)
    bpy.utils.unregister_class(config_panel.MaterialPanel)
    bpy.utils.unregister_class(config_panel.MaterialMenu)
    bpy.utils.unregister_class(marker_type.MarkerType)
    bpy.utils.unregister_class(config_panel.Material_UI_LIST)
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