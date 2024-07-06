import bpy

from .main import TileMarkers
from .dynamic_property import *

bl_info = {
    "name": "Tile marker",
    "author": "Crenantious",
    "version": (1, 0),
    "blender": (3, 2, 0),
    "location": "View3D > Add > Mesh > Tile markers",
    "description": "Generates tile markers on an object based on the generated grease pencil.",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}

addon_keymaps = []


def register():
    bpy.utils.register_class(TileMarkers)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    register_keymaps()


def register_keymaps():
    keymaps = bpy.context.window_manager.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
    items = keymaps.keymap_items.new(TileMarkers.bl_idname, 'F9', 'PRESS', ctrl=True, shift=True)
    items.active = True
    addon_keymaps.append((keymaps, items))


def unregister():
    bpy.utils.unregister_class(TileMarkers)
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    unregister_keymaps()


def unregister_keymaps():
    for keymaps, items in addon_keymaps:
        keymaps.keymap_items.remove(items)
    addon_keymaps.clear()


def menu_func(self, context):
    self.layout.operator(TileMarkers.bl_idname, text="Add tile markers", icon='PLUGIN')